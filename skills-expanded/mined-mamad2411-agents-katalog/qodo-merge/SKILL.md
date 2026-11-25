---
name: qodo-merge
description: Configure and use Qodo Merge, formerly PR-Agent, for AI-powered pull request reviews, descriptions, inline suggestions, labels, docs, and ticket checks across GitHub, GitLab, Bitbucket, and Azure DevOps. Use this skill whenever the user mentions Qodo Merge, PR-Agent, `.pr_agent.toml`, `pr_agent`, PR review bots, `/describe`, `/review`, `/improve`, GitHub App or Action setup, model configuration, or debugging PR-Agent automation.
version: 1.0.0
source: https://qodo-merge-docs.qodo.ai/
license: MIT
---

# Qodo Merge

Use this skill to install, configure, and troubleshoot Qodo Merge / PR-Agent without pulling large chunks of product docs into the active context.

## Start here

1. Identify the platform: GitHub Action/App, GitLab, Bitbucket, Azure DevOps, Docker, AWS Lambda, or self-hosted.
2. Identify the job: install, configure, use a tool command, switch models, or debug a failure.
3. Prefer repo-local `.pr_agent.toml` for stable settings and env vars only for secrets or one-off overrides.
4. Read only the reference file that matches the task instead of loading everything.

## Core commands

| Command | Use it for |
|---|---|
| `/describe` | Generate PR title, summary, walkthrough, labels, and optional diagram |
| `/review` | Review the PR for quality, correctness, security, and ticket alignment |
| `/improve` | Generate inline code suggestions and rank them by confidence |
| `/ask "..."` | Ask questions about the diff, files, or intent of the PR |
| `/add_docs` | Add missing docs for changed code |
| `/generate_labels` | Infer labels from PR content |
| `/help_docs "..."` | Answer repo questions from project documentation |

## High-value rules

- Config precedence is: CLI args -> env vars -> `.pr_agent.toml` -> defaults.
- For env var overrides, config keys map with double underscores, for example `PR_REVIEWER__REQUIRE_TESTS_REVIEW=false`.
- AWS Lambda env vars cannot contain `.`; use `__` instead.
- Non-OpenAI providers use their own API keys. Do not require `OPENAI_KEY` for Claude, Gemini, or similar providers.
- `suggestions_score_threshold` controls how aggressive `/improve` is; raise it to reduce low-value suggestions.
- `allow_dynamic_context = true` helps larger diffs by expanding surrounding code context.
- Use description markers when the user wants generated PR bodies to fit a repo template cleanly.
- Local Ollama setups generally require a self-hosted runner; hosted CI cannot reach local services.

## Troubleshooting shortcuts

| Symptom | First check |
|---|---|
| Model not found | Provider-specific model name format |
| API key missing | Matching secret/env var name for the selected provider |
| Permission denied | PR, issue, and contents write permissions in the integration |
| Bad JSON in provider config | `litellm.extra_body` formatting |
| Weak context on large PRs | Dynamic context and patch sizing settings |

## Routing guide

- Installation and platform-specific setup: `references/installation.md`
- Tool behavior and per-tool config: `references/tools.md`
- `.pr_agent.toml`, CLI flags, env vars, model wiring: `references/usage-guide.md`
- Self-reflection, compression, dynamic context, metadata: `references/core-abilities.md`
- Product overview, FAQ, and miscellaneous details: `references/other.md`
- Mirrored documentation index: `references/documentation/index.md`

## Working style

- Keep answers implementation-focused: pick the right platform path, show the minimal config, and explain only the options that matter to the user's case.
- Avoid dumping long examples from docs unless the user needs a ready-to-paste workflow or config block.
- Treat https://qodo-merge-docs.qodo.ai/ as the source of truth for exact option names and current behavior.
