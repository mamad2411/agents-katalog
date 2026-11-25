---
name: clio-mcp
description: Use when the task needs Clio memory: store, retrieve, update, persona, tasks, graph, or maintenance. DO NOT TRIGGER on a greenfield turn that needs no prior state.
---

# Clio MCP

Read the one row below that matches the task. Then open only that reference file.

| Group | When you need | Read |
|---|---|---|
| retrieval | Find memory or build grounded context. | `references/01-retrieval.md` |
| item-write | Create, correct or remove memory items. | `references/02-item-write.md` |
| item-read | Read, inspect or summarize stored items. | `references/03-item-read.md` |
| persona | Read or record stable preferences. | `references/04-persona.md` |
| task | Record task state and failure history. | `references/05-task.md` |
| memtree | Read hierarchical or temporal memory. | `references/06-memtree.md` |
| triple | Record or query factual triples. | `references/07-triple.md` |
| belief | Record or inspect beliefs. | `references/08-belief.md` |
| graph | Read or add memory relationships. | `references/09-graph.md` |
| hygiene | Inspect or clean memory hygiene. | `references/10-hygiene.md` |
| portability | Move or review memory exports and imports. | `references/11-portability.md` |
| ops | Diagnose, verify or repair operations. | `references/12-ops.md` |
| retention | Read or set retention policy. | `references/13-retention.md` |
| config | Read or change configuration. | `references/14-config.md` |
| ranking | Read or change ranking settings. | `references/15-ranking.md` |
| sync | Exchange memory between peers. | `references/16-sync.md` |
| compliance | Track subject requests and erasure. | `references/17-compliance.md` |

## Call rules

- Read only the group reference file you need.
- Call `tool_describe(name)` for exact arguments.
- If the reference and `tool_describe` disagree, trust `tool_describe`.
- Call a listed tool directly; call a hidden tool with `tool_invoke`.
- If you cannot find the tool, call `tool_search`.
- Do not read every reference file as a discovery step.

## Turn budget

At most four `retrieve` and `compose_context` calls combined are allowed per turn. This budget does not cap any other tool.

## End-of-session check

At session end, run `clio version --check` once. Repeat its one result line word for word. Report a newer release when the line names one. Report the check as unavailable when the line names no release. Apply no update.
