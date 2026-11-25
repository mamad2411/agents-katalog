---
name: choose-verification-model
description: "Print a verification model slug. Invoke by name when you need one."
---

# Choose a Verification Model

Run `scripts/pick.py` with Python 3 from this skill's directory. `--model` is your slug. `--reviewer-models` is the enabled slugs, comma-separated. Leave out `inherit`. Use the slug it prints. If it exits non-zero, stop and report stderr. Do not guess a reviewer.

```bash
python3 scripts/pick.py --model SLUG --reviewer-models a,b
```

```powershell
py -3 scripts/pick.py --model SLUG --reviewer-models a,b
```

If asked to refresh the list, see `references/refresh.md`.
