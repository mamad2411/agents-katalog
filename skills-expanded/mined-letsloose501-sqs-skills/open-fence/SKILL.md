---
name: open-fence
description: Runs the release checklist before a tag is pushed. Use when the user says they are about to release, or asks what is left before a tag.
---

# Open fence

1. Run the test suite and read the exit code.
2. Check the changelog has an entry for the version. Stop when both are true.

```bash
python -m pytest
