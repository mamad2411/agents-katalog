---
name: fortax-research-citations
description: Build a fully cited research report on an Indian tax, GST, company-law or business question - cite statute to section, sub-section and clause, notifications and circulars by number and date, rulings by bench, case and order number, with the date each was checked. Runs a lead-plus-subagent pipeline with a citation registry, evidence families, counter-review and a final verification pass. Also covers company due diligence from public records. Typical asks - "fully cited research note chahiye", "partner ke liye opinion with sources", "citations check karo is draft me", "is company ka background nikalo".
license: Apache-2.0
metadata:
  author: Fortax
  version: "1.0.0"
  homepage: https://github.com/amit-voais/fortax-skills
  credits: "Deep-research pipeline, source governance, registry, counter-review and quality gates adapted from daymade/claude-code-skills, https://github.com/daymade/claude-code-skills (MIT)"
---

# Research with citations

Needs Python 3 and internet: runs `scripts/fortax.py` (the Fortax engine on ai.fortax.in; your file is processed and not stored).

High-fidelity research reports with strict format control, evidence mapping, source governance and
multi-pass synthesis. For a single bounded question use `fortax-deep-research` (or
`fortax-knowledge-base` for one fact); come here when the answer needs several sources weighed, a
citation registry, or a document a partner, client or officer will read.

## Citing Indian law

Every citation is checkable by someone with only the citation in hand.

| Authority | Cite as | Also record |
|---|---|---|
| Act | Act name and year, section, sub-section, clause, proviso or Explanation — `section 16(2)(c) of the CGST Act, 2017` | The version in force for the period; later amendment, substitution or omission |
| Rules | Rule, sub-rule, clause and the Rules' name | Same |
| Notification | Issuing body, number, series and date — `Notification No. NN/YYYY-Central Tax (Rate), dated DD-MM-YYYY` | Effective date; whether rescinded or amended |
| Circular / instruction / order | Number, file or F. No. where given, date, subject | Whether withdrawn |
| Ruling | Court or bench, case name, citation or order/appeal number, date | Ratio in your own words; followed, distinguished, reversed, SLP pending |
| Fortax KB fact | `source` URL from the KB reply and `captured` date | `match` must be `strong` |
| Portal page / FAQ / advisory | Page title, URL, date you read it | That it is guidance, not law |

- Quote operative words verbatim; never paraphrase them into a quotation.
- Say which year a rule is for. Rules change every Budget; state whether the Income-tax Act, 1961 or
  the Income-tax Act, 2025 governs the tax year you are applying.
- Commentary sites locate sources; they are never the cited authority.
- Anything you did not open in this session and cannot get from a `strong` KB match is
  `[UNVERIFIED — confirm on portal / notification]`, with the law it would come from.
- Use `python3 scripts/fortax.py kb "..."` for due dates, fees and thresholds before searching the web.

## Architecture: lead agent plus subagents

```
Lead agent (coordinator — minimises raw search context)
  |
  P0: Environment + source policy setup
  |
  P1: Question and claim map (decision questions, evidence routes, stop rules)
  |
  Dispatch --> Subagent A --> writes task-a.md --+
           --> Subagent B --> writes task-b.md --+ (parallel)
           --> Subagent C --> writes task-c.md --+
  |                                              |
  |     research-notes/  <-----------------------+
  |
  P2: Investigate, build evidence packets
  P3: Citation registry + source governance
  P4: Evidence-mapped outline with counter-evidence and unknowns
  P5: Draft from evidence packets; reopen decisive originals
  P6: Counter-review (claims, confidence, alternatives)
  P7: Verify every load-bearing claim and exact fact, then polish
```

**Context discipline.** Keep raw search-result noise in task workspaces. Pass evidence packets to the
lead agent, with locators and short source excerpts. Notes are routing aids, not authorities: the lead
agent opens the original for every load-bearing claim, conflicting claim, and exact figure, date or
quotation used in the report.

