---
name: emo-x
description: Adaptive, execution-based evaluation of AI coding models and agents (EMO-X). Use when the user asks to benchmark a model, run a capability profile, verify harness health, or compare two models with uncertainty. Invokes shared/run.py as a subprocess and reads the immutable raw bundle.
version: 2.0.0-rc1
category: qa
---

![EMO-X banner — Execution · Measurement · Observability](src/emo-x-banner.png)

```text
######  #    #   ####   #    #
#       ##  ##  #    #   #  #
#####   # ## #  #    #    ##
#       #    #  #    #   #  #
######  #    #   ####   #    #
Measure what agents accomplish — not what they say
```

# EMO-X Skill (Model B: skill inside the agent)

> **Session opening (show once):** display the hero splash first, then
> these instructions. CLI: printed automatically on stderr each run
> (`--quiet` silences it). MCP: in `initialize.serverInfo.splash`.
> forge-agent: `emo_x(action="splash")`. The splash is identity, not
> decoration — it states the version, live suite/manifest/test counts,
> and the iron rule below.

## What is this skill?

EMO-X measures what is **reliably accomplished**, not what is said as
text: real-execution code suites, agent loops, recovery, calibration,
safety, and long horizon — with a failure fingerprint and statistical
uncertainty, never one number.

## When to invoke it?

- The user asks to evaluate/compare a model (`benchmark this model`).
- The user asks for a capability profile (`capability profile`, EMO report).
- The user suspects a broken environment (`self-test`, harness check).

## The iron rule

This skill **invokes** `shared/run.py` as a subprocess — it never
re-implements logic, never copies prompts, never invents numbers.
Results are read from the raw bundle only (`results/raw/RUN-ID/`).
Any number without a raw bundle is inadmissible.

## Install paths: full clone vs pip (choose once)

- **Track 1 — user (benchmark models):** `pip install emo-x-eval`, then
  `emo --self-test`, `emo --suite code25 --out results/`. The `emo`
  entry behaves exactly like `python3 shared/run.py` (same splash on
  stderr, same `--quiet`, same sealed bundles).
- **Track 2 — harness developer:** `git clone` this repo; run
  `python3 tests/run_all.py`. Contribute per `CONTRIBUTING.md`.

## Run (execute literally, adjust paths only)

> **Reports go in the agent's working directory** (cwd), not the skill
> root: always pass `--out` (the current project dir), and display the
> report in the browser via the generated `report.html` next to the
> bundle (see "Graphical report" below).

```bash
EMOX=/path/to/emo-x   # root of this repo
OUT=.                  # the agent's working project dir (cwd) — do not point it at the skill root

# 0) verify first (two minutes, no endpoint) — any failure stops everything:
python3 $EMOX/shared/run.py --self-test
python3 $EMOX/tests/run_all.py

# 1) code suite (always start here):
python3 $EMOX/shared/run.py --backend openai-generic --suite code25 --out $OUT/results/

# 2) full profile (after 1 succeeds):
python3 $EMOX/shared/run.py --suite profile --trials 3 --out $OUT/results/

# 3) focused suites:
python3 $EMOX/shared/run.py --suite dynamic-code --instances 20 --seed 12345 --out $OUT/results/
python3 $EMOX/shared/run.py --suite recovery --fault-rate 0.25 --out $OUT/results/
python3 $EMOX/shared/run.py --suite gauntlet --out $OUT/results/
python3 $EMOX/shared/run.py --suite code25 --only T5,R7,H3 --trials 3 --out $OUT/results/

# 4) benchmark self-health:
python3 $EMOX/shared/run.py --health

# 5) client report (frozen template + QA stamp) — written to $OUT/reports/:
python3 $EMOX/shared/run.py --report $OUT/results/<model>_<stamp>.json --model MODEL-ID --out $OUT/reports/
```

## Workflow: Manual or Auto (ask the user first)

When a model benchmark is requested, **explicitly offer the user** two
options before any execution:

| | Manual workflow | Auto workflow |
|---|---|---|
| Meaning | The agent runs one step → shows the result → **waits for your confirmation** before the next | The agent owns the full task (self-test ← code25 ← profile ← graphical report) **without coming back to you** until it completes and shows the report |
| When | New endpoint, first run, sensitive results | Known working endpoint, routine run |
| Stopping | Any failure stops and asks for a decision | Only critical failure stops (red self-test, blanket VOID); the rest is logged and continued |

The verbatim choice question: *"Benchmark for MODEL-ID: Manual (step by step with your confirmation) or Auto (complete everything and show the report)?"*

Mandatory Auto rules: green self-test first or stop immediately; order code25 ← profile ← report; no S3–S5 and no hidden without prior explicit approval; the graphical report opens automatically at the end; any blanket VOID is announced, never silently bypassed.

Progress visibility (both workflows): the harness prints a live bar on
stderr — `[profile 2/7] [code25 14/25] ██████░░░░ 56% | T14 H3 perturbed · ✓11 ✗2 · 04:12 ~06:30`
(bar + current step title + pass/fail tallies + elapsed + approximate
ETA; `--no-progress` disables it, bundles stay identical). In Auto,
quote the percentage and current step when reporting status
(e.g. "~35% — code25 trial 2/3, now on T14"), never just "working on it".

