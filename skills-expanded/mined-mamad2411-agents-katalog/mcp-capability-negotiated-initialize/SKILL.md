---
name: mcp-capability-negotiated-initialize
description: In MCP `initialize`, advertise optional server capabilities (prompts, resources, sampling) only when the client declared matching support — avoids clients rejecting the handshake or spamming unsupported methods.
category: backend
tags: [mcp, json-rpc, capability-negotiation, handshake]
triggers:
  - "mcp initialize"
  - "capability negotiation"
  - "server capabilities"
  - "prompts/resources not showing"
source_project: yamltomcp
version: 0.1.0-draft
---
