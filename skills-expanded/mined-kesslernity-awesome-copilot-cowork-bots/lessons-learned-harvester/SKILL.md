---
name: lessons-learned-harvester
description: Pulls recurring problems out of close-out reports, retrospectives and project correspondence into a themed register showing which lesson keeps repeating across projects. Use when the user asks for lessons learned, what keeps going wrong, to prepare a close-out, or whether a problem has happened before.
---

# Lessons Learned Harvester

Finds the lesson that has now been learned four times, which is the only kind worth acting on.

## Inputs
- **Enterprise Search** across close-out reports, retrospectives and project folders
- **Email** for the correspondence where problems were actually discussed
- `references/config.md` for the project list, the theme taxonomy and the lookback

## Procedure
1. **Gather** close-out and retrospective material across the configured projects and lookback.
2. **Extract individual lessons**, one per row, each with: the project, the date, what happened,
   what was recommended, and the source link.
3. **Theme them** against the config taxonomy. A lesson that fits no theme goes in `Unthemed`
   rather than being forced into the nearest one. Unthemed items are where new themes come from.
4. **Count recurrence per theme across projects**, which is the whole point: a lesson recorded
   once is an anecdote, the same lesson in four close-outs is a systemic finding.
5. **Rank themes by distinct project count**, not by total mentions. Ten mentions on one project
   is one project's problem.
6. **For recurring themes, state whether the recommendation changed** between occurrences. A
   theme where the same recommendation was made repeatedly means the recommendation did not work,
   and saying so is more useful than repeating it a fifth time.

## Output
| Theme | Distinct projects | Occurrences | Latest | Recommendation stable? | Sources |

Then: themes recurring across three or more projects, unthemed lessons, and themes where the same
recommendation keeps being made.

## Definition of done
Every lesson is sourced to a document, themes are counted by distinct project, and unthemed items
are listed rather than forced.

**One project's lessons are not a register.** If the material covers a single project, say so and
present it as that project's close-out rather than as a pattern.

## When there is no data
- No close-out material found: report the folders searched. Many organizations do not write these,
  and that finding is itself worth reporting.
- Material exists but has no recommendations: report the problems and say recommendations were
  absent.

## Boundaries
- **Never attribute a lesson to a named individual.** Lessons attach to projects and processes.
- Never state a cause the source material does not state.
- Never rewrite a recommendation into something stronger than what was written.
- 🔴 Never characterize a safety event, an incident classification or a regulatory finding.
  Those live in their own systems with their own process, and summarising them here would be
  creating an unofficial record of an official thing.
- **Draft only.**

## Self-check
- Is every lesson linked to its source document?
- Are themes counted by distinct project rather than mentions?
- Did I avoid naming individuals and avoid touching safety classifications?
