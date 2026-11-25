---
name: agents-md-housekeeping
description: "Maintain accurate, complete, retrieval-led AGENTS.md files and audit all tracked project AGENTS.md files."
compatibility: "Requires Git and a repository that uses AGENTS.md files."
metadata:
  source: "https://vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals"
---

# AGENTS.md Housekeeping

Use this skill when the user invokes it or when a task edits an `AGENTS.md`
file. Do not use it only because another repository change can affect an
instruction file.

## Principles

- Keep `AGENTS.md` files compact, factual, complete, and useful during active work.
- Put repository-wide rules and a compact route map in the root file.
- Put subtree-specific rules in the nearest useful child file.
- Create a child file only when the subtree has distinct rules or references.
- Use exact relative paths and give each important path a short purpose.
- Tell agents to read source files and detailed documents before they decide.
- Use canonical sources to prove each instruction. Do not use general knowledge as evidence.
- Treat the constitution, accepted ADRs, API contracts, and `ARCHITECTURE.md` as canonical when they govern the changed area.
- Read the current feature specification, plan, and tasks when they govern the changed area.
- Read related project guides, configurations, runbooks, tests, and source code when they support a local instruction.
- Keep detailed procedures in their canonical documents. Link to them instead.
- Keep each relevant canonical source reachable from the nearest useful `AGENTS.md`.
- Do not repeat a parent rule unless the child changes its scope.
- Preserve a useful route, rule, command, table, glossary entry, ADR index entry, or code block unless evidence shows it is obsolete.
- Remove instructions that no longer describe the repository.
- Write added or changed `AGENTS.md` text in Simplified Technical English.

## Procedure

1. List the project-owned instruction files:

   ```bash
   git ls-files -- ':(glob)**/AGENTS.md' | sort
   ```

2. Build an evidence set for each affected `AGENTS.md` file. Read its local source and each relevant canonical source:
   - Repository rules: `ARCHITECTURE.md`, `.specify/memory/constitution.md`, and accepted ADRs.
   - API behavior: the relevant OpenAPI contract.
   - Feature behavior: the current `spec.md`, `plan.md`, and `tasks.md`.
   - Local behavior: source code, configuration, tests, maintained guides, and runbooks.
   - Adjacent documents that the instruction file already routes to.

   Do not read unrelated documents only because they exist. Read enough evidence to prove each retained, changed, or removed instruction.

3. Identify facts that changed or required guidance that is missing:

4. Update the file that owns each fact:

   | Fact | File |
   | --- | --- |
   | Repository-wide rule | Root `AGENTS.md` |
   | Subtree-specific rule | That subtree's `AGENTS.md` |
   | Detailed design or procedure | Its canonical document, linked from `AGENTS.md` |

5. If a new child `AGENTS.md` file is needed, add a route from its nearest
   parent. The root file must route to every important project area.

6. Make sure that each changed instruction:
   - Its facts match the canonical source.
   - Its paths, links, and commands exist.
   - Its source routes cover the relevant architecture, principles, ADRs, contracts, specifications, and local guides.
   - It adds local guidance instead of copying parent guidance.
   - It links to detail instead of duplicating it.
   - It preserves required rules, indexes, glossary entries, tables, commands, and code blocks unless they are obsolete.
   - It does not describe generated or dependency files.

7. Review the final diff. Make sure that each deletion has evidence. If no instruction needs a change, make no edit.
