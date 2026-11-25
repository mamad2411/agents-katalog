---
name: langgraph-investigation-pipeline-graph
description: Wire a multi-stage incident investigation as a LangGraph StateGraph with conditional routing, a bounded plan→investigate→diagnose loop, and dual chat/investigation entry modes from one auth-injecting entry point.
category: agent-sdk
version: 1.0.0
version_origin: extracted
tags: [langgraph, agent, pipeline, state-graph, conditional-edges]
confidence: high
source_type: extracted-from-git
source_url: https://github.com/Tracer-Cloud/opensre.git
source_ref: main
source_commit: fb5ba0a1b4ef511d16c56a80f1f126b1f581d724
source_project: opensre
source_path: app/pipeline/graph.py
imported_at: 2026-04-18T00:00:00Z
---

# LangGraph Investigation Pipeline Graph

## When to use
You need a single LangGraph that supports both quick chat tool-calls and a longer multi-step investigation loop, gated on an auth-extraction step that runs before any branching. Useful for SRE, RAG-with-validation, or any "extract → plan → execute → judge → maybe loop → publish" flow.

## How it works
- One entry point (`inject_auth`) hydrates state from the LangGraph `RunnableConfig` (e.g. JWT claims) before the graph branches.
- A `route_by_mode` conditional edge picks between `"chat"` and `"investigation"` based on `state["mode"]`.
- Chat side: `router → (chat_agent | general)` with a `should_call_tools` conditional that routes the chat agent into a `tool_executor` and back.
- Investigation side: `extract_alert → resolve_integrations → plan_actions → investigate → diagnose → (loop back to plan_actions | publish)`.
- The diagnose node returns recommendations that feed the loop conditional. A counter (`MAX_INVESTIGATION_LOOPS = 4`) prevents runaway loops.

## Example
```python
from langgraph.graph import END, StateGraph

def build_graph(config=None) -> CompiledStateGraph:
    graph = StateGraph(AgentState)
    graph.add_node("inject_auth", inject_auth_node)
    graph.add_node("router", router_node)
    graph.add_node("chat_agent", chat_agent_node)
    graph.add_node("general", general_node)
    graph.add_node("tool_executor", tool_executor_node)
    graph.add_node("extract_alert", node_extract_alert)
    graph.add_node("resolve_integrations", node_resolve_integrations)
    graph.add_node("plan_actions", node_plan_actions)
    graph.add_node("investigate", node_investigate)
    graph.add_node("diagnose", node_diagnose_root_cause)
    graph.add_node("publish", node_publish_findings)

    graph.set_entry_point("inject_auth")
    graph.add_conditional_edges(
        "inject_auth", route_by_mode,
        {"chat": "router", "investigation": "extract_alert"},
    )
    graph.add_conditional_edges(
        "router", route_chat,
        {"tracer_data": "chat_agent", "general": "general"},
    )
    graph.add_conditional_edges(
        "chat_agent", should_call_tools,
        {"call_tools": "tool_executor", "done": END},
    )
    graph.add_edge("tool_executor", "chat_agent")
    graph.add_edge("general", END)

    graph.add_conditional_edges(
        "extract_alert", route_after_extract,
        {"end": END, "investigate": "resolve_integrations"},
    )
    graph.add_edge("resolve_integrations", "plan_actions")
    graph.add_edge("plan_actions", "investigate")
    graph.add_edge("investigate", "diagnose")
    graph.add_conditional_edges(
        "diagnose", route_investigation_loop,
        {"investigate": "plan_actions", "publish": "publish"},
    )
    graph.add_edge("publish", END)
    return graph.compile()
```

## Gotchas
- Always cap loops via a counter check inside the loop predicate; LangGraph won't stop a self-recursive subgraph by itself.
- A "noise" short-circuit (`route_after_extract → END`) saves a full pipeline run when the alert is junk.
- Keep `inject_auth` first so chat and investigation paths share a single auth surface.
- Maintain a compatibility shim (`app/graph_pipeline.py`) re-exporting `build_graph` for legacy deployment configs that hard-code the path.
