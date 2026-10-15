---
name: smart-read
description: >
  Read files surgically — grep first, read only relevant sections.
  Prevents loading entire large files when only a few lines are needed.
  Activates automatically when smart-read mode is on. Input token savings: 40–90%
  depending on file size and task scope.
---

## smart-read mode: ACTIVE

Never read an entire file unless the task genuinely requires full-file understanding.

## Protocol

Before reading any file, follow this order:

1. **Grep first** — search for the specific symbol, function, or pattern needed:
   ```bash
   grep -n "functionName\|ClassName\|keyword" path/to/file
   ```

2. **Read targeted range** — use line numbers from grep to read only the relevant section:
   ```bash
   sed -n '45,80p' path/to/file
   ```
   Read ±10 lines around the target for context.

3. **Full read only if**:
   - File is <50 lines total
   - Task requires understanding the entire file structure
   - User explicitly says "read the whole file"

## File size thresholds

| File size | Default action |
|-----------|----------------|
| < 50 lines | Read full |
| 50–200 lines | Grep first, read relevant sections |
| 200–1000 lines | Grep first, read targeted ranges only |
| > 1000 lines | Grep first, read max 100 lines at a time |

## Token impact

| File size | Normal read | Smart-read | Savings |
|-----------|-------------|------------|---------|
| 200 lines | ~1,400 tokens | ~280 tokens | ~80% |
| 500 lines | ~3,500 tokens | ~420 tokens | ~88% |
| 1000 lines | ~7,000 tokens | ~490 tokens | ~93% |

## Off

User says "read full file" or "smart-read off" → comply for that file, resume smart-read after.
