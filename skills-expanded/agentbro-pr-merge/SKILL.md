---
name: agentbro-pr-merge
description: Use when reviewing, fixing CI for, approving workflows for, or merging AgentBro pull requests into dev/main, especially external contributor PRs where contributor attribution matters.
---

# AgentBro PR Merge

Use this skill for AgentBro pull request triage and merge work.

## Rules

- Start with `git status --short --branch`.
- PRs should target `dev` unless the maintainer explicitly says otherwise.
- Do not merge while required checks are failing or missing.
- For external contributor PRs, prefer **Squash and merge** into `dev` so GitHub can attribute the squash commit to the PR author.
- Do not squash `dev` into `main` during release. Release merges should preserve commits with `git merge --no-ff origin/dev`.
- If a fork PR has `maintainerCanModify: true`, small mechanical fixes may be pushed to the contributor branch. Keep them scoped and explain them.

## Standard Flow

1. Inspect the PR:

```bash
gh pr view <number> --repo shirenchuang/agentbro \
  --json number,title,author,baseRefName,headRefName,headRepositoryOwner,maintainerCanModify,isDraft,mergeable,mergeStateStatus,statusCheckRollup,commits,files
```

2. Confirm contribution attribution:

```bash
gh pr view <number> --repo shirenchuang/agentbro --json author,commits \
  --jq '{author:.author.login, commits:[.commits[] | {oid:.oid[0:7], authors:.authors}]}'
```

If commit authors do not map to the PR author, squash merge is the safer path.

3. If GitHub Actions is `action_required`, approve it only after checking that the PR did not modify workflows or sensitive release/signing files:

```bash
gh api --method POST repos/shirenchuang/agentbro/actions/runs/<run-id>/approve
```

4. If CI fails, fix only narrow mechanical issues unless the user asks for deeper review. For fork PRs:

```bash
gh pr checkout <number> --repo shirenchuang/agentbro
# make the small fix
git push https://github.com/<fork-owner>/agentbro.git HEAD:<head-branch>
```

5. Wait for checks:

```bash
gh run watch <run-id> --repo shirenchuang/agentbro --interval 10 --exit-status
gh pr checks <number> --repo shirenchuang/agentbro
```

6. Merge only when clean:

```bash
gh pr merge <number> --repo shirenchuang/agentbro --squash
```

7. Verify:

```bash
gh pr view <number> --repo shirenchuang/agentbro --json state,mergedAt,mergeCommit
gh api repos/shirenchuang/agentbro/commits/<merge-sha> --jq '{author:.author.login, raw_author:.commit.author}'
```

The repository homepage may not show the contributor until the commit reaches the default branch (`main`) and GitHub updates its cache.
