---
name: mrp-commit-message
description: Generate well-structured git commit messages for the development task workflow. Use when asked to 'commit changes', 'commit to git', 'create a commit', 'make a commit', or any request involving committing code changes.
---

# Task context

Load the `mrp-dev-task` skill to determine the current task name {task_name} and task directory {task_dir} location.

# Commit message structure

## Summary line

Construct the summary line as follows:

1. **Linear issue prefix** — If the task description mentions a Linear issue (e.g. `AU-17889`), start the line with it: `AU-17889: <rest>`.

2. **Change type prefix** — After the optional issue prefix, add a conventional commit type:
   - `fix():` for bug fixes
   - `feat():` for features
   - `chore():` for maintenance tasks

3. **Component scope** — Inside the parentheses, name the major component being changed (e.g. `fix(cli):`, `feat(agent_personas):`). If no single major component is affected or multiple are, omit the parentheses entirely (e.g. `fix: <rest>`).

4. **Summary text** — A VERY concise description of the change. The entire summary line must be under 100 characters, and should aim for under 80 characters.

**Examples:**
- `AU-17889: fix(cli): handle missing config file gracefully`
- `feat(agent_personas): add support for custom persona templates`
- `chore: update dependency versions`

## Body

### First Commit in Development Task Branch

If the commit being made is the first commit in the development task branch, or a you are performing a rebase to squash all the development task branch commits into a single commit, use this format for the commit message:

The commit body has up to three sections, separated by blank lines. Scale the detail to the size of the change:

- **For changes under 10 lines of code:** Collapse problem and solution into a single short paragraph of a few sentences. Use a single `Problem/Solution:` label.
- **For changes under 100 lines of code:** Keep problem and solution descriptions short (a few sentences each).
- **For large changes (hundreds or thousands of lines):** Provide more detailed problem and solution descriptions proportional to the scope of the change.

Each section in the body must be explicitly labeled with a header line:

#### Problem:
Infer from {task_description} and optionally {research_report}. If these files are not available, infer the problem from the diffs being committed. Explain WHY this commit is being created in a concise paragraph.

#### Solution:
Infer from {design_spec} (if available), {implementation_spec} (if available) AND the diffs being committed. Explain HOW this commit addresses the problem at a high level. Do NOT include code snippets or overly detailed information — summarize the key aspects of the implemented solution.

#### Testing done:
Include testing steps that were carried out during implementation/verification (e.g. builds/compiles verified, unit tests added and executed, end-to-end verification steps carried out). Additionally, if {verification_report} exists in the task directory include a summary of the types of testing that were carried out. Omit this section entirely only if no testing is evident and no {verification_report} exists.

**Example commit body:**
```
**Problem:**
The CLI crashes with a stack trace when the user's config file is missing,
rather than falling back to default settings.

**Solution:**
Add a fallback path in the config loader that initializes default settings
when no config file is found, and log a warning to inform the user.

**Testing done:**
Added unit tests for the config loader fallback path. Verified manually that
the CLI starts cleanly with no config file present.
```

### Subsequent Commits in Development Task Branch

For subsequent commits in the development task branch, use a normal git commit message format, describe the changes that were made by the contents of the commit.
