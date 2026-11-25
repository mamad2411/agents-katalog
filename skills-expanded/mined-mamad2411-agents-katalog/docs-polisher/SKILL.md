---
name: docs-polisher
description: "Use to plan or implement documentation polish: docs information architecture, README/docs/wiki structure, navigation, links, duplication, stale/noisy content, source-backed claims, references, and diagrams. Use when the user asks to polish, reorganize, audit, clean up, plan, or improve documentation readability and structure."
---

# Docs Polisher

## Job

Plan or implement a documentation polish pass that makes docs easier to navigate, source-backed, low-noise, visually clean, and grouped by reader task, resource, topic, or domain.

Use an OKF-inspired knowledge model for docs, references, folder structure, knowledge catalogs, agent-readable navigation, or explicit OKF requests: concept-sized pages, directory indexes, explicit cross-links, citations for drift-prone claims, and optional lifecycle logs.

## Modes

- Plan-only: use when the user asks what to do, asks for an audit, or does not provide write scope.
- Write-polish: use when the user asks to make documentation changes and provides or implies safe docs write scope.

Default to plan-only for moves, renames, deletions, broad rewrites, or unclear scope. Implement directly only for approved documentation files.

## Reuse Local Skills

- Use $docs for writing, restructuring, README/wiki pages, runbooks, references, Markdown details, and docs validation.
- Use $audit with docs mode for read-only coverage, correctness, freshness, navigation, diagrams, links, and source-backed quality checks.
- Use $discover when repo, docs-set, or system understanding is needed before rewriting docs.
- Use $diagrams when choosing, drafting, validating, or improving source-backed diagrams.
- Use $domain-modeling when terminology, CONTEXT.md, glossary, context maps, or ADR candidates are in scope.
- Use $codebase-design when architecture docs need module, interface, seam, ownership, runtime, or technical-boundary vocabulary.
- Use $ast-grep only when structural search helps update doc references or source-backed links.
- Do not use $commit unless the user explicitly asks for commits.
- Do not use implementation skills unless the task changes from documentation polish to code work.

Alias mapping:

- documentation -> $docs
- documentation-audit -> $audit with docs mode
- project-discovery -> $discover
- architecture -> $diagrams, $docs, or $codebase-design depending on the artifact
- project-context -> $domain-modeling when durable terminology is in scope

## Workflow

1. Resolve scope, mode, write boundaries, non-goals, and target reader.
2. Inspect repo guidance, README files, docs folders, wiki folders, ADRs, runbooks, diagrams, navigation files, links, and assets.
3. Classify pages by purpose: landing, tutorial, how-to, reference, explanation, concept, task, troubleshooting, ADR, runbook, stale candidate, or duplicate candidate.
4. Build a current docs map and identify canonical sources of truth.
5. Check whether OKF-inspired structure would help: concept boundaries, directory `index.md`, optional `log.md`, useful cross-links, and citations.
6. Choose the smallest target docs map that improves navigation and grouping.
7. Plan or perform edits:
   - put high-signal summaries at page tops;
   - put quick paths and common tasks before details;
   - move stable facts into tables or reference sections;
   - merge duplicates into canonical pages and replace repeated content with links;
   - remove or move stale, irrelevant, noisy, or unverifiable content;
   - mark unknowns with verification paths.
8. Handle diagrams deliberately:
   - keep large overview diagrams when they orient the reader;
   - dissect large diagrams into smaller focused diagrams when they are dense;
   - add or update architecture, cloud/topology, system interaction, use-case, sequence, data/state, and trust-boundary views when they reduce cognitive load;
   - keep every diagram source-backed, labeled, directed, captioned, and readable.
9. Validate links, Markdown, diagrams, and docs build as practical.
10. Report changes, checks, skipped checks, risks, and recommended next pass.

Read `references/polish-model.md` before broad docs audits, broad reorganizations, diagram-heavy work, or link/duplication sweeps.
Read `../../references/okf/okf.md` when the work involves OKF, knowledge catalogs, references, folder structure, agent-facing docs, or durable docs navigation.

## Write Scope

Typical allowed paths only when user-approved:

- `README.md`
- `docs/**`
- `wiki/**`
- `.wiki/**`
- `adr/**`
- `docs/adr/**`
- `CONTEXT.md`
- `CONTEXT-MAP.md`
- `CHANGELOG.md` only if explicitly requested
- `.order` files only when wiki navigation is in scope

## Guardrails

- Do not edit source code, tests, production config, infrastructure, pipelines, secrets, generated files, lockfiles, or build outputs unless explicitly approved.
- Do not stage, commit, push, publish, deploy, upload, sync to a wiki, edit trackers, or mutate external systems.
- Do not delete docs without preserving, moving, or summarizing useful content unless deletion is explicitly approved.
- Do not expose secrets, tokens, keys, passwords, connection strings, private hostnames, private URLs, or sensitive operational values.
- Do not rewrite correct concise docs into long prose.
- Do not create a large documentation framework when a small docs tree is enough.
- Do not duplicate canonical source files. Link to the source of truth instead.
- Do not make decorative diagrams that are not useful.
- Do not invent ownership, architecture, process, APIs, deployment, commands, business facts, or operational behavior.

## Output

- Scope and mode.
- Skills used.
- Sources inspected.
- Current docs map.
- Target docs map or implemented structure.
- File tree and page structure changes.
- OKF-inspired concept, index, log, citation, or cross-link changes when applicable.
- Links fixed or flagged.
- Duplicate, repeated, noisy, stale, or irrelevant content handled.
- Aggregation changes by resource, topic, or domain.
- Diagrams added, updated, decomposed, verified, or flagged.
- References improved.
- Source-backed claims and unknowns.
- Files changed.
- Checks run and skipped.
- Risks and next recommended pass.
