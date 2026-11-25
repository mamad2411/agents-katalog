---
name: nyxid-service-discovery
description: Inventory and inspect NyxID services available to the current authenticated user across connected instances, the service catalog, proxy availability, and LLM routes. Use when a user asks what services they have, what can be added, whether a service is connected, active, healthy, or callable, which personal or organization source owns it, or needs exact service details before connecting, invoking, or maintaining it. 中文触发包括“我有哪些 NyxID 服务”“查看服务列表”“服务状态”。
version: "1.1"
metadata:
  category: tool-based
  tool-list:
    - nyxid_services
    - nyxid_catalog
    - nyxid_proxy
    - nyxid_llm_status
  tag:
    - nyxid
    - services
    - discovery
    - aevatar
    - broker
---

# Discover NyxID services

Use the NyxID access token supplied by the host. Never invoke the NyxID CLI, request a bearer token, or ask the user to expose credentials.

## Keep the states separate

Distinguish these facts instead of collapsing them into "available":

1. A catalog entry means NyxID knows how a service can be connected.
2. A connected service means the user or one of their organizations has an instance.
3. A proxyable service means the current token can discover it as callable now.
4. Developer-app authorization means the current app has consent for that service resource.
5. Provider scopes and request approval govern what an already connected service may do.

Only report a state that a tool result or host context establishes. In particular, never call a catalog-only service connected or infer app authorization from connection alone.

## Discovery workflow

1. For inventory, call `nyxid_services` with `action: "list"` first. Preserve each returned service ID, slug, label, active state, route, and owner/source fields when present.
2. If the user asks what can be added, call `nyxid_catalog` without a slug. For one candidate, call it again with the exact catalog slug before describing requirements.
3. If the user asks what is callable now, call `nyxid_proxy` without a slug and compare its result with the connected inventory.
4. If the question is about LLM readiness or routes, call `nyxid_llm_status` and correlate its service slug with the inventory. Do not assume every connected API is an LLM.
5. For "all services", merge by catalog slug but retain multiple connected instances as separate rows. Group results as connected and active, connected but inactive or unhealthy, and catalog-only.
6. For a narrow lookup, prefer exact ID or slug. If a label matches multiple instances, show the candidates and ask the user to select one before any later write.

## Report

Lead with the answer, then include only fields useful for the next decision. State unknown fields as unknown rather than guessing. Mention personal versus organization ownership only when the response identifies it.

If no services are connected, say so and suggest `nyxid-service-connect`. If a service is connected but the current app lacks access, describe it as connected but not authorized for this app and direct the user to the chat's authorization control. Use `nyxid-service-call` for invocation and `nyxid-service-maintenance` for changes.

Do not mutate services during discovery.
