---
name: research-domain
description: Run a disciplined multi-source sweep of an unfamiliar business domain before design starts. Use when the team cannot name the users, the workflow being replaced, or the domain vocabulary. Fixes the questions first, searches several distinct angles, records every claim with a source tier and two dates, resolves contradictions by rule, and synthesises a domain brief plus fact.v1 entries of type domain and glossary. Not for competitor analysis, pricing, or usability research on an existing product.
disallowed-tools: Write Edit NotebookEdit
user-invocable: true
argument-hint: "<domain or research question> [--jurisdiction XX] [--budget-searches N]"
context: fork
agent: foundry-research:domain-researcher
background: false
model: opus
effort: high
metadata:
  foundry.vertical: research
  foundry.io: "research question -> domain brief + fact.v1[]"
license: Apache-2.0
---

# Research a domain

A domain sweep without a protocol becomes a pile of tabs and a confident summary of the first
three results. This skill is the protocol. Six phases, in order, with a gate at each one.

**Firewall, stated first because it is the constraint everything else respects:** the full
brief and every claim record go to `.foundry/blackboard/<wave>/domain-researcher.json` via
`mcp__plugin_foundry-core_foundry__blackboard_write`. What comes back to the caller is a **≤ 300-token** summary.
This skill declares `context: fork`, so the sweep runs inside the `domain-researcher` subagent:
the fetched pages stay in that subagent's window, and when it stops, Foundry's `SubagentStop`
firewall rejects a reply over 3× the budget, so a pasted brief fails the run rather than merely
wasting context. The firewall fires on *any* subagent stop, so it still holds when the runtime
declines to fork a second time and tells you to run this body where you already are. It does not
hold if this body ever reaches you outside a subagent: keep the budget anyway, and say in the
reply that the firewall was not in force.

## When not to use this

- The domain is already documented in `fact.v1` entries — run `mcp__plugin_foundry-core_foundry__memory_search`
  with `type=domain` first and read what exists.
- The question is "which technology" → `evaluate-technology`.
- The question is "do our users understand this screen" → that is product research on an
  existing product, not domain research.
- The question is about market size, pricing or competitors → different discipline, out of scope.
- A single claim needs checking → hand it to `evidence-verifier`; do not run a whole sweep.

## Phase 0 — Preconditions and budget

Do not search until all four are written down:

1. **The question**, in one sentence, in the caller's words. Copy it verbatim.
2. **The jurisdiction(s)** in scope, as ISO 3166 codes, and the ones explicitly out of scope.
3. **The budget**: maximum number of distinct searches and maximum number of pages fetched.
   Default 25 searches and 40 fetches. Announce it; when it is exhausted, stop and report what
   is unanswered rather than quietly continuing.
4. **Access**: will a real practitioner be available? If not, every workflow claim is capped at
   `confidence: medium` and the brief says so on its first line.

**Gate 0:** all four recorded, or return a blocker.

## Phase 1 — Fix the question set

Write 8–15 questions across the ten classes in `references/question-bank.md` (actor, trigger,
sequence, decision, artifact, constraint, deadline, exception, quality, money). Each question
must be answerable by an obtainable document or an obtainable person.

Rules:
- Questions are written **before** the first search. Questions invented after reading a source
  are that source's agenda, not yours.
- A question you later decide is unanswerable is recorded as dropped, with the reason. It
  becomes an entry in `openQuestions` of the handoff.
- Adding a question mid-sweep is allowed and must be timestamped, so the reader can see which
  findings came from a widened scope.

**Gate 1:** ≥ 8 questions, each mapped to a class, written to the scratch file
`.foundry/scratch/<session>/questions.md`.

## Phase 2 — Sweep from distinct angles

One phrasing returns one worldview. Attempt every angle below; a dry angle is a recorded
result, not a skipped step.

