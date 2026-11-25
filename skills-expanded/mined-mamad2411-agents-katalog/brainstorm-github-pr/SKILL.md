---
name: brainstorm-github-pr
description: >-
  Activate PR brainstorming protocol to analyze and visualize commit history, review threads, and CI pipeline checks using Mermaid diagrams.
  You MUST load this skill when asked to analyze or brainstorm a Pull Request.
license: MIT
---

# Skill brainstorm-github-pr

<!-- markdownlint-disable MD013 MD023 MD031 MD032 -->

Analyze and visualize GitHub Pull Requests by mapping commit history, reviewer feedback, and CI/CD status into structured Mermaid diagrams to establish context before deep analysis.

## WHEN NOT TO USE

- When tasked with writing actual code to fix the PR; this skill is for *analyzing and visualizing* the PR state first.
- If the PR is trivial (e.g., a one-line typo fix) where generating four different Mermaid diagrams is unnecessary overhead.
- When analyzing repository-wide architecture outside the context of a specific Pull Request.

## Common Pitfalls

- **Skipping the Base Branch**: Creating a `gitGraph` without properly identifying where the feature branch diverged from `main`, resulting in a misleading history.
- **Overloading Diagrams**: Attempting to put every single CI log line into an Ishikawa diagram instead of summarizing the *categories* of failures.
- **Assuming Sequential Data**: Failing to account for concurrent or out-of-order review comments when mapping out the Kanban board.

## Core Process

1. **Commit History Visualization**: Map out the historical context of the PR by generating a list of commits into a Mermaid `gitGraph` diagram.
2. **PR Review Kanban Diagram**: Map active, outdated, and resolved review threads or comments into a Mermaid `kanban` diagram.
3. **CI Checks State Visualization**: Visualize the current state of Continuous Integration (CI) checks (passing, failing, pending) using a Mermaid `flowchart` diagram.
4. **CI Failures Summarization**: Categorize and summarize the root causes and affected jobs of any CI failures using a Mermaid `ishikawa-beta` diagram.

## Core Principles

- **Visual State Mapping**: Always translate raw PR data (commits, reviews, checks) into easy-to-read diagrams before diving into code or detailed logs.
- **Native Tooling**: Rely on native CLI commands like `gh pr view`, `gh pr checks`, `gh run view`, and `gh api graphql` for fast data extraction.
- **Progressive Disclosure**: Map high-level structure (commits, reviews, pipeline topology) first, then drill down into detailed logs only if needed.

## Brainstorming - Pull Request

When an active Pull Request is associated with the runtime context or the user requests PR analysis,
you MUST activate the PR Brainstorming protocol.

### Step 1: Commit History Visualization

First, map out the historical context of the PR by generating a list of commits in the form of a Mermaid `gitGraph` diagram.
This establishes the structural history before deep fact finding.

**Example `gitGraph` Diagram:**

```mermaid
%% This diagram visualizes the commit history of a PR.
%% Data for this diagram can be retrieved natively using:
%% gh pr view <pr_number> --json baseRefName,headRefName,commits
gitGraph
    commit id: "[base] main (base)"
    branch feature/update-config
    checkout feature/update-config
    commit id: "[abcdef1] Initial feature commit [author1]"
    commit id: "[1234567] Add new configurations [author2]"
    commit id: "[89abcd2] Fix linting errors [author2]"
```

To extract the list of commits that belong to the PR, use `gh pr view` or `git log`.

### Step 2: PR Review Kanban Diagram

Next, map out the active, outdated, and resolved review threads or comments on the Pull Request into a Mermaid `kanban` diagram.
This provides a clear track of outstanding issues and reviewer feedback before diving into the code checks.

**Example `kanban` Diagram:**

```mermaid
---
kanban:
  tickInterval: 1
---
kanban
  %% This diagram visualizes PR review threads and comments.
  %% Data can be retrieved using:
  %% gh api graphql -F owner="<owner>" -F repo="<repo>" -F number=<pr_number> ...
  Active
    [Fix inline comments support]
      bodyText: Make sure inline comments are part of labels properly.
      assigned: reviewer-name
      id: PRRT_kw1234
      path: path/to/file.md
  Outdated
  Resolved
```

To extract PR comments and review threads, use `gh api graphql` with the GitHub GraphQL API.

### Step 3: CI Checks State Visualization

Next, visualize the current state of the Continuous Integration (CI) checks to identify passing,
failing, or pending jobs. Map these findings using a Mermaid `flowchart` diagram.

**Example `flowchart` Diagram:**

```mermaid
flowchart LR
%% This diagram visualizes the topology and statuses of CI/CD checks for a PR.
    pr(["PR #123: Minor fixes"])

    subgraph Checks ["CI Format & Linting"]
        direction TB
        c3["Actionlint<br/>#&#123;run_id&#125;"]:::pass
        c1["Link Checker<br/>#&#123;run_id&#125;"]:::pass
        c2["Pre-commit<br/>#&#123;run_id&#125;"]:::pass
    end

    subgraph Tests ["Test Scenarios"]
        direction TB
        m1["default<br/>#&#123;run_id&#125;"]:::pass
        m3["qa<br/>#&#123;run_id&#125;"]:::fail
        m2["test<br/>#&#123;run_id&#125;"]:::fail
    end

    pr --> Checks
    pr --> Tests

    classDef pass fill:#d4edda,stroke:#28a745,color:#155724,stroke-width:2px
    classDef fail fill:#f8d7da,stroke:#dc3545,color:#721c24,stroke-width:2px
```

To extract the list of checks, use the `gh pr checks <pr_number>` command.

### Step 4: CI Failures Summarization

If any CI checks fail, use a Mermaid `ishikawa-beta` (fishbone) diagram to categorize
and summarize the root causes and affected jobs.

**Example `ishikawa-beta` Diagram:**

```mermaid
ishikawa-beta
%% This diagram categorizes CI failures for a PR, grouping them by logical categories.
    PR 123 CI Failures
    Test Scenarios
        qa (#1234)
            Job Canceled
            Missing artifact
        test (#1234)
            Root Failure (test scenario failed)
            Node.js 20 deprecated warning
    CI Format & Linting
        All Checks Passed
```

To gather a summary of failures,
use `gh run view <run_id>`.
At this step, don't check for more detailed logs yet.

## What to Avoid

- Attempting to map commit history without identifying the base and head branch structure.
- Diving into detailed job logs or codebase checks before visualizing the overall CI state and PR history.
- Rendering diagrams that include invalid Mermaid syntax or overly complex elements that break rendering.

## Related Skills

- **brainstorm**: You MUST load this skill when asked to brainstorm, explore options, or break down complex problems.
- **brainstorm-agent-runs**: You MUST load this skill when identifying agentic runs in CI/CD for a Pull Request.
- **mermaid**: You MUST load this skill when constructing `gitGraph`, `kanban`, and `flowchart` diagrams.
- **mermaid-beta**: You MUST load this skill when building `ishikawa-beta` diagrams.
