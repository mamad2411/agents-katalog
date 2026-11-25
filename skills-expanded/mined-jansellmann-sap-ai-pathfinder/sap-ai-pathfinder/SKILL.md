---
name: sap-ai-pathfinder
description: >
  Navigate SAP's AI technology landscape and guide implementation of AI use cases on SAP BTP.
  Use when someone asks which AI approach to use on SAP, how to build AI apps, agents, or ML
  models on SAP BTP, or needs guidance on SAP AI Core, Joule, Generative AI Hub, HANA Cloud ML,
  RPT-1, Document AI, or Joule Skills. Also use when deciding between low-code and pro-code
  agent development, or when planning the architecture of any AI solution in the SAP ecosystem.
license: "Apache-2.0. Based on SAP Architecture Center (github.com/SAP/architecture-center), Copyright 2025 SAP SE or an SAP affiliate company and architecture-center contributors. Licensed under Apache-2.0."
compatibility: Designed for any Agent Skills-compatible AI assistant (Claude Code, OpenAI Codex, VS Code Copilot, Roo Code, and others).
metadata:
  author: Jan Sellmann
  version: "1.0"
  upstream: https://github.com/SAP/architecture-center/tree/dev/docs/golden-path/ai-golden-path
---

# SAP AI Pathfinder

This skill guides architects, developers, and product managers through SAP's AI technology
landscape — from deciding whether AI is needed at all, to selecting the right approach, to
implementing production-ready solutions on SAP BTP.

## Step 1: Qualify the Use Case (Graph 1)

95% of enterprise AI initiatives deliver zero measurable return. Success is determined by the
value provided — not model quality. Ground every AI initiative in a concrete business problem
where AI's strengths genuinely align with operational needs.

**Four-dimension feasibility check:**
1. Business Impact: measurable cost, delay, or quality problem?
2. Data Availability: quality training/evaluation data accessible?
3. Technical Feasibility: can AI integrate with existing workflows?
4. Organizational Readiness: stakeholders prepared for change management?

**Diagnose the problem first — ask these questions:**
- Where do employees spend disproportionate time on repetitive, rule-based tasks?
- Where do delays occur due to information bottlenecks or manual data synthesis?
- Which decisions require rapid analysis of complex data patterns?
- Is this a genuine operational pain point or trend-chasing?

**Double-check: is AI actually the right approach?**
- Would process optimization or traditional automation solve this more effectively?
- Does the problem require pattern recognition, prediction, or content generation at scale?
- Will AI integrate smoothly with existing workflows, or create friction?
- Can the solution learn from feedback and adapt as processes evolve?

**Proceed with AI if:**
- The problem involves repetitive cognitive tasks requiring speed, consistency, and scale
- You have identified an approach with learning capabilities and deep workflow integration
- You can start simple/narrow and expand based on demonstrated value

**Be careful when:**
- Process redesign would solve the core issue more effectively
- You are pursuing AI to match competitors rather than solve a real pain point
- The problem requires judgment, empathy, or contextual understanding current AI cannot provide
- Implementation timeline or cost exceeds the potential operational benefit

**Route determination — outcome of Graph 1:**

| Situation | Outcome |
|---|---|
| Problem is about unclear processes, missing tools, or lack of standardization | Process Optimization — not AI |
| Requires human judgment, creativity, or complex contextual understanding | Human-Driven Process — not AI |
| Solvable with simple if/then rules, fixed decision trees, or deterministic logic | Traditional Automation (RPA, rules engines) — not AI |
| Requires analyzing historical data to predict/classify/detect — WITHOUT content generation | **→ Route A: Specialized AI** |
| Involves content generation, conversation, text understanding, or multi-step reasoning | **→ Route B: Generative AI** |
| Requires historical data analysis AND content generation/conversation | **→ Route B: Generative AI** |
| None of the above fits | Reassess whether automation is actually needed |

## Step 2 — Route A: Specialized AI (Graph 2.a)

Use when Graph 1 identified a need to predict outcomes, classify/categorize, or detect anomalies
from structured data — without content generation or language understanding.

**Decision tree:**
1. Is data **tabular/relational**?
   - No → Custom ML on SAP AI Core (if team has capacity to train/operate) — else reassess
