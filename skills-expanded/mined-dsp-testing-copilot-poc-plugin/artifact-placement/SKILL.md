---
name: artifact-placement
description: Create an issue with generated artifacts from a task.
---

# Artifact Placement Skill

This skill takes artifacts produced by a prior computation and creates an issue to share them.

## Inputs

1. `task_name`: Name of the task
2. `task_description`: One-line description of the task
3. `artifacts`: List of artifact file paths to include

## Workflow

1. Create a new issue with title: `[$task_name] Results for $DATE`
    - Replace `$task_name` with the actual task name
    - Replace `$DATE` with today's date in YYYY-MM-DD format
    - Set the body to:
        - the one-line task description
        -  For each artifact, create a `<details>` block with the artifact filename as the summary
            - If the artifact contents is markdown, render it as markdown; otherwise, include it in a code block.

3. Add the `Dreaming` label to the issue.

Example comment structure for markdown:

```
<details>
<summary>artifact-name.md</summary>

[artifact contents here]
</details>
```

Example comment structure for code:

```
<details>
<summary>artifact-name.json</summary>

\`\`\`
[artifact contents here]
\`\`\`
</details>
```

Use the GitHub API tools to create the issue and add comments with artifact contents.
