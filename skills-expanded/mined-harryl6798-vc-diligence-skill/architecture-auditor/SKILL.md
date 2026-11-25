---
name: architecture-auditor
description: Specialized technical auditor for deep startup architecture teardowns and high-fidelity visual design specifications. Handles component-by-component forensics and maps technical moats for VC diligence.
---

# Architecture Auditor Skill: The CTO's Forensic Handbook

This skill is designed to perform exhaustive technical audits of startup architectures. It moves beyond high-level boxes into "Plumbing Forensics"—identifying specific libraries, API patterns, and infrastructure moats.

## 1. THE RESEARCH MANDATE (EVIDENCE ARTIFACTS)
Before specifying a diagram, you MUST harvest the "Ingredients of Truth":
- **Library Forensics**: Search for specific implementation details (e.g., "Uses LangChain for orchestration with custom Pydantic schemas").
- **API Specifics**: Identify actual endpoint names, event codes (e.g., `DATA_INGESTED`, `INFERENCE_COMPLETE`), and auth protocols.
- **Model Tiering**: Map exactly which models are used for which tasks (e.g., "Llama-3-8b for routing, GPT-4o for final aggregation").

## 2. TECH STACK AUDIT CHECKLIST
Identify the specific providers and libraries used in the following layers to determine if it is a "proprietary moat" or a "commodity wrapper."

### 2.1 Core AI & Orchestration
- **Model Providers**: OpenAI (GPT-4o/o1), Anthropic (Claude 3.5), Meta (Llama 3), or Google (Gemini).
- **Orchestration**: LangChain, LlamaIndex, Haystack, or custom Python/FastAPI logic.
- **Fine-Tuning**: LoRA/QLoRA implementations, Unsloth, or proprietary training on H100 clusters.

### 2.2 Vector & Data Infrastructure
- **Vector Databases**: Pinecone, Milvus, Weaviate, Qdrant, or pgvector.
- **Data Curation**: Snorkel, Scale AI, or proprietary labeling pipelines.
- **Streaming/Real-time**: Kafka, RabbitMQ, or Upstash.

### 2.3 Observability & Safety
- **Evaluations**: Ragas, TruLens, or Giskard.
- **Monitoring**: LangSmith, Weights & Biases (W&B), or Arize Phoenix.
- **Guardrails**: NeMo Guardrails, Llama Guard, or custom PII filtering.

## 3. SYSTEM ARCHITECTURE PATTERNS
Look for these high-fidelity patterns to understand the "intelligence density" of the system.

### 3.1 RAG (Retrieval-Augmented Generation)
- **What to look for**: Multi-stage retrieval (Hybrid search), reranking (Cohere Rerank), and metadata filtering.
- **Moat check**: Are they using "naive RAG" or sophisticated "Agentic RAG" with self-correction?

### 3.2 Gated Ensemble Pipelines
- **What to look for**: Routing logic that sends "easy" queries to small models (Llama-3-8b) and "hard" queries to large ones (o1).
- **Moat check**: This indicates a compute-efficiency moat.

### 3.3 Autonomous Agent Workflows
- **What to look for**: Tools like CrewAI, AutoGPT, or custom loops using Tool-Calling APIs.
- **Moat check**: Does the agent have "Environment Memory" or is it a single-shot execution?

## 4. THE COMPONENT-BY-COMPONENT TEARDOWN
For each technical section of the report:
1.  **Gated Logic**: Describe the "Early Exit" or "Escalation" conditions between model layers.
2.  **Infrastructure Bottlenecks**: Identify exactly where latency or cost issues exist (e.g., "Vector DB query latency at 500ms+ due to high dimensionality").
3.  **Moat Verification**: Prove if a component is proprietary or off-the-shelf by auditing GitHub dependencies or whitepaper citations.

## 5. THE VISUAL DESIGN SPECIFICATION (VDS)
This is the formal prompt passed to the `excalidraw-diagram` skill. Generic specs are failures.

### 5.1 VDS Checklist:
- **Technical Diagram**: Map the data journey from Input to Output. 
    - **Annotations**: Every box must contain its technical purpose + dependency name.
    - **Binding**: Use the Two-Way Binding Protocol (Shape `boundElements` <-> Text `containerId`).
- **Market Diagram**: Use the "Displacement Path" pattern.
    - **Nodes**: Annotate incumbents with their market share % and key technical weakness.
- **Economic Graphs**: Use annotated axes with specific milestones (e.g., "Seed Round Achieved").

## 6. INTEGRATION PROTOCOL
When called by the `vc-diligence` skill:
1.  Read the raw findings in `raw_findings/tech/`.
2.  Perform any missing "Least-to-Most" technical sub-queries.
3.  Draft the `technical_commercial_deep_dive.md` section for Architecture.
4.  Generate the finalized Visual Design Specification for delegation.

---
*End of Architecture Auditor Skill.*
