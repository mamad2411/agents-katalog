---
name: write-guides-and-runbooks
description: >-
  Load this skill when writing or revising task docs for users or operators: user guides,
  getting-started and install guides, runbooks, troubleshooting. Trigger on "write a user guide",
  "ops runbook", "getting-started guide". Not for a whole docs set (use write-project-docs).
disable-model-invocation: false
user-invocable: true
license: Apache-2.0
---

# Write Guides and Runbooks

Write task-oriented docs that let a reader reach a goal without already knowing the system. Two
audiences, never blurred. When a request covers both (common for internal tools), the user's tasks
go in `docs/guide/` and the operator's in `docs/operations/`. Never interleave end-user steps with
privileged operator commands.

|           | **User guide**                        | **Operator guide / runbook**                              |
| --------- | ------------------------------------- | --------------------------------------------------------- |
| Reader    | Uses the product to do their own work | Installs, configures, runs, monitors, recovers the system |
| Asks      | "How do I do _my_ task?"              | "How do I keep this healthy and fix it when it breaks?"   |
| Assumes   | No internals; UI/CLI surface only     | Shell access, infra context, privileged credentials       |
| Worst day | "I can't figure out how to do X"      | "It's down at 2am and I'm on call"                        |
| Voice     | Friendly, plain                       | Terse, precise, copy-pasteable                            |

## Procedure

### 1. Pin down audience, scope, and source of truth

Pin these down before writing. When `ceh-documentation:write-project-docs` called this skill, its
survey table already answers 1, 3, and 4: take them from it rather than re-deriving them. When
sources conflict (the README says `uvicorn`, the user says Docker), the user's stated setup sets
the scope. Record the contradiction as an open item.

1. **Audience**: user, operator, or both? Sets voice, assumed knowledge, structure.
2. **Scope**: name the tasks in scope. Covering everything covers nothing.
3. **Source of truth**: code, CLI `--help`, config, existing draft. **Never invent commands, flags,
   env vars, or UI labels.** Mark anything unverifiable `[VERIFY: …]` and surface it, do not guess.
   Fabricated docs are worse than missing ones: they break trust on first use.
4. **Prerequisites/environment**: supported OS/versions, access, dependencies.

### 2. Pick the document type

Most guides combine a getting-started front and a how-to body.

| Type                       | Reader's goal                   | Spine                                                                                                                                                            |
| -------------------------- | ------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Getting Started**        | Zero to first success           | Install → configure → run the smallest real task → "you're set up" — under `write-project-docs`, install → run → verify, with configuration left to how-to pages |
| **How-To Guide**           | One specific task               | Goal → prerequisites → steps → verify → troubleshoot                                                                                                             |
| **User Manual**            | Reference for the whole product | Task-grouped chapters + feature reference + glossary                                                                                                             |
| **Operator Runbook**       | Operate/recover a system        | Architecture → routine ops → incident procedures → escalation                                                                                                    |
| **Install / Config Guide** | Stand the system up correctly   | Requirements → install → configure → verify health → common failures                                                                                             |
| **Troubleshooting**        | Diagnose a known failure        | Symptom → cause → fix, as a lookup table or flat entries                                                                                                         |

### 3. Structure the pages

Read `${CLAUDE_PLUGIN_ROOT}/references/docs-standard.md` ("the standard" below) before writing. It
fixes the layout, file naming, page anatomy (H1, breadcrumb, summary, footer), Markdown rules, link
rules, markers, and the report format. Everything below is what is specific to guides.

**Where files go.** Work against `<root>`: the project path the caller or user gave, else the
current working directory. This skill writes **two sections of the standard**, one per audience:
user tasks under `<root>/docs/guide/` and operator content under `<root>/docs/operations/`, each
with its own `index.md` hub. Docs that already live elsewhere are edited in place, never relocated.

A focused single-topic guide is one file, `docs/guide.md` (standard §1). Anything broader is a
tree:

```text
docs/guide/
├── index.md            # hub: every page, grouped, each with "read this when…"
├── getting-started.md
├── troubleshooting.md
└── how-to/             # HT-NN
    ├── HT-01-reset-password.md
    └── HT-02-export-data.md

docs/operations/        # OP-NN — the operator's own section, never interleaved with the guide
├── index.md            # hub
├── OP-01-install.md
├── OP-02-configure.md
└── database/           # OP-DB-NN
    ├── OP-DB-01-backup.md
    └── OP-DB-02-restore.md
```

- **User-only guide:** write `guide/` alone, no `operations/` section.
- **Operator-only runbook:** write `operations/` alone. The operator's first success is the install
  page, so there is no `getting-started.md`. Symptom-keyed entries live in the incidents page, so
  `troubleshooting.md` is dropped too unless end users also hit errors.

Numbering, prefixes, the two-page minimum for a folder, and renumbering all follow standard §3. A
**runbook page** (the multi-procedure `OP` pages) is thin when it would hold one procedure of under
five steps: merge it into its neighbour and renumber. A one-task how-to page is never merged for
being short, and Concept and Reference pages are never thin.

**User guide skeleton.**

```text
getting-started.md   — shortest path to first success; no options
how-to/HT-NN-<task>  — one task per page: goal, prerequisites, steps, verify, if it fails
troubleshooting.md   — symptom or literal error text → cause → fix
```

Feature and settings detail belongs in `docs/reference/` (see `write-api-reference`). Link to it
from the how-to pages instead of copying it into an appendix. When there is no reference section,
end the guide with a `## Reference` section on the page that needs it.

