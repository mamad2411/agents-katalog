# 12 AI Skills Roadmap 2026

The 12 AI capabilities that separate operators from spectators in 2026. Use this skill to advise on learning priorities, design AI-powered workflows, evaluate tool stacks, and build competency plans for any of the 12 domains.

Source: AI Emergence / AI Genesis content series — distilled into executable prompts.

---

## The 12 Skills at a Glance

```
01 PROMPT ENGINEERING      Goal → Context → Format → Precise AI Output
02 AI WORKFLOW AUTOMATION  Trigger → Action → Process → Result (no-code)
03 AI AGENTS               Plan (A) → Reason (B) → Execute (C) → Better Results
04 RAG                     Knowledge Sources → Retrieve → Augment Prompt → Grounded Answer
05 STAYING UPDATED         Curate → Synthesize → Apply → Share
06 MULTIMODAL AI           Text + Image + Audio + Code → ONE MODEL
07 FINE-TUNING & ASSISTANTS General-Purpose → Fine-Tuned → Domain Expert
08 VOICE AI & AVATARS      Voice Input → AI Processing → Talking Avatar
09 AI TOOL STACKING        Plan → Build → Execute → Scale (stacked tools)
10 AI VIDEO CONTENT        Script → Scenes → Voiceover → Publish
11 SAAS DEVELOPMENT        Idea → Build (no-code) → Iterate → Launch
12 LLM MANAGEMENT          Accuracy ↑ · Latency ↓ · Cost ↓
```

---

## Skill Prompts

### 01 — Prompt Engineering

**Tools**: ChatGPT · Claude · Gemini · Grok · Perplexity

```
Act as an expert prompt engineer. Rewrite the following request into a high-performance prompt using the Goal–Context–Format structure:

RAW REQUEST: [paste the request here]

Deliver:
- GOAL: One sentence defining the exact outcome needed
- CONTEXT: The background, constraints, audience, and tone the AI must know
- FORMAT: Output structure (length, sections, style, examples if needed)
- ROLE: The expert persona the AI should adopt
- CHAIN: If the task needs multiple steps, break it into a prompt sequence

Output: The rewritten prompt, ready to paste, plus a one-line explanation of what each section unlocks.
```

---

### 02 — AI Workflow Automation

**Tools**: Zapier · Make · n8n · Bardeen · Notion AI

```
Act as an automation architect. Design an AI-powered workflow for [BUSINESS PROCESS]:

WORKFLOW DESIGN:
- TRIGGER: What event starts this workflow? (new email, form submission, schedule, webhook)
- ACTIONS: List each step the automation performs in sequence
- AI LAYER: Where does an LLM plug in? (summarize, classify, draft, decide)
- DATA FLOW: What data moves between steps and how is it transformed?
- ERROR HANDLING: What happens when a step fails?
- TOOL RECOMMENDATION: Which platform handles this best (Zapier / Make / n8n)?

Produce: A named workflow, step-by-step diagram in plain text, and implementation notes.
```

---

### 03 — AI Agents

**Tools**: CrewAI · LangGraph · AutoGen · LangChain · Claude Agent SDK

```
Act as a multi-agent systems designer. Build an agent team for [TASK]:

AGENT ARCHITECTURE:
- ORCHESTRATOR: What is the lead agent's role and decision logic?
- SUBAGENTS: List each specialist agent (name, role, tools available)
- SHARED TASK: What is passed between agents and in what format?
- COMMUNICATION: How do agents hand off work? (sequential / parallel / hierarchical)
- MEMORY: What shared memory or context store do agents use?
- TERMINATION: What signals that the task is complete?

Produce: Agent roster, workflow sequence, tool manifest per agent, sample inter-agent message format.
```

---

### 04 — Retrieval-Augmented Generation (RAG)

**Tools**: LlamaIndex · Haystack · LangChain · Vectara

