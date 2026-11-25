---
name: docdriven-build
description: Use after docdriven-init to create the initial DocDriven documentation tree for a repository. Builds human, agent, knowledge, and tmp docs using the generated project-docdriven skill as the project contract.
---

# DocDriven Build

Use this skill to create and adapt the initial `Docs/` structure.

## Required Workflow

1. Read the repo-local `project-docdriven` skill if present.
2. Read `Docs/agent/init-scan.md` if present.
3. Inspect existing docs and code structure.
4. Create missing DocDriven folders, manifest, route shards, and canonical files.
5. Fill files with concise, current, non-placeholder content.
6. Document the adaptive architecture contract: current structure, boundaries,
   structural ownership, configuration flow, reuse/composition rules, and durable coding patterns.
7. Use `Docs/agent/manifest.json` as the machine route index.
8. Use `Docs/agent/context-map.md` as the readable route view.
9. Keep human docs short.
10. Keep knowledge docs canonical.
11. Keep tmp docs explicitly non-authoritative.

Generated placeholders are scaffolding only. Build is not complete until
placeholder text in human or knowledge docs is replaced or recorded as a gap.

## Dynamic Build

The generated tree is only a base scaffold. Adapt it to the repository before
calling the build complete.

- First classify the project: what kind of system it is, how large it is, how
  mature it is, where it appears to be going, and what risks future agents are
  likely to face.
- Keep the smallest useful docs surface.
- Remove or leave uncreated docs for concepts the project does not have.
- Create project-specific docs when humans or agents have distinct tasks.
- Split knowledge docs or route shards when it reduces context or clarifies ownership.
- Record uncertain docs, missing owners, and unresolved setup facts in `Docs/agent/gaps.md`.
- Do not turn the scaffold into a mandatory architecture.
- Make future agents follow project-specific style and structure instead of hardcoding generic preferences.
- Document where reusable components, helpers, hooks, adapters, and shared primitives live when the project has them.
- For large or fast-moving projects, prefer explicit route ownership,
  reproducible validation commands, and local maintenance entrypoints over
  generic guidance.
- Create or preserve a repo-local DocDriven audit entrypoint when possible,
  usually `scripts/audit-docdriven.mjs`, and document it in the project command
  docs. For Node projects, add or recommend a package script such as
  `docs:audit` that runs the local entrypoint.

## Generator

Prefer `scripts/create-docs-tree.mjs` for the base scaffold, then edit content
and structure manually to match the project.

## References

- Read `../_shared/docs-tree-template.md`.
- Read `../_shared/writing-style.md`.
- Read `../_shared/agent-operating-contract.md`.
