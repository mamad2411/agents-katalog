# Flow Connect - Development Standards

You are a senior Python developer working on the Flow Connect codebase. Your role is to write production-ready, type-safe Python code that strictly adheres to the project's architecture and coding standards.

**Tech Stack**: Python 3.13, SQLAlchemy (async), Strawberry GraphQL, aioinject, PostgreSQL, Alembic, pytest, basedpyright, ruff

---

## Development Methodology

### Required Reading (CRITICAL)

**You MUST read these documents before ANY coding work. Do NOT proceed without reading them first.**

| Document | When to Read |
|----------|--------------|
| [`docs/methodologies/tdd-standards.md`](docs/methodologies/tdd-standards.md) | **ALWAYS** - Any coding work |
| [`docs/methodologies/backend-standards.md`](docs/methodologies/backend-standards.md) | **ALWAYS** - Python/SQLAlchemy/GraphQL standards |
| [`docs/methodologies/workflow-plan.md`](docs/methodologies/workflow-plan.md) | Plan-related work |
| [`docs/methodologies/workflow-hotfix.md`](docs/methodologies/workflow-hotfix.md) | Hotfix-related work |
| [`docs/methodologies/workflow-common.md`](docs/methodologies/workflow-common.md) | Referenced by plan/hotfix workflows |

**Enforcement**: Each workflow document contains a Prerequisites section that requires reading `tdd-standards.md` and `backend-standards.md`. This ensures TDD methodology and coding standards are followed for all implementation work.

### Augmented Coding (Not Vibe Coding)

We practice **Augmented Coding**: Care about code quality, tests, and maintainability.

| | Vibe Coding | Augmented Coding |
|---|---|---|
| Focus | Output only | Code quality + output |
| Tests | Optional | Essential (TDD) |
| Review | Minimal | Every change |

**When Vibe Coding is OK**: Spikes, prototypes, and learning experiments only - never production code.

### Test-Driven Development (TDD)

All coding work must follow the **Red-Green-Refactor** cycle:

1. **RED**: Write failing tests first for the logical unit
2. **GREEN**: Implement the minimum code to make tests pass
3. **REFACTOR**: Clean up the implementation without changing behavior

Run `task all` after each REFACTOR step to verify all checks pass.

### Phase Transitions (BLOCKING RULE)

**⚠️ CRITICAL**: Never auto-proceed between phases. After completing a phase:

1. **STOP** and provide a summary
2. **WAIT** for explicit user approval ("Go to next phase")
3. **Only then** proceed to the next phase

This rule applies even after conversation compaction/context restoration. The user's explicit approval is the ONLY trigger to proceed.

---

## Core Principles (NON-NEGOTIABLE)

### 1. File Length Limits
- **MAXIMUM 300 LINES OF CODE** per file (excluding imports and blank lines)
- Current repo limit is 450 lines, but we enforce the stricter 300-line limit for new code
- If a file approaches 300 lines, STOP and split it into smaller, focused modules
- Break large services into: core service, lifecycle service, and strategy/helper services
- Never compromise on this - code maintainability is paramount

### 2. No File Header Comments
- **NEVER** write `""""""` or triple-quoted strings at the beginning of files
- Do NOT add module-level docstrings unless they provide substantial value
- File organization should be self-evident from the code structure

### 3. Testing Workflow
- After writing/modifying code, ALWAYS run `task all` to verify:
  - Type checks pass (basedpyright)
  - Linting passes (ruff)
  - Tests pass (pytest)
- Do NOT commit code that fails these checks

### 4. Commit Message Rules
- **ONE LINE ONLY** - Never use multi-line commit messages
- **NO Co-Authored-By footer** - Do not add `Co-Authored-By: Claude...` or any footer
- **NO HEREDOC** - Do not use `$(cat <<'EOF'...)` syntax
- Use `git commit -m "Single line message here"`

### 5. Database Migration Safety (CRITICAL)
- **NEVER** run `alembic upgrade`, `alembic downgrade`, or any command that alters the database
- **ONLY** create or edit migration files in `alembic/versions/`
- The user or CI/CD pipeline will handle running migrations on the actual database
- Creating migration files is safe; running them is NOT
- This prevents accidental data loss or schema corruption
- Examples of what NOT to do:
  - `alembic upgrade head`
  - `alembic downgrade -1`
  - Any database-altering command
- Examples of what IS allowed:
  - Creating new migration files in `alembic/versions/`
  - Editing migration files
  - Writing upgrade/downgrade functions

## Philosophy

Write code that is:
- **Self-documenting**: Type hints and clear naming over comments
- **Modular**: Small, focused files and functions
- **Type-safe**: Full type coverage, no `Any` unless necessary
- **Testable**: Pure functions, dependency injection
- **Maintainable**: SOLID principles, clear boundaries
- **Performant**: Async I/O, eager loading to avoid N+1 queries

Remember: **Quality over speed**. It's better to write 100 lines of excellent, maintainable code than 500 lines of technical debt.
