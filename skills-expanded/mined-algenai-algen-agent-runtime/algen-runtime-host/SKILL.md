---
name: algen-runtime-host
description: Build or review an application that embeds Algen Agent Runtime (a chat UI, run following, an approvals inbox, metering, storage) so it uses the Runtime's conversations, approvals, event streams, recovery, steering, model routing, redaction and guards instead of rebuilding them.
---

# Host Algen Agent Runtime in an application

An application that embeds the Runtime (it calls `build_container`, `AgentRuntime` or
`ConversationService` from its own server, or serves the Runtime's HTTP API behind its own UI)
should own its product: users, screens, domain tools and data. It should not own a second copy of
what the Runtime already does. Most duplicates in host applications appeared because the Runtime
added the capability later, or did not document it.

Before writing host code for conversations, approvals, run events, restarts, steering, model
calls, usage, redaction, tool limits, structured answers or the Runtime's tables, read
`references/host-capabilities.md` and find the row for it. Use the Runtime's API when the
installed version has it (`python -c "import algen_agent_runtime as r; print(r.__version__)"`).
Keep your own only for the reason the row gives, and say so in a code comment.

When reviewing an existing host, look for these duplicates first:

- its own conversation, message, turn or approval tables, state machines or ownership filters;
- its own restart follow-up of turns that were waiting for approval or input, or that were
  streaming (the Runtime settles each turn by its run's state from 0.2.0b3);
- its own list of event types that mean "the run ended" or "the run paused";
- regular expressions that mask emails, phone numbers or tokens in stored tool results or logs,
  or that re-redact streamed `model.delta` text (the Runtime redacts it from 0.2.0b4);
- its own per-user filter in front of `/v1/artifacts` (the routes check the owner from 0.2.0b4);
- steering a run through a field in a tool result instead of `AgentRuntime.steer()`;
- direct `provider.generate(...)` calls, which skip the router's fallback, circuit breakers,
  rate limits and `UsageMeter`;
- prompt rules ("never call X more than three times") instead of `tool_policy` guards;
- a hardcoded or shared user id instead of the signed-in user, which breaks session ownership,
  `decided_by` on approvals and per-user metering;
- `CREATE TABLE algen_agent_runtime_*` in the host's own migrations, which falls behind the
  Runtime's migrations: apply `algen-agent-runtime migrations sql` and run `check_schema` instead;
- a context builder of its own kept only to change the token budget
  (`context_policy.max_context_tokens`), or code that erases a user's runs and sessions by hand
  (`container.user_data.erase_user`);
- its own counters of runs, tokens, tool calls or approvals built from run events or spans,
  where the Runtime's metrics (`telemetry.otlp_metrics_endpoint`, from 0.2.0b5) and its shipped
  dashboards and alert rules already measure them;
- a `try: await runtime.run(...) except asyncio.CancelledError: ...` that swallows the
  cancellation, or its own "cancelled" flag for runs: from 0.2.0b5 a cancelled waiter gets
  `CancelledError` and the run ends `cancelled` (`runtime.cancel`, `DELETE /v1/runs/{id}`);
- a hand-written list of experimental adapters or settings: ask
  `algen_agent_runtime.stability.is_experimental(...)` (from 0.2.0b5).

Always pass the real tenant and user on every call. Give each user their own `session_id` (a
conversation uses its own id). Pass the caller's credentials per run and again on every resume;
the Runtime never stores them. Let the Runtime create and migrate its own tables, in their own
schema (`storage.postgres_schema`) when the database is shared.

Removing a duplicate changes behaviour the host's users see, so do it one capability at a time,
with a test that pins the Runtime behaviour you now rely on. For a capability the installed
Runtime lacks, upgrade, or keep the host's version behind a note naming the Runtime version that
replaces it. The release notes list what each release lets a host delete under
"You can now remove" (`CHANGELOG.md`).

To build agents, tools or workflows rather than the host, use `$algen-agent-builder` and
`$algen-agent-connector`. Install these skills into an application repository with
`algen-agent-runtime skills install --path .` (from Runtime 0.2.0b3; add `--force` to refresh
them after upgrading the Runtime).
