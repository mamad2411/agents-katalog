---
name: rfp-response-quality-tone-review
description: >
  Reviews a draft proposal for voice consistency, narrative coherence, the
  firm's configurable tone standards, weak or vague language, and structural
  quality. Runs after compliance review and salesperson corrections. Logs
  findings to the Review Findings SharePoint list and annotates the draft.
---

# Quality & Tone Review Skill

## Firm Profile (REQUIRED — fill in before use)

These values define who your firm is and how it writes. See `SETUP.md`.

- FIRM NAME:          [FIRM NAME]
- WHAT THE FIRM DOES: [one sentence]
- ROLE BOUNDARY:      [what the firm will NOT claim to do — leave blank if none]
- VENDOR STANCE:      [vendor-neutral OR resells/implements specific products]
- SPECIALIZATION:     [domains the firm credibly claims]
- NAMED METHODOLOGY:  [optional — e.g., a named multi-phase method]
- VALUE MODEL:        [optional — the through-line your proposals argue]
- VOICE:              [3–5 adjectives]

> **The voice standards in this skill are an EXAMPLE** (a precise,
> risk-disciplined advisory firm). Replace them with your firm's actual standards
> derived from the `VOICE` values above. Keep the structure; change the content.

---

## Purpose

A proposal that passes compliance may still fail on quality. This skill reviews
how the draft reads — whether it sounds like [FIRM NAME], whether the narrative
holds together, whether each section earns its place, and whether the language is
specific and confident enough to persuade an evaluator. This is not a
spell-checker; it is a structured editorial review calibrated to the firm's
voice, positioning, and the buyer's evaluation audience.

---

## Firm Voice Standards (EXAMPLE — customize for your firm)

Every quality finding is evaluated against these standards. Replace the examples
with your own before use.

### What the Firm's Voice Sounds Like

*Example (precise, risk-disciplined advisory voice):* writes like a trusted
senior advisor to a senior decision-maker — precise, confident, evidence-grounded.
Does not oversell, use promotional language, or claim what it cannot substantiate.
Proposals read as authoritative assessments, not marketing collateral.

| Quality | Description | Example |
|---|---|---|
| **Specific** | Claims anchored to facts, frameworks, or named methodology | "Our delivery framework begins with a structured readiness assessment" — not "We take a comprehensive approach" |
| **Risk-aware** | Acknowledges complexity and risk honestly | "Adoption at this scale presents change-management challenges that require clear decision rights before rollout" |
| **Outcome-oriented** | Explains what the client will do differently | "Following the design phase, the organization will have a defensible, audit-ready governance structure" |
| **Accountable** | Commitments clear and tied to the firm's scope | "We will deliver a framework and a knowledge-transfer plan — not a deployed system" |
| **Consistent with positioning** | Voice reflects the firm's VENDOR STANCE | "We will facilitate an objective evaluation of options against your defined requirements" |

### What the Firm's Voice Does Not Sound Like

| Pattern | Problem | Flag Severity |
|---|---|---|
| Vague superlatives: "comprehensive", "holistic", "robust", "seamless" without substance | Filler signaling lack of specificity | Medium |
| Promotional enthusiasm: "exciting opportunity", "transformative potential", "game-changing" | Inconsistent with a risk-disciplined tone | Medium |
| Language crossing the ROLE BOUNDARY: "we will configure", "we will roll out" (for an advisory firm) | Blurs positioning | High (escalate to Compliance Review if not already flagged) |
| First-person plural without clarity of role: "we will ensure" (ensure what? at what scope?) | Ambiguous accountability | Medium |
| Passive construction obscuring accountability: "the framework will be designed" | Firm must be the named actor in its own commitments | Low |
| Padded sentences: "It is worth noting that…", "It should be mentioned that…" | Weakens authority; delete the preamble | Low |
| Client flattery: "Your organization's forward-thinking approach…" | Unprofessional in formal proposals | Medium |

---

## Step 1 — Load the Draft and Inputs

1. Retrieve the compliance-reviewed and salesperson-corrected draft from the WIP
   Collaboration Folder.
2. Retrieve resolved and open **Review Findings** for this proposal (Compliance) —
   do not re-flag logged compliance issues; reference them only if they have a
   quality dimension not previously captured.
