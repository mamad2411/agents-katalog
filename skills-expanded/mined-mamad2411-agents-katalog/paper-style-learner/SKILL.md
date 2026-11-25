---
name: paper-style-learner
description: Use when learning transferable writing style from one or more reference economics papers before drafting, rewriting, translating, or polishing the user's paper. Trigger when the user asks to feed reference papers, imitate or learn writing style, extract a style profile, model introductions/results/literature/table-note style on nearby papers, or prioritize a learned paper style before applying other economics writing skills.
---

# Paper Style Learner

## Overview

Use this skill as the upstream style-learning layer. It studies closely related papers to create a reusable `style_profile`, then applies that profile before routing to `economics-writing-style`, `economics-paper-type`, `reduced-form-economics-writing`, `structural-economics-writing`, `literature-positioning`, `table-figure-design-writer`, `cn-top-econ-writing`, or `econ-paper-humanizer`.

The goal is to transfer writing strategy, not to copy sentences. Learn how the reference papers think, stage the question, move through evidence, choose verbs, hedge claims, position literature, explain results, and name tables or figures.

## Workflow

1. Confirm the task mode:
   - `learn-profile`: extract a style profile from reference papers.
   - `apply-profile`: use an existing or newly extracted profile to revise or draft text.
   - `diagnose-fit`: compare a draft against the learned profile and name the biggest mismatches.
2. Gather inputs:
   - reference papers or excerpts;
   - the user's paper topic, section, draft, and target audience when available;
   - whether the target section is introduction, abstract, literature, data, design/model, results, mechanisms, conclusion, or tables/figures.
3. Read the reference papers for transferable writing moves:
   - argument architecture;
   - introduction progression;
   - paragraph roles and transitions;
   - word choice, verbs, hedging, sentence rhythm, and authorial stance;
   - literature positioning and contribution framing;
   - results interpretation and evidence discipline;
   - table and figure title, caption, and note conventions.
4. Produce or update a `style_profile` using `references/style_profile_schema.md`.
5. Apply the profile using `references/application_workflow.md` when rewriting or drafting.
6. Audit the output against both the learned profile and the economics evidence constraints.

## Style Extraction Priorities

When analyzing reference papers, go beyond surface features. Identify the writing logic that could guide a new draft:

- What kind of economic object opens the paper: puzzle, fact, policy change, theoretical tension, institutional setting, or measurement problem.
- How the paper narrows from broad importance to a concrete research question.
- How quickly it reveals setting, data, design, model, main result, and contribution.
- How it makes the reader care without overclaiming.
- How it sequences literature: closest-paper contrast, strands, mechanism, method, setting, or empirical object.
- How paragraphs begin and end: claim-first, fact-first, contrast-first, question-first, or evidence-first.
- How it handles rival explanations, limitations, identification threats, model assumptions, or external validity.
- Which verbs and hedges dominate: `show`, `document`, `estimate`, `exploit`, `leverage`, `suggest`, `point to`, `is consistent with`, `imply`, `rationalize`, `discipline`.
- Whether results prose emphasizes coefficients, economic magnitudes, visual patterns, mechanisms, null results, heterogeneity, robustness, or caveats.
- Whether table and figure titles are descriptive, object-based, or result-forward; what notes include and omit.

## Non-Negotiables

- Do not copy distinctive sentences, paragraphs, title phrasing, or verbal signatures from reference papers.
- Do not import facts, claims, citations, institutional details, coefficients, mechanisms, or contribution claims that do not belong to the user's paper.
- Do not imitate a style move that conflicts with the user's evidence, target genre, language, or identification strength.
- Do not strengthen causal language to match a reference paper unless the user's design supports it.
- If reference papers conflict in style, name the conflict and build a hybrid profile rather than averaging vaguely.
- If the provided reference excerpts are too thin to support a style claim, mark the claim as tentative.

## Output Modes

For style learning:

1. `Part 1 [Reference Corpus]`
2. `Part 2 [Style Profile]`
3. `Part 3 [Transferable Rules]`
4. `Part 4 [Do Not Imitate]`
5. `Part 5 [How To Use This Profile]`

For applying a profile:

1. `Part 1 [Style Fit Diagnosis]`
2. `Part 2 [Revised Draft]`
3. `Part 3 [Style Moves Applied]`
4. `Part 4 [Evidence Gaps Or Risks]`

For introduction work, include a paragraph-by-paragraph map unless the user asks for only prose.

## Skill Routing

- Use `economics-paper-type` before applying the profile when the target output type matters.
- Use `reduced-form-economics-writing` for empirical sections after the style profile has set the writing strategy.
- Use `structural-economics-writing` for model, estimation, counterfactual, and welfare sections.
- Use `literature-positioning` when the learned style mainly affects literature and contribution framing.
- Use `table-figure-design-writer` for titles, captions, notes, and results prose around tables or figures.
- Use `econ-paper-humanizer` after profile-based rewriting if the resulting text sounds generic or AI-polished.
- Use `cn-top-econ-writing` when applying the profile to Chinese economics journal prose.

## References

Read `references/style_profile_schema.md` when creating or updating a profile.
Read `references/application_workflow.md` when using a profile to revise or draft a user's section.
