---
name: nextstage-harness
description: (NS) Harness discovery, artifact layout, and SDD planning gates for NextStage skills. Installed automatically as a dependency — use when resolving AGENTS.md, .nextstage-harness/rules, docs/versions paths, or confirmation gates.
---

# NextStage Harness

Shared reference documents for NextStage skills. Consumer skills point here for path resolution and planning gates — workflow logic stays in those skills.

## References

| File                              | When to read                                                                      |
| --------------------------------- | --------------------------------------------------------------------------------- |
| `references/harness-discovery.md` | Resolving `{product_root}`, `{harness_root}`, rules paths, or MCP GitLab pointers |
| `references/rules-sync.md`        | Canonical rules layout, manifest schema, `harness sync`                           |
| `references/artifact-layout.md`   | SDD artifact paths under `docs/versions/`, living specs, handoff rules            |
| `references/gates.md`             | Human confirmation gates before requirements, scope, or task generation           |

Read only the file(s) the active consumer skill names. Do not assume monorepo layout or stack unless discovery resolves it.
