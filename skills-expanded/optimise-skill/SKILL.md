---
name: optimise-skill
description: Use when tuning/optimising/"training" a skill's judge-shaped rubric (a single text document that makes a recurring, scorable decision) against outcome-labelled evidence — e.g. "train the triage rubric", "optimise the reviewer-severity rubric", or the command "/optimise-skill <consumer>". Runs on the Claude Max subscription via the CLI. Behavioural-only (it does NOT tune a skill's description for triggering — that stays with skill-creator). The home for skill-optimisation methodology.
---

# optimise-skill

A **decision-policy optimiser**. It tunes ONE judge-shaped document (a rubric that
makes a recurring, scorable decision) against an outcome-labelled corpus, accepting
an edited rubric only when a held-out score strictly improves and adversarial gates
pass. It adopts `microsoft/SkillOpt` (on OPRO foundations) as its `optimiser_engine`,
vendored unedited under `vendor/skillopt/`; everything skill-specific lives in the
rails outside it.

**Announce at start:** "I'm using optimise-skill to tune `<target>` against its corpus (autonomy: `<preset>`)."

It is **behavioural-only**. Tuning a skill's `description:` so Claude *invokes* it is a
different job (different artifact, signal, lifecycle) and stays with the official
`skill-creator`. See `CHARTER.md` for the full design and `dev/papers.md` for the
SkillOpt/OPRO lineage.

## Requirements

Run these from the `optimise-skill/` directory:

- **Python 3.10+** (tested on 3.13) with **PyYAML** — `pip install -r requirements.txt`. PyYAML is the only runtime dependency; the vendored SkillOpt's heavier backends (openai, azure, ray, …) are optional and unused on the default path.
- **Live tuning** picks a provider via the manifest's `model:` field:
  - `model: claude` (default) — needs the **`claude` CLI** + a **Claude Max subscription** (shells out to `claude -p`; billed against Max, not the metered API).
  - `model: openai` — for users **without Max**: `pip install openai` and set `OPENAI_API_KEY` (pay-as-you-go OpenAI billing; Azure OpenAI works similarly via SkillOpt's backend). Note: there is no Anthropic-HTTP-API backend, so using *Claude* here means the CLI/subscription, not an Anthropic API key.
- **Tests:** `pip install pytest && python3 -m pytest tests/` — runs with stub judges, no LLM required.

## When to use — the durable decision rule

Apply this to any signal, any skill, before making it a target:

> *Is it a recurring decision made by ONE tunable text document, where each decision
> is scorable and you can counterfactually imagine the edited document scoring better,
> with enough volume to hold out?*
>
> **Yes → an optimise-skill target.**
> **No → human-triage (one-off fixes, via a judge-shaped edit-queue) or monitoring (metrics).**

A complex orchestration skill has *several* recurring decision surfaces. Factor each
into its own judge-shaped rubric and it becomes its own target — **same process, N
targets, each earning its place**. Targets are tuned **independently**, never pooled
into one corpus (a held-out gate over mixed signals is meaningless).

## The three signals — only the first feeds the optimiser

| Signal | Optimiser input? | Where it goes instead |
|---|---|---|
| **(a) per-decision policy labels** | **YES** | projected into the standardised markdown corpus |
| **(b) one-off playbook fixes** (multi-file, sparse, non-counterfactual) | **NO** | a human + a judge-shaped edit-queue |
| **(c) run-health metrics** (aggregates, not a decision) | **NO** | a dashboard / regression alarm; optionally a weak prior into (a) |

This skill consumes **only grain (a)**. That is what keeps the optimiser sound: no
unbounded, ungated, badly-attributed edits.

## What a consumer supplies

Per target, an `optimisation/` directory:

```
optimisation/
  manifest.yaml          # the contract (see references/contract.md)
  rubric.md              # the ONE tunable document (the manifest's `target`)
  corpus/{train,val,test}/*.md   # standardised-markdown corpus (grain (a))
  holdout/*.md           # adversarial score-gate rows the trainer never sees (incidents / reversals)
  guards.py              # OPTIONAL — consumer anti-degeneracy code (e.g. an escalation-rate cap)
  scorer.py              # OPTIONAL — omit → default agreement-with-label scorer (auto-loaded if declared)
```

`holdout/*.md` feeds the POST-GATE score gate (it must be non-empty for a candidate to
promote). Pre-existing fixtures are **referenced where they already exist, never
duplicated** — and where they're not markdown (e.g. a consumer's JSON incident fixtures),
a consumer either projects them into holdout rows or reads them directly in `guards.py`.

## How it runs (the rails, around the unchanged trainer)

`scripts/optimise.py`:

