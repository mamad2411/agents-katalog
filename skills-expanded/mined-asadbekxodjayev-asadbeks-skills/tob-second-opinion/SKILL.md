# Second Opinion

**second-opinion** is a plugin that facilitates code reviews by integrating external LLM CLI tools into your workflow.

## Key Features

The tool enables code reviews across uncommitted changes, branch diffs, or specific commits using OpenAI Codex or Google Gemini. It "Shells out to `codex review` and/or `gemini` CLI with high-capability model configurations."

## Setup Requirements

To use this plugin, you'll need either:
- OpenAI's Codex CLI with valid API credentials, or
- Google Gemini CLI installed with authenticated extensions for code review and security analysis

## Primary Functionality

The `/second-opinion` command prompts users to select their review tool, specify the code scope to examine, optionally include project context files, and choose a review focus (general, security, performance, or error handling).

## Additional Capability

The plugin bundles Codex CLI's MCP server, providing two tools — **codex** and **codex-reply** — that offer "direct, programmatic access to Codex without the interactive prompt workflow" for multi-turn conversations.

## Installation

```
/plugin marketplace add trailofbits/skills
/plugin install second-opinion
```

## Source

Trail of Bits skills repository: https://github.com/trailofbits/skills
