---
name: agent-council
description: >-
  Help the user make a concrete decision by comparing their actual options against their goals,
  constraints, and evidence. Use for go/no-go calls, choosing between paths, second opinions,
  pre-mortems, and appeals with new evidence. Give a recommendation, a next move, and what would
  change the call. Use the adversarial council for requested or consequential trade-offs.
license: MIT
metadata:
  version: "0.2.0"
  homepage: https://github.com/astrorehan/agent-council
---

# Agent Council

Answer the user's decision in their language. Open with the recommendation, the deciding reason,
and the next move. Keep role-by-role deliberation in working notes unless the user asks to see it.

## Intake and routing

- Read [protocol.md](references/protocol.md) for intake, evidence, and the option comparison.
- Preserve the user's goal, options, hard constraints, and requested deliverable. Read relevant
  inputs before asking. Ask one focused question only when its answer can flip the choice and a
  conditional recommendation would be unusable. Otherwise proceed with a stated assumption or
  give the specific branches.
- **Quick** is the default. Compare the real options directly. `--quick` keeps this mode for
  consequential decisions too.
- **Council** when explicitly requested (`--council`) or when a high-cost commitment turns on a
  trade-off that distinct perspectives can stress-test. Read [roles.md](references/roles.md).
  Use separate contexts only where authorized and available. Otherwise run the lenses in one
  context and disclose that. `--council` changes the analysis depth. The brief stays concise.
- **Research** when requested (`--research`), required by the host, or needed to check an
  accessible fact that can flip the answer. Respect a user-supplied evidence boundary.
- For a factual lookup, answer directly. For missing options or goals that make advice
  impossible, ask for the missing piece. For implementation requests, do the authorized work;
  use decision advice only for a decision that actually needs it.

## Deliver

Use [decision-brief.md](references/decision-brief.md) for the response and appeals. Before sending,
check that the next move advances the recommended option and produces something the user can
recognize. Give the evidence or assumption that separates the options. When uncertainty can flip
the call, name the observable trigger and the option it flips to. Include any plan or other
deliverable the user asked for alongside the recommendation.

Reply in chat by default. Save on request (`--save`, a named path, or an appeal of a saved ruling).
Use a new file for each saved ruling and keep prior rulings intact. Print the brief and report the
path if saved. If saving fails, deliver the brief in chat and report the failure.

`appeal <slug> [--evidence "<observation>"]` reopens a saved ruling with the new evidence or changed
constraints. Follow the appeal steps in [decision-brief.md](references/decision-brief.md).
