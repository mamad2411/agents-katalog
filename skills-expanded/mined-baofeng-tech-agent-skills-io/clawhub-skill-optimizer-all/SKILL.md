---
name: clawhub-skill-optimizer-all
description: "Optimize publish-ready SKILL.md packages across ClawHub, Claude, Hermes, AgentSkill, AgentSkills.so, and GitHub. Use when: refining naming, frontmatter, body structure, bilingual copy, platform variants, and breakout positioning without changing runtime behavior."
---

# Publish Skill Optimizer

Optimize `SKILL.md`-based skills for public distribution across ClawHub, Claude, Hermes, AgentSkill, AgentSkills.so, GitHub, and related runtimes while preserving original runtime behavior.

## When to use

- When packaging or refining a skill for public distribution on ClawHub, Claude, Hermes, AgentSkill, AgentSkills.so, or GitHub
- When optimizing skill naming, frontmatter, and body structure for stronger discovery and invocation
- When generating bilingual English and Chinese variants
- When deciding how the source mother skill should differ from a platform-specific publish bundle
- When improving breakout positioning without rewriting runtime logic

## When NOT to use

- When the task is primarily about plugin manifests or marketplace wrappers; use `clawhub-plugin-packager`
- When the main task is auditing security or publish risk; use `clawhub-security-auditor`
- When editing business logic, API behavior, or runtime code beyond publish-surface alignment

## Scope boundary

This skill owns:

- naming and bilingual naming
- YAML frontmatter quality
- `SKILL.md` structure
- search discoverability and invocation wording
- publish-mode wording and section layout
- platform-specific publish variants
- breakout positioning and sibling-ladder separation
- review of previous breakout work before starting the next iteration
- candidate selection from existing AISA skills and top-ranked live skills when the task is breakout-oriented

This skill does not own:

- plugin manifest generation
- release zip assembly rules
- deep security/risk auditing
- broad runtime refactors

## Release modes

Choose the target mode before editing copy:

- `source mode`
  - canonical mother skill
  - keep portable, richer context
  - use canonical `metadata.aisa`
- `clawhub publish mode`
  - optimize for ClawHub search, upload safety, and parser compatibility
- `claude publish mode`
  - optimize for Claude Code readability, repo trust, and install clarity
- `hermes publish mode`
  - optimize for category/tag discovery and runtime-only clarity
- `agentskill publish mode`
  - optimize for quality review, security review, rating trust, GitHub proof, and platform coverage
- `agentskills-so publish mode`
  - optimize for weekly-download intent, GitHub trust, security posture, and reusable skill-catalog clarity
- `github release mode`
  - optimize for source trust, README clarity, and copy-paste installability

If one `SKILL.md` cannot satisfy all targets cleanly, generate separate publish variants instead of forcing a noisy compromise.

## Core principles

### 1. Selection happens on the description first

Most agents see `name` and `description` before they read the full body. Therefore the description must:

- say what the skill does in plain language
- contain `Use when:` or `触发条件：`
- include the exact task words users search for
- state the first useful outcome, not generic marketing

### 2. "Breakout" means clearer JTBD, not louder hype

Prefer:

- title = user task, system, or workflow surface
- first line = immediate user value
- examples = concrete, high-intent requests
- sibling skills = distinct jobs, not keyword overlap

Avoid:

- vague adjectives like `powerful`, `best`, `advanced`
- abstract names with no task signal
- making sibling skills compete for the same demand

### 3. Mother skill and publish bundle can differ

The source skill can stay richer and more portable. The publish bundle should only describe the shipped runtime and shipped files.

### 4. Breakout portfolios usually win as a ladder

Think in three layers:

- flagship skill
  - broad command center or command surface
- sibling skills
  - narrower, high-intent JTBD variants
- author factory
  - repeated naming logic, repeated trust logic, repeated install logic

### 5. Review the previous task before starting a new breakout push

Before making a new breakout edit, first check:

1. whether the previous task actually landed cleanly
2. whether there is doc/runtime drift to fix first
3. whether sibling skills are already competing for the same exact search surface

Do not stack a new breakout round on top of unresolved drift.

### 6. Breakout candidate selection should come from two lanes

