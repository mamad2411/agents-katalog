---
name: twin-analyze
agents: [orchestrator]
domain: twin
description: >-
  The multi-model analysis seam — pack a twin recording (+ binding map + property sidecar) into one
  deterministic bundle and have a NON-Anthropic model narrate a window of it, back as an advisory
  Markdown report the FRAMEWORK writes (never the worker). Two contracts, not a worker: bundle in
  (tools/analyze/bundle.js), report out (reports/analysis/<date>-<task>.md); the worker is a swappable
  adapter (openai-compatible endpoint, Hermes, or a human pasting the bundle into any chat UI). Use it
  to summarize a day of tag history, narrate anomalies in a recording, or draft an inspection report
  from binding data — advisory only, provider+model always named. This skill is the OPERATOR MANUAL:
  when to run `npm run analyze`, how to configure a worker, and the guardrails. NOT a build/verify gate
  (analysis gates nothing and writes no project files), NOT anomaly DETECTION (v1 narrates the
  deterministic stats block), and NOT for wiring a live source (that is twin-bind-data).
---

# Twin analyze (recording → bundle → other-model narration → advisory report)

Claude Code stays the build-and-verify system; **other models plug in here for analysis**. The seam is
the two contracts — a deterministic **bundle in**, an advisory **report out** — so the worker is
swappable: an OpenAI-compatible endpoint, a Hermes run, or a human pasting the bundle into any chat UI.

```
recording.ndjson ─┐
binding_map.json ─┼─▶ bundle.js ─▶ bundle.json ─▶ [worker: other model] ─▶ framework writes ─▶
duplex_props.json ┘   (data-in)     ≤ ~100 KB       narration only            reports/analysis/<date>-<task>.md
```

The worker returns **only a body string**; the framework wraps it in provenance frontmatter (task,
worker, provider/model, bundle sha256, window) and drops it under `reports/analysis/` — nowhere else.

## When to run it

- Summarize a recorded window of twin telemetry — a day of tag history, a captured incident window.
- Narrate the movements/excursions/drops the stats block surfaces, in plain language that names the
  bound element ("the boiler wall", not "tag boiler.temp").
- Draft an inspection-report skeleton from binding data for a human to finish.
- To get a bundle you can paste into ANY chat UI by hand — the worker is optional; the contract is the
  product. Build just the bundle with `node tools/analyze/bundle.js … --out bundle.json`.

## When NOT to reach for it

- You want a build/verify gate — analysis is **not** a gate. It writes no project files, moves no
  scene, and `verify_twin.sh` never runs it. It is advisory input, full stop.
- You need anomaly DETECTION — v1 narrates the deterministic stats block (min/max/mean/stddev,
  seq-gaps, range-crossings, max-step-delta). Fancier detection enters only as more pure functions in
  `tools/analyze/stats.js` with the same exact-expectation tests, never as worker cleverness.
- You are wiring a live source or authoring a binding map — that is `twin-bind-data`, not this skill.
- You want to close a loop on plant data — never. A report proposes nothing that acts (guardrail 2).

## The three-task menu

`--task <one of>` selects a reviewed prompt template (`skills/twin-analyze/tasks/*.md`); each states the
role, embeds the honesty rules, and defines the report structure. The bundle JSON is appended verbatim.

| Task                | What it produces                                                                     |
| ------------------- | ------------------------------------------------------------------------------------ |
| `summarize-window`  | A concise, faithful summary of one window: overview, per-tag summary, notable moves. |
| `narrate-anomalies` | Plain-language narration of the seq-gaps, range-crossings, and largest step-deltas.  |
| `inspection-report` | An inspection-report skeleton from the binding context, for a human to complete.     |

## The command

```
npm run analyze -- --task <summarize-window|narrate-anomalies|inspection-report> \
    (--bundle bundle.json | --recording rec.ndjson [--map M] [--sidecar S] \
     [--from-ms A --to-ms B] [--tags t1,t2] [--points-per-tag N] [--allow-oversize])
```

- **`--bundle`** — analyze a bundle you already packed (`node tools/analyze/bundle.js …`).
- **`--recording`** (+ optional `--map`/`--sidecar`/window/tags) — inline-build the bundle through the
  same packager, then analyze it. The size budget (~100 KB, `SIZE_BUDGET_BYTES`) is enforced here too:
  over budget it FAILs with the levers (narrow the window, select `--tags`, lower `--points-per-tag`)
  unless you pass `--allow-oversize` (loud).
- The report lands in `<project>/reports/analysis/<date>-<task>.md`. Project root resolves from
  `GAME_DIR` → `.xenodot.json` `projectDir` → the default sibling (NOT an argv scan — `--task`'s value
  would be misread as a path).

