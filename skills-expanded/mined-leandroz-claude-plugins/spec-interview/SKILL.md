---
name: spec-interview
description: Refine a rough SPEC.md into an implementation-ready specification through a multi-round interview, then break it into ordered tasks. Use when starting a new feature or turning a rough idea into something a developer can build without asking questions.
---

# Spec interview

Read `SPEC.md` in the working directory — a rough idea or draft spec — and turn it into a document someone unfamiliar with the conversation could implement without coming back with questions. Act as a senior technical PM and systems architect: the value is in the questions the user hasn't thought to ask themselves.

## Before asking anything

Explore the parts of the codebase the spec touches. Existing patterns, related files, conventions, architecture. This is what separates grounded questions from generic ones — you'll catch conflicts with code that already exists, spot reuse, and avoid proposing a design that fights the repo.

## The interview

Use `AskUserQuestion`, 2–4 related questions per round. Good questions point at a specific part of the spec, say what ambiguity or risk prompted them, and offer concrete options with their tradeoffs. Anything already answered in the spec is wasted.

`references/interview-dimensions.md` lists the areas worth probing — edge cases, data modeling, security, performance, state transitions, integrations, UX detail, rollout, observability, testing, tradeoffs. Read it when you want a prompt for where to dig; most specs only have real ambiguity in a few of them, and the interview should concentrate there rather than sweep everything.

Keep going round after round, letting each set of answers open the next. Challenge assumptions when something looks risky, and name contradictions when answers conflict with each other or with the code you read.

When the spec would survive a handoff with no follow-up questions, say you're ready to write it and ask whether anything is still uncovered.

## Writing the spec

Write the complete specification back to `SPEC.md`: every decision made during the interview, exact behavior for the edge cases discussed, explicit non-goals and out-of-scope items, and acceptance criteria where they help. Then rename it after the feature — `SPEC-user-notifications.md`, and so on.

## Tasks

Check the project's `CLAUDE.md` first. If it has a checklist that covers this kind of work, build the breakdown on that instead of inventing a generic one.

Create the tasks with `TaskCreate`, each small enough for one focused session — many small beats few large. Give each a description carrying enough context to implement without re-reading the whole spec. Then wire the dependencies with `TaskUpdate` so nothing is scheduled before the work it builds on. Show the resulting list with `TaskList` so the user can review the order before work starts.

## After implementation

Once the tasks are done, verify the build passes and the feature actually works before judging code quality. Then review the changes against the spec for bugs and deviations, and make a simplification pass over what changed — the `simplify` skill covers that.

Use any verification or code-review skills installed in this environment for those passes; where none are, do the same work directly.
