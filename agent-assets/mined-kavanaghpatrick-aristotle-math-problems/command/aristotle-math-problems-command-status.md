---
description: Check status of all Aristotle jobs
allowed-tools: Read, Bash
argument-hint: [slot-number]
---

Check status of Aristotle proof search jobs.

```bash
python3 scripts/aristotle_fetch.py status
```

This shows all tracked submissions with their current status:
- ✅ PROVEN — fetched and verified (0 sorry, 0 axiom)
- 📥 COMPLETE — ready to fetch (run `/project:fetch`)
- ⏳ IN_PROGRESS/QUEUED — still processing
- 📝 NEAR_MISS — 1 sorry remaining
- ❌ FAILED/COMPLETED — has issues

If a specific slot is requested via `$ARGUMENTS`, filter to just that slot.