```
Act as a RAG pipeline architect. Design a retrieval system for [KNOWLEDGE BASE / USE CASE]:

RAG DESIGN:
- KNOWLEDGE SOURCES: What documents/databases/APIs are indexed? (PDFs, URLs, databases, wikis)
- CHUNKING STRATEGY: How is content split for embedding? (size, overlap, metadata)
- EMBEDDING MODEL: Which embedding model and why?
- VECTOR STORE: Which vector database? (Pinecone / Weaviate / Chroma / Qdrant)
- RETRIEVAL LOGIC: Top-K, semantic search, hybrid search, reranking?
- AUGMENTATION: How is retrieved context injected into the prompt?
- EVALUATION: How do you measure retrieval accuracy and answer quality?

Produce: Architecture diagram (text), tool selection rationale, sample retrieval query + augmented prompt.
```

---

### 05 — Staying Updated

**Sources**: The Verge · TechCrunch · VentureBeat · MIT Technology Review · Feedly

```
Act as my AI intelligence curator. Build a personalized AI news monitoring system:

MY CONTEXT:
- Role/industry: [describe]
- Top 3 AI topics I care about: [list]
- Time available: [X minutes/day]

Design:
- SOURCE LIST: The 5 most signal-rich sources for my context (name + why)
- READING RHYTHM: Daily digest / weekly deep-dive schedule
- FILTER CRITERIA: What makes a story worth reading vs. skipping?
- SYNTHESIS HABIT: How do I turn news into actionable insight each week?
- SHARING SYSTEM: How do I repurpose insights for my audience?

Output: Curated source list, weekly reading schedule, a reusable weekly summary prompt I can run every Monday.
```

---

### 06 — Multimodal AI

**Tools**: Claude · ChatGPT · Grok · Gemini

```
Act as a multimodal AI strategist. Identify where multimodal capabilities add the most leverage for [BUSINESS / ROLE]:

MULTIMODAL AUDIT:
- TEXT TASKS: Where is text already handled well?
- IMAGE TASKS: What visual analysis, generation, or OCR would save time?
- AUDIO TASKS: What transcription, voice analysis, or audio generation is needed?
- CODE TASKS: What code generation, review, or debugging workflows apply?
- COMBINED FLOWS: Where do 2+ modalities combine in a single task?

For each identified use case:
- Which multimodal model handles it best?
- What is the prompt/API call structure?
- What is the estimated time saving?

Output: Prioritized opportunity map, top 3 quick-win use cases with starter prompts.
```

---

### 07 — Fine-Tuning & AI Assistants

**Tools**: OpenAI GPT Builder · Hugging Face · Cohere · NVIDIA · Flowise

```
Act as an AI assistant architect. Design a domain-specific AI assistant for [DOMAIN / COMPANY]:

ASSISTANT DESIGN:
- PERSONA: Name, role, tone, boundaries of the assistant
- KNOWLEDGE BASE: What domain knowledge must it have? (documents, SOPs, FAQs, data)
- FINE-TUNING vs RAG: Should this use fine-tuning (behavior/style) or RAG (knowledge)? Justify.
- SYSTEM PROMPT: Draft the complete system prompt
- TOOL ACCESS: What tools/APIs can the assistant call?
- GUARDRAILS: What must the assistant never do or say?
- EVALUATION: How do you test quality before deployment?

Output: Complete assistant specification document, system prompt draft, evaluation checklist.
```

---

### 08 — Voice AI & Avatars

**Tools**: ElevenLabs · HeyGen · Synthesia · VAPI

```
Act as a voice and video AI producer. Design a voice/avatar content system for [BRAND / USE CASE]:

PRODUCTION DESIGN:
- VOICE PERSONA: What tone, accent, pacing, and energy does the voice need?
- VOICE TOOL: ElevenLabs (cloning/TTS) vs VAPI (conversational) — which and why?
- AVATAR TYPE: Stock avatar (HeyGen/Synthesia) vs custom — requirements and tradeoffs
- CONTENT PIPELINE: Script → Voice → Avatar → Final edit → Publish (tool for each step)
- USE CASES: Sales video, training, podcast, social content, customer service bot?
- BRAND CONSISTENCY: How do voice and visual style stay consistent across outputs?

Output: Production workflow, tool stack with cost estimate, sample script + voice direction notes.
```

---

### 09 — AI Tool Stacking

**Tools**: Notion · ClickUp · Asana · Zapier

