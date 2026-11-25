---
name: release
description: Cut a mAIestro Code release — bump the version, build this machine's installers (the signed, notarized universal .dmg on the release Mac; the x64 Windows installer on the Windows PC), and publish one GitHub Release carrying all of them. Runs the scripts/release.sh pipeline from the primary checkout, usable from any session including a mAIestro Code-spawned worktree; re-run it on the other machine to complete the release.
allowed-tools: Bash(git *) Bash(gh *) Bash(scripts/release.sh *) Bash(cd *) Read Write AskUserQuestion
---

You are cutting a release. The mechanics live in `scripts/release.sh` (idempotent
commands: `bump`, `build`, `publish`, `finalize`); your job is the judgment
around them — where to run, what to bump, and the release notes — plus driving
the commands and reporting the result.

Releases are **local** and span **two machines**: one version, one tag, one
GitHub Release carrying

| Asset key | Built on | File |
|---|---|---|
| `macos` | the release Mac | the signed + notarized universal `.dmg` (Apple silicon + Intel) |
| `windows-x64` | the Windows PC (Git Bash) | `mAIestro-Code_X.Y.Z_x64-unsigned-setup.exe` |

Either machine can go first. The first `publish` creates a **draft** release;
each machine uploads its own assets; the release is **published only once
every asset is attached** (the repo has immutable releases on, so nothing can
be added after that). The Windows installer is **unsigned** for now —
Authenticode signing is issue #224. Because every command is idempotent,
re-invoking this skill after a failure resumes rather than restarts.

## Procedure

1. **Find the primary checkout and work there.** A mAIestro Code-spawned session runs
   in a *feature* worktree that has no `.env.release` and must never be released
   from. Run `git worktree list`; the **first** entry is the primary checkout.
   Prefix every command below with `cd <primary-checkout> && …` (or verify you
   are already in it). Do **not** switch this session's branch. Note which
   platform this machine is (macOS or Windows): it builds and publishes only
   its own assets.

2. **Confirm preconditions on the primary checkout.**
   ```
   git -C <primary> branch --show-current      # must be: main
   git -C <primary> status --porcelain          # must be empty
   git -C <primary> fetch origin && git -C <primary> pull --ff-only origin main
   ```
   If the branch isn't `main` or the tree is dirty, stop and tell the user.

3. **First or second machine?** Read the version on `main`
   (`backend/tauri.conf.json`) and check whether its tag exists on origin
   (`git -C <primary> ls-remote --tags origin v<version>`) and its release state
   (`gh release view v<version> --repo <owner/repo> --json isDraft,assets`).
   - **Tag exists and the release is a draft** → the other machine already
     started this release. Check out the tagged commit if `main` has moved on
     (`git -C <primary> checkout v<version>` — `publish` refuses any other
     commit; switch back to `main` once published), then **skip to step 7**.
     Don't bump, don't write notes.
   - **Tag exists and the release is published** → that version is done; a
     new release starts at step 4.
   - **No tag** → a new release: continue with step 4.

4. **Determine the bump kind.** From the skill args (`/release minor`,
   `/release 1.2.0`) if given, else ask with AskUserQuestion among `patch`,
   `minor`, `major`. `patch` is the default for a routine release.

5. **Draft release notes.** Find the previous tag
   (`git -C <primary> describe --tags --abbrev=0` — none means this is the first
   release) and read the commits since it (`git -C <primary> log <prev>..HEAD
   --first-parent --pretty='%s'`, or the last 30 commits when there is no prior
   tag). Write brief, internal-facing markdown notes (this is a solo tool — no
   localization, no character limits). Group user-visible changes; drop pure
   chore/CI noise. End with a per-platform line, e.g. *macOS (Apple silicon +
   Intel): signed and notarized universal .dmg. Windows (preview, unsigned — SmartScreen will warn): x64
   installer.* Windows stays "preview" until #160 closes and "unsigned"
   until #224 lands. **Show the draft and get approval** via AskUserQuestion
   ("Looks good, publish" vs "I'll tweak the wording") before touching anything.
   The notes are set once, by whichever machine creates the draft.