1. **PRE-FLIGHT** — `validate_manifest.py` checks the contract; `md_corpus.py` loads
   the markdown corpus into the vendored engine's items; the baseline rubric is run
   through the guards as a sanity check.
2. **TRAIN** — `ReflACTTrainer(cfg, adapter).train()` **unchanged**: its own
   Rollout → Reflect → Edit → Gate loop with an internal strict-improve `val` gate.
   The `CorpusJudgeAdapter` re-runs the *candidate* rubric (the judge) on each recorded
   context and scores its verdict against the stored label — this is what gives a
   gradient (pure label-replay would score every candidate identically).
3. **POST-GATE** — an adversarial `holdout/` the trainer never saw + the consumer
   `guards.py` + an engine-owned incident **meta-test** (enforces every holdout row
   flagged `incident: true`; a consumer may also carry must-catch enforcement in its
   own `guards.py`, as an automated-loop or reviewer-severity consumer does) → the **autonomy map** decides
   promote-vs-propose → human gate(s) if the policy declares any → write a versioned
   rubric + provenance.

## Running as a command — `/optimise-skill <consumer>`

When invoked as a command (or asked conversationally to "train/optimise the <X> rubric"),
resolve the argument to a manifest and run it:

1. **Resolve the target.** A consumer name → `~/.claude/skills/<name>/optimisation/manifest.yaml`.
   A path ending in `manifest.yaml` → use as-is. No arg → ask which consumer.
2. **Run it** (subscription; bounded for an interactive run):
   ```bash
   python3 ~/.claude/skills/optimise-skill/scripts/run.py <resolved-manifest> --max-steps 1
   ```
   Drop `--max-steps` for a full run once real outcome labels exist.
3. **Report** the JSON summary: the `action` (propose/auto-promote/reject), baseline vs
   candidate score, any guard/meta violations, and the written `candidate_path` —
   then offer to show the proposed rubric diff.

A run needs a logged-in Claude Code (this is the Max subscription). It takes a couple of
minutes (it fans many `claude` calls across the corpus + holdout).

## Triggering a run (conversational or scheduled)

One entrypoint — `scripts/run.py` — is what both a conversational "train the triage
rubric" and a scheduled routine call:

```bash
python3 ~/.claude/skills/optimise-skill/scripts/run.py \
  ~/.claude/skills/<consumer>/optimisation/manifest.yaml --change-category safe-code
```

It runs PRE-FLIGHT → train → POST-GATE and prints a JSON summary (decision, scores,
violations, the written candidate + provenance paths). `--max-steps N` bounds the run
(use `1` for a cheap smoke / short scheduled run). To run it continuously, point a
scheduled agent (`/schedule`) or a cron at the same command on whatever cadence fits.

**Execution model — the Max subscription, via the Claude CLI.** With `model: claude`
(the default both consumers use), every model call goes through the **Claude CLI** = your
**Max subscription**, for BOTH roles: the judge/rollout is the CLI judge
(`scripts/claude_code_judge.py`), and the optimiser is SkillOpt's `claude_chat` backend —
which in this vendored SkillOpt **is the CLI** (`vendor/skillopt/model/claude_backend.py`
shells out to `claude -p`), not the HTTP API. There is **no Anthropic-API backend** in
this engine at all. The run also scrubs `ANTHROPIC_API_KEY` / `ANTHROPIC_AUTH_TOKEN` /
Bedrock / Vertex from its environment so a stray key can't divert the CLI to metered
billing. **Cost model — effective 15 Jun 2026:** programmatic `claude -p` (every call this
engine makes) no longer draws the high-capacity *interactive* subscription; it draws a
**separate, capped, non-rollover Agent-SDK credit pool** (Pro $20 / Max-5x $100 / Max-20x
$200 per month) at API rates, and *pauses* when exhausted (overflow stays off — the env-scrub
above now also prevents silent pay-as-you-go). Architecture is unchanged; only the cost model
moved — budget bounded/scheduled runs against the monthly credit. Prerequisite: a logged-in Claude Code on the machine (or a `CLAUDE_CODE_OAUTH_TOKEN`
from `claude setup-token` for headless/scheduled runs). The only non-subscription path is a
different provider (`model: openai` → `openai_chat`), which needs its own key and an
injected judge — not used here. For tests/shadow the judge is injected as a deterministic
stub (no LLM). Contract details are in `references/contract.md`.

*Validated 31 May 2026:* a bounded live run against a real consumer completed entirely on the
subscription — the optimiser produced a real rubric edit and POST-GATE returned a
`propose` decision with provenance written (see the rollout-parallelism note: POST-GATE
fans the judge out across the holdout, default 6 workers).

