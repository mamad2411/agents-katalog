---
name: understand-coremind
description: CoreMind specific knowledge graph queries with governance-aware layer mapping and agent hierarchy understanding
argument-hint: <query>
---

# /understand-coremind

Query the CoreMind knowledge graph with governance-aware context. This skill understands the GAOS architecture, agent hierarchy, and 10-stage pipeline.

## Instructions

1. **Load the knowledge graph** from `CoreMind/.understand-anything/knowledge-graph.json`
2. **Parse the query** from `$ARGUMENTS` and determine query type:

### Query Types

**Architecture queries** ("how does X work", "what is the pipeline", "explain governance"):
- Map the query to relevant layers and nodes in the graph
- Explain using the orchestrator governance model:
  - **10-stage pipeline**: IntentParser -> PolicyGate -> GoalLedger -> Planner -> DelegationEngine -> AgentCoordinator -> ReflectionLoop -> OutcomeTracker -> WorldState
  - **4-tier governance**: ALLOW (auto-approve) / REVIEW (human check) / ESCALATE (multi-agent review) / BLOCK (deny)
  - **5-layer safety stack**: Input sanitization -> Policy gate -> Execution sandbox -> Output validation -> Recovery

**Agent queries** ("which agents handle X", "what does the CEO agent do"):
- Search the Agent Framework layer (236 nodes)
- Map agent hierarchy: L0 System Core -> L1 Executives (CEO/CTO/CFO/CMO/COO) -> L2+ Specialists
- Include agent capabilities, tools, and delegation patterns

**Module queries** ("what does the API layer do", "how does knowledge store work"):
- Search the relevant architecture layer
- Include: module purpose, file count, key components, dependencies (from module edges)
- Cross-reference with Memory MCP entities: `mcp__memory__search_nodes("CoreMind:Module:{name}")`

**Impact queries** ("what would break if I change X", "dependencies of core_mind"):
- Find the target node in the graph
- Traverse 1-hop edges (imports, calls, inherits, depends_on)
- Identify cross-layer impact
- Rate risk: LOW (same layer) / MEDIUM (adjacent layers) / HIGH (3+ layers affected)

**Tour queries** ("give me the tour", "where do I start"):
- Return the 15-step guided tour from the knowledge graph
- Each step: title, node, description, why it matters

## CoreMind Architecture Layers (8)

| Layer | Nodes | Key Components |
|-------|-------|----------------|
| Orchestration Core | 276 | CoreMind, Planner, PolicyGate, IntentParser, GoalLedger, DelegationEngine |
| Agent Framework | 236 | BaseAgent, executives (CEO/CTO/CFO/CMO/COO), tools, capabilities |
| Integration Layer | 454 | FastAPI routes, middleware, connectors, interfaces, billing |
| Governance & Safety | 146 | GAOS (5-layer safety), security (RBAC, JWT, hash chain, audit) |
| Knowledge & Learning | 127 | RAG pipeline, knowledge store, evaluation benchmarks |
| Data & Persistence | 181 | SQLAlchemy models (15 entity types), repositories |
| Presentation | 436 | Next.js frontend, 5 product surfaces (Forge, Helios, Nova, Command, Studio) |
| Cross-Cutting | 55 | LLM providers (OpenAI, Anthropic, Ollama, Kimi), model router |

## Response Format

Always include:
1. **Direct answer** to the query
2. **Graph context**: which nodes/layers are relevant
3. **Governance implications**: does this touch governance/safety layers?
4. **Suggestion**: related areas to explore or commands to run (`/understand-explain`, `/understand-chat`)
