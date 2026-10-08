---
name: treeseed
description: Operate a TreeSeed control plane through its current MCP capabilities for project, knowledge, governance, and execution work. Use when a task targets TreeSeed records or governed project-agent chat; do not use it as authority to run agents or mutate repositories.
metadata:
  protocol: "2026-07-28"
  catalog-receipt: "catalog-receipt.json"
  categories: "knowledge,governance,projects,execution,mcp"
---

# TreeSeed

Treat the connected TreeSeed server as the authority for identity, access, governance, scheduling, and receipts. Discover its current MCP tools, resources, templates, prompts, schemas, and capability annotations before choosing an operation. Do not rely on a remembered tool list or construct REST paths.

## Operating boundary

- Act as the authenticated external principal. Do not claim project-agent identity unless an explicit, authorized project-agent chat operation returns that delegation.
- Read current state before a consequential mutation. Follow returned blockers, concurrency tokens, confirmation requests, resource links, and next actions.
- Use server-provided structured input and output schemas. Never place credentials, session material, private keys, or bearer tokens in tool arguments or model-visible content.
- Treat `input_required` as a signed, exact-argument confirmation checkpoint. Ask the human when required; never alter, reuse, or synthesize confirmation state.
- Follow durable `treeseed://` resource links for asynchronous work. Use progress, cancellation, completion, and subscriptions when advertised instead of polling invented endpoints.
- Do not invoke or emulate `save`, `stage`, or `release` until the server advertises their accepted governed operations.
- For repository-backed project knowledge, use the `trsd library` workflow in `references/knowledge.md`; never assume an unbound virtual repository or a `src/content` library root.

## Choose the relevant guidance

- For questions, research, knowledge, or TreeDX projections, read [references/knowledge.md](references/knowledge.md).
- For proposals, decisions, estimates, reviews, or discussions, read [references/governance.md](references/governance.md).
- For teams, projects, repositories, or provider bindings, read [references/projects.md](references/projects.md).
- For agents, providers, capacity, plans, workdays, assignments, or explicit project-agent chat, read [references/execution.md](references/execution.md).
- For connection discovery, protocol behavior, errors, subscriptions, or confirmations, read [references/mcp.md](references/mcp.md).

## Distribution

Install and update the project-scoped skill with the pinned Vercel Labs Skills CLI version recorded by the consuming project:

```text
npx skills@1.5.23 add treeseed-ai/skill --skill treeseed --agent codex --yes
npx skills@1.5.23 update treeseed --project --yes
```

The receipt pins published SDK and API evidence for this copy. Runtime discovery remains authoritative when a connected server advertises a newer compatible catalog. Installed files and `skills-lock.json` belong to the consuming project; this repository remains the source of releases.
