---
name: manage-workspace-agents-md
description: Create, update, refactor, audit, or align repository AGENTS.md guidance from repository evidence without adding language, tool, or dependency recommendations.
---

# manage-workspace-agents-md

Use this skill to create or improve a high-signal root or nested `AGENTS.md` guide for a software workspace. The output should help coding agents make correct changes quickly without turning the guide into a policy dump, language handbook, or generic best-practices essay.

This skill is a procedure. It is not content to copy wholesale into a generated guide.

## Operating principle

Optimize for agent usability: concrete rules, stable headings, shallow hierarchy, and the smallest set of always-relevant instructions. The skill may infer repository standards from evidence, but it must not introduce preferred dependencies, package managers, frameworks, test libraries, or language-specific coding styles. Treat well-documented code, tests, executable examples, schemas, fixtures, and generator inputs as the source of truth for internal behavior; `AGENTS.md` should route agents to those surfaces rather than requiring separate narrative documents for implementation rationale.

A strong guide answers these questions immediately:

1. Where should an agent start for common work?
2. Which surface owns a change?
3. Is the surface user-facing, public integration, generated, validation-only, or internal?
4. Which user-facing docs, examples, tests, generated files, fixtures, and existing `AGENTS.md` guidance must change together?
5. Which narrow validation command proves the change?

## Decision kernel

1. Choose the smallest mode that answers the request.
2. Inspect repository evidence before making repository-specific claims.
3. Add only **Observed** or clearly justified **Inferred** facts to generated guidance.
4. Keep **Recommended** tools, dependencies, migrations, commands, frameworks, and workflow changes out of mandatory guide text.
5. Preserve existing local standards instead of replacing them with ecosystem preferences.
6. Keep root guidance short; split path-specific procedures into nested `AGENTS.md` or local docs.
7. Use precise validation wording; never imply commands were run when they were only reviewed.

## Do not use this skill for

- General repository documentation unrelated to contributor or coding-agent guidance.
- Release notes, README content, troubleshooting guides, or other repository documentation unrelated to agent routing and synchronization.
- Generic language, framework, or ecosystem best-practices guidance.
- Recommending new dependencies, package managers, test frameworks, type checkers, formatters, linters, or runtime frameworks.
- Writing or implementing code-level tests. Use a dedicated testing or language skill when available; for Rust test work, use `rust-test` when available.
- Creating, updating, auditing, or aligning `.agents/` directories, `.agents/*` guidance, skill files, custom-agent files, or persona files.
- Overriding local subtree guidance when a nested `AGENTS.md` file owns that scope.

## Reference map

Supporting files are source material and handoff scaffolding, not default output:

- `templates/mode-handoffs.md`: final response shapes for Draft, Patch/refactor, Audit, Alignment, and Checklist modes.
- `patterns/evidence-and-scope.md`: evidence gates, claim classification, conflict precedence, limited-evidence handling, and placeholder hygiene.
- `patterns/standards-inference.md`: how to infer repository standards from evidence without recommending new tools.
- `patterns/agent-guide-layout.md`: guide layout, audience labels, sync rules, workspace map patterns, size budget, and split triggers.
- `patterns/validation-guidance.md`: validation wording and validation-by-change-type routing.
- `checklists/agent-guide-audit.md`: final checklist for generated or patched `AGENTS.md` guidance.

Before using any example or bullet from a reference file, replace it with repository-specific guidance or omit it. Before final output, search for copied pattern headings, placeholder paths, and example commands from `patterns/*` or `templates/*`; remove or replace anything not backed by repository or artifact evidence.

## Output modes

Always identify the selected mode in one sentence before the main output.

