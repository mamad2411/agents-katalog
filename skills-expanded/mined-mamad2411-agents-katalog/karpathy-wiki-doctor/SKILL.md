---
name: karpathy-wiki-doctor
description: |
  Detached doctor only. Whole-wiki census: tests, schema, tags, frontmatter,
  related, rewrite jobs. Does not rewrite page bodies. Launched by wiki doctor
  or when doctor cadence is due. Main agent never loads this.
---

# karpathy-wiki doctor (detached census)

You are the detached wiki doctor. Wiki root is `${WIKI_ROOT}`. Run id is
`${WIKI_RUN_ID}`. Perform this census yourself. Do not launch another model.

## Completion

After the census succeeds:

```bash
bash "${WIKI_PLUGIN_ROOT}/scripts/wiki-complete-doctor.sh"
```

Exit non-zero if that helper fails.

## Steps

1. Run `wiki-archive-schema-proposals.py --wiki-root "${WIKI_ROOT}"` so leftover
   proposal files sit under pending archive, not in a live inbox.
2. Read `<wiki>/schema.md` and category `_index.md` files.
3. Read `.ingest-issues.jsonl` and `.doctor-runs.jsonl` if they exist.
4. Run page validation and tag lint (`wiki-validate-page.py`,
   `wiki-lint-tags.py`).
5. Collapse same-idea tag pairs. Lint is a detector; also use `tag-drift`
   lines in `.ingest-issues.jsonl`. Skip pairs that are not the same idea.
   For each same-idea pair run
   `wiki-collapse-tag.py --wiki-root "${WIKI_ROOT}" --same-idea <a> <b>`.
   One spelling remains on pages, indexes, and Tag Taxonomy. Do not write
   `==` synonym pairs. Do not treat historical `==` schema lines as the
   collapse plan.
6. Patch schema.md via `wiki-schema-patch.py` (objects, tags, categories,
   extra Page contract keys).
7. You may fix frontmatter, tags, and related lists. Leave page synthesis
   unchanged.
8. If a cluster needs a playbook body, write one rewrite job under
   `<wiki>/.wiki-pending/rewrite-jobs/` naming the object token and pages.
   Do not execute the rewrite.
9. Complete through the helper.

## Done

Tests ran, schema objects/tags/categories match the index, rewrite jobs
are recorded when a body rewrite is needed, page bodies are unchanged.
