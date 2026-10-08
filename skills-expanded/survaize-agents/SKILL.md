# AGENT Instructions

## Overview
- The main project code lives under `src/survaize`.
- Unit tests are in `tests/` and evaluation scripts/data in `evals/`.
- Development utilities such as lint scripts are under `devtools/`.
- Documentation is primarily in `README.md`, `development.md`, and `installation.md`.

When adding or modifying code, keep files within these directories. Any new source
files should go under `src/survaize` or a suitable subpackage.

## Contribution Guidelines
- Follow the coding standards from `.github/copilot-instructions.md`:
  1. Use explicit type annotations on all function parameters and return values.
  2. Choose descriptive names for functions and variables.
  3. Keep each function focused on a single responsibility.
  4. Provide docstrings for public functions and classes.
  5. Prefer immutable data structures; use `@dataclass` for simple containers and
     Pydantic models for complex validation.
  6. Aim for pure functions with minimal side effects.
  7. Use the `logging` library with `logging.getLogger(__name__)` for logging.
  8. Only comment code that is hard to understand—avoid redundant comments.
  9. Prefix private class methods with `_`.
  10. Place all imports at the top of the file.

## Development Workflow
1. Install dependencies and create the virtual environment using `uv`:
   ```bash
   uv sync --all-extras --dev
   ```
2. Run the application locally:
   ```bash
   uv run survaize
   ```
3. Run lint checks (codespell, ruff formatting, ruff lint, type checking):
   ```bash
   uv run python devtools/lint.py
   ```
   Alternatively you can run `uv run ruff check` for a quick lint pass.
4. Execute unit tests:
   ```bash
   uv run pytest
   ```
5. Optional type checking on its own:
   ```bash
   uv run basedpyright
   ```
6. For frontend development, navigate to the `web/frontend` directory and run:
   ```bash
   npm install
   npm run dev
   ```
7. To build the frontend assets for production:
   ```bash
   npm run build
   ```
8. To run the frontend tests:
   ```bash
   npm run test
   ```
9. To run the frontend linter:
   ```bash
   npm run lint
   ```
10. To format the frontend code:
    ```bash
    npm run format
    ```

## Working Approach
- When updating or adding features, consult the architecture overview in
  `.github/copilot-instructions.md` for context about core components.
- Keep documentation up to date when you change public behavior.
- Follow the style rules above and ensure `uv run python devtools/lint.py` and
  `uv run pytest` succeed before committing for backend code and `npm run format`,
   `npm run lint` and `npm test` succeed for frontend code.

## Pull Requests
- Include a summary of the changes and how they were tested.
- Provide citations to relevant lines of code or documentation when referencing
  specific sections in the PR description.
