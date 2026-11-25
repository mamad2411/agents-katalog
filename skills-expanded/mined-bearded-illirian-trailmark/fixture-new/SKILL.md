---
name: fixture-new
description: |
  Creates a parity fixture — the frozen scenario plus the contract its output
  must satisfy. Asks which skill and case, what shape the run must produce, and
  writes input.md and expect.yml. Ends by proving the new fixture actually
  fails on an empty directory.

  A fixture that passes when nothing ran is worse than no fixture: it reports
  coverage that does not exist. The last step exists to catch exactly that.

  Use when: "/fixture-new", "add a fixture", "cover this skill with a fixture",
  extending the parity suite to a skill it does not reach yet.
---

# Fixture-New Protocol

Writes one fixture: `fixtures/{skill}/{case}/` holding `input.md` and
`expect.yml`.

A fixture answers "did this runtime produce the same **shape** of work as the
reference one" — never "did it produce the same words". Two agents word an
artifact differently, and so does one agent twice.

## When to invoke

- A skill has no fixture and you want the parity suite to reach it
- An existing fixture covers the happy path and a second case is worth freezing
- Before claiming a runtime is supported for a skill nothing checks

## Input

The name of a shipped skill, a short case name, and knowledge of what that
skill's artifact looks like.

## Output

Two files under `fixtures/{skill}/{case}/`, plus a demonstration that the new
fixture fails when handed a directory with nothing in it.

## Hands off to

`$parity-check` — the skill that actually runs a fixture end to end.

---

## Step 0 — Locate the workspace root

```bash
test -d fixtures && test -d bin && echo "root ok"
```

Not there → walk up until `fixtures/` and `bin/` sit side by side.

---

## Step 1 — Name the fixture

Ask for the skill and a case name. Then check both:

```bash
ls aihub/.claude/skills/{skill}/SKILL.md      # the skill must exist
ls -d fixtures/{skill}/{case} 2>/dev/null      # the case must not
```

**Skill missing** → stop. A fixture for a skill that does not ship tests
nothing and will fail forever, which trains people to ignore red.

**Case exists** → stop and say so. Overwriting someone's fixture silently is
how a suite quietly loses coverage.

Case names read as `NNN-short-slug`: `001-add-endpoint`, `002-empty-input`. The
number orders them; the slug says what is being frozen.

---

## Step 2 — Decide the expected shape

Read the skill's own protocol to see what it writes, then fill these:

| Key | What to put | How to find it |
|---|---|---|
| `artifact` | filename glob, e.g. `plan-first-*.md` | the skill's artifact-writing step |
| `artifact_type` | value in `task_artifacts.artifact_type` | the skill's `INSERT` statement |
| `sections` | headings that must be present | the skill's artifact template |
| `gate` | substring proving an approval gate was offered | only if the gate lands **in the artifact** |
| `min_table_rows` | minimum rows in the first table | only when the protocol states a count |

**Headings are English.** The shipped skills write `## Plan`, `## Risks`,
`## Out of scope`. Writing a translated heading produces a fixture that fails
against a perfectly correct run — and it will be read as a broken framework,
not a broken fixture. Copy the heading from the skill's template, do not type
it from memory.

**Only assert what the artifact contains.** `plan-first` asks its mode question
in conversation, not in the file; asserting a gate there means permanent red.
Leave `gate` out unless the text lands on disk.

Pick assertions that would **notice a real divergence**. Three headings and a
database row catch a skill that half-ran. A single "file exists" catches almost
nothing.

---

## Step 3 — Write the task statement

`input.md` is handed to the agent verbatim. Write it as a task, not as a test:

- State the block of work in one or two sentences
- List the context the agent may assume — and keep it thin
- Say plainly that the context is minimal **on purpose**, so nobody later
  "fixes" the fixture by fattening it

The fixture tests the shape of the protocol's output, not the quality of a
solution to a real codebase. A statement rich enough to solve properly is a
statement rich enough to vary wildly between runs.

---

## Step 4 — Write both files

```
fixtures/{skill}/{case}/
  input.md      # the statement from Step 3
  expect.yml    # the keys from Step 2, one per line, list items as "  - value"
```

`expect.yml` is parsed by a small reader inside `bin/parity-run`, not by a YAML
library — a flat mapping with one nested list. Keep to that shape: no anchors,
no nesting beyond the `sections` list.

---

## Step 5 — Prove the fixture can fail

A fixture that never fails is decoration. Run it against a directory holding
nothing:

```bash
mkdir -p /tmp/parity-empty
bash bin/parity-run fixtures/{skill}/{case} /tmp/parity-empty --verbose
```

**Expected: non-zero exit, every assertion red.** That is the proof the
assertions are wired to something.

**If it passes** — the `expect.yml` asserts nothing real. Go back to Step 2 and
say what actually went wrong, rather than shipping a green fixture.

Then, if a real run of that skill exists, run against it too and read the
result. A fixture that fails on both an empty directory and a good run is
asserting the wrong shape.

---

## Anti-patterns

### ❌ A fixture that passes on an empty directory

The whole suite becomes a green light nobody earned. Step 5 is not optional.

### ❌ Translated headings

`## План` where the shipped skill writes `## Plan`. The fixture fails against a
correct run, and the reader concludes the runtime is broken.

**Rule:** copy headings from the skill's template.

### ❌ Editing a fixture until it goes green

The fastest way to a passing suite, and it destroys what fixtures are for.

**Rule:** change a fixture when it demonstrably expects the wrong shape — and
say that is what you are doing.

### ❌ A statement rich enough to be solved properly

The fixture then measures solution quality, which varies between runs and
between agents, instead of protocol shape, which should not.

---

## Step 99 — Log invocation (auto)

```bash
sqlite3 {routing_db} \
  "INSERT INTO skill_invocations (task_id, block_num, skill_name, invoked_at)
   VALUES ('{slug}', '{N}', 'fixture-new', datetime('now'))" 2>/dev/null || true
```

If `{slug}` / `{N}` are unknown the row is written with empty values; `|| true`
keeps a logging failure from aborting the skill.