| # | Angle | Query shape | Yields |
|---|---|---|---|
| 1 | Regulator / standards body | `<domain> <jurisdiction> regulation OR directive OR standard` | binding rules and official vocabulary |
| 2 | Professional body / certification | `<role> certification syllabus OR curriculum` | what practitioners are trained and tested on |
| 3 | Incumbent vendor documentation | `<incumbent product> user manual OR administrator guide` | the current de facto process model |
| 4 | Recruitment listings | `"<job title>" responsibilities` | the actual daily duties and tools, stated by employers |
| 5 | Practitioner community | `<role> forum OR "does anyone else" <pain phrase>` | friction, workarounds, the hated parts |
| 6 | Failure record | `<domain> post-incident report OR enforcement notice OR audit findings` | how software in this domain has already failed |
| 7 | Institutional research | `<domain> statistics <national statistics office>` | base rates and volumes you would otherwise invent |

Discipline for each angle:
- Issue the query shapes with `WebSearch` and open the results with `WebFetch`; both count
  against the Phase-0 budget. Batch the independent angle queries into one message — the seven
  angles do not depend on each other, and issuing them one at a time spends the budget on
  round trips instead of coverage.
- Search in the **domain's own vocabulary**, not the team's. If a search returns nothing, the
  first hypothesis is that you used the wrong word — go back to angle 2 for the right one.
- Search the **negation and the failure vocabulary** too: "does not", "cannot", "exception",
  "waiver", "derogation", "known issue".
- Record the query string itself. A sweep nobody can re-run is not evidence.
- Deduplicate by origin, not by URL: three pages quoting one press release are one source.

**Gate 2:** ≥ 5 of 7 angles attempted; every attempted angle has at least one recorded
outcome, including "no relevant results".

## Phase 3 — Collect with citations

Every finding is stored in the claim-record shape defined in `references/source-ladder.md`:
statement, tier (S1–S6), source, `published`, `retrieved`, jurisdiction, confidence, verified,
contradicts.

Non-negotiables:
- **Two dates on every claim**: when the source was published and when you read it. A source
  with no visible publication date is recorded as `published: undated`, which caps its
  confidence at `low`.
- **A tier caps confidence.** No claim may exceed the ceiling its tier allows. No design
  constraint may rest on S5 (practitioner testimony) or S6 (blogs, marketing, model output)
  alone.
- **Regulations are read at S1.** Cite the instrument, the article or section number, and the
  consolidated-text date. A law firm's summary of a regulation is S6.
- **Open every citation** with `WebFetch` (or `Read` for a local document). A reference that does
  not resolve, or resolves to something that does not contain the claim, is recorded as a phantom
  reference and the claim is dropped.
- **No paraphrase of an obligation without its article number.**

Never state a number, a version, a volume or a percentage that you did not read in a source you
opened. If you find yourself about to write a plausible figure, write `[UNVERIFIED]` and the
name of the document that would settle it.

**Gate 3:** every claim record complete; zero claims at `confidence: high` supported only by
tiers below S3.

## Phase 4 — Contradictions before synthesis

Cross-check every claim against every other claim in the same subject area. Any pair that
cannot both be true is a contradiction record: both statements, both tiers, both dates, and a
resolution produced by rule, in this order:

1. Higher tier wins.
2. Equal tier → later `published` date wins.
3. Equal tier and equal date → **both survive**, both marked `[UNVERIFIED]`, both at
   `confidence: low`, with a named person or document that could settle it.

Never resolve a contradiction by preferring the claim that suits the product. Record the rule
that was applied, so the resolution is auditable.

Also run the four decay checks in `references/source-ladder.md` (stale truth, scope creep,
jurisdiction drift, unit switch) across the whole set before moving on.

**Gate 4:** contradiction list complete, each with an applied rule; zero unresolved pairs
without an owner.

## Phase 5 — Synthesise

Fill `references/brief-template.md` in order. Nine sections, no additions, no reordering:
question set, actors, current workflow, glossary, regulatory frame, quality bar, known failure
modes, contradictions and unknowns, source register.

Two constraints on the synthesis:

- **No recommendations.** No architecture, no features, no tooling opinions. The moment the
  brief proposes a solution it stops being an honest input to the design agents.
- **Mark the workflow steps** as rule-driven (exists because a rule requires it) or
  habit-driven (exists because it always has). Habit-driven steps are automation candidates;
  rule-driven steps are constraints. This single distinction is most of the brief's value.

