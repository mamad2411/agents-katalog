---
name: release
description: Use when releasing the craft plugin from main.
disable-model-invocation: true
argument-hint: "[major|minor|patch]"
---

# Release

A release is a `vX.Y.Z` tag on `main`, the same `version` in
`.codex-plugin/plugin.json`, in `.claude-plugin/plugin.json` and in the
plugin's entry of `.claude-plugin/marketplace.json`, a section in
`CHANGELOG.md` and a GitHub release with that section as its notes. An
install from GitHub, in Claude Code, Codex or ZCode, updates only when that
`version` changes (PDR 0015), and `make check` fails when the three fields
differ.

This skill is the only place `version` and `CHANGELOG.md` change; other pull
requests leave them alone. It releases what is already on `main`: merging
another pull request is a separate decision, never a step of the release. The
release commit itself reaches `main` through a pull request of its own, as
every change does: the ruleset of `main` requires the checks.

Each command runs in a fresh shell, so `$last`, `$version`, `$base` and
`$merge` below stand for values: write the real ones (`v0.1.0`, `0.2.0`, a
commit hash) into every later command.

1. **Start from `main`.** Run `git fetch origin --tags`. Stop and say why if the
   branch is not `main` or the tree is dirty. Behind `origin/main`: `git merge
   --ff-only origin/main`. Stop if that fails, or if `HEAD` is still not
   `origin/main` — local commits the remote does not have. `git rev-parse HEAD`
   is `$base`, the commit that the release covers.
2. **Read what is unreleased.** `last=$(git describe --tags --abbrev=0 --match 'v[0-9]*')`, then
   `git log --format='%h %s' "$last"..HEAD`.
   A log line is the short hash, a space and the subject; steps 3 and 4 read
   the subject. No commits since the tag: stop, there is nothing to release. If
   `jq -r .version .codex-plugin/plugin.json` is not `${last#v}`, stop: the field
   moved outside a release, and that has to be undone first. The same for
   `CHANGELOG.md`: if `grep -m1 '^## ' CHANGELOG.md` is not `## ${last#v} ...`,
   a section was written outside a release; stop.
3. **Pick the level.** `$ARGUMENTS` when it is `major`, `minor` or `patch`;
   empty, the highest that applies; anything else, stop and say it is not a
   level. A subject's type is everything before its first `:` —
   `feat(github)!` is type `feat`, scope `github`, breaking:

   | Level | When |
   | --- | --- |
   | major | a type ends in `!` |
   | minor | a type is `feat` |
   | patch | anything else, reverts included |

   Bump `${last#v}` by that level — a minor resets the patch, a major resets
   both. Show the subjects, the level and the new version, and wait for a yes.
4. **Write the changelog section.** Insert it into `CHANGELOG.md` above the
   previous version's `## ` heading, under a heading `## $version - YYYY-MM-DD`
   with today's date. One line per subject from step 2, in `git log` order,
   grouped by type under `### Added` (`feat`), `### Changed` (every other type)
   and `### Fixed` (`fix`), in that order; leave out a group with no lines. A
   line is the scope in parentheses, then the subject without its type:
   `feat(github): check the citations (#24)` becomes `- (github) check the
   citations (#24)`. Every line has a scope. A subject with no scope gets one
   from the files its commit changes, `git show --name-only --format= <hash>`.
   Each file gives the area it belongs to:

   | Files | Area |
   | --- | --- |
   | `skills/<name>/`, and `docs/<name>/` when `skills/<name>/` exists | the skill without `-conventions`: `typescript` |
   | `.claude/skills/<name>/` | `<name>`: `release` |
   | `scenarios/<name>/` | the skill `<name>`: `github` |
   | any other file in `scenarios/` | `scenarios` |
   | `rules.md` | `rules` |
   | `hooks/` | `hooks` |
   | `.github/workflows/` | `ci` |
   | `.codex-plugin/`, `.agents/` | `codex` |
   | `tests/<name>_eval.sh` | the areas of the skills whose use it counts: `tests/skill_load_eval.sh` gives `react` and `typescript` |
   | any other test, and a fixture of a test | the area of the code the test runs: `tests/rules_test.sh` runs `hooks/rules.sh`, so `hooks` |

   Any other file gives no area: the root `README.md`, `CHANGELOG.md`, the
   `Makefile`, `.gitattributes`, `.claude-plugin/`. A manifest's description
   that only lists a new skill gives no area too. The scope is the areas in
   alphabetical order, comma-separated: `(react, typescript)`. Four or more
   areas, or none, give `(plugin)`. Breaking subjects (`!`) get `(breaking)` at
   the end of the line.
