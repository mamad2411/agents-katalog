---
name: devops-pipelines
description: Azure DevOps CI/CD pipeline operations. Use when asked to list, trigger, monitor, or troubleshoot build and release pipelines.
---

# DevOps Pipelines

## When to Use

- User asks to run, trigger, or queue a build/pipeline
- User wants to check pipeline status or recent runs
- User needs to read build logs or troubleshoot failures
- User mentions CI/CD, builds, deployments, or releases

## Instructions

### Triggering a Pipeline

1. Find the pipeline by name using `devops_list_pipelines`
2. Use `devops_run_pipeline` with the pipeline ID
3. Optionally specify branch and template parameters
4. Always confirm before triggering production deployments

### Monitoring a Run

- Status values: `notStarted`, `inProgress`, `completed`
- Result values: `succeeded`, `failed`, `canceled`, `partiallySucceeded`

### Troubleshooting Failures

1. Use `devops_get_pipeline_run` to confirm the failure
2. Use `devops_get_build_log` to retrieve log content
3. Look for error patterns: compilation errors, test failures, dependency issues
4. Summarize the root cause and suggest a fix

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| "npm install failed" | Lock file conflict | Delete node_modules, regenerate lock file |
| "tsc exited with code 2" | TypeScript error | Check the error line in logs |
| "Test suite failed" | Failing tests | Read test output, identify failing test |
| "Timeout" | Build exceeds limit | Optimize build or increase timeout |

## Tools

- `devops_list_pipelines` — List all pipelines in a project
- `devops_get_pipeline` — Get pipeline details
- `devops_run_pipeline` — Trigger a pipeline run
- `devops_get_pipeline_run` — Get run status and details
- `devops_list_pipeline_runs` — List recent runs
- `devops_get_build_log` — Retrieve build log output

## See Also

- **devops-repos** — repository and PR management
- **devops-boards** — work items and sprints
