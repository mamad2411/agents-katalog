---
name: publish-caeros-plugin
description: How to publish a Caeros plugin: packaging it in a git repo (root or plugins/ subdir), letting users add that repo as a marketplace by git URL, and shipping first-party plugins through the caeros-official marketplace and the hosted registry. Use when a plugin is built and needs to be distributed.
---

# Publishing a Caeros Plugin

Distribution is git-native: a plugin ships as a directory in a git repository, and users install from that repository. There is no build or bundling step; what is in the repo is what installs.

## 1. Package the plugin in a git repo

Two supported layouts:

- **Repo root**: the repository itself is the plugin. `.caeros-plugin/plugin.json` sits at the repo root next to `skills/`, `commands/`, `assets/`. Best for a single plugin with its own home.
- **plugins/ subdirectory**: one repository hosts many plugins, each in its own folder under `plugins/` (e.g. `plugins/my-plugin/.caeros-plugin/plugin.json`). Best for a team's shared collection, since one URL serves them all.

Before pushing:

- Validate the manifest: `python3 -m json.tool .caeros-plugin/plugin.json` (and `.mcp.json` if present).
- Make sure declared capability paths exist; a missing `skills/` directory installs as a plugin that does nothing.
- Never commit secrets: bundled MCP configs must reference secret names via `permissions.secrets`, not embed values.
- Tag releases if you want users on stable snapshots; the manifest `version` field is what users see.

## 2. Distribution as a marketplace (git URL)

Any git repository laid out as above can be added by users as a plugin marketplace inside Caeros: they add the repo's git URL in the Caeros plugins UI, and every plugin the repo contains becomes installable. This is the path for team-internal and community plugins:

- Private repos work with whatever git credentials the user's machine already has.
- Updating the plugin is `git push`; users pull updated plugin versions through the same marketplace entry.
- Share the URL, not an archive; the repo is the single source of truth.

## 3. First-party distribution

First-party (Caeros-authored) plugins ship through two official channels:

- **caeros-official marketplace**: the repository at `github.com/Caerosinc/caeros-plugins`, preconfigured in the product. Landing a plugin there means opening a PR against that repo with the plugin in its own directory, passing review, and merging. Users see it without adding any URL.
- **Hosted registry**: the Caeros-hosted registry indexes published plugins for in-product search and install, including storefront presentation from the manifest `interface` block (display name, descriptions, category, logo, screenshots, default prompts). Complete that block carefully before submitting; it is the listing.

For first-party submissions, expect review to check: manifest validity, minimal permissions, an original logo (no third-party trademarks), accurate storefront copy, and that skills and commands follow the conventions in the create-caeros-plugin skill.

## Publishing checklist

1. Manifest and .mcp.json validate with `python3 -m json.tool`.
2. Layout matches one of the two supported shapes (root or plugins/ subdir).
3. `version` bumped, release tagged if applicable.
4. No secrets in the repo; permissions minimal and accurate.
5. `interface` block complete: displayName, descriptions, category, developerName, logo.
6. Installed and smoke-tested locally from a fresh clone before announcing.
