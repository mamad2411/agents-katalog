---
name: agent-friendly-api-documentation-2026
description: Write API documentation that AI agents can reliably retrieve, parse, and use to take the correct action — not just documentation humans can read. Covers the human-vs-agent documentation difference (tolerance for ambiguity), OpenAPI as the source of truth with behavior-defining descriptions, documenting workflows (not just endpoints), terminology consistency, writing descriptions that work for LLMs (intent + preconditions + boundaries), the llms.txt discovery/prioritization layer, serving Markdown and raw specs, and the 12-item agent-ready documentation checklist. Use when writing or refactoring API documentation for agentic consumption, evaluating whether existing docs are agent-compatible, or designing the documentation layer of an agent-experience strategy. NOT for API design/architecture (use agent-experience-design-2026), DevEx measurement (use devex-verification-bottleneck-framework), or marketing discoverability (use generative-engine-optimization-2026).
---

# Agent-Friendly API Documentation 2026

## The Core Shift

API documentation has always been the source of truth for developers integrating with a product. As AI agents become part of the development workflow, that source of truth now needs to serve a second reader: software that does not browse, infer, or troubleshoot the way a human does.

**Agent-friendly API documentation is documentation that a model or agent can reliably retrieve, parse, and use to take the right action.** That usually means pairing human-readable docs with machine-readable artifacts: OpenAPI specifications, JSON Schema, Markdown pages, tool definitions, workflow guidance, and emerging discovery files like `llms.txt`.

This matters because agents increasingly operate across real product workflows. A support agent handling a refund may need to authenticate, retrieve an order, check eligibility, and call a `createRefund` endpoint with the correct `orderId`, `reason`, and `amount`. If the docs do not clearly define the required fields, valid states, error responses, and sequencing rules, the agent may call the wrong endpoint, omit required data, or invent behavior the API does not support.

## When to Use

- Writing or refactoring API documentation for an API that AI agents will consume
- Evaluating whether existing documentation is agent-compatible
- Designing the documentation layer of an agent-experience (AX) strategy
- Adding `llms.txt` or machine-readable specs to a documentation site
- Writing OpenAPI descriptions that LLMs use to decide when and how to call tools
- Onboarding AI coding agents to an internal or external API surface

NOT for:
- API design and architecture (schema design, idempotency, batch/streaming surfaces) — use `agent-experience-design-2026`
- DevEx measurement for AI-assisted development — use `devex-verification-bottleneck-framework`
- Marketing/generative-engine optimization discoverability — use `generative-engine-optimization-2026`
- Pure human-facing documentation without agent consumption

## The Key Difference: Human-Focused vs. Agent-Focused Documentation

Human-focused documentation is optimized for **learning and exploration**. Agent-focused documentation is optimized for **retrieval and execution**. That does not mean stop writing for people — it means the docs need a clearer underlying contract so humans and agents can both understand how the API is supposed to behave.

| Area | Human-Focused | Agent-Focused |
|---|---|---|
| **Context** | Assumes readers infer missing details from experience | Makes assumptions, constraints, dependencies explicit |
| **Error handling** | Expects developers to debug interactively | Provides structured errors, causes, recovery steps |
| **Workflow** | Explains endpoints, often one page at a time | Defines ordered workflows across endpoints |
| **Terminology** | Uses natural variation to keep prose readable | Uses consistent names for the same concept everywhere |
| **Format** | Relies on visual pages, navigation, examples | Prioritizes OpenAPI, JSON Schema, Markdown, tool definitions, metadata |
| **Goal** | Help developers understand and integrate | Help humans and agents retrieve, plan, execute correctly |

**The biggest difference is tolerance for ambiguity.** A developer can usually infer that `is_active` is a boolean. An agent performs better when the schema explicitly defines the type, default behavior, valid transitions, and what the field controls. When those answers are missing, the model relies on probability instead of a contract.

Agent-focused documentation should answer seven questions for every endpoint:
1. What is this endpoint for?
2. When should it be called?
3. What must happen before it is called?
4. Which parameters are required?
5. What values are valid?
6. What errors can occur?
7. What should the agent do next?

## Step 1: Use OpenAPI as the Source of Truth

The OpenAPI Specification is one of the strongest foundations for documenting HTTP APIs because it describes paths, methods, authentication, parameters, request/response bodies, and errors in a standardized format. For agent-facing documentation, the OpenAPI spec should do more than list endpoints — it should define the **behavior** around those endpoints.

