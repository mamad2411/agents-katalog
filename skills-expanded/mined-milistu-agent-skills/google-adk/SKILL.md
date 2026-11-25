---
name: google-adk
description: "ALWAYS use this skill for any question involving Google ADK (Agent Development Kit). This includes: building or configuring agents (LlmAgent, SequentialAgent, LoopAgent, ParallelAgent, custom BaseAgent), writing function tools or connecting MCP/OpenAPI tools, managing sessions/state/memory, multi-agent routing and pipelines, before/after callbacks, streaming with Gemini Live API (run_live, LiveRequestQueue), deploying to Cloud Run or Vertex AI Agent Engine, evaluating agent behavior, A2A protocol, context caching/compression, grounding with Google Search. Trigger on any mention of 'adk', 'google adk', 'agent development kit', 'LlmAgent', 'SequentialAgent', 'LoopAgent', 'AgentTool', 'tool_context', 'InMemorySessionService', 'VertexAiSessionService', or related ADK class/API names — even if the user doesn't call it ADK explicitly."
---

# Google ADK

Comprehensive reference for Google's Agent Development Kit. Use this skill when:
- Creating or configuring any ADK agent (`LlmAgent`, `SequentialAgent`, `LoopAgent`, `ParallelAgent`, custom agents)
- Wiring tools to agents (function tools, built-in tools, MCP, OpenAPI, tool authentication)
- Managing sessions, state, and memory
- Building multi-agent systems or agent pipelines
- Integrating the Gemini Live API or building streaming agents
- Deploying agents to Cloud Run, GKE, or Vertex AI Agent Engine
- Evaluating agent behavior or writing agent tests
- Using the A2A (Agent-to-Agent) protocol for inter-agent communication
- Configuring callbacks, grounding, context caching, or observability

## How to Use This Skill

1. Identify the task from the Quick Reference table below
2. Load the concept reference file (prose, architecture, API parameters)
3. If you need runnable code, also load the matching language sidecar: `filename-python.md`, `filename-typescript.md`, `filename-go.md`, or `filename-java.md`

**Language sidecar files exist for these 10 high-complexity references** — load them alongside the parent when you need code examples:

| Parent file | Python sidecar | TS sidecar | Go sidecar | Java sidecar |
|---|---|---|---|---|
| `agents/llm-agents.md` | `agents/llm-agents-python.md` | `agents/llm-agents-typescript.md` | `agents/llm-agents-go.md` | `agents/llm-agents-java.md` |
| `agents/custom-agents.md` | `agents/custom-agents-python.md` | `agents/custom-agents-typescript.md` | `agents/custom-agents-go.md` | `agents/custom-agents-java.md` |
| `agents/multi-agent-systems.md` | `agents/multi-agent-systems-python.md` | `agents/multi-agent-systems-typescript.md` | `agents/multi-agent-systems-go.md` | `agents/multi-agent-systems-java.md` |
| `tools/function-tools-overview.md` | `tools/function-tools-overview-python.md` | `tools/function-tools-overview-typescript.md` | `tools/function-tools-overview-go.md` | `tools/function-tools-overview-java.md` |
| `tools/mcp-tools.md` | `tools/mcp-tools-python.md` | `tools/mcp-tools-typescript.md` | `tools/mcp-tools-go.md` | `tools/mcp-tools-java.md` |
| `tools/tool-authentication.md` | `tools/tool-authentication-python.md` | `tools/tool-authentication-typescript.md`* | `tools/tool-authentication-go.md`* | `tools/tool-authentication-java.md`* |
| `callbacks/types-of-callbacks.md` | `callbacks/types-of-callbacks-python.md` | `callbacks/types-of-callbacks-typescript.md` | `callbacks/types-of-callbacks-go.md` | `callbacks/types-of-callbacks-java.md` |
| `sessions/state.md` | `sessions/state-python.md` | `sessions/state-typescript.md` | `sessions/state-go.md` | `sessions/state-java.md` |
| `sessions/memory.md` | `sessions/memory-python.md` | `sessions/memory-typescript.md`* | `sessions/memory-go.md` | `sessions/memory-java.md` |
| `streaming/part1-intro-to-streaming.md` | `streaming/part1-intro-to-streaming-python.md` | `streaming/part1-intro-to-streaming-typescript.md`* | `streaming/part1-intro-to-streaming-go.md`* | `streaming/part1-intro-to-streaming-java.md`* |