5. **Bump and check.** Set the three fields:

   ```sh
   for f in .codex-plugin/plugin.json .claude-plugin/plugin.json .claude-plugin/marketplace.json; do
     tmp=$(mktemp) && jq --arg v "$version" 'if .plugins then .plugins[0].version = $v else .version = $v end' "$f" >"$tmp" && mv "$tmp" "$f" || exit 1
   done
   ```

   Then `make check`. If the loop or the check fails, restore the four files
   and stop.
6. **Merge through a pull request, then tag the merge commit.** Commit on a
   branch and push it:

   ```sh
   git switch -C "chore/release-$version"
   git commit -m "chore(release): bump the version to $version" -- .codex-plugin/plugin.json .claude-plugin/plugin.json .claude-plugin/marketplace.json CHANGELOG.md
   git push -u origin "chore/release-$version"
   ```

   After the push succeeds, in a separate command:
   `gh pr create --assignee @me --title "chore(release): bump the version to $version" --body "The version in the Claude and Codex manifests and the $version section of CHANGELOG.md."`.
   Wait for its checks as `merge.md` of `craft:github` says, and stop
   where it stops. When the person drops the release there, close it:
   `gh pr close <PR> --delete-branch`, then `git switch main`. When the checks
   pass, run `git fetch origin main`. If `origin/main` is not `$base`, `main`
   moved, and the section misses its new commits: close the release the same
   way, and start again at step 1; step 4 writes the section again. Otherwise
   merge, with no *Finishing* of `craft:github`, as the release closes no
   issue:

   ```sh
   gh pr merge <PR> --squash --delete-branch \
     --subject "chore(release): bump the version to $version (#<PR>)" \
     --body "- Set the version to $version in the Claude and Codex manifests
   - Add the $version section to CHANGELOG.md"
   ```

   A squash merge makes a new commit, so the tag goes on the commit that the
   merge put on `main`: `gh pr view <PR> --json mergeCommit --jq .mergeCommit.oid`
   is `$merge`. Run `git fetch origin main`. If `git rev-parse "$merge^"` is
   not `$base`, commits landed between the check and the merge: the release
   holds them, but its section, and maybe its level, do not. Stop before the
   tag, and show the person `git log --oneline "$base..$merge^"` with the
   level that step 3 gives for them: the person decides how to correct the
   release. Otherwise:

   ```sh
   git tag -a "v$version" -m "v$version" "$merge"
   git push origin "v$version"
   git switch main && git merge --ff-only origin/main
   ```
7. **Publish the GitHub release** with the new section, heading left out, as
   its notes. One shell line, so the empty check guards the create. Nothing in
   this file may read as a dollar sign followed by a digit: Claude Code
   replaces those with the skill's arguments before the model reads it.

   ```sh
   notes=$(sed -n "/^## $version /,/^## /{/^## /d;p;}" CHANGELOG.md | sed '1{/^$/d;}') \
     && [ -n "$notes" ] && gh release create "v$version" --verify-tag --title "v$version" --notes "$notes"
   ```

   Empty notes mean the heading in step 4 does not read `## $version ` — fix
   it through a pull request of its own, merged as `merge.md` of
   `craft:github` says, then run this again on `main`. Without `--verify-tag`, a tag
   missing on the remote does not stop `gh`: it tags the default branch's HEAD
   and publishes the release there. With it, `gh` stops: run the tag push from
   step 6, then run this again. A failed `gh release create` leaves nothing to
   undo: fix the cause and run it again.
8. **Report** the new tag, the pull request, the release URL and the update steps from the
   README's *Update* section, the trust in `/hooks` included.
