---
name: productize-docs
description: >-
  Documentation gate for README, guides, help content, API docs, release docs, migration
  notes, support content, and docs consistency after product or code changes. Use when shipped
  behavior and written guidance must match.
---
<!-- AUTO-GENERATED from SKILL.md.tmpl - do not edit directly -->
<!-- Regenerate: npm run skills:generate -->

# Docs

## Productize Preamble

Before producing the artifact, implementation step, or code change, classify the work:

- **User/persona**: founder, product leader, AI PM, AI builder, stakeholder, or mixed/unknown.
- **Product stage**: idea, validation, PMF search, growth, scale, pivot, or unknown.
- **Artifact mode**: strategy memo, PRD, research plan, positioning, experiment, deck, roadmap, execution brief, diagnostic, or decision record.
- **Artifact format**: Markdown for short, repo-native, diff-sensitive artifacts; self-contained HTML for long, visual, shareable, interactive, or explicitly requested artifacts.
- **Evidence standard**: what is known, assumed, missing, and risky.
- **Decision mode**: recommend, ask for a blocking input, or proceed with explicit assumptions.

Operating rules:

1. Do not produce generic product strategy filler. Tie every recommendation to the user's context, evidence, stage, and decision pressure.
2. Separate facts from assumptions. Convert high-risk assumptions into tests, research prompts, or instrumentation.
3. Search existing context, attached docs, repo files, or prior Productize artifacts before inventing new structure when those sources are available.
4. Ask only for inputs that materially change the output. If the next step is obvious, proceed and state assumptions.
5. If another Productize skill is a better fit, name it and explain the routing in one sentence before continuing.
6. Enforce the output contract for this skill. Produce the artifact, implementation step, verification evidence, or code change; do not stop at a meta-explanation of the method.
7. End with the concrete next action, decision owner, validation step, metric, or artifact handoff when applicable.
8. Use the user's saved Productize preferences when available, but do not let stale preferences override explicit instructions in the current request.
9. If you must ask a blocking question, use this compact format: `AskUserQuestion: <one question> Why it matters: <decision it changes>`.
10. Record completion status for durable work as `completed`, `blocked`, `deferred`, or `needs-review` when runtime hooks are available.

Artifact format policy:

- Default to Markdown for short notes, repo-native documentation, changelog fragments, or artifacts where clean source diffs matter.
- Use a self-contained HTML file when the user asks for HTML, the artifact is likely to exceed about 100 lines, the reader needs diagrams/tables/comparisons/screenshots, the artifact is meant to be shared, or interaction/export controls would help the user stay in the loop.
- Route by product job first, then choose the format. Do not create a generic HTML workflow when a Productize playbook, gate, or routed skill owns the work.
- HTML artifacts must be local-first and portable: one file, embedded CSS/JS, no remote dependencies unless explicitly requested, readable without a dev server, responsive, accessible, and easy to skim.
- Prefer semantic sections, tables, SVG diagrams, annotated code blocks, status chips, collapsible detail, and copy/export buttons when they improve review speed. Avoid decorative complexity that hides the decision.
- For implementation work with ambiguities, use `$implementation-notes` when the user asks for a running notes file, especially `implementation-notes.html` or `implementation-notes.md`.

Runtime hooks, if available:

- Use `productize-workflow start "<user request>"` at the beginning of durable product work; it restores context, routes the request, records the session, and returns the required artifact contract.
- Use `productize-workflow complete --id <id> --status completed|blocked|deferred|needs-review --artifact-type <type> --summary <summary>` before ending durable product work; it records the artifact, saves context, and logs completion status.
- Use `productize-update-check --strict` at the start of maintenance, setup, release, or generated-output work.
- Use `productize-config` to read or write user/team preferences such as persona, artifact mode, evidence threshold, or update-check policy.
- Use `productize-session-log` to record important workflow decisions.
- Use `productize-artifact-log` when a durable artifact is produced.
- Use `productize-context-restore` before restarting long-running product work from scratch.
- Use `productize-context-save` after producing a durable strategy, research, spec, or stakeholder artifact.
- Use `productize-registry-search` or `productize-skill-router` when routing is ambiguous.
- Use `productize-completion-status` to log whether the workflow completed, blocked, deferred, or needs review.