When a task is about breakout retrofit or publish planning, default to these two lanes:

- `AISA-native upgrade lane`
  - choose an existing AISA-capable skill whose runtime is already valuable but whose naming, JTBD framing, or publish copy is weak
- `live-ranking retrofit lane`
  - choose a top-ranked live skill whose demand is already proven and adapt the job into an AISA-backed mother skill

Do not copy the branding shell blindly. Convert the underlying job only when it maps cleanly onto real runtime capability.

## Cross-platform ranking signals

### ClawHub

- plugin discovery now has separate downloads, installs, and stars boards, so names/descriptions should survive all three contexts
- exact keyword matches in `name`, `slug`, and `description` matter
- clear `Use when:` phrasing improves invocation fit
- type filters (`Code / Bundle`), trust filters (`Verified only`), and risk filters (`Executes code`) act like real pre-click ranking surfaces
- detail-page trust signals such as `Security Scan`, `VirusTotal`, `OpenClaw verdict`, `runtimeId`, and `source-linked` must agree with the package copy
- upload-safe wording and coherent metadata reduce trust friction

### Claude

- strong task titles and direct descriptions outperform abstract names
- repo trust, stars, installs, and example readability affect adoption
- marketplace/plugin packaging is evaluated partly by how clearly one repo represents one lane
- the publish copy should match the shipped runtime exactly

### Hermes

- category and tag clarity matter more than broad marketing copy
- section fit and workflow boundary clarity matter more than “heat” because Hermes is atlas-first, not download-first
- runtime-only, community-safe wording is important

### AgentSkill

- quality score is shaped by discovery, implementation, structure, and expertise
- security score, audit freshness, and issue severity influence trust immediately
- GitHub stars, platform coverage, and rating reinforce cold-start confidence
- owner pages and plugin families compound trust, so the skill should read clearly as part of a wider ladder

### AgentSkills.so

- weekly downloads are a visible demand signal, so titles must read like a real job-to-be-done
- GitHub repo trust and author continuity strongly affect cold-start confidence
- security posture is part of the public surface, so vague claims and unclear boundaries hurt ranking
- trust surfaces such as `Trust & Identity`, `Behavioral Monitoring`, `Vulnerability Exposure`, and distribution coverage should be reinforced by the shipped docs
- search-page wording and detail-page wording should describe the same narrow workflow

### GitHub

- README trust, install clarity, examples, and visible source proof matter
- publish bundles should not advertise files or flows that are not shipped

## Hard publish conventions

When optimizing a published repo skill, enforce these before polishing copy:

- if the skill already exists in `AIsa-team/agent-skills`, diff against that upstream skill first and treat `agentskills` as the default runtime baseline
- preserve runtime functionality unless the task explicitly asks for a behavior change
- use minimal frontmatter with `name`, `description`, and canonical `metadata.aisa`
- prefer `metadata.aisa.emoji`, `metadata.aisa.requires`, `metadata.aisa.primaryEnv`, and `metadata.aisa.compatibility`
- every command example should use `{baseDir}` when a runtime placeholder is needed
- keep `SKILL.md` aligned to the shipped runtime only
- if compare/test/sync/dev scripts are not in the publish artifact, do not mention them
- if EN and ZH variants exist, keep the same runtime surface area, command layout, and section structure

## Recommended body structure

Choose only the modules that help the shipped runtime:

- `When to use`
  - always include
- `When NOT to use`
  - include when sibling skills exist
- `Quick Reference`
  - include for CLI-first skills
- `Capabilities`
  - include for multi-function skills
- `High-Intent Workflows`
  - include when there are multiple top jobs-to-be-done
- `Inputs and Outputs`
  - include when the interface is structured
- `Example Requests`
  - include when discovery matters
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

## Breakout packaging heuristics

Before publishing, sanity-check whether the copy creates a true breakout surface:

1. Could a user search for this title directly?
2. Does the first line say what is done, for whom, and when?
3. Is the skill narrow enough to be memorable?
4. Is there proof, trust, or concrete result language?
5. Does this skill have a clear relationship to the rest of the author's portfolio?

## Breakout execution additions

Use these additions when the task is not just polish, but selecting or redesigning breakout candidates.

