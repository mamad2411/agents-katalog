---
name: outline-skills
description: Operate Outline knowledge bases through the Outline CLI. Use for documents, collections, search, users, groups, comments, attachments, sharing, revisions, and related workflows.
allowed-tools: Bash(outline-cli *)
---

# Outline Skills

Use `outline-cli` for Outline tasks. Start with the requested operation; do not run authentication checks or load setup instructions unless needed.

## Content guidance

Create native, readable Outline content rather than walls of text or ASCII substitutes. Actively choose headings, bullet/numbered lists, task lists, tables, quotes, code fences, callouts, attachments, and Mermaid diagrams to suit the material. Use tables for comparisons, code fences for commands, and diagrams for flows.

### Internal document references

When referencing another document within the same Outline workspace, proactively try a document mention instead of a plain Markdown link:

```markdown
@[Document title](mention://document/target-document-uuid)
```

Resolve the actual target UUID through search/info; do not guess it. Existing `--text` / `--text-file` inputs can create this document-icon chip. Ordinary `[title](/doc/id)` links are not the same node.

Markdown reads serialize document mentions as ordinary links. A full Markdown read-edit-write is therefore lossy: re-express intended references with mention syntax, and do not assume all original rich-text nodes are preserved.

### Math and diagrams

Use `$x^2 + y^2$` for inline math and dollar-delimited blocks for display math:

```markdown
$$
\int_0^1 x^2\,dx
$$
```

Avoid `\(...\)` and `\[...\]`, which may remain plain text. For diagrams, use a `mermaid` code fence rather than ASCII art.

## Obtain only what the task needs

- **Locate:** search with a small limit and bounded snippets. `--titles-only` changes search semantics, not just output.
- **Read/summarize/edit:** obtain complete text directly; never edit a truncated preview or fetch raw JSON just to get the body.
- **Specific information:** use `--fields` for complete values from original API paths, without unrelated objects. Paths apply across lists; filtering is local, not server-side.
- **Debug:** reserve `--raw` for inspecting complete API responses.

```bash
outline-cli search "topic" --limit 5 --max-text-chars 200
outline-cli documents info --id "document-id" --text-only
outline-cli documents info --id "document-id" --fields data.id,data.title,data.revision
```

Default output is compact JSON. Use `--max-text-chars 0` for no previews, `documents info --full-text` for full-body JSON, or `--text-only` for exact Markdown. See [output controls](references/output.md) for field paths, warnings, and constraints.

Put global connection flags (`--api-key`, `--base-url`, `--timeout`) before the subcommand. Output options may follow the nested command. Errors/warnings go to stderr.

## Write safely

Resolve required IDs from API results. For long document/comment bodies, use files:

```bash
outline-cli documents create --title "Title" --collection-id "collection-id" --text-file ./doc.md
outline-cli documents update --id "document-id" --text-file ./doc.md
outline-cli comments create --document-id "document-id" --data-file ./comment.md
```

Do not publish or share unless requested. Confirm ambiguous destructive actions. Never expose credentials. Report useful IDs/URLs and the result, not the whole response. Live write tests belong in an empty test collection.

## Load references only when needed

- Command/option lookup or sharing: [commands.md](references/commands.md). Read the sharing guidance before membership changes; use `outline-cli <command> <subcommand> --help` for exact flags.
- Local Markdown with images/assets: [publishing.md](references/publishing.md); use `create-from-file --dry-run` before uploading.
- Comments/replies: [commands.md](references/commands.md#comments--attachments). Comments have a smaller schema and one reply level; use the root parent ID for replies to replies.
- Missing CLI/key, invalid credentials, or setup help: [setup.md](references/setup.md).
- API/permission/connection failure: [troubleshooting.md](references/troubleshooting.md). Follow the CLI's specific hint first; do not mistake a resource 404 for missing credentials.
