---
name: evaluate-technology
description: Compare candidate technologies end to end and emit an adr.v1 recommendation. Use when choosing a framework, database, queue, auth provider, observability vendor or any dependency that will be expensive to remove. Fixes weights before scoring, measures maintenance signals instead of citing popularity, resolves licence compatibility from the repository LICENSE, prices operational burden and exit cost in days, then attacks its own result. Not for reversible choices like a formatter or a one-file utility.
disallowed-tools: Write Edit NotebookEdit
user-invocable: true
argument-hint: "<decision to make> [--candidates a,b,c] [--budget-searches N]"
model: opus
effort: high
metadata:
  foundry.vertical: research
  foundry.io: "requirement.v1 -> adr.v1 + fact.v1[constraint]"
license: Apache-2.0
---

# Evaluate a technology

Seven steps, in order. The order matters more than any individual step: weights before
candidates, candidates before scores, scores before opinion. Every reordering is a way of
laundering a preference into an analysis.

**Firewall:** the comparison table, the signal measurements and the full ADR go to
`.foundry/blackboard/<wave>/tech-scout.json` via `mcp__plugin_foundry-core_foundry__blackboard_write`. The reply is
**≤ 300 tokens**: artifact path, recommendation in one sentence, strongest counter-argument in
one sentence, exit cost in days, blockers.

## When not to use this

- The choice is reversible in an afternoon (formatter, logger wrapper, single-file utility).
  Pick one, note it, move on. The evaluation would cost more than the mistake.
- The real question is structural — one deployable or three, strong or eventual consistency,
  who owns which data. That is `foundry-dev:solution-architect`, and it is upstream of this.
- Only one candidate is genuinely available (a mandated vendor, a platform-native service with
  no substitute). Write it up as a constraint via `memory_write`, not as a decision.
- The question is legal ("may we use AGPL code here"). Gather the SPDX facts and hand to the
  legal vertical.

## Step 1 — Fix dimensions and weights, before naming candidates

Derive the dimensions from `requirement.v1`. Assign integer weights summing to **100**.
Dimensions scored 0 stay in the table at 0 so the reader sees they were considered.

| Dimension | Question it settles |
|---|---|
| Fit to requirements | can it do the job without adding a second component |
| Maintenance health | will it still be patched in three years |
| Licence compatibility | may we ship this, in this business model |
| Operational burden | what it costs to run at 03:00 |
| Exit cost | days to remove once it is load-bearing |
| Integration cost | days to first production use in *this* codebase |
| Security posture | vulnerability handling and supply-chain hygiene |
| Team capability | who here can debug it under pressure — by name |

Record the weights with a timestamp in `.foundry/scratch/<session>/weights.md` **before** step 2.
Changing a weight after seeing scores is permitted exactly once, must be stated in the ADR
`context`, and forces a full rescore.

A requirement with no measurable acceptance criterion cannot become a scoring dimension. Send
it back rather than inventing a measure for it.

**Gate 1:** weights sum to 100, timestamped, candidates not yet named.

## Step 2 — Source candidates, including the boring one

Minimum three candidates reaching scoring, of which at least two must be **structurally
different** — different architecture, different operational model, different data ownership.
Two vendors of the same architecture are one option.

Always include, named and scored: **"use what we already have / do nothing"**. It wins more
often than expected, and when it loses you have quantified why.

Sourcing angles: the ecosystem's own awesome-list or registry; what adjacent projects with the
same constraint chose (first-party statements only); the standard's list of conformant
implementations, if a standard exists; and what the incumbent replaced.

**Gate 2:** ≥ 3 candidates, ≥ 2 structurally different, baseline present.

## Step 3 — Measure maintenance signals

Collect every signal in `references/maintenance-signals.md` per candidate, each with the date
measured. Commands for the git-based signals are in that file and are runnable against a local
clone, which is more reliable than any aggregator.

