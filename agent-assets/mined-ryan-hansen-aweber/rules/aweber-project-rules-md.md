---
description:
globs:
alwaysApply: true
---
# General Rules

- Use Python with FastAPI for this project.
- Handle only one TaskMaster task or subtask at a time.
- Ask before proceeding to the next task.
- Include an OpenAPI spec (should be automatically provided with FastAPI)
- Ensure PEP8 compliance.
- The code should pass standard lint tests (eg: flake8 or similar).
- The code should pass bandit security analysis.
- Use Python type annotations.
- There is a Python 3.12 virtual environment in aweberenv.  Activate that before running any Python commands.

- For each TaskMaster task or subtask, do the following:
  1. First create an appropriate feature branch.
  2. Create a suite of automated tests (unit or functional) for that task.
  3. A task/subtask is not complete until all relevant tests are passing.
  4. Mark the related tasks and subtasks as complete.
  5. Commit the changes.
