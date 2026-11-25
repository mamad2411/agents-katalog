---
name: ticket-to-spec
description: Synthesizes the current discussion into a detailed specification and appends it to an existing lightweight ticket. Use when a clarified ticket needs its authoritative specification without creating another issue.
disable-model-invocation: true
---

# Ticket to Spec

Append a specification to the original ticket. Do not create a separate specification issue.

Read [REFERENCE.md](REFERENCE.md) completely before drafting.

## Gather context

Read `docs/agents/bb-skills.md`. If it is missing or inconsistent, stop and direct the user to `$setup-bb-skills`.

Resolve the source ticket from the user's reference or the current conversation. Ask only when the target is ambiguous; do not run a new requirements interview.

Read:

- the full ticket body and comments;
- the current conversation;
- relevant repository instructions, domain glossary, and ADRs;
- the codebase areas and prior tests relevant to the work.

## Confirm the testing seam

Prefer the highest existing behavioral seam and the fewest seams possible. Describe the proposed seam and check that it matches the user's expectations before publishing.

## Synthesize and append

Write the specification using the source template in the reference. Use project vocabulary and omit file paths and implementation snippets except for a decision-rich prototype excerpt.

Preserve the existing title, TL;DR, comments, release grouping, ticket classification, and unrelated metadata. Append the specification to the body after a thematic break.

If a specification section already exists, stop and ask how the user wants to proceed. Do not replace or duplicate it automatically.

After the append succeeds, remove the configured needs-details state. Do not apply task, executor, or legacy readiness classifications to the parent ticket.

Verify the body and classifications. If appending succeeds but state removal fails, report the partial result without rolling back the specification.
