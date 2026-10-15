---
name: shapes-init
description: >
  Bootstraps the Shapes Specification for an existing project. Explores
  the codebase, interviews the engineer about architecture and constraints,
  creates a Profile defining what fields matter, then generates a rich graph
  of shapes and constraints capturing the project's intent, rules, and
  boundaries.
user-invocable: true
argument-hint: "[project-path]"
---

```!
shapes preflight --init 2>/dev/null || echo "Shapes CLI not found. Install it: cargo install shapes-cli"
```

# Bootstrap Shapes for a Project

If a project path was provided as an argument, change to that directory
(`cd $ARGUMENTS`) before running `shapes init`.

The goal is to capture not just what the code does, but the **meaning behind
it** — the intent, the unwritten rules, the domain knowledge that lives in
the engineer's head. Code tells you *what* exists. Shapes capture *why*.

## Contents

- Step 1: Initialize the Store
- Step 2: Explore the Project
- Step 3: Interview the Engineer
- Step 4: Create Shapes
- Step 5: Create Constraints
- Step 6: (Optional) Create a Profile
- Step 7: Validate and Show

## Progress Checklist

Copy this checklist and track your progress:

```
Bootstrap Progress:
- [ ] Step 1: Store initialized (`shapes init --kit <kind>`)
- [ ] Step 2: Project explored (manifest, docs, structure, source, tests, CI)
- [ ] Step 3: Engineer interviewed (all rounds complete, understanding confirmed)
- [ ] Step 4: Shapes created and TODO placeholders filled in
- [ ] Step 5: Constraints created and TODO placeholders filled in
- [ ] Step 6: (Optional) Profile created if enforcement is desired
- [ ] Step 7: Validated clean (`shapes validate` exit code 0)
```

## Step 1: Initialize the Store

Pick the kit that matches the project's domain:

```bash
shapes init                    # software (default)
shapes init --kit research     # experiments, datasets, hypotheses
shapes init --kit editorial    # books, articles, narratives
shapes init --kit minimal      # only `rationale` is required
```

The kit controls what fields appear in scaffolded shapes and
constraints — it is *guidance*, not enforcement. Enforcement is opt-in
via Profiles (Step 6).

## Step 2: Explore the Project

Read the project thoroughly before asking questions:

- **Project manifest** — `Cargo.toml`, `package.json`, `pyproject.toml`, etc.
- **README and docs** — understand purpose and architecture
- **Directory structure** — `ls` the top-level and key subdirectories
- **Key source files** — entry points, config, module definitions
- **Test structure** — reveals component boundaries
- **CI/CD config** — `.github/workflows/`, `Makefile`, build scripts

Build an initial mental model of what the project is, how it's structured,
and what patterns you can observe.

## Step 3: Interview the Engineer

This is the most important step. Code tells you *what* exists. Only the
engineer can tell you *why*.

**Autonomous mode:** If you are working autonomously (no interactive user,
CI/CD, benchmark, or headless context), skip the interview. Instead, infer
intent from the specification, README, code, and project structure. Document
your inferences in shape intent fields and mark `source: ai`. The engineer
can refine these later. Do not use AskUserQuestion when there is no human
to answer.

**Interactive mode:** Use the **AskUserQuestion** tool to ask questions
interactively in batches of 2-4 at a time. Wait for answers before asking
the next batch. Continue until you truly understand the project.

**Round 1 — Purpose and identity**:
- What problem does this project solve? Who uses it?
- What must this system get right above all else?
- What is deliberately out of scope?

**Round 2 — Architecture and trade-offs**:
- Why was this architecture chosen? What alternatives were considered?
- What are the key trade-offs?
- How does data flow through the system?

**Round 3 — Constraints and rules** (the most valuable round):
- What rules must every contributor follow but aren't documented?
- What mistakes shaped current conventions?
- What invariants must always hold? (security, performance, correctness)

**Round 4 — Domain knowledge**:
- What domain concepts does this model? Non-obvious business rules?
- What terminology needs explanation?

**Round 5 — History and evolution**:
- Most significant change the system has undergone?
- Known tech debt that shapes how new work is done?
- What would a new team member need to know on day one?

