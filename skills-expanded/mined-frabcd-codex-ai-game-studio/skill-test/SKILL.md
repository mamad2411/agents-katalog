---
name: skill-test
description: "Validate skill files for structural compliance and behavioral correctness. Three modes: static (linter), spec (behavioral), audit (coverage report)."
---

> Port provenance: adapted from the pinned upstream source at `984023ddac0d5e27624f2baacde6105e45de375f` under MIT; see the repository parity ledger for the exact path and blob.

# Test a Codex skill

Evaluate a target skill as both a package and a behavior. Testing is read-only
unless the user separately approves writing a report.

## Static validation

1. Locate the skill directory and read `SKILL.md` plus `agents/openai.yaml`.
2. Require YAML frontmatter containing exactly `name` and `description`.
3. Confirm the directory name and frontmatter name match and use lowercase
   hyphen-case.
4. Confirm the description explains both what the skill does and when it should
   activate. Reject unsupported legacy frontmatter and broken relative links.
5. Confirm `agents/openai.yaml` has a useful display name, a 25-64 character
   short description, and a default prompt that explicitly names the skill.
6. Confirm mutating setup, installation, engine-control, catalog-refresh, and
   destructive enhancement workflows disable implicit invocation.
7. Scan for secrets, absolute developer paths, path escapes, unsupported model
   pins, product-specific tool declarations, and platform-only assumptions.

Run the official skill validator when it is available. Report the exact command,
exit status, and diagnostics.

## Forward testing

Use isolated Codex subagents with the raw skill instructions. Cover:

- a direct explicit invocation;
- a natural-language request that should select the skill when implicit use is enabled;
- a near-miss that should route elsewhere;
- a negative or unsafe request that must preserve approval and rights gates.

Do not reveal an expected answer in the test prompt. Score routing, instruction
adherence, safety boundary, artifact clarity, platform neutrality, and evidence.
For failures, distinguish instruction defects from missing external capabilities.

Return a concise test matrix and a prioritized improvement proposal. Do not edit
the tested skill until the user approves that separate change.

## Codex portability

Use the search, file-editing, shell, user-input, and subagent capabilities available in the active Codex surface. Use PowerShell syntax on Windows and POSIX syntax on macOS/Linux; do not require a Unix compatibility layer on Windows. Inherit the active model and permission mode, and do not weaken approval or sandbox boundaries.
