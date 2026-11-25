---
name: instructree
description: Diagnose Codex setup and map, explain, or lint repository-scoped coding-agent instructions. Use when Codex instructions or skills seem missing, or when auditing AGENTS.md, CLAUDE.md, Copilot instructions, agent skills, custom agents, or instruction conflicts before changing code.
license: MIT
metadata:
  short-description: Audit coding-agent instruction scope
---

# Instructree

Use Instructree to establish which instruction files exist, which may apply to a target, and whether their metadata or links are malformed.

## Run the audit

Work from the repository root. Prefer an already installed `instructree` command or the checked-out package's local binary. If neither is available, ask before downloading executable packages, then use the pinned release:

```bash
npx github:kotobuki09/instructree#6e6694c0cac60c06bb2d33162771eb9375ed13ad scan .
```

Do not add `--yes` unless the user has authorized non-interactive package downloads.

Choose the narrowest command that answers the request:

- `instructree scan . --json` inventories supported files and emits stable diagnostics.
- `instructree explain <file> --root .` shows instructions that may apply to one target.
- `instructree explain <file> --root . --client codex` selects the Codex repository project-instruction chain.
- Add repeatable `--fallback <filename>` values and `--max-bytes <n>` when the Codex project configuration uses non-default fallbacks or byte limits.
- `instructree explain <file> --root . --effective` includes recursive Copilot CLI imports.
- `instructree imports . --json` audits the recursive `@path` graph.
- `instructree skills . --client codex` concisely audits the shared `~/.agents/skills` root, Codex's deprecated default `~/.codex/skills` compatibility root, repository-local candidates, and supported user `~/.codex/config.toml` skill settings without installing, writing, or uploading anything. It reports disabled candidates, unmatched rules, unsupported relevant syntax, configured catalog pressure, and up to five largest enabled contributors under the fallback-character estimate. Add `--all` for every human-readable candidate or `--json` for the complete structured object. The `--client codex` flag may be omitted because `skills` is Codex-specific; use optional `--home <home>` only to inspect a different user scope.
- `instructree starter .` checks a focused six-skill Codex engineering stack against that local inventory, classifies companions as ready, disabled, invalid, or missing, and prints install commands only for missing skills. It is read-only and does not call the directory or install anything. Review each linked `SKILL.md` before installation; add `--json` for deterministic output.
- `instructree doctor .` produces one share-safe Codex pre-session report covering supported user project settings, user instructions, the current project chain, and summarized skill state. Add `--json` for deterministic structured output.
- `instructree scan . --sarif` emits SARIF 2.1.0 for code-scanning integrations.
- Add `--strict` only when warnings should fail the check.

## Interpret the result

Report file paths, line numbers, diagnostic codes, and the command's exit status. Separate schema or path errors from warnings. Describe `always`/`never` conflicts as possible conflicts requiring human review, not proof of agent behavior.

Instructree is static analysis. It does not upload repository content or call a model. Treat plain `explain` as a cross-client map of what may apply; use `--client codex` only for the documented repository project-instruction chain.

Use `doctor` when the user asks why Codex instructions or skills are missing, which project root or instruction files will be selected, or for a compact report suitable for an issue. It reads only a supported user-config subset and fails closed on unsupported relevant project settings. Treat its output as a pre-session preview, not live or resumed-session state; repeat its limitations when they matter.

The `skills` inventory follows Codex's documented shared `~/.agents/skills` root, its deprecated default `~/.codex/skills` compatibility root, and repository `.agents/skills` candidate scopes. It recursively scans depth-bounded roots, follows symlinked folders, deduplicates canonical targets, skips hidden descendants, and reports logical paths without exposing the home directory. It flags possible duplicate names with source lines, malformed metadata, scan failures, and an approximate initial-list character estimate including name, description, and logical path. The configured estimate ranks up to five largest enabled contributors and applies current Codex's 1,024-character per-description cap. It applies the supported skill subset of user `~/.codex/config.toml` with current Codex name/path and later-rule precedence, failing closed on unsupported relevant syntax. The 8,000-character comparison is only the unknown-context-window fallback; live Codex can use a model-context token budget and path aliases, so the ranking is a review aid rather than a prompt dump. The audit excludes custom `CODEX_HOME` roots, admin/system and plugin skills, session overrides, project-level skill rules, product restrictions, and configured project-root markers, so it does not claim an exact loaded list. Read the official [Codex skills documentation](https://developers.openai.com/codex/skills), the [skill-overload guide](https://kotobuki09.github.io/instructree/codex-skill-overload.html), Instructree's pinned [user-root research note](https://github.com/kotobuki09/instructree/blob/main/docs/research/codex-user-skill-roots.md), and the [skill-config research note](https://github.com/kotobuki09/instructree/blob/main/docs/research/codex-skill-config.md) when interpreting the estimate.

Do not edit instruction files unless the user asked for changes. After an authorized fix, rerun the same command and report the before-and-after diagnostics.
