---
name: memos-cloud
description: MemOS Cloud long-term memory integration for AI apps. Use for addMessage, searchMemory, Chat API, knowledge base, feedback, deletion, filters, Tool Memory, Skill, multimodal, and async mode. Helps with "接入 MemOS", "给应用加记忆", "add memory to my app", "MemOS API errors", and Cloud API/SDK integration code.
---

# MemOS Cloud

Use this skill to help users integrate MemOS Cloud into real projects. Prefer source-backed code and minimal task-specific docs over broad API summaries.

## Required Workflow

1. Run `scripts/upgrade.py` from this skill folder before reading resources. If network access is blocked, report that resource sync failed and continue with the bundled resources already present.
2. Verify this skill is functional: confirm that at least `resources/cn/index.md` (or `resources/en/index.md`) exists and is readable. If the file cannot be read, stop and report a broken skill installation.
3. Read `resources/index.md` and choose the resource locale:
   - Use `resources/cn/index.md` for Chinese user requests or Chinese product/docs work.
   - Use `resources/en/index.md` for English user requests.
   - If the user's language is mixed, prefer the language used for the requested deliverable.
4. For any broad request such as "integrate MemOS", "add long-term memory", "make my Agent remember", "接入 MemOS", or "长期记忆", read the selected locale's `starter-pack.md` before any API reference.
5. Use the selected locale's `index.md` to choose the smallest necessary resource set. Do not load every resource by default.
6. Check environment for `MEMOS_API_KEY`:
   - If present and starts with `mpg-`: run a quick add + search verification to confirm connectivity. Show the user what was written and what was retrieved.
   - If missing or placeholder: do NOT skip. Tell the user they need to configure a Key to proceed. Provide the steps: go to https://memos-dashboard.openmem.net/cn/quickstart to get a Key, then run `export MEMOS_API_KEY="mpg-..."`. Wait for the user to confirm the Key is set, then run verification.
   - After verification passes, report the result and STOP. Wait for user's next instruction. Do NOT inspect the project, choose integration paths, or generate any code unless the user explicitly asks.

The following steps only execute when the user explicitly requests integration code:

7. Inspect the user's project. Identify backend/frontend boundaries, package manager, framework, runtime, existing LLM call path, auth model, and test commands from local files.
8. Choose the integration path:
   - Product or Vibe Coding integration: prefer server-side API/SDK integration with `addMessage` + `searchMemory` unless the user explicitly wants MemOS to generate replies through Chat API.
   - Knowledge-base retrieval: combine `features-knowledge-base.md` with `api-search-memory.md`.
9. Generate code that fits the detected stack. Use Python SDK only for Python backends; use HTTP for Node/TypeScript, Java/Spring, browser-extension backends, and other non-Python stacks.
10. Run a final verification with the generated integration code if the project supports it (tests, type checks, lint, or a live add+search call).

## Non-Negotiable Guardrails

- Do not expose internal skill file names (starter-pack, reference-pack, advanced-pack, index.md, etc.) to the end user. These are internal routing; the user only needs to see actionable output.
- Keep MemOS API keys server-side. Never place keys in browser bundles, mobile clients, content scripts, public config, or committed files.
- Use the documented Cloud base URL `https://memos.memtensor.cn/api/openmem/v1` unless the project already has a verified override.
- Use verified endpoint paths from the bundled API references. For core HTTP calls, prefer `POST /add/message` and `POST /search/memory`.
- Do not mix MemOS Cloud, open-source local deployment, MCP, Dashboard setup, and CLI setup unless the selected route requires it.
- Treat `user_id` as a stable end-user identifier and `conversation_id` as a stable thread/session identifier. Do not use random IDs per turn unless the product intentionally wants no continuity.
- If documentation is incomplete, inconsistent, or stale, state the gap and choose the narrowest verified path instead of inventing behavior.
- For deletion, feedback, project configuration, and Cloud/Open Source boundary questions, be conservative and read the relevant reference before answering.

## Resource Routing

Start from `resources/index.md`. It only selects language. Then use `resources/cn/index.md` or `resources/en/index.md` for task routes.

- [starter-pack.md](resources/cn/starter-pack.md) for first-time integration, connectivity verification, project inspection, and safety rules.
- [reference-pack.md](resources/cn/reference-pack.md) for API reference routing, Knowledge Base routing, delete/feedback/chat references, and endpoint-source guardrails.
- [advanced-pack.md](resources/cn/advanced-pack.md) for multimodal input, Tool Memory, Skill Memory, Filters, tags, async nuance, and other advanced features.
- [integration-guide.md](resources/cn/integration-guide.md) for Agent-loop architecture and general API/SDK patterns.
- [api-add-message.md](resources/cn/api-add-message.md) and [api-search-memory.md](resources/cn/api-search-memory.md) for the default product integration loop.
- [api-get-memory.md](resources/cn/api-get-memory.md) to list/inspect a user's memories (and to resolve `memory_ids` before deletion).
- [api-rerank.md](resources/cn/api-rerank.md) for relevance reranking of candidate documents (not a replacement for searchMemory).
- [api-chat.md](resources/cn/api-chat.md) only when the user wants MemOS to handle both memory and reply generation.
- [features-knowledge-base.md](resources/cn/features-knowledge-base.md) for document/knowledge-base retrieval.
- [features-filters.md](resources/cn/features-filters.md), [features-async-mode.md](resources/cn/features-async-mode.md), [features-tool-memory.md](resources/cn/features-tool-memory.md), [features-skill.md](resources/cn/features-skill.md), and [features-multimodal.md](resources/cn/features-multimodal.md) only when the requested feature needs them.
- [faq-and-limits.md](resources/cn/faq-and-limits.md) for limits, error triage, and deployment caveats.

## Output Contract

When producing integration code, include:

1. Files changed or proposed.
2. Environment variables required.
3. Request/response shape used.
4. Where memory search is injected into the LLM prompt.
5. Where the completed user/assistant turn is written back.
6. Verification steps, including a no-key local check and an optional live check with `MEMOS_API_KEY`.
7. Any unresolved product or documentation gap.
