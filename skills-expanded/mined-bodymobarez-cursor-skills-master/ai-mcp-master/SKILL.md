---
name: ai-mcp-master
description: Master hub for AI, MCP & prompting. Use to build MCP servers, engineer/optimize prompts (incl. advanced prompt & context engineering), camera + AI vision analytics, human-natural code, God-mode autonomous agent behavior, faithful colloquial-Arabic intent→spec→literal execution, and work with AI model APIs. Bundles 15 specialized skills (in skills/<name>/GUIDE.md). Use this for any ai mcp task.
---

# AI, MCP & prompting — Master Hub

Use to build MCP servers, engineer/optimize prompts, and work with AI model APIs.

## How to use this hub

This single skill bundles **all 15 ai mcp skills**. Each bundled skill's full instructions live in `skills/<name>/GUIDE.md` (plus any `scripts/`, `data/`, `references/` next to it).

**Workflow:**
1. Match the user's request to one or more skills in the list below.
2. Read that skill's `skills/<name>/GUIDE.md` for full instructions before acting.
3. Combine multiple bundled skills when a task spans several areas.

## Bundled skills

- **prompt-engineering-advanced** ⭐ — Advanced prompt & context engineering for production LLMs (2026): ROLE/LIMITS/CONTEXT/OUTPUT format, context engineering (Write/Select/Compress/Isolate), few-shot, meta-prompting, ReAct, reasoning-model tips, failure modes, and prompt evals.  
  → `skills/prompt-engineering-advanced/GUIDE.md`
- **camera-ai-vision** ⭐ — Full camera handling + AI visual analytics: getUserMedia/mobile capture, on-device (MediaPipe/TFJS/WebGPU) vs cloud vision-LLM, object/face/pose detection, OCR, barcode/QR scanning, real-time frame pipelines, and privacy.  
  → `skills/camera-ai-vision/GUIDE.md`
- **human-natural-code** ⭐ — Write code & reasoning that read as authentic, human-authored and idiomatic: avoid AI "tells" (line-by-line comments, generic names, over-abstraction), match the project's style, natural naming/comments/commits — passes AI-code detectors by being genuinely natural.  
  → `skills/human-natural-code/GUIDE.md`
- **god-mode-autonomous-agent** ⭐ — Operate at maximum capability/autonomy: deep parallel context gathering, planning, relentless execution, rigorous self-verification (build/test/lint), and follow-through until truly done — with sensible guardrails.  
  → `skills/god-mode-autonomous-agent/GUIDE.md`
- **colloquial-arabic-intent-execution** ⭐ — Turn messy/colloquial ("بالبلدي") or mixed Ar-En instructions into a faithful word-by-word translation (drops nothing) → technical requirement/constraint analysis → **literal execution "بالحذافير"** with no invented scope, at the v2 quality bar.  
  → `skills/colloquial-arabic-intent-execution/GUIDE.md`
- **anthropic-claude-api** — Build, debug, and optimize Claude API / Anthropic SDK apps. Apps built with this skill should include prompt caching. Also handles migrating existing Claude API code between Claude model versions (...  
  → `skills/anthropic-claude-api/GUIDE.md`
- **anthropic-mcp-builder** — Guide for creating high-quality MCP (Model Context Protocol) servers that enable LLMs to interact with external services through well-designed tools. Use when building MCP servers to integrate exte...  
  → `skills/anthropic-mcp-builder/GUIDE.md`
- **blastum-foundation-models** — Add Apple Foundation Models (on-device LLM) to iOS/macOS/visionOS apps. Use when integrating generative AI, guided generation (@Generable), tool calling, content tagging, or custom adapters. Covers...  
  → `skills/blastum-foundation-models/GUIDE.md`
- **blastum-mcp-builder** — Guide for creating high-quality MCP (Model Context Protocol) servers that enable LLMs to interact with external services through well-designed tools. Use when building MCP servers to integrate exte...  
  → `skills/blastum-mcp-builder/GUIDE.md`
- **blastum-vision-ocr** — Extracts text from scanned PDFs and images using Apple Vision OCR (macOS Live Text engine). No dependencies or API keys. Outputs per-page text files. Use when a PDF has no embedded text, when OCR o...  
  → `skills/blastum-vision-ocr/GUIDE.md`
- **cloudflare-agents-sdk** — Build AI agents on Cloudflare Workers using the Agents SDK. Load when creating stateful agents, durable workflows, real-time WebSocket apps, scheduled tasks, MCP servers, chat applications, voice a...  
  → `skills/cloudflare-agents-sdk/GUIDE.md`
- **prompt-engineering** — Write effective prompts for LLMs — structure, few-shot examples, chain-of-thought, system prompts, and output parsing.  
  → `skills/prompt-engineering/GUIDE.md`
- **sentry-agents-md** — Creates and maintains concise AGENTS.md and CLAUDE.md project instruction files. Use when asked to create AGENTS.md, update AGENTS.md, maintain agent docs, set up CLAUDE.md, document repository age...  
  → `skills/sentry-agents-md/GUIDE.md`
- **sentry-claude-settings-audit** — Analyze a repository to generate recommended Claude Code settings.json permissions. Use when setting up a new project, auditing existing settings, or determining which read-only bash commands to al...  
  → `skills/sentry-claude-settings-audit/GUIDE.md`
- **sentry-prompt-optimizer** — Creates, optimizes, and iteratively refines agent prompts, system prompts, developer prompts, and reusable prompt templates. Use when asked to improve a prompt, optimize a system prompt, rewrite an...  
  → `skills/sentry-prompt-optimizer/GUIDE.md`

## Pairs well with

**`color-design-master`** — `ai-color-harmony-prompting` for structured LLM palette generation (use with `prompt-engineering-advanced`).

## Note

These bundled skills are intentionally not registered as separate Cursor skills (their files are `GUIDE.md`, not `SKILL.md`) so only this master appears in the skills list. Read the relevant `GUIDE.md` on demand.
