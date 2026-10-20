---
name: follow-service-run-on-config-run-on
description: Set/edit RunsOn runner configuration — `.github/runs-on.yml` runner definitions and `runs-on:` labels in workflows — merging with the existing config
related:
  - follow-service-run-on
---

## Goal

Set/edit RunsOn runner configuration — `.github/runs-on.yml` runner definitions and `runs-on:` labels in workflows — merging with the existing config

## Scope

- Covers `.github/runs-on.yml`, `.github-private/.github/runs-on.yml`, and `.github/workflows/*.yml`
- If the stack is not deployed yet → do `workflows/setup-run-on/SKILL.md` first
- Does not include automatic commit/push

## Execute

### 1. Read Current Config

> Goal: Know the current runner config before editing

1. Read `.github/runs-on.yml` and workflows that already use `runs-on:`
2. Do `/deep-review-codebase` domain `review-config` if the config must be compared with the deployed stack
3. If no config is found → do `workflows/setup-run-on/SKILL.md` first

### 2. Define Runners

> Goal: runner definitions match the workload

1. Create/edit `.github/runs-on.yml` in the repo (Flex), e.g.:
   ```yaml
   runners:
     gpu-type1:
       family: ["g4dn", "g5"]
       image: ubuntu24-gpu-x64
       cpu: [4, 16]
       spot: price-capacity-optimized
       extras: ["s3-cache"]
   ```
2. For org-wide definitions/warm pools → use `.github-private/.github/runs-on.yml`
3. Pick `family`, `image`, `cpu`, `ram`, `spot`, `extras` per workload — check official docs if unsure

### 3. Update Workflow Labels

> Goal: jobs route to the right runners

1. Edit `runs-on:` in `.github/workflows/<file>.yml`, e.g. `runs-on: runs-on=${{ github.run_id }}/runner=gpu-type1`
2. If `runs-on.yml` is not used → specify labels directly, e.g. `runner=2cpu-linux-x64`, `cpu=`, `ram=`, `image=`, `spot=`
3. Always use `runs-on=${{ github.run_id }}` as the routing key to prevent the runner from being claimed
4. If creating a new workflow → follow `/follow-create-github-action`

### 4. Validate

> Goal: the config really works on the runner

1. Trigger `workflow_dispatch` or push a commit, then watch Actions logs
2. Confirm the instance launches per labels and cost/spot behavior is correct
3. If it fails → run `/deep-validate` then `/ask-me`

## Rules

- Edit only the necessary runner definitions/labels — never rewrite whole workflows
- Always use `runs-on=${{ github.run_id }}` in the routing key
- No automatic commit/push — let the user confirm

## Expected Outcome

- `.github/runs-on.yml` and workflow labels correct for the chosen Flex/Fleet mode
- The workflow runs successfully on the specified runner
