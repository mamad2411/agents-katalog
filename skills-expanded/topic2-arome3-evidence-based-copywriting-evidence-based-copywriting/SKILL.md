---
name: evidence-based-copywriting
description: Produces and audits externally published marketing copy where factual claims must survive scrutiny — landing pages, product pages, launch emails, one-pagers, search/social metadata. Every statistic, competitor comparison, capability description, and proof point is traced to a fetched source or the project's own documents, labeled, and adversarially verified before it ships. Use when writing or rewriting high-stakes marketing copy; when copy must pass legal, compliance, brand, or claims review; when the audience is skeptical technical or executive buyers; when the company has little or no customer proof yet (pre-launch, zero customers); or when auditing existing copy for unsupported claims, invented capabilities, unverified statistics, or AI-slop language.
license: MIT. See LICENSE for complete terms.
compatibility: Full source verification requires internet access (web search and URL fetching). A no-network fallback is defined in SKILL.md.
metadata:
  author: Abraham Onoja (Arnen Labs)
  version: "1.1.0"
---

# Evidence-Based Copywriting

## Overview

**A claim that cannot be traced to a source you fetched or to the project's own documents does not ship.** That single rule is also US law for advertisers: the FTC requires a "reasonable basis" for objective claims *before* they are disseminated, not after a challenge (see `references/evidence-standards.md`). This skill turns that standard into a working pipeline: ground → research → write → verify → ship.

The output is not just copy. It is copy plus its audit trail: a fact base, per-section annotations with labeled sources, flagged open decisions, and a checklist a reviewer can falsify.

## The two failures this skill exists to stop

Baseline testing shows capable writers (human and model) rarely invent logos or testimonials anymore. They fail in two subtler ways:

1. **Citation without verification.** Real-sounding statistics with plausible URLs, written from memory, never fetched — sometimes shipped with a "verify before launch" note. Stats go stale, get superseded, or never said that. A TODO is not substantiation.
2. **Capability and terms fabrication.** Invented product mechanisms ("agentless sensor", "read-only connector", "syscall baselining"), commercial terms ("rate locked for life", "source-code escrow"), and architecture details that no document establishes. These *feel* like copywriting latitude. They are unsubstantiated claims — the FTC doctrine covers implied claims, and invented terms become contract disputes.

If you notice yourself doing either, stop and route the item to the fact base as an open question.

## Workflow

Copy this checklist into your working notes and check items off as you complete them:

```
Evidence-Based Copy Pipeline
[ ] 1. GROUND    — fact base built from project documents; open questions listed
[ ] 2. RESEARCH  — external evidence fetched + verified; competitors mapped; buyer language sampled
[ ] 3. WRITE     — deliverable drafted from the template, claims labeled inline
[ ] 4. VERIFY    — adversarial review passed; deterministic checks pass
[ ] 5. SHIP      — checklist marked honestly; open decisions flagged to the owner
```

### 1. Ground

Fill in `templates/fact-base-template.md` from the project's own documents (strategy docs, spec, pricing sheet, founder answers). Read every document the project provides before writing anything.

- Every claim the copy will make about the product must trace to a fact-base row with a source. This includes mechanism, architecture, integrations, performance, team credentials, and commercial terms — not just headline features.
- Anything the copy needs that no document answers goes in **Open questions for the owner**. It blocks that copy, or ships as an explicit `[Open decision for the owner]` flag in the deliverable's annotations. Never resolve an unknown by writing something plausible.
- When the owner's own directives conflict (stated audience vs. requested tone, demanded proof vs. actual stage), write to the documented facts and flag the conflict as an open decision — never silently pick a side, and never let the louder directive override a documented fact.
- Record the **stage honesty** section faithfully: customer count, certifications actually held, claims that are forbidden at this stage. If the company has zero customers, the copy will say so — see the stage-honesty playbook in `references/copy-craft.md`.

### 2. Research

Three parallel tracks (dispatch subagents if available; otherwise run sequentially). Full protocol: `references/evidence-standards.md`.

- **Market evidence.** Find external statistics that support the problem narrative. HARD RULE: a claim may only be used if you fetched its source URL during this engagement and confirmed the claim appears there, as worded. Prefer primary publishers; date-stamp everything; check whether the publisher has superseded the number; record conflicts instead of picking the favorable reading.
- **Competitor mapping.** Fetch the competitor pages the copy must differentiate against. Record their positioning, claims, pricing, CTAs, and recurring phrases *verbatim* — both to position against and so the similarity screen in step 4 can prove your copy doesn't echo them. Comparative claims about competitors carry legal exposure (Lanham Act — see `references/evidence-standards.md`); quote exactly and date-stamp.
- **Buyer language.** Sample the buyer's own vocabulary from public sources (job postings, community podcasts/blogs, public forums). Never fabricate access to private communities; state limitations plainly.

**No-network fallback:** if you cannot fetch, you cannot verify. Mark every external claim `[UNVERIFIED — do not publish until fetched]`, state at the top of the deliverable that source verification has not run, and do not mark the final checklist item for source verification.

### 3. Write

Draft into `templates/deliverable-template.md`. Craft rules — voice, banned lexicon, hero specs, section architecture, proof strategy by company stage, metadata truth — are in `references/copy-craft.md`. The non-negotiables:

