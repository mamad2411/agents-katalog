---
name: code-reading-and-change
description: Use when reading, explaining, debugging, reviewing, modifying, refactoring, testing, or validating source code, configuration, build failures, API behavior, repository structure, runtime errors, or implementation requests. Prefer this Skill when the task needs codebase orientation, evidence-backed diagnosis, scoped changes, tests, or risk reporting. Do not use for pure research, prose writing, data analysis, or frontend visual design unless code work is central.
meta:
  version: 1
  display_name: 代码阅读与修改
  source: jezweb/claude-skills dev-tools; anthropics/skills webapp-testing reviewed-not-bundled
  license: MIT
---

# Code Reading And Change

## Purpose

Handle code tasks by first understanding the live codebase, then making the smallest coherent change with validation evidence. The Skill owns code-reading process, owner/path discovery, diagnosis, change scoping, implementation discipline, tests, and residual-risk reporting.

This Skill adapts development workflow ideas from reviewed open-source Skills. Anthropic `webapp-testing` was reviewed as a high-star tool-bound reference but is not bundled or directly adapted. This Skill does not bundle helper scripts, Playwright automation, package commands, dev servers, or tool-specific instructions.

## Use When

Use for:

- reading, explaining, or tracing code behavior;
- diagnosing bugs, errors, failing tests, build failures, runtime issues, regressions, or unexpected behavior;
- implementing a requested code or config change;
- refactoring when behavior and ownership are clear;
- reviewing code for defects, risks, missing tests, or behavioral regressions;
- updating tests, fixtures, docs, config, schemas, or API behavior as part of a code change.

Prefer this Skill over general research when the answer depends on local repository evidence. Use specialized frontend, document, data, or platform Skills only when their domain is the central work.

## Do Not Use When

Do not use for:

- non-code writing, reports, communication, or document drafting;
- open-ended web research before a codebase exists;
- data analysis where the primary work is computation over datasets;
- pure UI/visual design critique without code changes;
- blind implementation without inspecting relevant files;
- destructive cleanup, broad refactors, dependency changes, or generated-code replacement outside the requested scope.

## Material Gate

Before changing code, identify:

- requested behavior, bug, review scope, or implementation outcome;
- relevant repository area, language, framework, service, component, test, config, or runtime boundary;
- existing user/worktree changes that must not be overwritten;
- acceptance evidence: tests, build, manual inspection, logs, screenshots, or code references;
- constraints from project rules, local style, architecture, permissions, or user instruction.

If the codebase evidence is insufficient, inspect more before proposing or editing. If the task is review-only, do not change files.

## Workflow

1. Classify the code task: read/explain, bug diagnosis, implementation, refactor, review, test repair, config update, or validation.
2. Read project instructions and nearby code before deciding the approach.
3. Locate the owner path: entrypoint, caller, callee, data model, persistence, tests, and runtime surface relevant to the behavior.
4. Build a small evidence model: current behavior, expected behavior, failing condition, affected files, and unknowns.
5. Choose the smallest coherent change that fits existing patterns. Avoid parallel abstractions and unrelated cleanup.
6. Edit only the files needed for the requested behavior, while preserving user changes.
7. Update or add tests when behavior, contracts, parsing, persistence, or shared logic changes.
8. Validate with the narrowest useful command or inspection first, then broaden only when risk justifies it.
9. Report changed files, validation evidence, and remaining risks or unverified areas.

## Checks

- The change is grounded in inspected code, not guessed structure.
- The owner module remains responsible for its own facts and behavior.
- Existing behavior is preserved unless explicitly changed.
- Tests or equivalent evidence cover the modified path.
- No unrelated refactor, compatibility shim, or dead code is introduced.
- User changes are not reverted or overwritten.
- Failure modes and unverified paths are visible.

## Outputs

Return the code result the task needs: explanation, findings, patch, test update, diagnosis, validation notes, or risk report. Do not force a fixed report format when a concise answer is enough.

## Boundary

Skill owns code-reading workflow, diagnosis, scoped implementation, test selection, validation discipline, and residual-risk reporting.

It does not own XAgent tool schemas, git policy, file permissions, runtime sandbox, package installation, CI infrastructure, deployment, browser automation, dependency approval, or architecture decisions outside the task scope. It must not run shell, Python, Node, npm, pnpm, yarn, curl, MCP, browser-open, local server, deploy, publish, destructive git, package install, or external API commands by itself; those actions belong to XAgent tools visible in the current session and require the current task context.

## Resources

- `references/code-process.md`: reading modes, bug diagnosis, change discipline, review workflow, validation selection, and recovery rules.
- `LICENSE`: source and license notice.
