---
name: version-control
description: Plan and run a release train in the Semantic Markdown repository. Given a list of features for a release (e.g. "1.2.0: link completion, smd fmt, mermaid diagnostics"), create the release branch and one independent branch per feature, develop each in its own worktree, merge feature PRs into the release branch, then — after the release is tagged and published — merge the release branch into main. Use this skill whenever the user gives features for a version, asks to start/plan a release or milestone (including "do the v1.2 items from the roadmap"), asks which branch to work on or where a PR should target, wants to add a feature to an in-flight release, or asks to finish/close a release. Use together with the smd-release skill, which owns compatibility checks, versioning rules and publishing.
---

# Version control: the release train

Every change reaches `main` through a release branch:

```text
main ──► release/vX.Y.Z ──► feat/a ──┐
                        ├──► feat/b ──┼──(squash PRs)──► release/vX.Y.Z ──► tag vX.Y.Z ──► publish ──(merge commit PR)──► main
                        └──► fix/c ───┘
```

- `main` only ever contains **released** code, so it always matches the latest tag.
- `release/vX.Y.Z` is the integration branch for one version. It is opened at its version: the bump and changelog heading are its first commit.
- Each **major feature** gets its own branch from the release branch, so features are developed, reviewed and dropped independently.

The compatibility gate, versioning rules, changelog format and publishing steps come from the **smd-release** skill. Follow it at the points marked ▶ smd-release.

## 1. Plan the release from the feature list

1. Pin down the version and the feature list.
   - If the user points at the roadmap ("the v1.2 items"), read that milestone with the semantic-markdown-reader skill (`smd agent ROADMAP.smd --section "v1.2…"`) and take the unchecked items.
   - Group small related items into one branch per **major feature**. A branch should be one reviewable PR, one changelog bullet group, and something that can be dropped without affecting the others.
   - Name branches `feat/<slug>` (user-visible capability), `fix/<slug>` (bug), `docs/<slug>`, `perf/<slug>`, `refactor/<slug>` or `chore/<slug>`, all lowercase kebab-case.
2. Check the version against the last tag (▶ smd-release `references/versioning.md`): new capabilities → minor, fixes only → patch, anything breaking → major.
3. Confirm the version and the branch list with the user before creating anything, since branches are pushed to the public repository.
4. Create them:

   ```bash
   node .claude/skills/version-control/scripts/plan-release.mjs 1.2.0 link-completion smd-fmt mermaid-diagnostics fix/preview-scroll
   ```

   Run it with `--dry-run` first to show the plan. The script:
   - creates `release/v1.2.0` from `origin/main`, or reuses it
   - commits the version bump and changelog heading on it (`chore(release): start 1.2.0`)
   - creates each feature branch from the release branch head
   - pushes everything
   - opens a **draft tracking PR** `release/v1.2.0 → main` with a checklist

   It never touches the current checkout. Re-run it with more features to add them to the same release.

## 2. Build each feature on its own branch

- **Use one worktree per feature** so parallel work (other sessions, other agents) never collides:

  ```bash
  git worktree add ../wt-feat-smd-fmt feat/smd-fmt
  cd ../wt-feat-smd-fmt/extension && npm ci
  ```

  Keep worktree paths short on Windows: `node_modules` exceeds the path limit under deep temp folders.
- **Never switch branches in a checkout someone else may be using.** If `git branch --show-current` or the terminal shows another session's branch, use a new worktree.
- Commit with Conventional Commits (`feat(fmt): …`) and no AI co-author trailers. Every feature PR adds its bullets under the **release's version heading** in `extension/CHANGELOG.md`, not under "Unreleased".
- Keep each feature independent. Base it on the release branch, never on another feature branch.
- **If a feature truly needs another one:** merge the first feature's PR into the release branch, then merge the release branch into the dependent feature branch. Don't stack PRs.
- Keep the feature branch current: when the release branch moves, merge it in (`git merge origin/release/vX.Y.Z`). Don't rebase shared branches.

## 3. Merge features into the release branch

1. Open the PR against the release branch, not `main`:

   ```bash
   gh pr create --base release/v1.2.0 --head feat/smd-fmt --title "feat(fmt): smd fmt and a VS Code formatter"
   ```

   Use the PR checklist from ▶ smd-release `references/branching.md`.
2. CI runs on PRs into `release/**`. The compatibility job runs `release-check.mjs --pr` against the last tag. Review anything it flags (▶ smd-release §2–3). CI does no static analysis, so run the SonarQube gate locally before opening the PR (▶ sonarqube-scan).
3. **Squash-merge** after approval: one commit per feature on the release branch. Then tick the feature in the tracking PR's checklist and delete the feature branch.
4. A feature that isn't ready by the release date **leaves the train**. Close its PR, or retarget it to the next release branch once that exists. Don't hold the release for it.

## 4. Release

On the release branch, once every planned feature is merged or dropped:

1. Finish `extension/CHANGELOG.md` for the version: every ⚠️ breaking change with a migration note, and empty headings removed.
2. Run the **full** check, `node .claude/skills/smd-release/scripts/release-check.mjs` (release mode), and the SonarQube gate, `node .claude/skills/sonarqube-scan/scripts/sonar-scan.mjs` (▶ sonarqube-scan, must pass). Get the maintainer's approval of both reports (▶ smd-release §5, mandatory).
3. Mark the tracking PR ready for review. Its CI runs the release gate as well.
4. **Tag the release branch head** (the exact commit that ships). Pushing the tag runs the Release workflow, which builds from the tag, creates the GitHub Release and publishes; then verify each registry (▶ smd-release §6–7):

   ```bash
   git tag -a v1.2.0 origin/release/v1.2.0 -m "Semantic Markdown 1.2.0" && git push origin v1.2.0
   ```

5. Verify every registry shows the new version before calling it released (▶ smd-release §7).

## 5. Merge the release branch into main (after the release)

1. Merge the tracking PR `release/vX.Y.Z → main` with a **merge commit**, never a squash, so the tagged commit is part of `main`'s history and `git describe` on `main` finds the tag.
2. Delete the release branch and any leftover feature branches. The tag keeps the release reachable.
3. If a later release branch is already open, merge `main` into it so it picks up anything that changed.

## Hotfixes to a shipped version

Start the patch train from the shipped tag, not from `main`, so unreleased work can't leak into the hotfix:

```bash
node .claude/skills/version-control/scripts/plan-release.mjs 1.2.1 fix/preview-scroll --base v1.2.0
```

Then follow the same steps: PR into `release/v1.2.1`, tag, publish, merge into `main` (the tracking PR targets `main`). Afterwards, merge `main` into any open release branch.

## Rules of thumb

| Situation | Do |
|---|---|
| "Where should this PR go?" | Into the open release branch for its version, not `main` |
| Tooling, CI or docs unrelated to a release | Include it in the current release train as a `chore/` or `docs/` branch |
| Two releases in flight | Each has its own `release/v…` branch. Fixes land in the older one first and are merged forward. |
| The release branch and `main` diverged | Merge `main` into the release branch (never the other way before the release) |
| A branch was merged | Delete it on GitHub and locally |

## Scripts

- `scripts/plan-release.mjs <X.Y.Z> <feature>…`: creates the release train (flags: `--dry-run`, `--no-pr`, `--no-bump`, `--base <branch|vX.Y.Z>`).
