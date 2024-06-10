# llmexec: Execute LLM-Generated Python Code

`llmexec` is a Python library that allows you to automatically execute python code snippets generated by large language models (LLMs). It's useful for projects that require automated code generation and execution and is a drop-in replacement for the python `exec()` function.

## Installation

```bash
pip install llmexec
```

## Usage

```python
from llmexec import llmexec

# LLM-generated code
llm_output = """
# Generate random data plot using matplotlib
import matplotlib.pyplot as plt
import numpy as np

x = np.random.rand(10)  # 10 random x values
y = np.random.rand(10)  # 10 random y values

fig, ax = plt.subplots()
ax.scatter(x, y)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_title('Random Data Plot')
plt.show()
"""

# Execute the LLM-generated code
llmexec(llm_output)
```

`llmexec` will automatically parse and execute the LLM-generated code snippet, displaying a random data plot using `matplotlib`.

## Features

- Automatically execute LLM-generated code snippets
- Parses out code from LLM outputs
- Trusted execution environment using `restrictedpython`
- Detailed logs and execution status
- Timeout and memory limits to prevent abuse

## License

[MIT License](https://github.com/your-username/llmexec/blob/main/LICENSE)