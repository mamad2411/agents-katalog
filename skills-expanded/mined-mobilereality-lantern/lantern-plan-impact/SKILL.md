---
name: lantern-plan-impact
description: Work out what a planned change touches from the Lantern map instead of guessing - `plan.mjs impact` lists the dependents and dependencies of the files, features or areas you start from, two hops out, with counts and the areas and features they belong to - and write the plan's `#impact` section from it, including the files the work will create. Use at step 2 of `lantern-plan`, and whenever the user asks "what would this touch", "what depends on this", "blast radius", "which areas does this change affect", "co to ruszy", in a project with a `.lantern/map`. Needs a settled map. Not for stages or approvals (`lantern-plan-stages`, `lantern-plan-review`).
---

# Lantern plan: impact

Impact is data, not opinion. The map records, per file, what it uses; `plan.mjs impact` turns that into
who is affected. You pick the seeds, read the output, and write down what the work really changes.
`$P` is the `lantern-plan` folder; run from the project root.

Write the `#impact` reasons in the map's primary language (`node $L/scripts/lang.mjs .`); paths and ids stay as they are.

## Pick the seeds

Start from what the request names, in this order, and use the first that fits:

1. A **feature** or **area** it names or clearly means: `.lantern/features`, `.lantern/areas` and the texts
   in `.lantern/lang/<code>/features.json` and `areas.json` say what each covers.
2. A **file** or folder it names. A folder ends with `/` and seeds every mapped file below it.
3. Behaviour with no name: search the purposes in `.lantern/lang/<code>/` for the words, take the files
   that match, and say so to the user as an assumption.

## Run it

```
node $P/scripts/plan.mjs impact --feature map-sync
node $P/scripts/plan.mjs impact --file skills/lantern-sync/scripts/sync.mjs --file src/main/lantern-prs.ts --depth 2
```

`--depth` follows relations further (1 to 4, default 2). A name the map does not have exits 2. It prints:

- **dependents**: files that use the seeds. A change to a seed can break them. Counts say how many seeds each reaches.
- **further dependents**: the second hop, files that use a dependent. Each is listed by path with its role,
  feature and area, and how many links reached it.
- **dependencies**: files the seeds use. Usually read, rarely changed. **Further dependencies** are the second hop.
- **by feature**, **by area**: the same files rolled up with counts. Start the section from these.
- **outside systems** the seeds talk to.

## Write the section

One `#impact` line per area, feature or file the work really changes, each with a one-line reason
(at most 160 characters):

```
node $P/scripts/plan.mjs add <slug> impact area build-the-map Plans are written beside the map.
node $P/scripts/plan.mjs add <slug> impact feature map-sync PR records gain a #plan line.
node $P/scripts/plan.mjs add <slug> impact file skills/lantern-sync/scripts/sync.mjs pr takes --plan and --item.
```

- **Names come from the output.** Copy them. `check` errors on an unknown one.
- **Edited files by path.** List every file you will change, one `file` line each. A plan that names four
  files for a feature that touches twenty hides most of its impact: the Lantern app marks the files you name
  and, quieter, their direct neighbours, and its "plan files only" filter shows exactly those.
- **Which of the listed files are relevant**: write one into `#impact` when the work changes it, or must
  change in step with a seed (a caller whose contract moves, a type or schema the seed shares, a test that
  pins the behaviour, a doc or map file that describes it). Skip a file that only reads a seed's stable
  surface and is not changed, a second-hop file with no reason to change, and anything in the output you
  cannot give a reason for in one sentence. A dependent that only calls a seed can go in as its feature,
  with the count in the reason ("6 dependents in map-sync").
- **Propose the files the work creates.** `new` is a kind next to `file`, `feature` and `area`; the reason
  is the file's purpose, one line, what it is for:

  ```
  node $P/scripts/plan.mjs add <slug> impact new src/main/lantern-plan-load.ts Loads every plan with the PRs that tick its items.
  node $P/scripts/plan.mjs add <slug> touch s1.1 new src/main/lantern-plan-load.ts
  ```

  Choose the path where it would sit among its neighbours in the map. A `new` path that already exists gets
  a warning: it is a `file`. A new path that a stage or item touches needs its `#impact new` line, or
  `check` errors.
- **Name areas only when the work lands in them.** An area that merely has a dependent is not impacted.
- **A new feature is not in the map yet.** Do not invent an id. Say it in the item title or in a
  `scope-in` line; the next map refresh gives it a record. A new *file* is different: name it with `new`,
  it needs no id.
- **A large reach is a finding.** More than one area, or dozens of dependents, belongs in a `risk` line and
  usually means smaller stages.
- **A file the map lacks** (`check` says it exists but is unmapped) means the map is behind: stop, tell
  the user to refresh it.

Stage and item `#touch` lines use the same names; `check` warns when a touch is not covered by this section.