2. Can the task be expressed as **classification or regression on a single table**?
   - Yes → **SAP-RPT-1** (in-context learning, no training required)
   - No → **Custom ML on SAP AI Core** (TensorFlow, PyTorch, scikit-learn)

See [references/classic-ml.md](references/classic-ml.md) for RPT-1 limitations, API details, and Custom ML patterns.

**PAL/APL (HANA Cloud) — specialist path, not in Graph 2.a:**
Graph 2.a routes only to RPT-1 or Custom ML. Use PAL when RPT-1 cannot meet operational constraints:
- Time series forecasting, anomaly detection, or clustering (RPT-1 does not support these)
- Latency < 200ms required (PAL achieves sub-10ms in-database)
- Data must stay within HANA Cloud (governance/residency)
- Explainability required now (RPT-1 explainability targeted H2 2026)

## Step 2 — Route B: Generative AI (Graph 2.b → Graph 3 or Graph 4)

Use when Graph 1 identified content generation, conversation, text understanding, or
multi-step reasoning as the core need.

**Readiness gate — verify before proceeding (Graph 2.b):**
- Quality training data or examples available?
- Clear success metrics defined?
- Integration capability in place?
- Executive sponsorship secured?

If any answer is No: gather data, define metrics, map workflows, secure sponsorship first.

**Agency determination (Graph 2.b):**

| Workflow type | Agency | Continue with |
|---|---|---|
| Single LLM call (single step) | Low/No | Graph 3 below |
| Fixed multi-step sequence — no on-the-fly decisions | Low/No | Graph 3 below |
| Multi-step, on-the-fly decisions expressible as simple rules | Low/No | Hybrid: rule-based workflow + targeted AI components → then Graph 3 |
| Multi-step, on-the-fly decisions requiring human-like reasoning | Medium/High | Graph 4 below |

### Low/No Agency Implementation (Graph 3)

Should users interact with this AI capability through natural conversation?

- **Yes** → **Joule Skill** (conversational via Joule, structured workflow, predefined steps,
  intents & entities, connected to backend GenAI)
  See [references/joule-skills.md](references/joule-skills.md)
- **No** → **Embedded AI** (direct API integration, button/form-based triggers, background processing,
  integrated into existing UI with predictable inputs/outputs)
  See [references/genai-applications.md](references/genai-applications.md)
  - Special case: input is a scanned or semi-structured document and goal is structured data
    extraction (invoices, POs, resumes) → **SAP Document AI** as Embedded AI implementation
    See [references/document-ai.md](references/document-ai.md)

### Medium/High Agency — Agent Implementation (Graph 4)

**Scope determination:**
- **Process Agent** — single domain, predictable requests, specialized workflow (conversational or not)
- **Broad Scope Agent** — multiple domains, high request variance, complex orchestration

**If Broad Scope AND conversational** → **Joule Functions/Agents for Agentic Orchestration**
(multi-domain capability, conversational interface, automatic Joule integration). Stop here.

**All other cases** (Process Agent any type, Broad Scope non-conversational) — choose creation path.
All code-based agents deploy to the unified Agent Fabric runtime on SAP AI Core:

| Complexity | Team preference | Recommended path |
|---|---|---|
| Complex custom logic or highly dynamic data sources | Max control / IDE-based | **Dev IDE (Pro-code)** |
| Complex custom logic or highly dynamic data sources | Lower barrier to entry | **Vibe (Prompt-driven)** |
| Standard logic, manageable integrations | Full control / IDE | **Dev IDE (Pro-code)** |
| Standard logic, manageable integrations | Natural language creation | **Vibe (Prompt-driven)** |

Both paths produce real, inspectable, versionable code — choice is about team preference and
problem complexity, not capability.
See [references/ai-agents.md](references/ai-agents.md) for implementation details and interoperability (A2A, MCP).

## Step 3: Key Implementation Pointers