6. **Bump on a release branch, then merge it via PR.** `main` is PR-only — a
   local `pre-push` hook and a GitHub branch ruleset both reject a direct push,
   and the release commit is no exception.
   ```
   cd <primary> && git checkout -b release/v<new-version>
   cd <primary> && scripts/release.sh bump <kind-or-version>
   git -C <primary> commit -am "chore(release): v<new-version>"
   git -C <primary> push -u origin release/v<new-version>
   gh pr create --repo <owner/repo> --base main --head release/v<new-version> \
     --title "chore(release): v<new-version>" --body "<one line + the notes>"
   ```
   `bump` moves `tauri.conf.json`, `package.json`, `Cargo.toml`, and
   `Cargo.lock` together and asserts they agree. Then merge once CI is green —
   the ruleset requires **all** CI checks to pass and zero approvals, so until
   then `gh pr merge` fails with *"the base branch policy prohibits the
   merge"*:
   ```
   gh pr checks <pr-number> --watch
   gh pr merge <pr-number> --merge
   git -C <primary> checkout main
   git -C <primary> pull --ff-only origin main
   git -C <primary> branch -d release/v<new-version>
   ```
   Everything below runs from this merged `main`, so the tag `publish` creates
   points at the released commit. If CI fails, fix it on the release branch and
   re-run this step — no need to redo the bump.

7. **Build this machine's assets:**
   ```
   cd <primary> && scripts/release.sh build
   ```
   On the Mac this builds one universal (arm64 + x86_64) app, checks both
   slices are present, and signs and notarizes it (slow — a round-trip to
   Apple). On
   Windows it builds the x64 installer (unsigned). `--platform` defaults to the host.

8. **Publish.** Write the approved notes to a temp file (first machine only),
   then:
   ```
   cd <primary> && scripts/release.sh publish --notes-file <tmp>   # first machine
   cd <primary> && scripts/release.sh publish                      # second machine
   ```
   This tags `v<version>` (or checks the existing tag is `HEAD`), finds or
   creates the draft, uploads this platform's assets, and publishes if that
   completed the set. Otherwise it prints what's still missing and the draft's
   URL.

9. **Report** the version, the release URL, and whether it is **published**
   or still a **draft waiting for the other machine** — in that case tell the
   user to run `/release` on the other machine (it lands in step 3's
   second-machine path). If any phase failed, say which one — re-running the
   skill resumes from there.

   Shipping without one platform is an explicit decision, never a default:
   only if the user asks, run `scripts/release.sh finalize --allow-missing
   <asset-key>` (repeatable), which publishes the draft and appends the
   omission to the notes.

## Command reference

`scripts/release.sh` is the release pipeline, split into idempotent commands so
a partially-failed release resumes by re-running it:

- **`bump <patch|minor|major|X.Y.Z>`** — version is single-sourced from
  `backend/tauri.conf.json`; this bumps it there plus `package.json`,
  `backend/Cargo.toml` and the `maiestro` entry of `backend/Cargo.lock`, and
  asserts all four agree. It does not commit.
- **`build [--platform macos|windows]`** — macOS: sources `.env.release`,
  validates the `APPLE_SIGNING_IDENTITY` and the `aarch64-apple-darwin` /
  `x86_64-apple-darwin` Rust targets, runs `pnpm tauri build --target
  universal-apple-darwin` (Tauri auto-notarizes when the Apple credentials are
  present), checks with `lipo` that the binary carries both the `arm64` and
  `x86_64` slices, verifies the signature / Gatekeeper assessment / notarization staple, and notarizes +
  staples the `.dmg`. Windows: `pnpm tauri build --target <triple> --bundles
  nsis` for `x86_64-pc-windows-msvc`, unsigned (ARM64 is #232).
  Both set `MAIESTRO_RELEASE=1` so the About panel shows the clean version.
- **`publish [--platform macos|windows] [--notes-file <file>] [--prerelease]`**
  — reads the version, derives `owner/repo` from the `origin` remote, checks
  this platform's assets (macOS: `stapler validate` on the `.dmg`; Windows: the
  installers exist), then:
  1. **Tag.** Fetches `v<version>` from origin if the other machine pushed it,
     and refuses unless it points at `HEAD` — so the two machines can never
     ship different commits under one version. Otherwise creates and pushes it.
  2. **Draft.** Reuses the release for the tag, else creates it as a draft
     with the notes. Drafts are invisible to `GET /releases/tags/<tag>`, so the
     lookup lists releases and matches `tag_name`. A **race guard** re-lists
     after creating and keeps the oldest draft (deleting its own if it lost).
  3. **Upload** this platform's assets, skipping any already attached in state
     `uploaded` and deleting a same-named `starter` corpse left by a failed
     upload.
  4. **Finalize** (below).

  The order matters because the repo has GitHub's **immutable releases** on,
  which freezes a release *and its assets* the moment it is published — an
  asset not yet attached can never be added (the upload returns HTTP 422
  "Cannot upload assets to an immutable release", and the release can't be
  edited afterwards, only deleted). It talks to GitHub via the **REST API**
  (`curl` + `GITHUB_TOKEN` from `.env.release`), not `gh`, matching the
  backend's "Talk to GitHub directly" decision, and refuses a dirty tree.
  `--prerelease` marks a newly created release as a pre-release (dry runs).
