---
name: harness-profile-adapter
description: Creates and maintains harness-specific subagent/profile adapters after agent-ready context and custom action skills exist, and separately checks whether the active harness can natively discover AGENTS.md and .agents/skills/ at all - bridging either with a local alias when it can't. The bridging check is baseline compatibility and applies whenever agent-ready-context finishes a pass, regardless of whether runtime adapters are also wanted; full subagent/profile/persona generation stays optional, used only when the user separately requests it, without either becoming a source of truth.
license: See LICENSING.md
compatibility: Requires an Agent Skills compatible harness, repository file read/write access, and Python 3.11+ for optional validation helpers (run them with uv when available). Requires web access or local harness documentation when current subagent/profile semantics are unknown.
metadata:
  version: "0.2.0"
  spec: agentskills.io
  author: Romain Monier
  author-url: https://github.com/rmonier
  source: https://github.com/rmonier/agent-smith
  harness-profile-adapter.companion-skills: agent-ready-context, skill-creator
  harness-profile-adapter.companion-skill-roles: agent-ready-context=preferred upstream context workflow; skill-creator=preferred upstream action-skill workflow
  harness-profile-adapter.provides: runtime-context-inspection, tooling-context-policy, harness-visibility-bridging, harness-adapter-generation
  harness-profile-adapter.runtime-detection: references/runtime-detection.md
  harness-profile-adapter.tooling-context-policy: references/tooling-context-policy.md
allowed-tools: Read Write Edit Bash(uv:*) Bash(python:*) Bash(git:*) Bash(readlink:*) Bash(test:*) Bash(mkdir:*) WebFetch WebSearch
---

# Harness Profile Adapter

Use this skill to create or maintain **harness-specific subagent/profile adapters** from the repository's existing agent-ready context.

This skill does **not** define a new portable subagent standard. It helps the current agent understand the active harness and write the native files expected by that harness, using current local or official documentation.

## Boundary rules

- **OKF wiki = context source of truth**: durable project knowledge, external evidence, tooling context, and provenance.
- **AGENTS.md = orientation/index/best practices**: short repo guide for agents.
- **Agent Skills = actions**: reusable procedures and scripts under `.agents/skills/`.
- **Subagent/profile adapters = runtime-specific projections**: generated or maintained for the active harness only.

Do not create new directories under `.agents/` except Agent Skills under `.agents/skills/`. `okf/wiki/tooling/` holds two things only: the minimal harness build record that every agent-ready pass writes (or explicitly declines — see `references/tooling-context-policy.md`), and fuller harness evidence persisted when this skill is explicitly run for a harness. Use the link policy in `references/tooling-context-policy.md`.

## Core workflow

Run this skill only after:

1. `AGENTS.md` exists or has been refreshed by `agent-ready-context`.
2. `okf/wiki/index.md` exists or has been refreshed.
3. Custom action skills have been created or reviewed by `skill-creator` when repeated actions were found.

This skill covers two things, and only the second is optional:

- **Baseline harness-visibility bridging** (Detect/Check/Bridge, steps 1-3 of the numbered workflow just below — not the prerequisites list above) — check whether the active harness can natively discover root `AGENTS.md` and `.agents/skills/` at all, and bridge the gap when it can't. Do this whenever this skill is invoked after the prerequisites above, whether or not the user separately asked for runtime adapters: without it, the harness cannot see any of what `agent-ready-context` and `skill-creator` just built, and no adapter generated in step 4+ would help either. Best-effort, never blocking: if the harness or its requirements can't be determined, say so instead of silently skipping.
- **Runtime subagent/profile adapters** (Design/Ask/Write/Validate, steps 4-7) — generated only when the user explicitly wants them, after the above.

Then:

1. **Detect the active runtime, not merely installed tools.**
   - Prefer explicit harness metadata exposed by the current environment or conversation.
   - Inspect parent process and environment hints if available.
   - Inspect repo files only as low-confidence hints.
   - Do **not** use `<tool> --version` or the presence of an installed binary as proof of the active harness.
   - If runtime remains ambiguous, ask the user which harness to target.

2. **Check what the active harness natively discovers, using current docs.**
   - Whether it reads `AGENTS.md` directly, or requires a differently named instruction file.
   - Whether it scans `.agents/skills/` directly, or only its own dedicated skills directory (harness-specific location, docs may cover more than one candidate location - confirm the one that actually applies).
   - Whether a newly created directory in either location needs a session/process restart before the harness picks it up - many harnesses only scan for skills at startup, so say so up front rather than after a bridge appears not to have worked.
   - Follow `references/harness-docs.md` for source priority and the full lookup checklist (instruction-file behavior, skills-directory behavior, restart requirement, plus everything needed for adapter generation).
   - If persistence is useful, record the evidence and summary under `okf/wiki/tooling/harnesses/<harness>.md`; otherwise keep it as transient reasoning/output. Baseline OKF bootstrap writes only the minimal harness build record defined in `references/tooling-context-policy.md` (or justifies its absence in the run report); fuller tooling pages stay adapter work.