**Forbidden as evidence:** star counts, download counts, "everyone uses it", "it is the
standard", survey rankings, and any sentence containing "popular". Adoption is admissible only
in this exact form:

> Organisation X, operating under constraint C at scale S, runs this in production, per
> <first-party source, published YYYY-MM-DD, retrieved YYYY-MM-DD>.

That is evidence about a constraint like yours. A download chart is evidence that a package
manager was invoked.

**Never state a version number you have not read today from the project's own release feed.**
Write `<version> (checked YYYY-MM-DD)` or "version not verified".

**Gate 3:** every signal measured or explicitly marked unavailable, each dated.

## Step 4 — Resolve licence compatibility

Follow `references/licence-compatibility.md`. In short:

1. Read the **SPDX identifier from the repository's `LICENSE` file**, not from the package
   registry metadata, which is frequently stale or wrong.
2. Check for **licence drift** — projects that relicensed at some release, where old and new
   versions differ. Record which versions carry which licence.
3. Determine the trigger (distribution / network use / never), the reach (whole work / modified
   files only), the patent position, and the attribution requirement.
4. Check whether the licence is **OSI-approved at all**. Source-available licences are not open
   source and carry commercial-use conditions; that belongs in `consequences.negative[]` in
   plain language, not in a footnote.
5. Repeat for transitive dependencies — your obligation is the union of theirs. Generate the
   dependency licence inventory with the ecosystem's own tooling and record the command used.

Emit each obligation as a `fact.v1` of `type: constraint` through `mcp__plugin_foundry-core_foundry__memory_write`,
citing the licence section. Ambiguity goes to the legal vertical marked `[UNVERIFIED]`.

**Gate 4:** every candidate has an SPDX id read from its repository; obligations enumerated;
project's own licence known (if not, this gate blocks the whole evaluation).

## Step 5 — Price operational burden and exit cost

**Operational burden** — answer all seven in writing, per candidate:
failure mode (fails closed / degrades / corrupts); what must be backed up and how long a tested
restore takes; upgrade path and recent breaking-release history; what it emits for
observability without extra work; the smallest non-toy configuration; who gets paged and what
runbook must be written; whether a managed option exists and how it changes licence and exit.

**Exit cost** — engineer-days to remove it after a year in production, covering blast radius
(how many modules import it, whether its types leak across boundaries), data gravity (portable
format? export path? has anyone run it?), behavioural lock-in, and contractual lock-in
(minimum terms, egress fees, deletion timelines).

Then the **isolation test**: can it sit behind an interface the codebase owns? If yes, add the
adapter cost and exit cost drops sharply. If no — because it dictates the programming model,
the data model or the deployment topology — it is a one-way door and needs a human decider.

**Gate 5:** seven questions answered per candidate; exit cost stated in days with assumptions
and isolation-test result.

## Step 6 — Score, then attack the result

Score 0–5 per dimension. Evidence discipline: a **4 or 5 requires a citable pointer** — URL with
retrieval date, benchmark command, file:line, or contract clause. **A 5 with no evidence is
automatically demoted to 3.**

| Score | Meaning |
|---|---|
| 5 | Meets the dimension's measure with headroom, evidenced |
| 3 | Plausibly meets it, no evidence — generates a spike task |
| 1 | Meets it only with components not in this option |
| 0 | Structurally cannot meet it |

Weighted total = Σ (weight × score). Then run all three attacks:

- **Weight flip.** Swap the top two weights. Winner changes → this is a values decision.
  `status: proposed`, escalate to named deciders.
- **Evidence haircut.** Drop every unevidenced 3 by one point. Winner changes → the
  recommendation is unsupported. Emit a time-boxed spike instead of an ADR.
- **Steel-man the runner-up.** Write the best honest case for second place. That paragraph
  becomes the mandatory `Strongest argument against:` line in `decision`. If it comes out weak,
  you sourced weak alternatives — return to step 2.

Ties within **10%** on weighted total are broken on exit cost: recommend the cheaper one to
undo, and say that is the reason.

