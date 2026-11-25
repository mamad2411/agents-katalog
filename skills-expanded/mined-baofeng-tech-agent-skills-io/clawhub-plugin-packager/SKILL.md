---
name: clawhub-plugin-packager
description: "Package skills into publishable plugin or bundle formats for ClawHub, Claude marketplace, and related runtimes. Use when: converting a skill into a plugin or release bundle, generating manifests, and assembling a release-ready upload directory. Not for standalone metadata optimization or deep security auditing."
---

# Publish Plugin Packager

Package existing skills into standard, release-ready plugin or bundle formats for ClawHub, Claude marketplace, GitHub distribution, and related runtimes.

## When to use

- When converting an existing skill into a publishable plugin or bundle
- When generating or fixing manifests such as `package.json`, `.claude-plugin/plugin.json`, or `openclaw.plugin.json`
- When creating the final runtime-only directory and zip structure for upload or distribution
- When producing a release artifact from an already-optimized source skill

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

This skill does not own:

- primary search-copy optimization
- deep Suspicious/security auditing
- large runtime refactors beyond what packaging requires

## Packaging targets

Choose the artifact first:

- `runtime skill bundle`
  - for direct GitHub distribution or skill-layer publishing
  - keeps the skill directory itself as the primary artifact
- `ClawHub bundle plugin`
  - `.claude-plugin/plugin.json` plus minimal `package.json`
  - best for pure skill collections
- `ClawHub code plugin`
  - `openclaw.plugin.json` plus `package.json`
  - use when config schema, native extensions, or code entrypoints are required
- `Claude marketplace plugin`
  - `.claude-plugin/plugin.json` and marketplace-compatible layout
  - wraps an already-trimmed skill for Claude plugin distribution

## Source skill hard conventions

Before packaging, validate that the source skill follows these repository conventions:

- Published source skills should use `name`, `description`, and canonical `metadata.aisa`.
- `metadata.aisa` should normally contain `emoji`, `requires`, `primaryEnv`, and `compatibility`.
- Command examples should use `{baseDir}` rather than bootstrap-only variables.
- Package only runtime-essential files by default: `SKILL.md`, runtime scripts, libraries, manifests, and minimal wrappers.
- Exclude compare, evaluate, test, sync, migration, and dev utilities unless the user explicitly asks for a developer bundle.
- If the repo keeps a richer mother skill plus publish bundles, preserve the mother skill and trim only the publish bundles.
- Prefer repo-local config and data defaults over home-directory defaults when the packaged runtime persists files.
- If both EN and ZH variants are published, validate that both variants were trimmed with the same runtime and safety policy.

## Packaging workflow

1. Analyze the source skill and the target platform.
2. Determine the artifact type:
   - raw runtime bundle
   - ClawHub bundle plugin
   - ClawHub code plugin
   - Claude marketplace plugin
3. Normalize the shipped file set:
   - keep runtime files
   - drop caches, tests, sync scripts, and packaging-only helpers
4. Generate the correct manifests.
5. Preserve core skill semantics inside `skills/<skill-name>/`.
6. Validate the package layout and manifest fields.
7. Create a root-level release zip so required files sit directly at the zip root.

## Preserve core skill content

The content within `skills/<skill-name>/`, especially `SKILL.md`, should remain semantically intact during packaging. The packager may:

- remove non-runtime helpers from the release bundle
- trim caches, logs, and generated artifacts
- add platform manifests and wrapper files

The packager should not:

- silently rewrite the skill's core workflow
- introduce new auth paths
- broaden the runtime surface just to satisfy packaging convenience

## Real upload lessons

Recent real uploads were flagged for these concrete reasons:

1. External CLI execution inside shipped helpers
2. Self-install or cache-sync behavior
3. Default writes into user-home data locations
4. Version-swapping or repo-mutation helpers
5. Shipping non-runtime test/compare/sync utilities
6. Aggressive data-retention wording
7. Browser cookie, Keychain, or local credential access helpers
8. Legacy secret inputs left in runtime config

Required packager behavior:

- bundle only runtime-essential files by default
- exclude helper scripts that invoke external CLIs or mutate local installs
- prefer repo-local persistence when persistence is required
- do not include `__pycache__`, `.pytest_cache`, logs, debug artifacts, or non-text binaries in release zips
- exclude deprecated multi-provider auth paths from API-key-only bundles
- apply the same safety trimming to EN and ZH variants

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

- `Package this runtime skill as a ClawHub bundle plugin`
- `Wrap this release skill as a Claude marketplace plugin`
- `Trim this repo down to a publishable runtime bundle and zip it correctly`
- `Generate the manifests for this code plugin without changing the skill semantics`
