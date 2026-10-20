---
name: repomix-context
description: Decide whether a repository task needs Repomix, define the smallest safe include scope, and govern generated repository references as disposable non-authoritative caches. Use for cross-module discovery, repository-wide architecture analysis, distant implementation comparison, or long tasks whose required context cannot be obtained efficiently through semantic navigation. Do not use for known files, isolated symbols, targeted edits, or facts already available from authoritative source files.
---

# Repomix Context

## Authority and boundary

- Treat this skill as the L8 implementation owner for bounded Repomix context
  preparation. Repository instructions and higher-layer product, domain,
  authorization, data, lifecycle, and dependency rules remain authoritative.
- Treat original source files, configuration, diagnostics, and version-matched
  official documentation as evidence. Treat packed output and generated Skills
  as disposable discovery caches.
- Do not use a generated artifact to define product semantics, architecture,
  completion, or approval.

## Decision gate

Use Repomix only when semantic declarations, references, usages, targeted file
search, and adjacent tests cannot answer the question efficiently. Stop and use
those narrower sources when the task concerns a known symbol, path, module, or
small set of files.

Before packing, state the exact question, the minimum sufficient include scope,
the exclusions, the output location, and how the result will be verified against
original files. Read [references/scope-policy.md](references/scope-policy.md) when
selecting patterns or handling generated reference Skills.

## Workflow

1. Resolve the repository root and read applicable repository guidance.
2. Inspect the active branch and working-tree state without changing it.
3. Use semantic navigation first for declarations, references, usages,
   implementations, and ownership boundaries.
4. Define the smallest include patterns that can answer the unresolved question.
5. Review `.gitignore`, `.repomixignore`, and Repomix configuration. Add explicit
   task exclusions for secrets, credentials, generated output, dependencies, and
   unrelated areas. Never rely on automatic security scanning as the only control.
6. Prefer the repository-pinned Repomix command. If none exists, obtain approval
   before downloading or executing a moving `@latest` version, then record the
   actual version used.
7. Apply the bundled `repomix-explorer` workflow under these stricter scope and
   security rules. Write output to a temporary location outside the working tree
   unless the user explicitly requests a retained generated reference.
8. Record the source commit, dirty-state limitation, include and exclude patterns,
   output path, compression choice, approximate token count, and security result.
9. Use the packed artifact only for broad discovery. Reopen every material finding
   in the original source before making a decision or edit.
10. Delete temporary output when it is no longer needed. Do not delete a retained
    artifact or user-owned output without explicit authorization.

## Generated reference Skills

Use Repomix `--skill-generate` only when a reusable snapshot materially helps a
long-running or remote-reference task. Keep generated Skills separate from this
authoritative workflow, mark them non-authoritative, and record their source state.
The generator is experimental; do not treat its current files or flags as a stable
contract.

For repository-local generated output, prefer
`.agents/skills/generated/<reference-name>/` and keep it ignored unless the user
explicitly asks to review and commit the snapshot. Never edit generated reference
content manually.

## Required report

Report:

- why Repomix was necessary after narrower discovery;
- repository and source revision;
- included and excluded scope;
- Repomix command and resolved version;
- output location, compression, token count, and security result;
- original files used to verify material findings;
- dirty-state caveats, assumptions, unresolved gaps, and cleanup status.
