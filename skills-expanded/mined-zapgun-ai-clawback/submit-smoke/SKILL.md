---
name: submit-smoke
description: Cheaply prove the PTY turn-submission mechanism actually lands turns BEFORE any timed or headline run spends real tokens. Runs .skills/submit-smoke/scripts/submit_smoke.sh — one tiny passthrough Haiku block — and checks two independent signals: the driver's own "confirmed N/M" tally AND the count of real (non-ping) records the proxy logged. PASS only when every turn confirmed and the proxy logged at least that many real turns. Also reports which Enter encoding won (pure \r vs an escalated \n / \r\n fallback). Run this first whenever the driver, the submit helper (benchmark/lib/turn_submit.js), or the claude TUI version changes.
---

# clawback submit-mechanism smoke

Run `.skills/submit-smoke/scripts/submit_smoke.sh` from the project root. It is the fast gate that
answers ONE question before a real benchmark: **does Enter actually submit?**

## Why this exists

The driver used to write `${prompt}\r` in a single chunk; Claude Code's
bracketed-paste path coalesced it and the `\r` landed as a newline INSIDE the
input box, so ~6 of 8 turns silently never ran. The box sat at "turn 0%" and
the settle-on-silence heuristic could not tell "claude finished" from "claude
never started." The fix (`benchmark/lib/turn_submit.js`) types the text,
pauses, sends Enter as its OWN keystroke, and CONFIRMS each turn against the
proxy's `--turn-log` before advancing — escalating `\r` -> `\n` -> `\r\n` only
when confirmation never arrives. This skill verifies that fix end to end on
real `claude`, cheaply, so a swallowed Enter can never silently under-drive a
headline run again.

## Usage

```bash
# default: 3 turns, passthrough, Haiku, port 8799
.skills/submit-smoke/scripts/submit_smoke.sh

# bump the confirmation window for a slower model (Opus streams later):
.skills/submit-smoke/scripts/submit_smoke.sh --model claude-opus-4-7 --confirm-sec 20 --turns 3
```

## How to read the verdict

The script prints a verdict block and exits non-zero on FAIL:

- **driver said: `confirmed N/M turn`** — the driver's own tally (a turn is
  confirmed when a new non-ping turn-log record OR a sustained PTY output
  burst appears within `--confirm-sec`).
- **real turn-log recs: K** — non-ping `/v1/messages` records the proxy
  actually wrote. Because the arm is passthrough (no keep-alive pings), this
  is an exact count of turns that truly hit Anthropic.
- **Enter encodings that won** — a histogram. All `"\r"` means CR-as-its-own-
  keystroke submits once separated from the text (the happy path). Any
  `"\n"` / `"\r\n"` winning means CR alone still did not submit and the
  fallback carried it — a real finding to note before the big run.

**PASS** = `confirmed N/M` with N==M, AND real records >= turns, AND the
driver exited 0. Anything else is **FAIL** (it points you at `drive.log` and
`proxy.log` in the run dir).

## Cost & safety

Spends real Anthropic tokens for `--turns` turns via the real `claude`
binary — keep it tiny (default 3) and on Haiku. Runs on port **8799** by
default so it never collides with a dev proxy on 8787. Each run writes a
self-contained `runs/submit-smoke-<ts>/` (turn-log, proxy log, drive log,
state) at 0600.

## When to run it

- After editing `benchmark/bin/drive_pty.js` or `benchmark/lib/turn_submit.js`.
- After a `claude` CLI upgrade (the TUI's paste / keyboard handling can move).
- As the first step of any `.skills/ab` session — a green submit smoke is the
  precondition for trusting an A/B block's turn counts.
