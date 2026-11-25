---
name: arch-map
description: |
  Automatic linking of an artifact to project architecture elements.
  Two modes: file-mode (by file paths, for fast-track flows) and
  feature-mode (by artifact text, for briefs/specs).
  Merge logic: appends to existing arch_ref, does not overwrite.
  Propagate: final arch_ref written up the chain epic → spec → brief.

  Use when: after plan-first in fast-track / pipeline; after saving
  brief / spec artifact
---

# Arch-Map Protocol

Maps an artifact onto architecture elements from an `arch_items` catalog. Fully automatic — does not ask the user, does not block the task.

---

## Step 1 — Find platform DB

```bash
DB_PATH=$(find {projects_root} -name "platform.sqlite" -path "*/data/platform/*" | head -1)
```

Not found or empty:
```
Arch-map: platform.sqlite not found — arch_ref = null
```
End protocol. Continue task execution.

---

## Step 2 — Load arch_items

```bash
sqlite3 "$DB_PATH" \
  "SELECT item_type, slug, title, description, url, path
   FROM arch_items WHERE path != '' OR title != '';"
```

---

## Step 3 — Determine mode and find matches

### file-mode (fast-track / pipeline)

Source: `files_to_modify` from plan-first.

For each file: check whether `arch_item.path` is a substring of the file path or the file path starts with `arch_item.path`.

### feature-mode (brief / spec)

Source: full text of the artifact.

For each arch_item check: does `arch_item.slug`, `arch_item.title`, or `arch_item.url` appear in the artifact text (case-insensitive).

Collect unique matches. Format: `{item_type}/{slug}`.

---

## Step 4 — Show result

**Matches found:**

```
Arch-map (file-mode):
  api/billing      → api/billing/    [OK]
  page_front/auth  → src/pages/auth/ [WIP]
arch_ref: api/billing,page_front/auth
```

**No matches:**

```
Arch-map: no matches found — arch_ref = null
```

---

## Step 5 — Add arch_ref column (if missing)

```bash
sqlite3 {routing_db} \
  "ALTER TABLE artifacts ADD COLUMN arch_ref TEXT;" 2>/dev/null || true
```

---

## Step 5.5 — Save result to log

Write `{log_dir}/arch-map.md` with task, date, mode, full result output, arch_ref value. If `{log_dir}` unknown — skip without error.

---

## Step 6 — Merge and write arch_ref

`arch_ref` not null:

1. Read current: `SELECT arch_ref FROM artifacts WHERE id = '{artifact_id}';`
2. Combine current + new → split by comma, deduplicate, join back
3. Write: `UPDATE artifacts SET arch_ref = '{merged}', updated_at = '{date}' WHERE id = '{artifact_id}';`

Artifact not yet in routing DB → hold `{arch_ref}` as variable for future INSERT.

---

## Step 7 — Propagate up (file-mode only)

After writing final `arch_ref` into current artifact — update parents up the chain.

Read `epic_id`, `brief_id`, `tz_id` from task frontmatter or routing DB via `links`.

For each parent — merge-write with same `arch_ref`. Unknown parent ID → skip that UPDATE without error.

---

## Rules

- **Never block execution.** Any error → `arch_ref = null` → continue
- **Do not ask the user.** Everything determined automatically
- **Always show the result** — one line, even if `arch_ref = null`
- **Merge, not overwrite** — always read current arch_ref and combine
- **Deduplicate:** one `item_type/slug` only once
- **Separator:** comma without spaces: `api/billing,page_front/auth`
- **Propagate** runs only from file-mode (fast-track / pipeline), not from brief / spec

---

## Anti-patterns

### ❌ Overwrite instead of merge
Agent replaces existing arch_ref with new value → history of previous mappings lost. Rule: always read current arch_ref and merge.

### ❌ Block on missing platform DB
DB not found → agent stops the entire task instead of gracefully setting `arch_ref = null`. Rule: never block — arch_ref is optional context.

### ❌ Ask the user which items match
Agent shows candidates and asks user to confirm. Rule: fully automatic. No questions.

### ❌ Propagate from feature-mode
Feature-mode is for briefs and specs — parents don't exist yet. Propagate only from file-mode where the chain epic → spec → brief is already formed.

---

## Related skills

- **plan-first** — provides `files_to_modify` in file-mode
- **brief** / **tz** — invoke arch-map in feature-mode after saving the artifact
- **ship-first** — records final arch_ref at task closure

---

## Step 99 — Log invocation

```bash
sqlite3 {routing_db} \
  "INSERT INTO skill_invocations (task_id, block_num, skill_name, invoked_at)
   VALUES ('{slug}', '{N}', 'arch-map', datetime('now'))" 2>/dev/null || true
```
