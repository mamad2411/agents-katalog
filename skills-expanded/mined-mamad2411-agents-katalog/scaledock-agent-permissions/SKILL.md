---
name: scaledock-agent-permissions
description: Give AI agents least-privilege, auditable access in a ScaleDock product using A2A, MCP, WebMCP, AG-UI, A2UI, AP2, x402, UCP, ACP, Web Bot Auth and the OWASP Top 10 for Agentic and LLM Applications, with PermDock deciding every tool call, delegation and human approval, and OpenTelemetry GenAI, OCSF, EU AI Act and NIST AI RMF record-keeping for the audit trail. Use when an agent calls your tools, when you publish an Agent Card, register WebMCP tools, stream approvals or agent-generated UI to a user, let agents pay or check out, verify bot traffic, publish AI usage preferences or Content Credentials, or threat-model and review agent security.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.2.0"
---

# ScaleDock agent permissions

Agents act for users, so every agent surface needs to know who the user is, which agent is acting, what the user delegated, and when a human must confirm. This skill wires the agent protocols into a ScaleDock product with PermDock deciding each step, and keeps an audit trail that answers "who did what, on whose behalf". The spec skills carry the rules of each protocol.

**Follow the workflow below step by step.** Only wire the surfaces the product has; each step names the input that switches it on.

## Inputs (fill in, or ask before starting)

- Agent runtimes: AI SDK, Claude Agent SDK, OpenAI Agents SDK, Eve, MCP (then also `scaledock-mcp-server`).
- Agent-facing surfaces: A2A agent (yes or no), WebMCP tools in the web app (yes or no), AG-UI chat UI (yes or no), agent-generated UI with A2UI or MCP Apps (yes or no), agent payments with AP2 or x402 (yes or no), agent checkout with UCP or ACP (yes or no), bot traffic over plain HTTP (Web Bot Auth, yes or no), crawler and AI-use rules for the site's content (yes or no), generated media that needs Content Credentials (yes or no).
- Delegation: what the user hands the agent (scopes, `authorization_details`) and for how long.
- Approval store and approvers: who may confirm destructive or money-moving actions, and whether they confirm on a separate device (CIBA).
- Audit and risk: where decision events go (OpenTelemetry, a SIEM in OCSF, both), whether the EU AI Act applies, and whether the product runs an AI risk program (NIST AI RMF).

## Skills to install

```bash
npx skills add ScaleDockHQ/scaledock-skills --skill owasp-agentic --skill opentelemetry-genai
npx skills add ScaleDockHQ/scaledock-skills --skill a2a --skill webmcp --skill ag-ui --skill ap2 --skill web-bot-auth   # the surfaces you selected
npx skills add ScaleDockHQ/scaledock-skills --skill ocsf --skill eu-ai-act --skill openfeature --skill cedar             # when they apply
npx skills add ScaleDockHQ/scaledock-skills --skill privacy-pass --skill webdriver --skill prompt-api
npx skills add ScaleDockHQ/PermDock
```

Optional installs, per surface (`npx skills add ScaleDockHQ/scaledock-skills --skill <name>`):

- **MCP:** `mcp` (base protocol for MCP servers and clients) and `mcp-apps` (interactive `ui://` views on tools), with `scaledock-mcp-server`.
- **Agent UI:** `a2ui` (declarative agent-generated UI drawn from a trusted component catalog), next to `ag-ui`.
- **Payments and checkout:** `x402` (HTTP 402 payments), `ucp` (Universal Commerce Protocol) and `agentic-commerce-protocol` (ACP agent checkout with delegated payment tokens), next to `ap2`.
- **Approvals:** `ciba` (the approver confirms on a separate authentication device).
- **Bot traffic and content:** `robots-txt` (crawler rules), `aipref` (Content-Usage preferences for AI training and use) and `c2pa` (Content Credentials on media agents generate), next to `web-bot-auth`.
- **Threat model and governance:** `owasp-llm` (LLM application risks), `mitre-atlas` (AI threat tactics and techniques) and `nist-ai-rmf` (AI risk program), next to `owasp-agentic` and `eu-ai-act`.

## Invariants

