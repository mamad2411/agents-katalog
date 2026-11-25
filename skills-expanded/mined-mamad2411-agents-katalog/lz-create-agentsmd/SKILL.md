---
name: lz-create-agentsmd
description: 'Interactive workflow to generate a full-lifecycle AGENTS.md using semantic AST/LSP analysis and chained user interviews.'
---

# `lz-create-agentsmd` Workflow

You are an expert AI engineering architect. Your task is to generate a comprehensive `AGENTS.md` file in the root of this repository that enforces full-lifecycle engineering guardrails based on Context Engineering research.

You MUST execute this workflow in the following three phases exactly as described.

## Phase 1: Deep Semantic & AST/LSP Scan
You must thoroughly analyze the repository to extract business terms and architectural patterns.
1. **Tech Stack Discovery:** Read package manager files (`package.json`, `.csproj`, `pom.xml`, etc.) to identify the core languages and test frameworks.
2. **Semantic / AST Search:** Do not rely on simple regex grep. Use your AST or LSP semantic search tools (if available) to traverse the codebase structure. If not available, do a deep file-read traversal.
3. **Discover Ubiquitous Language (DDD):** Identify the core business entities by looking at the Database Models, Entities, or domain classes.
4. **Discover Gold Standard Files:** Find the 2-3 highest quality files that perfectly demonstrate the repository's desired architecture (e.g. a perfect Controller, a perfect Service class). These will be used for "Progressive Disclosure" to prevent Context Rot in the markdown.

## Phase 2: User Interview (Chained `ask_question`)
You MUST NOT generate the file yet. You must present your findings and interview the user using your `ask_question` tool.
Iteratively ask the user:
1. "I have detected the following core Domain entities: `[List]`. Do you want to enforce these as the strict Ubiquitous Language so future agents don't hallucinate variable names?" (Allow them to add/remove terms).
2. "I found `[File 1]` and `[File 2]` as excellent representations of your architecture. Should I set these as the 'Gold Standard' reference files, or do you have better examples?"
3. "What is the exact CLI command required to run the automated tests with coverage for this project?"
4. "Are there any strict negative constraints or security policies you want enforced? (e.g. 'Never use raw SQL', 'Always use AWS Secrets Manager')."
5. "What are your Git and Workflow conventions? (e.g., branch naming like `feature/JIRA-123`, rules against force pushing, commit formats)."

## Phase 3: Template Generation
Once you have the user's explicit answers from Phase 2:
1. Read the `TEMPLATE_AGENTS.md` file located in your skill directory to understand the exact structure required.
2. Inject the user's validated answers (DDD terms, Gold Standard file links, Test commands, Security rules) into the template structure.
3. Write the final `AGENTS.md` to the root of the user's repository.
4. Print a success message confirming the full-lifecycle engineering guardrails have been applied.
