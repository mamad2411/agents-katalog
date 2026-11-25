# Plugin boundary

- Import lifecycle APIs from `@termco/kernel` and product contracts from their owning `@termco/*-base` packages; `termco-plugin.json` is the dependency source of truth.
- Consume `browser.automation`; never invoke private IPC.
- Operate on browser tabs supplied by the session-scoped `AiToolRuntime`.
- Keep external-origin actions dynamically approval-gated.
- Password entry and local-file upload always require approval.
- Own the per-session origin allowlist and expose it as `ai.browser-policy`.
- Publish AI-SDK-independent JSON schemas through `ai.tools`.
