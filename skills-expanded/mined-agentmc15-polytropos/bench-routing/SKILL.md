---
name: bench-routing
description: Rank published benchmark entries (Artificial Analysis Intelligence Index), recommend a model+effort per orchestration role given what each harness can actually dispatch, and check that recommendation against this repo's OWN measured routing outcomes. Use when the user asks whether a new/higher model should replace what a role currently runs on, wants a benchmark-informed routing recommendation, or asks "should we upgrade X to Y for this role" — the answer must be checked against the ledger, not just the benchmark.
allowed-tools: Bash, Read
---

# Bench routing

Run the engine that ships with this plugin. Use the `${CLAUDE_PLUGIN_ROOT}` env var Claude Code
sets for plugin-executed content; if it is unset, fall back to resolving
`../../bin/bench_routing.py` relative to this SKILL.md to an absolute path.

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/bin/bench_routing.py" rank --top 10
python3 "${CLAUDE_PLUGIN_ROOT}/bin/bench_routing.py" roles --harness claude
python3 "${CLAUDE_PLUGIN_ROOT}/bin/bench_routing.py" compare
python3 "${CLAUDE_PLUGIN_ROOT}/bin/bench_routing.py" demo
```

The dataset it reads, `${CLAUDE_PLUGIN_ROOT}/data/benchmarks.aa.json`, is a screenshot-transcribed
snapshot of the Artificial Analysis Intelligence Index — a general-capability composite, not this
repo's pricing and not a bill. Never edit that file from this skill.

## Subcommands

- **`rank`** — ranked tables from the benchmark file: by intelligence index, by VALUE (index /
  usd_per_task — a ranking ratio, never a price), and a "capability frontier" (cheapest entry
  clearing each index floor). `--provider P`, `--model M`, `--top N`.
- **`roles`** — per-harness role recommendation (`--harness claude|codex|copilot|all`).
  Availability is derived at run time from `data/pricing.json` / `pricing.codex.json` /
  `pricing.copilot.json` — a benchmark entry that matches no available model is reported
  UNAVAILABLE, never silently dropped. Role floors are this repo's own editorial judgement
  (`ROLE_POLICY` in the script), overridable with a repeatable `--floor "role=N"`.
- **`compare`** — THE ONE TO REACH FOR when the question is "should we route role X to a
  different/higher model." Joins each `roles` recommendation (Claude harness only — the only
  harness whose models map onto this repo's own haiku/sonnet/opus/frontier tiers) against this
  repo's own measured first-try rate per tier (reusing `bin/routing_scorecard.py`'s ledger, never
  re-parsed) — **but only for the role that ledger actually evidences.** This repo's ledger
  records per-TASK outcomes, which is implementer work; it carries no per-role result data for
  architect/planner, reviewer, orchestrator, or verifier, so those roles are reported
  `no_role_evidence` (benchmark pick stands unchallenged, no rate is quoted) rather than judged
  on a number that measures a different job function. Only `implementer` gets a real verdict:
  states plainly whether the ledger CONTRADICTS the benchmark's implied upgrade, and reports the
  MARGINAL GAIN — not just both numbers. **Measured outcomes win.** A nominally-positive gain
  that is small (e.g. "opus already clears ~100% vs sonnet ~97%") is reported as `not_supported`,
  because a few points don't justify the routing change. Where a tier has too few finished
  tasks, it says "insufficient sample" rather than guessing. `mechanical sweep` gets
  `cheapest_tier` when its pick lands on the cheapest repo tier — a tier-ladder fact, not a
  borrowed outcome claim.
- **`demo`** — synthetic smoke, no real files touched. Use to sanity-check the tool itself.

## Presenting the results

1. **Lead with `compare`'s verdict**, not the raw benchmark ranking — the benchmark is a prior;
   the ledger is what this repo has actually observed. If `compare` says `not_supported`, say so
   plainly and name the marginal gain; do not soften it into "might be worth considering."
2. **Never present `usd_per_task` as a bill.** It is a benchmark-workload cost for relative
   ranking only. This repo's actual dollars come from `routing_scorecard` / `cost_report`, a
   different measurement — never add the two together.
3. **Surface coverage gaps.** If the model `compare` recommends is measured at fewer effort
   points than the tier-mate it would displace (the tool computes and reports this — e.g. an
   "Opus at medium beats Sonnet" claim when Sonnet has no medium-effort benchmark entry), repeat
   that caveat: the comparison covers only the effort points actually measured.
4. **State the index's scope.** The Intelligence Index is a general-capability composite; Coding
   Index and Agentic Index are separate boards not included here. A strong entry is not
   automatically strong at agentic tool use — say this before recommending a routing change for
   an agentic role (implementer, verifier, orchestrator, mechanical sweep).
5. **Name the provenance.** The benchmark file is screenshot-transcribed (see its `cached_date` /
   `transcribed_from`), not an API export — flag it as re-verify-worthy if it looks stale.
6. **Never borrow implementer's rate for another role.** If `compare` says `no_role_evidence` for
   architect/planner, reviewer, orchestrator, or verifier, do not paraphrase it as "the ledger
   supports/contradicts this" — say plainly that this repo has no per-role evidence for that role
   (the ledger only measures implementer task outcomes) and the benchmark recommendation stands
   unchallenged either way.
