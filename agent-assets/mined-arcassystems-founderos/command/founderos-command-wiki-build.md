---
description: Rebuild the wiki graph. Tool invocation (run /founder-os:wiki-build). Walks OS markdown, extracts [[wikilinks]], refreshes the wiki_links section in brain/relations.yaml. Read-only on source markdown.
allowed-tools: ["Bash", "Read"]
---

# Founder OS wiki-build

Refresh the auto-extracted half of `brain/relations.yaml`. The hand-curated `relations:` section (semantic edges with type: informs/blocks/guards_against/etc.) is preserved untouched. Only the block between the auto-generated sentinel markers is replaced.

## Procedure

1. If `core/identity.md` does not exist, reply `Founder OS not set up here. Say "set up Founder OS" first.` and stop.

2. If `scripts/wiki-build.py` does not exist, reply `Wiki-build script not found. Say "update Founder OS" to restore the OS's own files.` and stop.

3. Run the build script:
   ```bash
   python scripts/wiki-build.py
   ```

4. Report the output line verbatim. Example: `Wrote 12 wiki links from 4 source files into brain/relations.yaml`.

5. If the script exits non-zero, report the error message verbatim and stop. Do NOT attempt to fix the underlying issue automatically.

6. Do NOT save a version of the change yourself. The user reviews the refreshed graph first; with version history on, it rides along in their next save.

## Wikilink syntax (Obsidian-compatible)

| Form | Meaning |
|---|---|
| `[[target]]` | Bare slug. Resolved at query time. |
| `[[target.md]]` | Explicit file (basename or repo-relative path). |
| `[[target.md#anchor]]` | File with heading anchor. |
| `[[target\|display text]]` | Alias form. Display text is discarded for the graph. |

## Rules

- Read-only on source markdown. The script only writes to `brain/relations.yaml`.
- Wiki-layer scope: `core/`, `context/`, `cadence/`, `brain/`, `network/`, `companies/`, `roles/`, `rules/`. Plugin-internal directories (`.claude/`, `skills/`, `templates/`, `docs/`) and the source archive (`raw/`) are excluded.
- Wikilinks inside fenced code blocks or inline backtick spans are ignored (so docs that describe the syntax do not pollute the graph).
- The script is idempotent. Running twice in a row produces no diff.
- Do not edit the auto-generated block by hand. Edits between `#@@WIKI_LINKS_AUTOGEN_BEGIN@@` and `#@@WIKI_LINKS_AUTOGEN_END@@` are overwritten on next run. Add semantic edges to the hand-curated `relations:` section instead.

## When to run

- After any session that added 3+ wikilinks to your OS.
- Before `/founder-os:lint` if you want lint to see the freshest cross-reference graph.
- Manually when curiosity strikes ("what links to context/clients.md?").

Not on a cron. Auto-running on session start would add latency for marginal value. Manual is fine.

## Voice

- No em dashes or en dashes. Hyphens only.
- No commentary outside what the procedure says to output.

<!-- private-tag: not applicable: writes brain/relations.yaml from extracted wikilinks (structured graph data, not user-provided speech) -->