*\* = stub only, source docs have no examples for this language yet*

All sidecar files are under `reference/` — prepend `reference/` to the paths above.

---

## Quick Reference: Common Tasks

| Task | Load These References |
|---|---|
| Create a basic LLM agent | `reference/getting-started/python-quickstart.md` or `typescript-quickstart.md` / `go-quickstart.md` / `java-quickstart.md` |
| Understand LlmAgent parameters (name, model, tools, instructions, output_key) | `reference/agents/llm-agents.md` + language sidecar |
| Build a sequential pipeline of agents | `reference/agents/workflow/sequential-agents.md` |
| Build a loop / retry pattern | `reference/agents/workflow/loop-agents.md` |
| Run agents in parallel | `reference/agents/workflow/parallel-agents.md` |
| Build a multi-agent system with routing | `reference/agents/multi-agent-systems.md` + language sidecar |
| Create a custom agent (subclass BaseAgent) | `reference/agents/custom-agents.md` + language sidecar |
| Write a function tool with ADK patterns | `reference/tools/function-tools-overview.md` + language sidecar |
| Use LongRunningFunctionTool or AgentTool | `reference/tools/function-tools-overview.md` + language sidecar |
| Connect an MCP server as tools | `reference/tools/mcp-tools.md` + `reference/tools/mcp-tools-python.md` |
| Expose an OpenAPI spec as tools | `reference/tools/openapi-tools.md` |
| Add OAuth/API key auth to tools | `reference/tools/tool-authentication.md` + `reference/tools/tool-authentication-python.md` |
| Add human-in-the-loop confirmations | `reference/tools/action-confirmations.md` |
| See all built-in & third-party integrations | `reference/tools/tools-and-integrations.md` |
| Read/write session state, use state prefixes | `reference/sessions/state.md` + language sidecar |
| Use output_key to pass data between agents | `reference/sessions/state.md` + language sidecar |
| Use persistent sessions (DatabaseSessionService) | `reference/sessions/sessions.md` |
| Add long-term memory (MemoryService) | `reference/sessions/memory.md` + language sidecar |
| Add callbacks (before/after model/tool/agent) | `reference/callbacks/types-of-callbacks.md` + language sidecar |
| Callback patterns and best practices | `reference/callbacks/callback-patterns.md` |
| Configure models (Gemini, Claude, Vertex, Ollama, LiteLLM) | `reference/models/models-overview.md` |
| Use Claude (Anthropic) as the model | `reference/models/claude.md` |
| Use Vertex AI hosted models | `reference/models/vertex-ai.md` |
| Use Ollama / local models | `reference/models/ollama.md` |
| Build a streaming / realtime agent | `reference/streaming/streaming-overview.md` + `reference/streaming/part1-intro-to-streaming.md` + `reference/streaming/part1-intro-to-streaming-python.md` |
| Stream audio, images, or video | `reference/streaming/part5-audio-images-video.md` |
| Use Google Search grounding | `reference/grounding/google-search-grounding.md` |
| Use Vertex AI Search grounding | `reference/grounding/vertex-ai-search-grounding.md` |
| Work with artifacts (files, blobs) | `reference/components/artifacts.md` |
| Run the agent (CLI / web UI / API server) | `reference/runtime/runtime-overview.md` |
| Deploy to Cloud Run | `reference/deployment/cloud-run.md` |
| Deploy to Vertex AI Agent Engine | `reference/deployment/agent-engine.md` |
| Evaluate agent quality / write eval tests | `reference/evaluation/evaluation-overview.md` |
| Expose an agent via A2A protocol | `reference/a2a/quickstart-exposing-python.md` |
| Consume a remote agent via A2A | `reference/a2a/quickstart-consuming-python.md` |
| Enable tracing / logging / observability | `reference/observability/observability-overview.md` |
| Use context caching to reduce cost | `reference/context/context-caching.md` |
| Compress long context windows | `reference/context/context-compression.md` |
| CLI commands reference | `reference/reference/cli-reference.md` |

