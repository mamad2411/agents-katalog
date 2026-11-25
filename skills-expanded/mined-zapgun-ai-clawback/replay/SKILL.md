---
name: replay
description: Drive a reproducible HTTP replay load against a running clawback proxy. Replays one captured /v1/messages fixture at a load profile's inter-turn gap schedule, with built-in carry-over control (fresh path-mode session id + per-block cache nonce). Auth is an OAuth bearer (CLAWBACK_OAUTH_TOKEN), never an Anthropic API key; pre-flights the proxy and bearer before spending tokens. Use to generate clean, per-knob, deterministic-timing traffic for the analyzer; pair with .skills/drive (the faithful PTY arm) to cross-check.
---

# clawback HTTP replay load driver

Run `.skills/replay/scripts/replay_load.sh` from the project root. It pre-flights (proxy
reachable? `CLAWBACK_OAUTH_TOKEN` bearer set?) and then forwards every argument
to `benchmark/bin/replay.js`. Data is captured by the **proxy's** `--turn-log`,
not by this driver — start the proxy (with its own turn-log) via
`.skills/monitor` first.

## Auth: OAuth bearer, never an API key

There is **no Anthropic API key** here. A real run forwards
`Authorization: Bearer $CLAWBACK_OAUTH_TOKEN` — the same OAuth credential
`claude` sends (Claude Max) — which clawback then forwards upstream. If you'd
rather not handle the bearer directly, drive real traffic through the PTY arm
(`.skills/drive`), which uses your actual `claude` login.

## Spends real tokens

A non-`--dry-run` run sends real `/v1/messages` requests against your
Anthropic limits — the very thing clawback stretches. Budget it (cap
`--turns`, use the cheap Haiku fixture for plumbing). `--dry-run` needs no
bearer and no proxy.

## Usage

```bash
# inspect the fixture + planned gap schedule, no proxy/bearer, no spend:
.skills/replay/scripts/replay_load.sh --dry-run --profile L0 --turns 5

# real block (proxy must be up with a --turn-log; bearer forwarded as
# Authorization, never an API key):
CLAWBACK_OAUTH_TOKEN=… .skills/replay/scripts/replay_load.sh \
  --profile L2 --turns 200 --fixture benchmark/fixtures/ccode.json \
  --port 8787 --session-id A5-L2
```

## Key options (forwarded to replay.js; see its header for the full list)

- `--profile L0|L1|L2|L3|L4` — inter-turn gap range (mirrors `.skills/drive`).
- `--turns N`, `--gap-sec N` (fixed-gap override for fast mechanics tests).
- `--fixture PATH` — the `/v1/messages` body to replay.
- `--session-id ID` — path-mode SESSION KEY; **use a fresh one per block**.
  Omitted → auto-minted per run.
- `--shared-cache` — skip the per-block cache nonce (measure a *warm* start
  across runs). Default is FRESH: a unique nonce is prepended to `system` so
  Anthropic's prefix cache starts cold for the block (carry-over control).
- `--anthropic-beta STR` — defaults to a realistic value including
  `extended-cache-ttl-2025-04-11`; required for arm A2 (1h-TTL) to be
  faithful, because clawback forwards but does not add this beta.
- `--stream`, `--model ID`, `--transcript PATH`.

## Fixture fidelity (read before quoting absolute numbers)

The shipped `benchmark/fixtures/ccode.json` is a **sanitized real capture**
(one Claude Code turn captured 2026-06-02 via `.skills/capture`; identifiers
and personal context scrubbed, `cache_control` breakpoints and `cch` structure
untouched). It is faithful in shape, but Claude Code's prompt evolves with
every release — for headline numbers on *today's* build, mint a fresh body
with `.skills/capture` (it drives one real claude turn through a
`--capture-body` proxy and promotes the pristine dump to a fixture), then pass
it here with `--fixture`. Or lean on `.skills/drive` (the faithful
real-`claude` arm).

## After a run

When both arms' turn-logs are collected, analyze with `.skills/bench`:

```bash
node benchmark/bin/analyze.js --out runs/report-$(date +%s) \
  --label A0=runs/A0.ndjson --label A5=runs/A5.ndjson
```