3. Retrieve the approved **Content Strategy Brief** (Phase 2) — assess the draft
   against the approved strategy, not just standalone quality.

---

## Step 2 — Assess Narrative Coherence

Before individual sections, assess the proposal as a whole. Read the executive
summary, then the first paragraph of each body section, then the closing. Ask:

- Does the exec summary make a clear, specific value proposition that the body sections substantiate?
- Is there logical progression across sections — does the argument build, or repeat?
- Does the proposal answer the evaluator's implicit question: *"Why this firm, for this engagement, for this client, at this moment?"*
- If the Firm Profile defines a VALUE MODEL, is it reflected in the overall structure?

Log coherence gaps as findings (Step 5). A coherence gap requires structural
changes, not line edits.

---

## Step 3 — Section-by-Section Quality Review

For each section:

**3a — Opening and Framing**
- Opens with relevance to the client's challenge — not a self-introduction or methodology description?
- First sentence specific enough to orient the reader?
- Flag inside-out framings ("[FIRM NAME] has extensive experience…", "Our approach is…"). Open from the client's perspective, then introduce the firm's response.

**3b — Specificity and Evidence**
- Does each substantive claim have a specific anchor (named methodology phase, referenced past engagement type, cited standard/framework)?
- Flag two or more consecutive sentences with no specific evidence, framework reference, or outcome.
- Flag "extensive" without a quantifier or example.

**3c — Differentiator Reinforcement**
- Cross-reference each section against the differentiators the Content Strategy Brief prioritised. Confirm each prioritised differentiator is present in at least one section with substantive language — not a one-line mention. Flag any that is absent from the full document.

**3d — Transition and Flow**
- Do sections connect logically (last sentence sets up the next, or the next heading signals progression)?
- Flag consecutive sections readable in any order without loss of meaning — suggests a missing narrative arc.

**3e — Length and Proportionality**
- Are sections proportional to the weight of the corresponding evaluation criterion? A 30% criterion should not get one paragraph while a 10% criterion gets a full page.
- Cross-reference section word counts against the evaluation weighting from Phase 2 (and the Page Budget Table, if present). Flag significant disproportionality.
- Flag sections over 600 words (Word) or 2 content slides (PowerPoint) that could be condensed without loss of substance.

---

## Step 4 — Line-Level Language Review

Mechanical checks — flag every instance.

### Weak Language Patterns (Low or Medium)

| Pattern | Action |
|---|---|
| "comprehensive", "holistic", "robust" (unsubstantiated) | Replace with specific descriptor |
| "seamless", "frictionless", "smooth" | Output promises, not advisory commitments |
| "innovative", "cutting-edge", "state-of-the-art" (without specifics) | Replace with what is specifically novel |
| "partner with" (client relationship) | Use "advise", "support", or "work alongside" (adjust to positioning) |
| "It is worth noting that" / "It should be mentioned" | Delete preamble, start with the substance |
| "going forward" | Replace with "from this point" or restructure |
| Sentences beginning "We believe…" | Assert, do not believe — replace with an evidence-backed statement |

### Tone Inconsistencies (Medium)
- Promotional language in body sections (acceptable in exec summary preamble only if balanced)
- Casual register in formal sections (contractions, colloquialisms)
- Inconsistent second-person address: mixing "the organization" and "you" in the same section

### Terminology Consistency (Low)

Check key terms are used consistently throughout — inconsistency suggests the
proposal was assembled from multiple sources without review. Build this table from
your firm's standard terminology; example rows:

| Term | Standard Usage (example) |
|---|---|
| Named methodology phases | Always the same names and casing (from Firm Profile NAMED METHODOLOGY) |
| The client | Client's formal name on first reference per section; "the organization" thereafter |
| "Engagement" vs. "project" | "Engagement" for the firm's work; "project" may refer to the client's initiative |

---

## Step 5 — Log Findings

For each issue, create an item in the **Review Findings** list:

