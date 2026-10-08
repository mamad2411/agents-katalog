---
name: bump-version
version: 0.1.0
description: >-
  Bumps the app release version (patch/minor/major/set) and keeps
  package.json, npm lock metadata, composer.json, and documented host
  overlays aligned. Use when the user asks to bump version, run
  /bump-version, or after shippable work when proposing a release bump.
---

# Bump Version

Keep the **app** release version in sync. This is not a dependency upgrade. Run from **project root**.

Read `CLAUDE.md` and `.cursor/PROJECT_CONTEXT.md` for extra sync paths.

## SemVer policy

| Kind | Example | When |
| ---- | ------- | ---- |
| **patch** | `1.3.2` → `1.3.3` | Bug fix, polish, small UX tweak, docs-only shippable fix |
| **minor** | `1.3.2` → `1.4.0` | New user-facing feature or notable surface |
| **major** | `1.3.2` → `2.0.0` | **Only when the user explicitly requests it** |

Do **not** bump for lint-only, rename-only, or unfinished WIP.

## Source of truth

1. `composer.json` `"version"` if that file exists and has a string version
2. Else root `package.json` `"version"`

Write the new version to every sync target that exists. See `reference.md`.

Dependency updates belong to `package-updater`.

## Commands

Prefer the host script:

```bash
./scripts/bump-version.sh patch
./scripts/bump-version.sh minor
./scripts/bump-version.sh major          # user-explicit only
./scripts/bump-version.sh set 1.4.0
./scripts/bump-version.sh --dry-run patch
```

If `./scripts/bump-version.sh` is missing, follow the fallback in `reference.md` (or copy the starter from this skill’s `scripts/bump-version.sh`).

## Agent workflow

### A) User invokes `/bump-version` or asks to bump

1. Confirm kind: `patch` | `minor` | `major` | exact `set x.y.z` (ask if unclear)
2. For **major**, require an explicit confirmation in this turn
3. Run the script (or fallback)
4. Report old → new version and synced files
5. After **minor** or **major** (or `set` that changes major.minor), remind `/write-changelog` if that command is installed
6. Do **not** commit unless asked

### B) End of shippable work (proactive)

After a meaningful, shippable change set:

1. Ask once: **Bump version?** → `patch` / `minor` / `skip` (never auto-major)
2. If they pick patch or minor, run the script
3. Skip the prompt for trivial edits, spikes, or when a bump already happened in this turn

## Do not

- Silently bump unless the user already named the kind (`/bump-version patch`, …)
- Edit only one manifest and leave the others stale
- Change `composer.json` `"version"` without refreshing `composer.lock`
- Treat `npm` / `yarn` / `composer require` as an app release bump
