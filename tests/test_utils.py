# test_llm_utils.py

import unittest
from llmexec.utils import preprocess_code

class TestPreprocessCode(unittest.TestCase):
    def test_valid_python_code(self):
        code = "print('Hello, World!')"
        expected_output = "print('Hello, World!')"
        self.assertEqual(preprocess_code(code), expected_output)

    def test_code_with_python_tag_and_backticks(self):
        code = "```python\nprint('Hello, World!')\n```"
        expected_output = "print('Hello, World!')"
        self.assertEqual(preprocess_code(code), expected_output)

    def test_code_with_backticks_only(self):
        code = "```\nprint('Hello, World!')\n```"
        expected_output = "print('Hello, World!')"
        self.assertEqual(preprocess_code(code), expected_output)

    def test_code_with_python_tag_without_backticks(self):
        code = "python\nprint('Hello, World!')"
        expected_output = "print('Hello, World!')"
        self.assertEqual(preprocess_code(code), expected_output)

    def test_code_without_tag_and_backticks(self):
        code = "print('Hello, World!')"
        expected_output = "print('Hello, World!')"
        self.assertEqual(preprocess_code(code), expected_output)

    def test_code_with_leading_description(self):
        code = "Here is the code to print 'Hello, World!':\n```python\nprint('Hello, World!')\n```"
        expected_output = "print('Hello, World!')"
        self.assertEqual(preprocess_code(code), expected_output)

    def test_code_with_trailing_description(self):
        code = "```python\nprint('Hello, World!')\n```\nThis code prints 'Hello, World!'"
        expected_output = "print('Hello, World!')"
        self.assertEqual(preprocess_code(code), expected_output)

    def test_code_with_leading_and_trailing_description(self):
        code = "Here is the code to print 'Hello, World!':\n```python\nprint('Hello, World!')\n```\nThis code prints 'Hello, World!'"
        expected_output = "print('Hello, World!')"
        self.assertEqual(preprocess_code(code), expected_output)

    def test_code_with_invalid_format(self):
        code = "This is not a valid Python code format."
        expected_output = ""
        self.assertEqual(preprocess_code(code), expected_output)

    def test_empty_code(self):
        code = ""
        expected_output = ""
        self.assertEqual(preprocess_code(code), expected_output)

    def test_code_with_leading_and_trailing_whitespace(self):
        code = "   ```python\nprint('Hello, World!')\n```   "
        expected_output = "print('Hello, World!')"
        self.assertEqual(preprocess_code(code), expected_output)

if __name__ == '__main__':
    unittest.main()