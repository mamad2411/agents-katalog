---
name: hermes-skill-library-management
description: "Use when importing, auditing, disabling, consolidating, or verifying Hermes/cross-agent skill libraries. Routes skill-package work into import, cleanup, consolidation, or platform-pitfall workflows with explicit backup and verification gates."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [hermes, skills, import, cleanup, curation, consolidation, interoperability]
    related_skills: [hermes-agent, hermes-agent-skill-authoring]
---

# Hermes Skill Library Management

Use this skill when the user asks to manage a Hermes skill library as a durable instruction corpus: importing skills from other agent ecosystems, adapting or translating upstream `SKILL.md` packages, cleaning up registered skills, consolidating narrow local skills into umbrellas, or verifying the resulting library.

This is a class-level umbrella for skill-library operations. Prefer one rich skill with labeled workflows and support files over many one-session micro-skills.

## Choose the workflow

Start by choosing exactly one branch, then follow that workflow to its completion gate:

- **Import branch** — upstream or cross-agent skill packages need to be installed, adapted, mirrored, or verified. Use Workflow A.
- **Cleanup branch** — installed skills need to be disabled, pruned, rationalized, or made less noisy. Use Workflow B.
- **Consolidation branch** — multiple local skills cover the same class of work and should become an umbrella. Use Workflow C.
- **Platform pitfall branch** — a skill operation failed because of paths, media delivery, shell differences, or harness-specific behavior. Keep the main workflow active and open the relevant reference only when the pitfall appears.

Completion means the chosen branch is verified through the real consumer path: Hermes skills load via `skill_view`, non-Hermes mirrors have matching files, and any backup/archive/provenance record exists before destructive changes.

## Core principles

- Treat skills as reusable class-level instructions, not session logs.
- Preserve recoverability: disable or archive before destructive removal; keep support files when content is still valuable.
- Preserve provenance and attribution for imported upstream assets.
- Normalize metadata so Hermes can parse and index skills reliably.
- Verify with the real Hermes skill inspection path, not only filesystem checks.

## Workflow A: import upstream agent skills

Use when a user wants skills from another agent ecosystem (for example Codex `.codex/skills`) made available in Hermes or across multiple harnesses.

1. **Inspect local and upstream sources.**
   - Check whether the local installation already ships the requested skills.
   - If not, inspect the upstream repository for `SKILL.md` directories and support folders such as `references/`, `templates/`, `scripts/`, `assets/`, and `agents/`.
   - Enumerate directories first, then fetch/copy each relevant `SKILL.md` and support file.
2. **Audit before installing.**
   - Search text files for command execution, network fetches, secret patterns, prompt-injection language, and dangerous permission/tool directives.
   - Inspect executable/script files separately before mirroring them.
   - Check license/notice files and preserve attribution.
3. **Install with safe naming and metadata.**
   - Use collision-safe names such as `codex-upstream-<name>` when provenance matters.
   - Quote long YAML descriptions, especially when they contain colons or commas.
   - Quote YAML dates as strings; bare dates can deserialize to native date objects and break downstream JSON serialization.
   - Add source metadata naming the upstream repo/path and whether support files were mirrored.
4. **Adapt when requested.**
   - Translate `SKILL.md` and operational references into English when the user asks for English usability.
   - Preserve intentional non-English output requirements when they are part of the style/domain.
5. **Support multi-harness installs when requested.**
   - Hermes global skills: `~/.hermes/skills/<category>/<skill-name>/`.
   - Codex global skills: `~/.codex/skills/<skill-name>/`.
   - Vesper global skills: `~/.vesper/skills/<skill-name>/`.
   - Copy the same adapted package unless the harness requires different frontmatter.
6. **Verify.**
   - Hermes: open the imported skill with `skill_view`, and open at least one linked support file.
   - Non-Hermes targets: confirm `SKILL.md` exists, parse frontmatter, count support files, and run safe lightweight bundled scripts when appropriate.
   - Report whether full support-file parity was achieved.

## Workflow B: clean up and rationalize a skill library

Use when the user asks to review, prune, clean up, disable, or rationalize their registered Hermes skills.

1. **Inspect the current list.**
   - Use the active skill listing or `hermes skills list` to get enabled/disabled counts and skill names.
   - Inspect descriptions/categories when needed; names alone are not enough.
2. **Inspect config before writing.**
   - `hermes config path` identifies the active `config.yaml`.
   - Global disables are usually under:
     ```yaml
     skills:
       disabled:
         - skill-name
     ```
   - Prefer global `skills.disabled` unless the user asks for platform-only behavior.
