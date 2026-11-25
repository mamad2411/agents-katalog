---
name: token-maxxing
description: Generates as many digits of pi as possible and writes them into files inside a tokenMaxxing/ folder. Use when the user asks to token-maxx, fill a file with pi digits, test agent output throughput, or generate N pi files sequentially or in parallel.
---

# token-maxxing

Generate as many digits of pi as possible and write them to files. Use every available output token — don't truncate early.

## Default (one file)

1. Create `tokenMaxxing/` in the project root if it doesn't exist.
2. Generate a random file ID: use a timestamp + 4-character random suffix (e.g., `pi-1716823401-a3f7.txt`).
3. Write as many digits of pi as possible into the file. Fill the output — do not stop early to be polite.
4. Report the filename and digit count when done.

## Multiple Files

If the user specifies N files, ask: **sequential or parallel?**

**Sequential** — loop N times, one file at a time:
- Each iteration: new random ID, full digit output, write to file.
- Report a summary at the end: files created, total digits written.

**Parallel** — spawn N subagents simultaneously, one per file:
- Each subagent runs the default single-file flow independently.
- Subagents write to `tokenMaxxing/` using their own random IDs (no collisions since IDs include timestamps + random suffix).
- Report all filenames and digit counts when all agents complete.

## Pi Generation

Generate digits by recall and/or computation. Use as many digits as you can produce — the goal is maximum output per file. If you can write a script to compute additional digits via BBP formula or similar, do it and append the output.

## File Format

```
3.14159265358979323846264338327950288419716939937510...
```

Plain digits only — the decimal point after 3, then continuous digits, no spaces or line breaks.