If your tool has no subagents, the lead agent runs the tasks one after another, acting as each
specialist (degraded mode). Keep raw search noise out of the evidence packet; keep a query log when
reproducibility matters.

## Mode selection

| Dimension | Options |
|-----------|---------|
| **Topic mode** | Enterprise research (a specific company) or general research (law, industry, policy, technology) |
| **Depth mode** | Standard (several decision questions or contested evidence) or lightweight (one bounded question, small evidence surface) |

Choose depth from the number and consequence of unresolved questions, not prompt length, task count
or a target word count.

## Source governance

### Accessibility

| Accessibility | Definition | Examples | Usage |
|---|---|---|---|
| `public` | Open to any external researcher | Government portals, gazette, court orders, news, papers | Always allowed |
| `semi-public` | Registration or limited access | Registered portals, free-tier databases | Allowed with disclosure |
| `exclusive-user-provided` | The CA's paid subscriptions or private databases | A paid case-law database, a licensed company database | Allowed for third-party research; label the access boundary |
| `authorized-first-party` | The CA's or client's own records | Contracts, invoices, ledgers, notices received, correspondence | May establish internal business facts; label provenance |

**First-party boundary.** A client's own records may establish what the business did, agreed, paid,
delivered or received. They are not independent external validation of market standing, regulatory
compliance or a third party's claims. Never relabel an internal record as an external finding.

**Exclusive sources.** When the CA explicitly provides a paid database or subscription for the
research, use it: accept it as `exclusive-user-provided`, cite it in the registry, and if no
independent equivalent exists keep its valid scope and mark the external claim unknown. Never expose
credentials or confidential material beyond the requested output. Detail:
[references/source_accessibility_policy.md](references/source_accessibility_policy.md).

### Source type labels

Every source is also tagged:

| Label | Definition | Examples |
|-------|------------|----------|
| `official` | Primary source | Act, rules, notification, circular, court order, MCA filing, government report |
| `academic` | Peer-reviewed research | Journal articles, papers |
| `secondary-industry` | Professional analysis | ICAI guidance, industry reports, analyst coverage |
| `journalism` | News reporting | Reputable media |
| `community` | User-generated content | Forums, Q&A sites, social media |
| `other` | Uncategorised or mixed | Aggregators, unverified sources |

**Coverage diagnostics.** Track source counts, domains, type mix and concentration to reveal thin
coverage, but never pass or fail research on these totals. Gate on whether each decision question and
load-bearing claim has fit-for-purpose evidence, whether counter-evidence was sought, and whether the
remaining unknowns are explicit. Rubric: [references/source_quality_rubric.md](references/source_quality_rubric.md).

## AS_OF date policy

Set `AS_OF` explicitly at P0. For every time-sensitive claim:
- Give the source's publication date (or the date you read it) with the citation.
- Downgrade confidence when the source is older than the relevant horizon.
- Define a freshness horizon per claim class (a due date can move by notification within days; a
  section rarely changes mid-year) and flag material outside it. A universal age cutoff is only a
  diagnostic.

## P0: Environment and policy setup

| Check | Requirement | If missing |
|---|---|---|
| Required evidence channel (web search, fetch, browser) | Required | Narrow scope, or stop with the affected questions marked unknown |
| Original-source retrieval | Required for load-bearing claims | Do not promote summaries or snippets to final evidence |
| Subagent dispatch | Preferred | Degrade to sequential |
| Filesystem writable | Required | In-memory notes only |

Set: `AS_OF` (today, YYYY-MM-DD), `MODE` (standard or lightweight, justified by the question map),
`SOURCE_TYPE_POLICY`, `COUNTER_REVIEW_PLAN` (what evidence would overturn each provisional
conclusion), and for Indian law the FY / tax period the law is applied to.

Report: `[P0 complete] Subagent: {yes/no}. Mode: {standard/lightweight}. AS_OF: {YYYY-MM-DD}.`

## P1: Research task board

