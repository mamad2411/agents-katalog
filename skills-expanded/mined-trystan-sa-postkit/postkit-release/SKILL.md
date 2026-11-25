---
name: postkit-release
description: Cut a new postkit release — bump the version in package.json (asks the user whether it's major / minor / patch), commit, tag on GitHub, publish a GitHub Release so watchers get notified, and publish to npm. Use when the user says "ship a release", "cut a new version", "publish to npm", or "release postkit".
---

# /postkit-release — cut a new postkit release

You are a release manager for the postkit npm package. Your job is to take
the current `main` branch, bump the version, tag it, publish a GitHub
Release, and publish to npm — in that exact order, with verification at
every step.

This skill operates on the **postkit repo itself**, not on a user's
scaffolded project. If the working directory isn't the postkit repo
(check that `package.json` has `"name": "postkit"`), stop and tell the
user.

## Before you start — preflight

Run these checks in parallel and bail if any fails:

1. `git status` — working tree must be clean. No uncommitted changes, no
   untracked files that should be committed.
2. `git rev-parse --abbrev-ref HEAD` — must be on `main`.
3. `git fetch origin && git status -sb` — local must be up to date with
   `origin/main` (no `ahead`/`behind`).
4. `gh auth status` — `gh` must be authenticated. If not, tell the user to
   run `gh auth login` and stop.
5. `npm whoami` — npm must be authenticated. If it errors, tell the user to
   run `npm login` and stop.
6. Read `package.json` and note the current version (`X.Y.Z`).

If preflight fails, surface the specific failure and stop. Do not attempt
to "fix" by stashing, force-pushing, or skipping checks.

## Step 1 — Ask which kind of bump

Ask the user **one question** with three concrete options, showing the
resulting version for each:

> "Current version is `X.Y.Z`. Which bump?
>  - **patch** → `X.Y.(Z+1)` (bug fixes, doc tweaks, internal changes)
>  - **minor** → `X.(Y+1).0` (new skill, new feature, backwards-compatible additions)
>  - **major** → `(X+1).0.0` (breaking change to the scaffolder contract or skill APIs)"

Wait for the answer. If the user picks something ambiguous, ask again. Do
not assume.

While you're at it, ask: **"Anything specific you want highlighted in the
release notes?"** — short answer is fine, can be skipped.

## Step 2 — Summarize the changes since last release

Find the previous tag and gather the commits since:

```bash
git describe --tags --abbrev=0      # previous tag, e.g. v0.2.1
git log <prev-tag>..HEAD --oneline
```

Group the commits into a short changelog under these headings (skip empty
ones):

- **Added** — new skills, new features, new options
- **Changed** — modified behavior of existing skills/features
- **Fixed** — bug fixes
- **Internal** — refactors, doc-only changes, build/CI

Show the proposed changelog to the user and **ask for confirmation before
proceeding**. They may want to edit the wording. Use the user's "anything
specific to highlight" answer from Step 1 to bias what goes at the top.

## Step 3 — Bump the version

Use `npm version` so it edits `package.json`, creates the commit, and
creates the tag in one shot:

```bash
npm version <patch|minor|major> -m "release v%s"
```

This:
- updates `package.json` (and `package-lock.json` if present)
- commits with message `release vX.Y.Z`
- creates an annotated git tag `vX.Y.Z`

Read `package.json` afterward to confirm the new version, and capture the
new tag name (`vX.Y.Z`) — you'll need it for steps 4–6.

If `npm version` fails (e.g. because the working tree wasn't clean), do
**not** retry with `--force`. Surface the error and stop.

## Step 4 — Push the commit and tag to GitHub

```bash
git push origin main
git push origin vX.Y.Z
```

Push the commit before the tag so GitHub renders the tag against the right
SHA. Verify both succeeded before moving on.

## Step 5 — Create the GitHub Release

This is what triggers watcher notifications — don't skip it.

```bash
gh release create vX.Y.Z \
  --title "vX.Y.Z" \
  --notes "$(cat <<'EOF'
<the changelog from Step 2, formatted with ## headings>
EOF
)"
```

Use `--latest` is implied for non-prerelease versions; don't pass `--draft`
or `--prerelease` unless the user asked for one. Capture the release URL
from the command output and report it.

## Step 6 — Publish to npm

Final step. The package is public, so no special flags needed beyond:

```bash
npm publish
```

If the package has a prepublish/prepare script, let it run — don't skip
hooks. If publish fails because of 2FA, prompt the user for the OTP and
retry with `--otp=<code>`.

After publish succeeds, verify with:

```bash
npm view postkit version
```

It should print the new `X.Y.Z`.

## Step 7 — Report back

Show the user:

- **Tag:** `vX.Y.Z`
- **GitHub Release:** the URL from Step 5
- **npm:** `https://www.npmjs.com/package/postkit/v/X.Y.Z`
- **What shipped:** the changelog, condensed to 2–3 bullets

End with a one-line suggestion for what to do next (e.g. "want me to test
the release by running `npx postkit@latest` in a temp dir?").

## Important

- **Never skip preflight.** A dirty working tree, a non-`main` branch, or
  unauthenticated `gh`/`npm` are stop conditions, not warnings.
- **Never use `--force`** on git push, npm publish, or `npm version`.
- **Never edit `package.json` by hand** to bump the version — `npm version`
  is the only correct path because it also creates the tag.
- **Do the steps in order.** Tag → push → GitHub Release → npm publish.
  If you publish to npm before tagging, you can't easily roll back the npm
  version (npm unpublish has a 72h window and breaks downstream caches).
- **If something fails mid-way**, stop and explain what happened. Do not
  attempt automated recovery — the user decides whether to roll back, fix
  forward, or retry.
- **Pre-1.0 note.** While the package is on `0.x.y`, treat any breaking
  change as a **minor** bump (per semver convention for 0.x). A `1.0.0`
  bump means the user is declaring the API stable — only do that if they
  explicitly say so.
