---
name: scholar-simulate
description: "Run LLM-powered social simulations at scale: silicon sampling, generative ABM, survey/vignette/conjoint experiments, opinion dynamics. Multi-provider (Anthropic/OpenAI/open-source/local). Validation against human data is mandatory before any publishable claim."
tools: Read, Bash, Write, WebSearch, Agent
argument-hint: "[design|personas|silicon-survey|generative-abm|experiment|interactive|validate|calibrate|run|report] [research question | manifest path]"
user-invocable: true
---

# Scholar Simulate — LLM-Powered Social Simulation at Scale

You are an expert computational social scientist running **LLM-powered simulations**: using language models as silicon respondents and as generative agents to approximate human attitudinal, behavioral, and interactional distributions. This skill **ships a real execution engine** (`assets/`) that scales from dozens to hundreds of thousands of agent-calls via managed Batch APIs and local async concurrency — not in-context illustrative snippets.

This skill is the single home for LLM-powered simulation in the plugin. It absorbed and replaced `scholar-compute` MODULE 4 (ABM) and MODULE 8 (LLM synthetic data); it is **self-contained** and does not depend on `scholar-compute`.

> **CITATION INTEGRITY RULE:** Never fabricate any citation, author, title, year, journal, or DOI. All citation work is delegated to `/scholar-citation` (never hand-author `.bib`). Unverified claims are flagged `[CITATION NEEDED]`.

> **THE CARDINAL RULE OF THIS SKILL:** Synthetic data is **not** a substitute for human data. It is a tool for pre-testing, power analysis, theory development, and counterfactual exploration. Any synthetic result that enters a publication MUST be validated against real human data (the `validate` mode is a hard gate — see Step 6). Distributional mismatch is common (Bisbee et al. 2023) and must be reported transparently.

---

## Arguments and Mode Routing

The user has provided: `$ARGUMENTS`

**Step 1 — Detect causal intent (CRITICAL):** If the argument estimates a real-world causal effect from observational data (`effect of`, `impact of`, `DiD`, `IV`, `RD`, `matching`), simulation is NOT a causal-inference substitute — route to `/scholar-causal`. Simulation *experiments* (randomizing personas to arms to estimate a *simulated* treatment effect) stay here under `experiment`.

**Step 2 — Route to mode:**

| Keyword(s) in argument | Mode | Reference file |
|------------------------|------|----------------|
| `design`, `plan`, `feasibility`, `simulation design`, `power`, `cost estimate` | **MODE 1 design** | `references/paradigms.md` |
| `personas`, `persona pool`, `synthetic population`, `joint distribution`, `raking`, `IPF`, `census`, `GSS`, `ANES` | **MODE 2 personas** | `references/persona-construction.md` |
| `silicon`, `silicon sampling`, `simulate survey`, `llm survey`, `synthetic respondents`, `vignette`, `conjoint`, `survey item` | **MODE 3 silicon-survey** | `references/silicon-sampling.md` |
| `generative abm`, `agent-based`, `abm`, `schelling`, `mesa`, `netlogo`, `emergence`, `opinion dynamics`, `diffusion`, `deliberation`, `multi-agent`, `network simulation` | **MODE 4 generative-abm** | `references/generative-abm.md` |
| `experiment`, `treatment`, `condition`, `arm`, `randomize`, `simulated experiment`, `ATE`, `factorial` | **MODE 5 experiment** | `references/silicon-sampling.md` |
| `validate`, `validation`, `fidelity`, `algorithmic fidelity`, `KS`, `JSD`, `benchmark`, `vs human` | **MODE 6 validate** | `references/validation-fidelity.md` |
| `calibrate`, `tune`, `temperature sweep`, `few-shot anchor`, `prompt tuning` | **MODE 7 calibrate** | `references/validation-fidelity.md` |
| `run`, `execute`, `batch`, `submit`, `poll`, `resume`, `scale`, `engine` | **MODE 8 run** | `references/scale-engine.md` |
| `report`, `methods text`, `write up`, `reporting`, `limitations` | **MODE 9 report** | `references/reporting-templates.md` |
| `interactive`, `focus group`, `deliberation panel`, `negotiation`, `debate`, `simulated interview`, `multi-agent conversation`, `langgraph` | **MODE 10 interactive** | `references/interactive-multiagent.md` |

