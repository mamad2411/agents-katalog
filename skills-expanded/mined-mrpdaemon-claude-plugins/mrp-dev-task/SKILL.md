---
name: mrp-dev-task
description: Manages development task artifact files and the git branch for the currently active development task. Use when asked to 'determine the current development task', 'write to task directory', 'list task files', 'determine changes done for the current development task' or any request involving reading/writing files to the task directory and determinining changes that have been done as part of the task.
---

We will be working on a specific development task. The name of the task we will be working on is specified by the `MRP_TASK` environment variable. If `MRP_TASK` is not set or is empty, **ask the user** for the name of the active development task. Store the name of the current task as {task_name}.

# Development Task File Management

Files representing artifacts related to the current development task are stored in a task-specific directory. The root path storing all task directories is specified by the `MRP_TASKS_DIR` environment variable. If this variable is not set or is empty, there is an issue with the user's configuration, ask the user to fix it by setting this variable. Store the value of the tasks directory as {tasks_dir}.

## Active Project

Task directories are scoped to a project so that tasks from different repositories do not share a single flat namespace. Store the active project name as {project_name}, and set {project_dir} to `{tasks_dir}/{project_name}`.

The active project is normally identified by the `MRP_PROJECT` environment variable, which is set in the user's shell when a task is bootstrapped. If `MRP_PROJECT` is not set or is empty, there is an issue with the user's configuration — ask the user to fix it by setting this variable (it is set as part of bootstrapping a task via the `mrp-new-task` skill or the `/linear-task` command). Take the value of `MRP_PROJECT` as `{project_name}`.

Bootstrap entry points (the `mrp-new-task` skill and the `/linear-task` command) do not rely on `MRP_PROJECT` and instead resolve `{project_name}` from the current repository using the procedure described in the next subsection.

### Resolving the active project from the current repository

This procedure derives `{project_name}` from the current repository, not from `MRP_PROJECT`. Any existing value of `MRP_PROJECT` is ignored when this procedure is used. It is invoked by the bootstrap entry points; everyday commands do not use it.

- Determine the current repository root (the top-level directory of the git repository containing the current working directory). If the current directory is not inside a git repository, stop and ask the user to run from inside the target repository.
- Read the project map at `~/.mrp-project-map`. The file is quoted CSV with one mapping per line, `#` comments, blank lines ignored, and two fields per row: the repository path and the project name. Multiple paths may map to the same project name (e.g. for git worktrees of the same project). Lookup is an exact string match against the repository root — no prefix matching, no symlink resolution.
- If the map file does not exist, or the repository root is not present in it, stop and instruct the user to add a line to `~/.mrp-project-map` for this repository. Show them the exact CSV line they should add, using the basename of the repository root as a suggested project name (e.g. `"/home/mark/Code/foo", "foo"`).

Store the resolved project name as `{project_name}`, and set `{project_dir}` to `{tasks_dir}/{project_name}`.

## Task Artifact Files

Artifacts related to the current development task are stored under the {project_dir}/{task_name} directory. Store this as {task_dir}. Each task directory may contain some of the following files. Refer to the contents of the appropriate file as needed to complete the user's requests.

| File | Variable | Type | Description |
|------|----------|------|-------------|
| `task.md` | `{task_description}` | required | The task description — what needs to be accomplished. |
| `research-report.md` | `{research_report}` | optional | Codebase research report with context and findings. |
| `design-spec.md` | `{design_spec}` | optional | High-level design document with architecture decisions. |
| `implementation-spec.md` | `{implementation_spec}` | optional | Detailed implementation spec with file-by-file changes. |
| `verification-plan.md` | `{verification_plan}` | optional | Verification plan with testing methodology and test cases. |
| `iterations.md` | `{iterations}` | optional | Task iteration history tracking changes across iterations. |
| `verification-report.md` | `{verification_report}` | optional | Verification report with test results and findings. |
| `user-review.txt` | `{user_review}` | optional | Review comments authored by the user, organized into rounds of findings. |
| `review-findings.md` | `{review_findings}` | optional | Review findings produced by code review sub-agents, organized into rounds. |

# Development Task Git Branch

Changes related to the current development branch go in the `markp/{task_name}` branch. Store the name of this branch as {task_branch}. All work that has already been done for this task (if any) would be contained in the commits between the base branch (main or master) and {task_branch}, as well as staged changes in the git index (if any) or uncommitted changes (if any).

# Conventions

## Task name guidance

- Task names must be **kebab-case** (e.g. `foo-bar-baz`)
- Task names are **all lowercase**
- Task names are **concise** — at most 4 words, often 2–3 words
