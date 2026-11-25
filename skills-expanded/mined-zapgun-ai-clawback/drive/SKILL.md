---
name: drive
description: Drive the REAL claude binary through clawback's PTY channel at a scripted inter-turn gap schedule — the faithful load arm. Because the bytes on the wire are produced by genuine Claude Code, this is the only driver that exercises the 1h-TTL nested-cache-control rewrite (arm A2) authentically. Use for headline/moat numbers and to cross-check the HTTP replay arm (.skills/replay). Requires node-pty and a running clawback proxy.
---

# clawback PTY-driven load driver (faithful arm)

Run `benchmark/bin/drive_pty.js` from the project root. It launches the real
`claude` binary inside a PTY clawback owns (reusing `src/launch_claude.js` →
`ptyProcess.write()`, the same mechanism auto-continue uses) and types
scripted prompts on a schedule. Data is captured by the **proxy's**
`--turn-log` — start the proxy (with its turn-log) via `.skills/monitor`
first, pointed at the same `--port`.

## Why this arm exists

The request bytes are, by definition, exactly what Claude Code sends —
including the precise `cache_control` breakpoint nesting that the 1h-TTL moat
rewrites. The HTTP replay arm (`.skills/replay`) can only *approximate* that
with a fixture. Agreement between the two arms is what makes a claim
bulletproof; divergence is itself a finding.

## Requirements

- `node-pty` installed (clawback's optional dep). Without it the driver
  errors out — it cannot fall back to non-PTY (it needs the master FD to
  inject keystrokes).
- A running clawback proxy with a `--turn-log`.
- The real `claude` binary on `PATH` (or `--command <path>`). A real run
  spends real tokens through `claude`.

## Usage

```bash
# print the planned gap schedule + prompt loading, spawn nothing:
node benchmark/bin/drive_pty.js --dry-run --profile L0 --turns 5

# real run at L2 (5–30 min gaps), 30 turns:
node benchmark/bin/drive_pty.js --profile L2 --turns 30 \
  --prompts benchmark/prompts/coding.txt --settle-sec 8
```

## Key options

- `--profile L0|L1|L2|L3|L4` — inter-turn gap range (mirrors `.skills/replay`).
  L4 (overnight/date-rollover) can't be faithfully automated in a short run;
  use a real overnight window.
- `--turns N`, `--gap-sec N` (fixed-gap override).
- `--prompts PATH` — one prompt per line (`#` comments ok); the driver cycles
  `prompt[i % N]`. The shipped `benchmark/prompts/coding.txt` is read-only-ish
  on purpose (asks for explanation, not edits) so long unattended runs don't
  mutate the tree.
- `--settle-sec N` — turn is "done" after N s of PTY silence (quiescence;
  Claude Code's TUI has no machine done-marker). `--max-turn-sec` caps it.
- `--model ID` — pin claude's model (cost control; e.g.
  `claude-haiku-4-5-20251001`).
- `--effort low|medium|high|xhigh|max` — pin claude's reasoning level
  (`claude --effort`). Effort resizes the thinking blocks that ride inside each
  turn and get cached, so it shifts the cache economics clawback is measured on.
  Jagged availability: Haiku has none; `xhigh` is Opus 4.7/4.8 only.
- `--command claude`, `--cwd DIR`, `--port 8787`, `--transcript PATH`.

## Reads no fixture; the proxy writes them now

This arm *is* the real client, so it reads no `benchmark/fixtures/` — it
types live prompts at claude. The PTY itself sees only terminal bytes, never
the decrypted HTTP body, so the *driver* can't write a fixture. The **proxy**
can: `--capture-body` dumps the pristine `/v1/messages` body before any
mutation. `.skills/capture` wires this driver (one turn) to a
`--capture-body` proxy to mint a real fixture for the replay arm. See
`.skills/capture`.

## After a run

Analyze the proxy's turn-log with `.skills/bench`, then chart with
`.skills/plot`. Compare against the `.skills/replay` (clean) numbers.