3. **Bridge whatever step 2 found the harness can't discover natively.**
   - `AGENTS.md` and `.agents/skills/` remain the canonical sources; a bridge is always a local alias pointing back at them, never a copy - one place to edit either way.
   - Confirm the exact required file/directory name or path from docs or the user before creating anything.
   - Use `scripts/ensure_local_alias.py` for both cases (it detects file vs. directory from `--source` automatically): a relative symlink first, and for a harness-required skills directory that a symlink can't reach (elevated-privilege platforms), a same-semantics directory alias with no admin rights required - see the script's own docstring for the exact fallback chain and why a directory alias has no text-pointer substitute.
   - Add the alias path to `.git/info/exclude` unless the user explicitly wants a tracked adapter (the script does this automatically).
   - If a restart is needed per step 2, tell the user before considering the bridge done.

4. **Design candidate subagent/profile adapters.**
   - Derive them from actual repository needs, OKF pages, and available skills.
   - Good candidates are task-scoped and permission-bounded, for example `okf-curator`, `skill-architect`, `repo-cartographer`, `security-reviewer`, or `dependency-scout`.
   - Do not embed long project context inside profile files. Point to `AGENTS.md`, `okf/wiki/index.md`, and relevant skills.
   - Follow `references/profile-authoring.md` for the full candidate-design checklist (what each adapter must answer) and anti-bloat rules before writing one.

5. **Ask the user how to track generated harness-specific files.**
   - Local-only via `.git/info/exclude`.
   - Ignored for all via `.gitignore`.
   - Committed as shared team adapters.
   - Default to local-only if the user has not chosen a team policy.
   - Follow `references/git-tracking-policy.md` for the full policy, including the different (gitignore, not exclude) rule for `okf/wiki/tooling/` pages.

6. **Write native adapter files by reasoning from current docs.**
   - Do not rely on hardcoded vendor renderers.
   - Do not assume fields are stable between harness versions.
   - Read the current docs and implement the native format directly.
   - Keep adapter files short: purpose, activation/description, permissions/tools if supported, and instructions to consult `AGENTS.md`, `okf/wiki/index.md`, and skills.

7. **Validate outputs.**
   - Verify the files are in the correct harness location.
   - Verify no profile embeds large OKF/project content.
   - Verify project OKF concept pages do not link back to `okf/wiki/tooling/`.
   - Verify the bundle-root `okf/wiki/index.md` lists `okf/wiki/tooling/` in a clearly labeled harness-specific section when tooling pages exist, and that the committed `tooling/index.md` navigation stub exists (tooling pages are local by default; the stub keeps navigation coherent on every clone).
   - Run:

```bash
uv run .agents/skills/harness-profile-adapter/scripts/validate_tooling_link_policy.py --repo .
```

## Tooling context in OKF

Harness documentation belongs in `okf/wiki/tooling/`, not in extra `.agents/` folders.

Declare the hand-authored `tooling/` exception in `okf/wiki/INSTRUCTIONS.md` so OpenWiki preserves it. Keep local tooling pages out of producer input, and review each refresh before accepting it.

The link direction stays strict for concept pages:

```text
tooling context -> project context is allowed
project concept pages -> tooling context is forbidden
```

This means `okf/wiki/tooling/harnesses/<harness>.md` may mention `AGENTS.md`, `.agents/skills/`, or project OKF pages. Normal project concept pages must not depend on or link back to tooling pages.

The bundle-root `okf/wiki/index.md` is the deliberate exception: OKF navigation must enumerate the bundle, so when `okf/wiki/tooling/` contains pages, the root index **must** reference it — in its own clearly labeled section marking it as harness-specific context that project pages never depend on. Root `okf/wiki/log.md` may likewise record tooling changes. Without that index entry the bundle stops being spec-navigable; with more than that (deep links from concept pages), agents start treating interchangeable harness details as project truth. Keep exactly the index entry, nothing more.

Read `references/tooling-context-policy.md` before writing tooling pages.

## Runtime detection rule

Never conclude “the active harness is X” only because `x` is installed. A user can have multiple agents installed while running another harness.

Use `scripts/inspect_runtime_context.py` only to collect hints; it does not replace user confirmation when signals are ambiguous.

```bash
uv run .agents/skills/harness-profile-adapter/scripts/inspect_runtime_context.py --repo .
```

## Non-goals

Do not:

- create a portable subagent standard;
- create `.agents/profiles/` or other non-standard `.agents/` folders;
- hardcode vendor profile renderers;
- copy `okf/wiki/` content into profiles;
- make harness docs a project source of truth;
- patch vendor skills;
- commit harness-specific outputs without an explicit user or repo policy.
