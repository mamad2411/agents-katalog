---
name: mcp-tool-definition
description: best practices for defining MCP tools using JSON schemas. Use this to design robust `inputSchema`, `outputSchema`, and `annotations` that guide the model effectively.
---

# MCP Tool Definition Standards

## Goal
Design "Model-Ready" tools that self-document their purpose, validation logic, and side effects, enabling agents to use them autonomously and correctly.

## The Tool Schema
Every tool must adhere to a strict JSON structure. While `inputSchema` is required, best practice dictates including `outputSchema` and `annotations` for robustness.

```json
{
  "name": "create_ticket",
  "description": "Creates a new support ticket in the Jira system. Use this when a user reports a bug or feature request.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "title": { "type": "string", "description": "Concise summary of the issue" },
      "priority": { "type": "string", "enum": ["low", "high"], "description": "Severity level" }
    },
    "required": ["title", "priority"]
  },
  "outputSchema": {
    "type": "object",
    "properties": {
      "ticket_id": { "type": "string" },
      "status": { "type": "string" }
    }
  },
  "annotations": {
    "destructiveHint": true
  }
}
