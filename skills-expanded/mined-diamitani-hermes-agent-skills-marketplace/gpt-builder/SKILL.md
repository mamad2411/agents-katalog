---
name: gpt-builder
description: "Use when designing, building, or refining custom GPTs. Covers system instructions, prompt engineering, optimization, and deployment. Consolidates Custom GPT Builder Guide, Compass GPT Builder, Custom GPT Guide, GPT Project Instructions Builder, GPT Creator Pro, and GPT Configurator."
version: "1.0"
tags:
  - gpt
  - openai
  - prompt-engineering
  - system-instructions
  - ai-configuration
---

# GPT Builder

## Overview

End-to-end guide for creating custom GPTs in ChatGPT. Covers system instruction design, knowledge file preparation, capability configuration, testing methodology, and iterative refinement. Applies prompt engineering best practices to produce reliable, on-brand GPTs.

## When to Use

- A user wants to build a new custom GPT from scratch
- An existing GPT needs system instruction refinement or optimization
- Converting a prompt template into a distributable GPT
- Troubleshooting a GPT that doesn't follow instructions consistently
- Configuring GPT capabilities (Code Interpreter, Web Browsing, DALL·E, Actions)
- Adding structured knowledge files or API Actions to a GPT

## How It Works

1. **Requirements Gathering** — Define the GPT's purpose, audience, tone, and constraints.
2. **System Instruction Design** — Write the core prompt following structured methodologies.
3. **Capability Configuration** — Select and configure tools (browsing, code, image gen, actions).
4. **Knowledge & Actions** — Prepare upload files and API schemas.
5. **Testing & Refinement** — Iterative test cases, edge-case validation, and optimization.

## Steps

### Step 1: Define the GPT Profile
Answer these before writing any instructions:
- **Name**: Short, descriptive, memorable
- **Purpose**: What problem does it solve? (one sentence)
- **Persona**: Expert, coach, assistant, analyst, creative partner?
- **Audience**: Who will use this? (skill level, context)
- **Output format**: What should responses look like? (structured, conversational, code-heavy?)
- **Guardrails**: What should the GPT NEVER do?

### Step 2: Write System Instructions
Structure using the **CORE framework**:

```
## Role
You are [name], a [persona] that [purpose].

## Context
[Background information the GPT needs to know]

## Instructions
- [Behavioral rule 1]
- [Behavioral rule 2]
- [Formatting rules]
- [When to ask clarifying questions]
- [When to push back or say no]

## Constraints
- NEVER [forbidden action 1]
- ALWAYS [mandatory behavior 1]
- If unsure, [default behavior]

## Examples
User: [example input]
Assistant: [ideal response]
```

### Step 3: Configure Capabilities
- **Web Browsing**: On if the GPT needs live data. Include instructions on when to search vs. use knowledge.
- **DALL·E Image Generation**: On if visual output needed. Specify style, aspect ratio, and generation rules in instructions.
- **Code Interpreter**: On if the GPT needs to run code, analyze files, or produce charts. Specify which file types to accept.
- **Actions**: Configure OpenAPI schemas for external API calls. Test with minimal schemas first.

### Step 4: Prepare Knowledge Files
- Format: `.txt`, `.pdf`, `.md`, `.json`, `.csv` (max 20 files, ~2M tokens total)
- Structure files with clear headings for retrieval accuracy
- Deduplicate information — retrieval doesn't work well with redundancy
- For large documents, chunk into topic-specific files for better retrieval

### Step 5: Test Iteratively
Run these test categories:
1. **Happy path**: Does it do the main job correctly?
2. **Edge cases**: Unusual inputs, empty inputs, very long inputs
3. **Guardrail tests**: Does it refuse when it should?
4. **Tone tests**: Does the persona hold across different question types?
5. **Knowledge tests**: Does it correctly reference uploaded files?

### Step 6: Publish & Iterate
- Set visibility: Only me / Anyone with link / Public GPT Store
- Add a conversation starter list (4 prompt suggestions)
- After 10-20 real uses, review conversations and refine instructions

## Common Pitfalls

- **Overly long instructions**: GPTs follow shorter, clearer instructions better. If over ~3000 words, prune.
- **Contradictory rules**: "Be concise" + "Be thorough" causes confusion. Pick one per context.
- **No examples**: Without concrete input/output examples, behavior is inconsistent.
- **Ignoring knowledge file retrieval**: GPTs don't automatically scan all files. Structure files so retrieval finds the right content.
- **Not testing with real users**: Your own testing is biased. Get 3+ other people to try it.

## Source

Consolidates: Custom GPT Builder Guide, Compass GPT Builder, Custom GPT Guide, GPT Project Instructions Builder, GPT Creator Pro, GPT Configurator.
