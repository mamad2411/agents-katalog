---
name: gh-pipeline-analyzer
description: Diagnose and debug failed GitHub Action runs using the gh CLI. Use when the user reports a pipeline failure or wants to analyze build errors on GitHub.
---

# GitHub Pipeline Analyzer

Expert in diagnosing GitHub Action failures. This skill automates the extraction of failure logs and identifies common error patterns in CI/CD pipelines.

## Workflows

### 1. Analyzing the Latest Failure

When asked why a build failed (e.g., "Why did the last build fail?"):

1.  **Check for Failures**: Use `gh run list --status failure --limit 3` to find the most recent failed runs.
2.  **Get Run Details**: Identify the `databaseId` of the relevant run.
3.  **Identify Failed Jobs**: List the jobs within the run that failed using `gh run view <run-id> --json jobs`.
4.  **Extract Logs**: For each failed job, fetch the logs:
    ```bash
    gh run view <run-id> --log --job "<job-name>"
    ```
5.  **Analyze**: Look for the specific error that caused the failure (e.g., compile error, test failure, missing dependency).

### 2. Monitoring Workflow Status

When asked about the status of a specific workflow:

1.  List workflows with `gh workflow list`.
2.  View the status of the chosen workflow with `gh workflow view <workflow-id>`.

## Resources

-   **Analysis Script**: `scripts/analyze_failure.sh` - Bash script to automate failure analysis and log extraction.
-   **Cheatsheet**: [gh-cli-cheatsheet.md](references/gh-cli-cheatsheet.md) - Reference for common GitHub CLI commands.

## Tips

-   **Authentication**: If `gh` reports auth issues, remind the user to run `gh auth login`.
-   **Verbose Logs**: If the error isn't clear, try viewing the full logs for the failing step.
