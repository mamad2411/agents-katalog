---
name: wikicommit-remove
description: Mark a wiki page (and its translations) as removed and prepare a removal PR
disable-model-invocation: true
---

# wikicommit-remove

Skill for removing a wiki page. Does not physically delete the file — it only performs a soft delete by setting `status: removed` on the target page (`DesignDoc-data.md §4.5`). This hides the page from the published wiki while preserving Git history and rollback capability.

## Usage

```
/wikicommit-remove <page>   # e.g. /wikicommit-remove .wikicommit/entity/ja/Person/yamada-taro.md
```

## Processing Flow

### Step 1: Confirm the Removal Reason

Confirm the removal reason with the user:

- `obsolete` (content is outdated or no longer needed)
- `merged` (merged into another page — also confirm the path of the merge target page)
- `gdpr` (personal data removal request, etc.)

If the target page doesn't exist, or already has `status: removed`, this is detected in step 2 — here, only confirm the reason.

### Step 2: Run `remove_page.py`

```bash
python .claude/skills/wikicommit-remove/scripts/remove_page.py <page> --reason <reason> [--merged-into <path>]
```

- When `--reason merged`, always add `--merged-into <path of the merge target page>`.
- On exit code `1` (error), present the output as-is to the user and stop. Expected errors:
  - The target page doesn't exist
  - The target page already has `status: removed`
  - `--reason merged` was given but `--merged-into` was not
  - The file pointed to by `--merged-into` doesn't exist

This script automatically does the following:

1. Sets `status: removed` / `removed_at` / `removed_reason` (and `merged_into` for `merged`) on the target page's frontmatter
2. Searches across all Type directories for translated pages that have the target page as their parent via `translated_from`, and applies the same `status: removed` etc. to them
3. Removes the corresponding entry from the `index.md` of any affected Type directory

### Step 3: Report Results

Extract the `REMOVED: <path>` lines from `remove_page.py`'s stdout and report them to the user as a list, including both the original page and any translated pages.

### Step 4: Guidance on Next Steps

```
Next steps:
- Run /wikicommit-merge to perform quality checks, PR creation, and merge
  (if any broken WikiLinks are detected, they will be shown as warnings.
   They won't block the merge, but if needed, use /wikicommit-remove separately
   to remove the referencing pages too, or fix the links manually)
```

## Notes

- Do not commit or create a PR against `main` or any branch (that is `wikicommit-merge`'s responsibility)
- Do not physically delete files (only sets the `status: removed` flag)
- Do not write to `.wikicommit/schema/` (read-only)
