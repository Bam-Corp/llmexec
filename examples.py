from llmexec import llmexec


# Example 1: Simple Arithmetic Operation
code = "result = x + y\nprint(result)"
globals = {'x': 10, 'y': 20}
result = llmexec(code, globals)
print(result)  # Outputs: 30

# Example 2: Running LLM-generated python code
llm_output = """Here is an example of Python code that generates a chart with random data using the matplotlib library:

```python
import matplotlib.pyplot as plt
import numpy as np

# Generate random data
x = np.random.rand(10)  # 10 random x-values between 0 and 1
y = np.random.rand(10)  # 10 random y-values between 0 and 1

# Create a figure and axis object
fig, ax = plt.subplots()

# Plot the data
ax.scatter(x, y)

# Add labels and title
ax.set_xlabel('X-axis')
ax.set_ylabel('Y-axis')
ax.set_title('Random Data Plot')

# Display the plot
plt.show()
```
"""

# Execute the LLM-generated code
llmexec(llm_output)