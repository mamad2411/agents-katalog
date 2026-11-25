---
name: skill-index
description: Use when browsing or searching the prompts/skills index. Triggers on skill discovery, prompt browsing, skill listing requests. Keywords: skill, index, prompt, listing, discovery, browser.
---

# Prompts Skills Index

## Overview

This directory contains all MCP prompt templates (36 skills) organized for Anthropic Skills compatibility. Each `.md` file is a self-contained prompt template with YAML frontmatter.

**Core Principle:** Every skill follows the Anthropic Skills specification with `name` + `description` + `params` frontmatter structure.

## Skills Catalog

### Superpowers Templates (18 skills, no parameters)

| # | File | Name | Description |
|---|------|------|-------------|
| 1 | `brainstorming.md` | `brainstorming` | Design and feature brainstorming before implementation |
| 2 | `writing-skills.md` | `writing-skills` | Create, edit, or validate agent skills (TDD for documentation) |
| 3 | `writing-plans.md` | `writing-plans` | Multi-step implementation plans before coding |
| 4 | `executing-plans.md` | `executing-plans` | Execute multi-step implementation plans |
| 5 | `dispatching-parallel-agents.md` | `dispatching-parallel-agents` | Dispatch independent tasks to parallel agents |
| 6 | `using-superpowers.md` | `using-superpowers` | Leverage superpower skills for development tasks |
| 7 | `verification-before-completion.md` | `verification-before-completion` | Verify task completion before final submission |
| 8 | `finishing-a-development-branch.md` | `finishing-a-development-branch` | Finalize development branches before merge |
| 9 | `mcp-builder.md` | `mcp-builder` | Build new MCP server modules |
| 10 | `systematic-debugging.md` | `systematic-debugging` | Systematically debug issues |
| 11 | `test-driven-development.md` | `test-driven-development` | Implement features using TDD methodology |
| 12 | `using-git-worktrees.md` | `using-git-worktrees` | Manage Git worktrees for parallel development |
| 13 | `workflow-runner.md` | `workflow-runner` | Execute workflow pipelines |
| 14 | `requesting-code-review.md` | `requesting-code-review` | Request code reviews from reviewers |
| 15 | `receiving-code-review.md` | `receiving-code-review` | Receive and respond to code reviews |
| 16 | `subagent-driven-development.md` | `subagent-driven-development` | Delegate implementation tasks to subagents |
| 17 | `evolution-workflow.md` | `evolution-workflow` | Prompt evolution workflow |
| 18 | `variant-comparison.md` | `variant-comparison` | Compare evolution variants |

### Chinese Standards Templates (4 skills)

| # | File | Name | Description |
|---|------|------|-------------|
| 1 | `zh-code-review.md` | `zh-code-review` | Chinese-style code reviews |
| 2 | `zh-commit-conventions.md` | `zh-commit-conventions` | Chinese commit conventions |
| 3 | `zh-documentation.md` | `zh-documentation` | Chinese documentation writing |
| 4 | `zh-git-workflow.md` | `zh-git-workflow` | Chinese Git workflows |

### Parameterized Templates (13 skills, all parameters optional)

| # | File | Name | Parameters | Description |
|---|------|------|------------|-------------|
| 1 | `create-prompt-template.md` | `create-prompt-template` | `prompt_name`, `prompt_description`, `prompt_arguments`, `template_content` | Create new MCP prompt templates |
| 2 | `dm-text-game.md` | `dm-text-game` | `base`, `opening_text`, `player_name` | Text adventure DM games |
| 3 | `refactor-mcp-project.md` | `refactor-mcp-project` | `source_path`, `target_path`, `code_type` | Refactor MCP server projects |
| 4 | `softtest-feature-request.md` | `softtest-feature-request` | `feature_type`, `use_case`, `reference_tools` | Analyze feature requests for soft testing |
| 5 | `softtest-report-template.md` | `softtest-report-template` | `report_name` | Generate software test reports |
| 6 | `softtest-changelog.md` | `softtest-changelog` | `version`, `scope` | Generate software update changelogs |
| 7 | `softtest-core-workflow.md` | `softtest-core-workflow` | `repo_source`, `analysis_depth`, `target_languages` | Multi-stage test analysis pipelines |
| 8 | `softtest-strategy.md` | `softtest-strategy` | `language`, `strategy_type` | Define software testing strategies |
| 9 | `softtest-bug-report.md` | `softtest-bug-report` | `project_lang`, `repo_size`, `actual_output`, `expected_output` | Generate software bug reports |
| 10 | `softtest-contrib-guide.md` | `softtest-contrib-guide` | `contrib_type`, `target_file` | Create software contribution guides |
| 11 | `softtest-project-info.md` | `softtest-project-info` | `query_type` | Collect software project information |
| 12 | `report-structure.md` | `report-structure` | None | Execution report structure specification (HTML/CSS template, module selection logic, styling norms) |
| 13 | `SKILL.md` | `SKILL` | None | Skills index file |

## Usage

Each skill file follows the Anthropic Skills specification:
- **YAML frontmatter**: `name` (1-64 chars, lowercase + hyphens), `description` (Use when... format), `params` (optional)
- **Body**: Markdown content with skill instructions, examples, and reference links
- **Parameters**: Passed via MCP prompt args form, all optional

## Registration

Prompts are auto-registered by `Lib/prompts/scripts/prompt_registry.py` which scans this directory and registers each `.md` file as an MCP prompt.

## Changelog (2026-06-11)

- Total prompt templates: 36 (updated from 32)
- Added: `evolution-workflow.md`, `variant-comparison.md`, `SKILL.md`
- Directory: `skills/` (Anthropic Skills standardization)