---

## 1. Getting Started

Start here when beginning a new ADK project or when you need installation, quickstart, or conceptual overview.

| Reference | When to Consult |
|---|---|
| `reference/home.md` | ADK high-level overview: what it is, key features, multi-language support |
| `reference/getting-started/technical-overview.md` | Architecture: agents, tools, sessions, events, runners — how they fit together |
| `reference/getting-started/advanced-setup.md` | Installation, virtual envs, CLI setup, API key config, optional dependencies |
| `reference/getting-started/python-quickstart.md` | First Python agent in 5 minutes |
| `reference/getting-started/typescript-quickstart.md` | First TypeScript agent in 5 minutes |
| `reference/getting-started/go-quickstart.md` | First Go agent in 5 minutes |
| `reference/getting-started/java-quickstart.md` | First Java agent in 5 minutes |
| `reference/getting-started/quickstart-multi-tool-agent.md` | Building an agent with multiple tools: weather + time + translation |
| `reference/getting-started/tutorial-agent-team.md` | Multi-agent tutorial: orchestrator + specialized sub-agents |
| `reference/getting-started/quickstart-streaming-python.md` | Getting started with streaming agents in Python |
| `reference/getting-started/quickstart-streaming-java.md` | Getting started with streaming agents in Java |
| `reference/getting-started/coding-with-ai.md` | Using AI assistants (Claude, Gemini, Cursor) to build ADK projects |

---

## 2. Agents

Core agent types and configuration. Almost every ADK task starts here.

| Reference | When to Consult |
|---|---|
| `reference/agents/agents-overview.md` | Overview of all agent types and when to use each |
| `reference/agents/llm-agents.md` | LlmAgent concepts: name, model, description, instructions, tools, output_key, planner, code_executor — load language sidecar for code |
| `reference/agents/workflow-agents.md` | Workflow agents overview: Sequential, Loop, Parallel — when and why |
| `reference/agents/workflow/sequential-agents.md` | SequentialAgent: chaining agents in order, passing context between steps |
| `reference/agents/workflow/loop-agents.md` | LoopAgent: iteration, stopping conditions, max_iterations |
| `reference/agents/workflow/parallel-agents.md` | ParallelAgent: concurrent execution, independent subtasks, fan-out patterns |
| `reference/agents/custom-agents.md` | BaseAgent subclassing: `_run_async_impl`, custom orchestration logic — load language sidecar for the StoryFlowAgent pattern |
| `reference/agents/multi-agent-systems.md` | Multi-agent coordination: sub_agents hierarchy, AgentTool, LLM transfer, shared state — load language sidecar for composition patterns |
| `reference/agents/agent-config.md` | Agent configuration file format (agentconfig.json) |

---

## 3. Models

Configuring which LLM backs your agent.

| Reference | When to Consult |
|---|---|
| `reference/models/models-overview.md` | All supported models, how to specify model strings, model selection guidance |
| `reference/models/gemini.md` | Google Gemini models (gemini-2.5-flash, gemini-2.0-flash, etc.), API keys, model IDs |
| `reference/models/claude.md` | Anthropic Claude models via API, supported model IDs, Python/TS/Go/Java setup |
| `reference/models/vertex-ai.md` | Models hosted on Vertex AI (Gemini, Claude, Llama, etc.) via Vertex endpoint |
| `reference/models/apigee.md` | Apigee AI Gateway for enterprise model routing and governance |
| `reference/models/ollama.md` | Ollama for local model inference: setup, model pull, connecting to ADK |
| `reference/models/litellm.md` | LiteLLM proxy: 100+ providers (OpenAI, Azure, Mistral, etc.) through one interface |
| `reference/models/vllm.md` | vLLM for high-throughput local inference |
| `reference/models/litert-lm.md` | LiteRT-LM for on-device inference on Android/embedded |

