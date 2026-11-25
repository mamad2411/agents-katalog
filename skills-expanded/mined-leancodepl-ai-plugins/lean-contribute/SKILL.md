---
name: lean-contribute
description: Walk a contributor through proposing a change to the LeanCode AI plugins marketplace — tweaking an existing plugin, adding a new one, and opening a PR against `leancodepl/ai-plugins`. Use when the user invokes `/lean-contribute`, asks how to contribute, asks how to add a plugin, or wants to propose an improvement. Manual-only entry point — does not auto-fire.
disable-model-invocation: true
---

# Contribute to LeanCode AI plugins

The guided contributor path for `leancodepl/ai-plugins`. The repo's `CONTRIBUTING.md` carries the same steps for contributors working without it. Read top-to-bottom for the full picture, or jump to the relevant path.

## How to respond

1. Ask what kind of change the user wants:
   - **Tweak** an existing plugin (improve a skill or reference, fix a typo, sharpen wording).
   - **Add a new plugin** (a new focused capability).
   - **Add a skill or reference** to an existing plugin.
2. Walk through the matching path below. Print exact commands. Do not run `git`, `gh`, or any state-changing command on the contributor's behalf unless they explicitly ask.
3. After the PR is pushed, point the user at `gh pr checks <pr-number>` to follow CI verdicts. CI is the source of truth.

## Reading the current state

Before answering questions about what plugins or clients exist, read the source of truth:

- Plugins: `.claude-plugin/marketplace.json` at the repo root.
- Supported clients: the "Supported clients" section of the root `README.md`.

Do not enumerate plugins or clients from memory.

## Where to work

All contribution work happens **inside a local clone of `leancodepl/ai-plugins`**, not in a consumer project. If the contributor does not have the clone yet:

```
gh repo clone leancodepl/ai-plugins
cd ai-plugins
```

If `gh` is not installed, point them at https://cli.github.com/ or, for a fully GUI flow, https://desktop.github.com/.

## Plugin shape

This repo ships Claude Code plugins. Every plugin lives under `plugins/<plugin-name>/`:

```
plugins/<plugin-name>/
  skills/
    <plugin-name>-usage/
      SKILL.md              # routing entry point, always present
      references/           # optional reference material the skill loads on demand
        <topic>.md
    <other-skill>/
      SKILL.md
  .claude-plugin/plugin.json
  README.md
  CHANGELOG.md
  .mcp.json                 # only if the plugin drives an MCP server
```

Notes:

- **`.claude-plugin/plugin.json` is the manifest.** It carries `name`, `displayName`, `description`, `version`, and points `skills` at `./skills/`. It has no `rules` key — Claude Code does not recognize one.
- **Every plugin ships `skills/<plugin-name>-usage/SKILL.md`** as its routing entry point. The skill `name:` in frontmatter must exactly match the folder name.
- **Skill names are unique across the whole marketplace.** If your slug could collide, prefix it with the plugin name.
- **Everything ships as a skill.** Use a workflow skill for a step-by-step action, and `references/*.md` alongside a `SKILL.md` for convention-style guidance the model should apply. Mark skills that should never auto-fire on inferred intent with `disable-model-invocation: true`.
- **Reference files are edited directly** — `SKILL.md` lists them under a "Reach for these references" section so Claude knows when to load each. They load only when referenced, so detailed material costs nothing until needed.
- **Setup and configuration docs have one canonical home: the plugin `README.md`.** Anything a user has to do to make the plugin work (env vars, dependencies, post-install steps, sample directories, MCP servers, etc.) lives there in full. Other surfaces — `<plugin>-usage/SKILL.md`, other skills, top-level README bullets — reference the plugin README rather than restating the setup. The single exception is a skill that needs to print setup inline at runtime (because the user is not on GitHub at that moment); when you keep an inline copy for that reason, say so in the skill so the next contributor does not assume the duplication is accidental. This rule prevents drift between `README.md`, the usage SKILL, and any workhorse SKILL that all happen to mention the same env var.

## Skill conventions

- Each skill is a folder `skills/<slug>/` containing a single `SKILL.md`.
- Frontmatter `name:` must equal the folder name.
- `description` should include "Use when …" with concrete trigger terms.
- Add `argument-hint: "<args>"` when the skill takes arguments.
- Add `disable-model-invocation: true` when the skill should never auto-fire on inferred intent.
- Skill names must be unique across the whole marketplace.

## Reference-material conventions

- Convention-style guidance lives in `skills/<plugin-name>-usage/references/*.md` as plain markdown (no frontmatter).
- List each reference file in the owning `SKILL.md` under a "Reach for these references" section, with a one-line note on what it covers, so Claude knows when to load it.
- A workhorse skill in the same plugin can cite a usage skill's reference with a relative path (e.g. `../<plugin-name>-usage/references/<topic>.md`).

## Path 1 — tweak an existing plugin

