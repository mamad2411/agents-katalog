---
name: github-aw-patterns
description: 'Reference and guidelines for designing GitHub Agentic Workflows using established operational patterns like BatchOps, CentralRepoOps, ChatOps, CorrectionOps, and others.'
license: MIT
---

# Skill: github-aw-patterns

<!-- markdownlint-disable MD013 MD023 MD031 MD032 -->

## WHEN TO USE

- When designing or architecting a new GitHub Agentic Workflow.
- When determining the best architectural pattern for automation (e.g., choosing between sequential vs. batch processing).
- When implementing specific Agentic Workflow patterns such as BatchOps, CentralRepoOps, ChatOps, DailyOps, etc.
- When organizing multi-repository or cross-repository workflow operations.

## WHEN NOT TO USE

- When writing the specific Markdown or YAML syntax of an individual workflow (use `github-aw-syntax`).
- For debugging a workflow that failed during execution (use `gh-aw-troubleshooting`).
- If the required automation is trivial and standard GitHub Actions without AI agents is perfectly sufficient.

## Common Pitfalls

- **Pattern Mismatch**: Using `WorkQueueOps` (sequential) for processing 500 independent items, leading to severe timeouts, instead of using `BatchOps`.
- **Missing Orchestration**: Trying to cram an entire company's CentralRepoOps logic into a single monolithic workflow file instead of utilizing Orchestrator/Worker dispatch patterns.
- **Ignoring Feedback**: Implementing CorrectionOps but failing to properly persist the human corrections into `repo-memory`, meaning the agent repeatedly makes the same mistakes.

## Core Principles

- **Pattern Selection**: Choose the pattern that best fits the scale, dependencies, and triggers of the operation.
- **Agentic Integration**: Combine deterministic computation (e.g., shell commands) with AI reasoning for optimal results (DeterministicOps).
- **Graceful Scaling**: Use patterns like BatchOps and WorkQueueOps to handle large volumes gracefully.
- **State Management**: Leverage MemoryOps for persistent workflow state and cross-run coordination.

## Agentic Workflow Patterns

### BatchOps

Use when you need to process large worksets in shards/chunks with throttling and aggregation.

BatchOps is a pattern for processing large volumes of work items efficiently. Splits work into chunks, parallelizes where possible, handles partial failures gracefully, and aggregates results into a consolidated report.

- **< 50 items, order matters**: Sequential (WorkQueueOps)
- **50–500 items, order doesn't matter**: BatchOps with chunked processing
- **> 500 items, high parallelism safe**: BatchOps with matrix fan-out
- **Items have dependencies on each other**: Sequential (WorkQueueOps)
- **Items are fully independent**: BatchOps (any strategy)
- **Strict rate limits or quotas**: Rate-limit-aware batching

### CentralRepoOps

Use when you need a private control repository that coordinates rollouts across many target repositories.

CentralRepoOps uses a single private repository as a control plane for large-scale operations across many repositories.
Use this pattern for organization-wide rollouts, phased adoption (pilot waves first), central governance, and security-aware prioritization across tens or hundreds of repositories. Each orchestrator run delivers consistent policy gates, controlled fan-out, and a complete decision trail without pushing main changes to individual target repositories.

### ChatOps

Use when you want slash-command driven, human-in-the-loop automation in issues or pull requests.

ChatOps brings automation into GitHub conversations through command triggers that respond to slash commands in issues, pull requests, and comments.

- **Interactive code reviews**: `/review` to analyze PR changes on demand
- **On-demand deployments**: `/deploy` staging when you're ready
- **Assisted analysis**: `/analyze` for specific investigations
- **Team collaboration**: Shared commands everyone can use

### CorrectionOps

Use when you want to improve workflow behavior from trusted human corrections without retraining the model.

CorrectionOps enables workflows to learn from human feedback. When a human corrects an agent's output, the correction is stored and used to guide future agentic reasoning, ensuring the workflow improves over time without needing model fine-tuning.

### DailyOps

Use when you want scheduled, small, recurring improvements that compound over time.

