---
name: ctf-sage
description: "Use when you need SageMath or CTF Python tooling in the lab, specifically the local conda environment `sage10.9` (SageMath 10.9 + pycryptodome). Covers non-interactive execution of Sage and Python (pycryptodome) code for factoring, lattice, ECC, polynomial and other crypto/math work. Note: pwntools is NOT installed in this env."
---

# CTF Sage

Use this skill when the task needs the local `sage10.9` conda environment.

Assume the normal path is:

- The agent runs on a Linux host with miniforge3 installed under `/root/miniforge3`.
- There is a conda environment named `sage10.9` providing SageMath 10.9 and `pycryptodome`.
- `pwntools` is **not** installed in `sage10.9`; for pwn exploits use `ctf-pwntools` workflow or install pwntools first.
- The preferred execution path is `scripts/run-sage.sh` or `conda run -n sage10.9 ...`.

## Quick Start

Sanity-check the environment:

```bash
conda run --no-capture-output -n sage10.9 python - <<'PY'
import Crypto
print('Crypto', Crypto.__version__)
PY
```

Run a small Sage command:

```bash
conda run --no-capture-output -n sage10.9 sage -q -c "print(factor(2026))"
```

Or via the helper script (resolves conda for you):

```bash
scripts/run-sage.sh 'sage -q -c "print(factor(2026))"'
```

## Workflow

1. Confirm the `sage10.9` env is reachable (`conda env list`).
2. Put the real work in a payload and execute it through `conda run -n sage10.9` or `run-sage.sh`.
3. Prefer non-interactive snippets, here-docs, and one-shot scripts.
4. For large payloads, write a `.sage`/`.py` file and run it with `run-sage.sh -f`.

## Patterns

### Run Multi-Line Python (pycryptodome)

Use a here-doc (non-interactive):

```bash
conda run --no-capture-output -n sage10.9 python - <<'PY'
from Crypto.Util.number import GCD, inverse
print('ready', GCD(2026, 1013))
PY
```

### Run Multi-Line Sage

```bash
conda run --no-capture-output -n sage10.9 sage -q - <<'SAGE'
R = PolynomialRing(ZZ, 'x')
x = R.gen()
print((x^2 + 1).factor())
SAGE
```

### Run A Script File

```bash
# .sage file -> automatically uses `sage`; .py -> `python`
scripts/run-sage.sh -f ./solve.sage
scripts/run-sage.sh -f ./solve.py
```

Or directly:

```bash
conda run --no-capture-output -n sage10.9 sage -q ./solve.sage
conda run --no-capture-output -n sage10.9 python ./solve.py
```

### Copy In An Exploit Or Script

Files are local; just run them in place:

```bash
cp /path/to/solve.py ./solve.py
conda run --no-capture-output -n sage10.9 python ./solve.py
```

## Script

### `scripts/run-sage.sh`

Execute a payload in the local `sage10.9` conda env by:

1. Locating `conda` (`$CONDA_EXE`, PATH, or `~/miniforge3/bin/conda`).
2. Running the payload via `conda run --no-capture-output -n sage10.9 ...`.
3. Supporting `-f <file>` (auto `.sage`→`sage`, `.py`→`python`) and `-` (stdin).

The env name can be overridden with `CTF_SAGE_ENV` if a different Sage env exists.

## Environment Notes

- `sage` is not on the global PATH; always go through `conda run -n sage10.9` or activate the env.
- `pycryptodome` is available; `gmpy2`/`sympy` may or may not be present — check before relying on them.
- This is a Linux-native environment; there is no WSL or remote SSH hop.

## Restricted Sandbox Fallback

If this skill is running inside a restricted sandbox and `conda`/network access fails because the sandbox blocks them, do not assume the lab is broken.

Ask the user for global permissions, explain that the failure is environmental, and retry the same command after permissions are expanded.

## Safety Notes

- Prefer non-interactive commands to avoid hanging the session.
- If you truly need an interactive TTY tool such as `gdb`, pause and confirm with the user first.
- If the command only needs generic Sage/Python and not the `sage10.9` env, still prefer the env to keep dependencies consistent.
