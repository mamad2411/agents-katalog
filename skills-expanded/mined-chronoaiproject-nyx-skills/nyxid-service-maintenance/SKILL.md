---
name: nyxid-service-maintenance
description: Maintain an existing NyxID service by inspecting and updating labels, endpoints, active state, direct or node routing, health, external-key metadata, and deletion, while sending all credential rotation or repair through NyxID's secure UI. Use when a user asks to edit, reroute, enable, disable, repair, rotate credentials for, diagnose, or remove a connected NyxID service. 中文触发包括“修改 NyxID 服务路由”“更新服务”“轮换凭据”“删除服务”。
version: "1.1"
metadata:
  category: tool-based
  tool-list:
    - nyxid_services
    - nyxid_endpoints
    - nyxid_external_keys
    - nyxid_proxy
    - nyxid_llm_status
  tag:
    - nyxid
    - services
    - maintenance
    - routing
    - credentials
    - aevatar
---

# Maintain a NyxID service

Use only the host-supplied NyxID tools. Never invoke the NyxID CLI or request a raw access token.

## Resolve and inspect first

1. Call `nyxid_services` with `action: "list"` and resolve one exact service ID. If a label or slug maps to multiple instances, ask the user to select one.
2. Call `nyxid_services` with `action: "show"` and that ID before changing anything. Record the current label, slug, active state, endpoint, node route, ownership, and external-key ID when present.
3. For LLM-specific health, call `nyxid_llm_status`. For a general health check, use only a documented read-only operation through `nyxid_proxy`; do not invent a `/health` path.

## Apply the smallest change

- Change a label, endpoint URL, active state, or node ID with `nyxid_services` `action: "update"`. Send only the fields the user requested.
- Change routing with `nyxid_services` `action: "route"`, using either one explicit `node_id` or `direct: true`.
- Use `nyxid_endpoints` only when the user is managing a standalone endpoint record. Confirm the exact endpoint ID before update or deletion.
- Use `nyxid_external_keys` `action: "list"` only for non-secret credential metadata. Do not echo even a partially exposed credential value.

After a successful update or route change, call `show` again and report the observed state. If the service belongs to an organization and the caller lacks permission, report that ownership boundary instead of attempting a workaround.

## Repair or rotate credentials securely

Never ask for a credential in chat. Never call `nyxid_services` `rotate_credential` or `nyxid_external_keys` `rotate`, because both send the new secret through model-visible arguments.

Send the user to the secure NyxID detail page for the exact service:

- Prefer a secure repair action supplied by the host.
- In production, the fallback is `https://nyx.chrono-ai.fun/keys/{url-encoded-service-id}`.
- In another environment, use its configured NyxID web origin; never guess it.

After the user returns, call `show` and then one documented read-only health operation. Report success only after both checks pass.

## Destructive operations

Before deleting a service, endpoint, or external-key record, show its label, ID, owner, and expected impact, then obtain explicit confirmation naming that target. After confirmation, call the relevant delete action once. Do not cascade to related records unless the user separately requested and confirmed each deletion.

If deletion succeeds, refresh the service list and state that the target is no longer present. If it fails, preserve the current state and report the exact non-secret error.
