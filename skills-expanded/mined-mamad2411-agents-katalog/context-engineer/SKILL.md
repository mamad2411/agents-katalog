---
name: context-engineer
description: "Master context engineering and prompt engineering for AI agents and LLMs. Optimize system prompts, craft few-shot examples, implement chain-of-thought reasoning, manage context windows, design structured outputs, and build self-improving prompt patterns. Covers Anthropic, OpenAI, and Google best practices. Includes prompt optimizer that audits drafts against best practices, and context builder that generates optimal context windows for any task. Built for AI agents — Python stdlib only, no dependencies. Use for prompt optimization, system prompt design, agent instruction writing, LLM output debugging, context window management, and few-shot example crafting."
homepage: https://www.agxntsix.ai
license: MIT
compatibility: Python 3.10+ (stdlib only — no dependencies)
metadata: {"openclaw": {"emoji": "🧠", "requires": {"env": []}, "primaryEnv": "", "homepage": "https://www.agxntsix.ai"}}
---

# 🧠 Context Engineer

Master skill for context engineering and prompt engineering — the art of crafting optimal inputs to LLMs.

## Features

- **Optimize prompts** against Anthropic, OpenAI, and Google best practices
- **Build context windows** with system prompt, user prompt, and examples
- **Design system prompts** for sub-agents, crons, and skills
- **Craft few-shot examples** that dramatically improve accuracy
- **Implement chain-of-thought** reasoning for complex tasks
- **Manage context windows** — prioritize critical info placement
- **Structure outputs** with JSON schema, markdown, or XML tags
- **Debug poor LLM outputs** with systematic prompt analysis
- **Write agent instructions** (AGENTS.md, SOUL.md patterns)
- **Apply role-based prompting** for domain-specific performance
- **Chain complex tasks** into accurate subtask pipelines
- **Reference 20+ templates** for common prompting patterns

## Requirements

| Variable | Required | Description |
|----------|----------|-------------|
| None | — | No API keys needed — pure prompt engineering knowledge |

## Quick Start

```bash
PY=~/.openclaw/workspace/.venv/bin/python3

# Analyze and improve a draft prompt
$PY skills/context-engineer/scripts/prompt_optimizer.py "Your draft prompt here"

# Build optimal context window for a task
$PY skills/context-engineer/scripts/context_builder.py "Analyze quarterly financials"

# Optimize from file
$PY skills/context-engineer/scripts/prompt_optimizer.py --file path/to/prompt.txt
```

## Commands

### Prompt Optimizer
```bash
# Analyze a prompt string
$PY skills/context-engineer/scripts/prompt_optimizer.py "Your prompt"

# Analyze from file
$PY skills/context-engineer/scripts/prompt_optimizer.py --file prompt.txt
```

### Context Builder
```bash
# Build context for a task
$PY skills/context-engineer/scripts/context_builder.py "Task description"

# With role and output format
$PY skills/context-engineer/scripts/context_builder.py --task "Code review" --role "Senior engineer" --output json
```

## The 10 Commandments of Prompting

1. **Be clear, direct, and detailed** — Treat the model as a brilliant new employee with no context
2. **Use examples** — 3-5 diverse examples dramatically improve accuracy and consistency
3. **Let it think** — Chain-of-thought for complex reasoning; extended thinking for hard problems
4. **Structure with tags** — XML tags prevent mixing of instructions, context, and examples
5. **Assign a role** — System prompts with specific personas boost domain performance
6. **Chain complex tasks** — Break multi-step work into subtask prompts for accuracy
7. **Manage context** — Put critical info at top and bottom; reference docs by tag name
8. **Specify output format** — JSON schema, markdown structure, or explicit format instructions
9. **Iterate empirically** — Test against eval criteria, not vibes
10. **Context > Prompt** — What you include matters more than how you ask

## References

| File | Description |
|------|-------------|
| `references/anthropic-best-practices.md` | Anthropic's official prompt engineering docs |
| `references/openai-best-practices.md` | OpenAI's prompt engineering guide |
| `references/google-best-practices.md` | Google's Gemini prompting strategies |
| `references/context-engineering-principles.md` | Context engineering theory (Karpathy et al.) |
| `references/prompt-templates.md` | 20+ reusable templates for common tasks |

## Script Reference

| Script | Description |
|--------|-------------|
| `{baseDir}/scripts/prompt_optimizer.py` | Analyzes prompts against best practices |
| `{baseDir}/scripts/context_builder.py` | Builds optimal context windows for tasks |

## Output Format

All commands output structured text by default with clear sections for analysis results, suggestions, and improved prompts.

## Data Policy

This skill processes prompts locally. No data is sent to external services unless explicitly using an LLM API.

## Sources

- Anthropic Prompt Engineering: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview
- OpenAI Prompt Engineering: https://platform.openai.com/docs/guides/prompt-engineering
- Google Gemini Prompting: https://ai.google.dev/gemini-api/docs/prompting-strategies
- Andrej Karpathy on Context Engineering (2025)

---

Built by [M. Abidi](https://www.agxntsix.ai)

[LinkedIn](https://www.linkedin.com/in/mohammad-ali-abidi) · [YouTube](https://youtube.com/@aiwithabidi) · [GitHub](https://github.com/aiwithabidi) · [Book a Call](https://cal.com/agxntsix/abidi-openclaw)
