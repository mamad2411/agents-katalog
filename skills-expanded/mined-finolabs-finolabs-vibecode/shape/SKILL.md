---
name: shape
description: Interview the user in short rounds, each with a recommended answer, until every decision an idea, plan or design depends on is settled. Use when the user wants to brainstorm, discuss, ideate, shape, stress-test or be grilled on an idea, plan or design, or requirements are unclear before building, in any language.
argument-hint: "<idea, plan or design to shape>"
---

# Shape

Turns an open idea, plan or design into decisions the user has made, one round of questions at a time, and acts on none of it until the user confirms the result.

Learned from `grilling` by Matt Pocock ([mattpocock/skills](https://github.com/mattpocock/skills), MIT); no text is copied.

**Topic:** $ARGUMENTS

## Which interview runs

Advisory (agent judgment), owner's order (12/11/2026):

1. This skill runs first.
2. `grilling` (`/grill-me`, or `/grill-with-docs` when the user wants a glossary and decision records kept) runs when this skill is not installed or the user asks for it by name; put its questions through the host's native question tool too.
3. Superpowers `brainstorming` only when the user wants many divergent design ideas rather than decisions, and it is installed.

In a Spec Kit repository this skill works inside a phase like the other phase tools and yields to Spec Kit's own clarify step. At router depth MIN, skip it unless the user asked for it.

## Procedure

Advisory (agent judgment); no hook or script enforces these steps.

1. **Map the decisions.** List what must be decided and draw the dependencies as a tree: a decision is open to ask only when every decision it depends on is settled.
2. **Split facts from decisions.** A fact the agent can find (a file, a command's output, a read-only subagent's search) is the agent's to find; never ask the user for it. Choices, priorities and trade-offs are the user's.
3. **Ask one round, in the native form.** Ask every open decision whose prerequisites are settled, and nothing that depends on an answer still missing. Each decision is one question in the host's native question tool (`AskUserQuestion` on Claude Code, `request_user_input` on Codex, `ask_question` on Antigravity), never a numbered text list: two to four options, your recommended option first with its trade-off in the option's description, the alternatives after it. A round larger than one call allows (four questions on Claude Code) is split across calls, blocking questions first. Plain text only when the session has no such tool, the tool fails, or the answer is free text. A question that waits on a lookup still running waits; ask the rest now.
4. **Update the tree.** Record each answer, add the decisions it opens, drop the ones it closes, and ask the next round.
5. **Close.** When no open decision remains, summarize what was decided and ask the user to confirm it. Act on nothing (no code, no file, no dispatch) before that confirmation.

When the user only wants many raw ideas, the first round offers two or three distinct directions as options; later rounds go deeper on the one they pick.

## Records

Advisory (agent judgment):

- Write each settled decision with its date where the work keeps its decisions: the work record's goal and acceptance section when `coding-router` created a work record, otherwise the plan, the issue or the pull request body.
- A decision the user cannot make yet stays open in that record, with who owns it and what would unblock it.
- In a delegated or headless run nobody can answer: list the open decisions with your recommended answers in the report, mark them unanswered, and never present a recommendation as the user's decision.

## Language

**Advisory (agent judgment):** Talk to the user in the language they are using, including questions and option labels; keep command names, flags, file paths, skill names and other technical names unchanged.
