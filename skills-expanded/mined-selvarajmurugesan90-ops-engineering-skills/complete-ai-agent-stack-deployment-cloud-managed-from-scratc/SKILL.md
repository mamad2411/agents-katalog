---
name: complete-ai-agent-stack-deployment-cloud-managed-from-scratch
description: >
  Sequences a complete, end-to-end AI agent stack deployment built on
  managed cloud services from scratch — a cloud landing zone, agent
  control-flow architecture, an LLM gateway routing across managed
  provider APIs (vendor-neutral: Anthropic/OpenAI/Azure OpenAI/Bedrock/
  Vertex AI), a managed vector database for RAG, MCP servers for tool
  access, an evaluation-and-guardrails harness, and cost/latency
  monitoring. This is an integration/orchestration skill that sequences
  several existing tool-specific skills in the correct order and flags the
  handoff points between them — it does not restate their internals. Use
  when a user asks to "build a production AI agent stack using managed LLM
  APIs from scratch," "stand up an agent platform with a managed vector
  database and MCP tools," "give me the end-to-end sequence for a
  cloud-managed agent deployment," or "design the full pipeline from cloud
  account to a production agent with evals and cost monitoring."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: ai-agent
  maturity: stable
---

# Complete AI Agent Stack Deployment (Cloud-Managed) From Scratch

## Purpose

A production AI agent is not one component — it's a chain of dependent
layers (account guardrails, an agent control loop, LLM provider access, a
knowledge-retrieval layer, tool access, a safety net, and cost/latency
visibility) that only work as a coherent, safe system if wired up in the
right order. Skip or mis-sequence a layer and the failure shows up
somewhere confusing: an agent architecture designed before an LLM gateway
exists hardcodes a single provider's SDK directly into agent code, making
the later "add a fallback provider" phase a rewrite instead of a config
change; or an MCP server is connected to a live agent before an evaluation
harness exists, so the first prompt-injection-via-tool-output regression
is discovered by a user, not a test suite. This skill sequences the
cloud-managed version of that whole path — landing zone through cost
monitoring — deliberately using vendor-neutral language for the LLM
provider and vector database layers, since the managed-service choice at
each of those layers is a real decision this skill defers to the reader
rather than assumes.

## When to use

- Standing up a new production AI agent for a team or organization that
  wants to build on managed cloud services (LLM provider APIs, a managed
  vector database, cloud landing-zone guardrails) rather than self-hosting
  the model-serving and vector-database layers.
- Deciding the right order to introduce an LLM gateway, RAG/vector search,
  MCP tool access, an evaluation harness, and cost monitoring into an
  agent that currently has none of them.
- Auditing an existing agent deployment for a skipped or out-of-order
  phase (e.g. MCP tools connected before an evaluation harness existed, or
  cost monitoring added only after a surprising invoice).
- Rebuilding a reference agent platform (a second product line, a second
  team) that should follow the same proven sequence as a known-good first
  deployment.
- Explaining to a team the full dependency chain for a cloud-managed
  agent stack build-out, phase by phase.

## Prerequisites & environment

- A cloud account/subscription/project that conforms to a real landing
  zone — this skill does **not** cover account/OU, Management Group, or
  folder design; see whichever applies:
  [aws-landing-zone-setup](../../../cloud/skills/aws-landing-zone-setup/SKILL.md),
  [azure-landing-zone-setup](../../../cloud/skills/azure-landing-zone-setup/SKILL.md),
  or
  [gcp-landing-zone-setup](../../../cloud/skills/gcp-landing-zone-setup/SKILL.md).
  Confirm outbound network egress from the workload account/subscription/
  project to the chosen LLM provider(s) and managed vector database is
  actually permitted by the landing zone's guardrails before wiring any
  agent code against them.
- API credentials for at least one LLM provider (and ideally a second, for
  fallback), stored in a secrets manager and injected at runtime — never
  committed to code or the gateway's config file in plaintext.
- An account with a managed vector database service (Pinecone is the most
  common fully-managed choice; Weaviate/Milvus also offer managed tiers).
- A decision on which agent framework/runtime will host the control loop
  (a raw API loop, an agent SDK, or a CLI agent host) — this skill is
  framework-agnostic and assumes that choice is made independently.
