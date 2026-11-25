---
name: docs-maintenance
description: "Keeps technical documentation, README instructions, examples, configuration references, and code samples aligned with the actual repository. Use after behavior or setup changes, when documentation is stale, or when preparing user-facing guides."
license: MIT
metadata:
  author: OpenSelfHosting
  version: "1.0.0"
---

# Documentation Maintenance

## Goal
Make documentation accurate, task-oriented, discoverable, and testable against the current implementation.

## Workflow
1. Identify audience and task: first-time setup, daily development, API use, operations, migration, troubleshooting, or architecture.
2. Read repository instructions and inspect the implementation/configuration that the documentation describes. Existing prose is evidence to compare, not proof of current behavior.
3. Find affected docs, examples, references, generated docs, and links. Prefer updating the source of truth rather than manually editing generated output.
4. Verify every operational claim: prerequisites, supported versions, commands, environment variable names, default ports, paths, permissions, expected output, and recovery steps.
5. Write the shortest sequence that lets the intended reader complete the task. Explain required values and safe placeholders; never add real credentials or personal information.
6. Ensure examples are internally consistent and match current schemas and APIs. Run code samples or documentation checks when tooling exists; clearly mark illustrative pseudocode that is not executable.
7. Add troubleshooting for likely failure modes and safe diagnostics. Avoid telling readers to disable security controls as a generic fix.
8. Review accessibility and navigation: descriptive headings, meaningful link text, code fences with language hints, clear warnings, and relative links that resolve.
9. Inspect the diff and remove stale claims rather than adding contradictory caveats in multiple places.

## Quality checklist
- A new user can identify prerequisites and the first successful path.
- Commands can be copied without undisclosed context.
- Defaults and platform-specific differences are explicit.
- Security-sensitive steps explain least privilege and secret handling.
- Limitations and unsupported cases are disclosed.
- Links and examples point to the right files or current endpoints.

## Report
List files updated, claims/commands verified, checks run, and known documentation gaps.

## Guardrails
Never invent features, flags, version support, benchmark numbers, or guarantees. If current external facts matter, use official sources where available and note when verified. Avoid broad unrelated rewrites that obscure the substantive update.
