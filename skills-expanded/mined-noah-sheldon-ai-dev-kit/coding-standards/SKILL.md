---
name: coding-standards
description: Project-wide coding standards enforcement: naming conventions, file organization, function size limits, complexity budgets, style guides, linting rules, code review standards, and language-specific conventions for Python and TypeScript. Includes linter configs and rules.
origin: AI Dev Kit
disable-model-invocation: false
---

# Coding Standards

Enforceable project-wide coding standards: naming conventions, file organization, function size limits, cyclomatic complexity budgets, linting rules, code review checklists, and language-specific conventions for Python and TypeScript. Includes ready-to-use linter configurations.

## When to Use

- Setting up a new project's linting and formatting toolchain
- Defining or updating team coding standards
- Reviewing code for compliance with conventions
- Onboarding new developers to the project's style guide
- Refactoring legacy code to meet modern standards
- Configuring pre-commit hooks and CI quality gates

## Core Concepts

### 1. Standards Hierarchy

```
┌─────────────────────────────────────────┐
│           ORGANIZATION LEVEL            │
│  Language standards (PEP 8, TypeScript  │
│  ESLint recommended, etc.)              │
├─────────────────────────────────────────┤
│           PROJECT LEVEL                 │
│  Naming conventions, file organization, │
│  complexity budgets, import ordering    │
├─────────────────────────────────────────┤
│           MODULE LEVEL                  │
│  Module responsibility, public API,     │
│  documentation requirements             │
├─────────────────────────────────────────┤
│           FUNCTION LEVEL                │
│  Size limits, parameter count,          │
│  cyclomatic complexity, return types    │
└─────────────────────────────────────────┘
```

### 2. Naming Conventions

**Python:**

```python
# Variables and functions: snake_case
user_count = 0
def calculate_total_price(items: list[Item], tax_rate: float) -> Decimal: ...

# Classes: PascalCase
class UserProfileService: ...
class DatabaseConnectionError(Exception): ...

# Constants: UPPER_SNAKE_CASE
MAX_RETRY_COUNT = 3
DEFAULT_PAGE_SIZE = 20
API_BASE_URL = "https://api.example.com"

# Private members: leading underscore
class UserService:
    def __init__(self):
        self._cache: dict = {}
        self._connection_pool: ConnectionPool | None = None

    def _build_query(self, filters: dict) -> str:  # Internal method
        ...

# Type aliases: PascalCase
UserId = str
EmailStr = Annotated[str, ...]

# Test functions: test_ prefix with descriptive name
def test_rejects_missing_email_field(self): ...
def test_returns_404_when_user_not_found(self): ...
```

**TypeScript:**

```typescript
// Variables: camelCase
const userCount = 0;
let isActive = true;

// Functions: camelCase
async function calculateTotalPrice(items: Item[], taxRate: number): Promise<Decimal> { ... }

// Classes/Interfaces/Types: PascalCase
class UserProfileService { ... }
interface UserCreateRequest { ... }
type ApiResponse<T> = { data: T; error?: string };

// Constants: UPPER_SNAKE_CASE
const MAX_RETRY_COUNT = 3;
const DEFAULT_PAGE_SIZE = 20;

// Private fields: # prefix (ES2022) or leading underscore
class UserService {
  #cache = new Map<string, User>();       // Private (ES2022)
  private _connection: Connection | null;  // Private (TypeScript)
}

// Enums: PascalCase for name, UPPER_SNAKE_CASE for values
enum UserRole {
  ADMIN = "ADMIN",
  USER = "USER",
  VIEWER = "VIEWER",
}

// React components: PascalCase
function UserTable({ users }: UserTableProps) { ... }

// Custom hooks: use prefix
function useDebounce<T>(value: T, delayMs: number): T { ... }

// Test descriptions: human-readable strings
it("rejects requests with missing email field", async () => { ... });
it("returns 404 when user is not found in database", async () => { ... });
```

### 3. File Organization

**Python — Module Structure:**

