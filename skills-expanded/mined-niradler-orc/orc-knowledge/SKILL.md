---
name: orc-knowledge
description: Use to search or cite ORC knowledge bases, write or edit KB documents, comment for a KB's digest, or set up a digest that keeps a KB current. Trigger on "search the docs", "cite the runbook", "add this to the learnings", "set up a digest".
allowed-tools: mcp__orc__kb_list mcp__orc__kb_search mcp__orc__kb_evidence mcp__orc__kb_read mcp__orc__kb_documents mcp__orc__kb_write mcp__orc__kb_document mcp__orc__kb_comment mcp__orc__kb_maintenance mcp__orc__kb_manage mcp__orc__kb_digest
---

# ORC Knowledge Workflow

A knowledge base (KB) is a set of documents that belongs to a project or is global. Documents are uploaded files (PDF, Word, PowerPoint, Excel, HTML, CSV, Markdown, text), Markdown written by people or agents, or copies of files from a registered folder. ORC never writes the folder; a copy follows its file until someone edits it in ORC. Search combines exact title/path matches, full-text and, when embeddings are configured, vectors.

Any KB can have a **digest**: an agent that runs the KB's own instructions on a schedule and keeps it current. Each active project starts with a **Learnings** KB whose digest turns memories, session summaries and comments into lessons, procedures and decisions.

| Knowledge bases                          | Memory                                   |
| ---------------------------------------- | ---------------------------------------- |
| Documents: reference material, lessons   | Short facts an agent discovered          |
| `kb_search` / `kb_evidence` / `kb_read`  | `memory_list` / `memory_read`            |
| Changed by people, agents and the digest | `memory_create` / `memory_update`        |

Every read is counted per document and per source (mcp, api, cli, ui), so pass `session_id` when you have one.

## Find and cite

```
kb_search({ query, project?, scope?, kb_ids?, labels?, mode?, limit? })   // passages + kb:<doc>@<rev>#<n>
kb_evidence({ query, token_budget? })                                     // answer-ready cited pack
kb_read({ citation: "kb:01J...@3#4" })                                    // one passage
kb_read({ id, heading: "Rollback" })                                      // one section
kb_read({ id, start_line: 40, end_line: 80 })                             // numbered lines
kb_read({ id })                                                           // whole document, can be long
kb_list({ project? })                       // KBs, document counts, "editable" or "read-only" for you
kb_documents({ kb_id, folder?, label? })    // documents with path, labels, revision, reads
```

By default search covers the project's KBs plus global ones; `scope: "all"` searches every project. Cite `kb:` handles in answers. Passages from agent-written summaries are flagged as derived, so don't count them as independent corroboration. A handle names a revision; if the document changed since, read it again by ID.

## Write and edit

Each KB lists the call sources that may change it (`editable_by`: ui, cli, api, mcp). Your MCP calls are source `mcp`; `kb_list` marks each KB editable or read-only for you. When a KB is read-only, leave a comment instead.

```
kb_write({ kb_id, title, content, path?, description?, labels?, note, derived_from? })    // new document
kb_write({ document_id, expected_revision, content, note })                               // full rewrite
kb_document({ action: "edit", id, expected_revision, note, edits: [
  { old: "exact text", new: "replacement" },              // exact text (add replace_all: true for every match)
  { start_line: 12, end_line: 14, new: "new lines" },     // whole lines; end_line = start_line - 1 inserts
]})
kb_document({ action: "update", id, expected_revision, title?, path?, description?, labels? })
kb_document({ action: "history" | "restore" | "delete", id, ... })
```

Edit long documents with `kb_document` edit: read numbered lines first, and all edits refer to the revision you read, so later edits never shift. Every write is a new revision recorded with your session. A stale `expected_revision` is a conflict: read again and redo the change. Never list the document you are rewriting in `derived_from`. `kb_maintenance({ kb_id })` lists stale derived documents, failed files and links to missing documents.

## Comments

Comments are how people and agents ask for a change: a correction, a source to digest, a lesson to record. The digest handles open comments first.

```
kb_comment({ action: "add", kb_id, document_id?, body })
kb_comment({ action: "list", kb_id, document_id?, status? })
kb_comment({ action: "resolve" | "dismiss", comment_id, reply })    // one reply: what was done, or why not
kb_comment({ action: "reopen", comment_id })
```

To get something into a KB you shouldn't edit directly (read-only, or it needs the digest's judgment), add a comment with the link or text and say what you want done.

## Set up a digest

1. Create the KB if needed: `kb_manage({ action: "create", name, description })` (`global: true` for every project).
2. Start from the template: `kb_digest({ action: "template" })`, then adapt it to what this KB should hold.
3. Save it: `kb_digest({ action: "set", kb_id, instructions, backend: "codex" | "claude" | ..., schedule: { type: "cron", cron: "0 3 * * *" } | { type: "manual" } })`. This creates the digest's ORC job.
4. `kb_digest({ action: "run", kb_id })` starts a run now; `runs` shows history; `get` shows settings and the last run.

Scheduled runs are skipped when nothing new happened since the last completed run (no open comments, memories, sessions or audit entries). Manual runs always run. Each run ends with `digest_complete`; a run without it counts as failed and the next run repeats the work.

## CLI equivalents

```bash
orc kb list
orc kb search "rollback procedure"
orc kb evidence "how do we rotate the signing key"
orc kb get kb:01J...@3#4
orc kb add Runbooks ./docs/*.pdf
orc kb sources add Runbooks ./handbook
orc kb comment add Learnings "Digest https://example.com/postmortem"
orc kb comment list Learnings
orc kb digest template
orc kb digest set Learnings --backend codex --cron "0 3 * * *"
orc kb digest run Learnings
orc kb editable-by Runbooks ui,cli,api
```

## Common mistakes

| Mistake                                        | Fix                                                        |
| ---------------------------------------------- | ---------------------------------------------------------- |
| Reading whole documents first                  | Search, then read a citation, heading or line range        |
| Answering without handles                      | Use `kb_evidence` and cite `kb:` handles                   |
| Rewriting a long document for a small change   | `kb_document` edit with exact text or line ranges          |
| Writing to a read-only KB some other way       | Add a comment for its digest                               |
| Retrying a write after a conflict as-is        | Read the current revision and reapply your change          |
| Closing a comment without saying what happened | Resolve or dismiss with a reply                            |

## Related

- **orc-memory**: short facts and discoveries
- **orc-session**: session start and end
