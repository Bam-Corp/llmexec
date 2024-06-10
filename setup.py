from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name="llmexec",
    version="0.1.0",
    author="Bam Corp",
    author_email="spencer@bam.bot",
    description="Execute LLM-Generated Python Code Automatically",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Bam-Corp/llmexec",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    keywords="llmexec, code execution, ai-generated code",
    install_requires=[
        "RestrictedPython",
        "rich",
        "bleach",
        "psutil",
    ],
    python_requires='>=3.7',
    project_urls={
        "Bug Tracker": "https://github.com/Bam-Corp/llmexec/issues",
        "Source Code": "https://github.com/Bam-Corp/llmexec",
    },
)