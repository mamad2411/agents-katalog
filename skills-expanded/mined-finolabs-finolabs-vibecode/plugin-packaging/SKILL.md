---
name: plugin-packaging
description: Package agent skills as one plugin for Claude Code, Codex and Antigravity. Use when creating or restructuring a plugin or skill repository, fixing a manifest or catalog, writing or reviewing its README, designing its icon or listing metadata, adding a host, or validating it before a release or directory submission.
---

# Plugin packaging

One repository, one `skills/` folder, one manifest per host. This skill holds the decisions that stay stable across hosts. Field-level schemas change often, so read them from each host's own tools and docs at the time you package (the **authority** column below) instead of copying them into the repository.

| Host | Manifest | Catalog | Authority for fields and checks |
| --- | --- | --- | --- |
| Claude Code | `.claude-plugin/plugin.json` | `.claude-plugin/marketplace.json` | [plugin manifest reference](https://code.claude.com/docs/en/plugins/manifest-reference.md), [marketplace reference](https://code.claude.com/docs/en/plugins/marketplace-reference.md), `claude plugin validate . --profile directory --strict` (well-formedness only: the directory portal's **Validate** runs more checks); the `plugin-dev` and `skill-creator` skills for authoring |
| Codex | `.codex-plugin/plugin.json` | `.agents/plugins/marketplace.json` | [build plugins](https://developers.openai.com/codex/plugins/build), [submission fields](https://developers.openai.com/plugins/deploy/submission); no local validator, the portal validates the upload |
| Antigravity | `.antigravity-plugin/plugin.json` | none; install from the repository URL | [build plugins](https://antigravity.google/docs/build-plugins), `agy plugin validate . --strict`; the built-in `plugin` and `agy-customizations` skills |

## 1. Layout

- Skills live in `skills/<name>/SKILL.md`; the folder name equals the `name` field. A shared name prefix keeps a pack's skills together and avoids collisions with other packs.
- Each host's manifest sits in its own folder. A root `plugin.json` is read by both Codex (its preferred location) and Antigravity (its native manifest, with a closed schema), so one file cannot satisfy both.
  Hooks shared by Claude Code and Codex stay in shell form. Claude Code's exec form (`"command": "node", "args": ["${CLAUDE_PLUGIN_ROOT}/…"]`, no shell) has no Codex counterpart: Codex hook handlers take one `command` string and no `args`, and expose `PLUGIN_ROOT` and `CLAUDE_PLUGIN_ROOT` as environment variables. To use exec form on Claude Code, give Codex its own hooks file through the `hooks` field of its manifest, which replaces Codex's default `hooks/hooks.json` ([Claude Code hooks](https://code.claude.com/docs/en/hooks.md), [Codex hooks](https://learn.chatgpt.com/docs/hooks)).
- Keep every skill folder self-contained: single-skill installers (skills.sh) copy one folder and nothing around it. Disclose reference material into `references/` and executables into `scripts/` beside the skill that uses them; a file two skills need gets a copy in each, with a CI check that the copies match. A skill that cannot work without another names it as a dependency and says how to install it. Keep machine-specific facts in user configuration, never in the package.
- Ship only what the host loads: no build output, caches, OS files, local notes or eval results.

Done when every host's validator finds the expected number of skills.

## 2. Manifests

- Fill the identity fields consistently on every host: `name` (kebab-case, no host or vendor name as a prefix), display name, description, version, author, homepage, repository, license (SPDX).
- **Version**: one manifest is the source of truth and the others copy it; CI fails when they differ. Bumps, tags and the changelog follow `versioning`.
- **Description**: what the plugin does and for whom, in the length each host recommends (Antigravity suggests 120–160 characters; Codex limits its short description to 30).
- **Listing metadata**: icon, documentation, support, privacy and terms URLs where the host reads them (Claude's directory fields, Codex's `interface` block). URLs point at files that exist in the public repository.

## 3. Skill frontmatter across hosts

- `name` and `description` are the portable core. The description carries the triggers: what the skill does, then each distinct case that should fire it.
- Claude Code also reads keys such as `disable-model-invocation`, `user-invocable` and `argument-hint`; other hosts ignore them, but a claude.ai skill upload rejects them. Keep that in mind before offering a skill as a standalone upload.
- A skill the human should start by hand (a setup or a router) sets `disable-model-invocation: true`, which removes its description from the agent's context. Hosts that ignore the key still list it, so its description also says to run it only when the user asks for it. Another skill then tells the human to type it rather than calling it.

## 4. Icon

Apply this section only when preparing a submission to a directory that asks for an icon; a plugin installed straight from its repository needs none of it.

- Square, transparent canvas, one simple glyph that reads at 32 px, in the project's brand family (stroke width, corner style, light and dark colors from the project's brand tokens).
- Light and dark variants with identical geometry. Keep the SVG sources and export 512 × 512 transparent PNGs; some directories accept only PNG.
- An `assets/NOTICE.md` records the concept, the owner's approval, that no third-party artwork or image-model output is included, and the SHA-256 of each file.
- The owner approves the design. Show variants side by side on light and dark backgrounds at full size and at 32 px.

## 5. Distribution

- Make the repository its own marketplace on hosts that use catalogs when the plugin is outside any family catalog, so `owner/repo` installs work before any directory listing; inside a family, install from the shared catalog (Codex shows each marketplace as its own group).
- A family of plugins shares one catalog repository serving every host that uses catalogs; it either pins each plugin by commit SHA or tracks protected default branches, and says which; details in [references/catalogs.md](references/catalogs.md), which also covers Antigravity's install from the repository URL.
- Offer single-skill installs beside the plugin: skills.sh (`npx skills add owner/repo --skill <name>`) finds `skills/<name>/SKILL.md` on its own. Tell users to pick one path per agent, since both list every skill twice.
- Write the README to [references/readme.md](references/readme.md): its sections in order, the facts it takes from the repository, and the install commands for every host, verified against each host's `--help`.
- Before preparing a submission to Anthropic's or OpenAI's plugin directory, read [references/directories.md](references/directories.md): which portal steps need the owner's approval, per-directory editions built from one source, and what each directory refuses or holds that no local validator shows.

## 6. Checks before a release

Run and read each one:

- every host validator above, strict where available, on each rebuilt directory edition too; the portal's own validation uploads the package, so it waits for the owner's approval and stays pending in the report until then;
- the trigger suite: one `claude plugin eval` case per model-invoked skill that must fire it, plus negative cases that must fire nothing (`--ablation none` keeps `Skill` graders scored). Run only the cases of skills whose `description` changed since the last release (`--case`), and the whole suite before a MINOR release; a patch release with no `description` change needs none;
- after installing on Claude Code, `/skill-doctor` for each skill's listing cost, and from the second release on, whether it is ever used (an interactive check: where it cannot run, say so);
- `open-source-review` for license, payload, leaks and community files, then the README checklist in [references/readme.md](references/readme.md) "Checklist": `scripts/readme_check.py` for the mechanical items (advisory: it reads files only) and the agent items; fix each failure in the release pull request or write there, per item, why not;
- when the plugin is listed in a shared catalog, run the catalog check and, if the catalog pins SHAs, update it after the tag.

A validator pass shows the package loads; only the trigger suite and real use show the skills help.

## Authority

Creating a marketplace repository, any directory portal step (upload, draft, repository access, portal validation, submitting), tagging and publishing need the owner's explicit approval. Preparing manifests, icons, editions and local checks needs none. A directory form's answers, attestations and acknowledgements are the owner's; when one conflicts with what the plugin does, show the owner the conflict.
