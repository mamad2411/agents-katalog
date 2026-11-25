---
name: git-submodule-missing-revision-recovery
description: Recover a registered Git submodule when `git submodule update --init` fails with "Unable to find current revision in submodule path" — by fetching the upstream into the submodule's local clone, clearing stray working-tree blockers, and checking out the recorded SHA directly.
category: Git & Repository Management
---

# Git Submodule Missing Revision Recovery Skill (v1)

This skill resolves the failure mode:

```text
fatal: Unable to find current revision in submodule path '<path>'
```

It occurs when the parent's tree records a submodule pointer SHA, the submodule entry is registered (`.git` is a
gitdir pointer to `<parent>/.git/modules/<path>`), but the submodule's **local** object database does not yet contain
the recorded SHA — typically because the submodule was added/registered without a successful initial fetch, or because
the upstream history was force-pushed and pruned.

This skill is **distinct** from
[`git-submodule-uninitialized-handler`](../git-submodule-uninitialized-handler/SKILL.md) — that skill assumes
`git submodule update --init --recursive` succeeds. This skill handles the case where it does not.

***

## 1. Environment & Dependencies

1. **Verify Git** (`>= 2.30`):

    ```bash
    git --version
    ```

    * `--version` — prints the git client version. Required because the gitdir-pointer layout used by submodules
      (`<parent>/.git/modules/<path>`) is the canonical layout from git 1.7.8+; all branches in this skill assume it.

2. **Position at the parent repo root** so submodule paths resolve correctly:

    ```bash
    cd "$(git rev-parse --show-toplevel)"
    ```

    * `rev-parse --show-toplevel` — prints the absolute path of the working tree root for the current repo. Wrapping
      it in `cd "$(...)"` guarantees subsequent relative paths (`<submodule-path>`) are interpreted from the parent
      repo, not from a nested subdirectory.

***

## 2. Diagnosis: Confirm the Failure Mode

Before mutating anything, prove this skill is the right one.

1. **Reproduce the failure** (read-only — `--init` only registers, the fetch/checkout is what fails):

    ```bash
    git submodule update --init -- <submodule-path>
    ```

    * Expected exit on the target failure mode:
      `fatal: Unable to find current revision in submodule path '<submodule-path>'`.
    * If the error is instead `No url found for submodule path`, the entry is missing from `.gitmodules` — route to
      [`git-submodule-orphan-gitlink-recovery`](../git-submodule-orphan-gitlink-recovery/SKILL.md) instead.
    * If the error is `Server does not allow request for unadvertised object` or HTTP 404, route to
      [`git-submodule-dead-upstream-audit`](../git-submodule-dead-upstream-audit/SKILL.md).

2. **Read the recorded pointer SHA from the parent's tree** (this is the ground truth for what the submodule MUST be
   checked out at):

    ```bash
    PAGER=cat git ls-tree HEAD <submodule-path>
    ```

    * `ls-tree HEAD <path>` — prints one line of the form
      `160000 commit <SHA>\t<path>`. Mode `160000` is the gitlink marker; the `<SHA>` is the recorded pointer.
    * `PAGER=cat` — bypasses the interactive pager so the output is captured cleanly in non-TTY contexts.
    * Capture `<recorded-sha>` for §4.

3. **Read the configured upstream URL** (so the fetch in §3 hits the right remote):

    ```bash
    git config -f .gitmodules --get submodule.<submodule-name>.url
    ```

    * `-f .gitmodules` — reads from the in-tree config file rather than `.git/config`, so the result reflects the
      committed URL even if `.git/config` is stale or missing.
    * `--get submodule.<name>.url` — the canonical key. `<name>` is the value between `[submodule "..."]` in
      `.gitmodules`, which is **not** always the path — verify with `git config -f .gitmodules --list | grep '\.url='`.

***

## 3. Phase 1: Fetch the Upstream into the Submodule's Local Clone

The recorded SHA is missing from the submodule's object DB. Fix the cause directly.

1. **Enter the submodule's working tree** (whose `.git` file points at `<parent>/.git/modules/<path>`):

    ```bash
    cd <submodule-path>
    ```

2. **Fetch all branches and tags from origin**:

    ```bash
    git fetch origin
    ```

    * `fetch origin` — downloads all refs from the configured remote and writes them under
      `refs/remotes/origin/*` in `<parent>/.git/modules/<path>/`. Critically, this populates the object database with
      every commit reachable from those refs, including `<recorded-sha>` if it is reachable from any branch tip.
    * Use `git fetch origin --tags` if the recorded SHA is referenced only by a tag (rare for submodules but possible).

3. **Verify the recorded SHA is now present**:

    ```bash
    git cat-file -t <recorded-sha>
    ```

    * `cat-file -t <sha>` — prints the object type (`commit`, `tree`, `blob`, `tag`). Expected: `commit`.
    * If it errors `fatal: Not a valid object name <sha>` even after `fetch origin`, the SHA is not reachable from any
      current branch — the upstream history was rewritten or the SHA exists only on a fork. Route to
      [`git-submodule-dead-upstream-audit`](../git-submodule-dead-upstream-audit/SKILL.md) for SHA-based fork
      discovery.

***

## 4. Phase 2: Checkout the Recorded SHA

`git submodule update` may still fail at this point if the working tree contains stray untracked files or has an
unborn HEAD (a residue of the failed initial init). Bypass by checking out the SHA directly.

