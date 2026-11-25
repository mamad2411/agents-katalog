---
name: make-repo-agent-legible
description: >-
  Help coding agents find a repository's purpose, architecture, constraints, workflows, validation, and authoritative sources. Use this skill when essential knowledge is unavailable, obsolete, or not enforced. Do not use it for general code review, marketing documents, product documents, or narrow implementation work.
---

# Make Repository Agent Legible

## Workflow

1. Establish the repository scale and type. Preserve effective documentation conventions. Do not add a large document tree to a small package.
2. Read the entry documents, instructions, document indexes, build configuration, test configuration, CI configuration, and a representative code sample.
3. Use the rubric to audit navigation, authoritative-source ownership, architecture, enforcement, task history, runtime inspection, and maintenance controls.
4. Separate roles:
   - `README.md`: purpose, audience, minimum useful workflow, boundaries, and links to detailed information.
   - `AGENTS.md`: short coding-agent guide, repository constraints, validation commands, and task routing.
   - Detailed repository documents: maintained architecture, operations, quality, decisions, and plans. Add them only when the repository needs them.
5. Select the smallest artifact or check that prevents the most repeated search work. Link to the authoritative source instead of duplicating it.
6. Move important knowledge from outside the repository into versioned artifacts only when verified. Mark inaccessible or uncertain knowledge as unknown. Do not reconstruct it from assumptions.
7. Use automated enforcement for repeated constraints when the verified benefit is greater than the cost. Make each failure message explain the recovery action.
8. Validate links, commands, ownership boundaries, and relevant runtime paths. Report what remains outside the repository or unenforced.

For an audit-only request, inspect and report without editing. For implementation, keep changes proportional to the repository and preserve unrelated documentation.

## Documentation Checks

For a repository with Markdown, inspect its Perfect Doc configuration, offline
command, installation instructions, and aggregate check. Report missing setup
during an audit. Add the missing setup only when implementation is in scope.

Use the native executable when no suitable Python or npm package is published.
Verify current installation instructions in the
[Perfect Doc README](https://github.com/btfranklin/perfect-doc#build-and-install).
Preserve an existing `perfect-doc.toml`. For new configuration, use
`perfect-doc init`, then select the intended Markdown files. Preserve dependency
and build exclusions. Exclude scratch files, worktrees, and generated copies.
Match the project's dialect, fragments, routes, and link rules.

Document `perfect-doc check . --offline --no-banner`, or the repository's
equivalent command, in `README.md` and `AGENTS.md`. Include it in the existing
aggregate check. Verify that existing CI runs the command and installs the
executable first. Do not create CI unless it is in scope.

Run the check. Confirm its selected document count and result. A missing
executable or incomplete scan is a failure. Review findings before changing
documents or rule policies. Keep checks for content, metadata, generated
references, and application behavior.

## Decisions

- Prefer a short repository guide to a long instruction document.
- Add architecture, operations, decision, or plan artifacts only when the repository's scale and work patterns justify maintaining them.
- Keep each fact in one authoritative location. Use indexes and cross-links for discovery.
- Move recurring rules from prose only when enforcement has a verified net benefit. Use helpers, structural tests, linters, or CI.
- Include runnable commands, repeatable reproductions, logs, and inspectable state when static documents are not sufficient.

## Resources

- Read [references/legibility-rubric.md](references/legibility-rubric.md) when auditing and prioritizing gaps.
- Read [references/artifact-patterns.md](references/artifact-patterns.md) only when you select or implement repository artifacts and enforcement.
- Read [examples/legibility-audit-output.md](examples/legibility-audit-output.md) when preparing a concrete audit report.
