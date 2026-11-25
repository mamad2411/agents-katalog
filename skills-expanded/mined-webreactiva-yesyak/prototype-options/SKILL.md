---
name: prototype-options
description: Builds a few navigable prototypes of what the interview decided, each in a different style or approach, with one subagent per option, a time limit and shared sample data, so the user chooses by looking instead of by reading. It then records the choice with the interview decisions. Use it whenever the user asks for prototypes, mockups, sketches, "show me how it will look", several visual styles or design options, or wants to compare approaches before the spec.
---

# Prototype options

A prototype answers one question: "is this what we decided?". It shows the decisions of `on-the-spot` on screen, without the full behavior. It is not the first version of the code.

## Before you start

1. Read `.scratchpad/<slug>/interview-decisions.md`. A prototype shows only what is decided there. A question that comes up goes to the user, not into the prototype.
2. Agree on three things with the user, with a recommended default:
   - How many options (default: three).
   - What changes between them: a visual style, a layout, an interaction or a technical approach.
   - What every option must show: the main path of the request, from the first screen or command to the result.
3. Prepare one small set of sample data that all options use. Take it from the real data when the project has data, so the user sees real names and sizes. Keep it in `.scratchpad/<slug>/prototypes/`.

## Build each option

Give each option to its own subagent, in parallel. Each subagent starts with a clean context, so its brief must hold everything:

- The decisions, the sample data path and the main path to show.
- Its option: what makes it different from the others.
- Where to write: `.scratchpad/<slug>/prototypes/<option>/`. Prototypes never go in the source tree.
- The smallest stack that shows the option: for example a static HTML page, a small script or a single component. Do not use the project's build unless the option needs it.
- A time limit (default: ten minutes). When the main path works, report. Do not polish.
- Before the final report, stop every server and close every browser that it started. A browser left open can block the next browser tool of the session.
- The report: how to open the option, what it shows, and what it leaves out.

Without subagents, build the options one after the other in the main session, with the same limits.

## Show and choose

1. Show the options side by side: how to open each one, one line about what makes it different, and one screenshot each if the environment can take them.
2. If an option is late, show the ones that are ready. Do not wait for all of them when the user is waiting.
3. Ask which option to keep, or which parts of each to combine.
4. Add the choice to `.scratchpad/<slug>/interview-decisions.md`, under its own heading, with what the user rejected and why. The spec uses the choice from that file.

The prototypes stay in `.scratchpad/`. The build of `execute-plan-loop` starts from the spec, not from the prototype code.