1. **Clear stray untracked files** that would block checkout (CAUTION: only do this if the user has confirmed nothing
   in the submodule working tree is theirs to keep):

    ```bash
    git status --porcelain
    ```

    * `--porcelain` — stable, machine-parseable status output (`??` prefix = untracked).
    * If untracked files are present and the user confirms they are stub artifacts (e.g., a 1-line stub `README.md`
      auto-created during a failed `git submodule add`), remove them:

    ```bash
    rm -f <stray-file>
    ```

    * **Operational guard**: NEVER run `git clean -fdx` blindly here — that would delete legitimate user work. List
      the files, present them to the user, and remove only confirmed stubs.

2. **Checkout the recorded SHA in detached-HEAD mode** (matching what `git submodule update` would normally do):

    ```bash
    git checkout <recorded-sha>
    ```

    * Result: working tree is materialized at the recorded pointer; `HEAD` is detached (`(HEAD detached at <sha>)`),
      which is the canonical state for a submodule managed by its parent.

3. **Verify**:

    ```bash
    PAGER=cat git log --oneline -1
    PAGER=cat git rev-parse HEAD
    ```

    * Expected: `git rev-parse HEAD` prints `<recorded-sha>` exactly.

***

## 5. Phase 3: Confirm the Parent Sees a Clean Pointer

Return to the parent and confirm the submodule no longer reports as uninitialized or modified.

1. **Return to the parent**:

    ```bash
    cd "$(git rev-parse --show-superproject-working-tree)"
    ```

    * `--show-superproject-working-tree` — prints the parent repo's working-tree root when invoked from inside a
      submodule. Falls back to empty if the cwd is not a submodule.

2. **Status check**:

    ```bash
    PAGER=cat git submodule status -- <submodule-path>
    ```

    * Expected: a single line beginning with a single space (`  `) — meaning the working-tree SHA matches the recorded
      SHA.
    * A `-` prefix means uninitialized (recovery failed).
    * A `+` prefix means the working-tree SHA differs from the recorded SHA (you checked out the wrong SHA — re-do §4
      with the SHA from §2.2).

3. **Parent working-tree status**:

    ```bash
    PAGER=cat git status -- <submodule-path>
    ```

    * Expected: `nothing to commit` for that path. If the parent reports `modified content` or `new commits`, the
      submodule is not at the recorded SHA.

***

## 6. Failure-Mode Routing Table

| Symptom after §3.3                                       | Route to                                                                                                        |
| :------------------------------------------------------- | :-------------------------------------------------------------------------------------------------------------- |
| `cat-file -t <sha>` errors after `fetch origin`          | [`git-submodule-dead-upstream-audit`](../git-submodule-dead-upstream-audit/SKILL.md)                            |
| `fetch origin` itself errors with HTTP 404 / 403         | [`git-submodule-dead-upstream-audit`](../git-submodule-dead-upstream-audit/SKILL.md)                            |
| `fetch origin` errors with permission denied (SSH)       | [`git-submodule-fork-reconfigure`](../git-submodule-fork-reconfigure/SKILL.md)                                  |
| `.gitmodules` has no entry for the path                  | [`git-submodule-orphan-gitlink-recovery`](../git-submodule-orphan-gitlink-recovery/SKILL.md)                    |
| Recorded SHA exists, but checkout fails on tracked files | Resolve dirty state via `git stash` or user confirmation, then re-run §4.2.                                     |

***

## 7. Reference Worked Example

The recovery sequence that triggered this skill, reproduced verbatim for traceability:

```bash
# Symptom (from parent root)
$ git submodule update --init -- vercel-labs_agent-skills
fatal: Unable to find current revision in submodule path 'vercel-labs_agent-skills'

# Diagnosis
$ git ls-tree HEAD vercel-labs_agent-skills
160000 commit 73140fc5b3a214ad3222bcf557b397b3c02d11c1  vercel-labs_agent-skills
$ git config -f .gitmodules --get submodule.vercel-labs_agent-skills.url
https://github.com/vercel-labs/agent-skills.git

# Phase 1: fetch into submodule's local clone
$ cd vercel-labs_agent-skills
$ git fetch origin
$ git cat-file -t 73140fc5b3a214ad3222bcf557b397b3c02d11c1
commit

# Phase 2: clear stray stub, checkout recorded SHA
$ rm -f README.md          # confirmed stub from failed initial add
$ git checkout 73140fc5b3a214ad3222bcf557b397b3c02d11c1
HEAD is now at 73140fc Refine react-view-transition skill

# Phase 3: confirm parent sees clean pointer
$ cd ..
$ git submodule status -- vercel-labs_agent-skills
 73140fc5b3a214ad3222bcf557b397b3c02d11c1 vercel-labs_agent-skills (heads/main)
```

***

## 8. Related Skills

- [`git-submodule-uninitialized-handler`](../git-submodule-uninitialized-handler/SKILL.md) — bulk init when the
  recorded SHAs are already fetchable; this skill is the single-pointer escalation when bulk init fails.
- [`git-submodule-uninitialized-audit`](../git-submodule-uninitialized-audit/SKILL.md) — read-only classification of
  every uninitialized pointer.
- [`git-submodule-dead-upstream-audit`](../git-submodule-dead-upstream-audit/SKILL.md) — invoked when the upstream is
  unreachable or the SHA is unrecoverable from the configured remote.
- [`git-submodule-orphan-gitlink-recovery`](../git-submodule-orphan-gitlink-recovery/SKILL.md) — invoked when
  `.gitmodules` has no entry for the path.
- [`git-submodule-fork-reconfigure`](../git-submodule-fork-reconfigure/SKILL.md) — invoked when the configured remote
  is unreachable due to permissions and a fork is required.
