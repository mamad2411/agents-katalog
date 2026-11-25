---
name: to-spec
description: Turn an agreed feature or plan into a proportionate, testable specification at the requested destination.
---

# Write the agreed specification

Synthesize the conversation and relevant code. Reuse the project's existing
specification format and terminology. Resolve implementation details from the
code; ask only about missing behavior or a material tradeoff that changes the
spec. Do not repeat an interview whose decisions are already settled.

Size the document to the change. A small feature may need a few paragraphs and
acceptance criteria; a multi-component change may need contracts and a rollout
plan. User stories are optional and have no target count.

Cover the needed parts:

- Problem and observable result, with concrete examples.
- Scope, exclusions, and constraints.
- Consequential implementation decisions and compatibility requirements.
- Acceptance criteria and how to verify them.
- Remaining material decisions or evidence that could change the plan.

Choose test boundaries from existing interfaces. Explain significant choices in
behavioral terms; do not require a separate approval for routine test placement.
Reference exact files, symbols, or prototype artifacts when they help a reviewer
find the relevant code, without turning the spec into a line-by-line itinerary.

Save at the requested local path or the project's usual location. Publish to an
external tracker only when authorized, following existing tracker instructions.
Use $setup-matt-pocock-skills only when required conventions cannot be discovered.
Triage vocabulary is optional; apply only configured labels. Report the saved
location and any unresolved decision that genuinely blocks implementation.
