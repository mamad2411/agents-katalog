---
name: near-duplicate-file-comparison
description: Forensic, rubric-driven comparison of two near-duplicate source files (e.g. `Foo.java` vs `Foo_old.java`) to determine which is canonical, what differs functionally, and whether the duplicate can be safely removed.
category: Code Hygiene & Maintenance
---

# Near-Duplicate File Comparison Skill

> **Skill ID:** `near-duplicate-file-comparison`<br>
> **Version:** 1.0.0<br>
> **Standard:** [Agent Skills (agentskills.io)](https://agentskills.io)

## Description

When two source files in the same directory have nearly identical names
(`Foo.java` + `Foo_old.java`, `helper.py` + `helper_backup.py`,
`Service.cs` + `Service.v2.cs`, …) and ostensibly the same purpose,
the agent MUST NOT settle for a shallow `diff`. This skill defines an
**eight-dimension forensic rubric** that proves which file is canonical,
quantifies functional drift, flags compile-blocking conflicts (same
class name in same package), and produces an actionable verdict
(keep / delete / merge).

It is the natural complement to the
[folder-comparison](../folder-comparison/SKILL.md) skill: folder
comparison answers *"are these two trees identical?"*; this skill
answers *"these two files are similar — what actually differs and which
one wins?"*.

## Prerequisites

| Requirement | Minimum |
|---|---|
| File access | Read access to both files |
| Optional | `diff` / `git diff --no-index` for line-level deltas |
| Optional | Language toolchain (`javac`, `tsc`, `python -m py_compile`, …) for compile-status dimension |

## When to Apply

Apply this skill when:

- Two files in the same directory share a base name with a suffix like
  `_old`, `_backup`, `_v1`, `_copy`, `.bak`, `_draft`, `_wip`, `_new`.
- The user asks to "compare these two files" and they are near-duplicates
  (not unrelated files).
- A directory listing or build error reveals a likely shadowed/duplicate
  class, function, or module.
- Before deleting a suspected obsolete file, to confirm nothing unique
  is lost.

Do NOT apply when:

- The two files are unrelated (use a normal `diff` or a code-review pass
  instead).
- Comparing whole directory trees (use
  [folder-comparison](../folder-comparison/SKILL.md)).
- Comparing two Git commits (use
  [git-commit-comparison-audit](../git-commit-comparison-audit/SKILL.md)).
- The user only wants a textual line-by-line diff with no judgement.

---

## Step-by-Step Procedure

### Step 1 — File Metadata Snapshot

Capture size and last-modified time of both files. Larger and/or
newer is a weak signal of canonical-ness, not proof — but useful
framing for the report.

```powershell
Get-ChildItem <fileA>, <fileB> | Select-Object Name, Length, LastWriteTime
```

```bash
ls -l <fileA> <fileB>
```

### Step 2 — Read Both Files in Full

Read each file completely (not snippets). The rubric requires
inspection of imports, comments, and dead/commented-out code that a
truncated read would miss.

### Step 3 — Apply the Eight-Dimension Rubric

For each dimension, fill the comparison table with concrete evidence
from both files. Do **NOT** skip a dimension because "it looks the
same" — explicitly record that fact.

#### 3.1 Header / Provenance

- Copyright header present? License? Author tag?
- Top-of-file Javadoc / docstring / module comment — does it correctly
  describe what the code does?
- **Red flag**: a comment that names a rule, ticket, or behaviour that
  the code below does **not** implement (mis-labelling).

#### 3.2 Imports / Dependencies

- Sorted, minimal, all-used vs. noisy with commented-out imports?
- Any import present in one file but missing in the other? Why?
- Dead imports (`// import …`) are a strong "scratch draft" signal.

#### 3.3 Class / Module Structure

- Same class name? Same package / namespace / module path?
- **Compile-blocker check**: in JVM / .NET / Go and similar languages,
  two files in the same package declaring the same public top-level
  type will not compile together. Filename suffixes (`_old`) do **not**
  rescue this — the type name inside is what matters. Flag explicitly.
- Same method signatures? Extra private helpers in one?

#### 3.4 Core Algorithm — the decisive dimension

Walk the primary method(s) step by step in both files:

1. Inputs consumed (which fields / collections / parameters).
2. Iteration shape (what is walked, in what order).
3. Predicate(s) applied.
4. Outputs produced (return value, side effects, framework
   `Status`/`Result` objects).
5. Edge-case handling (null, empty, error paths).

Decide whether the two implementations:

- Do the **same thing** (cosmetic-only differences).
- Do **different things** in the same domain (functional drift).
- One does the job; the other is **scaffolding / exploratory /
  always-success** (frequent for `_old` and `_draft` files).

#### 3.5 Error / Result Reporting Mechanics

- How are failures surfaced? (exceptions, framework status objects,
  return codes, logged warnings.)
- Placeholder / template-binding wiring (e.g. `placeholder_N` properties,
  i18n keys, structured log fields) — present in both? consistent?
- Side-channel output (`System.out.println`, `print`, `console.log`)
  that pollutes stdout is a "scratch draft" smell.

#### 3.6 Robustness / Defensive Coding

Score each file on:

| Concern | File A | File B |
|---|---|---|
| Null / nil checks on inputs | … | … |
| Empty-collection short-circuit | … | … |
| Null element skip inside loops | … | … |
| Trim-vs-isEmpty / whitespace handling | … | … |
| Stray debug logging | … | … |

#### 3.7 Compilation / Static Analysis Status

- Does each file compile **standalone**? (`javac`, `tsc --noEmit`,
  `python -m py_compile`, `go build`, …)
- If one only compiles because broken code is commented out, say so
  explicitly — uncommenting would fail (e.g. references to undeclared
  variables, missing imports).
- Any obvious lint violations (unused imports, dead code, shadowed
  variables)?

#### 3.8 Functional LOC Count

Strip blanks and comments, then count:

- Active functional lines in each file.
- Lines of commented-out scaffolding in each file.
- Net contribution to the program's behaviour (often **0** for `_old`
  files whose real logic is commented out).

