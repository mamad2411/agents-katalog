---
name: git-flow
description: Git flow standard for Stockbook (GitLab, Flutter, small squad integrating on `dev`). Conventional Commits, MR hygiene, rebase safety, mobile-specific never-commit list. MANDATORY TRIGGERS - "git commit", "commit message", "merge request", "MR", "PR title", "branch name", "rebase", "amend", "force push", "squash merge", "git flow", "conventional commits".
---

# git-flow

Canonical git rules for **Stockbook** (`gitlab-new.vndirect.com.vn`,
`origin/dev` integration branch, Flutter mobile app, small squad, Claude-driven
commits). Read this before authoring a commit, opening an MR,
rebasing, amending, or pushing.

Sources: Conventional Commits v1.0.0, cbea.ms/git-commit,
docs.gitlab.com/ee/topics/gitlab_flow, Google eng-practices "Small
CLs".

---

## 1. Commit message

**Subject line** — `<type>(scope?)!?: <imperative description>`

- Types: `feat`, `fix`, `chore`, `docs`, `style`, `refactor`, `perf`,
  `test`, `build`, `ci`. `feat` → MINOR, `fix` → PATCH per SemVer.
- ≤ 50 chars, capitalized, imperative mood, no trailing period.
- Sanity test: "If applied, this commit will __". If it doesn't
  read naturally, rewrite.
- Scope is optional — use only when it disambiguates a large area
  (`feat(feed):`, `fix(auth):`).
- Breaking change: `!` before colon (`feat(api)!: drop /v1`) or
  `BREAKING CHANGE: <desc>` footer. Either alone is sufficient.

**Body** — blank line after subject, wrap at 72 chars. Explain
*why*, not *how*. Skip the body for trivial changes.

**Footer** — one token per line:
- `Refs: STOCK-123` — non-closing ticket reference.
- `Closes: #45` — closes MR/issue on merge.
- `BREAKING CHANGE: <desc>` — the description of any `!` in subject.

Keep footers to information that resolves *outside* the current
session: tickets, breaking-change notes, real human co-authors. Do
not include session-scoped or tool-scoped noise (see § 10).

---

## 2. Branching

**Model**: short-lived topic branches integrated into `dev`.
GitFlow (`develop`/`release`/`hotfix` mesh) and GitLab-Flow's
production-branch variant are both heavier than a monthly-cadence
squad needs.

**Names**: `<type>/<slug>` where type ∈ `feat|fix|chore|docs|refactor`.

- `feat/feed-pagination`
- `fix/auth-refresh-race`
- `chore/pubspec-bump-flutter-3.29`
- With ticket: `feat/STOCK-123-feed-pagination`