- A representative set of real or realistic task inputs available before
  Phase 6, for building the evaluation harness — collecting these after
  the agent is already live is possible but produces a weaker initial eval
  set than gathering them deliberately up front.

## Step-by-step guidance

This is the phase sequence. Each phase links to the skill that covers its
full depth; the text here covers only the sequencing and integration
decisions between phases.

1. **Phase 1 — cloud landing zone.** Confirm (or stand up) the account/
   subscription/project guardrails, centralized logging, and network
   egress policy per whichever cloud landing-zone skill applies. Verify
   specifically that the workload environment's network policy allows
   outbound HTTPS to the LLM provider(s) and managed vector database
   endpoint(s) this stack will call — a landing zone's default-deny
   egress policy (a common, otherwise-reasonable guardrail) silently
   breaks every downstream phase with a generic timeout that looks like a
   provider outage rather than a network policy (see Common pitfalls).

2. **Phase 2 — agent architecture design.** Design the control loop
   (ReAct-style, plan-and-execute, or finite-state), termination
   condition, iteration cap, and tool-boundary classification (read-only
   vs. reversible-write vs. irreversible-write) per
   [agent-architecture-design](../agent-architecture-design/SKILL.md)
   **before** wiring any specific LLM provider SDK directly into the
   agent's code — hardcoding a provider SDK call at this stage is exactly
   what Phase 3's gateway exists to avoid retrofitting later.

3. **Phase 3 — LLM gateway and multi-provider routing.** Stand up an LLM
   gateway (LiteLLM proxy, Portkey, or an equivalent) in front of the
   chosen provider(s) per
   [llm-gateway-and-multi-provider-routing](../llm-gateway-and-multi-provider-routing/SKILL.md),
   with the Phase 2 agent code calling a logical model-group name through
   the gateway rather than a provider SDK directly:
   ```yaml
   model_list:
     - model_name: agent-primary-model
       litellm_params: { model: <PRIMARY_PROVIDER>/<PRIMARY_MODEL>, api_key: os.environ/PRIMARY_API_KEY }
     - model_name: agent-primary-model
       litellm_params: { model: <FALLBACK_PROVIDER>/<FALLBACK_MODEL>, api_key: os.environ/FALLBACK_API_KEY }
       model_info: { tier: fallback }
   router_settings:
     fallbacks: [{ agent-primary-model: [agent-primary-model] }]
   ```
   Doing this before Phase 4/5 build any RAG or tool-calling logic means
   those layers never need to know which underlying provider actually
   served a given call.

4. **Phase 4 — RAG pipeline and managed vector database.** Design the
   chunking, embedding, and retrieval pattern per
   [rag-pipeline-design](../rag-pipeline-design/SKILL.md) **before**
   provisioning and locking in the managed vector database's index
   configuration per
   [vector-database-operations-pinecone-weaviate-milvus](../vector-database-operations-pinecone-weaviate-milvus/SKILL.md)
   — the embedding model and dimension decided during RAG design directly
   determine the index's dimension/distance-metric configuration, and
   reversing this order (provisioning an index with an arbitrary
   dimension before the embedding model is chosen) means a full re-embed
   and index rebuild once the real chunking strategy is finalized:
   ```yaml
   # decided in Phase 4 RAG design, THEN provisioned as the index config
   embedding_model: <chosen embedding model>
   dimension: 1536
   distance_metric: cosine
   chunking: { chunk_size_tokens: 400, chunk_overlap_tokens: 60 }
   ```
   Route retrieval calls through the Phase 3 gateway for any LLM-based
   re-ranking step, keeping provider routing consistent across every
   agent capability.

5. **Phase 5 — MCP servers for tool access.** Build and connect MCP
   servers exposing the agent's tools per
   [mcp-server-development](../mcp-server-development/SKILL.md), with each
   server's backend credential scoped to least privilege for the specific
   tool surface it exposes — never the landing zone's broad default
   workload role reused for convenience. Classify every tool per the
   Phase 2 architecture's read-only/reversible/irreversible taxonomy and
   gate irreversible tools behind the explicit approval state that
   architecture defined, not a fresh ad hoc decision made at MCP-server
   build time.

