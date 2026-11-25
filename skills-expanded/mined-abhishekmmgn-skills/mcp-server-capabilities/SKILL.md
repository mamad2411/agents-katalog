---
name: mcp-server-capabilities
description: extended MCP features beyond tools, including Resources (data access), Prompts (templates), and Sampling (server-initiated model calls). Use this to implement rich, two-way agent interactions.
---

# MCP Server Capabilities

## Goal
Leverage advanced MCP features to provide agents with direct data access, reusable prompt templates, and the ability to request completions or user input from the host.

## 1. Resources (Contextual Data)
* **Definition:** A server-side capability allowing the host application to read static data (logs, file contents, database records) directly.
* **Usage:** Use when the agent needs to "read" the state of the world rather than "act" on it.
* **Mechanism:**
    * **URI-Based:** Resources are identified by URIs (e.g., `file:///logs/error.txt`).
    * **Embedded vs. Linked:** Resources can be returned fully embedded in the tool result or as a link to be fetched separately.
* **Security Note:** Always validate resource URIs against an allowlist to prevent arbitrary file access.

## 2. Prompts (Reusable Templates)
* **Definition:** Pre-defined prompt templates stored on the server that clients can retrieve and use.
* **Usage:** Use to standardize how agents interact with your tools (e.g., a "Bug Report" prompt that pre-fills the necessary context for the `create_ticket` tool).
* **Risk:** High risk of prompt injection. Clients should treat server-provided prompts as untrusted user input.

## 3. Sampling (Server-Initiated Intelligence)
* **Definition:** A capability that allows the **Server** to ask the **Client** (Host) to run an LLM completion.
* **Workflow:**
    1.  Tool needs complex reasoning (e.g., summarizing a massive log file it just fetched).
    2.  Server sends a `sampling/createMessage` request to the Client.
    3.  Client runs the model (potentially with human approval) and returns the text.
* **Benefit:** Offloads compute costs to the client and keeps API keys secure on the client side.

## 4. Elicitation (User Input)
* **Definition:** A mechanism for the Server to ask the Client to prompt the human user for input.
* **Usage:** Use for disambiguation (e.g., "Which project did you mean?") or required parameters that are missing.
* **Privacy:** Servers MUST NOT use elicitation to request sensitive information (passwords, API keys).