### Candidate-lane defaults

If market evidence is close, prefer these lanes:

1. Developer
2. Search and Research
3. Documents
4. Workspace
5. Automation
6. Security
7. Finance and Market Data

Treat Apple/macOS-local-only flows as premium side SKUs, not universal flagships.

### Role assignment

For each candidate, assign one role before editing copy:

- `flagship`
  - broad command-center or broad workflow surface
- `growth variant`
  - narrower, high-intent sibling that expands the same family
- `supporting sibling`
  - useful but intentionally smaller support lane that should not compete with the flagship

### Mother-skill rewrite checklist

When breakout work happens in a mother skill, make sure you review and, when needed, rewrite:

- `name`
- `description`
- `metadata.aisa`
- `Use when:` or `触发条件：`
- example requests
- permissions, persistence, and side-effect wording
- sibling overlap and portfolio separation

### `agent-skills-io` usage

When using this skill inside `agent-skills-io` for breakout work:

1. Read `PROJECT_OVERVIEW.md`, `README.md`, `targets/platform-skill-plugin-methodology.md`, and `targetSkills/PUBLISHING.md`.
2. Treat `targetSkills/` as the mother-skill source of truth.
3. Pull evidence from `../skillGet/reports/` and `../skillGet/public/data/`.
4. Default to at least one AISA-native upgrade and one live-ranking retrofit.
5. Regenerate the release layers after the mother-skill edit.
6. Hand off to packager and auditor skills before publish.

## 2026-04-20 live market lessons

### AgentSkill

- owner-page portfolios matter almost as much as the single skill card
- discovery improves when the first line names the system, task, and output clearly
- quality/security trust must be visible in the copy, not left implicit
- flagship skill + sibling ladder + coherent plugin family is more durable than one-off releases

### AgentSkills.so

- weekly-download competition rewards concrete task naming over abstract capability branding
- repo-backed skills with narrow scope and clearer security boundaries travel further
- authors who repeat one lane across multiple skills accumulate trust faster than broad generalists
- strong publish copy should sound like a reusable product surface, not an internal helper

## Validation checklist

Before publishing, verify:

1. Frontmatter is valid and machine-readable.
2. `name` is short, keyword-rich, and platform-appropriate.
3. `description` contains `Use when:` or `触发条件：`.
4. The skill body matches the shipped runtime and shipped files.
5. Required env vars and binaries are declared in `metadata.aisa`.
6. EN and ZH variants have parallel runtime scope.
7. The optimization changed wording and packaging clarity, not core runtime semantics.
8. Sibling skills do not compete for the same exact positioning.
9. Platform-specific proof signals are visible where needed: repo trust, audit posture, category/tag fit, or bilingual search fit.

## Lightweight publish-risk reminders

While this skill is not a full auditor, always avoid obvious publish regressions:

- do not advertise password, cookie, or browser-credential flows
- do not describe non-runtime helper scripts as part of normal usage
- do not default to home-directory persistence in public bundles
- do not claim functionality that only exists in source/dev tooling
- do not hide relay targets, upload paths, OAuth steps, or other real side effects behind vague wording
- do not let public `SKILL.md` text read like prompt injection, internal scaffold leakage, or autonomous override instructions
- do not let env requirements drift between `SKILL.md`, README, manifests, and registry-facing metadata
- do not let AgentSkill or marketplace copy promise a quality/security/platform story the bundle cannot support
- do not let AgentSkills.so copy imply demand, trust, or security posture the bundle cannot actually support

## Example requests

- `Optimize this skill for ClawHub search and upload`
- `Turn this mother skill into source mode plus Hermes publish mode`
- `Rewrite the SKILL.md so Claude, AgentSkill, and AgentSkills.so versions each read cleanly`
- `Make these EN/ZH variants consistent and more high-intent without changing runtime behavior`

## 2026-04-25 suspicious-aware copy lessons

- relay-based skills need explicit trust wording for keys, uploads, and remote targets
- prompt-heavy public instructions can be scanned as prompt-injection even when runtime code is harmless
- clean packaging still loses trust when registry metadata omits a required env var already declared in the bundle
- pending live scan output is not the same thing as a clean verdict
