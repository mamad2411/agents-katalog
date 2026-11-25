---
name: sanderson-full-methodology
description: Use as the orchestration skill for Brandon Sanderson's 2025 writing methodology. Routes a task through process, promise design, structure, character, speculative design, ending, revision, and publishing strategy as needed.
---

# Sanderson Full Methodology

Use this workflow skill when a story problem spans multiple craft layers or when the user explicitly wants the full Brandon Sanderson-style method.

## Component Skills

- `$sanderson-professional-writing`
- `$sanderson-promise-progress-payoff`
- `$sanderson-story-architecture`
- `$sanderson-character-engine`
- `$sanderson-speculative-design`
- `$sanderson-endings-and-revision`
- `$sanderson-publishing-strategy`

## Quick Start

Before substantial work:

- Read `references/craft-map.md`.
- Use `references/output-contracts.md` for the correct response shape.
- Use `references/source-index.md` if the user asks what lecture grounding supports the recommendation.

## Operating Loop

1. Identify the user's actual task and stage.
2. Start with `$sanderson-professional-writing` if process or project posture is unclear.
3. Run `$sanderson-promise-progress-payoff` to clarify the bargain.
4. Run `$sanderson-story-architecture` to give the story shape.
5. Run `$sanderson-character-engine` to tune investment and arc pressure.
6. Run `$sanderson-speculative-design` when the setting or magic materially affects choices and payoff.
7. Run `$sanderson-endings-and-revision` to design the resolution and repair the manuscript.
8. Run `$sanderson-publishing-strategy` only when business path or audience strategy is part of the user's ask.
9. End with the next concrete move, not a lecture.

## Routing Table

| User ask | Start with | Then route to |
|---|---|---|
| "Help me build this novel from scratch" | `$sanderson-professional-writing` | `$sanderson-promise-progress-payoff`, `$sanderson-story-architecture`, `$sanderson-character-engine`, `$sanderson-speculative-design` |
| "My middle drags" | `$sanderson-promise-progress-payoff` | `$sanderson-story-architecture` |
| "My protagonist is boring" | `$sanderson-character-engine` | `$sanderson-promise-progress-payoff` if the bargain is unclear |
| "Design my magic system" | `$sanderson-speculative-design` | `$sanderson-endings-and-revision` if climax fairness matters |
| "Fix this ending" | `$sanderson-endings-and-revision` | `$sanderson-promise-progress-payoff` |
| "How should I publish this?" | `$sanderson-publishing-strategy` | `$sanderson-professional-writing` if manuscript posture is the real issue |
| "Follow the whole Sanderson method" | `$sanderson-full-methodology` | all needed components in order |

## Default Output Rule

Prefer this order:

1. diagnosis
2. design recommendation
3. next workflow step

Do not dump every lecture point when the user only needs one move.
