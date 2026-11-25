---
name: plan
description: >
  Plan an approved phase before its code: cut it into end-to-end slices, each with its files, test plan,
  acceptance and dependencies, ready to become bd subtasks. Use when an OpenSpec phase, a ready spec or a bd
  task is approved and the code is about to start ("plan the phase", "break this into tasks"), and as the
  rules the tech lead follows when the feature pipeline asks for a plan. Next: build-tdd.
---

# Skill `plan` — a phase into slices

> Part of the dark-factory plugin. Reads the gate commands from `.claude/factory/feature-pipeline.json` in the project's main
> checkout (the first path of `git worktree list`) when the project has it. The same rules serve a person's session and the pipeline's tech lead.

A plan is a list of slices. Each slice, once committed, works from the entry point (webhook, route, command,
dispatcher) to the result for at least its own scenario and is covered by a test at the entry level. Never slice by
layers (data, then API, then UI) and never "all tests first, then code": between such slices the feature is not wired
up and a dead path passes every test.

## Steps

1. **Read** the project's rules (`AGENTS.md`; a solo-kit project without one: `CLAUDE.md`), `CODING_STANDARDS.md` and the source: the OpenSpec change (`proposal.md` with its WHEN/THEN
   scenarios, `design.md` when present, the phase in `tasks.md`), the spec, or the bd task.
2. **Read the actual code** the phase touches: repositories, services, dispatchers, settings, scheduled jobs,
   migrations. Plan edits to real files, not imagined ones; cross-check the design's "as-is" (file:line) if it has one.
3. **Cut the slices.** Fewer, file-coherent ones: a slice is the test file(s) and code file(s) that are always edited
   together. Split only along a real boundary — different files, or a dependency (the migration and repository are
   needed by the service, the service by the dispatchers). A file edited by two slices belongs to one of them; the
   other depends on it. The first slice is the narrowest scenario in full (with its migration, if one is needed).
4. **One edit node.** When the change sits on a path several entry points reach (a shared dispatcher, a ladder of
   branches), name the shared node, not each branch, and pin the behaviour at every entry point with its own test case.
5. **Write each slice:**
   - `key` (`3.1`), `title` in the project language (≤70 characters);
   - `description` — what exactly to do, tied to the requirement it closes;
   - `files[]` — paths from the repository root, new files and test files included;
   - `testPlan` — each test with its layer from `CODING_STANDARDS.md` §Test pyramid (the project's layers and
     directories) and what it checks; a rule goes to the lowest layer that can check it (a pure function — unit),
     api only for the HTTP contract (the `build-tdd` step 4 rule);
   - `acceptance` — criteria a reviewer can check; `blockedBy[]` — keys it depends on.
6. **Check before you hand it on** — the commonest faults of a plan:
   - every existing path in `files[]` exists (`ls`); test files are found where they live (`find <tests> -name …`) —
     suites live in several folders, and a wrong guess creates a duplicate instead of extending one;
   - every method, field and function named in a description or acceptance exists (`grep -rn "def <name>"`), or a
     slice adds it;
   - every message catalog key a slice needs is added by a slice that edits the catalog;
   - a requirement map: each requirement (a MUST of the spec, a `tasks.md` item, an acceptance criterion of the bug)
     names the slices that close it; none is left without one.
7. **Forks** — a safe default (KISS/YAGNI; a new flag defaults to off, the old path stays behind it), written down as
   an assumption. In a person's session, a fork that needs a product decision goes to the owner instead.
8. **Record the plan:**
   - in a session: the slices become children of the phase's bd task —
     `bd create --parent=<phase id> --type=task --title="…" --description="…\n\nFILES: <files>\nTESTS: <testPlan>" --acceptance="…" --design="key: <key>"`,
     then `bd dep add <slice> <dependency>` for each `blockedBy`. The feature pipeline (`feature-core`) can build the
     same graph unattended;
   - in a workflow: return the plan in the format the task asks; the run creates the subtasks itself;
   - without a bd queue: write the slices into the change's `tasks.md` (or, with no change folder, a checklist in the
     PR description) with the same fields — key, title, files, tests, acceptance, depends on.

No code and no commits while planning. Next: **`build-tdd`**, one slice at a time in dependency order.
