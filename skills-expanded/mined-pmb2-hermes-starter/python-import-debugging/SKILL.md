---
name: python-import-debugging
description: Diagnose and fix Python import resolution issues — ModuleNotFoundError,
  namespace package hijacking, sys.path contamination, editable install conflicts
version: 1.2.0
author: Hermes Agent
license: MIT
platforms:
- linux
- macos
- windows
metadata:
  hermes:
    tags:
    - Python
    - imports
    - debugging
    - ModuleNotFoundError
    - sys.path
    - namespace-packages
    related_skills:
    - systematic-debugging
    - python-debugpy
    triggers:
    - python import error
    - module not found
    - import debug
    - python module resolution
    - ModuleNotFoundError
    - ImportError
    - circular import
    - PYTHONPATH issue
    - C extension not found
    - pydantic_core not found
    - cross-version venv
    - CPython ABI mismatch
---

# Python Import Debugging

Debug Python import resolution failures — `ModuleNotFoundError` for files that exist, wrong module loaded, namespace package hijacking, and sys.path contamination. This skill covers the diagnosis pattern used when a module import silently resolves to the wrong location.

## When to Use

- A test or script fails with `ModuleNotFoundError` even though the file exists on disk
- Importing a package resolves to a different project than expected
- `import X` works on one machine but breaks on another
- A namespace package (a directory without `__init__.py`) picks up content from an unrelated project

## 1. Check Where Python Resolves the Module

When `import foo.bar` fails but `foo/bar.py` exists, check what `foo` actually resolves to:

```python
import foo
print(foo.__path__)   # namespace packages have __path__
print(foo.__file__)   # regular packages have __file__
```

If `__path__` points to a different project's directory, **sys.path contamination** is the cause.

## 2. Locate the Contamination Source

```python
import sys
# Find the matching path entry
for p in sys.path:
    if 'offending-project' in p:
        print(f"Contaminant: {p}")
```

Common contamination sources:
- `.pth` files in site-packages adding development project paths
- Editable installs (`pip install -e .`) that register `src/` directories
- `PYTHONPATH` environment variable
- `sitecustomize.py` or `usercustomize.py` that adds paths
- Editable install `__editable__.*.pth` files or `__editable__.*.finder.__path_hook__` entries in sys.meta_path

## 3. Fix: Make It a Regular Package

The cleanest fix for namespace hijacking: **add an `__init__.py`** to the target package directory.

```bash
echo "# Package marker" > path/to/package/__init__.py
```

An `__init__.py` forces the directory to resolve as a regular package. Python's namespace package resolution only applies to directories WITHOUT `__init__.py` — a `__init__.py` (even empty) gives the local package priority over far-away namespace directories on sys.path.

## 4. Fix: Clean the Path Contamination

If the real fix is removing the contamination:

```bash
# Find .pth files that inject dev paths
python -c "import site; [print(f) for f in site.getusersitepackages()]
site.getsitepackages()]"
grep -r "offending-project" $(python -c "import site; print(site.getusersitepackages())")/

# Disable PYTHONPATH
unset PYTHONPATH
```

## 5. Verify the Fix

After either fix, verify:

```bash
cd /path/to/project
python -c "import target_module; print(target_module.__file__)"
# Should print the expected path, not a hijacked one

# Then run the original failing test
python -m pytest tests/path/to/test.py -v
```

## 6. Cross-Version Venv Shadowing via PYTHONPATH

When multiple virtual environments coexist with different Python versions (e.g., `venv/` = Python 3.11, `.venv/` = Python 3.13), `PYTHONPATH` may list the older venv's site-packages **before** the new venv's site-packages. This creates a subtle import failure:

- The new Python (3.13) loads a package like `pydantic` from the old (3.11) site-packages
- That package's C extension `.pyd` file is tagged for the old ABI (`cp311-win_amd64.pyd`)
- Python 3.13 cannot load it → `ModuleNotFoundError: No module named '_pydantic_core._pydantic_core'`
- The error message may be misleading because it surfaces from a downstream lazy-import handler, not from the actual C extension load failure

**Symptom pattern:** A test that depends on a package with C extensions (e.g., fastapi → pydantic → pydantic-core) fails with a confusing error, often raising `SystemExit` from a lazy-import fallback rather than the actual `ModuleNotFoundError` about the C extension.

**Diagnosis:**

```bash
# 1. Check PYTHONPATH env var
echo "$PYTHONPATH"

# 2. Compare sys.path ordering
python -c "import sys; print('\n'.join(sys.path))"

# 3. Check which venv a package actually resolves from
python -c "import pydantic; print(pydantic.__file__)"

# 4. Verify Python version of each venv
/path/to/old/venv/Scripts/python --version
/path/to/new/venv/Scripts/python --version

# 5. Check .pyd files for ABI tag mismatch
ls -la old-venv/Lib/site-packages/pydantic_core/*.pyd
# → _pydantic_core.cp311-win_amd64.pyd  ← cp311 cannot load under Python 3.13

# 6. Verify target venv has all test deps (including pytest)
python -c "import pytest"
```

**Fix options (in order of preference):**

A. **Complete the migration** — Install all test dependencies (pytest, etc.) in the new venv, then fix PYTHONPATH to exclude the old venv or unset it.

B. **Run tests via the compatible venv** — Use the old venv's Python directly while the migration is in progress:
   ```bash
   /path/to/old/venv/Scripts/python -m pytest ...
   ```