### From a Hive session (the `mcp__ui__analyze` tool)

`npm run analyze` is **canonical**; the same seam is also reachable from a running session as the
`mcp__ui__analyze` tool (same shared dispatch core, so the two never drift). Its args mirror the CLI:
`task` (the whitelist enum), and EITHER `bundle` (a path) OR `recording` (+ optional
`map`/`sidecar`/`fromMs`/`toMs`/`tags`/`pointsPerTag`/`allowOversize`). It **returns an advisory
summary + the report path** — never the raw worker body, and it applies nothing. An unconfigured
worker is the same graceful no-op message. Prefer the CLI for scripted/batch runs; the tool is for
narrating a window from inside the session.

Consent + confinement (accurate statement): an **interactive** session gates each dispatch per call
(a real model call + a file write — allow/deny in the web UI), but **autonomous / all-policy
sessions auto-allow it**. That is WHY the tool **confines every model-supplied file path to the
project root** (realpath-checked, symlink-safe — out-of-tree paths are refused with a graceful
message): the confinement is the load-bearing control, the per-call gate is defense-in-depth.
Residual, stated honestly: in an unattended session the worst case is dispatching **in-project**
files the session could already read to the configured worker endpoint — nothing outside the
project can reach it. The operator-run CLI keeps absolute paths (a human typed them).

## Configure a worker (quickstart)

The default worker is **`openai-compatible`** — one `/v1/chat/completions` POST that covers OpenRouter,
local llama.cpp/Ollama, vLLM, and most hosted "other models". Configure it in `.xenodot.json` (the file
is gitignored — the key lives only here or in env):

```json
{
  "analysis": {
    "worker": "openai-compatible",
    "apiUrl": "https://openrouter.ai/api",
    "apiKey": "sk-…",
    "model": "meta-llama/llama-3.1-70b-instruct"
  }
}
```

Env overrides mirror the Hermes pattern (win over the saved block, no restart):
`ANALYSIS_WORKER`, `ANALYSIS_API_URL`, `ANALYSIS_API_KEY`, `ANALYSIS_MODEL`. A bare local endpoint needs
no key (`apiUrl: "http://localhost:11434"` for Ollama — the Bearer header is omitted when no key is set).

The **`hermes`** worker reuses the existing Hermes runs-API bridge and reads its connection from the
`hermes` config block (not `analysis`) — set `analysis.worker` (or `ANALYSIS_WORKER`) to `hermes` and
Hermes' own provider/model/billing apply. See `HERMES.md`.

Probe before you spend: `npm run analysis:check` confirms the selected worker is configured and the
endpoint answers (`GET /v1/models` — no model run, no charge), printing a one-line verdict.

## Graceful absence (guardrail 3)

An **unconfigured** worker is a no-op with a clear message pointing at setup — never a crash, never a
half-written report:

```
analyze: worker 'openai-compatible' is not configured — analysis.apiUrl is not set — point it at an
OpenAI-compatible endpoint (OpenRouter, Ollama, vLLM, …) in .xenodot.json `analysis` block or the
ANALYSIS_API_URL env var.
No report was written. Configure the worker (see above), then re-run.
```

Exit is nonzero (the job could not be produced, same precedent as `npm run hermes:check`). The framework
behaves identically to before otherwise — analysis is purely additive.

## Guardrails (inherited verbatim from the Hermes acceptance list)

1. Analysis workers never write project files; the framework writes only `reports/analysis/`.
2. Output is advisory input for humans/gated agents, never an action.
3. Unconfigured → no-op with a clear message.
4. Every report names its provider+model and its bundle hash.
5. No machine-access of any kind on any worker path.

These are not aspirations — they are enforced: the adapter module carries no `node:fs`/`node:child_process`
(guardrails 1 + 5, greppable), the report writer whitelists the task before it builds a path under
`reports/analysis/` and nowhere else (guardrails 1 + 4), and `configured()` returns a reason string rather
than throwing (guardrail 3).

## Honesty rules (summary — the templates carry the verbatim text)

Every task template embeds the standing wording rules; do NOT restate or edit them here. In short: narrate
the **data**, never claim a physics simulation/solver/live sensor unless the bundle says so; every cited
number must come from the bundle's `stats`/`series`; name elements from `bindings`, not raw tags; propose
no action. The full text and the frontmatter contract are in
[`references/report-format.md`](references/report-format.md); the bundle shape and its determinism/size
guarantees are in [`references/bundle-schema.md`](references/bundle-schema.md).

## RTK note

Prefix shell commands with `rtk` as usual. `npm run analyze` / `npm run analysis:check` and the bare-node
`tools/analyze/bundle.js` run without an rtk filter (passthrough). Never reference rtk inside the tool
sources.