DailyOps workflows automate incremental progress toward large goals through small, scheduled daily changes. Work happens automatically in manageable pieces that are easy to review and integrate.
Scheduled execution usually runs on weekday schedules (avoiding weekends) with `workflow_dispatch` enabled for manual testing.

### DeterministicOps

Use when you need deterministic data collection steps followed by agentic analysis and reporting.

Combines deterministic computation with AI reasoning, enabling data preprocessing, custom trigger filtering, and post-processing patterns. Shell commands in steps reliably collect and prepare data, then the AI agent reads the results and generates insights. Use this for data aggregation, report generation, trend analysis, auditing, and any hybrid pipeline.

### DispatchOps

Use when you need manual trigger flows (`workflow_dispatch`) with custom inputs for testing or controlled runs.

Enables manual workflow execution via the GitHub Actions UI or CLI using `workflow_dispatch`. Perfect for on-demand tasks, testing workflows during development, debugging production issues, or tasks that don't fit a schedule or event trigger.

### IssueOps

Use when you need fully automated issue triage, categorization, and responses on issue events.

Transforms GitHub issues into automation triggers that analyze, categorize, and respond to issues automatically. Use it for auto-triage, smart routing, initial responses, and quality checks. Handled securely without write permissions for the main AI job using safe-outputs.

### LabelOps

Use when you need label-driven workflow behavior when specific labels are added or removed.

Uses GitHub labels as workflow triggers, metadata, and state markers. Two distinct approaches:
1. `label_command` for command-style one-shot activation.
2. `names:` filtering for persistent label-state awareness.

### Monitoring with Projects

Use when you need durable tracking and monitoring of work items with GitHub Projects and safe outputs.

Monitoring with Projects leverages GitHub Projects (V2) as a persistent state store and dashboard for agentic workflows. It allows workflows to track the progress of long-running tasks, visualize work queues, and provide human-readable status updates without cluttering the repository with temporary files.

### MemoryOps

Use when you need workflows to persist state across runs using `cache-memory` and `repo-memory`.

Enables workflows to persist state across runs using `cache-memory` and `repo-memory`. Build workflows that remember their progress, resume after interruptions, share data between workflows, and avoid API throttling. Use for incremental processing, trend analysis, multi-step tasks, and workflow coordination.

### MonitorOps

Use when you need repository-wide workflow observability, trend reporting, and escalation for recurring failures or token waste.

Use this pattern when you want a scheduled workflow to inspect other agentic workflows, summarize what happened, and escalate unusual cost or failure patterns. Creates a durable operational record and can open or update issues when the same problem crosses a threshold.

### MultiRepoOps

Use when you need coordination and synchronization across multiple repositories.

Extends operational automation patterns across multiple GitHub repositories. Uses target-repo parameter on safe outputs to create issues, pull requests, and comments in external repositories. Use for feature synchronization (main repo to sub-repos), hub-and-spoke issue tracking, and org-wide enforcement.

### Orchestration

Use when you need orchestrator/worker architecture using reusable workflows or workflow dispatch.

Use this pattern when one workflow (the orchestrator) needs to fan out work to one or more worker workflows.
- **Orchestrator**: decides what to do next, splits work into units, dispatches workers using `dispatch-workflow`.
- **Worker(s)**: do the concrete work with scoped permissions/tools.

### ProjectOps

Use when you need intelligent routing and controlled field updates in GitHub Projects.

Builds on GitHub Projects to run project operations with less manual upkeep. Reads project state with GitHub tools and applies changes through safe-outputs. Useful for context-aware routing and field updates, giving teams faster triage decisions and cleaner board state.

### ResearchPlanAssignOps

Use when you need a flow from deep research to planning to automated issue assignment/implementation.

A four-phase development pattern that moves from automated discovery to merged code with human control at every decision point:
1. **Research**: A research agent surfaces insights.
2. **Plan**: A planning agent converts them into actionable issues.
3. **Assign**: A coding agent implements the work.
4. **Merge**: A human reviews and merges.

### SideRepoOps

Use when you want low-friction reporting/automation from a side repository targeting a primary repository.

A development pattern where you run agentic workflows from a separate "side" repository that targets your main codebase. Keeps AI-generated issues, comments, and workflow runs isolated from your main repository. Ideal for experimentation, centralized automation across multiple repos, or managing workflows for repos you don't directly control. (Different from MultiRepoOps which runs from the main repository).