C. **Unset PYTHONPATH** — Only works if the new venv is self-contained (has pytest + all test deps). Verify first:
   ```bash
   unset PYTHONPATH && /path/to/new/venv/Scripts/python -c "import pytest"
   ```

**Pitfall:** `unset PYTHONPATH` silently drops site-packages from sys.path if the new venv is incomplete — pytest itself can become unfindable, making it look like the env is broken when really it's just missing test deps.

D. **Reorder PYTHONPATH to prioritize new venv** — When you cannot (or don't want to) complete the full migration, keep both venvs in PYTHONPATH but put the new venv's site-packages **first**:
   ```bash
   export PYTHONPATH="/path/to/new/venv/Lib/site-packages:$PYTHONPATH"
   # Or on Windows (remove old venv entry from the front):
   set PYTHONPATH=C:\path\to\.venv\Lib\site-packages;%PYTHONPATH%
   ```
   This works because Python's import resolution walks PYTHONPATH entries in order — the first match wins. By placing the new venv first, its C extensions (correct ABI for the active Python version) load preferentially, while the old venv still supplies any packages not yet migrated.

   **Best practice when using option D** — explicitly construct the path in the right order rather than prepending to an inherited value that may already have the wrong order:
   ```bash
   PYTHONPATH="/path/to/project:/path/to/.venv/Lib/site-packages:/path/to/venv/Lib/site-packages" \
     python -m pytest tests/...
   ```

   **Verification:**
   ```bash
   python -c "import pydantic_core; print(pydantic_core.__file__)"
   # Should print a path under .venv/Lib/site-packages, NOT venv/Lib/site-packages
   ```

   **Pitfall:** If an intermediate parent process (cron daemon, fleet manager, gateway launcher) inherits a PYTHONPATH with the wrong order, the fix needs to be applied wherever that parent's environment is set — not just in the terminal where you run tests. Check the cron daemon's shell init or the fleet manager's `os.environ.copy()` injection.

## 7. Editable Install Path Ordering

Editable installs (`pip install -e .`) register their project directories in sys.path via `.pth` files in the active venv's site-packages. When combined with `PYTHONPATH` entries, the resolution order follows:

1. `PYTHONPATH` entries (in order)
2. `sys.path` built from the active venv (site-packages, `.pth` files)
3. User site-packages (when `ENABLE_USER_SITE` is true)

The `__editable__.*.pth` finder hook is registered via `sys.meta_path`, not `sys.path`, so it is checked **before** regular path entries. This can give editable installs priority over PYTHONPATH entries even though the PYTHONPATH paths appear earlier in the list.

**To find all editable installs:**

```bash
pip list --editable
# or
find /path/to/venv/Lib/site-packages -name "__editable__*.pth"
```

## 8. Hyphenated Module Filenames Can't Be Imported

Scripts named with hyphens (e.g. `cron-guardian.py`) raise
`ModuleNotFoundError: No module named 'cron_guardian'` on a plain `import` —
even when the file exists and its directory is on `sys.path`. Hyphens are
not valid in Python identifiers, so the import system can't map the filename
to a module name. `py_compile` and running the file directly still work;
only `import` fails, and `importlib.util.find_spec` returns None.

**Fix — load via importlib:**

```python
import importlib.util, sys

spec = importlib.util.spec_from_file_location("cron_guardian", r"C:\path\to\cron-guardian.py")
mod = importlib.util.module_from_spec(spec)
sys.modules["cron_guardian"] = mod   # register so intra-module imports resolve
spec.loader.exec_module(mod)
```

Registering under a valid module name in `sys.modules` matters when the
script itself does `from sibling import ...` — those resolve against
`sys.modules`, not the loader.

**Trigger:** any scripts/repo dir containing hyphenated `.py` files that you
need to test or monkeypatch (common for cron scripts: `cron-guardian.py`,
`auto-action-handler.py`). Check the filename before assuming a `sys.path`
problem.

## Pitfalls

1. **Don't assume a missing `__init__.py` is always a bug** — some projects intentionally use namespace packages for split packaging. Only add `__init__.py` when namespace hijacking is causing real import failures.

2. **Namespace resolution order** follows sys.path order, not your intuition. If two directories named `scripts` appear on sys.path, the FIRST one wins when neither has `__init__.py`.

3. **An empty `__init__.py` is enough** — you don't need content. A comment explaining the purpose is helpful but not required for the fix.

4. **sys.path pollution from editable installs** — `pip install -e` on multiple projects with same-named top-level directories (e.g., both have `scripts/`) will cause conflicts. Each editable install registers its `src/` in a `.pth` file. Check `pip list --editable` to find them all.

5. **CPython ABI tag mismatch** — A `.pyd` file's filename includes the target Python version (e.g., `cp311`, `cp313`). A Python 3.13 interpreter **cannot** load a `cp311`-tagged `.pyd` file. The error is `ModuleNotFoundError` on the C extension module name (e.g., `_pydantic_core`), not a clear "wrong ABI" message. Cross-check the ABI tag in the filename against `python --version` output.

6. **Lazy-import SystemExit masks the real cause** — When an import chain breaks mid-way (e.g., pydantic-core fails, but pydantic was being loaded lazily), the error handler may print a misleading message like "Web UI requires fastapi and uvicorn" instead of the actual `ModuleNotFoundError` for `_pydantic_core._pydantic_core`. Always scroll up in the traceback to find the **first** `ModuleNotFoundError` in the chain — that is the real root cause.