3. **Classify conservatively for disabling.**
   - Obvious non-day-to-day examples: prediction markets, gaming/emulator automation, smart-home control, jailbreak/red-team prompt packs.
   - Good review candidates but not automatic disables: specialized creative/media tools, MLOps tools, productivity integrations, and project-specific upstream workflow skills.
   - Do not disable broad workhorse skills such as Hermes config, GitHub workflows, debugging, planning, TDD, code review, file/tool skills, or user-known core workflows without asking.
4. **Disable safely.**
   - Create a timestamped backup of `~/.hermes/config.yaml` before editing.
   - Merge new names with existing `skills.disabled`; preserve order and avoid duplicates.
5. **Verify and report.**
   - Run `hermes skills list` again.
   - Confirm intended skills show disabled and tell the user how to refresh the session.

## Workflow C: consolidate narrow local skills into umbrellas

Use when the user asks for skill-library curation, umbrella-building, or consolidation.

1. **Scan the complete candidate set.**
   - Identify prefix/domain clusters such as `gateway-*`, `hermes-config-*`, `codex-*`, `mcp-*`, `security-*`, `pr-*`, or `knowledgebase-*`.
   - Do not rely on usage counters; judge content overlap and maintainability.
2. **Ask the umbrella question.**
   - For each cluster with 2+ members, ask whether a human maintainer would write N separate skills or one class-level skill with labeled subsections.
   - Distinct triggers are not enough to keep narrow siblings separate when they share a workflow class.
3. **Choose the consolidation shape.**
   - Merge into an existing umbrella when one skill is already broad enough.
   - Create a new umbrella when no member name/body is broad enough.
   - Demote session-specific material to `references/`, reusable starters to `templates/`, and static probes/scripts to `scripts/`.
4. **Archive absorbed siblings recoverably.**
   - Never touch bundled/hub-installed or pinned skills.
   - Do not permanently delete recoverable local knowledge; archive absorbed skills and pass an explicit `absorbed_into` target when using the skill manager so references can migrate.
5. **Verify and summarize.**
   - Load the umbrella skill after changes.
   - Produce a structured summary distinguishing consolidations from true prunings.

## Platform pitfall pointer

Keep platform-specific path, media-delivery, and shell notes out of the main decision path unless they affect the current branch. When they do, open the relevant reference under **Importing upstream skills** or the Windows/media path notes before editing or reporting success.

## References

### Importing upstream skills

- `references/codex-upstream-import-notes.md` — successful Codex-to-Hermes import notes.
- `references/security-translation-cross-agent-import.md` — security scanning, English adaptation, and mirrored installation checklist.
- `references/cross-agent-global-skill-installs.md` — directory conventions and verification checklist for Hermes/Codex/Vesper installs.
- `references/skills-cli-vesper-manual-mirror.md` — `npx skills` CLI pattern when Vesper is requested but not recognized as an agent; install supported agents, manually mirror into `~/.vesper/skills/`, and verify parity.
- `references/english-adapted-cross-agent-installs.md` — non-English upstream skill adaptation across harnesses.
- `references/public-docs-derived-cross-agent-skills.md` — creating safe skills from public docs sites.
- `references/github-repo-cross-agent-skill-import.md` — public GitHub repo skill-package import checklist.
- `references/x-post-linked-skill-imports.md` — resolving skills mentioned in X/Twitter posts/articles.
- `references/x-article-skill-bundle-assessment.md` — saving X Articles and assessing whether a case study should become an umbrella skill bundle.
- `references/windows-telegram-media-paths.md` — Windows media-delivery path pitfall encountered during skill import artifact delivery.

### Cleanup and consolidation

- `references/2026-06-01-skill-cleanup.md` — example safe cleanup pass.
- `references/gateway-media-delivery.md` — gateway media/file-delivery debugging and Windows path notes preserved from a narrower skill.
- `references/knowledgebase-capture.md` — durable web/article/post capture workflow preserved from a narrower skill.

## Pitfalls

- Do not uninstall or delete when disable/archive is enough.
- Do not import only `SKILL.md` when support files are required for functionality unless you clearly report partial parity.
- Do not let one-session bugs become standalone skills forever; move them under a class-level umbrella as sections or support files.
- Do not edit protected upstream/bundled skills to encode user-level library preferences.
- Remember that skill and tool surface changes often require `/reset`, CLI restart, or gateway restart to affect the active prompt.