```python
"""One-line module description.

Longer description if needed. Explains what this module does,
its responsibilities, and any important design decisions.
"""

# 1. Stdlib imports (alphabetical)
from __future__ import annotations
import logging
import os
from typing import Any

# 2. Third-party imports (alphabetical)
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

# 3. Local imports (alphabetical)
from app.db import get_session
from app.models.user import User
from app.services.auth import require_admin

# Constants
logger = logging.getLogger(__name__)
router = APIRouter(prefix="/users", tags=["users"])

# Classes
class UserCreate(BaseModel):
    """Request schema for creating a user."""
    name: str
    email: str


# Functions (public API)
@router.post("/", status_code=201)
async def create_user(data: UserCreate, admin=Depends(require_admin)):
    """Create a new user. Requires admin role."""
    ...

# Internal functions (leading underscore)
def _validate_email(email: str) -> str:
    """Internal email validation."""
    ...
```

**TypeScript — File Structure:**

```typescript
// 1. Type imports (alphabetical)
import type { Request, Response } from "express";
import type { User } from "../models/user";

// 2. Runtime imports (alphabetical)
import { z } from "zod";
import { requireAuth } from "../middleware/auth";

// 3. Local imports (alphabetical)
import { UserService } from "../services/user-service";
import { logger } from "../lib/logger";

// Constants
const userService = new UserService();

// Schemas (if applicable)
const createUserSchema = z.object({
  name: z.string().min(1).max(150),
  email: z.string().email(),
});
type CreateUserInput = z.infer<typeof createUserSchema>;

// Classes / Functions (exported)
export async function createUserHandler(req: Request, res: Response): Promise<void> {
  // Implementation
}

// Internal helpers (not exported)
function validateEmail(email: string): boolean {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}
```

### 4. Function and Complexity Budgets

| Metric | Limit | Action if Exceeded |
|---|---|---|
| Function length | 50 lines | Extract helper functions |
| File length | 300 lines | Split into multiple modules |
| Parameters per function | 4 (use objects/DTOs beyond) | Group into a data class or interface |
| Cyclomatic complexity | 10 per function | Decompose conditionals |
| Nesting depth | 3 levels | Extract early returns or guard clauses |
| Lines per class | 200 lines | Split by responsibility |
| Import count per file | 15 | Check for feature envy, extract module |

**Guard Clauses Over Nested Conditionals:**

```python
# BAD — deep nesting
def process_order(order):
    if order.is_active:
        if order.has_items:
            if order.payment_verified:
                if order.stock_available:
                    return ship_order(order)
                else:
                    return "No stock"
            else:
                return "Payment pending"
        else:
            return "Empty order"
    else:
        return "Order inactive"


# GOOD — guard clauses
def process_order(order):
    if not order.is_active:
        return "Order inactive"
    if not order.has_items:
        return "Empty order"
    if not order.payment_verified:
        return "Payment pending"
    if not order.stock_available:
        return "No stock"
    return ship_order(order)
```

### 5. Linting Configuration

**Python — Ruff (replaces flake8, isort, pyupgrade):**

```toml
# pyproject.toml
[tool.ruff]
line-length = 100
target-version = "py312"
src = ["src", "tests"]

[tool.ruff.lint]
select = [
    "E",      # pycodestyle errors
    "W",      # pycodestyle warnings
    "F",      # Pyflakes
    "I",      # isort (import sorting)
    "N",      # pep8-naming
    "UP",     # pyupgrade
    "B",      # flake8-bugbear
    "SIM",    # flake8-simplify
    "C4",     # flake8-comprehensions
    "RET",    # flake8-return
    "RUF",    # Ruff-specific rules
    "PTH",    # flake8-use-pathlib
    "FA",     # flake8-future-annotations
    "TCH",    # flake8-type-checking
    "PL",     # Pylint rules (subset)
    "TRY",    # flake8-try-except-raise
    "PERF",   # Perflint
    "FURB",   # Refurb
    "LOG",    # flake8-logging
]

ignore = [
    "E501",     # Line too long (handled by formatter)
    "PLR0913",  # Too many arguments (manual review)
    "PLR2004",  # Magic value comparison (too noisy)
    "TRY003",   # Avoid specifying long messages (subjective)
]

[tool.ruff.lint.isort]
known-first-party = ["app", "tests"]
split-on-trailing-comment-type = true

[tool.ruff.lint.per-file-ignores]
"tests/**" = ["S101", "PLR2004", "ARG"]  # Allow assert, magic numbers in tests
"__init__.py" = ["F401"]                   # Allow unused imports in __init__

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
skip-magic-trailing-comma = false
line-ending = "lf"
```

