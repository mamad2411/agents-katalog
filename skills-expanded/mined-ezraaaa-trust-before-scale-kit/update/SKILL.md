---
name: update
description: "Update the vendored kit from the installed plugin. Use for: update trust before scale, update the kit, kit update, tbs update."
---

# Update the project kit

1. Work from the Git repository root. Run the updater from the installed kit so the first
   update uses the installed version's safety checks. Substitute the base directory shown when
   this skill loaded and run `node "<this skill's base directory>/../../templates/scripts/update.mjs" --branch`.
   It checks for tracked changes and untracked installer targets, fetches `origin`, and starts
   the branch from the Git Flow integration branch, `origin/develop`, or the remote default
   branch, in that order. The branch uses the Git Flow feature prefix when configured, `feature/`
   when a `develop` branch exists, and `chore/` otherwise. Pass `--branch-name <name>` if the user
   requests a specific name. If the fetched base already has the installed kit version or newer, it
   creates no branch; a base without a valid `scripts/tbs/VERSION` stops it. For an update in place on an existing feature branch, omit `--branch`. If the
   kit is current, stop.
2. Pass `--codex-hook` if the user requests it. The updater also refreshes an existing kit Bash
   merge-gate hook and runs doctor after updating.
3. Stop on a failed update or doctor check and report the failure. After a successful update, review
   `git diff`, run the project's gates, commit, and open a PR following the project's rules and
   approval requirements. Never merge without the user's go-ahead.
