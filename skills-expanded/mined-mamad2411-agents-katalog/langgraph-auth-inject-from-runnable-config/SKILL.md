---
name: langgraph-auth-inject-from-runnable-config
description: Hydrate auth/user/org/thread/run identifiers into LangGraph state from the RunnableConfig at the very first node, so every downstream node sees a uniform identity payload regardless of caller.
category: agent-sdk
version: 1.0.0
version_origin: extracted
tags: [langgraph, auth, state, runnable-config]
confidence: high
source_type: extracted-from-git
source_url: https://github.com/Tracer-Cloud/opensre.git
source_ref: main
source_commit: fb5ba0a1b4ef511d16c56a80f1f126b1f581d724
source_project: opensre
source_path: app/nodes/auth.py
imported_at: 2026-04-18T00:00:00Z
---

# LangGraph Auth Inject Node

## When to use
LangGraph servers expose authenticated user info in `config["configurable"]["langgraph_auth_user"]`. You want that info inside `state` (so every node can access it without re-parsing config), and you want graceful fallback when running without auth (CLI, tests).

## How it works
A single LangGraph node is set as the entry point. It reads from `config["configurable"]["langgraph_auth_user"]` plus `thread_id`/`run_id`, falls back to existing state keys, and returns a partial-update dict that LangGraph merges into state.

## Example
```python
def _extract_auth(state, config) -> dict[str, str]:
    configurable = config.get("configurable", {})
    auth = configurable.get("langgraph_auth_user", {})
    thread_id = configurable.get("thread_id", "") or state.get("thread_id", "")
    run_id    = configurable.get("run_id", "")    or state.get("run_id", "")
    return {
        "org_id":        auth.get("org_id")           or state.get("org_id", ""),
        "user_id":       auth.get("identity")         or state.get("user_id", ""),
        "user_email":    auth.get("email", ""),
        "user_name":     auth.get("full_name", ""),
        "organization_slug": auth.get("organization_slug", ""),
        "thread_id":     thread_id,
        "run_id":        run_id,
    }

def inject_auth_node(state, config):
    return _extract_auth(state, config)

graph.add_node("inject_auth", inject_auth_node)
graph.set_entry_point("inject_auth")
```

## Gotchas
- The node receives `config` as a positional argument because it has two parameters; LangGraph binds it automatically.
- Always fall back to state values so CLI/tests that pre-populate state still work.
- Keep the partial dict flat — nesting auth in a sub-key would force every downstream node to re-flatten.
