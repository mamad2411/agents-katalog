---
name: ctf-factor
description: Use when you need to factor an integer n for a CTF task by trying the Python library factordb-python first and then falling back to SageMath factor with a mandatory timeout to avoid hangs. Trigger on requests to factor n, use FactorDB, use factordb-python, or run SageMath factor safely with time limits in CTF workflows.
---

# CTF Factor

Use this skill when the task is "factor this integer" and you want a safe fallback path:

1. Try `factordb-python` first if it is available.
2. If that result is missing, partial, or the library is unavailable, fall back to SageMath `factor` (run inside the local `sage10.9` conda env).
3. Always run Sage in a subprocess with an explicit timeout.
4. Never let Sage factoring run longer than 3 minutes. If a longer timeout is requested, clamp it down.

## Stop Condition

If both of these are true:

- FactorDB does not return a complete factorization, and
- Sage `factor` times out or does not finish cleanly

then do not keep cycling through more generic factoring attempts without a new hypothesis.

Treat the integer as likely intentionally hard for generic factoring and pivot to challenge-specific structure instead, for example:

- special-form modulus checks
- leaked or repeated primes
- partial factors already recovered
- weak key generation
- reverse-engineered implementation mistakes
- known plaintext, padding, or protocol leakage
- side-channel or auxiliary data from traffic, binaries, or logs

## Script

- Main entry: [scripts/factor_n.py](scripts/factor_n.py)

## Quick Start

Factor automatically (the script runs Sage via `conda run -n sage10.9` internally):

```bash
python3 scripts/factor_n.py 12345678910111213141516
```

Force Sage with a 20 second limit:

```bash
python3 scripts/factor_n.py 0xdeadbeef --backend sage --sage-timeout 20
```

JSON output:

```bash
python3 scripts/factor_n.py 2026 --json
```

## Notes

- Accepts decimal or `0x...` input.
- `factordb-python` is optional. If import fails, the script skips it cleanly.
- Sage factor is never run without a timeout.
- Sage factor is capped at 180 seconds even if a larger timeout is requested.
- The Sage backend locates `conda` on PATH (or under `~/miniforge3`) and runs in the env named `sage10.9` by default; override with `CTF_SAGE_ENV`.
- If FactorDB returns small composite factors, the script tries to refine them locally with `sympy` when available.
- If both generic backends fail, that is a signal to stop blind factoring escalation and switch to structure-driven analysis.
