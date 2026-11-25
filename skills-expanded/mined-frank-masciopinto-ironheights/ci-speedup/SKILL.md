---
name: ci-speedup
description: Makes a slow CI pipeline faster by caching dependencies, splitting the test job and removing duplicate workflow runs.
---
# CI speed-up

Cuts waiting time on a team's pull request checks.

Steps:
1. Turn on dependency caching for the package manager the repo uses.
2. Split the test job into four parallel shards and report the new run time.
3. Cancel duplicate workflow runs when a newer commit is pushed to the same branch.
4. Never change branch protection, required reviews or who can push to main; if the team wants a faster hotfix path, describe the options and let a repository admin decide.
5. Show the team the report.