```
Act as a productivity systems architect. Design an AI tool stack for [TEAM SIZE / FUNCTION]:

STACK DESIGN:
PLAN layer: Which tool manages ideas, projects, and tasks?
BUILD layer: Which automation platform connects the tools?
EXECUTE layer: Which AI assistants handle day-to-day work?
SCALE layer: Which analytics/monitoring tools measure performance?

For each layer:
- Primary tool + rationale
- AI features to activate
- Integration with other layers

WORKFLOW EXAMPLES:
- Map 3 recurring workflows through the full stack
- Identify where AI eliminates the most manual work

Output: Stack diagram (text), integration map, implementation priority order.
```

---

### 10 — AI Video Content Generation

**Tools**: Runway · VEED · Opus Clip · OpenAI Sora

```
Act as an AI video content director. Build a video production pipeline for [CONTENT TYPE / CHANNEL]:

PIPELINE DESIGN:
SCRIPT: How is the script generated or refined with AI?
SCENES: Which tool generates or sources visuals? (Runway / Sora / stock)
VOICE: Text-to-speech or cloned voice — which tool and voice profile?
EDIT: AI-assisted editing workflow (VEED / CapCut / Descript)
PUBLISH: Auto-distribution to which platforms?

CONTENT FORMATS:
- Short-form (60s): hook, value, CTA structure
- Long-form (10min): outline → talking points → scenes
- Clips from long-form: how Opus Clip identifies viral moments

Output: Full production SOP, tool stack, cost per video estimate, sample script template.
```

---

### 11 — AI-Powered SaaS Development

**Tools**: Lovable · Cursor · Windsurf · Bubble

```
Act as a no-code/AI-code SaaS product architect. Design the MVP for [PRODUCT IDEA]:

MVP BLUEPRINT:
- PROBLEM: What specific pain does this solve? (one sentence)
- USER: Who is the primary user and what is their current workaround?
- CORE FEATURE: The single feature that delivers the value promise
- AI LAYER: Where does AI create the competitive advantage in the product?
- TOOL CHOICE: Lovable (UI-first) / Bubble (complex logic) / Cursor (code-with-AI) — which and why?
- BUILD SEQUENCE: Steps 1–10 from blank canvas to first paying user
- VALIDATION: How do you test demand before building the full product?

Output: MVP spec, tool recommendation + rationale, 10-step build sequence, pre-launch validation checklist.
```

---

### 12 — LLM Management

**Tools**: PromptLayer · Helicone · TruLens · Arize AI · Phoenix

```
Act as an LLM operations engineer. Design the monitoring and management system for [AI APPLICATION]:

LLM OPS DESIGN:
- ACCURACY METRICS: How do you measure response quality? (evals, rubrics, human review rate)
- LATENCY TARGETS: What are acceptable p50/p95 latency thresholds?
- COST CONTROLS: What is the per-query cost budget? What triggers an alert?
- PROMPT VERSIONING: How are prompt changes tracked and rolled back?
- A/B TESTING: How do you compare model/prompt versions in production?
- OBSERVABILITY STACK: Which tools for logging, tracing, dashboarding?
- ALERTING: What conditions trigger an incident? What is the on-call response?

Output: LLM ops dashboard spec, alerting thresholds, prompt versioning SOP, observability tool stack.
```

---

## Quick Reference: Tool Matrix

| Skill | Primary Tools | When to Use |
|---|---|---|
| Prompt Engineering | Claude, ChatGPT, Gemini | Any AI interaction needing precision |
| Workflow Automation | Zapier, Make, n8n | Recurring multi-app processes |
| AI Agents | CrewAI, LangGraph, AutoGen | Multi-step autonomous tasks |
| RAG | LlamaIndex, Haystack, Vectara | Internal knowledge + AI |
| Staying Updated | Feedly, The Verge, TechCrunch | Continuous learning habit |
| Multimodal AI | Claude, Gemini, Grok | Tasks spanning text/image/audio |
| Fine-Tuning | HuggingFace, Cohere, OpenAI | Domain-specific AI behavior |
| Voice AI & Avatars | ElevenLabs, HeyGen, Synthesia | Scalable video/voice content |
| AI Tool Stacking | Notion, ClickUp, Zapier | Team productivity systems |
| AI Video | Runway, VEED, Opus Clip | Content at scale |
| SaaS Development | Lovable, Cursor, Bubble | Building AI products fast |
| LLM Management | Helicone, TruLens, Arize | AI in production |
