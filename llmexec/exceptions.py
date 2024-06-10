class ExecutionError(Exception):
    """Custom exception for execution errors."""
    pass


class TimeoutError(ExecutionError):
    """Custom exception for timeout errors."""
    pass


class MemoryError(ExecutionError):
    """Custom exception for memory errors."""
    pass
