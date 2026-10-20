---
name: persistent-env-vars-via-generated-envs-py
description: Capture build-time environment variables into a generated `envs.py` that the installed package reads at import time, so user-chosen cache paths or flags persist across pip installs without shell rc files.
category: build-system
version: 1.0.0
version_origin: extracted
tags: [setup-py, environment-variables, wheels, build-time, python-package, persistence]
confidence: medium
source_type: extracted-from-git
source_url: https://github.com/deepseek-ai/DeepGEMM.git
source_ref: main
source_commit: 7f2a703ed51ac1f7af07f5e1453b2d3267d37d50
source_project: DeepGEMM
source_paths:
  - setup.py
  - deep_gemm/__init__.py
imported_at: 2026-04-18T13:30:00Z
---

# Persistent Env Vars Via a Generated `envs.py` Module

## When to use
Your library reads environment variables at runtime (e.g. `DG_JIT_CACHE_DIR`, `DG_JIT_CPP_STANDARD`) but you want users who set those vars *at install time* to have them persist automatically for every future `python -c "import <pkg>"` — without asking them to edit `.bashrc` or remember to re-export.

## Steps
1. **In `setup.py`'s `CustomBuildPy.run()`**, before the regular `build_py.run()`, generate a Python file into the build-lib layout:
   ```python
   def generate_default_envs(self):
       code  = '# Pre-installed environment variables\n'
       code += 'persistent_envs = dict()\n'
       for name in ('DG_JIT_CACHE_DIR', 'DG_JIT_PRINT_COMPILER_COMMAND', 'DG_JIT_CPP_STANDARD'):
           if name in os.environ:
               code += f"persistent_envs['{name}'] = '{os.environ[name]}'\n"

       with open(os.path.join(self.build_lib, 'deep_gemm', 'envs.py'), 'w') as f:
           f.write(code)
   ```
   Only serialize vars that were actually present — no `None` entries, no default fallbacks.
2. **Wire into `setuptools.setup(... cmdclass={'build_py': CustomBuildPy})`** so the generator runs during `python setup.py build` / `bdist_wheel`.
3. **Read with a best-effort import in the package `__init__`:**
   ```python
   try:
       from .envs import persistent_envs
       for key, value in persistent_envs.items():
           if key not in os.environ:
               os.environ[key] = value
   except ImportError:
       pass
   ```
   - The `try`/`except` handles the case where `envs.py` wasn't generated (dev-mode install, no env vars were set at build).
   - The `if key not in os.environ` guard means an explicitly-exported env var at process start always wins over the baked-in one. This is the intuitive "override" behavior.
4. **Document which vars are persisted.** Users need to know that setting `DG_JIT_CPP_STANDARD=20` once before install is enough, but `DG_JIT_DEBUG=1` isn't persisted (diagnostic flags, not config).
5. **Ship `envs.py` in the wheel.** It's plain Python, no package_data dance required — it lives under `<pkg>/envs.py` and is automatically included.

## Evidence (from DeepGEMM)
- `setup.py:140-147`: the `generate_default_envs()` method — writes only env vars that were set.
- `setup.py:118-123`: the `CustomBuildPy.run()` hook points where generator runs before `build_py.run()`.
- `deep_gemm/__init__.py:6-13`: the import-time application, with `os.environ` priority over the baked-in values.

## Counter / Caveats
- **Builds become reproducible only if env is clean.** If CI sets `DG_JIT_CPP_STANDARD=17` but a developer on their workstation has `=20`, the shipped wheels differ. Either scrub env vars in the CI build step or document that these env vars are build-time inputs.
- **Reinstalling the same wheel overwrites `envs.py`.** If a user overrides via `DG_JIT_CACHE_DIR` at a later install, the old value is gone — correct but surprising. Users sometimes want "preserve previous".
- **Don't persist secrets.** Anyone who reads `envs.py` inside the wheel sees the value. Only use for non-sensitive flags.
- **The list of persisted vars is hardcoded in setup.py.** Adding a new persistent var requires a setup.py edit — acceptable for a small fixed set, painful if you expect dozens.
