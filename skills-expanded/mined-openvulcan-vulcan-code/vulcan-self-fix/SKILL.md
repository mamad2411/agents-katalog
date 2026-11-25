---
name: vulcan-self-fix
description: Use when the user asked to fix a Vulcan Code problem on their own device from the feedback window. Clones the Vulcan Code repository into the directory the user chose, builds a Debug version, reproduces, fixes and verifies the problem, and opens a pull request only after the user confirms.
---

# Fix Vulcan Code on this device

The user started this conversation from Vulcan Code's feedback window. The first message names the problem, the
installed Vulcan Code version, the feedback id when the report was already sent, and the source directory, which is
this conversation's project directory. Work only inside that directory.

Two rules hold for the whole conversation:

- **Never touch the running Vulcan Code.** This conversation runs inside the user's installed (Release) Vulcan Code.
  Never stop, replace or edit its processes or its installation directory, and never use its data directory. The
  Debug build you make lives in this checkout's `output/` with its own data root and ports, so both run side by side.
- **Nothing leaves the device without the user's yes.** Pushing, forking and opening the pull request each wait for an
  explicit confirmation in this conversation. Never handle GitHub tokens: when authentication is needed, ask the user
  to run the login command in their own terminal.

## 1. Get the source

1. If the directory is empty, clone into it:
   `git clone https://github.com/OpenVulcan/vulcan-code.git .`
2. If it already holds a checkout, run `git status --porcelain` first. If the work tree is not clean, stop and ask
   the user what to do with those changes; never discard them. Otherwise `git fetch --all --prune` and check out an
   up-to-date `main`.
3. Read `AGENTS.md` at the repository root before changing anything, then the on-demand documents in
   `docs/contracts/` whose condition matches the area you will touch. They are binding; this skill does not repeat
   them. `CONTRIBUTING.md` describes the pull request.

## 2. Line up the version

Fix on `main`. If the problem does not reproduce on `main`, check out the tag of the installed version (for example
`v0.1.9`) and try again. If it reproduces only there, it is probably fixed already: tell the user it should disappear
with the next update, suggest noting that on the feedback, and stop unless the user wants to continue.

## 3. Prepare and build

1. `make init-system` once per machine. It installs the toolchain and can take a long time; tell the user before
   starting it. On Linux it may ask for the user's password through sudo: let the user type it, never ask for it in
   the conversation.
2. `make sync`, then build the Debug distribution: `make br` on Windows (it builds, then restarts only the Debug
   build in `output/`), or `make build` followed by `make run` on Linux and macOS. Run long builds in the background
   and report progress instead of waiting silently.
3. If a step fails, read the error and fix the cause; do not skip checks or edit `output/` by hand.

## 4. Reproduce, fix, verify

1. Reproduce in the Debug build. Prefer a failing automated test that captures the problem before changing code.
2. Make the smallest fix that solves the cause, following `AGENTS.md`.
3. Verify with targeted tests first (`cargo nextest run -p <crate>`, `npx vitest run <dir>`), then run
   `cargo fmt --all` and `node scripts/check.mjs rustfmt repository`, adding the `web` or `desktop` group when the
   WebUI or desktop shell changed. Show the user the commands and their results.
4. If the fix changes visible behavior, confirm it in the Debug build as well.

## 5. Prepare the pull request

1. Check the GitHub CLI with `gh auth status`. If it is missing or signed out, ask the user to install it or run
   `gh auth login` in their own terminal. Without gh, the user forks on github.com and you push to their fork.
2. Create a branch `fix/<feedback id or short topic>` and commit with a message in the repository's existing style
   (`git log --oneline -10` shows it).
3. Show the user, and wait for an explicit yes:
   - the changed files and `git diff --stat`, with the key hunks;
   - the pull request title and body, written from `.github/pull_request_template.md`: the problem, the cause, the
     fix, the verification commands and their results, `Feedback: <id>` (or `none`), and a note that the change was
     made with Vulcan Code's help.
4. Only after that yes: `gh repo fork --remote` when the user has no fork yet, push the branch, and open the pull
   request against `OpenVulcan/vulcan-code` `main` with `gh pr create`.

## 6. Link the feedback

When the first message gave a feedback id, link the new pull request to it with the `feedback` tool
(`{"action":"link_pr","feedback_id":"<id>","url":"<pull request URL>"}`), which asks the user to approve. Then tell
the user the pull request link and that replies arrive in the message center.
