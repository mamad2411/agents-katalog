---
name: follow-tool-act
description: Use act (nektos/act) to run GitHub Actions workflows locally before push, reducing CI fails
argument-hint: "[workflow-or-job]"
related:
  - follow-tool-github-actions
  - resolve-errors
  - report

---

## Goal

Install and use `act` (nektos/act) to run GitHub Actions workflows on the local machine before push — reducing CI/CD failures and speeding up workflow debugging

## Scope

- Use when testing `.github/workflows/*.yml` without pushing
- Covers running full workflows, single jobs, event simulation, and secrets injection
- Boundary: use this skill only for running/debugging workflows locally — if the remote CI already failed, use `/resolve-github-actions-fails` instead; for writing/editing workflows themselves see `/follow-tool-github-actions`
- Works together with `/resolve-github-actions-fails` (watching and fixing remote fails)

- Latest: `act@0.2.89` (nektos/act) (verified 2026-09-13)
- References: [apis](references/apis.md) | [cli](references/cli.md) 
## Execute

### 1. Install act

> Goal: `act` ready to use

1. Check `act --version`
2. If missing → install via `download-program/workflows/package-manager`: try `mise use -g act` first, then `scoop install act` or `winget install nektos.act`
3. Verify the Docker daemon is running (`docker info`) because `act` runs jobs in containers

### 2. Inspect Workflows

> Goal: know what to run

1. Confirm `.github/workflows/*.yml` exists and parses correctly (valid YAML)
2. Run `act -l` or `act --list` to see all simulatable jobs
3. Pick the workflow/job from the argument or the `act -l` output
4. If the job is unclear → ask the user which workflow to run

### 3. Prepare Inputs And Secrets

> Goal: simulate the event and provide all secrets

1. Create an event payload when needed: `act <event> -e event.json` (pull_request, push, workflow_dispatch)
2. Provide secrets with `-s KEY=value` or `--secret-file .env.act` — pull values via `/follow-secret-manager`, never hardcode
3. Use `--var` for GitHub variables and `-W` to select a specific workflow file

### 4. Run Workflow Locally

> Goal: run and read the result

1. Run `act <event>` for the full workflow or `act <event> -j <job>` for a single job
2. Use `-n` (`--dryrun`) first to view the execution plan without running
3. Use `--container-architecture linux/amd64` on ARM machines
4. If the image is large → use `-P ubuntu-latest=ghcr.io/catthehacker/ubuntu:act-latest` (medium image)

### 5. Debug Failures

> Goal: find the root cause when a job fails

1. Read the failing step's log — compare against the real runner environment
2. Use `-v` (verbose) when the log is insufficient
3. Distinguish workflow bugs from act limitations (services, non-ubuntu `runs-on`, GitHub-specific contexts)
4. If the failure comes from the workflow → fix `.github/workflows/*.yml` and re-run
5. If it is an act limitation → document it and handle it remotely via `/resolve-github-actions-fails`

### 6. Report

> Goal: summarize before the real push

1. Produce a `/report` with columns: `No.`, `Workflow`, `Job`, `Result`, `Duration`, `Note`
2. State which jobs passed locally and the confidence they will pass remotely
3. If everything passes → ready to push; otherwise → run `/resolve-cicd`

## Rules

### 1. Dry Run First

- Always run `act -n` first to view the plan
- Run only the changed job — no need to run every workflow

### 2. Secrets Safety

- Never commit `.env.act` or secrets files — add them to `.gitignore`
- Use dummy values for secrets the workflow only consumes
- Never log secret values

### 3. Know The Limits

- `act` does not support every GitHub feature: some reusable-workflow patterns, OIDC, hosted runner services
- Windows/macOS jobs usually cannot run in containers — skip them and run on the remote
- If act cannot do it → fall back to `/resolve-github-actions-fails`

- Use /follow-tool-github-actions if needed (tool act)
- Use /resolve-github-actions-fails if needed
- Use /resolve-cicd if needed
- Use /resolve-errors if needed


- See best-practices/ for recommended patterns and pitfalls

## Expected Outcome

- `act` installed and running workflows locally
- Knowing before push whether a workflow will pass or fail
- Secrets handled safely with no leakage into the repo
