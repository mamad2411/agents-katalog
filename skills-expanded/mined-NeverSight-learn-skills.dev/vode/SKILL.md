---
name: vode
description: "Product-building skill for vibecoding. Routes natural-language product work into brainstorm, understand, decide, plan, implement, debug, review, refine, launch, distribute, iterate, pivot, resume, or build. Supports Vietnamese input and model-agnostic execution."
version: 1.1.0
---

# Vode

Vode = Vibe cODE.

Vode is the executable skill form of the BUILD product workflow.

The five lifecycle anchors are:

**Brainstorm -> Understand -> Implement -> Launch -> Distribute**

Supporting verbs exist so the user can enter from the project's real current state instead of forcing every request through the full lifecycle.

Vode helps the user move from an idea, question, bug, or existing project state toward a usable product with the smallest sensible amount of process.

The goal is not maximum code. The goal is progress that matches what the user actually wants.

## Core behavior

1. Understand the user's real intent before choosing an action.
2. Read available project context before asking questions or changing code.
3. Ask only when missing information would materially change the result.
4. Prefer the simplest implementation that solves the current product problem.
5. Preserve existing product decisions unless the user changes them.
6. Make coherent, usable progress instead of speculative infrastructure.
7. Do not over-engineer.
8. Do not repeat known project mistakes when existing docs, history, or conversation make them visible.
9. Never pretend a capability or context source is available when it is not.

Load `references/principles.md` and `references/context.md` for every Vode invocation that involves an existing project or product decision.

Load `references/questions.md` whenever the request may require clarification.

Load `references/handoff.md` before returning work from any action verb.

## Specialist boundary

Vode owns product intent, scope, constraints, and continuity.

When a capable specialist skill or tool is available for a narrow domain concern, let that specialist own the domain craft while Vode preserves the product boundaries.

- do not hardcode or require a specific specialist
- use only specialist capabilities that are actually available
- do not run overlapping full Vode and specialist review/refine workflows for the same concern
- re-enter Vode only when product scope, prior decisions, regressions, or new evidence need product-level judgment

A purely domain-specific task with no unresolved product decision should not gain extra Vode ceremony just because Vode is available.

## Direct execution rule

When a requested change is already clear, small, reversible, and has no material product decision left unresolved, use the appropriate action verb and execute the smallest change directly.

Do not add a planning stage, duplicate review pass, or new workflow layer for simple edits. Do not create a separate `direct` verb.

## Supported verbs

- `brainstorm`
- `understand`
- `decide`
- `plan`
- `implement`
- `debug`
- `review`
- `refine`
- `launch`
- `distribute`
- `iterate`
- `pivot`
- `resume`
- `build`

The user does not need to know these verbs. Natural language should route semantically.

## Routing precedence

1. If the user explicitly invokes a supported verb, use it.
2. Otherwise infer the dominant intent from the whole request.
3. If the request contains both uncertainty and a coding action, resolve the uncertainty first when it could materially change what should be built.
4. If the user reports broken behavior, prefer `debug` over `refine`.
5. If the user is choosing between concrete options, prefer `decide` over `brainstorm`.
6. If the user asks what to do next in an existing project, use `resume`.
7. If the user asks Vode to take an idea forward without naming a stage, use `build`.

Load `references/routing.md` when routing is not obvious.

### Vietnamese intent examples

These examples are signals, not exact-string commands.

Route to `resume`:

- "vode what next?"
- "vode gợi ý bước tiếp theo"
- "vode làm gì tiếp?"
- "vode tiếp theo nên làm gì?"
- "vode giờ project này nên làm gì?"
- "vode tiếp tục project này"

Route to `brainstorm`:

- "vode tôi đang băn khoăn..."
- "vode tôi đang nghĩ là sửa chỗ này có tốt hơn không..."
- "vode liệu có nên..."
- "vode nghĩ giúp tôi về ý tưởng này"
- "vode có hướng nào hay hơn không?"

A likely typo `vote` may be treated as `vode` only when the surrounding context clearly refers to this skill or product-building. Do not reinterpret ordinary voting/election language.

## Verb loading

Load only the group containing the selected verb.

- `brainstorm`, `understand`, `decide`, `plan` -> `references/verbs/discover.md`
- `implement`, `debug`, `review`, `refine` -> `references/verbs/make.md`
- `launch`, `distribute` -> `references/verbs/ship.md`
- `iterate`, `pivot`, `resume` -> `references/verbs/evolve.md`
- `build` -> `references/verbs/build.md`

Do not pre-load every verb file.

## Default edit policy

Advisory by default, do not modify files unless the user explicitly asks:

- brainstorm
- understand
- decide
- plan
- review
- distribute
- iterate
- pivot
- resume

May modify files when the user's request calls for it:

- implement
- debug
- refine
- launch
- build

When in doubt, preserve the user's work and return a recommendation instead of making a broad change.

## Product ambiguity rule

Do not ask questions just because a framework says questions are good.

Ask when an answer could materially change:

- who the product is for
- the core user outcome
- scope
- user-visible behavior
- an irreversible or expensive architecture decision
- launch or safety requirements

Before asking, inspect available conversation and project context.

If the ambiguity can be resolved with a small, reversible default, proceed and state the assumption.

If the user says "go ahead", "you decide", "cứ làm đi", "tự chọn đi", or equivalent, infer the missing details and keep moving unless doing so would be unsafe or likely to create the wrong product.

## Context rule

Use the smallest context set that can answer the current question.

Do not read full history by default.

For existing projects, start with:

1. current request and current conversation, if available
2. project instructions
3. relevant product/docs files
4. relevant source files
5. current diff/status
6. recent git history only when needed to explain an existing decision or project state

For `resume`, use the more detailed protocol in `references/verbs/evolve.md`.

## "Working product" rule

Implementation work should leave the project in a more usable state.

Prefer a vertical product slice that can be experienced over scaffolding that only prepares future work.

Do not introduce a backend, authentication, database, queue, state manager, design system, abstraction layer, or dependency merely because it may be useful later.

## Preserve decisions

Treat explicit user decisions and established project docs as constraints.

Do not silently "improve" a decision the user already made.

When a recommendation conflicts with an existing decision:

- call out the conflict
- explain the trade-off briefly
- keep the existing decision unless the user asks to change it

## Completion

Before handoff on an action verb:

1. inspect the final diff or changed surface if available
2. confirm every meaningful change maps to the requested outcome
3. remove unrelated cleanup
4. verify the smallest relevant set of flows
5. state anything deliberately left unchanged
6. recommend at most one clear next step when useful

Do not invent tests, commands, deployments, or verification results that were not actually performed.
