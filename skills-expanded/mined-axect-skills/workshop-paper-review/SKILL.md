---
name: workshop-paper-review
description: Produce OpenReview-ready peer reviews for ICML/NeurIPS/ICLR workshop papers (4-8 page submissions). Covers PDF intake, evidence-grounded review drafting, anti-anchoring scoring calibration, parallel fact-check verification against the source PDF, AI-writing-pattern removal, and bilingual (Korean draft → English submission) workflow. Produces a tight ~400-word review with Title, Rating, Confidence, Summary, Strengths, Weaknesses, and Questions for Authors — without an Overall section. Use when the user mentions reviewing a workshop paper, drafting an OpenReview submission, preparing a referee report for ICML/NeurIPS/ICLR workshops, fact-checking a review draft, or translating a Korean review draft into a publication-ready English submission.
---

# Workshop Paper Review

Use this skill to produce a polished OpenReview workshop review (target: ~400 words English, 5 sections, single rating). The skill embeds hard-won conventions from a 4-paper review batch and is opinionated about the anti-patterns that creep into LLM-drafted reviews.

It is **not** a friendly read-through; it is structured for honest scoring, fact-grounded weaknesses, rebuttal-friendly questions, and OpenReview submission style.

## When to use

- Reviewing an ICML / NeurIPS / ICLR workshop paper (4–8 page submissions, scope-clear venues).
- Drafting a Korean working review for personal calibration before producing the English OpenReview submission.
- Fact-checking an existing review draft against the source PDF.
- Polishing a draft to remove AI-writing patterns, severity tags, vague compliments, and reviewer-centric phrasing.

