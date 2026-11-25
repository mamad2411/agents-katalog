---
name: uru-context
description: Create, find, and maintain durable Uru Context. Use when work must remain available across threads or feed an Uru Agent's automatic retrieval.
---

# Uru Context

Context is durable workspace knowledge. It is the only Library resource that
feeds automatic Agent retrieval.

Use Uru Library tools for Context content and metadata. Use only tools visible
in the current catalog.

## Workflow

1. Search with `library_query` and `resource_type="context"`.
2. Read the best match before you create or change a Context.
3. Update the existing Context when the topic already exists.
4. Create a Context with `library_fs` and `op="write"` when no match exists.
5. Read the saved Context when exact content matters.
6. Report the path and the important change.

Create a Context at a clear Library path:

```json
{
  "op": "write",
  "path": "library/Contexts/Customer Research.md",
  "content": "# Customer research\n\nCurrent findings...",
  "create": true
}
```

Replace a complete Context only after a read:

```json
{
  "op": "write",
  "path": "library/Contexts/Customer Research.md",
  "content": "# Customer research\n\nRevised findings..."
}
```

Use `library_query` with `op="patch_preview"` before a complex patch. Apply the
same patch with `library_fs` and `op="patch"`.

## Content rules

- Keep one topic in each Context.
- Keep current facts. Remove old facts.
- Do not copy the same fact into several Contexts.
- Preserve source names, dates, links, owners, and confidence.
- Split a Context when separate topics need separate owners or update cycles.
- Use a title and path that people can find.

Do not ask for approval before a normal Context update. Follow the active tool
permission and confirmation rules.

## Scope and Agent retrieval

Use the `scope` field supported by Library operations for personal or workspace
Context. Use `library_collab` for access changes. Use `library_fs` for favorite
changes.

If the user requests a team or workspace-default setting that the visible tools
do not expose, report the missing capability with `report_friction`. Do not use
an old Context tool as a fallback.

Attaching a Context to an Agent makes it eligible for that Agent's automatic
retrieval. Other attached Library resources remain inventory. They require an
explicit tool read.

Read the Agent through `library_query` to inspect its current attachments. Edit
the returned Agent JSON through `library_fs` to change linked Context
references. Preserve fields that the request does not change.

## Links and backlinks

Use an id-pinned Library link when a tool or editor returns one. It survives a
rename.

Raw `[[Name]]` links resolve when Uru saves the Context. A backlink is derived
from the saved source. Do not edit a derived backlink directly.

Links and backlinks show relationships. They do not attach a Context to an
Agent. Collection membership also does not enable Agent retrieval.

Read `uru-library` for Library links, Collections, sharing, comments, labels,
versions, moves, trash, and restore.

## Stop rules

- Do not invent a Context id, resource slug, or Library path.
- Do not overwrite a Context that you did not read.
- Do not put secret values in Context.
- Do not use retired Context CRUD tools when the Library path is available.
- Stop after a failed write. Read the returned error and current resource
  state before you retry.
