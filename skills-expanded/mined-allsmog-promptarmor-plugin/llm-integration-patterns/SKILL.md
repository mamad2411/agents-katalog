---
name: LLM Integration Patterns
description: How to identify and analyze LLM integration points across popular frameworks — OpenAI SDK, Anthropic SDK, LangChain, LlamaIndex, Vercel AI SDK
version: 1.0.0
---

# LLM Integration Patterns

## Purpose

Teaches the recon-agent how to find system prompts, tool definitions, guardrails, and data flows in codebases using different LLM frameworks.

## When to Use

- During code reconnaissance (recon-agent)
- When the user asks "where are the LLM integration points?"
- When analyzing a new codebase for the first time

## Framework Detection

| Framework | Detection Patterns |
|-----------|-------------------|
| **OpenAI** | `import openai`, `from openai`, `ChatCompletion`, `chat.completions.create` |
| **Anthropic** | `import Anthropic`, `from anthropic`, `messages.create`, `@anthropic-ai/sdk` |
| **LangChain** | `from langchain`, `ChatOpenAI`, `ConversationChain`, `AgentExecutor`, `@langchain` |
| **LlamaIndex** | `from llama_index`, `VectorStoreIndex`, `QueryEngine`, `ServiceContext` |
| **Vercel AI** | `import { streamText }`, `import { generateText }`, `useChat`, `from 'ai'` |

## Methodology

1. **Detect framework** — Search for import patterns
2. **Find system prompts** — Framework-specific locations (see reference files)
3. **Find tool definitions** — Framework-specific registration patterns
4. **Find guardrails** — Content filters, validators, middleware
5. **Trace data flows** — User input → prompt → LLM → output

## Reference Files

- [OpenAI SDK Patterns](references/openai-patterns.md)
- [Anthropic SDK Patterns](references/anthropic-patterns.md)
- [LangChain Patterns](references/langchain-patterns.md)
- [LlamaIndex Patterns](references/llamaindex-patterns.md)
- [Vercel AI SDK Patterns](references/vercel-ai-patterns.md)
