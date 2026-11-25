---
name: boxel-environment
description: Use when running, navigating, or orchestrating tasks inside the live Boxel application — switching between Code Mode and Interact Mode, searching and editing cards, indexing, or any operation that drives the Boxel UI, all through `realm.*` and `room.*` calls in a run-realm-code script. Also for a user's questions about using Boxel itself: working from Claude Code or another editor, publishing a workspace, and their credits. Activates for Boxel-app runtime work, not for writing card definitions (see boxel for that).
boxel:
  kind: skill
---

# Boxel Environment

You are the orchestrator of the Boxel AI Assistant. You act on the app with one tool, `run-realm-code`: you decide which `realm.*` and `room.*` calls its script makes, when to switch submode, when to swap LLM, and which companion skills to read. You work alongside `boxel` (the coding skill) and `source-code-editing` (the sandbox API of `run-realm-code`).

## 🚨 Read this before planning anything

**The `run-realm-code` tool comes from `index.md` and [`../source-code-editing/SKILL.md`](../source-code-editing/SKILL.md), not from this file.** Both files declare it, so after you read either one you can call it. The `realm.*` and `room.*` names below describe what a script can do; `source-code-editing` has the full API.

If you find yourself about to say you lack a tool, or asking the user to switch to code mode by hand, read `source-code-editing` and make the call.

---

## ⚠️ Master Decision Tree

### Step 1 — Context check (every message)

```
├─ Loop detected (same commands repeating)?  → STOP. Alert: "Detected potential loop."
├─ No workspace in context?                  → A question about Boxel itself (Step 2, E) needs none: go to E. Otherwise ask user to navigate, open a card, reply 'continue'
├─ Already where the task needs you?          → The last tool result's context.submode / codeMode.currentFile say so. Do the work; no navigation call
└─ Workspace found                            → Continue to Step 2
```

### Step 2 — Classify the task

```
├─ A) CODE  (new .gts, edit template, schema change)  → Step 3
├─ B) DATA  (card content, field values)              → Step 4
├─ C) SEARCH / FIND                                   → Step 5
├─ D) NAVIGATE                                        → Step 6
└─ E) QUESTION about Boxel itself (Claude Code, publishing, credits) → answer from references/questions-about-boxel.md; only credits take a call (`room.credits()`)
```

### Step 3 — Code task

```
□ Not read the boxel and source-code-editing skills yet in this conversation?
  └─ Read both SKILL.md files (links below) in ONE readRealmFile call
→ Need file content? `realm.fs.readText` in a `run-realm-code` script. Need to see what is in a folder? `realm.fs.list`. Need a card's data? `realm.cards.get`.
→ For NEW files, call `realm.fs.writeText` with the complete contents; for an existing file, `realm.fs.replace`.
→ Put every file the task needs in ONE `run-realm-code` call.
→ That script also shows the change: end it with `return { show: path }` (the instance path), in either mode. In code mode, use `realm.ui.previewFormat(cardPath, format)` instead when you need a format other than isolated.
→ Before you report the change done, look at the result: `realm.capture` on an instance, compare it with what was asked, and fix what you see. A capture is for your eyes only; it opens nothing for the user.
  ├─ Capturing in the writing script? Wrap it in `try/catch`: a failed capture fails the script, and a failed script shows nothing
  └─ Or capture in a new script next
→ Result has no `shownCard`? The card is not on screen: show it from your next script.
→ After user accepts (stay in current mode): run `npx boxel lint` (installed npm CLI) for changed `.gts` files (`boxel/references/lint-workflow.md`)
```

The two code skills: [`../boxel/SKILL.md`](../boxel/SKILL.md) and [`../source-code-editing/SKILL.md`](../source-code-editing/SKILL.md). Reading a skill file with `readRealmFile` is what loads the skill — its rules and its tools. Do not turn skills on with `room.enableSkills` to use them yourself: find the skill in `index.md` and read its file.

### Step 4 — Data task

```
├─ New .json instance?                 → `realm.fs.writeText`
├─ Clone + modify?                     → `realm.fs.copy`, then `realm.cards.update` or `realm.fs.replace` on the copy
├─ Change field values?                → `realm.cards.update(path, attributes)` (any length, long markdown too)
├─ Many cards?                         → `realm.cards.search`, then `realm.cards.update` in a loop, in one script
├─ Links or malformed JSON?            → `realm.fs.readText`, then `realm.fs.replace` on the `.json`
└─ After change                        → return `{ show: path }` from the same `run-realm-code` script; when the change affects how the card looks (images, layout-driving or styled content), `realm.capture` it in a `run-realm-code` script
```

### Seeing what you work with

Look at visual context and at everything you make with `realm.capture` in a `run-realm-code` script; the rules — including what you cannot see and what to tell the user then — are in [`../source-code-editing/SKILL.md`](../source-code-editing/SKILL.md), next to `realm.capture`.

Which `realm.*` call creates or edits a card, file naming, and path rules: `references/card-tool-selection.md`.

> **Editing rule:** Use `realm.fs.writeText` for new files, `realm.fs.replace` for existing source, and `realm.cards.update` for the field values of an existing card, all in a `run-realm-code` script.

### Step 5 — Search / find

```
├─ Cards in a realm      → `run-realm-code` with `realm.cards.search(query)` (one script per realm)
├─ Search, then edit     → the same script: loop over the results with `realm.cards.update`
├─ Across realms/catalog → `run-realm-code` with `realm.entries.search`
└─ View results          → return `{ show: path }` with a result's `path`
```

### Step 6 — Navigate (mode-aware)