| Field | Value |
|---|---|
| **Proposal** | Proposal name (link to a Proposals tracking item) |
| **Review Type** | `Quality & Tone` |
| **Severity** | `High` (coherence gaps, missing critical differentiators) / `Medium` (tone, structure) / `Low` (line-level) |
| **Location** | Section name and paragraph or slide number |
| **Finding** | Description of the quality issue |
| **Verbatim text** | The exact phrase or sentence flagged |
| **Recommended fix** | Specific rewrite suggestion where possible |
| **Status** | `Open` |

Also add an inline annotation at each finding's location:
```
[QUALITY FLAG — Severity: Medium | Tone: Vague superlative]
"robust governance framework" — replace with specific description of what makes the framework defensible.
Suggested: "a governance framework with defined decision rights, documented escalation paths, and quarterly audit review cycles"
```

---

## Step 6 — Report Back to the User

Provide a summary with:

- Total findings by severity.
- Any High findings (coherence gaps, missing critical differentiators) listed explicitly — require structural changes.
- Count of prioritised differentiators confirmed vs. absent.
- Terminology consistency status (pass/fail per term).
- Proportionality assessment: over-/under-weighted sections relative to evaluation criteria.
- URL of the annotated draft and the Review Findings list.

### Example Summary Output

```
Quality & Tone Review complete.

Findings summary:
  High severity:    2
  Medium severity:  9
  Low severity:    14

HIGH — Structural changes required:
  1. Narrative coherence gap — Executive summary value proposition not substantiated
     in Section 3 (Approach). Section 3 reads as methodology description, not a
     response to the client's stated challenge. Recommend restructuring Section 3
     opening to connect explicitly to the client's priority identified in the RFP.
  2. Differentiator absent — "Structured knowledge transfer model" not reinforced
     anywhere in the document. This is a priority differentiator per the Content
     Strategy Brief. Suggest adding 1 paragraph to Section 6.

MEDIUM — Address before final publication:
  3.  [Exec Summary] "Your organization's progressive approach to AI" — client flattery, remove
  4.  [Section 2]    "Seamless integration of governance controls" — outcome promise, reframe
  5.  [Section 3]    Three consecutive sentences with no evidence anchor — add framework ref
  6.  [Section 4]    "We believe our methodology is well-suited…" — rewrite as assertion
  7.  [Section 5]    "Innovative risk tiering approach" — specify what is novel
  8.  [Section 5]    Mixes "the organization" and "you" — standardize to "the organization"
  9.  [Section 6]    Section is 820 words; evaluation weight is 10% — consider condensing
  10. [Section 7]    "Partner with the organization" — replace with "advise the organization"
  11. [Appendix A]   "Comprehensive case study portfolio" — unsubstantiated; use count

LOW — Recommended improvements: 14 findings (see Review Findings list)

Differentiator coverage:
  Vendor-neutral independence            — present
  Domain specialization                  — present
  Embedded security integration          — present
  Structured knowledge transfer model    — ABSENT  ← High finding #2
  Decision-quality methodology           — present

Terminology consistency:
  Methodology phase names                — consistent
  "Engagement" vs. "project"             — consistent
  Capitalization of key terms            — inconsistent (6 instances — standardize)
  Client name usage                      — consistent

Review Findings logged:
   https://contoso.sharepoint.com/sites/Proposals/Lists/ReviewFindings

Annotated draft:
   https://contoso.sharepoint.com/sites/Proposals/WIP/NorthwindRFP/Northwind_Proposal_DRAFT_QualityAnnotated.docx

Next steps: Salesperson addresses High and Medium findings, then submits for
final formatting before publication.
```

---

## Notes & Edge Cases

- **Highly technical proposals:** Be more tolerant of technical language, but
  still flag jargon a non-technical evaluator on the buyer's panel would struggle
  to assess.
- **PowerPoint proposals:** Focus on slide headline quality (each headline a
  complete, specific statement — not a topic label), bullet specificity, and
  narrative flow across slide order. Flag any bullet longer than 15 words on a
  slide face.
- **Salesperson voice vs. firm voice:** Highly personalized language ("I've worked
  with many organizations like yours…") is acceptable in a cover letter or intro
  email, not in the formal proposal body. Flag these as Medium.
- **Re-running after corrections:** On re-run, carry forward unresolved findings.
  Only re-check sections the salesperson edited — do not re-score the full
  document unless explicitly requested.
