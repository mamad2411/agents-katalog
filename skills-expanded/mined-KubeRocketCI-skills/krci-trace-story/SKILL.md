---
name: krci-trace-story
description: The implementation status of a story by its tracker key, per project — whether it merged, its first version, and which environments run it. Use when asked about the status or progress of a story or ticket key, which version contains it, or its deployment. Not for why an environment itself is unhealthy or empty, which `krci-debug-environment` covers.
license: Apache-2.0
compatibility: Requires the krci CLI v0.20.0 or later with a portal session, and git with read access to the project repositories. A tracker integration is optional. Written against KubeRocketCI 3.15.
metadata:
  access: read-only
  roles: ba, po, pm, dev, qa
  stage: plan
---

# Trace a story to its deployed version

At the end you know, per project a story touched: whether its commit merged, the first version that shipped it, and which environments run that version or a later one containing it. For BA, PO, PM, developers, and QA who need a story's status across every project and environment.

Platform vocabulary and the safety contract come from `krci-overview`. Run its preflight before the first krci call.

## Inputs

| Input | Where it comes from | If it is missing |
|---|---|---|
| Story key | the user, or the ticket already open | ask |
| Every project name and its repository | `krci project list -o json` (`name`, `gitUrl`) | stop, there is nothing to search |
| Ticket status and epic | the agent's own tracker integration, if one is configured | note it is missing and continue from Git |

## Steps

1. Read the story from the tracker through the agent's own integration, if one is configured: status and epic. Read-only: nothing here updates the ticket, per `krci-overview`.
2. List every project with `krci project list -o json`, `name` and `gitUrl` per item. Search every project whatever its `type`, including `system` (the GitOps repository), not only the one the user names: a story can span several projects.
3. Clone or fetch each repository with tags, then search all branches: `git log --all -E --grep '<KEY>([^0-9]|$)'`. The trailing boundary keeps a shorter key from matching a longer one that starts with it (`SHOP-14` must not match `SHOP-142`). `git log --grep` searches the whole commit message, not only its first line, so confirm each match sits in the commit title before counting it. The key in a commit's title is the link. Enforcement is optional: a team adds a `commit-validate` task against the Codebase's `commitMessagePattern` to its review pipeline, and `krci-overview` states the default. A project without the pattern can still carry the key. No match: look for the key in merge request titles and branch names through the Git provider, and remember a squash merge rewrites the commits, dropping the original title. Without Git access to a repository, the Git provider's API answers the same questions — commits by message, tags containing a commit, ancestry — explore it instead of stopping.
4. Merged: the commit is reachable from the default branch — `git branch -r --contains <sha>`, or `git merge-base --is-ancestor <sha> origin/<default>`.
5. First version: `git tag --contains <sha> --sort=creatordate`, the oldest match. Map the tag to the version with the versioning table in `krci-overview`'s vocabulary reference, section "Delivery contract of an application repository": semver strips the `build/` prefix, default versioning uses the tag (`<branch>-<timestamp>`) as the version. No tag means no successful build.
6. Environments: `krci project deployments <project> -o json`, read `env`, `version`, `status`, `sync`, `operation` per row. Resolve the deployed version to a tag, `build/<version>` first, then `<version>`, and test `git merge-base --is-ancestor <sha> <tag>`: a later version that passes counts, one from a branch that never merged the commit does not, whatever its timestamp. `version` `"NaN"` means the environment never deployed. A failed `operation` or an unhealthy `status` means the version is not confirmed running, even when it passes the ancestry test.
7. Merged but no tag anywhere: `krci pipelinerun list --project <project> --type build -o json`, and find the run whose `commitSha` is the merge commit or whose `prNumber` is the merge request; with the merge request number known, `--pr <number>` applies that filter for you. `--branch` matches the run's own source branch, not the branch the merge lands on, so `--branch <default>` misses a build the merge itself started. A failed match: `krci pipelinerun get <run> --reason`.

## Output

One block per story: key, summary, tracker status. Then one block per project: commits, merged, first version, and one entry per environment in promotion order (`krci env list` order). Close with one status line from the ladder:

- Not started — no commit carries the key.
- In review — commits carry the key, but only outside the default branch.
- Merged, not built — the key is on the default branch, and no tag contains it.
- Built — a tag contains it, but no environment runs it.
- Deployed to `<env>` — the furthest environment in `krci env list` order whose version contains it.

```text
Story SHOP-142

orders (semver)
  commits: 3, on feature/shop-142 and main
  merged: yes
  first version: 1.4.0-SNAPSHOT.7
  dev: 1.4.0-SNAPSHOT.9 (contains)   qa: NaN (not deployed)
  status: Deployed to dev

payments
  commits: 1, on main
  merged: yes
  first version: none
  dev: not deployed   qa: not deployed
  status: Merged, not built
```

## Checks

- Each cell comes from one read-only command; rerun it to confirm a row: `git log`, `git tag --contains`, `git merge-base --is-ancestor`, `krci project deployments`.

## Common mistakes

- Inventing a mechanism that writes the version back to the tracker. The story key in a commit title is the only link; `krci-overview` covers why.
- Comparing version strings or semver order instead of Git ancestry. A higher-looking version can come from a branch that never merged the commit.
- Filtering `krci pipelinerun list` by `--branch <default> --type build` to find a merge's build. `--branch` is the run's source branch, not the branch the merge landed on.
- Enumerating projects with kubectl, or guessing one project name, instead of `krci project list`.
- Counting a `"NaN"` placeholder version, or a version with a failed `operation` or unhealthy `status`, as deployed.

## Further reading

- [Artifact versioning](https://docs.kuberocketci.io/docs/user-guide/artifact-versioning)
- [Build pipeline](https://docs.kuberocketci.io/docs/user-guide/build-pipeline)
