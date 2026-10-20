---
alwaysApply: true
description: Vision, principles, and guardrails for ElizaOS logistics agents across creation, management, and maintenance
---

## ElizaOS Logistics Agent Vision & Guardrails

**North Star**: AI agents that reduce cycle time and cost per shipment while boosting OTIF (On‑Time In‑Full) across inbound, outbound, and returns.

### Key Outcomes
- **Faster quoting and booking**: Minimize back‑and‑forths; maximize first‑pass success.
- **End‑to‑end visibility**: Proactive exception detection and handling.
- **Reduced manual touches**: Automate document creation, validation, and filing.
- **Accurate landed cost & emissions**: Provide pre‑shipment estimates and post‑shipment actuals.

### Current Agent
- The `rate-quoter` agent is configured in [rate-quoter.json](mdc:rate-quoter.json) and uses SQL, Bootstrap, and Ollama plugins.

### Development Focus
- **Modular agent architecture** with clear separation of concerns.
- **Auditability**: Durable and queryable trails for every critical action.
- **Compliance-first**: GDPR, security, and data minimization by default.
- **Workflow automation**: Reduce or remove manual interventions safely.

---

## Architecture Principles

- **Single‑purpose agents**: Prefer small, composable agents per job (e.g., rate‑quoter, booking, documentation, tracking, exception‑manager, returns‑processor). Use an orchestrator/router when end‑to‑end flows need coordination.
- **Declarative configuration**: Define agent behavior in JSON/TOML configs stored at the repo root or under `agents/`. Follow the pattern of [rate-quoter.json](mdc:rate-quoter.json).
- **Stable interfaces**: Agents interact via typed messages and well‑defined tool schemas.
- **Deterministic tool calls**: Tool inputs and outputs must be schema‑validated and logged.
- **Model‑agnostic**: Default to local (Ollama) first; allow remote model fallbacks with safe degradation.
- **Idempotency & replayability**: Every external action must be idempotent or guarded by a deduplication strategy with durable correlation IDs.

Key code entry points to be aware of:
- [src/index.ts](mdc:src/index.ts)
- [src/plugin.ts](mdc:src/plugin.ts)
- [src/character.ts](mdc:src/character.ts)
- Frontend demo surface: [src/frontend/index.tsx](mdc:src/frontend/index.tsx)

---

## Agent Config Schema (guideline)

Configs should be human‑reviewable and machine‑validated. A minimal shape:

```json
{
  "name": "rate-quoter",
  "purpose": "Generate competitive rate quotes with rationale, SLAs, and emissions",
  "inputs": { "shipment": {"origin": "string", "destination": "string", "dims": "object"} },
  "outputs": { "quotes": "Quote[]", "explanations": "string" },
  "models": { "primary": "ollama:llama3.1", "fallbacks": ["gpt-4o-mini"] },
  "tools": ["sql", "http", "document"],
  "memory": { "policy": "stateless|short|long", "ttl": 86400 },
  "safety": { "pii": true, "rateLimits": {"rpm": 60} },
  "audit": { "level": "verbose", "redaction": "pii" },
  "metrics": ["cycle_time_ms", "first_pass_success", "touch_count" ]
}
```

- Validate configs at startup; reject on unknown keys or schema violations.
- Track config versions and migrations; store a `version` field and retain upgrade notes.

---

## Agent Lifecycle

1. **Creation**
   - Scaffold a new config file `<agent-name>.json` mirroring best‑practice fields above.
   - Register the agent in server exports and any routing tables if applicable.
   - Choose tools intentionally (SQL for rates, HTTP for carriers, document for PDF/EDI, etc.).

2. **Management**
   - Version configs and prompts; keep change logs with rationale and metrics deltas.
   - Gate config updates behind CI checks (schema validation, dry‑run simulations, tests).
   - Enforce rate limits and budget caps per agent and per environment.

3. **Maintenance**
   - Monitor drift: prompts, tools, carrier APIs, and data schemas.
   - Rotate secrets and keys; verify minimum necessary scopes.
   - Periodically re‑evaluate against golden datasets and real traffic samples.