---

## 4. Tools

Giving agents capabilities to act.

| Reference | When to Consult |
|---|---|
| `reference/tools/tools-and-integrations.md` | All built-in tools (Google Search, code exec, etc.) and third-party integrations (LangChain, CrewAI, Vertex) |
| `reference/tools/function-tools-overview.md` | Writing custom function tools: type hints, docstrings, return types, async, long-running — load language sidecar for LongRunningFunctionTool and AgentTool patterns |
| `reference/tools/tool-performance.md` | Parallel tool calls, caching tool results, performance optimization |
| `reference/tools/action-confirmations.md` | Requiring human approval before tool execution |
| `reference/tools/mcp-tools.md` | Connecting MCP servers as ADK tools: MCPToolset, stdio and SSE transports — load Python sidecar for full wiring patterns |
| `reference/tools/openapi-tools.md` | Generating tools from an OpenAPI 3.0 spec: RestApiTool, auth schemes |
| `reference/tools/tool-authentication.md` | Tool auth concepts: API keys, OAuth 2.0, service accounts — load Python sidecar for complete OAuth flow implementation |
| `reference/tools/tool-limitations.md` | Tool call limits, unsupported patterns, known constraints |
| `reference/tools/skills-for-agents.md` | ADK Skills: reusable packaged tool sets for inter-agent sharing |

---

## 5. Sessions, State & Memory

Persistence and context management across turns and sessions.

| Reference | When to Consult |
|---|---|
| `reference/sessions/sessions-overview.md` | Sessions architecture: what a session is, lifecycle, service types |
| `reference/sessions/sessions.md` | Session CRUD, InMemorySessionService vs DatabaseSessionService, AppConfig |
| `reference/sessions/rewind-sessions.md` | Rewinding a session to a prior turn |
| `reference/sessions/migrate-sessions.md` | Migrating session data between service backends |
| `reference/sessions/state.md` | State concepts: `context.state`, `output_key`, state scopes (session/user/app/temp), `{key}` templating — load language sidecar for code patterns |
| `reference/sessions/memory.md` | Long-term memory concepts: MemoryService, search, adding memories — load language sidecar for implementation patterns |

---

## 6. Context

Managing the LLM's context window efficiently.

| Reference | When to Consult |
|---|---|
| `reference/context/context-overview.md` | What context is in ADK: system prompt, session history, tool results |
| `reference/context/context-caching.md` | Caching repeated context (system prompt, documents) to reduce cost/latency |
| `reference/context/context-compression.md` | Compressing/summarizing long session history to fit within context limits |

---

## 7. Callbacks

Intercepting and modifying agent behavior at runtime.

| Reference | When to Consult |
|---|---|
| `reference/callbacks/callbacks-overview.md` | What callbacks are, registration, invocation order |
| `reference/callbacks/types-of-callbacks.md` | All 6 callback types: before/after model, before/after tool, before/after agent — load language sidecar for complete runnable examples |
| `reference/callbacks/callback-patterns.md` | Design patterns: logging, guardrails, caching, modifying requests/responses |

---

## 8. Components

Core ADK building blocks beyond agents and tools.

| Reference | When to Consult |
|---|---|
| `reference/components/artifacts.md` | Artifacts: storing/retrieving files and binary blobs within a session |
| `reference/components/events.md` | Event system: event types, reading event history, custom events |
| `reference/components/apps.md` | App layer: multi-session app management, AppConfig |
| `reference/components/plugins.md` | ADK plugins: extending the framework, plugin registration |
| `reference/components/mcp.md` | MCP server built into ADK: exposing your agent as an MCP server |

---

## 9. Streaming

Real-time bidirectional communication with agents.

