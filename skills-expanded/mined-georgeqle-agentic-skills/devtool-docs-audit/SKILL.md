---
name: devtool-docs-audit
description: Use only for developer-facing products; audit docs for quickstart clarity, examples, API reference, troubleshooting, and migration paths
type: review
version: v0.2
required_conventions: [alignment-page]
context_intake: artifact_only
---

# Devtool Docs Audit

Invoke as `$devtool-docs-audit`.

Review developer documentation for adoption blockers.

## Output

Write or update `research/devtool-docs-audit.md` with a findings-first docs audit covering quickstart clarity, examples, API reference, troubleshooting, migration paths, and missing proof artifacts. In the final response, include `Recommended next skill: <command>` using the `## Next-Skill Routing` rules below.

## Alignment Page

Follow the shared alignment-page convention via the packaged convention resolver; output path is `alignment/devtool-docs-audit-{topic}.html`.

## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.

## Next-Skill Routing

After writing or updating approved artifacts, recommend the next contextual action:

1. If the alignment page is still in review or the user has not provided final compiled YAML, stop and ask for review of the HTML alignment page. Do not include downstream routing until approval YAML has been provided.
2. If the audit identifies immediately actionable documentation or skill-contract cleanup and the user approves remediation, recommend the implementation route for the approved cleanup plan.
3. If `tasks/todo.md` has an unchecked devtool item in `## Priority Documentation Todo`, recommend the first unchecked devtool command from that queue.
4. Otherwise, recommend `$research-roadmap` to confirm the devtool documentation queue is complete and identify any non-devtool follow-up.
5. If `$research-roadmap` reports no queue, recommend `$roadmap` only when implementation planning is missing or stale.
