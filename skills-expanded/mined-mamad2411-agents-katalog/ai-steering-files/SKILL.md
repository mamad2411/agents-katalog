---
name: ai-steering-files
description: Use when creating, auditing, or updating AI steering files such as AGENTS.md, CLAUDE.md, GEMINI.md, .github/copilot-instructions.md, .cursor/rules/*.mdc, PRODUCT.md, TECH.md, STRUCTURE.md, VISION.md, or DESIGN.md in a software repository.
---

# AI Steering Files

## Overview

AI steering files are repo-local context documents that teach coding agents how to work in a project. Add the smallest file that removes recurring ambiguity, then keep it concrete enough that an agent can act on it without guessing.

## When to Use

Use this skill when:

- adding or revising repo instructions for AI coding agents
- choosing between `AGENTS.md`, tool-specific instruction files, and product or technical context files
- auditing whether a repo gives agents enough commands, constraints, and examples
- introducing a new agent tool that needs its own memory, syntax, or scope rules

Do not use it for one-off chat instructions, temporary implementation notes, or generic advice that is not grounded in the repository.

## Workflow

1. Inventory existing steering files before creating a new one. Read any `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `.github/copilot-instructions.md`, `.cursor/rules/*.mdc`, `PRODUCT.md`, `TECH.md`, `STRUCTURE.md`, `VISION.md`, and `DESIGN.md` already present.
2. Pick the narrowest durable home for the instruction. Repo-wide, vendor-neutral rules belong in `AGENTS.md`; tool-specific rules belong in that tool's file; path-scoped rules belong in a path-scoped rule file.
3. Write concrete repo facts: exact commands, exact paths, reliable examples, known constraints, and review expectations.
4. Prefer links and short summaries over duplicating long third-party documentation.
5. Remove stale or duplicated guidance while editing. Conflicting files make agents choose randomly.
6. Verify the commands or paths you mention. If a command cannot be run locally, say why in the file.

## File Chooser

| File | Use when | Should contain |
| --- | --- | --- |
| `AGENTS.md` | Rules should apply to any coding agent in the repo. | Project summary, workflow, exact install/test/build commands, branch policy, review expectations, risky actions requiring approval. |
| `PRODUCT.md` | Implementation choices need product context. | Users, problem, core workflows, business goals, success criteria, in-scope and out-of-scope boundaries. |
| `TECH.md` | Agents need stack and integration constraints. | Frameworks, runtimes, preferred libraries, external services, deployment targets, supported commands. |
| `STRUCTURE.md` | Agents keep putting files in the wrong place. | Directory map, ownership boundaries, import rules, naming conventions, placement rules. |
| `VISION.md` | Long-term direction should outlive individual specs. | Durable product vision, non-goals, taste direction, what should not drift, outcome-level success criteria. |
| `DESIGN.md` | Agents generate UI and need design-system guidance. | Tokens, typography, spacing, layout constraints, component patterns, accessibility rules, visual anti-patterns. |
| `CLAUDE.md` | Claude Code needs persistent tool-specific guidance. | Claude-specific workflow notes, build/test expectations, escalation boundaries, paths Claude should treat specially. |
| `GEMINI.md` | Gemini CLI needs persistent tool-specific guidance. | Gemini-specific project context, conventions, commands, and file priorities. |
| `.github/copilot-instructions.md` | GitHub Copilot needs repository-wide instructions. | Build/test commands, coding standards, constraints, review guidance, links to canonical examples. |
| `.cursor/rules/*.mdc` | Cursor rules should apply only to certain files or workflows. | Scope, globs, conventions for that scope, examples, auto-apply vs manual behavior. |

## Quality Bar

Good steering files:

- say what the file controls and who should read it
- include commands an agent can run, not vague preferences
- point to examples already in the repo
- name constraints that matter for safety, data, performance, accessibility, product, and deployment
- stay short enough to be reread during real work

## Common Mistakes

| Mistake | Fix |
| --- | --- |
| Adding every preference to every file. | Put shared rules in `AGENTS.md`, then let tool-specific files only add differences. |
| Writing generic agent advice. | Replace it with project-specific paths, commands, and examples. |
| Copying long external docs. | Summarize the local implication and link to the primary source. |
| Creating a new file for temporary work. | Keep temporary notes in the task, issue, or plan; steering files are durable. |
| Leaving conflicts between files. | Make one file canonical and have the others reference it. |

## Final Check

Before finishing, confirm:

- the chosen file matches the scope of the guidance
- file names and paths are exact, including capitalization
- install, test, lint, build, and deploy commands are current
- examples and links resolve
- the result explains when the file is worth adding, not just what it is
