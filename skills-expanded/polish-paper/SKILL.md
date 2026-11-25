---
name: polish-paper
description: Use this skill when the user wants to polish, review, or prepare an academic paper, workshop paper, rebuttal, abstract, introduction, method section, experiment section, conclusion, or related research writing for clarity, structure, correctness risk, reviewer-facing quality, grammar, concision, tone, and conference-style presentation while preserving the original technical claims.
---

# Polish Paper

## Overview

This skill improves research writing without changing the science. It is for tightening prose, sharpening contributions, reducing ambiguity, improving logical flow, and aligning wording with common ML, NLP, CV, systems, and broader academic-paper conventions.

Use it when the user wants an editing workflow, a rewrite prompt, a section-by-section polish pass, or a lightweight author-side review before polishing. The enhanced `review-and-polish` mode merges an OpenJudge-style review gate with a SciWrite-style clarity audit.

## When To Use

Use this skill when the user asks for any of the following:

- Polish a paper draft
- Rewrite an abstract, introduction, related work, method, experiments, or conclusion
- Improve academic English while keeping the technical meaning
- Make writing more concise, more formal, or more conference-ready
- Reduce repetition, weak claims, vague wording, or awkward transitions
- Turn bullet notes into paper-style prose
- Prepare a rebuttal or response letter in a professional academic tone
- Run an author-side review before polishing a draft
- Check correctness risk, reviewer-facing weaknesses, reference issues, and writing clarity in one pass

Do not use this skill when the main need is:

- Substantive scientific critique of correctness or novelty
- Reference formatting only
- Latex build debugging, figure creation, or citation-tool configuration
- Journal-specific copyediting that depends on a proprietary style guide the user has not provided

## Inputs

Gather as many of these as available:

- Target text to revise
- Paper title or topic
- Venue or target style such as NeurIPS, ICML, ICLR, ACL, EMNLP, CVPR, ICCV, or a journal
- Section type such as abstract, intro, method, experiments, rebuttal, or conclusion
- Constraints on length, tone, or aggressiveness
- Terms, notation, or claims that must remain unchanged
- Whether the user wants light edit, full rewrite, or tracked suggestions
- Whether the user wants `review-and-polish`, `sciwrite-pass`, or plain polishing
- Optional BibTeX file or references if the user wants reference checking

If the draft is incomplete, preserve the known content and improve wording and structure only. Do not invent experiments, results, citations, or claims.

## Owner Defaults

If the user does not specify preferences, assume the user is the paper author or author-side editor, default to CS/AI/ML conference expectations, keep the interaction concise, and answer process notes in the user's language. Keep manuscript rewrites in the manuscript language unless asked otherwise.

## Default Workflow

Follow this sequence unless the user asks for only one part:

1. `Intent Lock`
   Identify the section goal, target audience, and any claims or terminology that must not drift.
2. `Issue Scan`
   Detect verbosity, repetition, weak transitions, ambiguous pronouns, unsupported emphasis, inconsistent terminology, and tone mismatches.
3. `Rewrite`
   Produce a cleaner version that is tighter, more readable, and more conference-appropriate while preserving the technical meaning.
4. `Verification Pass`
   Check that notation, claims, numbers, model names, dataset names, and limitations remain faithful to the source.
5. `Optional Notes`
   If useful, briefly list high-impact edits or unresolved issues that still require author judgment.

## Review-And-Polish Workflow

Use this sequence when the user says `review-and-polish`, asks for OpenJudge-style paper review, asks for sciwrite integration, asks to prepare a draft for submission, or asks for one simple command that reviews and polishes.

1. `Review Gate`
   Check format/input completeness, correctness risk, reviewer-facing quality, criticality, and references when available. Classify issues as blocking, major, minor, or copyedit.
2. `SciWrite Clarity Pass`
   Audit clutter, passive voice and smothered verbs, sentence architecture, keyword consistency, numerical consistency, and citation integrity.
3. `Safe Rewrite`
   Polish only what can be safely improved without changing the science. Weaken unsupported claims instead of making them sound stronger.
4. `Author Decisions`
   List issues that require author judgment, new evidence, missing references, or experiment changes.
5. `Optional External Pipeline`
   If the user explicitly asks to run OpenJudge and `py-openjudge` plus model credentials are available, run the external pipeline and use its report as input to the local rewrite. If it fails, diagnose the root cause rather than replacing it with a pretending-to-be-equivalent manual read.

## Working Rules

- Preserve scientific fidelity. Do not add experiments, numbers, baselines, references, or conclusions not present in the source.
- Keep terminology and notation consistent with the original draft unless the user asks to normalize them.
- Prefer concrete wording over hype.
- Remove redundancy, filler, and throat-clearing.
- Strengthen logical transitions between sentences and paragraphs.
- Keep claims calibrated. Replace overstated language with precise academic phrasing when the evidence is limited.
- If the user asks for a full rewrite, retain the argument structure unless it is clearly harming readability.
- When polishing rebuttals, be firm, specific, and professional rather than defensive or emotional.
- For technical terms, do not vary wording merely to avoid repetition. Consistency is usually clearer than synonym churn.
- Do not mechanically remove every passive construction; preserve accepted field or methods-section conventions when passive voice is clearer.
- Treat mismatched numbers, inconsistent terms, suspicious references, and unsupported claims as review findings, not copyediting opportunities.

## Output Modes

- `light-polish`: minimally invasive wording cleanup
- `full-rewrite`: stronger structural and sentence-level rewrite while preserving meaning
- `with-rationale`: revised text plus a short list of major edit rationales
- `review-notes`: issue list first, then a suggested rewrite
- `rebuttal-mode`: concise, professional author-response style
- `sciwrite-pass`: five-pass scientific writing audit before revision
- `review-and-polish`: review gate plus SciWrite clarity pass plus safe polished text

## Recommended One-Line Prompts

For agents:

```text
Use $polish-paper on <paper-path-or-text> in review-and-polish mode: run the review gate first, then the SciWrite clarity pass, then return safe revised text and remaining author decisions.
```

For humans:

```bash
codex "Use \$polish-paper on <paper-path-or-text> in review-and-polish mode; target venue: <venue>; output language: en or zh."
```

## Reference File

When you need reusable prompt patterns, read:

- [references/prompt-templates.md](./references/prompt-templates.md)
- [references/review-and-sciwrite.md](./references/review-and-sciwrite.md)

Use these files for paste-ready prompts covering abstract polishing, section rewrites, rebuttal editing, issue-first review passes, OpenJudge-style review gates, and SciWrite-style clarity audits.