A useful agent-facing OpenAPI spec should include:
- Fully typed request and response bodies
- Required and optional fields
- Enum values and constraints
- Authentication requirements
- Status-specific error responses
- Preconditions for state-changing actions
- Idempotency and retry guidance where relevant

**Example — a refund endpoint that defines behavior, not just shape:**

```yaml
paths:
  /refunds:
    post:
      summary: Create a refund
      description: >
        Creates a refund for an order that has already been paid. Use this
        endpoint only after confirming that the order is eligible for a refund
        and that the requested amount does not exceed the captured payment.
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required: [orderId, reason, amount]
              properties:
                orderId:
                  type: string
                  description: Unique ID of the paid order to refund.
                reason:
                  type: string
                  enum: [duplicate, customer_request, fraudulent]
                  description: Business reason for the refund request.
                amount:
                  type: number
                  description: >
                    Refund amount in the order currency. Must not exceed
                    the captured payment amount.
      responses:
        "201":
          description: Refund created successfully.
        "409":
          description: Order is not eligible for a refund in its current state.
```

The schema defines the shape of the request; the descriptions explain the decision logic around it. Both humans and agents benefit.

## Step 2: Document Workflows, Not Just Endpoints

Agents often need to complete multi-step tasks. If docs only explain endpoints in isolation, the agent has to infer the workflow. Instead, provide explicit workflow pages for common tasks.

**Refund workflow example:**
```
1. Call GET /orders/{orderId}
2. Confirm status is paid or delivered
3. Confirm refundableAmount is greater than 0
4. Call POST /refunds with orderId, reason, and amount
5. If POST /refunds returns 409, tell the user the order is not eligible
6. If POST /refunds returns 201, return the refund ID and status
```

This is especially useful for MCP tools and agentic interfaces, where the agent has to choose which tool to call and in what order. It also makes documentation easier to evaluate because the expected behavior is explicit.

**The general workflow page pattern:**
```
1. Authenticate the request
2. Retrieve the relevant resource
3. Validate the resource state
4. Call the state-changing endpoint
5. Handle success or failure
6. Return the next best action to the user
```

## Step 3: Keep Terminology Consistent

Terminology drift is a common documentation problem. Humans can usually understand that "dashboard," "workspace," and "control panel" might refer to the same thing. Agents may treat them as separate concepts.

**Rules:**
- Use one canonical term for each resource and field
- If a field is `orderId` in your API, do not call it `order_id`, "order number," and "transaction ID" across different pages unless those are genuinely different concepts
- When synonyms are unavoidable, define them clearly

**A simple glossary helps:**
```
Order: A customer purchase record.
Payment: A money movement associated with an order.
Refund: A full or partial reversal of a captured payment.
Refundable amount: The remaining amount that can be refunded for an order.
```

Consistent language improves search, retrieval, and schema alignment. It also helps human developers move between guides, SDK docs, and API references without re-learning the same concept under different names.

## Step 4: Write Descriptions That Work for LLMs

LLMs use the natural-language `description` fields inside schemas (OpenAPI, JSON Schema, MCP tool definitions, SDK metadata) to decide when and how to call tools. **The description field is not decorative — it is part of the execution surface.**

A weak description tells the model what an endpoint does. A strong description tells the model when to use it, what must be true before use, and what the expected outcome is.

| Weak Description | Better Description |
|---|---|
| Creates a refund | Creates a refund for a paid order. Use only after confirming the order is eligible and the refund amount does not exceed the captured payment. |
| Deletes a user | Permanently deletes a user account after the user explicitly requests account closure or data removal. Do not use for temporary deactivation. |
| Updates status | Updates the order status. Valid transitions are pending to paid, paid to shipped, and shipped to delivered. |
| Gets customer data | Retrieves customer profile data by customer ID. Requires a valid access token with `customers:read` scope. |

**To make schema descriptions more useful for agents:**
- Be concise but explicit
- Describe intent, not just function
- Include preconditions and constraints
- Use consistent field and resource names
- Explain parameter relationships
- Document valid state transitions
- Include recovery guidance for expected errors

**Example:** Instead of "Deletes a user," write: "Permanently deletes a user account when the user explicitly requests account closure. Do not use this endpoint to suspend, deactivate, or hide a user."

That wording gives the agent a boundary. It reduces the chance the model will call a destructive endpoint for a related but incorrect task.

## Step 5: Add llms.txt as a Discovery and Prioritization Layer

The `llms.txt` proposal defines a Markdown file served from the root of a website, usually at `/llms.txt`, that points AI systems to the most important documentation on the site. It is best understood as a **discovery and prioritization layer**, not a replacement for OpenAPI, Markdown docs, or structured schemas.

