---
name: make-documentation
description: "Use when writing READMEs, architecture, changelogs, release notes, runbooks, notebook docs, install docs, or security articles; produces docs. Do not trigger for API docs, AGENTS.md, or diagrams."
metadata:
  short-description: Write project documentation.
---

# Make Documentation


## When to Use

- Writing or updating a README.md, architecture note, changelog, or release notes
- Auditing existing project docs before adding missing documentation
- Drafting customer-facing security guidance or partner-sensitive article prose from source material
- Writing live access, reproduction, lab interface, workstation/server, or operator runbooks
- Documenting notebooks, generated notebooks, or table-producing notebook workflows
- Writing WSL, local, Docker, or environment-specific install docs
- Writing agent operation manuals, role files, peer-status contracts, or AI-readable workflow docs
- Producing diagram documents only when the user explicitly asks or the project already uses them

## When NOT to Use

- Writing API reference documentation
- Creating or updating AGENTS.md. Use `agents-md`, even when the broader request also includes other docs.
- Generating diagram files by default when prose or tables are sufficient

## Workflow

1. Run [scripts/audit_documentation.py](scripts/audit_documentation.py) for new docs, large rewrites, doc moves, missing-doc investigations, or unclear structure. For tiny explicit edits, inspect the target file and nearby docs directly.
2. Choose only the deliverables justified by the user's request and the audit. Do not generate a fixed documentation bundle by default.
3. Route by document type: use [references/guide-readme.md](references/guide-readme.md) for `README.md`, [references/guide-architecture.md](references/guide-architecture.md) for `docs/architecture.md` or the repo's existing equivalent, [references/guide-ai-ingestion.md](references/guide-ai-ingestion.md) when the user says the document is for agents/AI ingestion, [references/guide-agent-ops-docs.md](references/guide-agent-ops-docs.md) for role/workflow docs consumed by agents, [references/guide-access-runbook.md](references/guide-access-runbook.md) for live access, reproduction, operator, lab interface, or capability ledgers, [references/guide-notebook-documentation.md](references/guide-notebook-documentation.md) for notebook explanations, [references/guide-install-runbook.md](references/guide-install-runbook.md) for WSL/local/Docker install docs, [references/guide-security-article.md](references/guide-security-article.md) for partner-sensitive security articles, and [references/guide-changelog.md](references/guide-changelog.md) for `CHANGELOG.md` or release notes. If AGENTS.md becomes part of scope, switch that file to `agents-md` instead of expanding this skill.
4. Use [references/guide-diagrams.md](references/guide-diagrams.md) only when the user explicitly asks for diagram docs or the project already maintains them.
5. For large docs, iterative reports, feature inventories, concept framing, or evidence-audit amendments, load [references/source-discovery-and-heading-stability.md](references/source-discovery-and-heading-stability.md) before writing.
6. For concept or strategy docs, include a visible first usable workflow before architecture depth so the reader can execute a small slice before absorbing the model.
7. Keep the output source-backed and terse. Preserve user-provided terminology and avoid generic rewrites that change domain meaning or connotation.
8. Preserve earlier requested documentation when later implementation work touches the same notebooks, docs, or folders. Re-open touched docs before finishing if there is a risk an unrelated implementation change removed prior documentation.
9. Review the result with [references/review-checklist.md](references/review-checklist.md) before finishing.

## Anti-Patterns

- Wrong: summarize a notebook from a generated README, review packet, AI commentary, or stale comments. Correct: trace executable cells, imports, widgets, SQL, configs, and outputs, then write the short explanation.
- Wrong: write folder-contract docs after a move from memory. Correct: audit the tree and update parent and child docs together.
- Wrong: duplicate validators, schemas, CLIs, table lists, or source-of-truth modules while documenting around implementation. Correct: scan for existing source-of-truth assets and link to them.
- Wrong: leave workflow docs tied to VS Code, one editor, or one UI unless the user explicitly requested that. Correct: state editor-independent start state and execution plane.
- Wrong: keep meta labels such as `review packet`, `AI-generated summary`, or `analysis artifact` in human-facing docs unless they are required schema fields. Correct: use natural section names that match the audience.
- Wrong: label demo-only flags or filters as future product interfaces. Correct: separate test scaffolding from durable user or agent interfaces.

## Deterministic Tools

| Tool | Use When | Outcome |
|------|----------|---------|
| [scripts/audit_documentation.py](scripts/audit_documentation.py) | You need a deterministic inventory before writing docs | Current-state documentation audit |

## References

- [references/guide-readme.md](references/guide-readme.md) - README workflow
- [references/guide-architecture.md](references/guide-architecture.md) - architecture documentation
- [references/guide-ai-ingestion.md](references/guide-ai-ingestion.md) - compact machine-ingestion documentation mode
- [references/guide-agent-ops-docs.md](references/guide-agent-ops-docs.md) - role, directive, peer-status, and execution-plane docs for agents
- [references/guide-access-runbook.md](references/guide-access-runbook.md) - live access, reproduction, interface, and capability ledgers
- [references/guide-notebook-documentation.md](references/guide-notebook-documentation.md) - notebook explanation and runnable-order preservation
- [references/guide-install-runbook.md](references/guide-install-runbook.md) - environment-specific install docs
- [references/guide-security-article.md](references/guide-security-article.md) - partner-sensitive security article workflow
- [references/guide-changelog.md](references/guide-changelog.md) - changelog and release notes
- [references/guide-diagrams.md](references/guide-diagrams.md) - opt-in diagram workflow only
- [references/review-checklist.md](references/review-checklist.md) - review pass before finishing
- [references/source-discovery-and-heading-stability.md](references/source-discovery-and-heading-stability.md) - large-doc source discovery and stable heading checks
- [references/ascii-art-standards.md](references/ascii-art-standards.md) - diagram formatting standards when diagrams are in scope
