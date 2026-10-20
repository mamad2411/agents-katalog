<!-- AX_START -->
## ax

Call `ax_preflight` exactly once per turn **before all other work** whenever the ax MCP server is available. Full workflow: see `.claude/rules/ax.md`.

**Directive capture:** When the user states a durable rule — `je moet`, `altijd`, `nooit`, `voortaan`, `always`, `never`, `you must`, `@rule` — persist it. `ax_preflight` returns `directiveDetected` + a ready `captureProposal`; ask the questions it lists, then call `ax_policy_capture(action="save", rule)` after the user confirms. This works even if the project has no policy yet (the first save bootstraps it). Never silently ignore such a directive.

**Capability discovery:** ax is actively developed. Do not rely on cached knowledge of ax features — `ax_preflight` returns the latest capabilities, rules, and skills each call. Use any new tools or rules it returns.

**Version freshness:** Call `ax_status` at session start. If the index is stale or a newer version exists, warn the user and suggest `ax upgrade` or re-index.

MCP unreachable → report `ax MCP unreachable: [error]`, state `Mode: DEGRADED`; do not proceed silently.
<!-- AX_END -->
