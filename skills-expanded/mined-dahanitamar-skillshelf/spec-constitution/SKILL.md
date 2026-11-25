---
name: spec-constitution
description: Write the repository's constitution — the principles, conventions, and verification command that specs, task lists, and implementation work should follow. Use at the start of a project, when conventions live only in reviewers' heads, when a team keeps re-litigating the same review comments, or when an agent keeps producing code that doesn't match the house style. Writes docs/CONSTITUTION.md. Does not describe features.
---

# Spec Constitution

A constitution answers one question: *what is true about this repository regardless of what we are building this week?*

That is a narrow question, and keeping it narrow is the whole job. The moment a constitution starts describing features, it becomes a spec that nobody updates. The moment it lists aspirations nobody enforces, it becomes decoration — and a document readers have learned to ignore is worse than no document, because the next reader still trusts it.

## The one rule

**A rule earns its place only if you can name what breaks when it's violated.**

- *"Write clean code"* — nothing breaks, because nothing is specified. Delete it.
- *"`domain/` imports no framework"* — business logic dissolves into controllers and becomes untestable. Keep it.
- *"Prefer functional style"* — a preference, not a rule. Delete it or make it enforceable.
- *"Every outbound call has a timeout"* — a missing timeout is a hang that propagates. Keep it.

If you cannot state the consequence, you are writing a mission statement.

---

## Workflow

### Phase 0 — Read the repository first

Existing practice outranks your preferences. Before proposing anything, look at:

- `package.json` / `pyproject.toml` / `go.mod` / `*.csproj` — the stack, and the scripts that already exist
- The directory tree — what layering is already implied
- 3–5 representative source files — actual naming, actual file sizes, actual error handling
- `.eslintrc` / `ruff.toml` / `.editorconfig` — rules already being enforced
- `README.md`, `CLAUDE.md`, `AGENTS.md`, `CONTRIBUTING.md` — rules already written down

**A constitution that contradicts the codebase it governs is a bug report, not a constitution.** Where the repo already does something consistently, document that. Where it does something inconsistently, that is a decision to surface — pick one and say which files are now non-conforming.

For an empty repository, skip to Phase 1 and derive from the stack instead.

### Phase 1 — Questions, at most four

Ask all questions in one message as a numbered list with a concrete default for each, and wait for one reply; if your tool has a structured-question feature you may use it. Never ask one at a time.

Only these four are ever worth asking, and only when the repo doesn't already answer them:

1. **What command proves the code works?** (`npm test`, `cargo test`, `pytest -q`, or "nothing automated yet") — this becomes `verifyCommand`, and it is the single most valuable line in the document. a task runner runs it after every task and nothing else.
2. **Which existing inconsistency should become the rule?** Only when Phase 0 found the repo doing the same thing two ways.
3. **What is non-negotiable here that an outsider wouldn't guess?** Regulatory constraint, a performance budget, a platform that must keep working, a dependency that may never be added.
4. **Who reads this code?** Solo · a small team · outside contributors. Decides how much the document explains versus states.

If the user says "you decide", decide. Record it under **Standing decisions** and move on.

### Phase 2 — Draft the principles

Three to seven. Fewer than three means you had nothing to say; more than seven means it is a wish list and readers will skim it.

Read `references/principles.md` for the test a principle has to pass and the catalog to draw from.

Each principle is one sentence stating the rule, plus one clause stating the consequence of breaking it. Nothing else.

### Phase 3 — Fill the mechanical sections

These come from the repository, not from taste. Layout, dependency direction, naming, size limits, tooling, and the verify command. State only rules this repo will actually follow.

**Size limits are the section most often written and least often honored.** Include only limits the linter enforces, or that you are willing to have a drift check report as a finding. A limit nobody checks teaches readers the rest of the document is optional too.

### Phase 4 — Write `docs/CONSTITUTION.md`

Follow this structure exactly:

```markdown
# <Repo Name> — Constitution

> Status: Active · <date> · Constitution version 1.0

## Principles
1. **<Rule.>** — <what breaks if violated.>

## Layout
<Top-level tree, one comment per directory: what may live there and what may not.>

## Dependency direction
<One line, then mechanical. e.g. "ui → services → domain ← db. domain/ imports no framework.">

## Naming
| Kind | Convention | Example |

## Size limits
| Unit | Soft | Hard |

## Tooling
| Concern | Tool |

## Verification
**Verify command:** `<the command, or "none — verified by reading">`
**Static analysis:** `<the dead-code / lint command, or "none">`
**Reviewed:** `<verify command verbatim> - <name> <date>, or "not reviewed">`
<What each covers, and what it does not.>

## Standing decisions
<Choices made without explicit confirmation, numbered so any one can be rejected.>
1. <decision> — <what changes if it's wrong>
```

Then tell the user the path and the verify command you recorded. Say that a task runner following this file should print the command and ask for confirmation before running it, and again whenever it changes. The `Reviewed:` line must contain the exact command, `Reviewed: <command verbatim> - <name> <date>`; a non-interactive run may execute the command only if it equals the text on that line, so editing the command in a pull request means editing the `Reviewed:` line in plain view. Record `Reviewed:` only when the user told you who reviewed it; never fill it in yourself.

---

## Boundaries

**This skill never describes a feature.** No entities, no endpoints, no user stories. If you find yourself writing about shifts or invoices or users, you have crossed into spec writing; stop.

**This skill never writes code.** It documents what code must look like.

**One constitution, and one spec set, per root.** This layout assumes one set of docs per repository root: `docs/CONSTITUTION.md`, `docs/SPEC.md` and `docs/changes/` all sit under one directory. For a monorepo, treat each package root as its own root: run these skills with `docs/` under that package directory and keep one constitution there. Not one per feature, and no shared or layered constitutions. For an agency or any set of similar repositories, copy `docs/CONSTITUTION.md` from a template repository into each root and keep a one-line `Template: <name> <date>` header so drift from the template is visible. A shared overlay is unsupported.

## Calibration

A solo weekend project gets principles, verify command, and naming — three sections, one page. A repo with outside contributors gets all of them, with layout and dependency direction carrying real weight because those are what a stranger gets wrong first.

## Reference files

- `references/principles.md` — the test a principle must pass, and a catalog by project shape
