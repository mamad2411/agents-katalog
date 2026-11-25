---
name: clawhub-skill-optimizer
description: "Optimize publish-ready SKILL.md packages across ClawHub, Claude, Hermes, and GitHub. Use when: refining naming, frontmatter, body structure, bilingual copy, and release-mode variants without changing runtime behavior. Not for plugin manifest generation or deep security auditing."
---

# Publish Skill Optimizer

Optimize SKILL.md-based skills for public distribution across ClawHub, Claude, Hermes, GitHub, and related runtimes, while preserving the original runtime behavior.

## When to use

- When packaging or refining a skill for public distribution on ClawHub, Claude, Hermes, or GitHub
- When optimizing skill naming, frontmatter, and body structure for better search discoverability and agent invocation
- When generating bilingual English and Chinese variants
- When deciding how a mother skill should differ from a platform-specific publish bundle
- When improving first-turn clarity, task framing, and "爆款化" positioning without rewriting runtime logic

## When NOT to use

- When the task is primarily about plugin manifests or marketplace wrappers; use `clawhub-plugin-packager`
- When the main task is auditing security or Suspicious/upload risk; use `clawhub-security-auditor`
- When editing business logic, API behavior, or runtime code beyond what is needed for publish-surface alignment

## Scope boundary

This skill owns:

- skill naming and bilingual naming
- YAML frontmatter quality
- `SKILL.md` structure
- publish-mode wording and section layout
- search discoverability and invocation wording
- deciding between source-skill and platform-release variants

This skill does not own:

- plugin manifest generation
- release zip assembly rules
- deep security/risk auditing
- broad runtime refactors

## Release Modes

Choose the target mode before editing copy:

- `source mode`
  - canonical mother skill in `targetSkills/`
  - keep cross-platform structure
  - prefer `metadata.aisa` as the source of truth
- `clawhub publish mode`
  - optimize for ClawHub search, parser compatibility, and low-risk upload wording
  - prefer short high-intent descriptions and conservative publish surfaces
- `claude publish mode`
  - optimize for Claude Code / skills.sh readability and direct invocation
  - remove references to files or commands not shipped in the release bundle
- `hermes publish mode`
  - optimize for Hermes category/tag discovery, runtime-only packaging, and community-safe wording

If one `SKILL.md` cannot satisfy all targets cleanly, generate separate publish variants rather than forcing a single noisy compromise.

## Core principles

### 1. Selection happens on the description first

Agents usually see `name` and `description` before they read the full body. The description must therefore:

- say what the skill does in plain language
- contain the trigger phrase `Use when:` or `触发条件：`
- include the exact task words a user would actually search for
- state the first useful outcome, not generic marketing

### 2. "爆款化" means clearer task framing, not hype

When improving a public skill, prefer:

- title = user task, not internal project codename
- first line = immediate user value
- examples = concrete, high-intent requests
- family positioning = each sibling skill owns a distinct job instead of keyword overlap

Avoid:

- generic adjectives like `powerful`, `best`, `advanced`
- vague platform bragging
- making multiple sibling skills compete for the same exact positioning

### 3. Mother skill and publish bundle can differ

The source skill can stay richer and more portable. The publish bundle should only describe the shipped runtime and shipped files.

## Hard repository conventions

When optimizing a published repo skill, enforce these before polishing copy:

- Use minimal frontmatter with `name`, `description`, and canonical `metadata.aisa`.
- Prefer `metadata.aisa.emoji`, `metadata.aisa.requires`, `metadata.aisa.primaryEnv`, and `metadata.aisa.compatibility`.
- Do not leave legacy fields like `argument-hint`, `allowed-tools`, `user-invocable`, `homepage`, or `repository` in a published skill unless the target platform truly requires them.
- Every command example must use `{baseDir}` when a runtime placeholder is needed.
- Keep `SKILL.md` aligned to the shipped runtime only. If compare/test/sync/dev scripts are not in the publish artifact, do not mention them.
- For Python skills, prefer stdlib-first runtime bundles. Do not describe `requests`, `httpx`, `uv`, or `pyproject.toml` as required unless the shipped runtime truly depends on them.
- If the repo contains a richer mother skill plus slimmer publish bundles, optimize the publish bundles and do not strip the mother skill's developer workflows.
- In stateless publish bundles, remove references to watchlists, recurring briefings, SQLite accumulation, or long-lived schedulers unless they intentionally ship.
- If a feature depends on side-channel auth such as direct GitHub tokens and is not core to the publish runtime, remove it from publish copy instead of advertising split-auth behavior.
- If EN and ZH variants exist, keep the same runtime surface area, safety trimming, command layout, and section structure across both.

## Recommended body structure

Choose only the modules that help the shipped runtime:

- `When to use`
  - always include
- `When NOT to use`
  - include when nearby sibling skills exist
- `Quick Reference`
  - include for CLI-first skills
- `Capabilities`
  - include for multi-function skills
- `High-Intent Workflows`
  - include when the skill has multiple high-value user jobs
- `Inputs and Outputs`
  - include when the interface is structured
- `Example Requests`
  - include when search/discovery matters
- `Setup`
  - include only what the published runtime actually needs

## Description rules

Preferred English pattern:

```text
[Core task]. Use when: [trigger]. Supports [important outcomes].
```

Preferred Chinese pattern:

```text
[核心任务]。触发条件：当用户需要[场景]时使用。支持[关键结果]。
```

Description quality checklist:

- 50-200 characters when possible
- no angle brackets `<>`
- exact task keywords present
- no marketing fluff
- no undocumented dependencies

## Validation checklist

Before publishing, verify:

1. Frontmatter is valid and machine-readable.
2. `name` is short, keyword-rich, and appropriate for the platform.
3. `description` contains `Use when:` or `触发条件：`.
4. The skill body matches the shipped runtime and shipped files.
5. Required env vars and binaries are declared in `metadata.aisa`.
6. EN and ZH variants have parallel runtime scope.
7. The optimization changed wording and packaging clarity, not core runtime semantics.
8. Sibling skills do not compete for the same exact positioning.

## Lightweight publish-risk reminders

While this skill is not a full auditor, always avoid obvious publish regressions:

- do not advertise password, cookie, or browser-credential flows
- do not describe non-runtime helper scripts as part of normal usage
- do not default to home-directory persistence in public bundles
- do not claim functionality that only exists in source/dev tooling

## Example requests

- `Optimize this skill for ClawHub search and upload`
- `Turn this mother skill into source mode plus Hermes publish mode`
- `Rewrite the SKILL.md so Claude and Hermes versions each read cleanly`
- `Make these EN/ZH variants consistent and more high-intent without changing runtime behavior`
