---
name: change-advisory-prep
description: Assembles the pack for the next change advisory board from the change requests, threads and documents already circulating, with the risk and rollback position for each change stated or marked missing. Use when the user asks to prepare for CAB, build the change board pack, review upcoming changes, or says a change board is coming up.
---

# Change Advisory Board Prep

Builds the pack from what people actually wrote, and names every change that arrived without a
rollback plan.

## Inputs
- **Email** and Teams traffic about upcoming changes
- **Enterprise Search** for change records, runbooks and prior post-incident notes
- `references/config.md` for the board date, the required fields and the risk vocabulary

## Procedure
1. **Find the changes** proposed for the board window.
2. **For each change, extract the required fields** from config. The usual set: what changes, who
   owns it, the window, affected systems, risk rating as stated by the proposer, rollback plan,
   and who has already approved.
3. **Mark every missing field MISSING.** Do not infer a rollback plan, ever. An inferred rollback
   plan is the single most dangerous thing this skill could produce.
4. **Cross-reference** each change against prior incidents touching the same system, through
   Enterprise Search, and note them as context rather than as objections.
5. **Order** by stated risk, then by blast radius implied by the affected systems.
6. **Write** the pack, and list separately every change arriving with a missing required field.

## Output
| Change | Owner | Window | Systems | Stated risk | Rollback | Prior incidents | Missing |

Then: changes ready for the board, changes with missing fields, and prior-incident context.

## Definition of done
Every change has every required field either filled from evidence or marked MISSING, and the
missing list is surfaced first because it is the board's real agenda.

**A board with nothing to review is fine.** Say so.

## When there is no data
- No changes found: state the window searched.
- A change with only a title: list it with everything MISSING. Do not quietly drop it.
- No prior incidents found for a system: say "none found", which is different from "none exist".

## Boundaries
- **Never approve, reject or schedule a change.** The board decides.
- **Never write a rollback plan.** Report its absence.
- Never state a risk rating of your own. Report the proposer's and say it is theirs.
- **Draft only.** The pack goes to the user for circulation behind approval.

## Self-check
- Did I infer any rollback plan or risk rating? If so, remove it.
- Is the missing-fields list first?
- Is prior-incident context labelled as context, not objection?
