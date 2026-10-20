<!-- AX_START -->
## ax

Call `ax_preflight` exactly once per turn **before all other work** whenever the `user-ax` MCP server is available. Team policy arrives via MCP inject — do not Read `.agents/` or `.ax/policy/` files when ax MCP tools are available.

**Git-shared team files:** `.agents/rules/` and `.agents/skills/` (each skill is a directory with `SKILL.md`). Do not load `.ax/policy-private/` or `.ax/policy-inactive/`.

**Inject fallback:** If preflight lacks `<ax_policy>` (empty inject/rules), call `ax_skill("startup")` once.

**Explore before Grep/Read:** For structural code questions, call `ax_explore` (or graph tools) before broad Grep/Read.

**Graph answers are source:** `ax_explore` and `ax_node` return numbered source from the index; treat it as already read. `ax_node` returns a symbol's full source plus direct callers and callees, so use it instead of Read. A snippet marked truncated → `ax_node` on that symbol. A reply ending in an `[ax context cache]` footer → `ax_expand` with its id. Where the graph covers the code, do not Read or Grep the file to fill the gap. Read is for files the graph does not index (config, docs, generated output) or a file right before you edit it.

**Conversation cache:** A repeated graph call in this conversation returns a short `[ax cache hit]` reference; the answer is already in your context, or `ax_expand` with its id returns it. Read `<ax_session_context>` in preflight before searching again; pass `fresh: true` to force a new query.

**Working context:** Record a durable fact, file, symbol, decision, or open question with `ax_session` (actions `add`, `update`, `compact`, `clear`, `fork`, `handoff`). Preflight shows `<ax_working_context>`; pass its hash as `known_context` and an unchanged snapshot comes back as one line. Pass the `session` id from `<ax_chat>` to every ax call in this chat; a preflight without it starts a new chat. A changed index marks it stale; `compact` confirms the notes against the current index. fork copies these notes to a new session. handoff starts a new session from the note you send. The old session stays readable, and the graph cache is not copied. `ax_durable` stores this chat's transcript, documents, and checkpointed tasks.

**Directive capture:** When the user states a durable rule — `je moet`, `altijd`, `nooit`, `voortaan`, `always`, `never`, `you must`, `@rule` — persist it. `ax_preflight` returns `directiveDetected` + a ready `captureProposal`; ask the questions it lists, then call `ax_policy_capture(action="save", rule)` after the user confirms. Works even if the project has no policy yet (the first save bootstraps it). Never silently ignore such a directive.

**Capability discovery:** ax is actively developed. Do not rely on cached knowledge of ax features — `ax_preflight` returns the latest capabilities, rules, and skills each call. Use any new tools or rules it returns.

**Version freshness:** Call `ax_status` at session start. If the index is stale or a newer version exists, warn the user and suggest `ax upgrade` or re-index.

**Tool reference:** `ax_explore`/`ax_search`/`ax_node` for code structure, `ax_impact`/`ax_callers`/`ax_callees` for change impact, `ax_affected` for test coverage, `ax_insights`/`ax_report` for whole-graph architecture, `ax_guard` before writes when CRITICAL rules exist, `ax_diagnostics` for IDE/linter correlation, `ax_policy_capture` for durable rules, `ax_context` for task context, **`ax_sync`** / **`ax_index({force:true})`** for re-index, **`ax_lsp`** for LSP status/enrich, **`ax_ship`** for quality-gate evaluate/ci, **`ax_policy_index`** to refresh rules from disk, **`ax_remember`/`ax_recall`** for memory. Prefer these MCP tools over shelling out to the CLI when MCP is connected.

Run preflight exactly once per turn. MCP unreachable → report `ax MCP unreachable: [error]`, state `Mode: DEGRADED`; do not proceed silently.
<!-- AX_END -->