Telemetry standard:

- Keep telemetry local by default in `.productize/` or `PRODUCTIZE_STATE_DIR`.
- Log artifact type, routing decision, evidence gaps, and completion status; do not log secrets or private customer data unless the user explicitly asks for it.

Current skill metadata:

- **Skill**: `docs`
- **Lifecycle**: Launch & Learn
- **Category**: Delivery
- **Primary artifact**: Docs gate report with docs scope, consistency check, update plan, decision, and handoff

Use this gate to keep documentation aligned with shipped behavior and user learning
needs. Docs owns accuracy, discoverability, and update scope.

Docs is a post-change audit, not a writing prompt. It cross-references what changed
against what users, support, developers, and stakeholders will read.

## Artifact Format

Use Markdown for targeted doc edits or proposed sections. Use self-contained HTML
when the docs review needs a coverage map, stale-claim matrix, reader-journey map,
screenshots, API/example audit, or shareable documentation readiness report.
Treat implementation notes as source evidence when they explain why behavior
differs from the original spec.

## Pre-Flight And Diff Analysis

1. Identify the change source: diff, release candidate, product plan, shipped behavior,
   API change, UX flow, support issue, or policy change.
2. Discover documentation surfaces:
   - README / getting started
   - docs site / guides
   - API / SDK / CLI docs
   - migration / upgrade notes
   - changelog / release notes
   - support / help center content
   - internal runbooks / architecture docs
   - privacy/security/legal docs when data practices changed
3. Classify the change: user behavior, developer behavior, API contract, data model,
   setup, migration, pricing, permissions, support workflow, or operational process.
4. State which docs are in scope and which are intentionally excluded.

## Per-File Audit

For each relevant doc:

| Doc | Audience | Current claim | Change impact | Action |
|---|---|---|---|---|

Action must be one of: no change, update, add link, add section, remove stale claim,
flag for owner, or block release.

## Update Rules

- Be conservative: update only claims contradicted by the change or required for
  successful use.
- Do not rewrite whole docs when a targeted section is enough.
- Do not remove large sections without an explicit decision.
- Preserve local voice and structure.
- Link docs together when discoverability is the issue.
- If developer docs are involved, call `$dx-review` for setup/examples/error paths.
- If customer-facing release language is involved, call `$comms-review` or
  `$release-notes`.

## Risky Documentation Decisions

Ask or record a decision when:

- the docs would promise a capability not fully shipped
- the product behavior is intentionally changing but migration guidance is unclear
- data, privacy, security, pricing, or contractual language changes
- multiple docs contradict each other and the source of truth is unclear
- release should block because users cannot succeed without docs

## Consistency And Discoverability

Check:

- every changed concept is findable from README, docs nav, or an obvious entry point
- naming is consistent across product, docs, release notes, and UI
- examples still compile or match current API/CLI behavior when applicable
- screenshots or UI references still match current screens
- TODOs or known limitations are updated rather than left stale

## Output Discipline

If the host agent can edit files and the user asked for docs updates, apply targeted
updates and list changed files. If not editing, produce exact proposed sections and
owners. Never claim docs are current without a per-file audit or explicit caveat.

## Route Internally

- `$design-handoff`
- `$technical-translation-and-stakeholder-communication`
- `$skimmable-writing-transformation`
- `$release-notes`
- `$structured-requirements-from-design-assets`
- `$privacy-policy` when data practices change
- `$dx-review` when developer-facing docs are part of the user experience
- `$implementation-notes` when implementation-time decisions changed what docs must explain

## Required Output

Return:

1. **Docs Scope**: docs affected, audiences, and behavior changes that must be reflected.
2. **Per-File Audit**: current claim, change impact, and action for each doc.
3. **Consistency Check**: contradictions, stale guidance, missing links, examples, screenshots, and unclear ownership.
4. **Updates Applied / Proposed**: exact files/sections or content blocks to add, revise, or leave unchanged.
5. **Risky Decisions**: promises, migration gaps, privacy/security/pricing language, or source-of-truth conflicts.
6. **Decision**: docs clear, update required, block release, or defer with owner.
7. **Handoff**: release, comms, DX, product, or support follow-up.