Then emit facts through `mcp__plugin_foundry-core_foundry__memory_write` — never by writing files:

- `type: glossary`, one per term, each with definition, authority, counter-example and a
  collision check run against the repository
  (`grep -riE "\b<term>\b" --include='*.{ts,tsx,java,py,go,rs,sql}' .`).
- `type: domain`, one per durable finding about actors, workflow, constraints or quality bar.
- `type: domain` tagged `failure-mode`, one per known way software in this domain has failed,
  phrased as **"this system will fail if …"**.

Set `expires` on any claim whose source is older than 24 months in a fast-moving or regulated
subject. Set `source` to `external:<url>` for external claims so the register stays traceable.

**Gate 5:** ≥ 10 glossary facts, ≥ 3 failure-mode facts, all validating via
`mcp__plugin_foundry-core_foundry__contract_validate`.

## Phase 6 — Write the artifact, return almost nothing

1. `mcp__plugin_foundry-core_foundry__blackboard_write` with `wave: <wave>`, `agent: domain-researcher`,
   `schema: handoff.v1`, `data` containing the brief path, the emitted fact ids in
   `artifacts[]`, `openQuestions[]` from the dropped questions, and `summary`.
2. `summary` is the **only** narrative that crosses into the parent context. Structure it as:
   artifact path · fact counts by type · the three findings that change the design · open
   questions · what was not examined.
3. Return that summary verbatim. Nothing else. No tables, no source list, no reasoning replay.

**Gate 6:** reply ≤ 300 tokens and contains no content that is not in `summary`.

## Exit criteria

- [ ] Question set written before the first search and preserved in the brief.
- [ ] ≥ 5 of 7 angles attempted; dry angles named.
- [ ] Every claim has a tier, a source, a `published` date and a `retrieved` date.
- [ ] Every citation was opened; phantom references recorded and their claims dropped.
- [ ] Zero `confidence: high` claims below tier S3.
- [ ] Jurisdictions examined **and** not examined both stated.
- [ ] Workflow has ≥ 5 steps, each marked rule-driven or habit-driven.
- [ ] ≥ 10 glossary terms, each with counter-example and repository collision check.
- [ ] ≥ 3 failure modes phrased as "will fail if …".
- [ ] Every contradiction resolved by a recorded rule, or escalated with a named owner.
- [ ] Every `[UNVERIFIED]` claim names who or what document could verify it.
- [ ] Search budget respected, or exhaustion reported rather than exceeded.
- [ ] Reply ≤ 300 tokens.

## Interop and degradation

- If `superpowers` is installed, invoke `superpowers:brainstorming` **after** the brief exists
  to turn findings into candidate requirements. Never before — ideation contaminates observation.
  If it is absent, hand the raw brief to the requirements agents and say ideation was unassisted.
- If the `foundry` MCP server is unavailable: stop before Phase 5. Do not hand-write memory
  files; `memory_write` owns id assignment and `supersedes` chains. Report the blocker, keep
  the brief in `.foundry/scratch/<session>/`, and say the facts are unpersisted.
- If `WebSearch`/`WebFetch` are unavailable: run angles 3 and 4 against local material only
  (vendor PDFs, exported manuals, the repository), mark the sweep `partial` in the handoff
  status, and list the unreachable angles.
- A claim that a design will depend on goes to `evidence-verifier` before it is promoted to
  `confidence: high`.

## Deliberately not covered

- Primary human-subject research: this skill specifies the questions a practitioner should be
  asked; it does not run interviews, surveys or diary studies.
- Legal interpretation: it establishes that an instrument says X, never whether X applies here.
- Quantitative modelling and forecasting: it reports cited base rates and stops.
- Competitive, pricing and market-size analysis.
- Solution design of any kind.

## References

- `references/question-bank.md` — the ten question classes with worked examples and the
  disqualifying patterns for each.
- `references/source-ladder.md` — tiers S1–S6, confidence ceilings, the claim-record format,
  and the decay checks.
- `references/brief-template.md` — the nine-section brief, with the fact-emission mapping.