**Gate 6:** all three attacks run and recorded in `context`.

## Step 7 — Emit the ADR

`mcp__plugin_foundry-core_foundry__blackboard_write` with `schema: adr.v1`, `agent: tech-scout`. Field mapping:

| ADR field | Content |
|---|---|
| `drivers[]` | one per dimension: "<dimension> (weight N): <measure>" |
| `options[]` | **every** candidate that reached scoring, losers included, each with `pros`, `cons`, and `cost` = build days + run cost + cost to reverse |
| `decision` | the recommendation, then a separate paragraph beginning `Strongest argument against:` |
| `consequences.positive[]` | each traceable to a driver and its measure |
| `consequences.negative[]` | what is given up, concretely; licence conditions in plain language |
| `consequences.risks[]` | each with a **detection signal**, so it is observable before fatal |
| `status` | `proposed` unless the caller is the accountable decider |
| `context` | weights and their timestamp, the three attack outcomes, what was not examined |

Validate with `mcp__plugin_foundry-core_foundry__contract_validate` before returning. Then render to
`docs/adr/NNNN-<slug>.md` through the ADR writing skill of the dev vertical if it is available;
if it is not, leave the artifact on the blackboard and say the ADR was not rendered.

**Gate 7:** artifact validates; losing options present; `Strongest argument against:` present.

## Refuse to recommend when

- The only argument for the leader is adoption, familiarity or momentum.
- The project's own licence is unknown, making compatibility undecidable.
- Fewer than two structurally different candidates exist.
- Every score above 3 is unevidenced.
- The requirement has no measurable acceptance criterion.

Report the blocker. A recommendation produced under any of these conditions is a guess wearing
a table.

## Exit criteria

- [ ] Weights sum to 100, timestamped before candidates were named.
- [ ] ≥ 3 candidates, ≥ 2 structurally different, "do nothing" included and scored.
- [ ] Every maintenance signal measured or marked unavailable, each dated.
- [ ] Zero version numbers without a checked date.
- [ ] SPDX id per candidate read from its repository; transitive licence inventory generated
      with a recorded command.
- [ ] Seven operational questions answered per candidate.
- [ ] Exit cost in engineer-days, with isolation-test result.
- [ ] Every 4–5 score carries an evidence pointer with a retrieval date.
- [ ] Weight flip, evidence haircut and steel-man all executed and recorded.
- [ ] `decision` contains `Strongest argument against:`.
- [ ] Losing options present in `options[]`.
- [ ] `adr.v1` validates; reply ≤ 300 tokens.

## Interop and degradation

- The recommendation's load-bearing claims go to `evidence-verifier` before `status` moves to
  `accepted`.
- If `superpowers` is installed, invoke `superpowers:verification-before-completion` before
  reporting done; otherwise say verification was self-administered.
- If the `foundry` MCP server is unavailable: keep the comparison in
  `.foundry/scratch/<session>/`, report the blocker, and do not hand-write memory or blackboard
  files.
- If network access is unavailable: measure git-based signals from local clones, mark every
  unmeasurable signal `unavailable`, set ADR `status: proposed`, and list what a networked run
  must still check.
- If `gh` or an equivalent forge CLI is absent, use the plain `git` commands in
  `references/maintenance-signals.md`; they need only a clone.

## Deliberately not covered

- Running benchmarks. Benchmarks are cited with their methodology and date; unevidenced
  performance claims stay at score 3.
- Architecture. Boundaries, consistency and topology are decided upstream.
- Legal advice. Obligations are identified, never adjudicated.
- Procurement, contract negotiation, vendor security questionnaires, pricing.
- Migration execution. The exit plan is produced; the migration is planned elsewhere.

## References

- `references/maintenance-signals.md` — every signal with the exact command and how to read it.
- `references/licence-compatibility.md` — obligation triggers, reach, the compatibility
  direction, and the traps.
- `references/scoring-sheet.md` — the comparison table format and the three attack procedures.