After each round, summarize and check understanding with AskUserQuestion.
Continue with additional rounds if answers reveal unexplored areas.

## Step 4: Create Shapes

Each call to `shapes create shape` writes a YAML file with `TODO:`
placeholders for every field the active kit expects, plus commented
stub blocks for `parents`, `children`, `constraints`, and `realization`.
Your job is to **`Read` the file and replace each `TODO:` with real
content**, uncommenting the stub blocks you need and deleting the ones
you don't.

```bash
shapes create shape --name "<ShapeName>" --kind <kind>
```

Flags:
- `--name` (required) — the shape's name.
- `--kind` (optional) — defaults to the active kit's default kind.
- `--description`, `--summary` (optional) — pre-fill those fields instead
  of leaving TODOs.
- `--profile <id>` (optional) — attach a Profile for enforcement (Step 6).

After running it, **read the created file** (the path is printed to
stderr) and use `Edit` to fill in the TODOs. Use `Edit`, not `Write` —
`Write` requires reading the file first anyway, and `Edit` is safer for
targeted changes.

Workflow per shape:

1. `shapes create shape --name X --kind feature` → note the file path.
2. `Read` the file. Every required field appears as `TODO: <hint>`. Every
   optional field appears as a commented `# field: TODO: <hint>` line.
   Stub `parents`/`children`/`constraints`/`realization` blocks are
   commented out at the bottom.
3. `Edit` the file: replace each TODO with real content; uncomment and
   fill in the stub blocks you need (set `parents:` for child shapes,
   `children:` for parent shapes, `constraints:` for governing rules,
   `realization:` for source-file pointers); delete stubs you don't need.
4. Repeat for each shape. Create children before their parent if you want
   to reference child IDs in the parent's `children:` block, or create
   the parent first and reference its ID in each child's `parents:` block
   — both are fine.

Shapes should be **rich and detailed**. Go deep — not just top-level
modules, but interfaces, patterns, data flows, and sub-features.

## Step 5: Create Constraints

Same flow as shapes:

```bash
shapes create constraint --name "<Name>" --kind invariant --enforcement machine
```

`--enforcement` accepts only **`manual`** (human review) or **`machine`**
(automated check) — never `human`.

The scaffold writes TODO placeholders for `description`, `rule`,
`intent.rationale`, and any other required fields the template declares,
plus commented stub blocks for `parents`/`children`/`realization`/
`evidence`. `Read` and `Edit` exactly as in Step 4.

Attach constraints to the shapes they govern by uncommenting the
`constraints:` block in each shape's YAML and listing the constraint IDs.

## Step 6: (Optional) Create a Profile

Profiles are **optional** and only needed if you want enforcement —
required intent fields, kind validation, lifecycle gates. If you're just
documenting intent and constraints, skip this step.

```bash
shapes create profile --name "<ProjectName> Profile"
```

The scaffold seeds the Profile with the active kit's field and kind
declarations as a sensible starting point. `Read` the file and edit:
toggle `required: true|false` per field, add or remove kinds, adjust the
lifecycle gates. Then attach the Profile to shapes/constraints by passing
`--profile <id>` to subsequent `shapes create` calls (or by editing
existing nodes' `profile:` field).

## Step 7: Validate and Show

```bash
shapes validate
```

If `shapes validate` reports errors (exit code 2), fix each issue and
re-validate. Repeat until exit code 0 — do not proceed with errors. The
most common failure is leftover `TODO:` placeholders that didn't get
edited; grep the `.shapes/` tree for `TODO:` to find them.

Once clean, show the final structure:

```bash
shapes tree shape
shapes tree constraint
```

Summarize what was created for the engineer — the key shapes, constraints,
and how they relate.

## Next Steps

After bootstrapping, these skills handle ongoing work:

- `/shapes:shapes-context` — teaches the shapes-first workflow; auto-triggers
  when starting work in a project with `.shapes/`
- `/shapes:shapes-maintain` — keeps the graph in sync with code changes;
  auto-triggers when editing code, preparing commits, or completing tasks
- `/shapes:shapes-archive` — archives stale amendments when their insight
  value has decayed