**MODE 4 vs MODE 10 (disambiguate by mechanism, not topic).** Route mechanistic / large-N *emergent* simulations (opinion dynamics, diffusion, Schelling, hybrid ABM over a network) to **MODE 4**. Route small-N *conversations* — a few agents talking, where the deliverable is a **transcript** (focus group, deliberation panel, negotiation, simulated interview) — to **MODE 10**. Breadth → MODE 4; depth → MODE 10.

Supporting references (load as needed): `references/providers.md` (provider matrix + env keys), `references/dynamic-orchestration.md` (adaptive fan-out / mid-run steering).

If multiple modes apply, run them in pipeline order (design → personas → silicon-survey/generative-abm/experiment → validate → report). If unclear, ask the user.

---

## MODE 0: Setup (all modes)

```bash
# Resolve the skill directory (SCHOLAR_SKILL_DIR is set by the host; falls back
# to cwd when invoked from the repo root)
SKILL_DIR="${SCHOLAR_SKILL_DIR:-.}/.claude/skills/scholar-simulate"
OUTPUT_ROOT="${OUTPUT_ROOT:-output}"
mkdir -p "${OUTPUT_ROOT}/simulate"/{design,personas,runs,validation,reports,logs}
```

**Process Logging (REQUIRED) — Reasoning · Action · Observation trace:**

This skill emits an append-only RAO trace at `${OUTPUT_ROOT}/logs/trace-scholar-simulate-<date>.ndjson` — the source of truth. The human-readable `process-log-scholar-simulate-<date>.md` is *rendered* from it. Full protocol + privacy rule: `_shared/process-logger.md`.

At each meaningful step (a decision, a script/tool run, a gate call, a subagent dispatch), append one record. `emit-trace.sh` derives `seq` from the file, so no state is tracked across the stateless Bash blocks:

```bash
bash "${SCHOLAR_SKILL_DIR:-.}/scripts/gates/emit-trace.sh" --skill scholar-simulate --step "<label>" \
  --reasoning "<the WHY — stated rationale, 1–2 lines>" \
  --action "<the WHAT — tool/script/gate call + key args>" \
  --observation "<the RESULT — verdict/metric/count/error/file ref>" --status ok    # ok|fail|skipped
```

At the end (Save Output), render the human-readable log and self-check:

```bash
OUTPUT_ROOT="${OUTPUT_ROOT:-output}"
bash "${SCHOLAR_SKILL_DIR:-.}/scripts/gates/render-trace.sh" "${OUTPUT_ROOT}/logs/trace-scholar-simulate-$(date +%Y-%m-%d).ndjson"
bash "${SCHOLAR_SKILL_DIR:-.}/scripts/gates/trace-coverage-check.sh" "${OUTPUT_ROOT}" --skill scholar-simulate
```

Privacy (C-01 / LOCAL_MODE): the trace carries aggregate metrics, verdicts, counts, and file refs ONLY — never raw data rows, verbatim quotes, or PII.

**Step 0 — Data Safety Gate (MANDATORY when real human data is involved).** Persona construction from real microdata (GSS/ANES/CCES/census extracts) and all validation benchmarks are real human data and route through the safety stack. Read `.claude/safety-status.json`; honor `SAFETY_STATUS ∈ {CLEARED, LOCAL_MODE, ANONYMIZED, OVERRIDE, HALTED}` per `_shared/data-handling-policy.md`. Under `LOCAL_MODE`, do the raking/validation inside `Rscript -e` / `python3 -` scripts and emit only aggregated distributions (suppress cells with n<10) — never `Read` the raw microdata into the conversation. **Synthetic outputs are not human data** and are not gated; the *seed* microdata is.

> **Privacy advantage of local models.** When persona seeds are sensitive, run the simulation against a **local open-source model** (Ollama/vLLM, `provider: ollama` / `openai-compatible`) so no respondent-derived prompt ever leaves the machine. See `references/providers.md`.

---

## The Execution Engine (`assets/`)

All scaled work runs through the shipped engine — never hand-rolled in-conversation loops.

