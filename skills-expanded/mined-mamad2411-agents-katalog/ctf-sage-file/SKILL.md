---
name: ctf-sage-file
description: "Use when creating, converting, or reviewing SageMath source files such as CTF solve scripts. Enforce .sage suffixes for Sage-dependent code, avoid unnecessary sage.all imports, and prefer Sage built-ins over handwritten helpers."
---

# Sage File

Use this skill when writing or editing SageMath source files, especially CTF solver scripts.

This skill is about file conventions and code style.
It complements `ctf-sage`, which covers how to run Sage in the local lab.

## Core Rules

- If the script depends on Sage-specific globals, syntax, or runtime, use `exp.sage`, not `exp.py`.
- If the script does not actually need Sage, keep it as `exp.py`.
- When converting `exp.py` to Sage, rename the file to `exp.sage`.
- Prefer short, readable scripts over defensive wrappers or reusable frameworks.
- For obvious template题, keep the script close to the textbook attack path instead of overengineering it.

## When A File Must Be `.sage`

Use `.sage` when any of these appear:

- Sage globals such as `ZZ`, `QQ`, `crt`, `xgcd`, `continued_fraction`, `Matrix`, `vector`, `GF`, `EllipticCurve`, `PolynomialRing`
- Sage-only syntax such as `R.<x> = PolynomialRing(...)`
- Sage helpers such as `small_roots`, `nth_root`, `factor`, lattice or polynomial workflows
- The intended execution path is `sage -q exp.sage`

If none of those are needed, do not force Sage into the solution.

## Import Policy

- Do not write `from sage.all import *`.
- In `.sage` files, do not import Sage globals that are already available by default.
- Only import non-Sage modules that are actually needed, such as:
  - `re`
  - `hashlib`
  - `pathlib`
  - `Crypto.Util.number`
- If a helper is globally available in `.sage`, call it directly.

Examples:

- Good: use `crt(cs, ns)` directly in `exp.sage`
- Good: use `ZZ(c).nth_root(3)` directly in `exp.sage`
- Bad: `from sage.all import ZZ, crt`
- Bad: `from sage.all import *`

## Style Rules For `exp.sage`

- Prefer Sage built-ins over handwritten helpers when the built-in is clear.
- Do not hand-roll CRT, extended Euclid, continued fractions, integer roots, or factoring if Sage already provides a direct primitive.
- Keep the happy path only. Do not add extra abstraction just to make the file look generic.
- Avoid unnecessary functions if the whole solve fits cleanly in a short script.
- Keep comments sparse and only for non-obvious math steps.

## Recommended Conversions

Common replacements when shortening a solver:

- handwritten CRT -> `crt(...)`
- handwritten egcd -> `xgcd(...)`
- handwritten continued fractions -> `continued_fraction(...).convergents()`
- `gmpy2.iroot` for Sage scripts -> `ZZ(...).nth_root(...)`
- manual math object setup in Python -> direct Sage objects in `.sage`
