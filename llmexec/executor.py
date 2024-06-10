import logging
import os
import subprocess
import sys
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Dict, Optional, List
from llmexec.utils import preprocess_code

import psutil
from bleach.sanitizer import Cleaner
from rich.console import Console
from rich.logging import RichHandler
from rich.panel import Panel
from rich.syntax import Syntax
from rich.live import Live

# Configure rich logging
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)]
)
logger = logging.getLogger("rich")

console = Console()

class ExecutionError(Exception):
    pass

class TimeoutError(Exception):
    pass

class MemoryError(Exception):
    pass

cleaner = Cleaner()

def sanitize_and_validate_output(output: str) -> str:
    """
    Sanitize and validate the output to prevent security risks.

    Args:
        output: The output to sanitize and validate.
    
    Returns:
        The sanitized and validated output.
    """
    return cleaner.clean(output.strip())

def check_memory_limit(memory_limit: int) -> float:
    """
    Check if the current memory usage exceeds the memory limit.

    Args:
        memory_limit: The maximum memory usage in bytes.
    
    Raises:
        MemoryError: If the memory usage exceeds the limit.
    """
    process = psutil.Process(os.getpid())
    memory_usage = process.memory_info().rss
    if memory_usage > memory_limit:
        raise MemoryError(f"Memory usage exceeded the limit: {memory_usage / (1024 * 1024):.2f} MB > {memory_limit / (1024 * 1024):.2f} MB")
    return memory_usage / (1024 * 1024)  # Return memory usage in MB

def validate_code(code: str) -> str:
    """
    Validate and sanitize the code to prevent invalid characters.

    Args:
        code: The code to validate and sanitize.

    Returns:
        The sanitized code.

    Raises:
        ExecutionError: If the code contains invalid characters.
    """
    if isinstance(code, bytes):
        code = code.decode(errors='ignore')
    # Remove null bytes and non-printable characters except line breaks
    sanitized_code = ''.join(char for char in code if char is not None and (char.isprintable() or char in ('\n', '\r')))
    return sanitized_code

def run_code_in_subprocess(code: str, globals_dict: Dict[str, Any], memory_limit: int, timeout: int) -> str:
    """
    Execute the code in a subprocess with a timeout to prevent abuse.

    Args:
        code: The code to execute.
        globals_dict: The dictionary of global variables for execution context.
        memory_limit: The maximum memory limit in bytes.
        timeout: The timeout in seconds. 0 indicates no timeout.

    Raises:
        MemoryError: If the memory usage exceeds the limit.
        TimeoutError: If the execution time exceeds the timeout.
    """
    with tempfile.NamedTemporaryFile('w', delete=False, suffix='.py') as temp_script:
        for var, value in globals_dict.items():
            temp_script.write(f"{var} = {repr(value)}\n")
        temp_script.write("\n")
        temp_script.write(code)
        temp_script_path = temp_script.name

    env = os.environ.copy()
    start_time = time.perf_counter()

    process = subprocess.Popen(
        [sys.executable, temp_script_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        env=env
    )

    try:
        stdout, stderr = process.communicate(timeout=timeout if timeout > 0 else None)
    except subprocess.TimeoutExpired:
        process.kill()
        raise TimeoutError(f"Execution timed out after {timeout} seconds.")

    os.remove(temp_script_path)

    if process.returncode != 0:
        raise ExecutionError(f"Error executing code:\n{stderr}")

    end_time = time.perf_counter()
    execution_time = end_time - start_time

    memory_usage = check_memory_limit(memory_limit)  # Get memory usage in MB

    return stdout.strip(), stderr.strip(), execution_time, memory_usage

def llmexec(
    code: str,
    globals: Optional[Dict[str, Any]] = None,
    locals: Optional[Dict[str, Any]] = None,
    timeout: int = 0,
    memory_limit: int = 100 * 1024 * 1024,  # 100 MB
    whitelisted_libraries: Optional[List[str]] = None,
    enable_logging: bool = True,
) -> Any:
    # Preprocess the code
    code = preprocess_code(code)

    if not code:
        raise ExecutionError("No valid Python code found in the input.")
    
    if globals is None:
        globals = {}
    if locals is None:
        locals = globals

    if whitelisted_libraries is None or '*' in whitelisted_libraries:
        whitelisted_libraries = ['*']

    globals_dict = globals  # Remove sandboxing for now

    code_str = validate_code(str(code))  # Ensure code is a string and validate it

    if enable_logging:
        syntax = Syntax(code_str, "python", theme="monokai", line_numbers=True)
        console.print(Panel(syntax, title="Executing Code"))

    with ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(run_code_in_subprocess, code_str, globals_dict, memory_limit, timeout)
        try:
            start_time = time.perf_counter()
            with Live(console=console, refresh_per_second=10) as live:
                while True:
                    if future.done():
                        try:
                            output, error, execution_time, memory_usage = future.result()
                        except TimeoutError as e:
                            status_panel = Panel(
                                f"Memory usage: {memory_usage:.2f} MB\nElapsed time: {timeout:.2f} seconds\nStatus: Timed Out",
                                title="Execution Status",
                                style="bold red"
                            )
                            live.update(status_panel)
                            console.print(Panel(str(e), title="Timeout Error", border_style="red"))
                            raise e
                        status = "Completed" if not error else "Failed"
                        status_panel = Panel(
                            f"Memory usage: {memory_usage:.2f} MB\nElapsed time: {execution_time:.2f} seconds\nStatus: {status}",
                            title="Execution Status",
                            style="bold green" if not error else "bold red"
                        )
                        live.update(status_panel)
                        if output:
                            console.print(Panel(output, title="Output", border_style="green"))
                        else:
                            console.print(Panel("No output produced.", border_style="yellow"))
                        if error:
                            console.print(Panel(error, title="Error", border_style="red"))
                        sanitized_output = sanitize_and_validate_output(output)
                        return globals.get('result', sanitized_output if sanitized_output else "Execution completed successfully.")
                    elapsed_time = time.perf_counter() - start_time
                    memory_usage = check_memory_limit(memory_limit)
                    live.update(Panel(
                        f"Memory usage: {memory_usage:.2f} MB\nElapsed time: {elapsed_time:.2f} seconds\nStatus: In progress",
                        title="Execution Status",
                        style="bold blue"
                    ))
                    time.sleep(0.1)
        except (MemoryError, ExecutionError) as e:
            raise e
        except Exception as e:
            raise ExecutionError(f"Unexpected error during execution: {e}") from e