1. **The spec skills win on protocol details.** Agent Cards follow `a2a`; MCP messages follow `mcp`; page tools follow `webmcp`; UI events follow `ag-ui`; generated UI follows `a2ui` or `mcp-apps`; mandates follow `ap2`; payments and checkouts follow `x402`, `ucp` and `agentic-commerce-protocol`; request signatures follow `web-bot-auth`; span names follow `opentelemetry-genai`.
2. **Principal and actor are separate.** The user is the principal, the agent is the actor. Both come from verified transport auth or the host session, never from a task body, tool argument or model output.
3. **Delegation is explicit.** An agent gets only what the user delegated, intersected with what the user may do. An actor with no delegation is denied everything.
4. **Destructive and money-moving actions wait for a human.** Grants on delete, publish, pay, approve, refund and access changes carry `approval`, the requester cannot approve their own request, and AP2 mandates, x402 payment payloads and UCP or ACP payment tokens never replace that approval.
5. **Every decision is recorded.** Each tool call produces a decision event with principal, actor, permission, outcome and reason, nested under the GenAI `execute_tool` span.
6. **Flags select, they never grant.** OpenFeature may pick which declared role or plan applies; a flag never turns a denial into a grant.
7. **One policy language in the app.** PermDock policies are the source of truth. Cedar sits next to them only where an external gateway already evaluates Cedar; both use deny-overrides-permit, so keep the two in step rather than translating one into the other.

## Workflow

1. **Set the inputs and threat-model.** Walk the `owasp-agentic` checklist for each selected surface, focusing on tool misuse and identity and privilege abuse. Add `owasp-llm` for the model-facing risks (prompt injection, output handling) and tag threats with `mitre-atlas` techniques when the product keeps a threat model.
   ✓ Every surface has a named principal source, actor source and delegation.
2. **Tool calls.** For each runtime, use the matching PermDock adapter (`permdock/ai-sdk`, `permdock/claude-agent`, `permdock/openai`, `permdock/eve`, `permdock/mcp`) with `subject`, `actor`, `delegation` and one permission per tool. Follow `wire-permdock`.
   -> [`references/stack.md`](references/stack.md)
   ✓ A tool the user has not delegated is denied, and a destructive tool returns `approval-required`.
3. **Agent-facing surfaces.** A2A: generate the Agent Card and extended card with `permdock/a2a` and protect each skill. WebMCP: register only snapshot-allowed tools with `permdock/webmcp`. AG-UI: surface `approval-required` as the protocol's human-in-the-loop events. A2UI or MCP Apps: render only catalog components or `ui://` views, and send every action they trigger through the same PermDock decision. AP2, x402, UCP and ACP: treat mandates, payment payloads and checkout tokens as evidence attached to an approval, not as the approval. Web Bot Auth: enable `webBotAuth` on the HTTP adapter so a verified signer becomes the actor. Content: publish `robots-txt` rules and `aipref` Content-Usage statements for crawlers, and attach `c2pa` Content Credentials to media agents generate.
   ✓ Each selected surface passes its spec skill's Verify list.
4. **Approvals.** Mount `approvalsHandler` from `permdock/approvals` with a durable store, pass the store to every adapter, and resume with the `PermDock-Approval` header. When the approver confirms on a separate device, run that confirmation as `ciba` describes and attach the result to the approval.
   ✓ An approval resumes only the exact call it was issued for, by a distinct approver.
5. **Audit trail.** Instrument with `instrument` from `permdock/otel` so decisions nest under `execute_tool` spans; export decision events as OCSF when a SIEM needs them. If the EU AI Act applies, map the logging and human-oversight obligations in `eu-ai-act` to these events; with an AI risk program, map them to the `nist-ai-rmf` subcategories they evidence.
   ✓ For any tool call you can answer who asked, which agent acted, what was decided and who approved.
6. **Test and audit.** Add scenario tests for delegation, denial and approval with `permdock/testing`, then run `audit-permissions` from `ScaleDockHQ/PermDock` (it reports OWASP ASI02 and ASI03 per adapter).
   ✓ Tests pass and the audit has no blocker.

## Verify before done

- [ ] No agent surface reads a subject, tenant or actor from model-controlled input.
- [ ] Every agent adapter sets `delegation`, and it lists scopes, not the principal's whole role.
- [ ] Every destructive or money-moving tool returns `approval-required`, and self-approval is refused.
- [ ] Every selected spec skill's Verify list passes.
- [ ] Decision events carry principal, actor, permission, outcome and reason, and `pnpm verify` passes.

## Reference index

- **[`references/stack.md`](references/stack.md)**: each spec mapped to the PermDock adapter and the audit trail.
