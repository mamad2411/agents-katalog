---
name: git-clone-repo
description: Clone a git repository with branch selection and shallow clone support
---

# Git Clone Repository

Clone a git repository with branch selection and shallow clone support

## When to Use

- User wants to git clone
- User wants to clone repo
- Keywords: git, clone, vcs, repository

## Required Parameters

- **repo_url** (string): Git repository HTTPS URL
- **target_dir** (string): Local target directory

## Output

- **success** (boolean): Clone success
- **path** (string): Cloned path
- **commit_hash** (string): HEAD commit

## Security

- Sandbox level: standard
- Max execution time: 180000ms
- Network whitelist: github.com, gitlab.com, bitbucket.org
- JadeGate verified: Yes (5-layer security check passed)

## Execution Flow

Entry: `validate_url` -> 6 steps -> Exit: `ret_ok`, `ret_fail`
