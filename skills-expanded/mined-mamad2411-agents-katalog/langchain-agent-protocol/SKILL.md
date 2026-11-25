---
name: langchain-agent-protocol
description: >-
  Agent Protocol: Agent Protocol is our attempt at codifying the framework-agnostic APIs that are needed to serve LLM agents in production. Covers Agent Protocol. Use when implementing the LangChain Agent Protocol. Triggers: Agent Protocol.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.1.0"
  kind: standard
---

# Agent Protocol

Agent Protocol from LangChain is a framework-agnostic HTTP API for serving LLM agents: stateless and background runs, threads with state history, agent introspection, a long-term memory store and thread streaming. This skill quotes the repository README and its OpenAPI document (`openapi.json`, API version 0.1.6) at a pinned commit.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text, labelled with the section they come from. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: Agent Protocol server implementer, client or SDK author, or reviewer of an agent-serving API.
- Target version: Agent Protocol (current). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher for a newer revision or version line.

## Invariants

1. **Threads: multi-turn interactions.** "Ensure that only one run per thread is active at a time"
2. **Threads: multi-turn interactions.** "Track history of past states of a thread, modelled as an append-only log of states"
3. **PATCH /threads/{thread_id}.** "Update a thread's values or metadata. Updating values creates a new revision in the thread's history."
4. **DELETE /runs/{run_id}.** "Delete a finished run. A pending run needs to be cancelled first, see previous endpoint."
5. **GET /runs/{run_id}/stream.** "Join the output stream of an existing run. Only output produced after this endpoint is called will be streamed."
6. **RunCreate.thread_id.** "The ID of the thread to run. If not provided, creates a stateless run. 'thread_id' is ignored unless Threads stage is implemented."
7. **RunCreate.on_completion.** "Whether to delete or keep the thread when run completes. Must be one of 'delete' or 'keep'. Defaults to 'delete' when thread_id not provided, otherwise 'keep'."
8. **RunCreate.if_not_exists.** "How to handle missing thread. Must be either 'reject' (raise error if missing), or 'create' (create new thread)."
9. **ThreadCreate.if_exists.** "How to handle duplicate creation. Must be either 'raise' (raise error if duplicate), or 'do_nothing' (return existing thread)."
10. **Thread.messages.** "If messages are contained in Thread.values, implementations should remove them from values when returning messages. When this key isn't present it means the thread/agent doesn't support messages."
11. **POST /threads/{thread_id}/stream.** "Closing the HTTP connection unsubscribes from this stream."

## Workflow

1. **Pick the version.** Use the current line unless a named consumer needs a supported one. Do not author a legacy line. Emit a preview only when its posture is build and the user asked for that draft.
   -> [`references/versions.md`](references/versions.md)
   ✓ The target version is recorded, and it is not a legacy line.
2. **Apply the pinned requirements.** Walk the quotes in [`references/requirements.md`](references/requirements.md) and implement each one that applies to the role.
   -> [`references/requirements.md`](references/requirements.md)
   ✓ Each applicable quote is either implemented or recorded as out of scope for the role, with the section it came from.
3. **Upgrade** (only when asked). Follow the upgrade section from the source line to the target.
   -> [`references/versions.md`](references/versions.md)
   ✓ The result cites the target line and no longer depends on a requirement that only the old line stated.

## Verify before done

- [ ] The artifact cites the target line's revision from [Sources](#sources).
- [ ] Every applicable quoted requirement in [`references/requirements.md`](references/requirements.md) holds.
- [ ] Each `enum`-valued property the server accepts (`on_completion`, `on_disconnect`, `if_not_exists`, `if_exists`, cancel `action`) rejects values outside the OpenAPI enum.
- [ ] Nothing from a preview line is emitted unless its posture is build and the user opted in.

## Reference index

- **`references/versions.md`**: every version line, which one to use, and how to upgrade. Load for steps 1 and 3.
- **`references/requirements.md`**: quotes taken from the pinned specification, grouped by source. Load for step 2.

## Related skills

Install related spec skills by name with `npx skills add ScaleDockHQ/scaledock-skills --skill <name>`: `openapi`, `server-sent-events`, `websocket`, `json-schema`, `a2a`, `mcp`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [Agent Protocol README](https://raw.githubusercontent.com/langchain-ai/agent-protocol/fb81f3e27ee507557926ecf923d0f933a1c76d44/README.md): Specification, commit fb81f3e, 2026-09-22, checked 2026-10-06.
- [Agent Protocol OpenAPI document](https://raw.githubusercontent.com/langchain-ai/agent-protocol/fb81f3e27ee507557926ecf923d0f933a1c76d44/openapi.json): Specification, commit fb81f3e, 2026-09-22, info.version 0.1.6, checked 2026-10-06.
