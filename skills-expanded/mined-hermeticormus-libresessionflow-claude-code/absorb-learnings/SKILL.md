---
name: absorb-learnings
description: "Distills what a session taught (project intent, direction, domain knowledge, decisions with their reasons, stakeholder context, working preferences) into persistent memory files that future sessions load. Use at the end of a deep session, after domain-modeling or architecture discussions, before /close, /compact, or /clear, or when the user says to remember what was learned."
user-invocable: false
---

# Absorb: session knowledge into persistent memory

> "What did this session teach us that no file in the repo can?"

Extract the understanding a session built and write it where the next session will find it. Not code patterns (those live in the code) and not task state (that is the handoff's job). Absorb keeps **intent, direction, vision, domain knowledge, decisions, and preferences** that would otherwise evaporate when the context clears.

## Arguments

```
/absorb                  full session distillation
/absorb @project:<name>  scope to one project
/absorb @dry             show what would be saved, write nothing
```

## Where memory lives

Resolve the memory folder once, in this order:

1. `SESSIONFLOW_MEMORY_DIR`, if set.
2. `memory_dir` in the settings file `${SESSIONFLOW_CONFIG:-~/.claude/sessionflow.json}`, if the file exists and the key is not empty.
3. The Claude Code **auto memory** folder of the current project, when auto memory is on. Claude Code states that folder's path in the session context; it sits under `~/.claude/projects/<project>/memory/` and its `MEMORY.md` index is loaded at the start of every session.
4. Otherwise `<project root>/.claude/memory/`. The first time you create it, tell the user once that the files load automatically only if the project `CLAUDE.md` imports the index, by adding this line: `@.claude/memory/MEMORY.md`.

Print the folder you chose in the final report.

## Phase 1: extract (nigredo)

Scan the whole conversation for knowledge that is **not** derivable from the code, the git history, or existing docs.

Classify each finding into exactly one type:

| Type | What it captures | Goes to |
|---|---|---|
| **intent** | Why the project exists, who it serves, what problem it solves | `project_<name>.md` |
| **direction** | Current phase, priorities, what is being built now | `project_<name>.md` |
| **domain** | Business concepts, taxonomies, terminology, rules | `project_<name>.md` or a topic file |
| **decision** | An architectural choice and the reason behind it | `project_<name>.md` |
| **vision** | Long-term aspiration, design principles | `project_<name>.md` |
| **person** | A stakeholder's role, preferences, relationship to the work | `project_<name>.md` or `contact_<name>.md` |
| **feedback** | How the user wants to work: corrections, validated approaches | `feedback_<topic>.md` |
| **reference** | External resources, accounts, where a thing lives | `reference_<topic>.md` |
| **environment** | Services, ports, deployment layout, tooling facts | `reference_environment.md` |

For each finding, record:

```yaml
- insight: <one-line statement>
  type: <from the table>
  evidence: <what in the session shows this; quote or point at it>
  novelty: new | extends | contradicts | duplicate
  weight: critical | important | useful | noise
```

Drop everything marked `noise` or `duplicate`.

## Phase 2: purify against what is already saved (albedo)

Read the memory folder's `MEMORY.md` and every topic file the findings touch.

| Novelty | Action |
|---|---|
| **new** | Create a new entry |
| **extends** | Merge into the existing entry; add detail, do not duplicate |
| **contradicts** | Replace the old entry with the new truth and say why it changed |
| **duplicate** | Skip |

Rule: what this session actually observed beats an older assumption. When the session contradicts memory, the new observation wins, with its reason.

## Phase 3: structure (citrinitas)

### Project files

```markdown
---
name: <Project name>
description: <one line: what this project is>
type: project
---

## Intent
<why it exists, the problem, who it serves>

## Direction
<current phase, what is being built, near-term priorities>

## Vision
<what it becomes when it is "done">

## Domain knowledge
<concepts, taxonomies, terminology, rules not in the code>

## Key decisions
<Decision, because Reason.>

## Stakeholders
<who is involved, their role, their preferences>
```

Include only sections that have content.

### Feedback files

```markdown
---
name: <topic>
description: <the rule in one line>
type: feedback
---

<rule>

**Why:** <reason from the session>
**How to apply:** <when and where it kicks in>
```

### The MEMORY.md index

After writing topic files, update `MEMORY.md`:

- one line per file: `- [Title](file.md): one-line hook`
- keep each line short; the index points, it does not store
- Claude Code loads only the start of this file into every session (up to 200 lines, about 25 KB), so keep it an index and move detail into topic files

### Instructions belong in CLAUDE.md

If a finding is a **directive** rather than an observation (a terminology rule, a build command, an architecture constraint), propose adding it to the project `CLAUDE.md` instead. CLAUDE.md holds instructions for Claude; memory holds observations about the world. Show the proposed CLAUDE.md lines and add them only if the user agrees.

## Phase 4: write and verify (rubedo)

With `@dry`, print the planned changes and stop.

Otherwise write each file, then check:

- [ ] no duplicate entries across files
- [ ] no secrets, tokens, passwords, or connection strings; point at where a secret lives instead of copying it
- [ ] no ephemeral data (task ids, temp paths, today's progress)
- [ ] every topic file has frontmatter (`name`, `description`, `type`)
- [ ] `MEMORY.md` points at every new file
- [ ] entries read as durable facts, not session narration
  - Bad: "Today we discovered the catalog table has misfiled rows."
  - Good: "The catalog table mixes product rows and bundle rows; bundle rows have a null `sku` and must be filtered out of stock counts."

Then report:

```
ABSORBED
Memory folder: <path>
Project: <name or "cross-project">

Insights:
  + <insight> [<type>]
  ~ <merged into an existing entry> [<type>]
  - <skipped: duplicate or noise>

Files:
  <path>  [created]
  <path>  [<n> changes]

Depth: shallow | moderate | deep
```

`shallow` means facts only; `moderate` adds intent, direction, and some domain; `deep` covers intent, vision, domain, decisions, and stakeholders.

## What not to absorb

- code patterns, file paths, function signatures (read the code)
- git history (use `git log`)
- the fix for a bug (it is in the commit)
- anything already in a CLAUDE.md
- current task state (that belongs in a handoff)
- conclusions drawn from a single data point

The test: would a future session benefit from knowing this, **and** can it not be discovered from the codebase? Both yes: absorb it.

## Related plugins

| Plugin | Relationship |
|---|---|
| handoff | Handoff captures task state for the next session; absorb captures understanding for every future session |
| close | Close runs this method as its memory step |
| pickup | Future pickups benefit from what absorb saved |
| meet | Meet writes `contact_<name>.md` files into the same memory folder |
