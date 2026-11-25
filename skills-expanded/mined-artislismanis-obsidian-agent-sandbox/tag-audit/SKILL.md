---
name: tag-audit
description: Find and merge tag variants (e.g. #project vs #Project vs #projects) across the vault. Use when the user asks to audit tags, consolidate tag variants, normalise tag casing, or clean up tag sprawl.
---

# tag-audit

Vault tags drift over time: the same concept ends up as `#project`, `#Project`, `#projects`. This skill finds those variants, proposes a merge plan, and applies it once the user approves.

**Read `../reviewed-edit/references/vault-safety.md` before your first write.** It carries the shared rules: the three write modes, per-file delete confirmation, plan-before-applying, one unit at a time. For this skill the unit is one variant cluster. Print the merge plan and get approval before the first rewrite.

## When to use

- "Audit my tags."
- "Consolidate `#foo` and `#Foo` into one."
- "Which of my tags are used only once?"
- "Normalise my tag casing."

## Do not use

- Adding new tags to notes (use `vault_frontmatter_set` or direct edits).
- Single-file tag lookup (use `vault_tags` directly).

## Tool chain

### Phase 1: Discover

1. **`vault_tags`**: returns every tag with a usage count. Sort by count to find the heavy hitters and by name to spot adjacent variants.
2. Identify candidates: tags that differ only in case, plurality, or a separator (`-` vs `/`). Rare tags (count 1–2) are also worth reviewing: they may be typos or abandoned.
3. If the user uses frontmatter-style tags (a `tags:` YAML key), also run **`vault_properties`** with `property: "tags"` to get distinct values with counts.

### Phase 2: Propose a merge plan

For each variant cluster, write the plan as a human-readable list before doing anything. `vault_tags` returns `#tag: N` per line, so restate it in plan form:

```
Merge plan:
  #Project: 12 → merge into #project  [canonical]
  #projects: 3 → merge into #project
  #proj: 1     → merge into #project
```

Present to the user and wait for explicit approval. Don't apply without it.

### Phase 3: Apply

For each `variant → canonical`:

1. **`vault_search`** with query `#variant` to get the list of affected files (or use `vault_tags` output if it lists files).
2. For each affected file, **`vault_search_replace`** with `search: "#variant"` and `replace: "#canonical"`. Prefer case-sensitive so you don't mangle similar substrings.
3. If the vault uses frontmatter `tags:` arrays, also use `vault_frontmatter_set` to rewrite the array per file, or `vault_batch_frontmatter` with a dry-run first.

Apply one variant cluster at a time, not all at once: a review modal then shows a coherent diff per merge instead of interleaving three merges across the same file.

### Phase 4: Verify

Run `vault_tags` again. Confirm the canonical tag's count increased by exactly the merged total and the variants are gone.

## Rules

- **Never** rename without a plan printed first.
- Case-insensitive dedup is usually wanted, but ask before assuming `#FooBar` and `#foobar` are the same: they may be intentional in some vaults.
- Watch for `#project/sub` hierarchies: don't rewrite `#project` in a way that breaks nested tags.
- After a merge, the backlinks in a `[[Note#Tag]]` link anchor are NOT tags: don't rewrite those.

## Example flow

```
User: "My tags are a mess, lots of duplicates."

1. vault_tags
   → #Project: 12, #project: 5, #projects: 3, #task: 30, #Task: 1, #daily: 8, ...
2. Propose:
     Merge #Project, #projects → #project  (total will be 20)
     Merge #Task → #task                    (total will be 31)
3. User approves.
4. For #Project → #project:
     vault_search(#Project) → [notes/foo.md, notes/bar.md, …]
     For each: vault_search_replace(#Project → #project, caseSensitive: true)
5. For #Task → #task: same.
6. vault_tags
   → #project: 20, #task: 31, #daily: 8
   Confirmed.
```
