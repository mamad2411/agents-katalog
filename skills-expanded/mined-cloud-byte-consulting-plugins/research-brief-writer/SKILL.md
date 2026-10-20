---
name: research-brief-writer
description: Use this skill whenever the user asks to write a research brief, summarize a report, turn findings into a brief, produce an executive summary of research, digest a whitepaper, or do a research writeup. Also triggers on "brief this report", "condense these findings", "what does this study actually say", "synthesize these sources", "summarize this survey", "make this digestible for leadership", or any request to convert source material — reports, papers, surveys, vendor studies, talk transcripts, multiple mixed sources — into a dense, evidence-first written brief. If source material exists and the deliverable is prose that must carry its findings faithfully, use this skill. Do not use it for interview-based case studies (use interview-case-study-writer) or for original research with no sources to digest.
---

# Research Brief Writer

## Purpose

Produce research briefs that are extraction-grade, not summary-grade. A summary tells the reader a source exists and is roughly about X. A brief replaces the source for decision-making: every number, framework, formula, and threshold the reader would act on is reproduced in full, with provenance. The test of a finished brief: **the reader should never need the source.**

This is a writing method, not a topic skill. It applies to any domain — market research, engineering surveys, academic papers, policy reports, vendor whitepapers.

## Core model

### Brief anatomy

Every brief follows this spine, compressed or expanded by deliverable type:

1. **Hook** — one or two sentences stating a quantified tension or paradox from the material, not a topic announcement. Weak: "This report covers measurement practices." Strong: "Nearly 30% of teams say they don't measure success, yet only 24% admit they don't know whether their metrics improved — a gap that means some teams are reporting improvements they never measured." If the sources contain no tension, the hook is the single most decision-relevant number.
2. **TL;DR findings** — 3–6 bullets, ranked by decision impact (not source order). Each bullet is a complete claim with its key number, readable standalone.
3. **Evidence sections** — one section per finding or theme. Exact numbers, methodology notes, and source attribution inline. This is the body.
4. **Framework extraction** — any model, taxonomy, formula, or maturity ladder the sources define (or that emerges across them), reproduced completely: all levels, all components, all formula terms.
5. **Implications by audience** — what each named audience should do differently, in their own currency (see calibration below).
6. **Caveats and limitations** — methodology weaknesses, sponsorship, sample issues, unresolved conflicts. Always present, never buried.
7. **Next questions** — 2–4 things the sources cannot answer that a decision-maker would ask next.

### Evidence discipline

- **Exact numbers over adjectives.** Never "significant improvement" when the source says "lead time fell from 20 minutes to 8 minutes (60%)". Never "most teams" when the source says "40.8%".
- **Every statistic carries its source and year** on first use: "(Vendor X survey, 2025, n=847)". Subsequent uses of the same source can abbreviate.
- **Classify every claim as measured, claimed, or projected** — and say which. Measured: instrumented before/after data. Claimed: self-reported or asserted without shown data. Projected: extrapolation or vendor forecast. A brief that presents all three in the same register is misleading regardless of accuracy.
- **Flag survey data vs. system data.** Self-reported survey answers and telemetry from real systems are different evidence classes; name the class.
- **Mark vendor-sponsored or commissioned material** explicitly ("commissioned by [vendor]") wherever its findings appear, not just in a footnote.
- **State sample sizes** whenever the source discloses them; write "sample size not disclosed" when it doesn't — the absence is itself a finding.
- **Surface inconsistencies, never smooth them.** If a source contradicts itself or another source, the contradiction is content: state both figures and the delta. Internal inconsistencies are often the most decision-relevant finding in the material.

### Density rules

- Reproduce frameworks, formulas, and thresholds **fully**, not by reference. "The report defines a 4-level maturity model" is a pointer; the brief must list all four levels with their defining criteria.
- Reproduce the arithmetic of any worked example: inputs, formula, result ("50 developers × 2 hours/week saved × $75/hour × 52 weeks = $390,000/year"). Readers trust numbers they can recompute.
- Cut connective filler, background the audience already has, and restatements. Density comes from removing padding, not from compressing evidence.
- Every paragraph must contain at least one thing the reader can quote, act on, or verify. Paragraphs that only orient get merged or cut.

### Structure devices

Use these deliberately; they carry argument better than prose:

- **Named enumerations.** Give recurring structures a countable name — "the five cost categories", "the three path types" — then enumerate all of them. Named things get remembered and reused in meetings; unnamed lists don't.
- **Level ladders.** When sources describe maturity or progression, render it as an explicit ladder (Level 1 → N) with a one-line definition and a "what changes at this level" note per rung.
- **Two-column trade-off tables** for any either/or the sources weigh (build vs. buy, framework A vs. B): one row per decision criterion.
- **Worked examples with real arithmetic** wherever the sources provide inputs, even if the source itself never multiplied them out.
- **Per-audience blocks** in the implications section, one heading per audience.

### Voice

