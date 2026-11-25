---
name: capture
description: Capture a REAL Claude Code /v1/messages body as a replay fixture, so the HTTP replay arm (.skills/replay) faithfully reproduces Claude Code's cache_control breakpoint structure (a hand-authored fixture makes the 1h-TTL knob look like a no-op). Starts a clawback proxy with --capture-body, drives ONE real claude turn through it via the PTY driver, verifies the dump carries cache_control breakpoints, and promotes it to the fixture path. Spends real Anthropic tokens (exactly one turn; pin a cheap model with --model). Use once before replay-based benchmarking, or to refresh the fixture when Claude Code changes its request shape.
---

# clawback fixture capture

Run `.skills/capture/scripts/capture_fixture.sh` from the project root. It captures the
genuine Claude Code request body end to end:

1. starts a standalone clawback proxy with `--capture-body <tmp>` (detached,
   via `.skills/monitor`'s `run_monitor.sh --detach`);
2. drives **one** real `claude` turn through it (`benchmark/bin/drive_pty.js
   --turns 1`), which points claude at the proxy and types a single prompt;
3. stops the proxy;
4. verifies the dump with `benchmark/bin/verify_fixture.js` (must carry ≥1
   `cache_control` breakpoint, else the 1h-TTL arm is a no-op);
5. promotes the temp dump to the fixture path at mode 0600.

The captured bytes are the request body only — system prompt, tools, and the
one message. The Anthropic API key is **not** captured (it rides in headers
clawback never dumps). Still, treat the fixture as sensitive: it contains your
system prompt and tool definitions. It is gitignored-by-convention and excluded
from the npm tarball.

## Spends real tokens

Step 2 runs the real `claude` binary against your own Anthropic limits —
exactly one turn. Pin a cheap model to keep it trivial:

```bash
.skills/capture/scripts/capture_fixture.sh --model claude-haiku-4-5-20251001
```

Requirements: the `claude` CLI on PATH, `node-pty` installed (`npm i
node-pty`), and claude already authenticated.

## Usage

```bash
# default: capture to benchmark/fixtures/ccode.json on 127.0.0.1:8787
.skills/capture/scripts/capture_fixture.sh --model claude-haiku-4-5-20251001

# custom destination / port / prompt:
.skills/capture/scripts/capture_fixture.sh --out benchmark/fixtures/mywork.json \
  --port 8790 --prompt "Summarize README.md in one line."
```

## Options

- `--out PATH` — fixture destination (default `benchmark/fixtures/ccode.json`).
- `--host`, `--port` — proxy bind (default `127.0.0.1:8787`).
- `--model ID` — pin claude's model (cost control; forwarded to drive_pty).
- `--prompt TEXT` — the single prompt to type (default: a read-only listing).
- `--keep-tmp` — keep the temp dump even if verification fails (debugging).
- everything after `--` is forwarded to `drive_pty.js`.

## Why this exists

`--capture-body` (in `src/server.js`) dumps the **pristine** body once, before
clawback's strip/1h-rewrite mutations — so the fixture is exactly what
Claude Code put on the wire. Replaying it through clawback then exercises the
real cache mechanic. See `.skills/replay`.

## After capture

Replay the fixture with `.skills/replay`, then analyze with `.skills/bench`
and visualize with `.skills/plot`. For the faithful (non-replay) arm that
drives real claude live, see `.skills/drive`.
