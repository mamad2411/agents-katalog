---
name: spinoff-idea
description: Derive a portable product-idea kickoff prompt from the invoking repository for use with $idea-scope-brief in a different repository. Use when a repo suggests an adjacent product, SaaS, devtool, library, workflow, or experiment worth briefing elsewhere, but the user wants an idea prompt rather than code extraction or repo creation.
type: planning
version: v0.0
argument-hint: "[optional spinoff theme, target repo path, or audience]"
---

# Spinoff Idea

Invoke as `$spinoff-idea`.

Use this skill to turn the current repository into a clean, transferable prompt for starting `$idea-scope-brief` in another repo. This is a planning handoff, not a code spin-off: do not create repositories, copy source files, or mutate the destination repo.

## Process

1. **Resolve the handoff scope.**
   - Parse any requested theme, target repo path, audience, or product category from `$ARGUMENTS`.
   - If the user names a target repo path, inspect only lightweight orientation files there when readable: `README.md`, `AGENTS.md`, `CLAUDE.md`, `.agents/project.json`, `research/.progress.yaml`, and relevant existing idea briefs. Do not write there.
   - If the spinoff direction is ambiguous, inspect the source repo first and present 2-4 candidate idea boundaries only when the final prompt would otherwise be unfocused.

2. **Inspect the invoking repo for transferable signals.**
   - Read orientation docs: `README.md`, `AGENTS.md`, `CLAUDE.md`, package manifests, app/package indexes, `docs/`, `specs/`, `research/`, and current task docs when present.
   - Identify the core product model, recurring workflows, internal tooling, user/problem hypotheses, distribution assumptions, constraints, existing proof, and adjacent opportunities.
   - Prefer evidence from docs, research, specs, package metadata, and recent tasks over inferred code shape. Use code only to understand concrete capabilities, not to copy implementation details.
   - Keep source references short and repo-relative, for example `README.md`, `research/foo.md`, or `packages/bar/package.json`.

3. **Choose the spinoff idea boundary.**
   - Prefer the smallest idea that can be briefed independently in another repo.
   - Classify source context as:
     - `core transferable`: should shape the new idea prompt.
     - `proof`: evidence that the idea may matter.
     - `constraint`: source-repo limits the new repo should know.
     - `source-only`: implementation, roadmap, or operational detail that should not travel.
     - `unsafe`: secrets, private URLs, customer data, proprietary implementation detail, local paths, or unrelated strategy to exclude.
   - If multiple viable ideas exist and no user preference is clear, select the one with the strongest combination of user value, repo evidence, and independent briefability. Mention the runners-up only briefly.

4. **Compose the target prompt.**
   - Start with the exact command the user should run in the target repo: `$idea-scope-brief <short-topic>`.
   - Make the prompt self-contained. The future agent in the target repo should not need source-repo access.
   - Include these sections:
     - `Source Inspiration`: source repo name/path, what it does, and why it suggests the spinoff.
     - `Spinoff Concept`: one-paragraph product idea and normalized slug.
     - `Problem Hypothesis`: the pain, workflow, or gap the spinoff might address.
     - `Beneficiary Hypothesis`: likely user, buyer, operator, or developer.
     - `Value Wedge`: why this could be different enough to investigate.
     - `Evidence From Source Repo`: concise bullets with repo-relative references.
     - `Constraints And Non-Goals`: what should stay out of the new idea.
     - `Assumptions And Unknowns`: what `$idea-scope-brief` should interrogate first.
     - `Target Repo Instructions`: how to treat the prompt in the destination repo.
     - `Desired Output`: ask `$idea-scope-brief` to follow its normal interrogation and alignment-page approval flow before writing canonical artifacts.

5. **Apply safety and privacy filters.**
   - Do not include secrets, tokens, local absolute paths, private service URLs, customer or user data, proprietary source snippets, unreleased business strategy unrelated to the idea, or large quoted blocks from source docs.
   - Summarize sensitive internal context at the level needed to brief the idea, or omit it.
   - If the prompt depends on unsafe context, replace it with a sanitized placeholder and state what kind of input the user should provide manually.

6. **Deliver the handoff.**
   - Default to returning the ready-to-paste prompt in the final response.
   - Write a durable prompt file only when the user asks or the source repo already has a clear place for spinoff prompts. Prefer `research/<slug>-spinoff-idea-prompt.md` in the source repo; do not write into the target repo unless explicitly requested.
   - End with the target command and the prompt. Do not recommend `$spin-off`, `$scaffold`, or implementation skills unless the user asks for code extraction after the idea brief exists.

## Output Template

Use this shape for the generated prompt:

```md
$idea-scope-brief <short-topic>

We are exploring a spinoff idea inspired by `<source repo name/path>`. This prompt is intended to start an idea-scope-briefing in this target repo; treat the source repo context as inspiration and evidence, not as implementation instructions.

## Source Inspiration

<What the source repo does and why it suggests this adjacent idea.>

## Spinoff Concept

- Working name: <name>
- Slug: <slug>
- Concept: <one paragraph>

## Problem Hypothesis

<Pain, workflow gap, or unmet need.>

## Beneficiary Hypothesis

<Likely user/customer/operator/developer and why they may care.>

## Value Wedge

<What could make this worth investigating separately.>

## Evidence From Source Repo

- <Evidence point> (`path/to/source.md`)
- <Evidence point> (`path/to/package.json`)

## Constraints And Non-Goals

- <Constraint or non-goal>

## Assumptions And Unknowns

- <Assumption or open question for interrogation>

## Target Repo Instructions

- Use this as input to `$idea-scope-brief`, not as a spec or implementation plan.
- Follow the skill's normal stage-zero interrogation and alignment-page approval flow before writing canonical research artifacts.
- Preserve source context only as evidence; adapt naming, scope, and workflow to this target repo.

## Desired Output From idea-scope-brief

Produce an approved idea brief and interview log for this concept, with customer-discovery readiness and next-step routing.
```

## Constraints

- Keep the prompt concise enough to paste into a fresh session, usually under 2000 words.
- Do not run `$idea-scope-brief` from this skill. The handoff is the output.
- Do not create or extract a code repository; use `$spin-off` only for implementation extraction work.
- Do not treat source-repo evidence as market validation. Mark it as inspiration, proof of internal need, or implementation precedent.
- Do not update source repo task docs when using this skill unless the user asks for durable tracking.