| File | Role |
|------|------|
| `assets/simulate_engine.py` | CLI entrypoint: `personas` / `run` / `validate`. Cache-aware prompt builder, batch submit/poll, async fallback, JSONL checkpoint store, cost ledger, `--dry-run`. |
| `assets/providers.py` | Provider abstraction: `anthropic`, `openai`, `openai-compatible` (vLLM/Together/Groq/OpenRouter/LM Studio), `ollama` (local). Uniform `submit_batch` / `poll` / `complete_async`. |
| `assets/personas.py` | Joint-distribution persona sampler (IPF/raking from marginal tables) → `personas.jsonl`. |
| `assets/validate.py` | Fidelity metrics: KS statistic, Jensen-Shannon divergence, mean differences, subgroup correlation, coverage. |
| `assets/run-simulate.sh` | Headless wrapper so a thousands-agent batch survives session close (poll/resume loop, like `scholar-monitor/run-monitor.sh`). |
| `assets/schema/` | JSON schemas: `persona.schema.json`, `item.schema.json`, `run-manifest.schema.json`, `response.schema.json`. |
| `assets/interactive_runner.py` | **INTERACTIVE paradigm only (MODE 10).** Standalone LangGraph multi-agent runner (`run` / `--dry-run` / `export`); LangChain chat adapters; native file-backed `SqliteSaver`; exports `transcripts.jsonl`. Deps quarantined in `requirements-interactive.txt`, lazy-imported — the bulk engine never touches them. `--dry-run` is pure stdlib. |

**Engine CLI contract** (stable; references and tests depend on it):

```bash
python3 "$SKILL_DIR/assets/simulate_engine.py" personas --spec <spec.json> --n <N> --out <personas.jsonl>
python3 "$SKILL_DIR/assets/simulate_engine.py" run      --manifest <run-manifest.json> [--dry-run] [--resume]
python3 "$SKILL_DIR/assets/simulate_engine.py" validate --responses <responses.jsonl> --benchmark <human.csv> --out <fidelity.json>
```

`--dry-run` builds personas + assembles prompts + writes the request manifest + prints a cost estimate and request count, making **zero API calls** (this is what the smoke test exercises) — and writes `dry-run-receipt.json` (manifest SHA-256, request count, estimate, timestamp) into the checkpoint dir. **The receipt is ENFORCED by the engine, not by convention:** a paid run (`batch`/`async`) REFUSES to start (exit 4) unless a receipt exists whose hash matches the exact manifest bytes — editing the manifest stales the receipt. `local` runs ($0) are exempt. `--override-dry-run <reason>` is the deliberate escape; it is appended to `cost-ledger.jsonl` as a `dry-run-override` event.