**Operator guide / runbook skeleton.**

```text
operations/OP-01-system-overview  — Concept: components, data flow, where things run (Mermaid), the "Names used in this guide" table
operations/OP-02-install          — How-to: prerequisites, steps, post-install health check
operations/OP-03-configuration    — Reference: each setting's name, purpose, default, valid values, effect
operations/OP-04-routine-ops      — How-to: start/stop/restart, change a setting, deploy, backup, rotate secrets
operations/OP-05-monitoring       — How-to: what to watch, healthy ranges, where dashboards and logs live
operations/OP-06-incidents        — How-to: per symptom, detection → diagnosis → remediation → verification
operations/OP-07-recovery         — How-to: rollback, restore from backup, escalation when the runbook runs out
```

Each page keeps one mode: OP-01 explains and OP-03 lists, so neither holds a procedure. Changing a
setting is a procedure in OP-04. **Under `write-project-docs`**, drop OP-01 and OP-03: the overview
belongs in `docs/concepts/` and the settings in `docs/reference/configuration.md`, and the runbook
links to both instead of repeating them. Renumber the remaining pages from `OP-01` (standard §3), so
install becomes `OP-01-install`.

### 4. Write each procedure

A how-to page holds one task. Three kinds of page group several: `troubleshooting.md`, the runbook
pages that name several operations (`OP-04-routine-ops`, `OP-06-incidents`, `OP-07-recovery`), and
a single-file guide. On those, each procedure is a `##` section with the same body, and a `##`
section that is not a procedure (a constraint such as "Do not scale past one replica") is short
prose with no When/Prerequisites block. Drop any of the three bullets that would be empty or
obvious: **Time / impact** is usually "seconds, no downtime" for a library.

An **incident entry** (`OP-06-incidents`, and operator entries in `troubleshooting.md`) is headed
by the symptom and uses these fields in place of the three bullets: **Detection** (the alert or
what the operator sees), **Cause**, then numbered steps (diagnosis first, remediation after), then
**Verify** and **If it fails**.

````markdown
# HT-02 — Rotate the API signing key

[← Guide](../index.md)

Replace the signing key without logging users out. Run this when the key is due for rotation or may
have leaked.

- **When:** <triggering condition — for runbooks, the alert or symptom>
- **Prerequisites:** <access, tools, preconditions>
- **Time / impact:** <duration; for ops, whether it causes downtime>

1. <Action>. <Result the reader can confirm.>

2. <Action>.

   ```bash
   actual --command --here
   ```

   Expected output:

   ```text
   the real output to compare against
   ```

**Verify:** <the single check that proves it worked>

**If it fails:** <1-2 likely failure modes + fix, or a link to troubleshooting>

---

[← HT-01 Change your email](HT-01-change-email.md) · [Guide](../index.md) · [HT-03 Export data →](HT-03-export-data.md)
````

Step standards:

- One action per step. If a step has an "and", consider splitting.
- A warning is the first block **inside** the dangerous step, indented 3 spaces:
  `> **Warning:** this drops the table.` (standard §7).
- Bold UI labels exactly as shown: click **Advanced settings**.
- Fence every command the reader runs as a step. A short command or path named inside a sentence or
  table cell stays inline (standard §5).
- For destructive/irreversible ops, state blast radius and recovery in the same block.
- Cross-reference, do not repeat: link to the canonical procedure instead of copy-pasting it.

### 5. Self-review

- [ ] Every command, flag, path, env var, UI label comes from a real source, none invented;
      unverifiable items marked `[VERIFY: …]`.
- [ ] A reader with only the stated prerequisites can complete each task end to end.
- [ ] Each procedure ends with a verifiable success check.
- [ ] Prerequisites and warnings precede the steps that need them.
- [ ] User and operator content are not interleaved.
- [ ] Numbered = ordered; bullets = unordered.
- [ ] Destructive ops state blast radius and recovery.
- [ ] Spine is tasks, not a feature dump.
- [ ] Terminology is consistent throughout.
- [ ] Every page passes `${CLAUDE_PLUGIN_ROOT}/references/docs-standard.md`: file names and prefixes
      (§3), H1 + breadcrumb + summary + footer (§4), Markdown rules (§5), every link and anchor
      resolves (§6), markers verbatim (§7).
- [ ] Each section's `index.md` lists every page of that section, grouped, in reading order.

## Rules

- **Task-oriented, not feature-oriented.** Organize by what the reader wants to _do_ ("Reset a
  password"), not by what the software _has_ ("Settings Panel"). Feature detail goes in the
  reference, not the spine.
- **One procedure = one numbered list.** Numbered = ordered sequence; bullets = unordered options
  only.
- **Every step has a verifiable result.** "Click **Save**; the banner turns green." A step the
  reader cannot confirm is broken.
- **Imperative, second person.** "Run the migration", not "The migration should be run."
- **Show the exact thing**: real command, bolded UI label, real path, real output. No
  `<placeholder>` without a concrete example beside it.
- **Prerequisites up front**, never buried in step 4.
- **Write for the reader's worst day**: front-load the answer, defer the theory.
- Never bury an assumed or invented detail in confident prose.

## Output

Files under `<root>/docs/guide/` and `<root>/docs/operations/` in the layout of step 3. End the
reply with the report of `${CLAUDE_PLUGIN_ROOT}/references/docs-standard.md` §10. When
`write-project-docs` called this skill, return only the rows and open items for it to merge.
