---
name: technical-analysis-workflow
category: architecture
description: Use when you start an analiz task - explore every affected repository and resolve unknowns before writing the report
source: obra/superpowers (MIT), adapted
---
# Technical Analysis Workflow

## Overview

Turn an analiz task into a fully-formed technical understanding through investigation, not guessing. The analysis report you write later — one HTML document whose sections are the spec and the plan (analiz-html-report) — is only as good as this grounding.

**Hard gate:** Do NOT write the report, or any implementation task, until you have explored the actual repository and resolved the ambiguities below. This applies to EVERY analiz task regardless of perceived simplicity — "simple" requests are where unexamined assumptions cause the most wasted developer work.

## The Process

### 1. Clone and explore EVERY relevant repository first
- The analiz task's description lists the projects/repositories the PM believes are involved. Clone/pull ALL of them into your task workspace and review each — a cross-project feature is only understood when every affected repo is read.
- **Project model first, before diving into code.** `get_project_brief(repository_id)` — stack, components, commands, conventions, reference docs. `list_links(repository_id)` — who calls what, including other repositories, so you can trace a contract to its consumers. `list_component_checks` — the commands the plan's verify steps will use, instead of inventing one. `get_environment` / `list_runtime_errors` when the request is about production behaviour.
- **`codebase_search`, `grep_code`, `expand_symbol_context`, `get_symbol_skeleton` and `read_file` only cover the repository already in your workspace** — they do not reach into a repository you have not cloned. **Do not trust the PM's list as complete, and do not assume the tools will surface a repo you didn't open.** To check for an affected repo the PM missed: `list_repositories` for the remote/root of each candidate, `run_terminal` `git clone --depth 1 <remote_url or root_path> _analysis/<name>` inside your workspace (an analiz run never publishes a branch, so this is safe), then point `grep_code`/`read_file` at `path: "_analysis/<name>"` and call `get_project_brief`/`list_links` with that repository's id. If you find an affected repo this way, include it in the analysis and note it in your review summary.
- Explore before proposing anything: codebase_search for concepts, grep_code for exact symbols, get_repo_tree for structure, expand_symbol_context for focused reads.
- **Read the repo's own rules**: `CLAUDE.md`, `AGENTS.md`, `CONTRIBUTING.md`, `docs/adr`/`docs/decisions`, lint configs. Their constraints go verbatim into the plan's Global Constraints block (implementation-plan-authoring).
- **Name the analog.** State the closest existing feature (file:line) the new work follows. "No analog" must be said explicitly — it is a signal to take the heavier approach in step 4.
- **Check third-party APIs against the locked version.** Find the dependency's version in `go.mod`/`package.json`/`pubspec.lock`, then `fetch_url` the official docs for THAT version (or `web_search` to find them) before naming a function in the design. A call you did not see in the repo or in the docs for the locked version does not go in the plan.
- Read existing docs and recent commits. Follow existing patterns — never invent a parallel convention.
- **No commits.** You are analysing, not implementing — never commit to any repo. Your entire output is the analysis report attached to the analiz task via add_task_document (`format: "html"`), plus a summary add_task_comment.
- **Keep what you read.** Note each file path and symbol as you read it — the report's `context` section is a table of exactly these, and a path you did not see in this run has no place in it.

### 2. Understand the intent
- Restate the request in your own words: what outcome is wanted, for whom, and why. Write it in the report's `summary` as two lines — "Asked" (what the task literally says) separate from "Assumed" (what you inferred) — so a reviewer can tell your inference from the human's instruction.
- Assess scope early: if the request describes multiple independent subsystems, decompose it into sub-analyses first — what are the independent pieces, how do they relate, in what order should they be built? Don't refine details of a project that needs splitting.
- Focus questions on: purpose, constraints, success criteria.
- **Scale the analysis** to the question, and when unsure, take the heavier path:
  - **Spike** ("can we / is it possible…"): `summary`, `context`, a findings-and-recommendation subsection, `risks`; `plan` and `split` are omitted or say "none".
  - **Bounded** (a clear, contained change): all sections, kept short.
  - **Architectural** (new integration, no analog, cross-repo, a schema or contract change): all sections, full depth, decision record (spec-authoring) and migration-and-contract-review where they apply.

### 3. Identify WHAT and WHERE
- Name the units of work, their interfaces, and the exact files/areas each change touches.
- Design for isolation: each unit has one clear purpose, communicates through well-defined interfaces, and can be understood and tested independently. For each unit answer: what does it do, how is it used, what does it depend on?
- If you can't change a unit's internals without breaking its consumers, the boundary is wrong — fix the boundary in the design.

### 4. Propose approaches
- Propose 2–3 approaches with trade-offs; lead with your recommendation and the reasoning.
- YAGNI ruthlessly: strip anything the acceptance criteria don't require.
- Pick one approach and state every ambiguous point explicitly — a requirement readable two ways becomes a defect.

### 5. Resolve unknowns
- Resolve technical unknowns from the code, never by assuming.
- Only genuine PRODUCT decisions escalate — record them with `record_open_questions`, never in the report's text and never with `ask_user` (you have no `ask_user` tool here). Default to non-blocking: a reasonable answer exists, so record it as `recommended_answer` and keep going. Mark one blocking only when proceeding on any guess would waste the implementation (open-questions-protocol has the worked examples). Never block on a question the codebase can answer.

## Output

This grounding feeds directly into the report: its `context` section (what exists, with real paths), then spec-authoring for the `design` section and implementation-plan-authoring for the `plan` section, all in the one document analiz-html-report describes. If you cannot yet name the files to touch and the interfaces between units, the analysis is not done.

## Worked Example

Analiz: "Users can export a project's tasks to CSV." PM named the `backend-api` repo.

1. Clone `backend-api`. `get_project_brief` + `list_links` first. `codebase_search "task list endpoint"` → find `TaskHandler` + `TaskRepository.ListByProject` already exist → the export reuses them.
2. Cross-check: `list_repositories` shows a `web` repo (NOT named by the PM) linked to `backend-api`. `run_terminal git clone --depth 1 <web's root_path> _analysis/web`, then `grep_code "api/v1/projects" path:"_analysis/web"` → the board page will need a download button. Add `web` to the split. This is the PM-missed repo the cross-repo check surfaces — `codebase_search`/`grep_code` alone would not have found it, since they only cover the cloned, in-workspace `backend-api`.
3. WHAT/WHERE: new `TaskExporter` service (backend) consuming `ListByProject`; new `GET /projects/:id/tasks/export`; a web button calling it.
4. Approaches: (a) stream CSV from the handler, (b) build in a service and return bytes. Pick (b) — testable without HTTP. State it. Analog: the existing `/projects/:id/report` endpoint follows the same handler→service→repo shape (`internal/adapter/http/report_handler.go:40`) — bounded, not architectural.
5. Unknowns resolved from code (column order = the DTO fields). No stakeholder question needed.

Now the files and interfaces are named → analysis is done, the report can be written.

## Red Flags

- "This is too simple to need analysis" — the design can be short, but it must exist.
- Proposing an approach before reading the relevant code.
- A spec section that says "TBD" or could be read two ways.
- Escalating a question you could answer with grep.