- **`finalize [--allow-missing <asset-key>]...`** — re-reads the draft's
  assets from the API and publishes only if every expected asset (`macos`,
  `windows-x64`) is attached in state `uploaded`; otherwise
  prints what's missing and leaves the draft. `--allow-missing` publishes
  without that asset and appends *"Not included in this release: …"* to the
  notes. `publish` runs this automatically.

The expected asset set is one list (`ALL_ASSET_KEYS`) in `scripts/release.sh`;
adding a platform means adding a key there and to its case statements.

Run `scripts/release.sh` with no args to see the usage from the shell.

## Release machines

- **Mac:** a Developer ID Application certificate in the login keychain, the
  Rust targets for the universal build (`rustup target add
  aarch64-apple-darwin x86_64-apple-darwin`), notarization credentials and `GITHUB_TOKEN` in `.env.release`.
- **Windows PC:** Git Bash (the supported shell — not WSL or PowerShell),
  Python 3 (`python3`, `python` or `py -3`, whichever really runs), Node +
  pnpm, Rust (MSVC toolchain) with Visual Studio's C++ build tools, and
  `GITHUB_TOKEN` in `.env.release`. The manually run **Windows installer**
  workflow installs, exercises and uninstalls the installer
  (`scripts/smoke-test-installer.ps1`, also runnable locally). It doesn't run on PRs, so trigger it before a release:
  `gh workflow run windows-installer.yml --ref <branch>`.

## Code signing (and why it also governs Keychain trust on macOS)

Beyond distribution, the Developer ID signature is what makes the app's Keychain
access usable: macOS binds a Keychain item's "Always Allow" decision to the
app's *designated requirement*. For an ad-hoc/unsigned build that requirement is
the binary's cdhash, which changes on every rebuild — so the access prompt
returns each launch. A stable Developer ID signature anchors the requirement to
the certificate, so the grant persists.

Dev builds (`tauri dev`) run the raw, ad-hoc-signed binary and will re-prompt on
each rebuild — that is expected and accepted. Signing is **not** committed to
`tauri.conf.json`; the signing identity and notarization secrets live in a
gitignored `.env.release` (template: `.env.release.example`).

On Windows, Credential Manager access doesn't depend on a signature, so the
unsigned installers work; signing there only affects download trust and
SmartScreen. Issue #224 adds Azure Artifact Signing, through a `--config`
override at build time — still nothing signing-related in `tauri.conf.json`.

## Notes

- `bump` accepts `patch|minor|major` or an explicit `X.Y.Z`.
- `publish` / `finalize` require `GITHUB_TOKEN` in `.env.release` (Contents:
  read/write on this repo) on whichever machine runs them. `publish` refuses an
  un-notarized `.dmg`, a dirty tree, or a `HEAD` that isn't the release tag.
- Never release from a feature/spawned worktree — always the primary checkout:
  a spawned worktree has no `.env.release`.
- Never push the release commit straight to `main`; it goes through a PR like
  any other change. `git push --no-verify` gets past the local hook but not the
  GitHub ruleset.