If the user wants an adversarial pre-submission audit on their *own* draft (not someone else's), use `adversarial-review` instead.

## Inputs to confirm

Ask only for what is missing:
- path to the source PDF
- workshop venue (only matters for CFP scope sanity; otherwise generic OpenReview workshop form is assumed)
- output language(s): Korean only, English only, or both (default: both — Korean working draft + English final)
- output directory (default: same directory as the PDF)
- whether a v3-style full internal review is also wanted alongside the short OpenReview submission (default: no — submission only)

## OpenReview workshop form assumption

Default form layout (override only if the user specifies a different form):

| Field | Type | Source |
|-------|------|--------|
| Title | one-line summary of the review (~10–13 words) | the Title block in the output file |
| Review | Markdown with LaTeX, max ~200,000 chars (target ~400 words) | the body below `---` in the output file |
| Rating | 1–10 with OpenReview-rubric labels (see `references/scoring.md`) | `## Rating` line |
| Confidence | 1–5 | `## Confidence` line |

There is no separate "Comments to AC" field by default — the entire review is author-visible. Spotlight recommendations and other AC-only signals are therefore **omitted** from the body.

## Output structure

Every submission file follows exactly this structure. **No Overall section** — Rating + the content sections are self-sufficient.

```markdown
# OpenReview Submission — Paper #<id>

## Title

<one declarative sentence, 10-13 words>

## Rating: **N / 10** (<exact OpenReview rubric label>)
## Confidence: **N / 5**

<Granular confidence statement: most confident on X-type critiques, less
confident on Y-type observations. Tells the AC which parts to weight more.>

---

## Summary

<3-5 sentences. Neutral. No Fig references. State the problem, the method, and
the key result + key limitation as the paper itself reports them.>

## Strengths

1. **<short title>**. <1-2 sentences with specific substance. Where useful, name
the broader-community takeaway (e.g., "serves as a methodological warning about
TTR with learned forward models").>
2. **<short title>**. <1-2 sentences>
3. **<short title>**. <1-2 sentences>
4. (optional fourth)

## Weaknesses

1. **<short title>**. <1-3 sentences. Factual problem statement. One concrete
piece of evidence (number, quote, or specific section). No severity tag —
ordering conveys priority.>
2. **<short title>**. <...>
3. **<short title>**. <...>
4. **<short title>**. <...>

## Questions for Authors

1. <Rebuttal-actionable: "Could the authors report / clarify / compare ..."?>
2. <...>
3. <...>
4. <...>
5. (optional fifth)

## Minor points on figures and tables (optional)

These are bookkeeping observations, not substantive critiques. Include only if
the paper has 2+ such issues; otherwise fold into Weaknesses or omit.

1. <cross-reference inconsistency, caption-ambiguity, unexplained asymmetry,
or insightful observation triggered by careful reading>
2. <...>
```

For borderline ratings (5–6), the final sentence of the **last Weakness** or the **last item of Questions** should declare score mobility explicitly: *"If the authors add [specific item] in revision, I would move my rating to [N+1]."* This makes the rebuttal target concrete for the author.

Read `references/template.md` for ready-to-fill copies of this structure at every rating tier (rejection, marginal, accept, clear accept).

## Core workflow

### Step 1 — PDF intake

- Read the entire PDF up-front. If it is >12 pages or >2 MB, use the `pages` parameter on `Read` (e.g. `pages: "1-10"` then `pages: "11-20"`).
- While reading, capture: the paper's claimed contribution, the empirical setup, the headline numbers, the explicit limitations or self-acknowledgments, and any cited prior work that would be a natural baseline.
- Note quotable phrases verbatim — direct quotes from the paper are the strongest weakness evidence.
- **Cheap-but-clarifying-experiment scan**: while reading, ask "what *analytic / simulation / reference* tools did the authors use to *generate* their training data, baselines, or ablations?" Those tools are typically **available at test time at no cost** and may settle ablation questions the paper itself raised. Examples: a paper using an analytic matching function to *generate* training data can re-use the same function as an *alternative forward model* at test time. Catching these is the highest-leverage type of weakness suggestion.
- **Figure/table cross-reference notebook**: keep a short notebook of (figure caption) vs (body text) groupings, bolded "best" entries, parameter-asymmetries, and "weakest channel" attributions. Carefully-read papers often have minor inconsistencies; these belong in the optional Minor Points section, not in main Weaknesses.

### Step 2 — Korean working draft (if user wants both)

Draft the review in Korean first. Korean drafting is easier for the user to scan and edit. The structure is exactly the same as the English submission (no Overall).

Default depth: ~350–450 Korean words. The draft should already be free of severity tags, anti-anchoring meta-commentary, and reviewer-centric phrasing — see `references/anti_patterns.md` before drafting.

### Step 3 — Score the paper

Use `references/scoring.md` for the exact OpenReview 1–10 rubric. Mandatory steps:

1. Read each rating's actual OpenReview label. The label semantics are **different** from typical ML-conference 1-10 scales (7 = "Good paper, accept", not borderline; 6 = marginal-accept; 5 = marginal-reject; 4 = rejection).
2. Run the **anti-anchoring check**: in a 4-paper batch, more than 2 papers landing on the same rating is suspicious. Re-evaluate via pairwise comparison (the higher-rated paper has *what specifically* that this paper lacks?).
3. Match Confidence honestly to actual domain familiarity. Confidence 3 is the most common honest answer; Confidence 4–5 should be reserved for the reviewer's own subfield with full literature familiarity.
4. **Granular confidence statement**: instead of a generic "some familiarity with X" sentence, articulate (a) which dimensions of the paper the reviewer is most confident about, (b) which dimensions are partial, and (c) which type of critique the AC should weight more. Example: *"Most confident on attribution and baseline-completeness critiques, less confident on the novelty of the physics observations. Please weight my comments accordingly."*
5. **Score-mobility declaration** for borderline ratings (5–6): in the last sentence of the last Weakness or the last Question, declare *"If the authors add [specific item] in a revision, I would move my rating to [N+1]."* This gives the author a concrete rebuttal target and gives the AC a clear sense of the score's elasticity.

### Step 4 — Parallel fact-check (mandatory)

Before declaring the review final, dispatch a fact-check pass. For long PDFs this is best done as a subagent task (see "Fact-check subagent prompt" below). For short PDFs, the reviewer can do it inline.

Every quantitative claim, every direct quote, every section/table/figure reference, and every claim of an internal contradiction in the paper must be verified against the PDF text. Hallucinated contradictions or misattributed quotes are the most credibility-damaging mistakes a reviewer can make.

Read `references/fact_check.md` for the strict check-list and recommended subagent prompt.

### Step 5 — Apply corrections honestly

If fact-check disputes a claim that was load-bearing for the rating:
- Remove the disputed claim from the review **and** re-examine whether the rating still holds.
- Do not "launder" the rating by silently keeping the score after removing one of its justifications. Anti-anchoring discipline applies here too.
- Do **not** mention the reviewer-internal fact-check process in the final review — corrections are internal-only.

### Step 6 — Anti-pattern polish

Run the anti-pattern audit (`references/anti_patterns.md`):

1. **No severity tags**. Remove `(Critical)`, `(Major)`, `(Moderate)`, `(Minor)` and their bilingual variants. Ordering of weaknesses conveys priority.
2. **Reviewer-centric phrasing — nuanced**. *Comparative/rarity* claims like "rarely seen in workshop papers", "흔치 않은", "in my experience" are reviewer-centric and should be removed. *First-person hedges* like "I'd suggest...", "I find this interesting because...", "I'm most confident on..." are **OK when substance follows** — they signal the reviewer's stance honestly. The anti-pattern is *vague* first-person ("I think this is interesting" with no follow-on), not *all* first-person.
3. **No vague compliments**. "Valuable", "interesting", "novel" as standalone descriptors → replace with what specifically the contribution makes possible. (In Titles, brief descriptors like "novel framing" are OK due to space constraints.)
4. **No AI-style transitions**. "Indeed,", "Moreover,", "Furthermore," at sentence start → cut.
5. **No em-dash (—) in body**. Use `:`, `,`, or sentence splits. (En-dash `–` is acceptable for ranges.)
6. **No Unicode math**. Replace `α, σ, ², →, ≈, ±, ×` with `$\alpha$, $\sigma$, $^2$, $\to$, $\approx$, $\pm$, $\times$`. Section sign `§` → `Sec.`.
7. **No Fig references in Summary**. They belong in Strengths/Weaknesses where a specific claim is made.
8. **No batch leak**. Never mention other papers the reviewer is currently reviewing. Confidentiality.
9. **No checklist meta-references**. The author has not read your checklist; "v3 §11", "anti-anchoring", "spotlight criteria 3 of 5" are reviewer-internal.
10. **No Overall section**. Rating + Strengths + Weaknesses + Questions are self-sufficient.
11. **No Spotlight recommendation in body**. Spotlight is an AC decision; a reviewer voting Spotlight in the author-visible review is overreach.
12. **No "Major revision and resubmit" framing**. Workshops are typically accept/reject; revision-cycle language is for journals.
13. **No orphan section references**. `(§4.1)` style cross-references in Questions are only valid if the *paper* has §4.1. If the reference points to a weakness in the *review's own* numbered list, omit it (ordering is enough).
14. **No `Non-negotiable`, `self-undermining`, `fundamentally`, etc.** Strong absolutist verdicts read as dictatorial; weakened phrasing ("limits reproducibility", "leaves the claim unverified", "carries weight in the likelihood") is more accurate and more defensible at Confidence 3.

The full table with bilingual examples lives in `references/anti_patterns.md`.

### Step 7 — Translate to English (if user wants both)

If the user wants both languages, produce the English version by close translation of the polished Korean. Translation principles:

- Preserve all LaTeX math verbatim.
- Preserve all direct paper quotes verbatim (italic form: `*"exact phrase"*`).
- Preserve all proper nouns and technical terms verbatim (RPPO, RAPTOR, MAF, Sinkhorn, ILR, etc.).
- Match OpenReview rubric labels **exactly**, including capitalization ("Ok but not good enough", not "OK"; "Top 50% of accepted papers, clear accept" with "papers").
- Avoid AI-style English: do not let "Indeed,", "Moreover,", "Furthermore,", excessive em-dashes, or "making the paper a strong fit for X" creep back in during translation.
- Citations like `(Schneider 2015; Aricò 2020)` keep their semicolons — these are legitimate.

Per the user's CLAUDE.md, translation tasks are typically delegated to a Sonnet subagent. For these short reviews (~400 words), translation in-line is acceptable if style consistency across the batch is a concern; otherwise dispatch one Sonnet subagent per file with strict style instructions.

### Step 8 — Final verification

Run the verification script (`references/verify.py` if present, otherwise inline checks):

- Unicode math characters in body: **0**
- `§` characters: **0** (use `Sec.`)
- Em-dash in body (excluding header line): **0**
- Severity tags: **0**
- Other-paper number references: **0**
- Rating label: exact OpenReview rubric string
- Title word count: 10–14
- Body word count: 300–500
- Overall section: absent

Read `references/verify.md` for the explicit Python audit script.

## Fact-check subagent prompt

When the PDF is long enough to benefit from a parallel fact-check, dispatch with a prompt like:

```
You are a strict fact-checker for an ICML workshop review.

Verify every factual claim in the OpenReview submission against the actual PDF.
Flag every discrepancy, hallucination, mischaracterization, or unverifiable
claim. False claims in a review undermine the reviewer and unfairly damage
authors.

Submission: <path>
Source PDF: <path>

For each numerical claim, methodology claim, italic quote, section/table/
figure reference, and "internal contradiction" claim, label as
VERIFIED / DISPUTED / UNVERIFIABLE / NEEDS-CONTEXT and provide the actual
PDF content for disputed items.

End with:
- Summary: N verified / M disputed / K unverifiable
- Critical issues affecting verdict
- Recommended corrections
```

For a 4-paper batch, dispatch 4 such subagents in parallel.

## Anti-anchoring scoring discipline

In a multi-paper batch, the single biggest threat to honest reviewing is the gravitational pull of the "comfortable" rating (typically 7). Concrete rules:

- **Pairwise pre-commit**: before fixing a rating, articulate one specific dimension on which the candidate paper is weaker than the next-higher-rated paper in the batch and one on which it is stronger than the next-lower-rated. If you cannot, the rating is anchored.
- **Score-justification audit**: if a Critical-tier weakness in the draft turns out to be wrong on fact-check, do not silently keep the rating. Re-examine.
- **OpenReview rubric is non-uniform**: 7 ≠ borderline-accept (that is 6). 4 ≠ strong reject (that is 2). Use the actual labels.

## Anti-patterns specifically observed in LLM-generated reviews

These creep back in even after one cleanup pass; audit for them after every revision:

- "Indeed,", "Moreover,", "Furthermore,", "Additionally," at sentence start.
- "X is important to the likelihood, but its sensitivity is not demonstrated; Y may therefore depend ..." — the semicolon-plus-`therefore` construction.
- "suggesting X rather than Y" — AI-style epistemic hedging.
- "making it a strong fit for workshop discussion" — formulaic closer.
- "Although the paper ..., therefore ..." — formal concession-conclusion construction.
- "valuable substrate", "valuable strength", "interesting framing" — vague compliments that read as filler.
- Em-dash (`—`) used as sentence connector. Em-dash is fine in the file header `# OpenReview Submission — Paper #N`; the *body* should be em-dash-free.
- Long compound titles (>15 words) that summarize the paper rather than the review.

## Quality bar

A review produced by this skill should:

- Be defensible at Confidence 3 — every quantitative claim has a PDF source.
- Survive the most adversarial author rebuttal — every Weakness names a specific deficit a careful author cannot honestly deny.
- Be at most ~500 words in English (the typical OpenReview workshop review length).
- Read as written by a thoughtful human reviewer, not as written by an LLM that loves em-dashes and section-numbered cross-references.

## What this skill does NOT do

- It does not nominate Spotlight / Oral / Best Paper status — that is an AC decision and including it in the author-visible review is overreach.
- It does not produce a full v3-style internal review with Argument Flow chains and per-section checklists. That format is for reviewer self-calibration; the OpenReview submission is the compressed product. If the user wants both, they can ask for the internal version separately.
- It does not write a recommendation-to-PC paragraph. The Rating field carries the recommendation.
- It does not invent comparisons to other concurrent papers in the same review batch. Confidentiality.

## Reference files

- `references/template.md` — fill-in templates for rejection / marginal / accept / clear-accept reviews.
- `references/scoring.md` — OpenReview 1–10 rubric with exact labels + anti-anchoring protocol.
- `references/anti_patterns.md` — full table of phrases and constructions to avoid, with substitutions.
- `references/fact_check.md` — fact-checking protocol and subagent prompt template.
- `references/verify.md` — final-verification Python audit script.
