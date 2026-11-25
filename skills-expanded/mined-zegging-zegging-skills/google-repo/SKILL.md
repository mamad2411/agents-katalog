---
name: google-repo
description: Use google-repo to coordinate development across multiple independent git repositories through a manifest. Use when the user needs to work in many repos at once, asks how to keep multi-repo versions reproducible, mentions Google's `repo` tool, `manifest.xml`, AOSP-style workflow, or wants an alternative to git submodule / monorepo / Nx for repos that stay independent. For terminology see `GLOSSARY.md`; for XML rules see `MANIFEST_REFERENCE.md`; for failures see `TROUBLESHOOTING.md`.
---

# google-repo

`google-repo` (Google's [`repo`](https://gerrit.googlesource.com/git-repo/) tool) coordinates many independent git repositories through a single **manifest** — a versioned XML file that says which repos exist and at which **revision** each one sits. One `repo init && repo sync` materializes the whole **workspace**; one **manifest** commit captures one reproducible **snapshot**.

Use `google-repo` when:

- Multiple repos must be checked out together, but each stays independently owned and released.
- Reproducing "what was deployed on date X" matters and you cannot collapse to a monorepo.
- Submodules feel too rigid (their lock is implicit in the parent commit; cannot describe ad-hoc combinations cleanly).

Do not use `google-repo` when:

- Repos share code at the source level and benefit from a real build graph — reach for monorepo tooling.
- There are only two repos and one strictly owns the other — submodule is simpler.

Terms in **bold** below are defined in `GLOSSARY.md`.

## Mental model — the three planes

Hold these apart; conflating them is the most common source of confusion:

1. **Manifest plane** — one git repository whose only job is to hold `default.xml` (and optionally named snapshot files). Every commit on this repo is a **snapshot** of "which project at which revision".
2. **Workspace plane** — a local directory where `repo` materializes the projects described by the manifest. Contains `.repo/` (machinery) plus one subdirectory per project.
3. **Project plane** — each individual git repo, living as a subdirectory of the workspace, behaving as a normal git repo for day-to-day work.

Daily development happens on the **project plane** with standard git. The **manifest plane** changes only when the baseline of "which combination is canonical" changes, or when locking a snapshot.

## Phase 1 — Bootstrap a workspace

The user starts a multi-repo task. Set up the workspace once; reuse it for the lifetime of the task.

### Steps

1. **Pick or create a manifest repository.** A small, dedicated git repo (private is fine) that holds `default.xml`. One manifest repo per long-lived workspace; do not put business code in it.
2. **Write `default.xml`.** Minimal shape:

   ```xml
   <?xml version="1.0" encoding="UTF-8"?>
   <manifest>
     <remote name="origin" fetch="<base URL of your git host>" />
     <default remote="origin" sync-j="4" />

     <project name="<group>/<repo-a>" path="repo-a" revision="refs/heads/main" />
     <project name="<group>/<repo-b>" path="repo-b" revision="refs/heads/main" />
   </manifest>
   ```

   Always use the `refs/heads/<branch>` form for revisions during development, never the bare branch name — `repo` may otherwise treat it as a tag. See `MANIFEST_REFERENCE.md` for full syntax rules, including the XML escaping pitfalls that break `repo sync`.
3. **Validate the XML locally before pushing.** Any XML parser will do (`xmllint --noout default.xml`, `python -c 'import xml.etree.ElementTree as E; E.parse("default.xml")'`). A manifest that fails to parse breaks every workspace that syncs it.
4. **Commit and push the manifest** to its remote.
5. **Initialize the workspace** in an empty directory:

   ```bash
   repo init -u <manifest-repo-URL> -b <manifest-branch>
   repo sync -c -j4
   ```

   `-c` fetches only the current branch (not all branches) per project — strongly recommended.
6. **Verify** the workspace contains one subdirectory per `<project>`, each on the revision declared in the manifest.

### Completion criterion

- [ ] `repo list` prints every project from the manifest.
- [ ] For each project, `git -C <project> rev-parse HEAD` resolves and matches the revision the manifest pointed at (allowing fast-forward if revision is a branch).
- [ ] Re-running `repo sync -c` is a no-op.

## Phase 2 — Daily development

Cross-repo work happens here. Treat the workspace as N independent git repos that happen to live as siblings.

### Steps

1. **Create work branches with `repo start`, not `git checkout -b`.**

   ```bash
   repo start <branch-name> --all          # all projects
   repo start <branch-name> <project>      # just one project
   ```

   `repo start` branches off the manifest's declared revision for each project. This is the only correct way to escape **detached HEAD** — `repo sync` leaves projects detached on purpose.
2. **Edit, commit, push per project, normally.** Each project is a standalone git repo; `git add / commit / push` work as usual. There is no cross-project atomic commit — that is a property of monorepos, not of `google-repo`.
3. **Use the manifest's remote name, not `origin`.** `repo` creates each project's git remote using the `name` attribute from `<remote>` in the manifest. If the manifest declares `<remote name="origin" …>`, the git remote is `origin`; if it declares `<remote name="company" …>`, the git remote is `company`. `git fetch origin` fails when the manifest's remote is named otherwise. See `GLOSSARY.md` → "Two kinds of remote".
4. **Cross-repo commits share a marker, not a transaction.** Put the task ID in every commit message; cross-reference the resulting MRs/PRs in their descriptions; lock the combined state via a snapshot (Phase 4) once merged.

### Completion criterion

- [ ] Every project that needs a code change is on a named work branch (verify with `repo branches`), not detached HEAD.
- [ ] Commits exist on those branches with a shared identifier (task ID) in the message.
- [ ] Each touched project has been pushed to its remote.

## Phase 3 — Review and merge

Submit one MR/PR per touched project, cross-referenced, merged in dependency order.

### Steps

1. **Open one MR/PR per touched project**, all with the same source-branch name (the one from `repo start`).
2. **Cross-reference** in each description: list the sibling MR/PR URLs and the manifest-repo URL. This is how a reviewer reconstructs "what cross-repo change does this belong to".
3. **Merge in dependency order**: providers before consumers. The platform cannot enforce this; it is on the author.
4. **Pull updated baselines** after each merge:

   ```bash
   repo sync -c          # picks up the merged commit on the manifest's revision
   ```

### Completion criterion

- [ ] Every touched project has a merged MR/PR.
- [ ] Each MR/PR description names its siblings and the manifest repo.
- [ ] CI is green on each project's default branch after the merges.

## Phase 4 — Lock the snapshot

After a delivery, freeze the exact combination so it can be reproduced.

### Steps

1. **Capture current HEADs** by letting `repo` rewrite the manifest with concrete SHAs:

   ```bash
   repo manifest -r -o snapshots/<date-or-label>.xml
   ```

   `-r` replaces each project's `revision` with its current HEAD SHA. The output is a complete, self-contained manifest file.
2. **Commit the snapshot file** to the manifest repo. Tag the commit with a meaningful name (release name, incident date, task ID).
3. **Verify reproducibility** in a separate directory:

   ```bash
   repo init -u <manifest-URL> -b <tag> -m snapshots/<file>.xml
   repo sync -c -j4
   ```

   Each project's HEAD must equal the SHA in the snapshot file.

### Completion criterion

- [ ] A snapshot file exists in the manifest repo with every project pinned to a concrete SHA.
- [ ] A tag or named ref points at the manifest commit that introduced the snapshot.
- [ ] A clean re-init in an empty directory reproduces the snapshot bit-for-bit.

## Phase 5 — Adjust the manifest

When the baseline changes (a project moves to a new long-lived branch, a repo joins or leaves the set, a revision must point at a different ref), edit the manifest — not the workspace.

### Steps

1. **Edit `default.xml`** in a clone of the manifest repo (not in `.repo/manifests/` inside a workspace — that copy is `repo`-managed).
2. **Validate the XML locally** before pushing (see Phase 1, step 3).
3. **Commit and push.**
4. **In each workspace**, run:

   ```bash
   repo sync -c
   ```

   `repo sync` first pulls the latest manifest, then reconciles each project. Existing work branches created via `repo start` are rebased onto the new revision automatically; uncommitted changes block the rebase and must be stashed or committed first.

### Completion criterion

- [ ] The new manifest is the HEAD of its branch on the remote.
- [ ] Every workspace that runs `repo sync -c` ends up with the new revisions checked out.
- [ ] Work branches are rebased onto the new baseline, or the user explicitly chose to `repo abandon` and recreate them.

## Reproducing a historical snapshot

To bring up the exact state from a past snapshot in a fresh directory:

```bash
repo init -u <manifest-URL> -b <snapshot-tag-or-branch>
repo sync -c -j4
```

Or pin to a specific snapshot file:

```bash
repo init -u <manifest-URL> -b <manifest-branch> -m snapshots/<file>.xml
repo sync -c -j4
```

Do this in a **separate directory**, never in an active workspace — `repo init` repoints the workspace and replaces the work-branch baseline.

## Handing the workspace to another agent

The whole workspace is encoded in three values: manifest URL, manifest ref, target directory. Anyone (human or agent) with those three plus network access reproduces the exact same workspace via:

```bash
repo init -u <manifest-URL> -b <manifest-ref>
repo sync -c -j4
repo start <work-branch> --all     # if they will commit
```

Place an `AGENTS.md` (or equivalent) at the root of the **manifest repo** describing the cross-repo conventions (commit-message prefix, merge order, anything project-specific). It travels with every workspace that syncs the manifest.

## Anti-patterns

- **Editing `.repo/manifests/default.xml` directly.** That file is `repo`-managed and overwritten on next sync. Edit in a clone of the manifest repo, push, then `repo sync`.
- **Committing on detached HEAD.** Use `repo start` first. A commit on detached HEAD is reachable only via reflog and can be lost by a later `repo sync`.
- **Renaming a project's `path`.** `repo sync` does not move existing directories; the old path lingers. If a path must change, plan a transition (rename in manifest, `repo sync`, manually delete the old directory in every workspace).
- **Moving a workspace directory.** Each project's `.git` is a symlink into `.repo/projects/`; moving the workspace breaks them. Re-init in the new location instead.
- **Treating a snapshot file as mutable.** Snapshots are append-only history. To revise a snapshot, write a new one and update the tag.

## Worked example

`examples/manifest-repo/` shows the file shapes a small three-project manifest repo takes — a `default.xml`, a release snapshot, an incident snapshot, an `AGENTS.md`, and a `README.md`. Read it as the target layout when creating a new manifest repo from scratch.

## When something goes wrong

See `TROUBLESHOOTING.md`, grouped by phase (init / sync / daily / manifest / platform).
