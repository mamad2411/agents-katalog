---
name: delete
description: alias → /apply delete (safe file/folder deletion — dry-run, confirm, update references)
argument-hint: "[scope]"
related:
  - apply
  - delete-cicd-fails
  - delete-git-branch
  - delete-git-submodules
  - delete-git-worktree
  - delete-projects
  - delete-project-temp
---

## Goal

Alias of `/apply` mode `delete` — safely delete the specified files or folders by checking impact, asking for confirmation, backing up when needed, and updating references

## Scope

Use when the user invokes `/delete` — this skill is only an alias stub; the real workflow lives in `apply` (`### Mode: Delete`)

For domain-specific deletes, invoke the skills directly: `/delete-cicd-fails`, `/delete-git-branch`, `/delete-git-submodules`, `/delete-git-worktree`, `/delete-projects`, `/delete-project-temp`

## Execute

Run the full `/apply` mode `delete` workflow

## Rules

- Never duplicate the `/apply` workflow in this file
- If the alias is missing steps → always read `apply/SKILL.md`

## Expected Outcome

- `/apply` mode `delete` is executed through every step — targets deleted + no broken refs + rollback possible