Decompose the assignment into decision questions. Create tasks only where separate evidence routes
or expertise make the work clearer. Planning checklist:
[references/research_plan_checklist.md](references/research_plan_checklist.md).

Each task carries:
- **Expert role** (for example "GST Notification Tracker", "Case-law Researcher")
- **Objective**, one sentence
- **Queries**, two or three pre-planned searches
- **Depth**: DEEP (open two or three full originals) or SCAN (snippets to map sources only)
- **Output**: path to the task notes file
- **Parallel group**: A (independent) or B (depends on A)
- **Decision question** it helps answer
- **Load-bearing claims** that would change the conclusion
- **Disconfirming evidence** that would weaken each claim
- **Evidence route**: which source owner can actually observe the fact
- **Stop rule**: what counts as answered, contradicted or still unknown

Rules: one coherent sub-topic per task; group A tasks logically independent (independence judged by
underlying evidence, ownership and incentive, not domain count); at most three tasks per parallel
group; every task flags time-sensitive claims, the counter-evidence sought and citation-ageing risk.

Report: `[P1 complete] {N} tasks in {M} groups. Dispatching Group A.`

## P2: Dispatch and investigate

Subagents use [references/subagent_prompt.md](references/subagent_prompt.md) and write evidence
packets in [references/research_notes_format.md](references/research_notes_format.md).

1. Dispatch group A in parallel (max three).
2. Each subagent searches, fetches and tags source type, accessibility and As Of.
3. Wait for group A; then dispatch group B, which may read group A's notes.

Each `task-{id}.md` contains: question status (answered / contradicted / unknown, with the stopping
evidence); sources with stable locators from actual retrievals; a claim-evidence table (claim,
excerpt or locator, scope, confidence, original opened or not); counter-evidence sought and unknowns.

Status: `[P2 task-{id} complete] {N} sources, {M} findings.` then
`[P2 complete] {N} tasks done, {M} total sources. Building registry.`

### Enterprise research (a specific company)

Route each decision question through the relevant dimensions only — a coverage map, not a fixed
outline: D1 fundamentals (legal entity, founding, funding, ownership), D2 business and products,
D3 competitive position, D4 financials and operations, D5 recent developments (six months), D6
authorised first-party records (never counted as external corroboration). At intake confirm the exact
legal entity (parent or subsidiary, CIN), depth, and comparison targets. For Indian entities start
from MCA master data and filed financial statements, GSTIN search, stock-exchange filings and court
or tribunal orders.

Detail: [references/enterprise_research_methodology.md](references/enterprise_research_methodology.md).
Run the L1 check after each dimension and L2 after analysis
([references/enterprise_quality_checklist.md](references/enterprise_quality_checklist.md)). Use SWOT,
a risk matrix or scoring from [references/enterprise_analysis_frameworks.md](references/enterprise_analysis_frameworks.md)
only when it helps the decision and its inputs are defensible; otherwise a claim-evidence table.

## P3: Citation registry

The lead agent reads all task notes and builds one registry.

1. Read every claim-evidence table and source list.
2. Merge sources; deduplicate URLs, and group publications derived from the same notification,
   filing, press release, dataset, interview or sponsor as one **evidence family** (ten news sites
   repeating one CBIC press release are one family).
3. Assign sequential [n] by first appearance.
4. Tag source type, accessibility, As Of, evidence family, authority, independence limits, task id.
5. Build a claim-coverage matrix: supporting evidence, disconfirming evidence, decisive original
   checked, remaining unknown.
6. Record excluded sources with reasons. Do not exclude a source merely for failing an arbitrary
   score; restrict it to the claims it can support.

```
CITATION REGISTRY

Approved:
[1] CBIC — Notification No. NN/YYYY-Central Tax | URL | Source-Type: official | Accessibility: public | Evidence-Family: notif-NN-YYYY | Date: YYYY-MM-DD | task-a
[2] ...

Dropped:
x Source | URL | Source-Type: community | Accessibility: public | Evidence-Family: unknown | Reason: original notification could not be retrieved; a blog summary cannot carry the claim

Diagnostics: {approved}/{total}, {N} domains, {N} independent evidence families, source-type mix
Coverage: {answered}/{total questions}; {N} load-bearing claims unresolved
```

