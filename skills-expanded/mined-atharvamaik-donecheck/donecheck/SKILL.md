---
name: donecheck
description: Use before a coding agent claims work is finished. Runs DoneCheck and fixes obvious proof failures.
---

# DoneCheck

Before saying work is done, run:

```bash
python donecheck.py --cmd "<project test command>"
```

If there is no project test command, run:

```bash
python donecheck.py
```

If `DONECHECK.md` says `FAIL`, fix the findings and rerun. Final responses should mention the receipt status.