- Every factual sentence carries its register: verified fact (with link), internal product claim (with document path), projection/design target (labeled), strategic recommendation, or copywriting judgment. Annotations after each section list them.
- Superlatives only where the cited source itself uses them. Paraphrases preserve the source's unit, population, and date.
- Quotes are verbatim. Attributing an author's summary to survey respondents is quote drift, and quote drift is fabrication.
- Projections, design targets, and roadmap intentions are labeled as such at every occurrence, not just the first.
- What you deliberately *excluded* (stats that failed verification, superseded numbers) goes in the annotations. The exclusion list is part of the standard.

### 4. Verify

Two layers, both required:

- **Deterministic.** Run: `python3 scripts/check_copy.py DELIVERABLE.md` (banned lexicon + embedded word/char limits; exits non-zero on failure). Then run `python3 scripts/check_copy.py DELIVERABLE.md --urls` to produce the citation worksheet for the fact-check pass. Add project-specific banned terms with `--lexicon FILE`. *No-execution fallback:* if you cannot run scripts on this surface, apply the banned lexicon and the template's `check:` budgets manually, and record in the checklist that the deterministic pass was manual, not scripted.
- **Adversarial.** Independent review passes per `references/verification.md`: (a) web fact-check that re-fetches every cited URL and tests the copy's *exact phrasing* against it, (b) internal-fidelity check against the fact base, (c) constraints/compliance check, (d) skeptical-buyer persona read, (e) competitor-similarity screen. Fix all blockers; re-run the deterministic checks after edits.

### 5. Ship

Mark the deliverable's self-review checklist honestly — a checklist item a reviewer can falsify does more damage than the defect it hides. Surface every `[Open decision for the owner]` item in your handoff summary. If the project has a claims registry or formal review gate (legal, brand, MLR-style), attach the annotations and citation worksheet — they are built to be reviewed (see `references/enterprise-integration.md`).

## Iron Laws

Individually citable; quote them by number in reviews.

1. **Trace or cut.** Product claims trace to the fact base; external claims trace to a URL fetched this engagement.
2. **Fetch before you cite.** A URL from memory is an unverified claim wearing a citation.
3. **Mechanism is a claim.** How-it-works copy, architecture, integrations, performance, and commercial terms need sources, exactly like statistics.
4. **Label the register.** Verified fact / internal claim / projection / recommendation / judgment — visible in annotations.
5. **The source sets the ceiling.** No superlative upgrades, no unit shifts, no population swaps, no undated "recent studies."
6. **Invented proof never ships.** Customers, testimonials, logos, case studies, certifications, partnerships, metrics, results. In the US, faked testimonials and reviews are also illegal (16 CFR Parts 255 and 465).
7. **Stage honesty is strategy.** State plainly what proof does not yet exist. Disclosure converts better with skeptical buyers than borrowed credibility — and it is the only posture that survives diligence.
8. **Unknowns are flagged, not filled.** An unestablished fact becomes an open question for the owner, never plausible copy.

## Rationalizations — all of them mean stop

| Excuse | Reality |
|---|---|
| "I'll add a note to verify before launch" | Verification precedes drafting. A TODO is not substantiation. |
| "I remember this stat from a well-known report" | Memory is not a source. Fetch it or cut it. |
| "Describing how the product obviously works isn't a claim" | Mechanism descriptions are capability claims; implied claims count. |
| "Concrete terms make the offer feel real" | Invented terms become contracts. Flag as an open decision. |
| "It's just placeholder copy" | Placeholders ship. Mark them unmistakably or don't write them. |
| "The candor section proves we're honest" | Honesty about customers doesn't license invention elsewhere. |
| "The stat is directionally right" | Direction isn't the claim. Unit, population, and date are the claim. |
| "The source is blocked, but secondary coverage matches" | Stop presenting it as primary. Re-route per the blocked-source protocol in `references/evidence-standards.md` — usable only relabeled `verified-secondary`, with the block noted. |

## Red flags — stop and re-ground

- A statistic in your draft you have not personally fetched this engagement
- A product detail you cannot point to in the fact base
- A superlative ("largest", "first", "only", "#1") not present in the cited source
- A commercial term (lock-in, discount, guarantee, SLA) the owner never stated
- A quote you tightened, merged, or reattributed
- A checklist item you're about to mark that a reviewer could falsify

## Reference routing

| Read | When |
|---|---|
| `references/evidence-standards.md` | Before research; when judging any source; for the legal floor and the evidence-trap catalog |
| `references/copy-craft.md` | Before writing; for voice, banned lexicon, heroes, section architecture, stage-honesty proof, metadata |
| `references/verification.md` | Before the verify stage; defines the adversarial review panel and fix protocol |
| `references/enterprise-integration.md` | When the client has claims review, brand governance, or regulated-industry requirements |

Templates: `templates/fact-base-template.md` (fill first), `templates/deliverable-template.md` (write into). Script: run `scripts/check_copy.py` (do not read it into context; its `--help` and output are self-explanatory).

This skill governs claims and evidence. It deliberately does not replace a company's brand-voice guide — it layers under one (see `references/enterprise-integration.md`). Nothing in it is legal advice; regulated industries route final copy through counsel.