> **Continuous improvement caveat:** the *machinery and trigger* run now on the
> subscription, but genuine improvement needs an outcome-labelled corpus. Today the
> corpora are authored/seed (shadow → propose only). The loop becomes load-bearing as the
> extractors fill `corpus/` from live decisions (e.g. an automated loop's per-decision
> corpus, or a reviewer-severity ledger) with `outcome-derived` labels over time.

## Logging & version control of the skill

Two layers record how a skill evolves:
1. **`optimisation/ledger.md`** (committed, append-only) — `run.py` writes one row per run:
   date, model, baseline→candidate score (Δ), action, promotable, violation counts, the
   candidate's content hash, and the candidate filename. This logs **every** run, including
   shadow proposals that were never promoted — the "what the optimiser tried and why" history.
2. **The target rubric's git history** — when a candidate is *promoted*, that is a commit to
   the rubric file itself, so `git log` on (e.g.) a judge-shaped skill's `rubric.md` is the
   canonical record of *what the skill is now*. Ledger + rubric git history together = the full evolution.

Heavy per-run artifacts (trainer state, predictions, `candidate_vNNNN.md`) land in
`optimisation/runs/` and are **gitignored**; the ledger is the durable, committed summary.

## Long runs & timeouts

A real run (many steps over a real corpus) makes hundreds of slow `claude` calls and will
exceed any single interactive timeout. Handle it by **bounding + detaching + going
incremental**, not one long blocking run:
- `--max-steps N` bounds the work (POST-GATE rollout is already parallelised, default 6 workers).
- **Run detached** so it isn't tied to an interactive turn, leaving a trail in the ledger + a log:
  ```bash
  nohup python3 ~/.claude/skills/optimise-skill/scripts/run.py \
    ~/.claude/skills/<consumer>/optimisation/manifest.yaml --max-steps 2 \
    > /tmp/optimise-run.log 2>&1 &
  ```
- **Incremental on a schedule** — short bounded runs (a couple of steps) on a routine,
  accumulating in the ledger, rather than one marathon. This is both the timeout fix and the
  continuous-improvement cadence. (Defer turning the schedule on until real outcome labels exist.)

## Autonomy (presets are sugar over a per-category action map)

`shadow` = all propose-only (the zero-risk phase that mints fresh agreement labels);
`assisted` = `safe-*` auto-act, rest propose-only; `autonomous` = all gated auto-act.
**Engine invariants:** an `unknown` category is always propose-only; `permanent_gates`
never auto-flip; `shadow` always proposes. Human gates are optional per-skill policy
(0..N) — an automated-loop skill might keep `financial`/`irreversible` permanently gated;
a low-stakes skill declares none.

> **User-facing standard — two words, owned by `upskill`** (to keep the choice low-cognitive-load): **ask-me-first** (`= shadow`, the default) / **just-do-it** (`= autonomous`), set per decision-type. The three internal presets stay as the mechanism; operators only ever pick the two. The graduation rule is **not** an approval count — a decision-type goes just-do-it only when it is **undoable** (reversibility is the line, reusing a merge-gating allow-list + git-revertibility rule), its **review provably catches that type's incident fixtures** (the calibration gate — same idea as "enable autonomous-financial only after the panel escalates every incident-regression fixture"), **and a human flips it on**. Un-undoable actions (money, statutory submissions, deletion, real sends, `config`/`secrets`, unreverted schema) **never** graduate. See `upskill/SKILL.md` § Autonomy for the full plain-language model; this engine supplies the `decide_action` map underneath it.

## Onboarding a new consumer

`python3 scripts/setup.py <path-to>/optimisation --apply` scaffolds the dir (idempotent;
dry-run by default; `--check` reports readiness; `--force` backs up to `*.bak`), mirroring the
conventional `optimisation/` layout. `scripts/seed.py` generates synthetic cold-start seeds (positives + manufactured
negatives, `source: synthetic`) over an injectable runner. Every generated draft carries
`PENDING_REVIEW`; a run refuses until a human sharpens the drafts and deletes the sentinels.
See `references/contract.md` §9–§10. Capture of live decisions is via
`scripts/decision_record.py --corpus-dir <consumer-corpus-dir>` (§9), wired additively into
the producing skill (e.g. an automated loop).

## Status

Engine + rails built and RED-verified against fixtures. The "build now" slice is
implemented (enriched decision-capture, the thin capture path, extractor enrichment, the
promotion-gate source guard, median-of-N + margin + trust-stratified split, the setup
scaffolder + synthetic seeding, the process-emitting judge) — all in `scripts/`, `vendor/`
untouched. Two consumers exist (one tuning an automated loop's triage rubric, one a
reviewer-severity rubric), so `schema_version: 1` is frozen.
