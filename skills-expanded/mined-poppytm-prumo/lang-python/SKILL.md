# Python Idiomatic Reliability, Strict Typing & Systems Hygiene

## 1. Purpose
Author, refactor, and audit production systems written in **Python 3.12+**. This skill enforces complete static type coverage (`mypy --strict` / `pyright`), immutable data modeling (`@dataclass(frozen=True, slots=True)`), structured concurrency via `asyncio.TaskGroup`, eradication of bare exceptions and silent failures, elimination of insecure serialization (`pickle`, `eval`, `yaml.unsafe_load`), and automated static verification with `ruff`.

---

## 2. Use When
- Developing backend services, microservices, developer CLIs, or harness tools in Python.
- Writing asynchronous I/O pipelines, event loops, or worker pools using `asyncio`.
- Designing typed domain models, configuration loaders, or API schemas with Pydantic v2 or dataclasses.
- Implementing data analysis, automation scripts, or integration test harnesses using `pytest`.
- Operating in mode(s): `implementation`, `review`, `testing`, `audit`.

---

## 3. Do Not Use When
- Developing in Go (use `lang-go`), Rust (use `lang-rust`), or C/C++ (use `lang-c` / `lang-cpp`).
- Working purely on low-level OS drivers or real-time sub-millisecond execution where GC pauses are unacceptable.
- The project is legacy Python 2 or pre-3.10 where modern type hints and structured concurrency are unavailable.

---

## 4. Required Context
Before implementing or modifying Python code, verify:
- **Python Version**: Minimum Python 3.11+, targeting modern 3.12+ syntax (PEP 695 type parameter syntax: `def func[T](val: T) -> T:`).
- **Type Checker**: `mypy` in strict mode (`disallow_untyped_defs = true`, `no_implicit_optional = true`) or `pyright`.
- **Linter & Formatter**: `ruff` with standard rule presets (`E, F, W, I, N, UP, B, SIM, RUF`).
- **Concurrency Model**: Structured asynchronous I/O (`asyncio.TaskGroup`) vs CPU-bound processing (`ProcessPoolExecutor`).

---

## 5. Procedure

```
[Domain Modeling & Types]
         |
         v
[1. Strict Type Definitions] ------> PEP 695 generics, frozen slots dataclasses
         |
         v
[2. Error Handling & Invariants] --> Custom typed exceptions, zero bare excepts
         |
         v
[3. AsyncIO Structured Loop] ------> TaskGroup lifecycle, CancelledError propagation
         |
         v
[4. Static Lint & Type Check] -----> ruff check --fix, mypy --strict
         |
         v
[5. Dynamic Pytest Verification] --> Deterministic fixtures, parameterized tests
```

### Step 1: Strict Static Typing & Immutability
1. Every public and internal function must declare explicit parameter and return types:
   ```python
   def compute_checksum[T: bytes | bytearray](payload: T) -> str: ...
   ```
2. Favor immutable data structures with slots to reduce memory footprint and prevent accidental attribute mutation:
   ```python
   from dataclasses import dataclass


   @dataclass(frozen=True, slots=True)
   class ProcessJob:
       job_id: str
       timeout_seconds: float
       priority: int = 0
   ```
3. Disallow raw `Any`. If a generic value is truly arbitrary, use `object` with explicit runtime `isinstance()` narrowing.

### Step 2: Resilient Error Handling
1. Never swallow exceptions:
   ```python
   # FORBIDDEN:
   try:
       ...
   except Exception:
       pass

   # MANDATORY:
   try:
       ...
   except SpecificDomainError as err:
       logger.warning("Operation failed: %s", err)
       raise ProcessingFailureError(f"Job {job_id} aborted") from err
   ```
2. Exception hierarchies must derive from a domain base exception:
   ```python
   class DomainError(Exception):
       """Base error for domain."""


   class ResourceNotFoundError(DomainError): ...


   class ValidationError(DomainError): ...
   ```

### Step 3: Structured Concurrency with AsyncIO
1. Manage concurrent async tasks using `asyncio.TaskGroup` (Python 3.11+). Never spawn orphan tasks via detached `asyncio.create_task()`:
   ```python
   async def run_pipeline(items: list[str]) -> list[str]:
       results: list[str] = []
       async with asyncio.TaskGroup() as tg:
           for item in items:
               tg.create_task(fetch_and_process(item, results))
       return results
   ```
2. Cancellation hygiene: always allow `asyncio.CancelledError` to propagate after resource cleanup.

### Step 4: Security & Dangerous Function Eradication
- `eval()` and `exec()` are strictly banned.
- `pickle` deserialization on untrusted inputs is banned. Use `json` or `msgpack`.
- Shell execution: use `subprocess.run(["cmd", "arg"], check=True, shell=False)`. Never pass raw formatted strings with `shell=True`.
- File system traversal: use `pathlib.Path.resolve()` and verify `path.is_relative_to(base_dir)`.

### Step 5: Static Analysis & Test Verification
1. Run `ruff check .` and `ruff format --check .`.
2. Run `mypy --strict .` to ensure 100% type soundness.
3. Run `pytest -v --tb=short` with high coverage.

---

## 6. Decision Rules & Invariants
- **RULE 1 (Zero Bare Excepts)**: `except:` without an exception class or catching `Exception` to silently `pass` fails static analysis immediately.
- **RULE 2 (No Unconstrained Any)**: Use of `typing.Any` must be guarded by runtime type narrowing or replaced with generic type variables / `object`.
- **RULE 3 (Path Safety)**: Any file access using user input must be resolved and verified against directory traversal (`is_relative_to`).
- **RULE 4 (Subprocess Bounded Execution)**: Every external process invocation must specify a finite `timeout` parameter and set `shell=False`.

---

## 7. Evidence Required
- **Type Checking Evidence**: `mypy --strict` passes with 0 errors across all source modules.
- **Linting Evidence**: `ruff check` passes with 0 warnings or errors.
- **Test Evidence**: `pytest` passes 100% of unit and integration test fixtures.

---

## 8. Output Contract
- Fully typed Python source files (`.py`) conforming to PEP 8, PEP 585, PEP 604, and PEP 695.
- Project configuration (`pyproject.toml`) containing tool definitions (`[tool.ruff]`, `[tool.mypy]`, `[tool.pytest]`).
- Python Verification Report (`templates/python-verification-report.md`).

---

## 9. Stop Conditions
- `mypy --strict` and `ruff check` report 0 errors.
- All test suites execute successfully under `pytest`.
- Token budget exhausted.
- Blocked on external dependency.

---

## 10. Escalation Rules
- Escalate if a legacy third-party library without typing stubs (`py.typed`) causes unresolvable mypy errors in client code.
- Escalate to security lead if an existing system component relies on arbitrary `pickle` deserialization.