### SpecOps

Use when you need to maintain formal specifications and propagate spec updates to consuming implementations.

A pattern for maintaining formal specifications using agentic workflows. Leverages the w3c-specification-writer agent to create W3C-style specifications with RFC 2119 keywords and automatically propagates changes to consuming implementations across repositories.

### TrialOps

Use when you need isolated trial repositories to validate workflows before production rollout.

TrialOps uses dedicated "trial" or "sandbox" repositories to test and refine agentic workflows before they are deployed to production repositories. This minimizes risk and allows for rapid iteration in a safe environment.

### WorkQueueOps

Use when you need durable queue processing for many items via issues, sub-issues, discussions, or cache-memory.

A pattern for systematically processing a large backlog of work items incrementally instead of processing everything at once. Survives interruptions, rate limits, and multi-day horizons.
Queue Strategies:
1. Issue Checklist as Queue
2. Sub-Issues as Queue
3. Cache-Memory Queue

## References

- [BatchOps](https://github.com/github/gh-aw/blob/v0.74.0/docs/src/content/docs/patterns/batch-ops.md)
- [CentralRepoOps](https://github.com/github/gh-aw/blob/v0.74.0/docs/src/content/docs/patterns/central-repo-ops.mdx)
- [ChatOps](https://github.com/github/gh-aw/blob/v0.74.0/docs/src/content/docs/patterns/chat-ops.md)
- [CorrectionOps](https://github.com/github/gh-aw/blob/v0.74.3/docs/src/content/docs/experimental/correction-ops.md)
- [DailyOps](https://github.com/github/gh-aw/blob/v0.74.0/docs/src/content/docs/patterns/daily-ops.md)
- [DeterministicOps](https://github.com/github/gh-aw/blob/v0.74.3/docs/src/content/docs/patterns/deterministic-ops.md)
- [DispatchOps](https://github.com/github/gh-aw/blob/v0.74.0/docs/src/content/docs/patterns/dispatch-ops.md)
- [IssueOps](https://github.com/github/gh-aw/blob/v0.74.0/docs/src/content/docs/patterns/issue-ops.md)
- [LabelOps](https://github.com/github/gh-aw/blob/v0.74.0/docs/src/content/docs/patterns/label-ops.md)
- [MemoryOps](https://github.com/github/gh-aw/blob/v0.74.0/docs/src/content/docs/guides/memoryops.md)
- [Monitoring with Projects](https://github.com/github/gh-aw/blob/v0.74.3/docs/src/content/docs/experimental/monitoring-with-projects.md)
- [MonitorOps](https://github.com/github/gh-aw/blob/v0.74.3/docs/src/content/docs/patterns/monitor-ops.md)
- [MultiRepoOps](https://github.com/github/gh-aw/blob/v0.74.0/docs/src/content/docs/patterns/multi-repo-ops.md)
- [Orchestration](https://github.com/github/gh-aw/blob/v0.74.0/docs/src/content/docs/patterns/orchestration.md)
- [ProjectOps](https://github.com/github/gh-aw/blob/v0.74.0/docs/src/content/docs/patterns/project-ops.mdx)
- [ResearchPlanAssignOps](https://github.com/github/gh-aw/blob/v0.74.0/docs/src/content/docs/patterns/research-plan-assign-ops.md)
- [SideRepoOps](https://github.com/github/gh-aw/blob/v0.74.0/docs/src/content/docs/patterns/side-repo-ops.mdx)
- [SpecOps](https://github.com/github/gh-aw/blob/v0.74.0/docs/src/content/docs/patterns/spec-ops.md)
- [TrialOps](https://github.com/github/gh-aw/blob/v0.74.3/docs/src/content/docs/experimental/trial-ops.md)
- [WorkQueueOps](https://github.com/github/gh-aw/blob/v0.74.0/docs/src/content/docs/patterns/workqueue-ops.md)

## Related Skills

- **gh-aw**: To run and manage GitHub Agentic Workflows.
- **github-aw-syntax**: For detailed syntax reference of Agentic Workflows.