**Python — mypy (type checking):**

```toml
# pyproject.toml
[tool.mypy]
python_version = "3.12"
strict = true
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
disallow_untyped_decorators = true
no_implicit_optional = true
warn_redundant_casts = true
warn_unused_ignores = true
warn_unreachable = true

# Per-module overrides
[[tool.mypy.overrides]]
module = ["tests.*"]
disallow_untyped_defs = false  # Tests don't always need full types
```

**TypeScript — ESLint with TypeScript:**

```js
// eslint.config.js
import js from "@eslint/js";
import tseslint from "typescript-eslint";
import reactPlugin from "eslint-plugin-react";
import reactHooksPlugin from "eslint-plugin-react-hooks";
import importPlugin from "eslint-plugin-import";

export default tseslint.config(
  js.configs.recommended,
  ...tseslint.configs.strictTypeChecked,
  ...tseslint.configs.stylisticTypeChecked,
  {
    languageOptions: {
      parserOptions: {
        project: true,
        tsconfigRootDir: import.meta.dirname,
      },
    },
    plugins: {
      import: importPlugin,
      react: reactPlugin,
      "react-hooks": reactHooksPlugin,
    },
    rules: {
      // --- Correctness ---
      "no-unused-vars": "off",  // Use TypeScript's version
      "@typescript-eslint/no-unused-vars": [
        "warn",
        { argsIgnorePattern: "^_", varsIgnorePattern: "^_" },
      ],
      "@typescript-eslint/no-misused-promises": [
        "error",
        { checksVoidReturn: { attributes: false } },
      ],
      "@typescript-eslint/no-floating-promises": "error",
      "@typescript-eslint/await-thenable": "error",
      "@typescript-eslint/no-explicit-any": "warn",
      "@typescript-eslint/no-non-null-assertion": "warn",

      // --- Style ---
      "@typescript-eslint/consistent-type-imports": [
        "error",
        { prefer: "type-imports", fixStyle: "inline-type-imports" },
      ],
      "@typescript-eslint/consistent-type-exports": "error",
      "@typescript-eslint/no-import-type-side-effects": "error",
      "import/order": [
        "error",
        {
          groups: ["builtin", "external", "internal", "parent", "sibling", "index"],
          "newlines-between": "always",
          alphabetize: { order: "asc", caseInsensitive: true },
        },
      ],

      // --- Complexity ---
      complexity: ["warn", 10],
      "max-depth": ["warn", 3],
      "max-lines-per-function": ["warn", { max: 50, skipComments: true }],

      // --- React ---
      ...reactPlugin.configs["jsx-runtime"].rules,
      ...reactHooksPlugin.configs.recommended.rules,
      "react/react-in-jsx-scope": "off",
    },
  },
  {
    ignores: ["node_modules", "dist", "build", ".next", "coverage"],
  },
);
```

**TypeScript — tsconfig.json (strict):**

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "lib": ["ES2022", "DOM", "DOM.Iterable"],
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitOverride": true,
    "noPropertyAccessFromIndexSignature": true,
    "exactOptionalPropertyTypes": true,
    "forceConsistentCasingInFileNames": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "resolveJsonModule": true,
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,
    "outDir": "dist",
    "rootDir": "src",
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"]
    }
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist", "**/*.test.ts", "**/*.spec.ts"]
}
```

### 6. Pre-Commit Hook

```yaml
# .pre-commit-config.yaml
repos:
  # Formatters
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.4.0
    hooks:
      - id: ruff        # Linting
        args: [--fix]
      - id: ruff-format # Formatting

  - repo: https://github.com/pre-commit/mirrors-prettier
    rev: v4.0.0
    hooks:
      - id: prettier
        types_or: [typescript, javascript, css, json, markdown]

  # Type checkers
  - repo: local
    hooks:
      - id: mypy
        name: mypy
        entry: mypy
        language: system
        types: [python]
        pass_filenames: false
        args: ["src", "tests"]

      - id: tsc
        name: TypeScript type check
        entry: npx tsc --noEmit
        language: system
        types: [typescript]
        pass_filenames: false

  # Security
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.18.0
    hooks:
      - id: gitleaks

  # Quality gates
  - repo: local
    hooks:
      - id: pytest-smoke
        name: pytest smoke tests
        entry: pytest tests/ -m smoke --tb=short -q
        language: system
        types: [python]
        pass_filenames: false