**The distinction matters:**
- `robots.txt` tells crawlers what they may or may not access
- `sitemap.xml` lists URLs
- `llms.txt` helps LLMs find high-value, context-rich documentation without parsing full HTML pages, navigation menus, ads, or client-side rendering

**Example `llms.txt` file:**
```
# Example API docs

> Documentation for integrating with the Example payments API.

## Start here

- [Authentication](https://example.com/docs/auth): How to authenticate API requests
- [Refund workflow](https://example.com/docs/refunds): End-to-end refund flow and eligibility rules
- [OpenAPI spec](https://example.com/openapi.yaml): Machine-readable API contract
- [Error handling](https://example.com/docs/errors): Error codes, retry behavior, and recovery steps

## Agent guidance

- Use the OpenAPI spec as the source of truth for request and response schemas.
- Confirm resource state before calling state-changing endpoints.
- Do not call destructive endpoints unless the user explicitly requests the action.
```

**For agent-facing docs, `llms.txt` is useful because it can:**
- Point agents to canonical docs instead of outdated pages
- Highlight workflow guides, API specs, and error references
- Provide a lightweight map of the documentation structure
- Reduce noise from HTML, navigation, and duplicate pages
- Make documentation easier to retrieve in LLM-assisted development tools

`llms.txt` is still an emerging convention, not a formal web standard enforced across all AI providers. Treat it as a helpful addition to strong docs, not as the whole strategy.

**A-Tech caution (from `ai-license-circumvention-defense`):** Do NOT publish `llms.txt` for paid-tier or commercial-only documentation. Tailwind CSS's creator rejected `llms.txt` because "the docs are the only way people find out about our commercial products." Structure documentation so AI agents discover the open-source value while commercial offerings remain discoverable only through human journeys.

## Step 6: Serve Markdown and Raw Specs Where Possible

Many documentation sites are built for visual browsing. That is fine for humans, but it can make ingestion harder for agents if content depends heavily on JavaScript, tabs, hidden panels, or complex navigation.

Where possible, provide:
- Clean Markdown versions of important pages
- Raw machine-readable files for specs (raw `.yaml`, `.json`)
- `llms.txt` and `llms-full.txt` where documentation platforms support them
- Simplified content served to AI crawlers

**The goal is not to abandon the visual docs site.** The goal is to make sure the same information is available in formats that agents can retrieve and parse reliably.

## Examples in Practice (2026)

Several developer platforms already experiment with agent-facing documentation patterns:

| Platform | Pattern |
|---|---|
| **Cash App** | Exposes documentation indexes for AI agents via `/llms.txt` and `/llms-full.txt`; supports Markdown versions of pages |
| **Stripe** | AI integration docs include LLM-guidance for Stripe workflows and an installable MCP server |
| **Rightbrain** | Provides machine-readable documentation endpoints for agents, LLMs, and automated systems |
| **Fern** | Documentation platform that generates and maintains `llms.txt` and `llms-full.txt` |
| **n8n** | AI Agent node documentation explains how agents connect to tools and execute workflows |

The broader trend: **documentation is becoming part of the agent runtime.** Docs no longer only explain how a developer should use a product; they also shape how automated systems discover tools, choose actions, and recover from errors.

## The Agent-Ready Documentation Checklist

Before publishing or updating API docs for agent consumption, verify:

- [ ] Complete OpenAPI or equivalent machine-readable API contract
- [ ] Typed request and response bodies
- [ ] Required and optional fields
- [ ] Enum values, constraints, and defaults
- [ ] Authentication and authorization requirements
- [ ] Workflow guides for common multi-step tasks
- [ ] Preconditions for state-changing endpoints
- [ ] Structured error responses and recovery guidance
- [ ] Consistent terminology across docs, schemas, and SDKs
- [ ] Markdown or raw-text versions of important pages
- [ ] A maintained `llms.txt` or equivalent documentation index
- [ ] Versioning and freshness signals for agent-facing resources

You do not need to solve every item at once. **The highest-impact improvements are usually the ones that reduce ambiguity around workflows, destructive actions, and required fields.**

## The Core Principle

Writing documentation for AI agents is not about replacing human-readable docs. It is about making existing documentation more explicit, structured, and executable.

- Human developers still need explanations, examples, and conceptual guidance
- Agents need schemas, constraints, workflows, and clear instructions about when to use each tool
- The best documentation strategy supports both

