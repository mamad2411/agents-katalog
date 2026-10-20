---
name: Python Standards
globs: "*.py, **/*.py"
alwaysApply: true
---

# Pyhton coding assistant

You are a Python coding assistant. You use the following tools:

- Python 3 as the primary programming language
- Use type hints consistently
- Optimize for readability over premature optimization
- Write modular code, using separate files for models, data loading, training, and evaluation
- Follow PEP8 style guide for Python code
- Uv for environment and package management

## When using FastAPI
- Follow FastAPI patterns
- Ensure to use RESTful API design practices
- Use FastAPI's built-in error handling and middleware features
- Use FastAPI's built-in authentication and authorization features
- Avoid using global state

## Make proactive use of modern libraries

- Use native Libraries for calling LLMs for simple cases.
- Use frameworks such as LangChain, Crew.ai, Autogen for more complex orchestration.
- PyTorch for deep learning and neural networks
- NumPy for numerical computing and array operations
- Pandas for data manipulation and analysis
- Jupyter for interactive development and visualization
- Other such as pydantic, pytest, uvicorn, fastapi, flask, python-dotenv.