1. Open `plugins/<plugin-name>/` and find the file to change.
2. Edit it. Keep the change focused — one PR per concern.
3. Bump the plugin's `version` in `.claude-plugin/plugin.json`. PATCH for wording / docs, MINOR for new behavior, MAJOR for renames or removals. See "Versioning" below for what Claude Code does with the bump.
4. Add a bullet to `plugins/<plugin-name>/CHANGELOG.md` under a new top entry matching the new version.
5. Update `plugins/<plugin-name>/README.md` if the change affects what the plugin lists.
6. Branch, commit, push, open a PR — see "Open the PR" below.

## Path 2 — add a skill or reference to an existing plugin

Same as Path 1, plus:

- New skill → `plugins/<plugin-name>/skills/<skill-slug>/SKILL.md` with frontmatter `name: <skill-slug>` and a `description` that includes "Use when …" with concrete trigger terms. Add `disable-model-invocation: true` if it should not auto-fire. Also append the skill's plugin-relative path (e.g. `"./skills/<skill-slug>"`) to the plugin's `skills` array in `.claude-plugin/marketplace.json`.
- New reference → `plugins/<plugin-name>/skills/<plugin-name>-usage/references/<topic>.md` (plain markdown), and list it under "Reach for these references" in that `SKILL.md`.
- Mention the new asset in `plugins/<plugin-name>/README.md`.

## Path 3 — add a new plugin

1. Pick a kebab-case name with a prefix that reflects scope:
   - `flutter-<scope>` for a Flutter capability (the bulk of this marketplace).
   - `lean-<scope>` for a meta or repo-wide plugin with no natural domain (matches `lean-core`).

   Do not ship a bare slug. The prefix is what makes the marketplace listing predictable — users remember prefixes plus autocomplete, not full slugs.
2. Create `plugins/<plugin-name>/` with at minimum:
   - `skills/<plugin-name>-usage/SKILL.md`
   - `.claude-plugin/plugin.json`
   - `README.md`
   - `CHANGELOG.md` with a `0.1.0` entry
3. Copy manifest shape from a sibling plugin. Set `version: "0.1.0"`.
4. Register the plugin in `.claude-plugin/marketplace.json` — append to `plugins[]` with `name`, `source`, `description`, and a `skills` array listing every skill's plugin-relative path (e.g. `"./skills/<plugin-name>-usage"`).
5. Add the plugin to the human-readable overview in the root `README.md` under the matching group.
6. Branch, commit, push, open a PR.

## Versioning

Per-plugin semver in `.claude-plugin/plugin.json`.

- **PATCH** — wording, doc only.
- **MINOR** — new skill, new reference, new behavior; expanded scope; additive change.
- **MAJOR** — rename, removal, or reversal of existing guidance.

Keep `plugin.json` to fields in the official Claude Code plugin manifest schema — CI runs `claude plugin validate . --strict`, which fails on unrecognized fields.

### What Claude Code does with the version

`plugin.json.version` is the cache key for `/plugin update`. **Bumping it is load-bearing.** If you ship changes without bumping, users running `/plugin update` see "already at the latest version" and never get your change. Bump it on every release. (See https://code.claude.com/docs/en/plugins-reference.md, "Version management".)

`marketplace.json.metadata.version` is **decorative** — no documented refresh or update behavior. Bump by convention when plugins are added/removed/renamed if you want, but nothing depends on it.

Users get updates by running `/plugin update` (or auto-update if enabled) — no reinstall needed on a normal version bump.

## Open the PR

```
git checkout -b <short-slug>
git add -A
git commit -m "<plugin-name>: <what changed>"
git push -u origin HEAD
gh pr create --repo leancodepl/ai-plugins \
  --title "<plugin-name>: <what changed>" \
  --body "<one paragraph: what and why; mention any breaking changes>"
```

If `gh` is not installed, push the branch and open the PR via the GitHub web UI. The PR description should answer: what changed, why, and which plugins it touches.

## CI is the safety net

Every PR runs on GitHub Actions:

- **Structure** — manifest fields, marketplace registration, file shape and skill names (`go run ./cmd/validate-plugins`), plus the validator's own tests (`go test ./...`).
- **Spec** — the official Claude Code plugin-spec check (`claude plugin validate . --strict`, warnings fail the build).
- **Lint** — Go formatters/linters for repo tooling.

Contributors do not need to install Go locally — CI runs it. Watch the verdicts with:

```
gh pr checks <pr-number>
```

A green PR means the shape is correct. Review focuses on guidance quality, not boilerplate.

## What NOT to do

- Do not bundle changes across multiple plugins in a single PR. One plugin per PR keeps review tight.
- Do not ship a Claude Code-visible change without bumping `plugin.json.version` — see "Versioning" above.
- Do not invent guidance that is not grounded in real usage. If you cannot point at a concrete reason for a skill or reference claim, leave it out.
- Do not enumerate plugins or clients from memory — read the source of truth.