```

### 7. Code Review Checklist

Every PR should be checked against these criteria:

**Correctness:**
- [ ] Logic is correct for the stated requirements
- [ ] Edge cases handled (null, empty, boundary, concurrent)
- [ ] Error paths handled (no silent failures)
- [ ] No race conditions or unhandled promises

**Security:**
- [ ] No hardcoded secrets, API keys, or credentials
- [ ] User inputs validated at boundaries
- [ ] No SQL injection or shell injection risks
- [ ] Authentication and authorization enforced

**Maintainability:**
- [ ] Function size ≤ 50 lines
- [ ] File size ≤ 300 lines
- [ ] Cyclomatic complexity ≤ 10
- [ ] Meaningful variable and function names
- [ ] No magic numbers or strings (use named constants)
- [ ] No commented-out code
- [ ] No TODOs without issue references

**Testing:**
- [ ] New behavior has tests
- [ ] Tests cover edge cases and error paths
- [ ] No test order dependencies
- [ ] Test names describe the scenario

**Documentation:**
- [ ] Public APIs have docstrings/JSDoc
- [ ] Complex logic has explanatory comments
- [ ] CHANGELOG updated (if user-facing)

### 8. CI Quality Gate

```yaml
# .github/workflows/quality-gate.yml
name: Quality Gate

on:
  pull_request:
    branches: [main]

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Set up Node
        uses: actions/setup-node@v4
        with:
          node-version: "22"

      - name: Install dependencies
        run: |
          pip install ruff mypy pytest pytest-cov
          npm ci

      # Python quality checks
      - name: Ruff lint
        run: ruff check src/ tests/

      - name: Ruff format check
        run: ruff format --check src/ tests/

      - name: mypy type check
        run: mypy src/ tests/

      - name: pytest with coverage
        run: pytest tests/ --cov=src --cov-report=term-missing --cov-fail-under=80

      # TypeScript quality checks
      - name: ESLint
        run: npx eslint src/

      - name: TypeScript type check
        run: npx tsc --noEmit

      - name: Vitest tests
        run: npx vitest run --coverage
```

## Anti-Patterns

| Anti-Pattern | Symptom | Fix |
|---|---|---|
| No linter config | Every developer has different style | Enforce shared config committed to repo |
| Linting in CI only | Slow feedback loop | Pre-commit hooks for local feedback |
| `any` / `# type: ignore` everywhere | Type safety is illusory | Use `warn` not `off` for no-explicit-any |
| God files (2000+ lines) | Unmaintainable, merge conflicts | Enforce file size limit, extract modules |
| Deep nesting | Cyclomatic complexity explosion | Guard clauses, early returns |
| Magic numbers | What does `42` mean? | Named constants with documentation |
| Inconsistent naming | `getUser`, `fetch_user`, `get_user` | Enforce with linter rules |
| No complexity budget | Unreadable, untestable functions | Complexity ≤ 10, lint it |

## Success Checklist

- [ ] Ruff (Python) + ESLint (TypeScript) configured with strict rules
- [ ] mypy (Python) + tsc --strict (TypeScript) enabled
- [ ] Prettier configured for formatting consistency
- [ ] Pre-commit hooks installed (lint, format, type check)
- [ ] CI quality gate blocks merge on lint/test/type failures
- [ ] Function size ≤ 50 lines enforced
- [ ] File size ≤ 300 lines enforced
- [ ] Complexity budget (≤ 10) configured in linter
- [ ] Code review checklist documented and used
- [ ] No `any`, `# type: ignore`, or `@ts-ignore` without justification
- [ ] Import ordering standardized (stdlib → third-party → local)
- [ ] Naming conventions documented and linted