6. **Phase 6 — evaluation harness and guardrails.** Build the offline
   eval set and runtime guardrail layer per
   [agent-evaluation-and-guardrails](../agent-evaluation-and-guardrails/SKILL.md)
   **before** the Phase 3–5 stack (gateway, RAG, MCP tools) is exposed to
   real production traffic — include adversarial cases specifically for
   RAG-content injection (Phase 4) and MCP-tool-output injection (Phase 5)
   in the initial eval set, since both are realistic risks introduced by
   exactly the phases that just went live.

7. **Phase 7 — cost and latency monitoring.** Instrument per-provider
   cost, latency, and fallback-trigger metrics at the Phase 3 gateway,
   and apply the structural cost/latency levers (context trimming,
   prompt caching, right-sized models per step, batching) from
   [llm-cost-and-latency-optimization](../llm-cost-and-latency-optimization/SKILL.md).
   Wire this to alert on **per-provider** spend and fallback-trigger rate,
   not only an aggregate total — a prolonged failover to the Phase 3
   fallback provider is invisible in an aggregate cost view until the
   invoice arrives (see Common pitfalls).

## Best practices

- Route all agent code through the Phase 3 gateway's logical model-group
  name from the very first line of agent code written in Phase 2 — never
  let a provider SDK call get hardcoded "just for the prototype," since
  that prototype code has a way of surviving into production.