| Reference | When to Consult |
|---|---|
| `reference/streaming/streaming-overview.md` | Streaming overview: Gemini Live API integration, use cases, architecture |
| `reference/streaming/part1-intro-to-streaming.md` | Streaming setup concepts: LiveRequestQueue, run_live() — load Python sidecar for full FastAPI WebSocket example |
| `reference/streaming/part2-sending-messages.md` | Sending text and audio messages to a streaming agent |
| `reference/streaming/part3-event-handling.md` | Handling streaming events: text chunks, audio, function calls, turn completion |
| `reference/streaming/part4-run-configuration.md` | RunConfig for streaming: voice, response modalities, speech config |
| `reference/streaming/part5-audio-images-video.md` | Multimodal streaming: audio input/output, images, video frames |
| `reference/streaming/streaming-tools.md` | Using tools in streaming mode: streaming-compatible tool patterns |
| `reference/streaming/streaming-configuration.md` | Full streaming configuration reference |

---

## 10. A2A Protocol (Agent-to-Agent)

Connecting ADK agents across services and organizations.

| Reference | When to Consult |
|---|---|
| `reference/a2a/a2a-introduction.md` | A2A protocol overview: agent cards, task lifecycle, discovery |
| `reference/a2a/quickstart-exposing-python.md` | Expose a Python ADK agent as an A2A server |
| `reference/a2a/quickstart-consuming-python.md` | Consume a remote A2A agent from a Python ADK agent |
| `reference/a2a/quickstart-exposing-go.md` | Expose a Go ADK agent as an A2A server |
| `reference/a2a/quickstart-consuming-go.md` | Consume a remote A2A agent from a Go ADK agent |

---

## 11. Grounding

Connecting agents to real-world data sources.

| Reference | When to Consult |
|---|---|
| `reference/grounding/google-search-grounding.md` | Google Search grounding: enable web search in responses, citation handling |
| `reference/grounding/vertex-ai-search-grounding.md` | Vertex AI Search grounding: enterprise search over your own documents |

---

## 12. Runtime & CLI

Running, serving, and inspecting agents.

| Reference | When to Consult |
|---|---|
| `reference/runtime/runtime-overview.md` | Runner, InvocationContext, execution lifecycle overview |
| `reference/runtime/web-interface.md` | `adk web` dev UI: testing agents interactively |
| `reference/runtime/command-line.md` | `adk run` and other CLI commands for running agents |
| `reference/runtime/api-server.md` | `adk api_server`: serving agents as a REST/WebSocket API |
| `reference/runtime/resume-agents.md` | Resuming long-running or paused agents |
| `reference/runtime/runtime-config.md` | RunConfig: max turns, streaming mode, response modalities |
| `reference/runtime/event-loop.md` | Event loop internals: how ADK processes events between runner and agent |
| `reference/reference/cli-reference.md` | Full CLI reference: all commands and flags |

---

## 13. Deployment

Taking agents to production.

| Reference | When to Consult |
|---|---|
| `reference/deployment/deployment-overview.md` | Deployment options comparison: Agent Engine vs Cloud Run vs GKE |
| `reference/deployment/agent-engine.md` | Vertex AI Agent Engine: managed serverless deployment |
| `reference/deployment/agent-engine-standard-deployment.md` | Standard Agent Engine deployment: packaging, deploying, versioning |
| `reference/deployment/cloud-run.md` | Deploying ADK agents to Cloud Run: Dockerfile, service config, scaling |
| `reference/deployment/gke.md` | Deploying ADK agents to GKE: Helm charts, autoscaling, GPU support |

---

## 14. Observability & Evaluation

Understanding and measuring agent behavior.

| Reference | When to Consult |
|---|---|
| `reference/observability/observability-overview.md` | Tracing with OpenTelemetry/Cloud Trace, metrics, Vertex AI evaluation integration |
| `reference/observability/logging.md` | Logging configuration: log levels, structured logging, Cloud Logging |
| `reference/evaluation/evaluation-overview.md` | Agent evaluation framework: test cases, criteria, running evals |
| `reference/evaluation/evaluation-criteria.md` | Evaluation criteria types: trajectory match, response match, custom metrics |
| `reference/evaluation/user-simulation.md` | Simulating multi-turn user conversations for automated evaluation |

---

## 15. Safety

| Reference | When to Consult |
|---|---|
| `reference/safety.md` | Safety guidelines: input/output filtering, responsible AI practices |
