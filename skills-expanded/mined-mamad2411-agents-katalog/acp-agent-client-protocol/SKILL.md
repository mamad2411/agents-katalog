---
name: acp-agent-client-protocol
description: Applies the Agent Client Protocol (ACP) open standard for connecting external coding agents to IDEs. Use when building agent-IDE integrations, designing agent interoperability, or implementing bring-your-own-agent workflows.
---

# Agent Client Protocol (ACP)

## Overview

The Agent Client Protocol (ACP) is an open standard that decouples the IDE from the AI coding agent — the "LSP moment for AI agents." Just as the Language Server Protocol (LSP) standardized how editors communicate with language servers (enabling any editor to use any language server), ACP standardizes how IDEs communicate with AI coding agents (enabling any IDE to use any AI agent).

Before ACP, every AI coding agent (GitHub Copilot, Claude Code, Cursor, Codex, etc.) required its own proprietary IDE integration. Switching agents meant switching IDEs or installing vendor-specific plugins. ACP breaks this coupling: the IDE speaks ACP, the agent speaks ACP, and any ACP-compatible agent works with any ACP-compatible IDE. This gives developers agent choice without IDE lock-in, preserves IDE-specific code intelligence, and enables team governance over which agents are approved.

## Key Framework & Principles

### Standardized Context Passing

ACP defines a bidirectional communication protocol between IDE and agent:

**IDE → Agent (context in):**
- **Files**: Current open files, file contents, file trees
- **Diffs**: Uncommitted changes, staged changes, recent commits
- **Terminal output**: Command results, error logs, build output
- **Selection**: Active editor selection, cursor position
- **Diagnostics**: LSP errors, warnings, lint results

**Agent → IDE (actions out):**
- **File edits**: Precise diffs to apply to files
- **Tool calls**: Structured requests to execute IDE-resident tools (search, refactor, run tests)
- **Shell commands**: Commands to execute in the project's terminal
- **Permission requests**: Human-in-the-loop approval for sensitive actions

This standardized context passing means agents get rich, structured project context without vendor-specific plugins, and IDEs receive structured actions they can review and apply safely.

### Curated Agent Registry + Custom Agents

- **Curated registry**: A maintained registry of ACP-compatible agents, similar to how LSP has a registry of language servers. Developers can browse and install agents directly.
- **Custom agents via `acp.json`**: Projects or teams can define custom agents via an `acp.json` configuration file, specifying agent endpoints, capabilities, and constraints. This enables organization-specific agents with internal knowledge.
- **Per-project configuration**: Different projects can use different agents, and the same project can use different agents for different tasks.

### BYOK and Infrastructure Control

- **Bring Your Own Keys (BYOK)**: Developers provide their own API keys for the underlying LLM provider. No mandatory subscription to any single agent vendor.
- **Provider-agnostic**: ACP agents can run on any backend — local models, cloud APIs, self-hosted inference, or hybrid. The protocol doesn't dictate the inference infrastructure.
- **Infrastructure control**: Teams can route agent requests through their own infrastructure for logging, compliance, cost management, or data residency requirements.

### Specialization

ACP embraces **agent specialization** — different agents for different tasks, all within the same IDE:

- **Frontend specialist**: An agent tuned for UI/component work
- **Refactoring agent**: An agent focused on code structure improvements
- **Debugging agent**: An agent optimized for tracing and fixing bugs
- **Documentation agent**: An agent that generates and updates docs
- **Custom domain agents**: Organization-specific agents with internal knowledge

Developers can switch between specialized agents contextually without leaving their IDE.

### Supported Agents

ACP-compatible agents include (non-exhaustive):
- GitHub Copilot
- Claude Code
- Cursor
- Codex
- Gemini CLI
- Junie
- OpenCode
- Cline

### JetBrains Implementation

JetBrains has implemented ACP across its IDE ecosystem:

