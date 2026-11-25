---
name: onboarding-intake
description: Use when onboarding a store whose setup depends on facts the platform cannot observe — what the store is trying to achieve, what discounting it can afford, how much work it can sustain, what its brand does and does not permit, which channels and markets are restricted, and when its real peaks are. Asks only the questions the derived store context could not already answer, and stores the answers back onto the store record so every later skill reads them as constraints instead of asking again.
license: MIT
metadata:
  targetbay.display_name: Onboarding Intake
  targetbay.version: "0.2.0"
  targetbay.category: intake
  targetbay.requires: onboarding.store_context, onboarding.intake
  targetbay.composes: context-audit
  targetbay.risk_level: mutation
  targetbay.execution_mode: execute_with_approval
  targetbay.status: foundation
---

# Onboarding Intake

## Purpose

Collect the small number of facts that no amount of store data will ever reveal, and put them somewhere
every product's skills can read.

Margin posture, capacity, brand policy, restricted markets and real seasonality are not weakly evidenced —
they are unobservable. A store's discount history shows what it ran, not what it could afford. Its send
history shows what it did, not what it is willing to do. Asking is the only valid source, and asking well
means asking once, asking little, and never asking something already on file.

## When to Use

- Onboarding a store, after [context-audit](../context-audit/SKILL.md) has established what is already known
- The derived store context returned `absent` for brand, and brand decisions are imminent
- A blueprint is blocked on a constraint only the store owner can supply
- Revisiting stated constraints after a change of plan, ownership or season

## When Not to Use

- The answer is observable from store data. Read it instead (G8); asking a store what its catalogue
  contains damages the one conversation you will reliably get.
- The question is about what the store *should* do. Intake collects constraints, not decisions; the
  decision belongs to [onboarding-blueprint](../onboarding-blueprint/SKILL.md).
- Nothing is blocked on a missing constraint. An intake run with no gap to close is an interview nobody
  needed.

## Required Context

| Context | Why it is needed | Without it |
|---|---|---|
| Existing intake answers | Prevents asking what has already been answered (G8) | Partial; risk of repeat questions, state the risk |
| The derived store context | Determines which questions are already answered by data | Partial; ask the full set and say why |
| Whether brand is derivable | Brand questions are asked only when the pack could not derive brand | Partial; ask the brand questions |
| A writable store record | Answers must outlive the session | Partial; hold in session, warn that they will not persist |

## Required MCP Capabilities

Defined in [../../capabilities.yaml](../../capabilities.yaml); mappings **TODO**.

| Capability | Used for |
|---|---|
| `onboarding.store_context` | What the platform already answered, and whether brand is derivable |
| `onboarding.intake` | Reading existing answers and writing new ones back to the store record |

## Decision Process

```
1. Read existing answers and the pack  ← what is already known
2. Subtract                            ← every question the data or a prior answer already covers
3. Ask what remains                    ← from the fixed set below, never more
4. Record unanswered as absent         ← an unanswered question is not a defaulted one
5. Preview the answer set              ← show exactly what will be written
6. Write on approval                   ← to the store record, as stated values
```

Step 2 is what makes this bearable for the store owner. A store with history and templates on file may be
asked four questions; a store nine days old may be asked eleven.

## Decision Rules

Binding: [../../rules/global-rules.md](../../rules/global-rules.md),
[../../rules/safety-rules.md](../../rules/safety-rules.md),
[../../knowledge/evidence-and-provenance.md](../../knowledge/evidence-and-provenance.md).

- **Ask only what the platform cannot observe** (G8). Read first, subtract, then ask.
- **Never exceed the fixed question set.** It is twelve questions because an intake that grows gets
  abandoned halfway, and a half-finished intake is worse than a short one.

  | # | Question | Feeds |
  |---|---|---|
  | Q1 | Primary objective for the next ninety days | objectives |
  | Q2 | A target for Q1, if there is one | objectives |
  | Q3 | Maximum discount the store is willing to offer | constraints |
  | Q4 | Can rewards or points be funded from margin? | constraints |
  | Q5 | Who maintains this, and how many hours a week? | constraints |
  | Q6 | Maximum messages per customer per week the store is comfortable with | contact budget (X1) |
  | Q7 | Products or categories that must never be promoted | constraints |
  | Q8 | Tone the brand permits, and forbids | brand |
  | Q9 | Is discounting on-brand? | brand |
  | Q10 | Sender name, reply-to address, logo, primary colour | brand |
  | Q11 | Restricted or prohibited channels and markets | constraints |
  | Q12 | Real peak months and blackout dates | seasonality |

