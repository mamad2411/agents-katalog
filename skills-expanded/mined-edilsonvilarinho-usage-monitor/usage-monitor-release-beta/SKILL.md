---
name: usage-monitor-release-beta
description: Beta channel of usage-monitor — publish a vX.Y.Z-beta.N prerelease for opted-in users, fix it with the next beta, promote the series to stable, or withdraw/restore a beta. Use for any beta release task; plain stable releases use usage-monitor-release.
---

# Usage Monitor Beta Release

Run the whole life of a beta for the users who opted into the beta channel (issue #355). Publishing
is the stable release flow ([usage-monitor-release](../usage-monitor-release/SKILL.md)) with a
different tag and a different promise: **a beta never becomes `latest`**, so nobody outside the
channel receives it.

## Operations (the argument picks one)

| Argument | What it does | Section |
|---|---|---|
| `patch` / `minor` / `major` | Publish `beta.1` of a new series for the next stable of that type | Workflow |
| `next` | Publish `beta.N+1` of the open series (the way to **fix** a bad beta) | Workflow |
| `promote` | Publish the stable `vX.Y.Z` of the open series — the beta "goes to main/master" | Promote |
| `withdraw [tag]` | Hide a beta: nobody new is offered it (reversible) | Withdraw |
| `restore [tag]` | Undo a `withdraw` | Restore |

There is **no "move the beta to main"**: the tag already points to a commit on `main` —
`verify-version` refuses anything else. The code is merged *before* the beta exists; what "going to
stable" means is publishing a new, stable build of that code (`promote`). There is also **no
rollback** for testers who already installed a beta: the app never downgrades. They leave the beta
when a higher version reaches them — the next beta or the stable.

## How the channel works (read before tagging)

- Tag format: `vX.Y.Z-beta.N`, `N ≥ 1`. Nothing else is accepted — `verify-version` rejects
  `-rc.1`, `-beta` without a number and any other suffix, and the Linux updater refuses them too.
- The workflow sets `prerelease: true` and `make_latest: false` for `-beta.N` tags. Clients outside
  the channel read `/releases/latest`, which the GitHub API never answers with a prerelease — that is
  the whole protection, and it also covers app versions older than the channel.
- Clients inside the channel list `/releases?per_page=20` and take the highest non-draft version by
  SemVer precedence: `42.0.0-beta.1 < 42.0.0-beta.2 < 42.0.0`. The stable `42.0.0` therefore reaches
  every beta tester of the `42.0.0` series. Turning the channel off never downgrades.
- `X.Y.Z` is the **next stable** version the beta previews. Never tag a beta for a number that is
  already released as stable: `41.0.0-beta.1` after `v41.0.0` is lower than the running stable and is
  never offered to anyone.
- Packaging: Exe/Dmg carry only `X.Y.Z` (jpackage rejects the suffix), Deb/Rpm carry `X.Y.Z~beta.N`;
  `CURRENT_APP_VERSION`, the NSIS installer name, the tarball and the release assets keep the full
  `X.Y.Z-beta.N`.

## Workflow

1. Read [AGENTS.md](../../../AGENTS.md), [build.gradle.kts](../../../build.gradle.kts) and
   [.github/workflows/release-linux.yml](../../../.github/workflows/release-linux.yml) first.
2. Invoking this skill already means "cut and publish the beta". Do not ask for confirmation to tag or
   push — go through the whole flow and report the result. The only question allowed is the one in
   step 6 (window hosts).
3. Pick the operation from the request (see the table above). `promote`, `withdraw` and `restore`
   have their own sections below; this workflow is for publishing a beta:
   - `patch` / `minor` / `major` — start a new series for the next stable of that type:
     `N = 1`.
   - `next` (or no type while a series is open) — continue the open series: `N + 1`.
   - If the request is ambiguous and there is no open series, ask which type.
   - An **open series** is `vX.Y.Z-beta.*` with no stable `vX.Y.Z` yet.
4. Verify that `main` is clean and matches `origin/main` — the tag must point to a commit already on
   the remote `main`, or `verify-version` refuses it:
   - `git fetch origin --tags && git status --short --branch`
   - `git log --oneline -5`
5. Compute the version. **There is no version bump commit** — the version comes from the tag.
   - Last stable: `git describe --tags --abbrev=0 --match "v[0-9]*" --exclude "*-beta*"`.
   - Betas of the series: `git tag --list "vX.Y.Z-beta.*"`, highest `N` by numeric sort
     (`git -c versionsort.suffix=- tag --sort=-version:refname --list "vX.Y.Z-beta.*" | head -n 1`).
   - New series: `X.Y.Z` = last stable bumped by the type; refuse if `vX.Y.Z` already exists.
   - Continue: same `X.Y.Z`, `N + 1`; refuse if the stable `vX.Y.Z` already exists (the series is
     closed — start a new one).
6. Run the local verification that must pass before the tag exists:
   - `gradlew.bat allTests` — mandatory. A beta is still a public tag; a broken suite discovered after
     the push is a burned tag.
   - **Window hosts changed? Stop before the tag** (#342), exactly as in the stable skill: run
     `git diff --name-only $(git describe --tags --abbrev=0)..HEAD` and look for `HudWindow.kt`,
     `DesktopWindowFrame.kt`, `Main.kt` or any `*WindowHost*.kt`. If one changed, list the rows of
     [`docs/hud-notch.md` › "Fora do alcance dos testes"](../../../docs/hud-notch.md#fora-do-alcance-dos-testes)
     the change touches and ask the maintainer whether the build was opened on Linux (X11). A beta is
     a good place to *find* such bugs, but the testers still run it as their daily app.
   - Do not package locally as a gate; CI owns packaging for the three OSes.
7. Publish:
   - annotated tag with the temporary agent git identity:
     `git -c user.name=claude -c user.email=claude@anthropic.com tag -a vX.Y.Z-beta.N -m "vX.Y.Z-beta.N"`
   - push **only the tag**: `git push origin vX.Y.Z-beta.N`.
8. Watch `Release Desktop Packages` and report the outcome. Then confirm on the published release:
   - it is marked **Pre-release**:
     `gh release view vX.Y.Z-beta.N --json isPrerelease` → `true` (`gh` has no `isLatest` field);
   - it is **not** Latest — `/releases/latest` still points to the last stable:
     `gh api repos/edilsonvilarinho/usage-monitor/releases/latest --jq .tag_name`;
   - every artifact family is there, each with a `sha256:` digest (auto-update refuses assets without it):
     `UsageMonitor-Setup-X.Y.Z-beta.N.exe`; `.deb`, `.rpm` and `usage-monitor_X.Y.Z-beta.N_linux_x64.tar.gz`;
     `usage-monitor_X.Y.Z-beta.N_macos_arm64.dmg` and `usage-monitor_X.Y.Z-beta.N_macos_x64.dmg`.
     `gh release view vX.Y.Z-beta.N --json assets --jq '.assets[] | [.name, .digest] | @tsv'`
   A beta missing an artifact family, or published as Latest, is a failed release and must be reported
   as such. If it went out as Latest, edit it back with
   `gh release edit vX.Y.Z-beta.N --prerelease --latest=false` and report it — every user outside the
   channel was being offered the beta.
9. The release notes come from the workflow's `Generate release notes` step: a beta diffs against the
   previous tag (beta or stable); the stable release later diffs against the previous **stable**, so it
   lists the whole series. Do not write them by hand.

## Promote — the open series becomes the stable release

The stable is a **new tag and a new build**, never the beta release edited into a stable one. The beta
binaries carry `X.Y.Z-beta.N` in `CURRENT_APP_VERSION`, in the installer name and in the receipt; an
edited release would hand every user a build that calls itself beta. Never run
`gh release edit ... --prerelease=false` or `--latest` on a beta.

1. Find the open series: `git -c versionsort.suffix=- tag --sort=-version:refname --list "v*-beta.*" | head -n 1`
   gives `vX.Y.Z-beta.N`. Refuse if `vX.Y.Z` already exists (nothing to promote) or if there is no
   beta tag.
2. Decide **what** becomes stable:
   - default — the current `origin/main` (the beta code plus whatever was merged after it). Say in
     the report which commits are new since the last beta:
     `git log --oneline vX.Y.Z-beta.N..origin/main`.
   - `promote exact` — the very commit the testers ran: tag `vX.Y.Z` on `vX.Y.Z-beta.N^{commit}`.
     `verify-version` accepts it, because that commit is on `main`.
3. Run the stable flow of [usage-monitor-release](../usage-monitor-release/SKILL.md) from its step 4
   (clean `main` = `origin/main`, `allTests`, the #342 window-host question, annotated tag, push only
   the tag, watch the workflow, check every artifact) with the version fixed to `X.Y.Z` — do **not**
   bump it by type. For `promote exact`, create the tag on the beta commit:
   `git -c user.name=claude -c user.email=claude@anthropic.com tag -a vX.Y.Z vX.Y.Z-beta.N^{commit} -m "vX.Y.Z"`.
4. Confirm: `gh release view vX.Y.Z --json isPrerelease` → `false`, and `/releases/latest` → `vX.Y.Z`.
   The stable notes diff against the previous **stable**, so they list the whole beta series.
5. Result: users outside the channel receive `X.Y.Z` as a normal update; testers on
   `X.Y.Z-beta.N` receive it too (`beta.N < X.Y.Z`) and see its "Novidades". The series is closed —
   the next beta starts a new one.

## Withdraw — a bad beta stops being offered

Withdrawing **hides** the release; it does not delete anything and it is reversible (`restore`).
The client ignores drafts, and anonymous API calls — the ones the app makes — do not see them.

1. Target: the tag in the request, or the highest `v*-beta.*`. Refuse a stable tag: withdrawing a
   stable is not this skill's job.
2. `gh release edit vX.Y.Z-beta.N --repo edilsonvilarinho/usage-monitor --draft=true`
3. Confirm it is hidden from what the app reads:
   `gh api "repos/edilsonvilarinho/usage-monitor/releases?per_page=20" --jq '.[] | select(.draft == false) | .tag_name'`
   must not list it (this call is authenticated and sees drafts only with `draft: true`), and
   `/releases/latest` is unchanged.
4. Report what it does **not** undo, every time:
   - testers who already installed that beta **stay on it** — there is no downgrade. They move when a
     higher version reaches them;
   - an auto-update already downloaded but not yet applied is still applied on the next exit.
5. What to do next — say it in the report:
   - **fix forward** (the normal path): merge the fix and run this skill with `next` —
     `vX.Y.Z-beta.N+1` is offered to everyone in the channel, including those stuck on the bad one;
   - **abandon the series**: `promote` a stable that does not include the bad change, or start a new
     series later. Never reuse a withdrawn tag name — a client may already know it.
6. The tag stays on the remote. Deleting the release or the tag (`gh release delete --cleanup-tag`)
   is permanent and **not** part of this skill: it gains nothing over the draft and loses the record.
   If the maintainer really wants it, tell them the command and let them run it.

## Restore — undo a withdraw

1. `gh release edit vX.Y.Z-beta.N --repo edilsonvilarinho/usage-monitor --draft=false --prerelease --latest=false`
   — the three flags together, so it comes back exactly as a beta and never as Latest.
2. Confirm `isPrerelease: true`, `/releases/latest` unchanged, and that the channel sees it again
   (the non-draft listing above lists it).
3. If a newer beta or the stable of the series already exists, restoring an older beta changes nothing
   for anyone — say so instead of restoring.

## Guardrails

- Never publish a stable version from this skill except through `promote`, which runs the stable
  flow of `usage-monitor-release` with the version fixed to the open series.
- Never turn a beta release into a stable or Latest one by editing it; `restore` always passes
  `--prerelease --latest=false`.
- Never delete a release or a tag; `withdraw` hides it as a draft.
- Never tag a suffix other than `-beta.N`.
- Never tag a beta whose `X.Y.Z` is already released as stable.
- Do not release from a dirty tree unless the user explicitly wants that risk.
- Do not ask the user to confirm the tag or the push; the one exception is step 6 (#342).
- Prefer current code and workflow files over older notes when they disagree.
