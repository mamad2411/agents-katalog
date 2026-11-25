---
name: prompt-forge
description: "Use when a developer explicitly asks for help crafting or refining an execution prompt. Not triggered by general task requests — only when they specifically ask for prompt writing assistance, not task execution."
---

# Prompt Forge

A prompt refinement skill that extracts what a developer actually means — especially when they're too deep in a session to say it clearly. It investigates the codebase, researches the ecosystem, and surfaces the perspectives that fatigue makes you forget, then produces a grounded prompt that the developer hands to their execution tool.

Built on Anthropic's official prompting best practices. Designed to work as a plugin for Claude Code and Gemini CLI, alongside GSD and Superpowers.

## The Cardinal Rule

**Investigate freely — but never implement.** Prompt Forge is a prompt writer, not a task executor. Its only job is to produce a refined, grounded prompt. See `src/core/constraints.md` for full boundary definition.

## Core Workflow

The workflow has two grounding passes — one before asking questions, one after.

| Step | Module | What Happens |
|------|--------|-------------|
| 1. Receive input | `src/core/intent_parser.md` | Read raw input, detect fatigue signals |
| 2. First grounding | `src/core/intent_parser.md` | CLAUDE.md → code analysis → web research |
| 3. Ask questions | `src/core/intent_parser.md` | 1-3 grounded, fatigue-friendly questions |
| 4. Second grounding | `src/core/intent_parser.md` | Targeted deep-dive from answers |
| 5. Apply lenses | `src/core/prompt_builder.md` | 9 perspective lenses (business, QA, architecture, UX, security, performance, DX, edge cases, migration) |
| 6. Produce output | `src/core/prompt_builder.md` | Intent breakdown + copy-paste prompt |
| 7. Scope check | `src/core/constraints.md` | Verify no implementation drift |
| 8. Deliver | `src/utils/helpers.md` | Present prompt, stay open for refinement |

## Module Index

### Core Logic
- **`src/core/intent_parser.md`** — Steps 1-4: input parsing, grounding, clarifying questions
- **`src/core/prompt_builder.md`** — Steps 5-6: lens analysis, task classification, output generation
- **`src/core/modes.md`** — 5 compilation modes (build, audit, debug, research, optimize)
- **`src/core/constraints.md`** — The Cardinal Rule, scope boundaries, drift detection

### LLM Adapters
- **`src/adapters/claude.md`** — Claude/Anthropic formatting (XML tags, @ references)
- **`src/adapters/gemini.md`** — Gemini/Google formatting (MUST/MUST NOT, markdown)
- **`src/adapters/openai.md`** — OpenAI/GPT formatting (system/user split, few-shot)

### Command
- **`src/commands/prompt-forge.md`** — Slash command entrypoint and invocation guide

### Helpers
- **`src/utils/helpers.md`** — Tone, collaboration style, complexity adaptation, delivery protocol

### Templates
- **`prompts/templates/task-type-blueprints.md`** — 8 task-type prompt structures
- **`prompts/templates/gsd-output-format.md`** — GSD-optimized output format
- **`prompts/templates/superpowers-output-format.md`** — Superpowers-optimized output format
- **`prompts/templates/context-file-template.md`** — Template for project context files
- **`prompts/templates/anthropic-prompting-guide.md`** — Anthropic prompting best practices

### Examples
- **`prompts/examples/example-session.md`** — Full walkthrough: vague input → 3 output formats

### Evaluation
- **`evals/test_cases.md`** — 14 functional test cases
- **`evals/adversarial_cases.md`** — 15 boundary and failure mode tests
- **`evals/benchmark.md`** — Cross-model benchmark framework (8 cases)
- **`evals/scoring.md`** — Scoring rubric (clarity, constraints, structure, grounding, leakage)

### Documentation
- **`docs/architecture.md`** — System design and directory map
- **`docs/usage.md`** — Integration and usage guide

## Reference Files

When building prompts, read the relevant references:

- **Task-type blueprints** — Primary reference on every invocation
- **Anthropic prompting guide** — Prompting principles: XML structuring, few-shot, chain-of-thought, grounding
- **Context file template** — For generating project context files
- **GSD/Superpowers output formats** — When plugins are detected