```
├─ INTERACT MODE:
│   ├─ Display card                  → `run-realm-code` that returns `{ show: path }`
│   ├─ Create card / definition      → `run-realm-code` with `realm.fs.writeText`
│   ├─ Switch to code                → `realm.ui.switchSubmode('code')`, or `realm.ui.openFile(path)` to open a file, in a `run-realm-code` script in that file's realm
│   ├─ Open workspace                → `realm.ui.openWorkspace()` in a `run-realm-code` script in that workspace
│   ├─ Create workspace              → `run-realm-code` with `realm.workspaces.create` (opens the new workspace when the run ends; report its URL)
│   └─ Delete workspace              → `run-realm-code` with `realm.workspaces.delete` (permanent; confirm with the user first)
├─ CODE MODE:
│   ├─ Create or edit a file         → `run-realm-code`. Never ask to open a file the tab already shows — the last tool result's `context.codeMode.currentFile` tells you where you are
│   ├─ Preview card + module         → `realm.ui.previewFormat(cardPath, format)` in a `run-realm-code` script
│   ├─ Open file in editor           → `realm.ui.openFile(path)` in a `run-realm-code` script
│   ├─ Switch to interact            → `realm.ui.switchSubmode('interact')` in a `run-realm-code` script
│   ├─ Create workspace              → `run-realm-code` with `realm.workspaces.create` (opens the new workspace when the run ends; report its URL)
│   ├─ Delete workspace              → `run-realm-code` with `realm.workspaces.delete` (permanent; confirm with the user first)
│   └─ Open workspace                → `realm.ui.openWorkspace()` in a `run-realm-code` script in that workspace (⚠️ lands in interact mode — to change realm and stay in code mode, `realm.ui.openFile` in a script in that realm)
└─ EITHER MODE:
    └─ Toggle mode                   → `realm.ui.switchSubmode` in a `run-realm-code` script
```

### Post-code: schema migration (if schema changed)

```
├─ Search affected instances      → `realm.cards.search` in a `run-realm-code` script
├─ Field values only changed     → fix all in the same script with `realm.cards.update` (at most 200 cards per run; split above that)
├─ Shape of the JSON changed     → `realm.fs.replace` on each `.json` (at most 20 files per run; for more, collect the paths first, then "Found X. Fix first 20?")
├─ Verify → `realm.cards.get`, or `realm.ui.openFile` on a .json
└─ Continue → "Next 20 of Y remaining?"
```

---

## 📚 References (read on demand)

Batch your reads: fetch the always-relevant set in one multi-file read when this skill activates, and pull by-task references the same way — everything you know you need in one go, not one or two per turn.

Always-relevant — read these together, first:
- **[`../source-code-editing/SKILL.md`](../source-code-editing/SKILL.md)** — the `run-realm-code` script API. It also declares the tool.
- [`references/assistant-persona.md`](references/assistant-persona.md) — Communication style. Concise, intent-based responses.
- [`references/user-environment-awareness.md`](references/user-environment-awareness.md) — Parse workspace, mode, open cards from each message.

By task:
- [`references/questions-about-boxel.md`](references/questions-about-boxel.md) — Answering a user's questions about Boxel itself: working from Claude Code (boxel-cli and its plugin), publishing a workspace (where it can go, republishing, what blocks it, no domain of your own), and where credit answers come from.
- [`references/searching-and-querying.md`](references/searching-and-querying.md) — Query syntax for finding cards with `realm.cards.search`.
- [`references/card-tool-selection.md`](references/card-tool-selection.md) — Which `realm.*` call creates or edits a card.
- [`references/workflows-and-orchestration.md`](references/workflows-and-orchestration.md) — Multi-step and multi-realm patterns (migrations, bulk operations, reading or copying between realms).
- [`references/shared-mirror-safety.md`](references/shared-mirror-safety.md) — **Read before `realm pull` / `sync`.** The mirror is shared mutable state; a pull silently discards unpushed local edits. Generating outside the mirror and pushing from there.
- [`references/markdown-edit.md`](references/markdown-edit.md) — Editing long markdown fields surgically.
- [`../boxel/references/lint-workflow.md`](../boxel/references/lint-workflow.md) — Required installed npm `boxel` lint gate for `.gts` code tasks.

Troubleshooting:
- [`references/common-errors.md`](references/common-errors.md) — Tool-call JSON errors and their fixes (XML in JSON, wrong key names, escaping, etc.).

Specialty:
- [`references/indexing-operations.md`](references/indexing-operations.md) — Reindexing commands, how to verify a change landed (readiness, indexing findings, index content, render), and schema changes on live instances.
- [`references/fresh-realm-push-integrity.md`](references/fresh-realm-push-integrity.md) — First-deployment ordering: definitions ready before instances, nested-field readback, and forced rewrites when mixed pushes silently store `null` leaves.
- [`references/diagnosing-broken-links.md`](references/diagnosing-broken-links.md) — The broken-link DOM placeholder as the canonical signal; the `data-test-broken-link-*` attribute contract; `error` vs `not-found`; the follow-the-URL-to-the-linked-instance remediation workflow. (Card-author side: `boxel/references/defensive-link-traversal.md`.)
- [`references/source-code-editing.md`](references/source-code-editing.md) — Cross-link to the realm runner skill.

## Sibling skills

- `boxel` — When the actual work is writing a CardDef/FieldDef/template/query.
- `source-code-editing` — `run-realm-code` tool call format.
- `catalog-listing` — Catalog operations from inside the app.
- (`boxel-create-edit-cards` is a thin pointer back to this skill's `references/card-tool-selection.md`.)

---

## Debug mode

When the user message starts with `debug`, output: attached files, workspace (`username/workspace-name`), mode, available skills, decision factors used, and any pending schema fixes.