**Life**: ≤ 2–3 days on your laptop. Rebase onto `origin/dev`
daily. Delete the branch on merge (GitLab MR setting: "Delete
source branch when merge request is accepted" — leave on).

**Release branches** — only when App Store review lag matters. Cut
`release/<version>` (e.g. `release/1.4.0`) at code-freeze;
cherry-pick hotfixes back to `dev`. Justification: iOS review can
hold a build for days and `dev` must keep moving. Do **not**
maintain a permanent `develop` branch.

Do **not** work directly on `dev`. `.claude/settings.json` denies
`Bash(git checkout main)` — use `git switch main` for reads, and
create a topic branch (`git checkout -b feat/<slug>`) for any edit.

---

## 3. Merge request (MR)

Stockbook uses **GitLab MRs**, not GitHub PRs. Use `glab`, not `gh`.

- One topic per MR. Split refactor from feature; land refactor first.
- Target ≤ **200 LOC** net; hard-flag > 400 (Google eng-practices:
  small CLs review faster, catch more bugs, roll back cleaner).
- MR **title = commit subject** (Conventional Commits form) so
  squash-merge produces a clean history entry.
- Open as **Draft** while CI churns; mark ready only after
  `/review` + `/lint` + `/test` pass and description is complete.
- MR description must contain: Summary / Screenshots or recording
  (mobile: mandatory per DoD) / Test plan / Risk & rollback /
  Linked ticket. Ticket noise lives in the MR body, not the commit.
- At least one human reviewer. Claude is never the sole approver
  (Human gate = Phase 12).

### GitLab merge method — pick

Project → Settings → Merge requests → set to **Fast-forward merge**
+ **Squash commits when merge request is accepted**.

- Linear history → bisect-friendly, clean blame.
- Squash → one Conventional Commits entry per feature → drives
  release notes.
- `dev` never carries WIP commits.
- Avoid the **Rebase** merge method: GitLab docs note it "removes
  GPG signatures" and CI does not re-run after the automatic
  rebase.

Enable "Pipelines must succeed" and "All threads must be resolved"
as merge checks.

---

## 4. Rebase, amend, force-push

**Safe** — on your own topic branch, before push, or after push if
no one else has pulled it:
- `git rebase -i` to squash/reword
- `git commit --amend` to fix the tip commit
- `git rebase origin/dev` to keep the MR fast-forward-mergeable

**Forbidden** — on `dev` or any shared branch:
- Rebase / amend commits that exist on `origin/dev` or on a
  branch someone else has pulled.
- Any `git push --force` (blind clobber). Denied in settings.json.
- Any force to `dev` or `release/*`. Denied in settings.json.

**When you must overwrite your own topic branch** (e.g. after an
interactive rebase you just did):
```bash
git push --force-with-lease origin feat/<slug>
```
Never `--force` — `--force-with-lease` refuses the push if the
remote moved since your last fetch.

**Before opening MR**: `git fetch origin && git rebase origin/dev`.

---

## 5. Signed commits

GitLab supports GPG, SSH, and X.509 signing; Premium/Ultimate can
enforce via the "Reject unsigned commits" push rule.

**Recommend, don't mandate**. If corporate GitLab enforces it,
SSH signing is easiest (reuses your push auth key):

```bash
git config --global gpg.format ssh
git config --global user.signingkey ~/.ssh/id_ed25519.pub
git config --global commit.gpgsign true
```

Caveat: the **Rebase** merge method strips signatures — another
reason to prefer Fast-forward + Squash.

---

## 6. `.gitignore` / `.gitattributes`

`.gitattributes`:
```
* text=auto eol=lf
*.png binary
*.jpg binary
*.jpeg binary
*.ttf binary
*.otf binary
*.keystore binary
*.jks binary
```

`.gitignore` must cover: `.dart_tool/`, `.flutter-plugins*`,
`build/`, `ios/Pods/`, `ios/.symlinks/`, `**/*.g.dart`,
`**/*.freezed.dart`, `coverage/`, `.env*`, `*.keystore`, `*.jks`,
`*.p12`, `*.p8`, `*.mobileprovision`, `android/key.properties`,
`ios/Runner/GoogleService-Info.plist` (if it embeds real keys),
`firebase_options.dart` if it embeds prod keys.

Git LFS only for genuinely large binaries (> ~5 MB). Icons and
small assets stay in git.

---

## 7. Hook tiers

- **pre-commit** (fast, < 5 s): `dart format --set-exit-if-changed`
  on staged files, `dart analyze --fatal-infos`, secret scan.
  Currently: `.claude/hooks/pre-commit.sh`.
- **pre-push** (thorough, 30–90 s): `flutter test` + coverage gate
  + hook self-test. Currently: `.claude/hooks/pre-push.sh`.
- Hooks live in-repo under `.claude/hooks/`; users symlink into
  `.git/hooks/` (or set `git config core.hooksPath .claude/hooks`).
- CI must re-run the same checks — never trust local hooks alone
  (devs can `--no-verify`).

---

## 8. Anti-patterns to refuse

- Mixing refactor + feature + bugfix in one commit.
- WIP commits (`wip`, `.`, `stash`, `fix stuff`) — squash message
  must still be a valid Conventional Commit.
- `git add .` in a mixed working tree — use `git add -p` or
  explicit paths.
- Committing generated files: `*.g.dart`, `*.freezed.dart`,
  `.dart_tool/`, `build/`, `coverage/`.
- Committing secrets or signing artefacts (see § 9).
- Rewriting shared history (see § 4).
- `git commit --no-verify` — silently skips gates. Forbid outside
  emergency hotfix; require a follow-up commit re-running the gate.
- Landing a merge with red CI or unresolved threads.

---

## 9. Mobile — never commit

- `*.keystore`, `*.jks`, `key.properties`, `*.p8`, `*.p12`,
  `*.mobileprovision`, `AuthKey_*.p8`, `service_account.json` (Play),
  Firebase `google-services.json` / `GoogleService-Info.plist` **if
  they contain unrestricted API keys**, `.env*`,
  `fastlane/report.xml`.
- Provisioning / signing config (`android/app/build.gradle`
  signingConfig, `ios/Runner.xcodeproj` provisioning) — release
  engineer only, per CLAUDE.md § 9.
- Never hand-edit `pubspec.lock` (CLAUDE.md § 9). If it changed
  unexpectedly, revert.

**Version bump** = its own commit:
```
chore(release): bump to 1.4.0+42
```
Touches only `pubspec.yaml`. No feature work in the same commit —
keeps rollback and changelog clean.

**Store metadata** (`fastlane/metadata/**`, screenshots) — dedicated
`chore(store): …` commit, ideally on the `release/*` branch.

---

## 10. Author attribution

- Git `Author` = the human decider who answers for the change.
- Git `Committer` = whoever applied it; may differ after rebase.
- `Co-Authored-By: Real Human <real@email>` is appropriate when
  pair-programming with another real human — real humans only.
- Keep the message free of session-scoped or tool-scoped trailers
  (run IDs, tool IDs, local audit markers like `P0`/`P1`/`P2` /
  `verdict:*` / `review-pass:N`) — those belong in the MR body or
  review notes, not in permanent git history.
- Author identity for this repo: whatever `git config user.email`
  resolves to for `~/Projects/VND/*` (per-developer machine
  config, e.g. via a `~/.gitconfig-vnd` includeIf).

---

## One-page cheat card

- Subject: `type(scope?)!?: imperative ≤50`. No period. No bot trailers.
- Body: blank line, wrap 72, *why*. Footer: `BREAKING CHANGE:` / `Refs:` / `Closes:`.
- Branch: `feat|fix|chore|docs|refactor/<slug>` off `origin/dev`; life ≤ 2–3 d; rebase daily.
- MR ≤ ~200 LOC, one topic, Draft until green, `glab` (not `gh`), title = squash subject.
- Merge: **Fast-forward + Squash on merge**; CI green; threads resolved.
- Never rebase/amend/force-push published `dev` or `release/*`. `--force-with-lease` only on your own branch.
- Never commit: secrets, keystores, `*.g.dart`, `*.freezed.dart`, `build/`, hand-edited `pubspec.lock`.
- Version bump = solo `chore(release):` commit. `release/*` branch only when App Store lag warrants.
- pre-commit fast + pre-push thorough; CI re-runs both.
- Human approves the MR. Claude never self-approves.

---

## Templates

### Commit message

```
<type>(<scope>?)!?: <imperative subject ≤50 chars>

<why this change; 72-char wrapped body; skip for trivial>

BREAKING CHANGE: <description if subject has !>
Refs: STOCK-<id>
Closes: #<mr-or-issue>
```

Keep footers to trailers that resolve outside the session (see
§ 10).

### MR description

```markdown
## Summary
<one paragraph>

## Screenshots / recording
<mandatory for any UI change>

## Test plan
- [ ] unit + widget tests updated
- [ ] golden snapshots regenerated if UI changed
- [ ] verified on iPhone SE (compact) + one tablet size

## Risk & rollback
<what breaks if this is wrong; how to revert>

## Linked ticket
STOCK-<id>

<!-- AI-assisted: yes -->
```