- **Ask Q8 to Q10 only when brand could not be derived.** A store with templates on file has an
  observable voice; asking it to describe itself invites an aspiration rather than a fact.
- **An unanswered question stays absent.** It is never filled with a vertical default, and never inferred
  from behaviour — inferring margin posture from discount history is exactly the error this skill exists
  to prevent (G3).
- **Answers are stored as stated values**, carrying the question they came from, so later skills can
  always distinguish being told from having measured.
- **A stated constraint outranks a derived preference** (G9). Record it as a constraint, not as an input
  to be weighed.
- Q6 feeds the cross-product contact budget and is reconciled there, not applied per product
  ([../../rules/contact-ownership-rules.md](../../rules/contact-ownership-rules.md)).

## Workflow

| Phase | Action | Risk |
|---|---|---|
| DISCOVER | Read existing answers, the pack, and whether brand is derivable | `read_only` |
| ANALYZE | Subtract answered questions; determine the remaining set | `analysis` |
| ASK | Put the remaining questions to the store owner or operator | — |
| PREVIEW | Show the complete answer set that would be written, including what stays absent | `plan` |
| APPROVE | Human confirms the answer set | — |
| EXECUTE | Write answers to the store record as stated values | `mutation` |
| VALIDATE | Re-read what was written and confirm it matches what was approved | `read_only` |

## Expected Output

A [skill result](../../schemas/skill-result.schema.json) containing: the questions asked and why each was
asked rather than read; the answers, each recorded as a stated value carrying its question id; the
questions deliberately skipped because the platform already answered them; the questions left unanswered,
recorded as absent; and confirmation of what was written to the store record.

## Validation

- [ ] No question asked whose answer was already in the pack or on file (G8)
- [ ] No more than the twelve questions in the fixed set
- [ ] Brand questions asked only when brand could not be derived
- [ ] Every answer stored as a stated value carrying its question id
- [ ] Every unanswered question recorded as absent, never defaulted (G3)
- [ ] The full answer set previewed before writing (S4)
- [ ] What was written re-read and confirmed against what was approved (S10)

## Approval Requirements

| Action | Risk | Approval |
|---|---|---|
| Read existing answers and context | `read_only` | None |
| Ask questions | — | None |
| **Write answers to the store record** | `mutation` | **Preview, then confirm** |

Writing is previewed because intake answers become constraints for every later skill. An answer recorded
wrongly does not fail loudly — it quietly bends every subsequent decision.

## Examples

**"We just signed up — what do you need from us?"**
The pack has a catalogue and no templates, so brand is absent. The audit already established the
catalogue shape, so nothing about products is asked. Eleven questions go to the store owner; Q2 is
declined and recorded as absent rather than assumed to be "growth". The answers are previewed, approved
and written, and the blueprint that follows treats the 15% discount ceiling and the three-messages-a-week
limit as constraints rather than preferences.

**"Do we need to interview them again? We onboarded them last quarter."**
Existing answers are read first. Nine of the twelve are on file and unchanged, brand is now derivable
from the templates sent since, so the brand questions are skipped entirely. Two questions are asked:
whether the peak months have changed, and whether capacity has. The run takes a minute and writes two
values.

## Failure Handling

| Situation | Response |
|---|---|
| `onboarding.intake` unreadable | **Partial.** Ask the full set, warn that prior answers could not be checked |
| `onboarding.intake` not writable | **Partial.** Hold answers in the session, state plainly that they will not persist and that later skills and any self-serve run will ask again |
| Store context unavailable | **Partial.** Ask the full set; say why every question is being asked |
| Store gives a vague answer | Ask once for a number or a boundary. If it stays vague, record what was said verbatim as stated, and flag the vagueness as a risk to any decision resting on it |
| Answers contradict the pack | Report both. A stated constraint outranks a derived preference (G9), but a contradiction is a finding worth surfacing, not a conflict to resolve silently |

Degraded outcomes set `status` and populate `unmet_requirements`.
