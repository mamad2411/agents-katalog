---
name: skill-update-check
description: Check whether installed or vendored agent skills have changed upstream on GitHub, show what changed, and offer a refresh. Covers skills installed with the skills CLI (via ~/.agents/.skill-lock.json) and third-party skills copied into a repo (via a vendor.json). Use when the user asks "are my skills up to date", "check for skill updates", "refresh vendored skills", or before a release of a repo that vendors skills.
---

# Skill update check

Read-only until the user approves a refresh. Upstream skills change often, sometimes by moving content into a new skill, so a refresh is a decision, not a reflex.

## Run

```bash
# skills installed with the skills CLI
GITHUB_TOKEN=$(gh auth token) python3 -I <this skill's folder>/scripts/check_updates.py --lock

# third-party skills copied into a repo
GITHUB_TOKEN=$(gh auth token) python3 -I <this skill's folder>/scripts/check_updates.py --vendor vendor.json
```

- The token is optional. Without it GitHub allows about 60 requests per hour, which a large lock file can exceed. Never print the token.
- `--only a,b` checks named skills. `--fail-on-changes` exits 1 when anything changed, for CI.
- It compares the git tree hash of each skill folder with the same folder on the upstream default branch. Only public repo names and paths are sent to `api.github.com`.

## After running

1. Report the counts, then each changed skill with the upstream commits listed under it. Say "unknown" results plainly (folder moved, repo gone, rate limit).
2. For each changed skill, read the commit titles and say what kind of change it is: fixes, new content, or a restructure. A restructure (for example "Add better-motion skill" after content left `better-ui`) can mean refreshing one skill drops content that now lives in another; check the upstream repo for new sibling skills before refreshing.
3. Ask before changing anything. Then:
   - **CLI installs:** refresh with `npx skills add <source> --global --agent <agents> --skill <name> --yes`, through the `skill-pack-installer` skill so collisions are checked. Do not run `npx skills update --help`; it performs a real update.
   - **Vendored copies:** replace the folder with the upstream folder at the new commit, keep the repo's added files (such as a copied `LICENSE`), update the pinned commit in `vendor.json` and the notices file, and run the repo's validator.
4. Re-run the check and show that the refreshed skills now report "up to date".

## Rules

- Never edit a vendored skill to "merge" upstream changes by hand. Replace it with upstream and keep only the repo's own added files.
- Do not refresh skills the user has edited locally without asking; a refresh overwrites their edits. If a skill folder is a real directory rather than a link into `~/.agents/skills`, treat it as user-managed.
- Run the `skill-vetter` skill on a refreshed third-party skill when its scripts changed.