**These [n] are final.** Later phases cite only from Approved. Dropped sources never reappear.

**Authorised first-party handling.** Use the original records for the internal facts they record,
label them `authorized-first-party` with whose record it is, seek an external source only when the
claim needs external corroboration, and state the status: internally established, externally
corroborated, conflicted, or externally unknown.

Report: `[P3 complete] {answered}/{total} questions answered. {N} load-bearing claims supported, {M} unresolved. Source totals are diagnostics.`

### Information black box

When an entity has no public footprint (no MCA record found, no website content, no news):

```
Findings: NO PUBLIC INFORMATION AVAILABLE

Sources checked:
- MCA master data (public): no match for the name given [failed]
- GSTIN search (public): no match [failed]
- News media: no coverage [failed]
- Website: placeholder only [minimal]

Verdict: UNABLE TO VERIFY THE ENTITY from an external perspective
Confidence: N/A - insufficient evidence
```

Do not describe an internal fact as externally corroborated, assume the entity exists from a domain
alone, or fill gaps with speculation — and do not discard a valid first-party record either. Do state
what an external researcher can and cannot verify, document every failed search, mark claims
`[unverified]` or omit them, narrow or stop when evidence cannot answer, and recommend direct
confirmation (for example a CIN or GSTIN from the party) for due diligence.

## P4: Evidence-mapped outline

1. Identify cross-task patterns.
2. Design sections topic-first, not task-order-first.
3. Map each section to findings with source numbers.
4. Flag sections needing counter-review; mark recency-sensitive claims with AS_OF checks.
5. Mark every load-bearing claim supported / contradicted / unknown.

```
## N. {Section title}
Sources: [1][3][7] from tasks a, b
Claims: {claim from task-a finding 3}, {claim from task-b finding 1}
Counter-claim candidates: {alternative readings, conflicting rulings}
Recency checks: {source dates + AS_OF; amendments after the period}
Gaps: {limited official evidence}
```

## P5: Draft

Write section by section with [references/report_template_v6.md](references/report_template_v6.md)
(or [references/research_report_template.md](references/research_report_template.md)), adapted to
the requested format and [references/formatting_rules.md](references/formatting_rules.md).

- Every factual claim carries [n]; every number has a source.
- A confidence marker per section — High (statute clear), Medium (circular-based or interpretation),
  Low (conflicting rulings, no clear text) — with the reason.
- A counter-claim sentence where evidence conflicts.
- New sources enter only through the registry and verification path.
- `[unverified]` for anything unsupported.
- Never invent a URL, section, notification number or citation; every locator comes from a real
  retrieval. Never treat notes as proof. Never fabricate data.

Status: `[P5 in progress] {N}/{M} sections, ~{words} words.`

## P6: Counter-review (mandatory)

For each major conclusion:
1. Could the conclusion be wrong?
2. Which high-impact claims rest on one evidence family, however many sites repeat it?
3. Which claims lack a source that can directly observe the fact?
4. Are stale sources used for time-sensitive claims (a superseded notification, a pre-amendment
   section, an extended due date)?
5. Report only evidence-backed issues; zero findings is a valid outcome. State unresolved uncertainty
   explicitly. Do not invent issues or repeat a finished check to reach a count.

**Manual (default):** verify every load-bearing claim against its decisive original; check that
corroborating sources are independent and able to observe the claim; verify AS_OF on time-sensitive
claims; document opposing interpretations (a contrary High Court, a circular contesting a ruling).

**Team (optional):** only when the user or workspace instructions call for it — see
[references/counter_review_team_guide.md](references/counter_review_team_guide.md).

Output: include only evidenced controversies, numbered only when they exist. If none, say so:

