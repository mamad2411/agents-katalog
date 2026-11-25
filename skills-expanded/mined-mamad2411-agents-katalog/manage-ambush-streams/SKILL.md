---
name: manage-ambush-streams
description: Manage a user's Ambush news streams through the Ambush Streams MCP server. Use when the user wants to create, list, inspect, rename, change, pause, resume, or delete an Ambush stream, or review a stream's emitted news items and delivery configuration.
---

# Manage Ambush Streams

Use the Ambush Streams MCP tools to turn plain-language monitoring requests into personalized news streams and manage those streams throughout their lifecycle.

The MCP API currently retains legacy tool and field identifiers such as `list_feeds`, `create_feed`, and `base_feed_id`. Use those exact identifiers when calling tools, but refer to the resulting resources as streams when speaking with the user.

## Operating rules

- Verify that the Ambush Streams MCP tools are available before acting. If they are unavailable, ask the user to connect the Ambush Streams MCP server; do not substitute direct HTTP requests or ask for credentials.
- Use `list_feeds` to discover the user's streams. Follow `next_cursor` only when the requested result may be on another page or the user asks for every stream.
- Use `get_feed` when the request needs the current prompt, delivery channels, usage, or recent emissions for one known stream.
- Resolve a stream by its returned ID. When names are duplicated or the target is ambiguous, present the matching names, prompts, and IDs and ask the user to choose.
- Never invent a stream ID, base stream ID, cursor, prompt, status, emission, or tool result.
- Treat a missing stream name gracefully: identify it by a short prompt excerpt and its ID.
- If authentication is required, ask the user to connect or reauthenticate Ambush Streams. Never ask the user to paste a bearer token.
- Report the result of every mutation, including the stream ID and returned status. Do not repeat a non-idempotent create call after an uncertain failure.

## Create a stream

1. Translate the user's request into a focused monitoring prompt. Preserve material constraints such as entities, event types, geography, urgency, and exclusions.
2. Ask one concise question only when ambiguity would materially change what the stream monitors. Do not require the user to know Ambush-specific fields.
3. Call `create_feed` with `prompt`, an optional `name`, and an optional known `base_feed_id`. At least one of `prompt` or `base_feed_id` is required.
4. Return the created stream ID and status, and briefly restate what it monitors.

Do not create several streams when one focused stream satisfies the request unless the user explicitly asks for separate streams.

## Update, pause, or resume a stream

1. Resolve the exact stream, using `list_feeds` first when the user supplied a name instead of an ID.
2. Call `update_feed` with only the fields the user asked to change:
   - `prompt` changes what the stream monitors.
   - `name` renames it.
   - `status: "paused"` pauses it.
   - `status: "active"` resumes it.
3. Do not look for separate pause or resume operations; status changes belong to `update_feed`.
4. Confirm the resulting status and stream ID.

## Review streams and emissions

- For an overview, call `list_feeds` and summarize names, statuses, current prompts, and channel counts. Do not expose cursors unless diagnostically useful.
- For one stream's recent activity, use `get_feed`. Use `list_emissions` when the user requests the complete or paginated history.
- Follow `next_cursor` until it is null only when the user asks for all matching emissions; otherwise return the requested page or a concise recent sample.
- Summarize structured emission payloads accurately. Clearly distinguish an empty history from a failed request.

## Delete a stream

Deletion is permanent and destructive.

1. Resolve the exact stream and state its name or prompt excerpt and ID.
2. Obtain explicit confirmation to permanently delete that exact stream. A general request such as "clean up my old streams" is not confirmation.
3. Call `delete_feed` only after confirmation. If the user's current message already unambiguously identifies the exact stream and explicitly says to permanently delete it, that message counts as confirmation.
4. Report the deleted stream ID. Never claim that deletion can be undone.

## Scope boundaries

- Use this skill for Ambush stream lifecycle and emission requests, not for unrelated news research, generic RSS development, or delivery-channel setup that the exposed tools cannot perform.
- Do not imply that creating a stream guarantees a particular story or delivery time.
- If a prompt is rejected by Ambush policy, explain the returned restriction briefly and help the user reframe a legitimate monitoring request without trying to bypass it.
