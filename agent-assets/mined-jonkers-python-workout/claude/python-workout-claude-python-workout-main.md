# Project: Python Workout

## Project Description
This directory holds solutions to a variety of exercises set out in Manning's Python Workout book (https://www.manning.com/books/python-workout-second-edition).

I am using this project to refresh my Python skills, starting from foundations and building out to more sophisticated Python features.

Primarily, I would like you to review my work and suggest improvements to make my Python code more idiomatic.

I'd also like to refresh my testing experience too, so I would appreciate guidance on how to introduce and write good tests for each project (from unit tests to higher-level tests, as appropriate).

**Important:** Do not suggest implementations unless I explicitly request it. I want to practice writing the code myself.

The author has published their solutions in a project on GitHub, but I think these are for the first edition of the book: https://github.com/reuven/python-workout. I think the chapter numbers are off by one: chapter two in the new edition is chapter one in the first edition.

## Project Structure

This directory holds directories for each chapter of the book.

Within those directories, there are subdirectories for each of the Python exercises.

Each exercise follows this file structure:
```
ch_N/exM_name/
├── main.py           # Implementation
├── test_*.py         # Unit tests
├── pyproject.toml    # Exercise dependencies
└── CLAUDE.md         # Exercise requirements and notes
```

## Tech stack
- Python 3.12 or later.
- Pytest for unit testing.
- uv for Python dependency and environment management.

## Running Tests
Run all tests from the project root:
```bash
uv run pytest
```

Or run tests for a specific exercise:
```bash
uv run pytest ch_2/ex1_guessing_game
```

## Running Type Checks
Run mypy from the project root to verify type hints:
```bash
uv run mypy ch_2 ch_3 ch_4 ch_5 ch_6 ch_7 ch_8 ch_9 ch_10
```

Or check a specific exercise:
```bash
uv run mypy ch_4/ex13_printing_tuple_records/main.py
```

Mypy is configured in strict mode (see `pyproject.toml`).

## Future Tool Suggestions

- **pytest-cov** — Coverage reporting to identify untested code paths.
- **ruff** — Fast linter that catches PEP8 issues and common bugs automatically.