---

## Observability, Audit, and Safety

- **Event log** every decision: prompts, tool calls, SQL queries, HTTP requests/responses (redacted), document reads/writes, and errors. Include correlation IDs and parent/child spans.
- **PII handling**: redaction at log‑write; store only hashes or masked values where possible. Classify common logistics PII (names, emails, phone, addresses, IDs).
- **Replay & forensics**: persist compact, redacted traces sufficient to reproduce a decision offline.
- **Guardrails**: schema validation, tool whitelists, output checking, monetary/time budgets, and escalation to human‑in‑the‑loop for high‑risk actions.

---

## Compliance (GDPR and beyond)

- **Data minimization**: only collect fields strictly required for the task.
- **Purpose limitation**: bind usage to the task and record purpose in audit.
- **Retention policy**: default short TTLs; configurable per environment and agent.
- **Access controls**: role‑based access to tools, data, and logs.
- **DSRs**: support data subject requests (access, deletion) via indexed, redactable logs and data stores.

---

## Testing and Evaluation

- **Unit and integration tests**: Cover tool schemas, SQL queries, and routing logic in `src/__tests__/`.
- **E2E scenarios**: Use Cypress tests under `src/__tests__/cypress/` for UI/agent workflows.
- **Golden sets**: Maintain representative shipments (sizes, modes, geos, incoterms) with expected outcomes (cycle time, landed cost, emissions, exceptions).
- **KPIs**: cycle time reduction, cost per shipment, OTIF, exception rate, first‑pass success, manual touches avoided.
- **Regression gates**: Any config/prompt change must not degrade protected KPIs beyond thresholds.

---

## Data, Tools, and Integrations

- **SQL**: Used for rates, lanes, historicals; must lint queries and parameterize inputs.
- **HTTP/Carrier APIs**: Wrap with client libraries that enforce idempotency, retries with backoff, and structured errors.
- **Document ops**: Parse/fill PDFs, EDI, commercial invoices, BOLs; extract fields with vision/OCR only when permitted.
- **Caching**: Memoize frequent lookups (e.g., surcharges, FX rates, emissions factors) with explicit TTLs.
- **Emissions & landed cost**: Centralize methodologies and data sources; version factors.

---

## Performance and Reliability

- **SLAs**: Set per agent (e.g., quote in < 3s). Use timeouts and fallbacks.
- **Rate limiting**: Global and per‑tool; shed load gracefully.
- **Retry & backoff**: Cap attempts; log final failures with context and notify orchestrator.
- **Idempotency keys**: For all external mutations (booking, doc issuance, updates).

---

## Frontend and UX

- Keep demos under `src/frontend/` using accessible, responsive components.
- Show audit context for each agent action and allow safe replays.
- Provide clear provenance for quotes (rates, surcharges, assumptions) and emissions.

---

## Documentation and CI/CD

- Update `README.md` when adding or changing agents, tools, or KPIs.
- Use pre‑commit checks for config schema validation and test runs (`scripts/test-all.sh`).
- Maintain a CHANGELOG per agent reflecting config/prompt/tool changes and KPI impact.

---

## Repository Conventions

- **Configs**: `<agent-name>.json` (e.g., [rate-quoter.json](mdc:rate-quoter.json)). Consider an `agents/` directory as the fleet grows.
- **Source**: Keep agent logic modular in `src/` and surface exports via [src/index.ts](mdc:src/index.ts).
- **Naming**: Descriptive, action‑oriented agent names (e.g., `exception-manager`, `returns-processor`).

---

## Extensibility and Roadmap Hints

- New agents to consider: booking, documentation, exception‑manager, tracking, returns‑processor, procurement optimizer.
- Add a router/orchestrator with policy‑driven routing across agents.
- Expand model coverage (multimodal vision for document extraction; small models on edge for low‑latency checks).
- Introduce an agent registry and health dashboard.

---

By following this rule, all contributors and tools (Cursor and GPT‑5) should align on vision, constraints, and high‑leverage practices while building and evolving ElizaOS logistics agents.

