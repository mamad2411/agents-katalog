---
description: AgentTrip product and talk constraints
alwaysApply: true
---

# AgentTrip

This is a conference-demo app for Agentic UI, not a production travel product.

- Never let the AI generate React, HTML, CSS, or executable code.
- The agent may only select from the component registry and pass typed props.
- Prefer mock tools with realistic latency over live travel APIs.
- Booking/finalizing a plan always requires explicit user approval.
- Keep travel-domain components separate from agent infrastructure.
- Visual components receive props and render. They do not call tools or own agent state.
- The product is a generic travel agent. Destination-specific copy belongs in demo data and scripts, not in chrome or presentational components.
- Preserve a deterministic demo path that works without an LLM. The live talk prompt is “Plan the Spiti trip”.
- Live mode uses the Vercel AI SDK. Do not use streamUI or let the model generate markup.
