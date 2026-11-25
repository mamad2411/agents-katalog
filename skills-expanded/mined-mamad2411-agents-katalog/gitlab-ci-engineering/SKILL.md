---
name: gitlab-ci-engineering
description: Build reliable GitLab CI pipelines. Use when authoring or debugging
  .gitlab-ci.yml pipelines.
metadata:
  tags: gitlab, ci, engineering
---

# GitLab CI Engineering

## Use this skill when
- Authoring pipelines with jobs, stages, and rules
- Using templates and reusable CI components
- Debugging pipeline runs

## Do not use this skill when
- Other CI platforms
- Generic pipeline design (use cicd-engineer)

## Instructions
1. Keep stages sequential and minimal; use rules to gate jobs.
2. Use includes/components to avoid duplication.
3. Set rules with explicit when: (always/on_success/on_failure/manual).
4. Cache dependencies with proper keys; use artifacts between stages.
5. Assign runners with constraints and visibility.
6. Store secrets in CI/CD variables (masked/protected).
7. Use needs for the DAG when stages alone are too coarse.

## Checklist
- Rules unambiguous
- Secrets masked
- Artifacts sized sensibly

## Output Format
- Pipeline layout | rules | cache/artifacts | variable map

## Common Mistakes
- Catch-all rules that run prod jobs on forks
- Duplicated config pasted everywhere
- Plain-text secrets in yaml
