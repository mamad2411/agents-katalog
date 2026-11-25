---
name: oxygen-knowledge
description: Operate OXYGEN Knowledge: index-first retrieval, wiki pages and folders, citations, revisions and sources, proposals for canonical copy, workspace skills and a local mirror. Use for company and ICP context, offers, voice, rubrics and learnings.
---

# Give the engine durable context

Read [the runtime contract](../../../docs/runtime-contract.md). The kit's `company/` examples and `context/` pages are local authoring inputs. When context is promoted to OXYGEN, record which hosted pages and revisions the motion uses; do not maintain competing copies.

## Index first

1. Read `oxygen knowledge index --json` before searching or inventing a slug.
2. Search and open relevant pages; follow wikilinks and backlinks.
3. Cite the slugs and revisions used.
4. File durable findings into the closest existing page.

Reads cost 0 credits. `knowledge page get <slug> --view full` returns content, links and sources together.

## Pages, folders and skills

- Folders: `knowledge folders list`, `create --name "..."`, `move`. Pages: `knowledge page upsert --title "..." --folder <id> --create-only`.
- Fit rubrics live well as pages: a Classify column or a Function can quote them, and changing the page changes the rule in one place.
- Demo or example pages should be clearly labelled (a draft status and a `demo` tag) so the workspace's own agents do not treat them as its real ICP.
- Workspace skills hold private reusable guidance: `oxygen skills workspace create` or `import --directory ./skill`. They grant no tool, spend or approval authority.

## Write boundary

Working research and learnings can be filed as logged revisions. Canonical voice, brand, positioning, offer and pinned playbook changes go through proposals and approval; never silently overwrite live copy. Hosted Knowledge is authoritative; `knowledge sync` makes a disposable local mirror.