- Declarative sentences. State findings; don't narrate your reading process ("the report goes on to discuss…" is banned).
- No hedging filler ("it could be argued", "somewhat", "fairly"). Uncertainty is expressed precisely — via the measured/claimed/projected labels and the caveats section — not via vague qualifiers.
- Every claim falsifiable. If a sentence cannot be wrong, it carries no information; delete it.
- Hooks and section openers quantified wherever the material allows.

### Length and format calibration

| Deliverable | Length | Contains | Cuts |
|---|---|---|---|
| Exec brief | 1 page | Hook, TL;DR, one table or chart-ready dataset, dollar/risk implications, top 3 caveats | Methodology detail, full framework reproduction, per-source narration |
| Working brief | 3–5 pages | Full anatomy; frameworks reproduced; worked arithmetic; per-audience implications | Source-by-source walkthrough, raw quotes beyond the load-bearing ones |
| Full digest | As needed | Everything decision-relevant in the sources, organized by theme, not by source | Only true padding |

Audience calibration inside any format: **executives** get dollars, risk, and visual/tabular structure — convert technical wins to money whenever inputs allow. **Practitioners** get workflow specifics and before/after states ("deployment took 4 hours, now 10 minutes") — what they would do differently Monday morning.

### Multi-source synthesis

When briefing more than one source:

- **Triangulate:** organize by claim, not by source. For each key claim, list what each source says about it.
- **Mark agreement and conflict explicitly:** "Sources A and B independently report ~40%; source C reports 62% using a broader definition."
- **Never average conflicting numbers.** A fabricated midpoint is worse than an honest range. Report the range and the reason for the spread if determinable.
- **Weight by methodology, and say so:** a measured n=2,000 system-data study outranks a claimed n=90 opt-in survey. State the weighting rationale in one line rather than silently preferring one source.
- Where sources use different definitions for the same term, define both and keep them separate throughout.

## Workflow

1. **Intake.** Establish three things before reading deeply: (a) the source list — enumerate every source with type, year, publisher, and any sponsorship; (b) the audience(s); (c) the deliverable type (exec brief / working brief / full digest). If the user hasn't specified (b) or (c), ask — the same material produces different briefs.
2. **Extraction pass, per source.** Pull into working notes: every statistic (with location), every named framework/formula/threshold, methodology and sample size, sponsorship, internal inconsistencies, and load-bearing quotes. Label each item measured/claimed/projected as you go — it is much harder to retrofit.
3. **Synthesis matrix** (multi-source only). Rows = claims/themes, columns = sources. Fill cells with each source's figure or position. Mark agreements, conflicts, and gaps. This matrix decides section structure.
4. **Draft per the anatomy.** Write the TL;DR last, from the finished evidence sections — writing it first biases the extraction.
5. **Density and evidence audit.** Check the draft against this list; fix every failure:
   - [ ] Every statistic has source + year attached
   - [ ] Every claim labeled or contextually clear as measured/claimed/projected
   - [ ] No adjectives standing in for available numbers
   - [ ] All frameworks/formulas reproduced fully, not referenced
   - [ ] Conflicts between sources stated, none averaged or smoothed
   - [ ] Vendor sponsorship marked at point of use
   - [ ] Sample sizes stated or "not disclosed" noted
   - [ ] Caveats section present and specific
   - [ ] Hook is quantified, not topical
   - [ ] Each paragraph passes the quote/act/verify test
6. **Deliver** in the agreed format. Offer the other calibrations ("a 1-page exec version of this working brief is quick to derive") when the audience is mixed.

## Guardrails

- **No unattributed statistics.** A number without a source is a rumor; either attribute it or cut it.
- **No smoothing of source conflicts.** Disagreement between sources is reported as disagreement, with both figures.
- **No absorption of marketing language.** Strip superlatives, category slogans, and vendor framing ("industry-leading", "seamless", "the only platform that…") from everything you carry over; keep the underlying claim only if it survives as a falsifiable statement.
- **Flag access gaps honestly.** If a cited source is paywalled, gated, or truncated, say so and mark dependent claims as unverified — never reconstruct the missing content from the abstract or from memory.
- **Shorter but lossless.** The brief must be substantially shorter than its sources, but lossless on decision-relevant content. When forced to choose, cut narrative before evidence.
- **The brief is not an opinion piece.** Recommendations live in the implications section and must trace to stated evidence; everything else reports what the sources support.

## Suggested effort

- Single short source (blog post, 5–10 page report) → exec or working brief: light effort; extraction pass plus draft in one sitting.
- Single long source (30+ page whitepaper) → working brief: moderate; budget a full extraction pass before drafting, and expect the framework-reproduction step to dominate.
- Multi-source synthesis (3+ sources, mixed methodologies) → working brief or digest: high; the synthesis matrix is mandatory, and the conflict-handling rules will be exercised. Do not skip step 3 to save time — it is where the value is.
- If the material is primarily interviews or first-person practitioner accounts rather than reports and data, hand off to the sibling skill **interview-case-study-writer**, which handles narrative evidence; this skill's evidence rules assume documentary sources.
