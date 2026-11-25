---
name: clawhub-plugin-packager-all
description: "Package skills into publishable plugin or bundle formats across ClawHub, Claude, Hermes, AgentSkill, AgentSkills.so, and GitHub. Use when: converting a skill into a release plugin, generating manifests, trimming runtime-only files, and assembling a breakout-ready upload artifact."
---

# Publish Plugin Packager

Package existing skills into standard, release-ready plugin or bundle formats for ClawHub, Claude, Hermes, AgentSkill, AgentSkills.so, GitHub, and related runtimes.

## When to use

- When converting an existing skill into a publishable plugin or bundle
- When generating or fixing manifests such as `package.json`, `.claude-plugin/plugin.json`, or `openclaw.plugin.json`
- When creating the final runtime-only directory and zip structure for upload or distribution
- When producing a release artifact from an already-optimized source skill
- When shaping the package so it can compete better in public plugin directories

## When NOT to use

- When the deliverable is only a `SKILL.md` optimization; use `clawhub-skill-optimizer`
- When the main task is auditing upload risk; use `clawhub-security-auditor`
- When the main work is rewriting runtime behavior rather than packaging it

## Scope boundary

This skill owns:

- plugin or bundle directory structure
- manifest generation
- release layout and zip shape
- packaging validation
- runtime-only file trimming
- platform-aware breakout packaging rules

This skill does not own:

- primary search-copy optimization
- deep Suspicious/security auditing
- large runtime refactors beyond what packaging requires

## Packaging targets

Choose the artifact first:

- `runtime skill bundle`
  - for direct GitHub distribution or skill-layer publishing
- `ClawHub bundle plugin`
  - `.claude-plugin/plugin.json` plus minimal `package.json`
- `ClawHub code plugin`
  - `openclaw.plugin.json` plus `package.json`
- `Claude marketplace plugin`
  - `.claude-plugin/plugin.json` and marketplace-compatible layout
- `Hermes runtime bundle`
  - runtime-only skill directory with Hermes-safe copy and structure
- `AgentSkill publish bundle`
  - runtime-only bundle optimized for quality/security review, platform labels, and GitHub trust proof
- `AgentSkills.so publish bundle`
  - runtime-only bundle optimized for weekly-download intent, GitHub trust, and reusable catalog-style clarity

## Cross-market breakout packaging rules

### 1. Package for trust, not just parser correctness

Public users install plugins only when the package feels coherent:

- name, description, manifests, and README must describe the same thing
- side effects must be visible
- source repo and shipped files must agree
- only runtime files should ship

### 2. Package one sharp JTBD per artifact

Breakout plugins usually win because each artifact has a tight job:

- one system
- one operational surface
- one clear result

### 3. Package a flagship plus a sibling ladder

The best public creators rarely stop at one package. Prefer:

- flagship package
  - broad command center or broad plugin surface
- sibling packages
  - narrower high-intent actions or adjacent workflows

### 4. Package proof and install clarity

Strong public packages usually include:

- coherent manifest fields
- runtime-only files
- README proof of what the package actually does
- trustworthy install/setup steps
- clear scope boundaries

## Platform-specific packaging heuristics

### ClawHub

- package for all three public plugin boards: downloads, installs, and stars
- keep bundle vs code-plugin boundaries crisp
- make `runtimeId`, capabilities, and README match exactly
- prefer source-linked, coherent, scanner-friendly bundles
- make detail-page trust surfaces easy to verify: `Security Scan`, `VirusTotal`, `OpenClaw verdict`, compatibility, and capabilities should all tell the same story
- describe concrete side effects such as config writes, gateway restarts, or remote fetches

### Claude

- prefer clean repo-backed layouts and example-driven READMEs
- repo identity should make the lane obvious even before the user reads the whole bundle
- marketplace bundles should read clearly without relying on out-of-bundle files

### Hermes

- optimize for category/tag clarity and runtime-only contents
- package one workflow unit per bundle so the section/path choice stays obvious
- avoid noisy install or dev sections in the publish bundle

### AgentSkill

- quality score, security score, rating, GitHub stars, and platform coverage become part of the packaging surface
- package so reviewers can see discovery, implementation, structure, and expertise clearly
- think about the owner page and sibling plugin family too, not just one isolated listing
- preserve source linkage and README coherence when GitHub is the trust anchor

### AgentSkills.so

- weekly-download competition rewards narrow JTBD packaging and clear repo-backed proof
- package so the detail page can express one reusable workflow, not a fuzzy toolkit
- make security boundaries, side effects, and setup expectations obvious in shipped docs
- strong repo continuity and author-family logic help sibling packages travel further

### GitHub

- package as a trustworthy source release, not a local workspace snapshot
- keep changelog/provenance/readme/install paths aligned

## Source skill hard conventions

Before packaging, validate that the source skill follows these conventions:

