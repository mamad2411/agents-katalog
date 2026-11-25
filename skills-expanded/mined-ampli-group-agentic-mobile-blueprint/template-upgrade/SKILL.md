---
name: template-upgrade
description: Upgrade a project that is based on the agentic-mobile-blueprint template. Use when the user asks to check for template updates, upgrade to a newer version, or apply template changes.
---

# Template Upgrade

This project is based on [agentic-mobile-blueprint](https://github.com/Ampli-Group/agentic-mobile-blueprint).

Template releases publish upgrade notes to `.agents/skills/template-upgrade/vX.Y.Z.md`.
Each file documents only **shared infrastructure changes** — skills, `_shared/` utilities, build config, env vars, deps.
App scaffold files (`mobile/app/`, example screens) are intentionally excluded.

---

## Step 1 — Check for updates

Read the local version:

```bash
cat TEMPLATE_VERSION
```

Fetch the template's latest version:

```
https://raw.githubusercontent.com/Ampli-Group/agentic-mobile-blueprint/main/TEMPLATE_VERSION
```

If local == latest: nothing to do. Stop here and tell the user they are up to date.

## Step 2 — Discover upgrade notes to apply

Fetch the list of upgrade files from the template:

```
https://api.github.com/repos/Ampli-Group/agentic-mobile-blueprint/contents/.agents/skills/template-upgrade
```

This returns a JSON array. Filter for files whose name matches `vX.Y.Z.md` and whose version is **strictly greater than** the local version and **less than or equal to** the latest version. Sort them in ascending semver order (oldest first).

**Semver comparison:** parse each version as `[MAJOR, MINOR, PATCH]` integers and compare numerically — do not do lexicographic string comparison.

Example: local = `0.1.0`, latest = `0.3.1` → apply `v0.1.1.md`, `v0.2.0.md`, `v0.3.0.md`, `v0.3.1.md` in that order (only files that actually exist).

## Step 3 — Fetch and read each upgrade file

For each file to apply, fetch its content:

```
https://raw.githubusercontent.com/Ampli-Group/agentic-mobile-blueprint/main/.agents/skills/template-upgrade/vX.Y.Z.md
```

Read the full file before applying anything. Build a complete picture of all changes across all versions first.

## Step 4 — Apply changes

Work through the upgrade notes in version order. For each version:

1. **Breaking Changes** — apply these first and confirm with the user if they are destructive.
2. **New Features / Improvements** — copy or adapt shared files as described.
3. **Bug Fixes** — apply targeted fixes to shared code.
4. **Dependency Updates** — update `package.json`, `deno.json`, or relevant config files.

**Key rules while applying:**

- Only touch files listed in the upgrade notes. Do not infer other changes.
- For shared utilities (`supabase/functions/_shared/`), copy the change directly — these files are not expected to be customised by consuming projects.
- For skills (`.agents/skills/`), merge carefully — the project may have added its own skills.
- For `AGENTS.md`, apply the described changes as a patch rather than overwriting — the project will have customised it.
- For env vars: add new entries to `.env.local` files and remind the user to fill them in. Run `mise run configure` if the upgrade notes say to.
- Never touch `mobile/app/`, example screens, or `maestro/` flows — these are owned by the consuming project.
- **Never copy `.agents/skills/template-upgrade/vX.Y.Z.md` files into the project.** These release notes live only in the blueprint repo. Fetch and read them from GitHub; do not write them to disk.
- **Never copy `.agents/skills/template-release/` into the project.** The release skill is for cutting blueprint releases — it has no use in a consuming project.

## Step 5 — Bump local TEMPLATE_VERSION

After applying all changes:

```bash
echo "X.Y.Z" > TEMPLATE_VERSION
```

## Step 6 — Report

Summarise:
- What versions were applied
- What files were changed
- Any manual steps the user still needs to take (e.g. fill in new env vars, review a merged conflict)
- Anything skipped and why

---

## Shortcut — check only, no apply

If the user just wants to see what would change without applying it:

1. Follow Steps 1–3 only.
2. Print a summary of each version's changes.
3. Ask the user which versions or sections to apply.
