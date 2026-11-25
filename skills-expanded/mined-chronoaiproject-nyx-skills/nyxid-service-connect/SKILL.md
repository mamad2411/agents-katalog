---
name: nyxid-service-connect
description: Connect, add, reconnect, or repair a NyxID service through NyxID's secure credential and provider OAuth surfaces, then grant the current Aevatar developer app incremental access to that connected service. Use when a user wants a new NyxID service, sees a missing-connection or missing-credential error, needs provider OAuth, or must authorize an already connected service for NyxID Chat without exposing secrets to the model. 中文触发包括“连接新的 NyxID 服务”“新增服务”“授权服务”。
version: "1.1"
metadata:
  category: tool-based
  tool-list:
    - nyxid_services
    - nyxid_catalog
  tag:
    - nyxid
    - services
    - connect
    - oauth
    - credentials
    - aevatar
---

# Connect a NyxID service

Treat service connection and app authorization as two separate user decisions:

- Connection stores or obtains the upstream provider credential in NyxID.
- Authorization adds the connected service resource to the current Aevatar app's NyxID consent.

A connected service is not automatically authorized to every developer app.

## Secret boundary

Never ask the user to paste an API key, client secret, refresh token, password, or private key into chat. Never place a secret in a URL, tool argument, log, or final response.

Do not call `nyxid_services` with `action: "create"` or `action: "rotate_credential"`. Those actions currently carry `credential` through model-visible tool arguments. Use NyxID's secure web credential or provider OAuth flow instead.

## Connection workflow

1. Call `nyxid_services` with `action: "list"` and look for an exact slug or an unambiguous label match.
2. Call `nyxid_catalog` with the candidate slug. Use its declared authentication type, credential fields, endpoint requirements, and provider scope information; do not invent them.
3. If a usable connected instance already exists, do not create a duplicate. Continue to app authorization.
4. If no usable instance exists, hand the user to the secure NyxID service flow with the catalog slug preselected:
   - Prefer a secure connect action supplied by the host.
   - In production, the fallback is `https://nyx.chrono-ai.fun/keys?slug={url-encoded-catalog-slug}`.
   - In another environment, use its configured NyxID web origin with `/keys?slug=...`; never guess a non-production origin.
5. Tell the user only what decision the secure page will request, such as provider OAuth scopes, a credential, an endpoint, or node routing. NyxID, not the chat, must collect the secret.
6. After the user returns, call `nyxid_services` again and verify the instance is present and active. Do not claim success before this check.

## App authorization workflow

If the connected service is not authorized for the current Aevatar app, stop before invocation and present the chat host's service authorization action for the exact service ID. In NyxID Chat this is the existing Authorization control backed by `/api/auth/authorize?serviceId={user-service-id}`.

The user must click and approve the incremental NyxID consent. Preserve existing resource grants and add only the selected service. Do not request blanket access, silently widen consent, or treat initial login as consent for future services. The core `chrono-llm-public` and `ornn-api` resources may be requested during initial NyxID Chat login; other services remain incremental.

After the OAuth callback, refresh the service inventory before proceeding. If consent is denied or cancelled, keep the service connected but report that this app is not authorized to use it.

## Finish

Return one of: connected and authorized, connected but awaiting app authorization, awaiting secure NyxID connection, or failed with the exact non-secret error. Use `nyxid-service-call` only after both connection and app authorization are ready.