**Start with the API contract.** Make OpenAPI/JSON Schema definitions complete, add intent-rich descriptions, document multi-step workflows, and publish clean Markdown or `llms.txt` indexes so agents can find the right context. Keep agent-facing resources versioned and current.

**If an agent cannot understand your docs, it cannot reliably use your product.** As more development workflows move through AI assistants, documentation quality becomes part of API usability, product discoverability, and operational safety.

## A-Tech Application Matrix

### A-Coder
- **Every A-Coder extension includes `llms.txt`** describing commands, keybindings, and API surface — so AI agents can self-onboard to A-Coder's capabilities (already a principle in `agent-experience-design-2026`; this skill provides the writing craft to execute it)
- **Workflow documentation for agent consumers:** A-Coder's MCP tool definitions include explicit workflow pages (initialize context → generate → review → apply patch) so consuming agents call tools in the correct order
- **Intent-rich descriptions:** every tool's `description` field includes preconditions, valid states, and recovery guidance — reducing the chance an agent invokes a destructive action incorrectly

### Be Practical
- **Curriculum module:** "Writing agent-friendly API documentation." The seven questions, the workflow-page pattern, the intent-vs-function description technique, the `llms.txt` discovery layer, the 12-item checklist.
- **Exercise:** Take an existing API's documentation. Audit it against the 12-item checklist. Rewrite three endpoint descriptions using the intent+precondition+boundary pattern. Add an `llms.txt` file. Document one multi-step workflow explicitly.
- **Frameworks taught:** human-vs-agent documentation difference, OpenAPI-as-source-of-truth, workflow documentation, terminology consistency, intent-rich descriptions, `llms.txt` as discovery layer, Markdown/raw-spec serving.

### Builder's Club
- **Open-source documentation templates:** Reference `llms.txt`, workflow-page, and intent-rich OpenAPI description templates that community members can adopt for their own APIs.
- **Agent-readiness audit service:** A community checklist/tool that evaluates whether an API's documentation is agent-compatible (runs the 12-item checklist as an automated audit).
- **Documentation-as-runtime:** Position A-Tech's documentation practice as "docs are part of the agent runtime" — a differentiator for community members building agent-consumable APIs.

## Cross-References

- **`agent-experience-design-2026`** — the six AX design principles (schema-first, idempotency, machine-readable context, batch/streaming, reversible actions, negotiation protocols). This skill provides the *documentation writing craft* that executes the Documentation and Discovery principles.
- **`devex-verification-bottleneck-framework`** — the 3 D's of agent-friendly APIs (Design/Documentation/Discovery) as part of the DevEx verification framework. This skill operationalizes the Documentation and Discovery D's.
- **`generative-engine-optimization-2026`** — `llms.txt` for AI search/marketing discoverability. This skill covers `llms.txt` for *API documentation* discovery; that skill covers `llms.txt` for *brand/content* discoverability.
- **`ai-license-circumvention-defense`** — the Tailwind CSS `llms.txt` rejection case. This skill's `llms.txt` guidance respects that boundary: publish `llms.txt` for open-source docs, not for paid-tier/commercial-only documentation.
- **`spec-driven-development-framework`** — machine-readable intent for agents. This skill's workflow documentation complements spec-driven intent by documenting the API consumption side.
- **`mcp-server-monetization-2026`** — MCP tool definitions as agent-consumable documentation. This skill's intent-rich description pattern applies to MCP tool `description` fields.
- **`spec-driven-cognitive-partnership`** — spec-driven development. This skill provides the documentation surface that specs generate.

## Key Takeaways

1. **Two readers, one contract:** documentation must serve humans (learning/exploration) and agents (retrieval/execution). The shared foundation is an explicit, unambiguous contract.
2. **OpenAPI is the source of truth** — but it must define behavior (preconditions, valid transitions, recovery), not just shape.
3. **Document workflows, not just endpoints** — agents complete multi-step tasks; isolated endpoint docs force them to guess sequencing.
4. **Terminology consistency is non-negotiable** — synonyms that humans resolve effortlessly become separate concepts to agents.
5. **The `description` field is execution surface** — intent + preconditions + boundaries, not "what it does."
6. **`llms.txt` is a discovery layer, not a replacement** — it points agents to canonical docs; it does not substitute for OpenAPI or structured schemas. Respect the paid-tier boundary.
7. **Serve Markdown and raw specs** — visual docs sites are for humans; agents need parseable formats.
8. **Documentation is becoming part of the agent runtime** — it shapes how automated systems discover tools, choose actions, and recover from errors.