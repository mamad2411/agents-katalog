---
name: repo-summary-and-relation-mapping
description: Analyze a local repo, write a short objective summary, explain its relation to sibling repos, and produce a reusable local summary file under ~/.AGENTS-temp/<repo>/. Use when organizing multiple repos, reducing repo sprawl, or deciding what belongs in code repos versus skills.
---

# Repo Summary And Relation Mapping

Use this skill to summarize a repo’s purpose and its relationship to nearby repos.

## Use when

- you need a 3-5 line objective for a repo
- you need to explain how one repo relates to sibling repos
- you are planning repo consolidation, decomposition, or cleanup
- you want a reusable local summary file for later migration work

## Do not use when

- you only need a code walkthrough for one module
- the task is to edit application code rather than classify repo boundaries

## Output rule

Do not write summaries to `/tmp`.

Write local summary files under:

```bash
~/.AGENTS-temp/<repo-name>/
```

Recommended file:

```bash
~/.AGENTS-temp/<repo-name>/repo-summary.md
```

## Main script

### Collect repo facts

```bash
bash scripts/collect-repo-facts.sh \
  <repo_path> [related_repo_path...]
```

This script gathers:
- git branch
- git remote
- top-level files and directories
- presence of `README.md`, `ROADMAP.md`, `PLANS.md`, `AGENTS.md`
- short previews of those files when present

Use the script output as input to the human-written summary.

## Expected summary shape

Write:

1. repo object
2. main kinds of code/artifacts it should own
3. relation to sibling repos
4. what should move out to skills or temp

Keep it short and operational.

## Recommended workflow

1. run `collect-repo-facts.sh` on the target repo
2. read only the small set of files that define purpose and boundaries
3. write a short repo summary into `~/.AGENTS-temp/<repo-name>/repo-summary.md`
4. if sibling repos matter, include a short relation section:
   - overlaps
   - boundaries
   - migration direction

## Related repos

This skill is useful for repo sets like:

- `hcr`
- `trustdev`
- `patching`
- `packer`
- `infra`
- `agent-skills`
- `awsops`

## Related skills

- use this before large repo decomposition work
- pair with `cis-*`, `ecs-*`, or `gitlab-triage` only when the repo contains those reusable workflows
