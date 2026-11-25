---
name: messages-inbox-triage
description: Triage unread conversations in the signed-in first-party macOS Messages app by voice or text while preserving read state and requiring exact, recipient-bound reply authorization. Use for interactive message triage, not unattended outreach, bulk replies, or general contact research.
---

# Messages Inbox Triage

Process one frozen unread-conversation snapshot quickly without losing choices, repeating cards, or sending to an unverified destination.

## Start

- Resolve the complete request from the current conversation. A standalone load request means load this skill and report ready without opening Messages; a triage request means start. Pause, stop, and scope changes take precedence.
- Read [triage-protocol.md](references/triage-protocol.md) once per run. Reuse the same first-party Messages app instance, frozen inventory, manifest, and cache across turns.
- Use the supported first-party Messages app through the documented foreground interaction controls. Do not query message databases, Contacts, AppleScript, connectors, or APIs. If the host lacks the required native app or documented runtime, report that prerequisite and do not mutate the app. Do not install dependencies silently.
- Take one shallow sidebar snapshot. Freeze opaque keys in visible order and preserve each original unread state. Distinguish a visible badge from the actual inventory; do not invent timestamps, services, endpoints, or identity hashes.
- Present the first complete safe sidebar card before protocol loading, helper initialization, or bootstrap. Retain it and up to three complete safe successor previews in volatile memory with their real observation times. Do not open successors to prepare the first card.
- While the user reviews the first card, initialize the bounded cache and body-free bootstrap once. Provisional rows stay `{key, materialized:false}` until exact identity is exposed.

## Decision loop

Load `scripts/foreground_cards.cjs` and then `scripts/messages_startup.cjs` once in the host's documented persistent JavaScript runtime. Use the runtime's supported module-loading route; do not assume an ESM Node REPL, direct CommonJS import, or any private tool exists. If none is available, stop at the prerequisite instead of switching runtimes or installing one.

1. Keep every safe successor within the next three frozen keys, with a 90-second expiry from its original observation. Never persist message bodies.
2. Record the user's exact choice with `scripts/triage_state.py` before UI work and pass the actual result to `cards.applyResult(result)`.
3. Present `next_card` immediately, then acknowledge it with `cards.presented(key)` in the next existing runtime call. Call `cards.beforeStep(step)` before mutation, refill, setup, or bookkeeping; a false result blocks that step.
4. Apply and verify one foreground mutation at a time. A queued or inflight operation is not complete.
5. Refill only from a fresh shallow sidebar read that does not open successors or change unread state. A missing safe preview gets one precise explanation, not a setup loop.

## Cards, pauses, and stop

Each card covers one frozen unread conversation and includes the visible sender/group, service and audience when known, time, content, minimal context, and a recommendation. Never infer a service or identity from a name or list position.

In voice ask one question: `Leave unread, mark read, or reply?` `skip` and `next` mean leave unread; `repeat` repeats only the current card. `Read the full message` means read the current complete text immediately, or perform the focused read in the protocol without rebuilding the inventory.

A process question, complaint, correction, or status request pauses the UI and next-card presentation. Use `cards.pause()` only if the cache exists. On clear continuation, resume the same frozen run and expire stale previews. On stop, preserve the requested unread state, use the helper's atomic stop-intent command when needed, call `cards.stop()`, and show no successor. After a durable stop or session loss, explicit continuation requires fresh identity evidence and a new cache. Never re-ask recorded decisions or infer a send from a hash.

## Recipient and reply safeguards

A visible contact name or group title is a provisional label, not send identity. For read-state-only choices, reacquire the exact unique sidebar row and independently verify its rendered unread marker. For a reply, establish the exact direct endpoint or complete group participant set, and the visible iMessage/SMS service, then materialize that body-free identity once. Reconfirm the destination against the binding before each submission; any changed or uncertain account, thread, participant set, service, or content blocks the send.

Drafts follow the user's current instructions. Existing conversation style may be used only when the user explicitly authorizes that context; no private tone tool or history corpus is required. Keep iterative drafts in chat. Present the complete current version and require an explicit send instruction for that version unless the user directly instructed the exact reply. Review-first requests control.

Before every necessary submission, perform one combined fresh check of exact destination, recipient-visible text, intended attachments and order, and absence of added attribution. Dispatch once. Read back the rendered outgoing result once and verify destination/service, exact content and attachments, cleared composer, no failure or duplicate, and no AI attribution. Do not retry after an ambiguous or uncertain outcome.

## State and recovery

Use the helper and protocol recipes. Store only opaque identities, decisions, hashes, operation state, and proof state in a private mode-0600 manifest under a runtime-resolved task directory. Send drafts through standard input; never persist names, endpoints, bodies, previews, or draft text.

Only one foreground mutation may be inflight. A semantic operation gets one primary attempt and, only after definitive failure, at most one fresh-read alternate. A bookkeeping error never authorizes another send. If opening a conversation changes unread state, restore the user's chosen state and obtain rendered proof before recording completion. A reply normally finishes read; an explicit reply-and-keep-unread choice requires a separate ordered mark-unread and proof.

Finish only with a selected disposition and fresh rendered proof for every frozen item, no queued or inflight operation left unverified, and one final delta scan. Report unresolved items separately. Offline tests do not prove live app access or send success.