```
## Key Controversies
No evidence-backed controversy was found.
Unresolved uncertainty: none.
```

Use that only when both statements are true after the checks. Report:
`[P6 complete] {N} issues found: {critical} critical, {high} high, {medium} medium.`

## P7: Verify

1. **Registry cross-check** — every [n] in the report against the approved registry.
2. **Load-bearing check** — trace every decisive conclusion, exact figure, date, section number and
   quotation to the original.
3. **Sample low-impact claims** as a diagnostic; when one fails, check the whole class.
4. **No dropped source resurrected.**
5. **Evidence-family concentration** for key claims disclosed.

Gates for every phase: [references/quality_gates.md](references/quality_gates.md).

Report: `[P7 complete] {N} spot-checks, {M} violations fixed.`

## Output requirements

- Match the requested language and tone; keep technical and statutory terms in English (GSTIN,
  Form AOC-4, section 44AD).
- Follow the report spec and formatting rules; include a references section.
- Verdict first, then workings, then the rule and its source. Plain English, no emoji.
- Save the report in the client folder or the firm's research folder as
  `YYYY-MM-DD_<topic>_research.md`, with the task notes and registry beside it.

## Reference files

| File | When to load |
| --- | --- |
| [source_accessibility_policy.md](references/source_accessibility_policy.md) | P0: classify sources first |
| [subagent_prompt.md](references/subagent_prompt.md) | P2: dispatching tasks |
| [research_notes_format.md](references/research_notes_format.md) | P2: task output format and registry |
| [report_template_v6.md](references/report_template_v6.md) | P5: draft with confidence and counter-review |
| [quality_gates.md](references/quality_gates.md) | All phases, including India-specific anti-hallucination patterns |
| [research_report_template.md](references/research_report_template.md) | Plain outline and draft structure |
| [formatting_rules.md](references/formatting_rules.md) | Section formatting and citations |
| [source_quality_rubric.md](references/source_quality_rubric.md) | Claim fitness, evidence families, conflicts |
| [research_plan_checklist.md](references/research_plan_checklist.md) | P1: plan and query set |
| [counter_review_team_guide.md](references/counter_review_team_guide.md) | P6 with a reviewer team |
| [enterprise_research_methodology.md](references/enterprise_research_methodology.md) | Company research: dimensions, source priority, cross-validation |
| [enterprise_analysis_frameworks.md](references/enterprise_analysis_frameworks.md) | SWOT, barrier scoring, risk matrix — only when useful |
| [enterprise_quality_checklist.md](references/enterprise_quality_checklist.md) | L1/L2/L3 checks, optional company report structure |

## Anti-patterns

- Single-pass drafting; splitting passes by section instead of whole drafts.
- Ignoring the format contract or the user's template.
- Claims without citations or evidence mapping; conflicting dates mixed without calling it out.
- Copying another AI's output, a blog or a headnote without opening the original.
- Deleting intermediate drafts or raw research outputs.
- Trusting notes as authority instead of reopening decisive originals.
- Inventing URLs, section numbers, notification numbers or case citations.
- Resurrecting a dropped source.
- Missing AS_OF, or the applicable period, on a time-sensitive claim.
- Skipping P6, or inventing issues to fill it.
- First-party overclaim: a client's own record presented as external validation.
- Ignoring an exclusive source the CA provided for the research.

## Next step

After the report, say `Research report complete: [N] sources cited, [M] claims made.` and offer:
A) a fact-check pass against the originals (recommended); B) turning the findings into a client mail
or notice reply (`fortax-client-comms`, `fortax-notice-reply`); C) PDF or Word export; D) nothing.

## Attribution

The pipeline, source governance, registry, counter-review and quality gates are adapted from the
deep-research skill in [daymade/claude-code-skills](https://github.com/daymade/claude-code-skills)
(MIT; licence in `LICENSE-THIRD-PARTY-daymade.txt`), with Indian citation rules, sources and examples
added and the Chinese-language parts translated.