- if the skill already exists in `AIsa-team/agent-skills`, diff against that upstream skill first and treat `agentskills` as the default runtime baseline
- preserve complete runtime behavior unless the task explicitly asks for a behavior change
- published source skills should use `name`, `description`, and canonical `metadata.aisa`
- `metadata.aisa` should normally contain `emoji`, `requires`, `primaryEnv`, and `compatibility`
- command examples should use `{baseDir}` rather than bootstrap-only variables
- package only runtime-essential files by default
- exclude compare, evaluate, test, sync, migration, and dev utilities unless the user explicitly asks for a developer bundle
- preserve the richer mother skill when the repo uses separate publish bundles

## Packaging workflow

1. Analyze the source skill and the target platform.
2. Determine the artifact type.
3. Normalize the shipped file set.
4. Generate the correct manifests.
5. Preserve core skill semantics inside `skills/<skill-name>/`.
6. Validate the package layout and manifest fields.
7. Create a root-level release zip so required files sit directly at the zip root.

## Preserve core skill content

The content within `skills/<skill-name>/`, especially `SKILL.md`, should remain semantically intact during packaging. The packager may:

- remove non-runtime helpers from the release bundle
- trim caches, logs, and generated artifacts
- add platform manifests and wrapper files
- add packaging metadata that improves trust and publish clarity

The packager should not:

- silently rewrite the skill's core workflow
- introduce new auth paths
- broaden the runtime surface just to satisfy packaging convenience

## Real upload lessons

Recent real uploads were flagged for these reasons:

1. External CLI execution inside shipped helpers
2. Self-install or cache-sync behavior
3. Default writes into user-home data locations
4. Version-swapping or repo-mutation helpers
5. Shipping non-runtime test/compare/sync utilities
6. Aggressive data-retention wording
7. Browser cookie, Keychain, or local credential access helpers
8. Legacy secret inputs left in runtime config
9. Relay targets, upload behavior, or OAuth side effects described too vaguely
10. Registry/manifest env requirements drifting away from the shipped skill files
11. Public `SKILL.md` wording that looks like prompt injection or internal prompt scaffolding

Required packager behavior:

- bundle only runtime-essential files by default
- exclude helper scripts that invoke external CLIs or mutate local installs
- prefer repo-local persistence when persistence is required
- do not include `__pycache__`, `.pytest_cache`, logs, debug artifacts, or non-text binaries in release zips
- exclude deprecated multi-provider auth paths from API-key-only bundles
- apply the same safety trimming to EN and ZH variants
- make relay destinations, uploads, OAuth, and external writes explicit in shipped docs and manifests
- make env requirements match across `SKILL.md`, README, manifests, and registry-facing metadata
- keep suspicious scan states distinct: `pending`, `clean`, and `suspicious` are different package states

## Plugin breakout lessons from live ClawHub plugin analysis

As of 2026-04-23, ClawHub plugin pages expose separate downloads / installs / stars boards, but public numeric detail is still weaker than the ranking surface itself. Packaging should therefore emphasize:

- task-first or system-first titles
- relevance across all three public boards
- explicit side effects and setup expectations
- strong verification surfaces such as source-linked provenance
- code-plugin clarity when real runtime behavior exists
- family logic that supports a flagship plugin plus narrower siblings

Public packaging now needs to carry part of the growth strategy.

## Additional breakout lessons from 2026-04-20 AgentSkill / AgentSkills.so analysis

### AgentSkill

- skill cards, owner portfolios, and plugin families are all part of the packaging surface
- installs, quality score, security score, and GitHub trust should be reinforced by the shipped README, not left to the listing alone
- flagship package plus narrower siblings is more durable than one giant undifferentiated bundle

### AgentSkills.so

- weekly-download winners usually package one reusable workflow with a concrete name and clear repo proof
- security posture is part of the public conversion surface, so packaging should reduce ambiguity about persistence, permissions, and side effects
- detail-page trust surfaces should be reinforced in the shipped README, not left implicit
- bundles should feel like clean product surfaces, not snapshots of internal workspace clutter

## Layout rules

### ClawHub bundle plugin

```text
plugin-name/
├── .claude-plugin/
│   └── plugin.json
├── package.json
├── skills/
│   └── skill-name/
│       ├── SKILL.md
│       └── ...
└── README.md
```

### ClawHub code plugin

```text
plugin-name/
├── openclaw.plugin.json
├── package.json
├── skills/
│   └── skill-name/
│       └── SKILL.md
└── README.md
```

### Claude marketplace plugin

```text
plugin-name/
├── .claude-plugin/
│   └── plugin.json
├── package.json
├── skills/
│   └── skill-name/
│       ├── SKILL.md
│       └── ...
└── README.md
```

## Zip rule

The release zip should place `package.json`, manifests, `skills/`, and other required root files directly at the root of the archive, not inside an extra `package/` folder.

## Example requests

- `Package this runtime skill as a ClawHub code plugin`
- `Wrap this release skill as a Claude marketplace plugin`
- `Trim this repo down to a publishable AgentSkill or AgentSkills.so bundle and zip it correctly`
- `Generate the manifests for this plugin without changing the skill semantics`
