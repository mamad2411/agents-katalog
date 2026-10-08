---
description: Phase 0b helper for w-task — load module-aware context by reading module README + features/*.md + workflow-links, then write context.md. Generic version of dev-task's streaming-docs-aware context load.
argument-hint: <task-slug> [<module-name>]
allowed-tools: Bash, Read, Write, Edit
---

# w-context-load

Build `context.md` for the current task by reading structured module docs
(README, features/*.md, workflow-links.md) when they exist, falling back to
git-grep file inventory when they don't.

Reads `.claude/workflow.yaml` to find:
- `workflow.module_docs_root`
- `workflow.feature_records_subdir`
- `workflow.workflow_links_filename`
- `project.module_glob`
- `project.src_dirs`

---

## Inputs

- `$1` — task slug (e.g. `CISTREAMIN-11-sign-up-api`)
- `$2` (optional) — module name override; otherwise inferred from intake.md

Reads `<state_root>/<task-slug>/intake.md` for title + description.

---

## Step 1 — Resolve module

If `$2` is provided, use it.
Otherwise, infer from intake.md:
1. Extract 3-5 keywords from title + description (nouns).
2. If `module_docs_root` set: `ls <module_docs_root>/` and match keywords against folder names.
3. Fallback: read first 30 lines of intake.md, look for explicit "Module: X" line.
4. If still ambiguous: pause, ask developer to pick from listed modules.

Write `state.yaml.module: <name>` once resolved.

---

## Step 2 — Read module README (if exists)

If `<module_docs_root>/<NN>-<module>/README.md` exists:
- Parse "Implementation Status" section — extract ✅ Complete and ⏳ Deferred lists.
- Parse "Depends on" / "Blocks" — cross-module deps.
- Note last update date and any "Last modified by task: <slug>" markers.

If absent: note "Module README not found — context will be code-only."

---

## Step 3 — Read feature records

If `<module_docs_root>/<NN>-<module>/<feature_records_subdir>/` exists:
- `ls` the subfolder, list all `*.md` files.
- For each file, read the "Constraints for future features" section.
- Cross-reference constraints against the current task keywords.
- Collect any "Conflict candidates" — features that touch overlapping concerns.

---

## Step 4 — Read code (filtered by README)

Use the Implementation Status ✅ Complete list to scope file reads:
- For each ✅ item, find the matching file under `project.module_glob` /
  `project.src_dirs` and read it.
- Skip ⏳ Deferred items — they don't exist yet.

If no README available, fall back to generic Phase 0b behaviour:
```bash
git ls-files | head -300
git grep -l "<keyword>" 2>/dev/null | head -20
```
Read top 3-5 matched files.

---

## Step 5 — Reuse check

Scan for cross-cutting utilities under `project.src_dirs` (e.g. `src/common/`,
`src/shared/`):
- Common guards, decorators, exceptions
- Shared services
- Already-installed libs from `package.json` / equivalent

---

## Step 6 — OQ surfacing

If `workflow.oq_docs_path` is set: invoke `w-oq-check <module-or-task-slug>`
and append its output under § Known Constraints in context.md.

---

## Step 7 — Write context.md

```markdown
# Context — <title>

## Task Summary
<intake title, ticket ID, module, developer notes>

## Module Snapshot
**Implementation Status (from README):**
- ✅ <list>
- ⏳ <list>

**Depends on:** <list>
**Blocks:** <list>

## Relevant Files
| File | Why relevant |
|------|-------------|
| ... | ... |

## Patterns Observed
<naming conventions, existing similar features>

## Available Utilities
<reusable guards/decorators/libs found in Step 5>

## Previous Feature Decisions
<constraints from features/*.md — omit section if none>

## Known Constraints
<OQs from w-oq-check + flags from README>

## Suggested Approach
<1-2 sentences>
```

---

## Step 8 — Update workflow-links

If `workflow.module_docs_root` + `workflow_links_filename` set:
- Path: `<module_docs_root>/<NN>-<module>/<workflow_links_filename>`
- Create from template if absent:
  ```markdown
  # Workflow Links: <module>

  | Task | Folder | Started | Status |
  |------|--------|---------|--------|
  ```
- Append row: `| <task-slug> | [<state_root>/<task-slug>/](...) | <date> | in-progress |`

---

## Output

Print to chat: "Context loaded for module `<name>`. Found N relevant files,
M previous feature decisions, K known constraints. Run /w-task to start planning."
