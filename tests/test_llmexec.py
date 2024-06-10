# test_llmexec.py

import os
import tempfile
import unittest
from unittest.mock import patch
from llmexec import llmexec, ExecutionError, TimeoutError, MemoryError
import math

class LLMExecTestCase(unittest.TestCase):
    def test_simple_arithmetic_operation(self):
        code = "result = x + y\nprint(result)"
        globals = {'x': 10, 'y': 20}
        result = llmexec(code, globals)
        self.assertEqual(result, "30")

    def test_code_with_syntax_error(self):
        code = "result = x + y\nprint(result"  # Missing closing parenthesis
        globals = {'x': 10, 'y': 20}
        with self.assertRaises(ExecutionError):
            llmexec(code, globals)

    def test_code_with_runtime_error(self):
        code = "result = x / 0"  # Division by zero
        globals = {'x': 10}
        with self.assertRaises(ExecutionError):
            llmexec(code, globals)

    def test_code_with_infinite_loop(self):
        code = "while True: pass"
        with self.assertRaises(TimeoutError):
            llmexec(code, timeout=1)

    def test_code_with_memory_limit_exceeded(self):
        code = "large_list = [0] * (10 ** 7)"  # Allocate large memory
        with self.assertRaises(MemoryError):
            llmexec(code, memory_limit=10 * 1024 * 1024)  # 10 MB memory limit

    def test_code_with_imported_module(self):
        code = "import math\nresult = math.pi"
        result = llmexec(code)
        self.assertEqual(result, str(math.pi))

    def test_code_with_file_write(self):
        code = "with open('test.txt', 'w') as file:\n    file.write('Hello, World!')"
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, 'test.txt')
            llmexec(code, globals={'file_path': file_path})
            self.assertTrue(os.path.exists(file_path))
            with open(file_path, 'r') as file:
                content = file.read()
                self.assertEqual(content, 'Hello, World!')

    def test_code_with_invalid_characters(self):
        code = "result = 'Hello\0World'"  # Null byte in the code
        with self.assertRaises(ExecutionError):
            llmexec(code)

    def test_code_with_whitelisted_libraries(self):
        code = "import numpy as np\nresult = np.array([1, 2, 3])"
        result = llmexec(code, whitelisted_libraries=['numpy'])
        self.assertEqual(result, "[1 2 3]")

    def test_code_with_non_whitelisted_library(self):
        code = "import requests"
        with self.assertRaises(ImportError):
            llmexec(code, whitelisted_libraries=['numpy'])

    def test_code_with_dynamic_memory_usage(self):
        code = """
        import numpy as np
        large_array = np.random.rand(1000, 1000, 100)
        result = np.sum(large_array)
        """
        result = llmexec(code)
        self.assertIsInstance(float(result), float)

    def test_code_with_matplotlib(self):
        code = """
        import matplotlib.pyplot as plt
        plt.plot([1, 2, 3], [4, 5, 6])
        plt.title('Example Chart')
        plt.xlabel('X-axis')
        plt.ylabel('Y-axis')
        """
        with patch('matplotlib.pyplot.show') as mock_show:
            llmexec(code)
            mock_show.assert_called_once()

    def test_code_with_no_output(self):
        code = "x = 10"
        result = llmexec(code)
        self.assertEqual(result, "Execution completed successfully.")

    def test_code_with_bytes_input(self):
        code = b"result = 'Hello, World!'"
        result = llmexec(code)
        self.assertEqual(result, "Hello, World!")

    def test_code_with_non_existent_global_variable(self):
        code = "result = non_existent_var"
        with self.assertRaises(ExecutionError):
            llmexec(code)

    def test_code_with_large_output(self):
        code = "result = 'A' * 1000000"  # 1 MB output
        result = llmexec(code)
        self.assertEqual(len(result), 1000000)

    def test_code_with_logging_disabled(self):
        code = "result = 'Hello, World!'"
        result = llmexec(code, enable_logging=False)
        self.assertEqual(result, "Hello, World!")

if __name__ == '__main__':
    unittest.main()