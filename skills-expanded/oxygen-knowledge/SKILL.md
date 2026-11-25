---
name: oxygen-knowledge
description: Read and maintain OXYGEN Knowledge pages, sources, revisions and approved context so GTM functions use traceable company knowledge.
---

# Give the functions durable context

Read [the runtime contract](../../../docs/runtime-contract.md). The kit's `company/` examples and `context/` pages are local authoring inputs. When context is promoted to OXYGEN, record which hosted pages and revisions the motion uses; do not silently maintain competing copies.

```sh
oxygen capabilities search "workspace knowledge ICP and offer" --json
oxygen commands get "knowledge index" --json
oxygen commands get "knowledge search" --json
```

Read the index first, search the concept, then open the relevant pages and their sources. Reuse stable slugs instead of making near-duplicate pages. Follow useful wikilinks/backlinks and cite the slugs/revisions used. Similarity rank is not confidence; inspect semantic availability and lexical fallback when returned.

Sources preserve evidence; pages synthesize it. File durable findings into the closest page with source dates, boundaries and an append-only log entry. Treat model summaries and the demo's synthetic data as such. Use proposals for changes to canonical offer, voice, positioning or pinned playbooks, and follow existing authorized decisions.

Inspect current folder/upsert schemas before creating or moving pages; retain placement unless changing it is intended. Lint structural changes and read back the actual revision and web_url.

A Knowledge sync is a disposable local mirror: sync before editing, push deliberate changes and resolve conflicts. A repository mount is a separate source connection. Discover its current schema and access scope if the user wants to mount their GitHub/Obsidian workspace; cloning this kit does not connect it.

For a scoring/copy run, map the intended evidence/rubric into the callable inputs as described in [composition](../../../docs/composition.md). The presence of a local file or hosted page does not prove that the caller bound its content.
