# Secrets-Sync — AI Agent Instructions

## CRITICAL: Never Reference Private Repositories

**DO NOT add private repositories to `secrets-config.yml` or mention them in any PR, commit
message, comment, or documentation in this repository.**

This repository is **public**. Any repo name added to `secrets-config.yml` — including in PR
diffs, review comments, or commit messages — becomes permanently public record.

### Private repos that must NEVER appear here

Private repos must never be named in this repo. If you are unsure whether a repo is private,
**do not add it**. Ask the user to confirm first.

### What to do instead

If a private repo needs secrets distributed to it, the owner must handle that out-of-band
(manually via `gh secret set`, not via this sync workflow).

## Repository Purpose

Distributes GitHub Actions secrets and variables stored on this repository to target repositories via a sync workflow.
Only public repositories should be listed in `secrets-config.yml`.

## Alphabetical Ordering

Per `CONFIGURATION.md`, repository lists must be sorted alphabetically.