### Step 4 — Produce the Comparison Report

Render the findings as a Markdown report with:

1. **Header table** — path, size, mtime, role guess.
2. **One H2 section per rubric dimension** (§3.1 – §3.8), each
   containing a 2-column table or prose comparison with concrete
   evidence (filenames + line refs).
3. **Summary verdict** — exactly one of:
   - `CANONICAL = <fileA>; DUPLICATE = <fileB>; SAFE TO DELETE`
   - `CANONICAL = <fileA>; DUPLICATE = <fileB>; MERGE UNIQUE BITS FIRST` — list the unique bits
   - `BOTH VALID, DIFFERENT PURPOSES; RENAME TO DISAMBIGUATE` — propose names
   - `INSUFFICIENT EVIDENCE; ASK USER` — list the questions
4. **Compile-blocker call-out** if §3.3 detected a same-type-same-package
   collision — this elevates the verdict's urgency.

All file references in the report MUST follow the workspace's
[markdown link conventions](../../../ai-agent-rules/markdown-generation-rules.md)
(no backticks around paths; `[path](path#Lline)` form).

### Step 5 — Authorized Cleanup (optional)

If the verdict is `SAFE TO DELETE` and the user authorizes it:

```powershell
Remove-Item <duplicate-path>
```

```bash
rm <duplicate-path>
```

If the file is tracked by Git, prefer `git rm <duplicate-path>` and let
the user choose between a fresh commit or folding it into an existing
one via the
[git-commit-edit](../git-commit-edit/SKILL.md) skill.

The agent MUST NOT delete a file before producing the report and
receiving explicit user authorization.

---

## Heuristics: Which Side Is Usually Canonical?

Weak signals — never decisive alone, but useful for framing:

| Signal | Canonical side |
|---|---|
| Filename has no suffix vs. `_old`/`_bak`/`_v1`/`_draft` | The unsuffixed file |
| Larger byte size with denser logic (not just comments) | The larger file |
| Has copyright header + Javadoc/docstring | The documented file |
| Has `@author` / `@since` tags | The annotated file |
| Cleaner imports, no `// import` lines | The clean file |
| Implements the rule named in its own header comment | The matching file |
| Compiles cleanly without commented-out blocks | The compiling file |
| Newer `LastWriteTime` | The newer file (weakest — refactor backups invert this) |

Conflicting signals MUST be reported in the verdict, not silently
resolved.

---

## Worked Example (sanitized)

Two files in the same package:

- `Rule0053.java` — 3,734 B, has copyright + Javadoc + `@author` tag,
  iterates the relevant domain entity (`SystemConst`), reports failures
  with framework placeholder binding, null-safe.
- `Rule0053_old.java` — 2,851 B, no header, single mis-labelling
  comment, prints to stdout, iterates an unrelated entity, has the
  real logic commented out (and the commented block references an
  undeclared variable), always returns success.

Both declare `public class Rule0053` in the same package, so they
**cannot compile together** — only the `_old` filename suffix prevents
the conflict from biting. Verdict:
`CANONICAL = Rule0053.java; DUPLICATE = Rule0053_old.java; SAFE TO DELETE`,
flagged with the compile-blocker call-out.

---

## Anti-Patterns (Forbidden)

- ❌ Producing a verdict from a `diff` alone, without walking the
  rubric.
- ❌ Treating "newer mtime" as proof of canonical-ness.
- ❌ Deleting a file before the rubric is filled in and the user has
  authorized the deletion.
- ❌ Skipping the compile-blocker check in languages where filename ≠
  type identity (Java, Kotlin, C#, Go).
- ❌ Reporting "they look the same" without explicit per-dimension
  evidence.

---

## Related Skills

- [folder-comparison](../folder-comparison/SKILL.md) — directory-level
  parity (broader scope, less depth-per-file).
- [git-commit-comparison-audit](../git-commit-comparison-audit/SKILL.md)
  — comparing two commits rather than two working-tree files.
- [deleted-files-audit](../deleted-files-audit/SKILL.md) — once a
  duplicate is removed, validate that no stale references remain.
- [git-commit-edit](../git-commit-edit/SKILL.md) — fold the deletion
  into the originating commit instead of producing a new one.

---

## Traceability

- Skill authored: 2026-05-16.
