# GitHub Copilot Instructions

These instructions guide GitHub Copilot to generate consistent, idiomatic code for this Python project.

## 🧪 Tests

- Use **pytest**.
- Follow the **GIVEN / WHEN / THEN** structure in all tests.
- Use `assert` statements for validation.
- Group related setup under `# GIVEN`.
- The action being tested goes under `# WHEN`.
- Assertions and expectations go under `# THEN`.
- **Always place imports inside test functions** — this ensures proper load order and test isolation.

### Example:

```
def test_user_creation():
    # GIVEN
    #     a user data payload
    from myapp.users import create_user
    user_data = {"name": "Alice", "email": "alice@example.com"}

    # WHEN
    #     we create the user
    user = create_user(user_data)

    # THEN
    #     the user is stored with correct attributes
    assert user.name == "Alice"
    assert user.email == "alice@example.com"
```

## 📦 Project Structure

- Source code lives in the `src/` directory.
- Tests live in the `tests/` directory, mirroring the source layout.

## ✅ Style & Linting

- Follow [PEP8](https://peps.python.org/pep-0008/).
- Linting is enforced by **Ruff**.
- Do **not** use `assert` in production code — raise exceptions instead.

## 🧩 Type Hints

- The project **must be fully typed**.
- Use Python type hints (`str`, `int`, `Optional[...]`, etc.) in all functions, classes, and variables where applicable.
- All public APIs must have complete type annotations.
- Use `mypy` to enforce type checking.

## 💡 Docstrings

- Use [Google-style docstrings](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings) for all public functions, methods, and classes.