| User asks for | Choose | Output |
| --- | --- | --- |
| “Create an `AGENTS.md`” and no suitable guide exists | Draft | A complete guide based only on repository evidence. |
| “Improve this file,” “clean this up,” or “make targeted edits” | Patch | Minimal edits; preserve structure unless structure is the problem. |
| “Refactor,” “reorganize,” or “make this guide easier to scan” | Patch | Structural edits that preserve repository facts; verify evidence for changed or newly emphasized claims. |
| “Review,” “is this good,” or “could it be improved?” | Audit | Findings by severity with concrete fixes. |
| “Compare against the repo,” “is this stale,” or “does this match CI/docs?” | Alignment | Drift report against repository truth. |
| “Apply the checklist” | Checklist | Pass/fail/not-checked notes. |

For existing `AGENTS.md` artifacts, treat “check,” “review,” “is this good,” and “could this be improved” as Audit. Treat “edit,” “apply,” “rewrite,” “patch,” or “update the file” as Patch. If a prompt says “improve” without an edit verb, prefer Audit unless the user clearly expects changed `AGENTS.md` content.

Ambiguous prompt examples:

- “Improve this AGENTS.md” -> Patch.
- “Could this AGENTS.md be improved?” -> Audit.
- “Apply your recommended improvements” -> Patch.

If the user provides only an `AGENTS.md` guide and no repository, perform an evidence-limited Audit or Patch. Do not invent repository commands, paths, manifests, sync rules, or validation claims.

In Patch mode, make the file changes when repository write access is available. If edits cannot be applied directly, provide a unified diff or exact replacement sections before the handoff. Do not provide only advisory findings unless the selected mode is Audit.

When the request is ambiguous, choose the smallest useful mode. Prefer Audit for existing guidance unless the user clearly asked for edits.

### Severity definitions for audits

- **Critical**: likely to cause wrong edits, false validation claims, broken commands, stale public-contract guidance, or unsafe repository-wide assumptions.
- **Important**: likely to slow agents down, duplicate guidance, obscure ownership, miss required docs/tests synchronization, or overstate recommendations as repository truth.
- **Nice to have**: improves readability, routing, concision, examples, or handoff quality without materially changing correctness.

## Required workflow

1. **Select mode.** Declare Draft, Patch, Audit, Alignment, or Checklist.
2. **Inspect evidence.** For `AGENTS.md` work, use `patterns/evidence-and-scope.md`.
3. **Check agent platform compatibility when applicable.** If the request or repository names a target agent runtime, use `patterns/evidence-and-scope.md` to check supported instruction filenames, discovery locations, precedence, merge behavior, and size limits before choosing where `AGENTS.md` guidance belongs. Do not assume one agent platform reads another platform's files.
4. **Infer standards for repository guidance work.** Use `patterns/standards-inference.md` to classify local conventions as **Observed**, **Inferred**, or **Recommended**.
5. **Use reference files selectively.** Layout, evidence, validation, and checklist files are inputs to judgment, not sections to paste.
6. **Draft, patch, audit, align, or checklist-review.** Keep changes as small as the selected mode allows.
7. **Check for support-file leakage.** Before final output, search for copied pattern headings, placeholder paths, example commands, and fenced examples from `patterns/*` or `templates/*` that are not backed by evidence. Remove or replace them.
8. **Validate or disclose.** Run only available checks that fit the scope, then use exact validation wording in the handoff.

## Evidence floor

Match evidence depth to the selected mode:

- **Draft and Alignment:** inspect broad repository evidence, including the top-level tree, existing root and nested `AGENTS.md` guidance, README/contributor docs, manifests, lockfiles, workspace config, package metadata, CI workflows, runner files, and named docs/examples/tests/generated surfaces.
- **Patch:** inspect the guide being patched, applicable local guidance, and evidence for every changed or added command, path, ownership claim, synchronization rule, or validation claim.
- **Audit:** inspect enough repository evidence to verify or challenge the artifact's claims. If coverage is incomplete, mark findings evidence-limited.
- **Checklist:** inspect only the files needed to check each item. Mark unsupported items `Not checked`.
- **Platform compatibility:** when a target agent or runtime is named, inspect evidenced platform rules for instruction discovery, local precedence, override behavior, and size limits. Mark uninspected platform behavior as `Not checked`.

