---
name: team-lead-mode
description: The orchestrator for a team lead's week. Runs the other team-lead skills in a stated order inside one task and assembles their outputs into a single review, degrading gracefully when a skill is not installed. Use when the user asks for their weekly team review, to run the team lead routine, says it is Monday planning, or wants everything in one place.
---

# Team Lead Mode

Runs the pack in order and assembles one review, rather than making you run four things.

🔴 **This is not multi-agent, and the distinction matters.** Grok Bot has a roster of Bots that
message each other and pass ownership. Cowork runs **one task that loads several skills**. This
skill calls others in sequence inside that single task. If you came here expecting agents
negotiating, that is the capability Cowork does not have, and pretending otherwise would waste
your afternoon.

## The skills it invokes, in order

1. `workstream-health` if installed, else read `project.md` files directly and say you did
2. `one-to-one-prep` for each direct report named in config
3. `project-decomposer` **only** for a project config marks as needing decomposition
4. `calendar-defender` if installed, for the week ahead

## Procedure

1. **Check which of the four are available.** State the list up front: "running with three of
   four, `calendar-defender` not installed". The reader must know what is missing before they
   read conclusions drawn without it.
2. **Run each in the order above.** Do not parallelise: later steps read earlier output, and the
   1:1 briefs are better when the workstream picture already exists.
3. **If a skill is missing**, degrade in the way named above rather than failing the whole run,
   and mark its section DEGRADED with one line on what is weaker as a result.
4. **If a skill errors**, keep its section, say it failed, and continue. A partial review
   delivered Monday beats a complete one delivered Wednesday.
5. **Assemble one document** in a fixed order: the week's shape, then per-person, then per-project,
   then the calendar. Do not merge or rewrite the sub-outputs: carry them with their links intact.
6. **Write one summary at the top**: the three things that need the user this week, each pointing
   into the section below it.

## Output

One document, in order:
- **This week needs you on:** three items, each linking down
- **Workstreams:** from `workstream-health` or the fallback
- **People:** one section per report
- **Projects needing decomposition:** only if config asked
- **Calendar:** conflicts and focus time
- **Run report:** which skills ran, which degraded, which failed

## Definition of done

Every section is present or explicitly marked DEGRADED or FAILED, the run report is accurate, and
the top three items each point at a section.

**A quiet week produces a short review.** If nothing needs the user, say so in the summary and let
the sections be brief. An orchestrator that produces four pages regardless of input is how a
weekly routine gets abandoned in month two.

## When there is no data

- No reports configured: skip the people section, say so.
- All four skills missing: stop and say the pack is not installed, rather than producing an empty
  shell that looks like a result.

## Boundaries

- **Inherits every boundary of the skills it calls, and may not relax any of them.** If
  `one-to-one-prep` refuses to characterize a person, this does too, including in the summary.
- **Never send, post, create or schedule anything.** It assembles.
- Never fill a degraded section with its own analysis. Degraded means thinner, not invented.
- **Draft only**, to the user.

## Self-check

- Is the run report honest about what ran?
- Did I carry sub-outputs with their links rather than rewriting them?
- Did I avoid filling a degraded section with my own content?
