---
name: init-mission-base-workflow
description: Bootstrap the mission workflow in a project by ensuring AGENTS.md carries the path-addressed mission workflow guidance.
---

# init-mission-base-workflow

Bootstraps the mission-driven workflow inside a project. Its duty is `AGENTS.md`: it ensures that file carries the `## Mission Workflow` guidance, which tells anyone working in the project where missions live and how each is named and finished. It probes nothing and creates no mission directory or other scaffold — `/define-mission-goal` checks the workflow's runtime prerequisites each time it runs and creates each mission's directory directly in its scope. Run this **once** per project, before any other workflow skill, and once more after upgrading a project whose `AGENTS.md` still carries the older `## Milestone Workflow` section.

This skill is idempotent: it creates `AGENTS.md` when it is missing, appends the section when the file holds neither heading, and replaces an older `## Milestone Workflow` section whole, carrying the project's principle store to the workspace root in that same pass, but never rewrites a `## Mission Workflow` section already there or any line outside the section it writes. It commits `AGENTS.md`, with the store's old and new paths when it moved the store, as one path-scoped commit.

## Usage

```
/init-mission-base-workflow
```

No arguments.

## Workflow

### 1. Detect existing state

Check whether `AGENTS.md` exists at the workspace root. If it does, read it and note whether it contains a `## Mission Workflow` section — any section under that heading, whatever its text says — and, when it holds none, whether it contains a `## Milestone Workflow` section, the older section an earlier copy of the plugin wrote.

If a `## Mission Workflow` section is present, the project is already bootstrapped: stop without changing anything and committing nothing, whether or not an older section stands beside it, and print this one line and nothing else:

```
Workflow already bootstrapped — the guidance section is present.
```

### 2. Write the workflow guidance into AGENTS.md

Write the `## Mission Workflow` section exactly as `${PLUGIN_ROOT}/shared/workflow-guidance.md` states it, by the one of that file's three cases that applies: **if `AGENTS.md` does not exist**, create it with the minimal content shown there; **if it exists and holds neither heading**, append the section to the end of the file, leaving every existing line untouched; **if it holds the older `## Milestone Workflow` section**, replace that section whole as the third case states, from its heading line down to the line before the next `# ` or `## ` heading or to the end of the file, leaving every line outside it untouched.

### 3. Carry the principle store over

Only when step 2 replaced an older section: if `milestones/answer_decision_principles.md` stands in the working tree and `answer_decision_principles.md` does not stand at the workspace root, copy the store to the root unchanged, byte for byte, with this one command:

```
cp milestones/answer_decision_principles.md answer_decision_principles.md
```

Leave the old file in place: step 4's commit removes it, so the move lands in the same commit as the section. When both files stand, or only the root one does, or neither, move nothing; a run that created `AGENTS.md` or appended the section moves nothing either.

### 4. Commit the bootstrap

Read and follow the shared commit procedure at `${PLUGIN_ROOT}/shared/commit-procedure.md`, running its one commit-tool command yourself as this step's one git tool call. Supply it these inputs:

- **PATHS** — this skill's own change set: `AGENTS.md`, which step 2 created, appended the section to, or replaced the older section in, and also `answer_decision_principles.md` when step 3 copied the store.
- **REMOVALS** — `milestones/answer_decision_principles.md` when step 3 copied the store, and none otherwise.
- **SUBJECT** — `Workflow-bootstrap: missions`.

Supply no BODY: the commit is subject-only. Hand the path over unchanged — uncommitted changes already present in `AGENTS.md` before this run (for example a file just written by `/init`) are swept into this commit, with no status probe beforehand, no stop, no confirmation, no hunk-level staging, and no advisory.

The commit tool runs the dirty-own-path guard, the store's removal when one is named, the path-scoped staging, and the commit, so the section and a moved store land as one commit.

### 5. Confirm

On the success path — the commit in step 4 recorded the bootstrap — print exactly one fixed terse status line and nothing else:

```
Workflow bootstrapped.
```

Do not say whether the file was created, appended to, or had an older section replaced, or whether the store moved, name the commit, or add any next-step or handoff pointer; the commit diff shows what was written.

If instead the step-4 commit tool printed `Nothing committed — none of the paths changed.` (the file already matched the last commit, so nothing was committed), do not print the terse line — print this one fixed line and nothing else:

```
Bootstrap committed nothing — the guidance already matched the last commit.
```