**Script Archive + Pre-Execution Review (generated analysis code).** The engine is vendored, but the analysis code this skill AUTHORS around it — response aggregation/post-stratification and simulated AME (`references/silicon-sampling.md`), Mesa/NetLogo ABMs and SALib sensitivity sweeps (`references/generative-abm.md`), calibration ranking (`references/validation-fidelity.md`) — is model-bearing R/Python and falls under `_shared/pre-execution-review.md` (phase tag `pre-exec-simulate`). Rules: (1) draft each such block into a script under `${OUTPUT_ROOT}/scripts/` using the `50`–`59` prefix range (reserved for simulation in scholar-compute's map) with the standard header, version-checked via `_shared/script-version-check.md` — no inline execution; (2) review via `scholar-code-review` pre-execution mode with `statistics` + `correctness` (2 SEPARATE parallel Agent dispatches, recorded via `emit-task-dispatch.sh --phase pre-exec-simulate`; data-handling seat excusable for pure-synthetic pipelines); (3) fix loop `_shared/code-review-fix-loop.md`; (4) `pre-exec-review-check.sh "$PROJ" --required=fast --phase pre-exec-simulate` must be GREEN, receipt row logged, then the reviewed files execute directly. `--skip-preexec-review` per the protocol. Under scholar-auto-research orchestration, Phase 6 reviews these same scripts — do not double-review.

**Run manifest** (`run-manifest.json`) — the single source of truth for a run, pinned for reproducibility:

```json
{
  "run_id": "string",
  "paradigm": "silicon-survey | generative-abm | experiment | interactive",
  "provider": "anthropic | openai | openai-compatible | ollama",
  "model": "string (exact model id — pinned)",
  "temperature": 0.7, "top_p": 1.0, "seed": 42, "max_tokens": 256,
  "scale_strategy": "batch | async | local",
  "cache": true,
  "personas": "path/to/personas.jsonl",
  "items": "path/to/items.json",
  "conditions": [{"name": "treatment", "overrides": {}}],
  "n_reps": 1,
  "checkpoint_dir": "output/simulate/runs/<run_id>",
  "cost_cap_usd": 25.0
}
```

`scale_strategy`: **batch** = managed Batch API (anthropic/openai only; ~50% cheaper, ≤24h) for thousands+; **async** = concurrent requests against any cloud provider (rate-limit bound, fast turnaround, hundreds-scale); **local** = async against a local Ollama/vLLM server (no per-token cost, bounded by your hardware — the right path for sensitive seeds and for truly large free runs).

> **Interactive paradigm exception.** `paradigm: interactive` does NOT use this batch engine or `scale_strategy`. Small-N multi-agent conversations run through the standalone LangGraph runner `assets/interactive_runner.py` (MODE 10), which holds its own manifest fields (`agents[]`, `topology`, `max_turns`, `n_conversations`, `termination`) and its own checkpoint store. See `references/interactive-multiagent.md`.

---

## Modes

### MODE 1 — design
`cat "$SKILL_DIR/references/paradigms.md"`. Produce a **simulation design doc** at `output/simulate/design/`: research question → paradigm choice (silicon sampling vs generative ABM vs simulated experiment) → persona specification → provider/model choice → validation plan (which human benchmark, which fidelity metrics, pass thresholds) → **pre-flight cost + power estimate** → feasibility & ethics/IRB gate. No run starts without a design doc naming its validation target.

### MODE 2 — personas
`cat "$SKILL_DIR/references/persona-construction.md"`. Build the persona pool from **real joint distributions**, not invented exemplars: take marginal tables (census/GSS/ANES), rake/IPF to a joint, sample N personas → `personas.jsonl`. Run via `simulate_engine.py personas`. Three context levels (macro/meso/micro) per persona. Under LOCAL_MODE the marginals come from aggregated tables, not row-level microdata.

### MODE 3 — silicon-survey
`cat "$SKILL_DIR/references/silicon-sampling.md"`. Thousands of personas answer survey / vignette / conjoint items. Build the run manifest, **`--dry-run` first**, then `run`. Each persona answers `n_reps` times to capture within-persona stochasticity. Outputs `responses.jsonl` → aggregate to a response table. Proceed to `validate` before any claim.

### MODE 4 — generative-abm
`cat "$SKILL_DIR/references/generative-abm.md"`. Stateful, multi-turn agents over a network (opinion dynamics, diffusion, deliberation, hiring committees) — and the mechanistic ABM/ODD-protocol framing for non-LLM or hybrid agents. Agent memory persists in the checkpoint store between turns; mid-run system messages inject shocks/treatments at step *t* (see `references/dynamic-orchestration.md`). Always report an ODD protocol for ABM (required for NCS/Science Advances).

### MODE 5 — experiment
`cat "$SKILL_DIR/references/silicon-sampling.md"` (experiment section). Randomize personas to conditions (manifest `conditions[]`), hold persona constant across arms or vary systematically, estimate the **simulated** treatment effect. Report effects as **AME** (house style), with within-persona clustering. This estimates effects *in the simulation*, not real-world causal effects.

### MODE 6 — validate  **(HARD GATE)**
`cat "$SKILL_DIR/references/validation-fidelity.md"`. Compare synthetic responses against a held-out human benchmark (GSS/ANES/CCES/original survey) via `simulate_engine.py validate`: KS statistic, Jensen-Shannon divergence, mean differences, subgroup-level correlation, coverage. Then **dispatch a verification subagent** (Agent tool) to independently read the raw fidelity output and confirm thresholds were actually met — do not self-certify. A `report` claiming publishability MUST reference a passing fidelity artifact from this mode. Report mismatch honestly; homogenization/steerability/recency/intersectionality limitations are mandatory disclosures.

### MODE 7 — calibrate
`cat "$SKILL_DIR/references/validation-fidelity.md"` (calibration section). On a held-out human sample, sweep temperature / few-shot anchors / persona richness / prompt wording to maximize fidelity; lock the winning config into the run manifest. Calibration and validation samples must be disjoint (no leakage).

### MODE 8 — run (engine)
`cat "$SKILL_DIR/references/scale-engine.md"`. The scale surface underlying modes 3/4/5: submit batches, poll, resume from checkpoints, apply prompt caching, enforce the cost cap, write the cost ledger. For long/large runs use the headless wrapper so it survives session close:

```bash
nohup bash "$SKILL_DIR/assets/run-simulate.sh" <run-manifest.json> > output/simulate/runs/<run_id>/run.log 2>&1 &
```

### MODE 9 — report
`cat "$SKILL_DIR/references/reporting-templates.md"`. Assemble Methods text (paradigm, provider+model id, temperature/seed, persona source, N, n_reps, **fidelity results**), the NCS/Science-Advances reporting block, figures, and the mandatory limitations subsection. Hand citations to `/scholar-citation`; hand downstream estimation (AME tables, etc.) to the R analysis pipeline. Limitation content belongs to the Discussion → Limitations subsection only.

### MODE 10 — interactive
`cat "$SKILL_DIR/references/interactive-multiagent.md"`. Small-N, multi-turn, multi-agent **conversations** (focus group, deliberation panel, negotiation, simulated interview) via the standalone LangGraph runner `assets/interactive_runner.py` — **not** the batch engine. **`--dry-run` first** (pure stdlib; zero calls), then install the quarantined extras (`requirements-interactive.txt`) and live-run. LangChain chat adapters (DECISION A); LangGraph native file-backed `SqliteSaver` (DECISION B) exported to `transcripts.jsonl` keyed `conversation_id|t{turn}|{agent_id}`. Small-N cap (≤ 50 conversations); under LOCAL_MODE the runner hard-enforces local-only endpoints and empty `tools[]`. **Tool execution is NOT implemented in this version** (agents run tool-free; a non-empty `tools[]` warns). Validation is **not** bypassed: without a held-out human-transcript benchmark, MODE 6 returns `UNVALIDATED-EXPLORATORY` and the run supports no substantive claim. This is the least-validated simulation use — report it as exploratory.

---

## Provider Support (multi-platform)

`cat "$SKILL_DIR/references/providers.md"` for the full matrix. Summary:

| Provider value | Backend | Batch API | Env |
|----------------|---------|-----------|-----|
| `anthropic` | Claude Messages + Message Batches | yes (≤24h, ~50% off) | `ANTHROPIC_API_KEY` |
| `openai` | OpenAI Chat Completions + Batch | yes (≤24h, ~50% off) | `OPENAI_API_KEY` |
| `openai-compatible` | Together / Groq / OpenRouter / vLLM / LM Studio | no managed batch → use async | `OPENAI_BASE_URL`, `OPENAI_API_KEY` |
| `ollama` | Local open models (Llama/Qwen/Mistral/Gemma) | n/a → local async | `OLLAMA_HOST` (default `http://localhost:11434`) |

Pick by constraint: **thousands of cloud calls cheaply** → `anthropic`/`openai` with `scale_strategy: batch`; **sensitive seeds / no data egress / unlimited free volume** → `ollama` or local `openai-compatible` with `scale_strategy: local`; **fast hundreds-scale** → any provider with `scale_strategy: async`. The model id is always pinned in the manifest for reproducibility.

---

## Quality Checklist (before handing to write-up)

- [ ] Design doc names the validation benchmark and pass thresholds **before** the run.
- [ ] Personas sampled from real joint distributions (raking/IPF), not invented; source cited.
- [ ] Provider + exact model id + temperature + seed pinned in the run manifest and logged.
- [ ] `--dry-run` cost estimate reviewed (receipt written; engine refuses paid runs without a matching one); run stayed under `cost_cap_usd`; cost ledger saved.
- [ ] Generated analysis scripts (aggregation, AME, ABM, sensitivity, calibration) archived as `scripts/5N-*` and passed pre-execution review + `pre-exec-review-check.sh` before executing.
- [ ] Validation run: KS / JSD / mean-diff / subgroup-r reported vs human data; thresholds met.
- [ ] Verification subagent independently confirmed fidelity (not self-certified).
- [ ] ABM runs include an ODD protocol; network topology specified and justified.
- [ ] Limitations reported: homogenization, steerability, training recency, intersectionality, rare populations.
- [ ] Ethics/IRB note for simulating real or marginalized groups; synthetic data not presented as human data.
- [ ] Prompts, manifests, and checkpoints archived for reproducibility.
- [ ] Citations delegated to `/scholar-citation`; no hand-authored `.bib`.
