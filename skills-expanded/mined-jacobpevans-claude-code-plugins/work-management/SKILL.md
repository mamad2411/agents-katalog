---
name: work-management
description: "Start work from a tracker card, rank a card or epic, or run the weekly work review, all by the work management
  standard. Use when asked to pick up a card, start a session on a task, score work, or review the board."
license: Apache-2.0
metadata:
  version: 1.0.0
  author: dryvist homelab
  hermes:
    category: workflow
    tags:
      - tracking
      - planning
      - prioritization
    related_skills:
      - track-followups
      - wrap-up
---

# Work Management

The card is the contract, not the tool. This skill holds three procedures: `start`, `rank` and `review`.
The **work management standard** owns every definition they use: the ready check, the four runner steps,
the score, the scales, the limits and the view names. Read it first. Never restate or guess a value from it.

## Read the standard first

The standard is the page `tools/work-management-standard` in the private documentation source. Read it
from the local clone of that source, or from the private docs site. If neither is readable, stop and say
so. Do not work from memory.

## start

Takes one card reference. Any runner can take a card. `<runner>` is the agent that will do the work.

1. Read the card and its epic through the tracker's own agent or tools.
2. Run the standard's ready check. If an item is missing, stop and list what is missing. Offer `rank`, or
   a question to the card's owner. Never fill a gap by guessing.
3. Check the In Progress limit on the card's board. At the limit, stop and name the cards that hold the slots.
4. Claim the card as the standard says.
5. Create a worktree the way the repository's contributor rules say. With Herdr,
   `herdr worktree create --cwd <repo> --branch <branch> --base <default-branch ref> --path <absolute path>`
   creates it and opens a workspace on it.
6. Build the goal with `/agentops:craft-goal` from the card's objective, its done-when check and what must
   not be touched.
7. Start the runner on the worktree. With Herdr: `herdr agent start <name> --kind <runner> --pane <id>`,
   then `herdr agent prompt <id> "<goal>"`. Without Herdr, print the goal and the worktree path so a person
   can start it.
8. Report one line: card, branch, and pane or path.

The session that does the work reports on the card and closes it as the standard says. A Claude Code
session ends with the `wrap-up` skill, which invokes the `track-followups` skill.

## rank

Takes one card or epic.

1. Read the item. Priority, Value and Risk Reduction belong to a person. Ask for each one that is empty,
   and put the standard's scale in the question. Never set them yourself.
2. For a task, propose its epic and a Job Size. Give one line of reason for each.
3. Write only what the person confirmed. Code sets the score. Never type one in.
4. A new epic must meet the standard's epic rules. If it does not, say which rule blocks it.

## review

Run weekly, or when asked. Use the skills already installed. If one is absent, skip it and say so.

| Question | Skill | Output |
| --- | --- | --- |
| Are Now, Next and Later still right? | `/product-management:roadmap-update` | Proposed column moves |
| Are the limits kept? | `/product-management:sprint-planning` | Items over a limit |
| What are the trends? | `/product-management:metrics-review` | Created against done, age, unscored |
| Who needs to know? | `/product-management:stakeholder-update` | One short update |

Also list every item the standard's `Audit:` views would show. Propose changes only. A person confirms
each move of an epic.

## Never

- Change Priority, Value or Risk Reduction without a person's answer.
- Delete or cancel a card.
- Start a card that fails the ready check.
- Copy client work from one tracker to another.

## Related Skills

- **track-followups** (this plugin): records new work that a session finds.
- **wrap-up** (this plugin): ends the session that did the work.
- **`/agentops:craft-goal`**: builds the goal the runner starts from.