### GenAI Applications
- Use **SAP AI SDK** (Java, Python, TypeScript) for all LLM interactions — not raw HTTP
- Use **Prompt Registry** to manage prompts — never hardcode prompts in application code
- Use **Orchestration Service** for harmonized multi-model access, content filtering, data masking
- Use **benchmark engineering** (Evaluation Service + Prompt Optimizer) to stay model-agnostic
- Use **CAP** as backend framework with AI SDK integration for enterprise-grade apps
- Log all LLM interactions (prompts, responses, token usage) for auditability

### AI Agents
- Code-based agents (Dev IDE or Vibe path) integrate with Joule via **A2A "Bring Your Own Agent" (BYOA)** pattern
- A2A is SAP's preferred standard for multi-agent collaboration (not raw MCP for external)
- MCP is used internally by Joule for SAP business capabilities access
- Agent Gateway (not yet GA) enables exposing Joule agents to external ecosystems

### Joule Skills (Low Agency)
- Always implement **confirmation dialogs** for create/update/delete operations (AI ethics requirement)
- Use **Joule's built-in Message Generation** instead of static response templates
- Use **asynchronous API requests** for long-running operations (> few seconds)
- Test in standalone environment before deploying to production shared environment

## Gotchas

- **RPT-1 context limits**: RPT-1-small supports 2048 rows, RPT-1-large supports 65,536 rows.
  Requests exceeding these limits will fail. Check GPU availability in target data center before committing.
- **RPT-1: SAP AI SDK does not support RPT-1 yet** — use the `requests` library directly.
  See [references/classic-ml.md](references/classic-ml.md) for the code pattern.
- **Don't start with PAL/APL for classification/regression** — always evaluate RPT-1 first.
  RPT-1 typically delivers better prediction quality with less engineering effort.
- **RPT-1 explainability not yet available**: Model observability targeted July 2026,
  full explainability (column/row level) and RPT-1.5 targeted H2 2026. Use PAL/APL if
  explainability is required now.
- **Model deprecation in production**: LLM model versions get deprecated. Use Prompt Registry
  and Orchestration Service model fallback to avoid production outages when models are retired.
  Monitor SAP Note 3437766 for model availability changes.
- **Agent Gateway is not yet GA**: Full bidirectional Agent Gateway targeted Q4 2026.
  Integration Suite MCP Gateway (Q2 2026) exposes SAP APIs as managed MCP servers but is
  not the full Agent Gateway. Don't architect for inbound external agent consumption yet.
- **Joule Skills ≠ AI Agents**: Use Joule Skills for low-agency conversational workflows.
  Use custom agents (Dev IDE / Vibe paths, or Joule Functions/Agents for broad-scope conversational)
  when complex reasoning, state management across sessions, or external AI model integration is needed.
- **Process Agent vs Broad Scope Agent**: Single-domain/predictable → Process Agent (always Dev IDE
  or Vibe, regardless of whether it's conversational). Multi-domain + conversational → Joule
  Functions/Agents. Multi-domain non-conversational → Dev IDE or Vibe path.
- **Scenario Dependencies are not a substitute for agents**: Chain Joule Skills for simple
  orchestration, but switch to custom agents for complex reasoning or advanced state management.
- **Vibe output is real code**: Vibe (prompt-driven) produces actual, inspectable, versionable code —
  not a low-code configuration. Teams can transition to Dev IDE at any time without rewriting.
- **Extended plan required**: RPT-1 and most GenAI Hub features require SAP AI Core
  Extended plan — not the standard plan.
- **A2A vs MCP boundary**: A2A for external/vendor interoperability; MCP is used
  internally within SAP's Joule infrastructure. Don't expose raw MCP endpoints externally.

## Reference Files

Load these only when the task requires that specific domain:

- [references/genai-applications.md](references/genai-applications.md) — GenAI app architecture, RAG, CAP integration, observability, benchmark engineering
- [references/ai-agents.md](references/ai-agents.md) — Agent building (low-code and pro-code), A2A/MCP interoperability, Joule integration patterns
- [references/joule-skills.md](references/joule-skills.md) — Joule Skill development workflow, capabilities, best practices, tutorials
- [references/classic-ml.md](references/classic-ml.md) — RPT-1, HANA PAL/APL, custom AI Core ML, decision framework, code examples
- [references/document-ai.md](references/document-ai.md) — SAP Document AI service, PaaS vs SaaS patterns, API access, setup