- **ACP in WebStorm**: Full ACP support, allowing WebStorm users to connect any ACP-compatible agent.
- **Air (agentic development environment)**: JetBrains' agentic dev environment built around ACP, designed for multi-agent workflows.
- **Multi-agent concurrent execution**: Air supports running multiple agents simultaneously — e.g., a refactoring agent and a testing agent working in parallel on different parts of the codebase.

### Deep Agents + ACP Adapter (LangChain)

LangChain provides a **Deep Agents + ACP adapter** that bridges LangChain's agent framework to ACP:

- **`write_todos` planning tool**: Agents maintain a structured todo list, enabling transparent planning and progress tracking visible in the IDE.
- **Sub-agent spawning**: A primary agent can spawn specialized sub-agents for sub-tasks, all communicating via ACP.
- **Human-in-the-loop permission requests**: Agents request permission for sensitive actions (file deletions, shell commands with side effects), and the IDE surfaces these as approval prompts.
- **Session-scoped always-allow**: Users can grant always-allow permissions for specific actions within a session, reducing friction for trusted operations.

## Practical Application Guidance

### For IDE Developers

If you're building an IDE or editor extension:

1. **Implement the ACP client**: Handle the standardized context passing (files, diffs, terminal, diagnostics → agent) and action handling (edits, tool calls, shell commands ← agent).
2. **Expose an agent selection UI**: Let users browse the curated registry and configure custom agents via `acp.json`.
3. **Implement permission prompts**: Surface human-in-the-loop approval requests from agents.
4. **Support multi-agent execution**: Allow multiple agents to run concurrently where appropriate.

### For Agent Developers

If you're building an AI coding agent:

1. **Implement the ACP server**: Accept standardized context from IDEs and return structured actions.
2. **Register in the curated registry**: Make your agent discoverable.
3. **Support `acp.json` configuration**: Allow teams to configure your agent for their specific needs.
4. **Leverage BYOK**: Don't lock users into your API; let them bring their own provider keys.

### For Development Teams

1. **Define approved agents**: Specify which ACP agents are approved for use in your codebase via `acp.json`.
2. **Set up data compliance routing**: Route agent requests through approved infrastructure for logging and compliance.
3. **Create custom agents**: Build organization-specific agents with internal knowledge (codebase conventions, internal APIs, domain logic).
4. **Establish governance**: Define policies for which agents can access which repositories and what actions require human approval.

### Benefits Summary

- **Switch agents without switching IDEs**: Try new agents without abandoning your preferred IDE and its code intelligence.
- **Keep code intelligence**: Your IDE's indexing, refactoring, navigation, and debugging work alongside any agent.
- **No vendor lock-in**: BYOK, provider-agnostic, open standard.
- **Team governance**: Approved providers, data compliance routing, custom agents with internal knowledge.

## A-Tech Alignment

- **Open Source**: ACP is an open standard, directly analogous to LSP's open approach. The protocol specification, agent registry, and adapters (e.g., LangChain's Deep Agents adapter) are open.
- **Data Privacy**: ACP enables direct IDE-to-agent communication without forcing data through a vendor's cloud. Teams can route through their own infrastructure, maintain data residency, and audit data flows.
- **Financial Freedom**: BYOK means no mandatory subscriptions to any single agent vendor. Developers can use free local models, cheap API providers, or enterprise infrastructure — their choice.
- **Practical Implementation**: ACP has working integrations across major IDEs (JetBrains ecosystem) and agents (8+ named agents), a curated registry, and adapter libraries. This is a deployed, usable standard, not a proposal.

## Cross-References

- **open-source-funding-channels-2026**: Relevant for sustaining open-source ACP implementations, agent registry infrastructure, and adapter libraries.
- **genai-privacy-choice-ecosystems**: ACP's direct IDE-to-agent communication model aligns with data minimization principles — relevant when designing privacy for agent-IDE integrations.
- **ietf-federated-learning-agent-privacy**: When ACP agents are trained via federated learning, this skill's privacy architecture applies to the training pipeline.