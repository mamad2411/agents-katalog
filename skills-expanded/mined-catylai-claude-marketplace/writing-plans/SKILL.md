---
name: writing-plans
description: "Turns an approved spec into an implementation plan whose tasks each list exact files, the signatures they consume and produce, real code and real commands, with the spec's global constraints copied into the header so a single dispatched task carries them. Use after design-intake's architectural path, or when a spec or written requirements exist and the work is multi-step. Not for producing the design (use design-intake); not for running the plan across workers (use release-train)."
when_to_use: "write an implementation plan, turn this spec into tasks, break this spec into tasks, I have requirements and need a plan, task breakdown for the spec"
argument-hint: "[path to the spec, or the feature name]"
allowed-tools: Read, Grep, Glob, Bash(date *), Edit(docs/plans/**), AskUserQuestion
license: MIT
---

# Writing plans

Produce the document that stands between an approved spec and the code someone writes.

The spec: $ARGUMENTS — if this is a path, read it; if it is a feature name, look for a matching
file under `docs/specs/`; if nothing is found, ask for the spec's location.

Write for a skilled engineer who has no context for this codebase, its tooling or its domain, and
who sees one task at a time. Each task goes to a fresh session with no history once the plan is
dispatched, so everything a task needs — files, code, test, command, expected output, commit — is
in the task.

## Preconditions

- A plan argues from a spec. With no spec and no written requirements, run `design-intake` first:
  a plan written from a conversation has no authority to settle a conflict between two tasks.
- A spec covering several independent subsystems gets one plan per subsystem, each producing
  working, testable software on its own.
- One plan, one repository. Paths are repository-relative, so a cross-repository change gets one
  plan per repository, cross-referenced in each header.

## Where the plan goes

`docs/plans/<YYYY-MM-DD>-<feature-name>.md`, with the date from `date +%F` — plans sort by date,
so a guessed one misfiles it. An existing repository convention for plan location wins.

**Without a checkout (Cowork/web):** ask the user to paste the spec and today's date, then print
the plan for them to save.

## Map the files first

Before writing any task, list which files will be created or modified and what each is
responsible for. Task boundaries are drawn on this map.

- One clear responsibility per file; prefer smaller, focused files that fit in context.
- Files that change together live together — split by responsibility, not technical layer.
- Follow existing patterns; plan a split only for a file this work modifies that has already grown
  unwieldy.

## Task sizing

A task is the smallest unit that carries its own test cycle and that a reviewer could reject while
approving its neighbour. Fold setup, configuration and docs into the task whose deliverable needs
them. Within a task, each step is one action of a few minutes: write the failing test, watch it
fail, implement minimally, watch it pass, commit. Where the repository has its own test
conventions, follow them.

## The plan header

```markdown
# <Feature> implementation plan

> Executor: <release-train (dispatched) | inline in one session>. Steps use `- [ ]` checkboxes so
> progress is visible in the file.

**Goal:** <one sentence>
**Architecture:** <two or three sentences>
**Tech stack:** <key technologies>
**Spec:** <repository-relative path to the spec>

## Global constraints

<The spec's project-wide requirements — version floors, dependency limits, naming rules, licence
headers — one line each, values copied verbatim. Every task implicitly includes this section.>
```

- **`Spec:`** makes the spec the authority, so a conflict between tasks mid-execution is settled by
  reading it rather than by an arbitrary ruling.
- **Global constraints** are copied, not referenced, because a dispatched worker receives one task
  and neither the plan nor the spec. Copy exact values: `node >= 20`, not "a recent Node".
- **Executor** is stated so the plan is not run in whatever way its opener prefers.

## The task template

````markdown
### Task N: <component>

**Files:**
- Create: `exact/path/to/new_file.ts`
- Modify: `exact/path/to/existing.ts:123-145`
- Test: `tests/exact/path/to/new_file.test.ts`

**Interfaces:**
- Consumes: `parseConfig(raw: string): Config` from Task 2
- Produces: `applyDefaults(c: Config, env: Env): Config` — returns a new object, never mutates

- [ ] **Step 1: write the failing test**

```ts
test("applyDefaults fills the retry count from env", () => {
  expect(applyDefaults({ retries: undefined }, { RETRIES: "3" }).retries).toBe(3);
});
```

- [ ] **Step 2: run it and confirm it fails**
Run: `npm test -- applyDefaults` — Expected: FAIL, "applyDefaults is not defined"

- [ ] **Step 3: write the minimal implementation**

```ts
export function applyDefaults(c: Config, env: Env): Config {
  return { ...c, retries: c.retries ?? Number(env.RETRIES) };
}
```

- [ ] **Step 4: run it and confirm it passes**
Run: `npm test -- applyDefaults` — Expected: PASS

- [ ] **Step 5: commit**
`git add src/config/defaults.ts tests/config/defaults.test.ts && git commit -m "feat(config): apply env-derived defaults"`
````

**Why `Interfaces`:** an implementer who sees only its own task cannot look up what Task 2's
`parseConfig` returns, so it invents a plausible name and shape, and the code fails to link with
its neighbours. Exact signatures — names, parameter and return types, and any contract the type
does not express — prevent that. `Consumes` also records the dependency edges: consuming from Task
2 means depending on Task 2.

**Why exact `Files`:** paths are what prove two tasks are disjoint. Write full paths, not globs
like `src/config/**`, which read as precise but hide overlaps.

## Write real content in every step

These are plan defects, because each reads as fine only to someone holding the whole design:

- "TBD", "TODO", "implement later", "fill in the details".
- "Add appropriate error handling / validation / edge cases" — name them.
- "Write tests for the above" without test code.
- "Similar to Task N" — repeat the code; tasks are read in isolation and out of order.
- A code step with no code block.
- A type or function no task defines.

## Self-review

Run once, yourself, after the plan is complete, and fix inline:

| Pass | Method | Fix |
| --- | --- | --- |
| Spec coverage | Walk each spec requirement; point at the task implementing it | Add tasks for the gaps |
| Placeholder scan | Search for every pattern in the list above | Write the content |
| Type consistency | Compare names and signatures across tasks | Reconcile — `clearLayers()` vs `clearFullLayers()` is a bug |
| Path consistency | Compare `Files:` blocks: modified but never created? created twice? a shared registry file in several tasks? | Add the creating task, merge the colliding tasks, or give the shared file to one task |

## Handing off for execution

For dispatched execution, `release-train` decides which tasks can run in parallel: it takes each
task's `Files:` block as the owned paths, `Files: Create:` as planned new paths, the run-and-confirm
steps as acceptance criteria, and `Interfaces: Consumes` as dependency edges. Its skill owns the
disjointness check and merge order; see it for the details.

Once saved, offer the choice rather than picking:

> "Plan saved to `docs/plans/<name>.md`. Two ways to run it: dispatched with `release-train`, one
> worker per bundle in its own worktree; or inline, working the tasks in order here with a review
> checkpoint at each. Which?"

Say that inline execution skips the fresh-reviewer gate at each task boundary.

## Verify

Before offering execution: the file exists at the stated path; the header has a `Spec:` line that
resolves; every task has `Files`, `Interfaces` and a run-and-confirm step; and the self-review found
no remaining gaps.

<example>
Weak task: "Task 4: add config loading. Similar to Task 2; handle errors appropriately."
Strong task: "Task 4: config loader. Files — Create `src/config/load.ts`, Test
`tests/config/load.test.ts`. Interfaces — Produces `loadConfig(path: string): Config`, throws
`ConfigNotFound` when the file is missing. Steps with the test code, `npm test -- load` expecting
FAIL then PASS, and the commit."
</example>