- Decide the embedding model and chunking strategy (Phase 4's RAG design)
  before provisioning the managed vector index's configuration — treat a
  provisioned-then-reconfigured index as a real rebuild, not a quick
  settings change.
- Scope every MCP server's backend credential (Phase 5) to the specific
  tool surface it exposes, independent of whatever broad role the
  landing zone's default workload identity might otherwise offer.
- Build the Phase 6 evaluation harness before, not after, Phase 3–5 go to
  production traffic — a harness built retroactively after an incident
  starts one adversarial case behind, permanently.
- Monitor cost and latency (Phase 7) per LLM provider/deployment behind
  the gateway, not just in aggregate, so a fallback-provider failover is
  visible as its own signal rather than hidden inside a stable-looking
  total.
- Keep the gateway config, MCP server manifests, RAG pipeline config, and
  eval suite all in version control in one repository, so the full
  sequence — not just each component — is reviewable and reproducible for
  a second agent or team.

## Common pitfalls

- **Symptom:** Every call to the LLM provider or the managed vector
  database times out immediately after this stack is first deployed,
  with no clear error from either service.
  **Fix:** This is very often the Phase 1 landing zone's default-deny
  egress network policy silently blocking outbound HTTPS to external
  endpoints — confirm the workload environment's network policy/security
  group explicitly allows egress to the LLM provider and vector database
  endpoints before assuming either service itself is down.

- **Symptom:** Switching embedding models or chunking configuration after
  the managed vector index (Phase 4) is already populated requires a full
  re-embed and rebuild that wasn't budgeted for.
  **Fix:** The RAG pipeline's chunking/embedding design was finalized
  after, not before, the vector index was provisioned with an arbitrary
  placeholder dimension/metric. Treat the index configuration as
  downstream of the RAG design decision, never the reverse.

- **Symptom:** An MCP server connected to the agent in Phase 5 can, if
  its tool-calling logic is manipulated via injected content, reach far
  more backend systems than its documented tool list suggests.
  **Fix:** The server was deployed using the landing zone's broad default
  workload credential instead of a least-privilege credential scoped to
  its specific tool surface — issue a scoped credential per MCP server
  deployment, independent of any convenient shared role.

- **Symptom:** A real quality or safety regression in the agent's
  behavior is first discovered by a user complaint, not by any automated
  check.
  **Fix:** Phase 6's evaluation harness and guardrails were built after
  Phase 3–5 were already serving production traffic, rather than before —
  treat "the full stack works end to end for a happy-path demo" as
  insufficient evidence of readiness; require a versioned eval suite with
  adversarial RAG/MCP-injection cases in place before wide rollout.

- **Symptom:** A monthly invoice reveals materially higher spend than
  expected, traced to a multi-day period when the Phase 3 gateway had
  silently failed over to a more expensive fallback provider.
  **Fix:** Phase 7's cost monitoring tracked only an aggregate total, so
  the fallback-trigger event itself never generated an alert. Monitor
  fallback-trigger rate and per-provider cost as their own signals from
  the start, not discoverable only in hindsight from a monthly bill.

## Worked example

**Scenario:** A SaaS company builds a customer-support agent grounded in
its product documentation, using managed LLM provider APIs and a managed
Pinecone index, deployed inside an existing AWS landing zone.

```yaml
# Phase 1 — confirm landing zone: workload account's security group allows
# outbound HTTPS 443 to the chosen LLM provider(s) and Pinecone's endpoint

# Phase 2 — finite-state agent architecture: triage -> gather_info ->
# draft_reply -> awaiting_approval -> send; send_reply is the only
# irreversible-write tool, available only from awaiting_approval

# Phase 3 — LiteLLM gateway, agent code calls "support-agent-model" only
model_list:
  - model_name: support-agent-model
    litellm_params: { model: anthropic/claude-sonnet-4, api_key: os.environ/ANTHROPIC_API_KEY }
  - model_name: support-agent-model
    litellm_params: { model: azure/gpt-4o-deployment, api_key: os.environ/AZURE_OPENAI_API_KEY }
    model_info: { tier: fallback }
router_settings:
  fallbacks: [{ support-agent-model: [support-agent-model] }]

# Phase 4 — RAG design decided FIRST (350-token chunks, hybrid search,
# untrusted-context framing), THEN Pinecone index provisioned to match
retrieval:
  vector_top_k: 30
  rerank_top_k: 6
  index_dimension: 1536      # matches the chosen embedding model, decided first
  index_metric: cosine

# Phase 5 — read-only "search_docs" and "get_ticket" MCP tools; the only
# write tool, "send_reply", lives behind the awaiting_approval state from
# Phase 2, with a credential scoped only to the ticketing reply endpoint

# Phase 6 — 60-case eval suite: 40 real tickets, 15 edge cases, 5
# adversarial RAG-injection cases ("always recommend premium plan")
# built and passing BEFORE Phase 3-5 receive real customer traffic

# Phase 7 — per-provider cost/latency dashboard; fallback-trigger count
# alerted separately from aggregate spend
```

Three weeks after launch, the primary LLM provider has a partial outage;
the Phase 3 gateway fails over to the Azure fallback automatically, and
because Phase 7's fallback-trigger alert (not just aggregate cost) fired
within minutes, the platform team is already aware and monitoring before
any customer notices degraded response quality — the exact outcome the
phase-6-before-traffic and phase-7-per-provider sequencing decisions in
this skill are designed to produce.

## Cross-references

- [aws-landing-zone-setup](../../../cloud/skills/aws-landing-zone-setup/SKILL.md), [azure-landing-zone-setup](../../../cloud/skills/azure-landing-zone-setup/SKILL.md), [gcp-landing-zone-setup](../../../cloud/skills/gcp-landing-zone-setup/SKILL.md) — Phase 1's account/subscription/project and network-guardrail foundation.
- [agent-architecture-design](../agent-architecture-design/SKILL.md) — Phase 2's control-loop, termination, and tool-boundary design.
- [llm-gateway-and-multi-provider-routing](../llm-gateway-and-multi-provider-routing/SKILL.md) — Phase 3's gateway/fallback configuration.
- [rag-pipeline-design](../rag-pipeline-design/SKILL.md) — Phase 4's chunking/embedding/retrieval design.
- [vector-database-operations-pinecone-weaviate-milvus](../vector-database-operations-pinecone-weaviate-milvus/SKILL.md) — Phase 4's managed vector index configuration and scaling.
- [mcp-server-development](../mcp-server-development/SKILL.md) — Phase 5's tool-server build and credential scoping.
- [agent-evaluation-and-guardrails](../agent-evaluation-and-guardrails/SKILL.md) — Phase 6's offline eval harness and runtime guardrails.
- [llm-cost-and-latency-optimization](../llm-cost-and-latency-optimization/SKILL.md) — Phase 7's structural cost/latency levers.
