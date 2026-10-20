---
name: squad-cli
description: 'Manage human-led AI agent teams for any project using the Squad CLI. You MUST load this skill when using the squad command.'
license: MIT
---

# Squad CLI

<!-- markdownlint-disable MD013 MD023 MD031 MD032 -->

## WHEN TO USE

- Initializing a new AI agent team in a project.
- Upgrading Squad-owned files or the CLI itself.
- Monitoring issues and auto-triaging work with Ralph (watch mode).
- Managing team roster, decisions, and session history.
- Externalizing or internalizing squad state.

## WHEN NOT TO USE

- General GitHub CLI operations (use `gh` skill).
- Core GitHub Copilot coding tasks (use `@copilot`).
- Standard project build/test tasks.

## Step-by-Step Workflows

### Initial Setup

1. **Install CLI**:
   ```bash
   npm install -g @bradygaster/squad-cli
   ```

2. **Initialize Squad**:
   ```bash
   squad init
   ```
   *Alias: `squad hire`*

3. **Verify Installation**:
   Check if `.squad/team.md` was created.

### Watch Mode (Ralph)

1. **Triage Mode**:
   Poll for issues without execution.
   ```bash
   squad watch
   ```

2. **Execution Mode**:
   Monitor and auto-execute against actionable issues.
   ```bash
   squad watch --execute --interval 5
   ```

3. **Custom Execution**:
   ```bash
   squad watch --execute \
     --agent-cmd "gh copilot" \
     --copilot-flags "--yolo --agent squad"
   ```

### Maintenance and Upgrades

1. **Update CLI**:
   ```bash
   squad upgrade --self
   ```

2. **Update Project Files**:
   ```bash
   squad upgrade
   ```

3. **Diagnostics**:
   ```bash
   squad doctor
   ```

### State Management

- **Show Status**: `squad status`
- **Link Remote Team**: `squad link <team-repo-path>`
- **Externalize State**: `squad externalize` (moves `.squad/` outside the working tree)
- **Internalize State**: `squad internalize`
- **Context Hygiene**: `squad nap --deep`

## Common Pitfalls

- **Interactive Prompts**: Using `squad` without `--yolo` when running agents might cause hangs in non-interactive environments as it waits for tool approvals.
- **Git State**: Failing to commit the `.squad/` directory means the team's accumulated knowledge won't be shared with others.
- **Watch Mode Auth**: Ensure `gh auth login` is completed before running `squad watch` if it needs to interact with GitHub issues or PRs.

## References

- [Squad Repository](https://github.com/bradygaster/squad)
- [Squad Documentation](https://bradygaster.github.io/squad/)
