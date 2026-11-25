---
name: harness-onboard
description: Orient a coding-agent session to an existing project harness by reading repository instructions, current work state, recent history, environment checks, and acceptance criteria. Use when starting or handing off a session in a project with harness files; do not claim tasks, start services, install dependencies, or mutate Git without authority.
---

# Harness Onboard

Build a concise, evidence-based orientation before implementation. The packaged SessionStart hook only reports that a harness exists; this skill performs the deeper read when needed.

## 1. Read the map

Start with applicable repository instructions, contributor documentation, package metadata, and architecture maps. Follow scoped instruction files for the directory being changed. Avoid loading every design document into context; open only what the task needs.

## 2. Establish current state

Inspect read-only state:

- current branch, status, and diff summary;
- recent commits relevant to the task;
- active plan, issue, feature, or acceptance criteria;
- progress or handoff notes;
- task locks and ownership, if the project uses them;
- validation commands and environment prerequisites.

Assume existing uncommitted changes belong to the user or another active task until proven otherwise.

## 3. Verify the environment proportionately

Run a safe, relevant health check. Do not automatically install packages, kill processes, start persistent servers, open browsers, or call external services. Ask when those actions require new authority.

If `init.sh` exists, inspect it before running it. A generated script is not automatically safe or applicable.

## 4. Select work

If the user provided a task, prioritize it over an internal feature list. Otherwise identify the highest-priority unblocked task from the repository's actual source of truth.

For parallel-agent projects, follow the documented claim protocol. Creating, changing, or deleting a lock is a mutation: do it only within the authorized workflow and never remove someone else's lock based only on age.

## 5. Handoff summary

Before implementation, be able to state:

- goal and acceptance criteria;
- relevant files and architecture constraints;
- current dirty state and ownership assumptions;
- environment or dependency status;
- plan, risks, and open questions.

At session end, update the repository's chosen task and handoff records only when the task authorizes those writes. Do not stage or commit automatically.