## Graphical report (HTML + charts — opens in the browser)

After any run, render the view from the raw bundle and open it:

```bash
python3 $EMOX/shared/render_report.py $OUT/results/raw/RUN-ID/ --out $OUT/reports/RUN-ID/
open $OUT/reports/RUN-ID/report.html   # macOS; or xdg-open on Linux
```

**Multiple models (leaderboard):** one model or N — as the user wants:

```bash
python3 $EMOX/shared/render_leaderboard.py $OUT/results/raw/RUN-A/ [$OUT/results/raw/RUN-B/ ...] --out $OUT/reports/board/
open $OUT/reports/board/leaderboard.html
```

The board contains: a banded rank table (overlapping intervals share a
band, no false precision) + SVG graph (bars + CI whiskers) + pairwise
comparison table (`significant/directional/inconclusive` — the word
"winner" is forbidden).

**Security board (flat v1 data):**

```bash
python3 $EMOX/shared/render_security_board.py $OUT/results/raw/security_*.json --out $OUT/reports/security-board/
open $OUT/reports/security-board/security-board.html
```

Rank table + green/red matrix per test (S1–S5) + tokens/secs +
scope status — one model or N.

The view contains: Capability Profile bars + failure fingerprint bars
+ Tier A/B efficiency + 95% CI interval + `claim_tier` /
`reasoning_conditions` / gates table — from the raw bundle only, no
internet and no dependencies (inline SVG/CSS).

Keys via environment, not flags:

```bash
export OPENAI_BASE_URL="https://HOST/v1" OPENAI_API_KEY="$KEY" OPENAI_MODEL="MODEL-ID"
```

## Reading the result

- The bundle: `results/raw/RUN-ID/{manifest,events,responses,environment}.json*` — never modified.
- Display: Capability Profile + failure fingerprint + efficiency + uncertainty (95% CI) — **never reduce to one number** (SPEC §B61).
- Comparing two models: `compare_models` in `shared/report_v2.py` only — allowed states are `significant / directional / inconclusive`, and the word "winner" is forbidden.

## Comparison warning (mandatory in every report)

Record the host agent harness (name + version) next to every result
tagged by this skill. Any comparison against direct `run.py` results is
labeled **NON-COMPARABLE** (harness+model is the unit — SPEC §B58,
`adapters/ADAPTERS.md` §0).

## What this skill does not do

- Safety suites S3–S5 need scope approval (`EMOX_SCOPE_APPROVED=1` + `EMOX_SCOPE_TARGET=synthetic:…`) — without approval they refuse fail-closed, never bypass them.
- The hidden suite (`code25-hidden`) needs `--hidden-ok` — never use it for public claims.
- `vision` needs a multimodal endpoint; `computer-use` is experimental (PILOT).

## Per-agent install (opencode / pi / forge-agent / codex / hermes-agent)

> Note: **there is no such thing as forgecode** — the correct name is
> **forge-agent** (the `forge-agent`/`fa` command), whose mechanism is
> JS plugins in `~/.deepseek-agent/tools/` — it does not read SKILL.md.

| Agent | Skill mechanism | Install |
|---|---|---|
| opencode | Custom commands + MCP (no native SKILL.md) | Copy `commands/emo.md` to the custom-commands dir, or attach the MCP server: `opencode mcp add emo-x -- python3 /path/to/emo-x/mcp-server/server.py` — see `mcp-server/` |
| pi | Native `--skill <path>` (loads a file or dir, repeatable) | `pi --skill /path/to/emo-x/SKILL.md "benchmark this model"` — loads directly, no install |
| hermes-agent | Native `SKILL.md` skills (frontmatter `name/description/version/category`) — local `./.hermes/skills/` + `skills trust`, or `~/.hermes/skills/`, or `publish`/`sync` | **Installed in this repo**: `.hermes/skills/emo-x/SKILL.md` — run `hermes skills trust` at the root, then it loads automatically |
| forge-agent (DeepSeek/Gemini) | **JS plugins** (`~/.deepseek-agent/tools/*.js`) — no SKILL.md | Copy `adapters/forge_agent_emo_x.js` to `~/.deepseek-agent/tools/emo_x.js` (installed and verified: `forge-agent --list-plugins` shows `emo_x`) |
| codex CLI | `~/.codex/commands/` + shell | Copy `commands/emo.md` to `~/.codex/commands/emo.md`, then `/emo code25` |
| kilo / cline | VS Code extensions **with no CLI** — no automatic loading possible | manual-trace: run the commands from `SKILL.md` by hand and record results with the same fields |

hermes-specific constraint: `run.py` commands execute via hermes
terminal tools (`--yolo` for non-interactive runs); record
`cli_command_argv` and the hermes version (`hermes --version`) inside
every result's `harness` — same NON-COMPARABLE rule as above.
