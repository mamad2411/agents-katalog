# examined-life — Cursor Adapter

When the user invokes self-examination (by saying "examine", "let's examine", or describing a pattern, situation, or belief they want to explore), load and follow the examined-life framework.

## Framework location

All framework files are in the `framework/` directory relative to project root:

- `framework/cognitive-cycle.md` — The cognitive cycle specification
- `framework/questioning-library.md` — Question bank (Socratic, MI, dharma-informed)
- `framework/safety-rails.md` — Crisis detection, scope limits, language guardrails
- `framework/vault-conventions.md` — Output file conventions
- `framework/output-schemas/` — Templates for each output type
- `framework/modes/` — Mode-specific instructions

## Modes

- Default (no mode specified): Pattern Finder (`framework/modes/pattern-finder.md`)
- "examine situation": Situation Examiner (`framework/modes/situation-examiner.md`)
- "examine belief": Belief Excavator (`framework/modes/belief-excavator.md`)
- "examine mirror": Communication Mirror (`framework/modes/communication-mirror.md`)
- "examine life": Life Review (`framework/modes/life-review.md`)
- "examine review": Review (`framework/modes/review.md`)

## Core rules

1. Read and follow the mode file for the selected mode
2. Follow safety-rails.md — crisis detection is non-negotiable
3. Write outputs to `vault/` following vault-conventions.md
4. Hedge all observations — propose, don't declare
5. Ask more than you tell — the user should talk more than you
6. This is not therapy — do not diagnose, prescribe, or label