For large repositories, inspect every named surface and representative evidence for each claimed workflow category. If full coverage is impractical, state what was inspected, mark remaining areas as not checked, and avoid repository-wide claims for uninspected categories.

## Output boundaries

Generated guidance should contain only repository-specific instructions that contributors and coding agents need while editing. Do not copy this skill's procedure, output mode rules, evidence gates, templates, pattern files, or checklists into `AGENTS.md` unless a point is directly relevant to daily repository work and supported by evidence.

Do not add `AGENTS.md` guidance that only restates `.gitignore`, ignored build or cache directories, dependency caches, or tool output directories. Treat ignored outputs as non-source by default; mention them only when a repository-owned generator, checked-in generated artifact, cleanup workflow, or validation step makes the path part of normal editing.

Do not add or keep workspace-map entries, decision-flow steps, or sync rules for generic manifests, lockfiles, dependency metadata, dependency automation config, package-manager config, or routine CI config just because they exist. Use these files as evidence for workspace shape, commands, package manager, and validation. Mention them in generated guidance only when the repository has a documented, non-obvious editing procedure for that exact surface that agents must follow during ordinary work. In Patch, Alignment, and Checklist modes, remove existing guide text that only says to keep lockfiles aligned, update dependency automation schedules/groups/labels, or route ordinary dependency metadata edits.

When repository evidence identifies high-risk edit surfaces, include a short boundary note: generated outputs should be changed through their generator when one exists; release, deployment, migration, or production configuration files may require extra approval when local guidance says so; secrets, credentials, and vendored dependencies must not be edited as ordinary source. Do not invent restricted areas that are not evidenced by repository files or existing guidance.

Prefer a root `AGENTS.md` under 220 lines. Split into nested `AGENTS.md` or local docs when a procedure is path-specific, generated-output-heavy, release-only, troubleshooting-oriented, or longer than a short checklist. If the target agent has an evidenced instruction-size or truncation limit, keep the applicable guidance under that limit or split path-specific material closer to the files it governs.

## Terminology boundary

Use these terms narrowly:

- `AGENTS.md`: durable repository or subtree guidance for most coding-agent work in that scope. Root and nested `AGENTS.md` files are the only agent-guidance artifacts this skill creates, patches, audits, aligns, or checklist-reviews.
- Non-`AGENTS.md` agent artifacts, including skill directories, custom-agent files, persona files, plugins, MCP servers, tool integrations, scripts, and executable helpers, are out of scope for this skill.

Do not collapse these surfaces into one file type merely because the word “agent” appears in a path.

## Standards guidance boundary

This skill can describe standards only when they are repository standards:

- **Observed:** directly evidenced by existing files, commands, tests, docs, manifests, CI, or local guidance.
- **Inferred:** strongly implied by repeated local practice, workspace structure, or public entry points.
- **Recommended:** plausible but not current repository truth; keep out of generated guide text unless the user explicitly asked for a proposal.

Do not add language-specific rules merely because a language appears in the repository. Name local standards only when they affect agent routing, ownership, synchronization, or validation.

For code-level conventions, use the relevant dedicated skill when available. If a dedicated language or testing skill already owns a pattern, this skill should point to existing repository guidance or a real `AGENTS.md` path only when that path exists and is relevant.

## Validation wording

This section is the canonical validation wording for the skill and its templates. Use these exact distinctions:

- `Validated with: <command>` only for commands or checks actually run.
- `Reviewed only; not executed because: <reason>` for static review without execution.
- `Not validated; missing repo access / command unavailable / outside requested scope: <reason>` when validation was not possible or not attempted.

Do not say `validated`, `tested`, `passes`, or `works` for changes that were only inspected.

## Final response format

Use the appropriate template from `templates/mode-handoffs.md`. For small requests, compact the handoff while preserving selected mode, changed or audited scope, validation wording, missing evidence, and actionable next steps. Include:

- selected mode;
- what changed or what was audited;
- important assumptions;
- validation performed with exact wording;
- validation not performed and why;
- unresolved conflicts or missing evidence;
- directly actionable next steps, only when useful.
