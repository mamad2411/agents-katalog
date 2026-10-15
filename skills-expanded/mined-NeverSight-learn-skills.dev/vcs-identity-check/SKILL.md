---
name: vcs-identity-check
description: >-
  Verifies the VCS author identity (name + email) is set correctly
  before committing, and recommends configuring commit signing
  (GPG or SSH) when it isn't already set up.
when_to_use: >-
  Use as a precondition before any commit (`git commit`, `hg commit`,
  `jj commit`, amend, reword); pairs with vcs-commit-msg. Triggers:
  «проверь git config», «проверь автора», «настрой подпись коммитов»,
  «check git identity», «verify commit author»,
  «configure commit signing», or any commit flow without prior
  verification in the session.
---

# vcs-identity-check

Verify the VCS identity before committing
so the commit is attributed correctly,
and recommend commit signing when it isn't configured.

## Procedure

1. Read the identity for the VCS in use:
   - git → `git config --show-scope --get user.name`
     and `git config --show-scope --get user.email`
     (`--show-scope` is git ≥2.26;
     it prints the scope —
     `local` / `global` / `system` —
     alongside the value);
   - hg → `hg config ui.username`,
     then split on the last `<…>` pair into name and email
     (e.g. `Petr Korobeinikov <pk@example.com>` →
     name `Petr Korobeinikov`, email `pk@example.com`);
     if there is no `<…>`,
     treat the whole string as name and the email as unset;
   - jj → `jj config get user.name` / `user.email`.
2. Check:
   - **name** is non-empty,
     has ≥2 whitespace-separated tokens,
     and is not a literal email.
     The two-token rule assumes First Last conventions;
     for users with a single-token mononym
     (some Indonesian or Icelandic naming patterns),
     accept the value on the user's explicit confirmation
     and skip this sub-check;
   - **email** is non-empty,
     contains exactly one `@`,
     with at least one character on each side.
3. Read signing config:
   - git → `git config commit.gpgsign`,
     `git config tag.gpgsign`,
     `git config user.signingkey`,
     `git config gpg.format`;
   - jj → `jj config get signing.behavior`
     and `jj config get signing.backend`.

   Classify into one of three states:
   - **Configured** —
     `commit.gpgsign=true`,
     `user.signingkey` non-empty,
     `gpg.format` set
     (missing `tag.gpgsign=true` is a soft warning, not broken);
   - **Not configured** —
     `commit.gpgsign` unset or `false`,
     and `user.signingkey` empty;
   - **Broken** —
     anything else
     (e.g. `commit.gpgsign=true` with empty `user.signingkey`) —
     commits will fail to sign at runtime.

   This step is informational
   and does not block the commit by itself.
4. **Short-circuit when prior commits already match.**
   If the same author has a prior commit in this repo
   whose signing intent matches the current config,
   skip the confirmation in step 5 and the signing recommendation —
   the user has implicitly validated this setup before
   by committing under it.

   For git, run
   `git log -1 --author="<email>" --pretty=format:'%G?'`
   and treat as a match when:
   - prior commit carries a signature (`%G?` ≠ `N`)
     and current signing is **Configured**; or
   - prior commit has no signature (`%G?` = `N`)
     and current signing is **Not configured**.

   This compares intent (sign / don't sign), not the key,
   so it works for GPG and SSH alike
   regardless of how `user.signingkey` is written
   (key ID, fingerprint, with or without `0x…` prefix,
   or a public-key file path).

   Anything else — no prior commit by this author,
   **Broken** state, or non-git VCS — falls through to step 5.
5. Show the resolved values and ask the user to confirm —
   «`<First> <Last>` <email> (from `<scope>`) —
   correct order, no typo?».
   `<scope>` is what git reported (`local` / `global` / `system`);
   for hg/jj, name the source file if available, otherwise omit.
   Order can't be detected automatically;
   confirmation is required.
   In the same message:
   - signing **Not configured** →
     include the recommendation from the **Signing** section below;
   - signing **Broken** →
     name the inconsistent settings explicitly
     and treat it as fix-now, not a suggestion.
6. If any identity check fails or the user rejects, stop.
   Do not proceed to the commit.

## Fix

- git, repo-local:
  `git config --local user.name "First Last"`
  (and `user.email`).
- git, global: same with `--global`.
- hg: `[ui] username = First Last <you@example.com>` in `~/.hgrc`.
- jj: `jj config set --user user.name "First Last"`
  (and email).

Re-run the checks after fixing.

## Signing

Signing commits is a good practice:
it lets reviewers verify a commit really came from the stated author,
and platforms like GitHub / GitLab / Gitea show a «Verified» badge
on signed commits.
Recommend it whenever it isn't configured.

Two formats; pick what fits the user's setup:

- **GPG** —
  the traditional path,
  works everywhere git is hosted;
  requires generating a GPG key and uploading the public key
  to the host's «GPG keys» settings.
- **SSH** —
  reuses an existing SSH key,
  no extra tooling beyond `git` ≥2.34 and `ssh-keygen`;
  fits well when GPG isn't already in use.
  Requires uploading the public key as a «signing key»
  (separate from the auth key) on the host.

Setup (git, global):

GPG:

```sh
git config --global gpg.format openpgp
git config --global user.signingkey "<KEY-ID>"
git config --global commit.gpgsign true
git config --global tag.gpgsign true
```

SSH:

```sh
git config --global gpg.format ssh
git config --global user.signingkey "<path-to-public-key>"
git config --global commit.gpgsign true
git config --global tag.gpgsign true
```

Then upload the public key to the host's signing-keys settings.
