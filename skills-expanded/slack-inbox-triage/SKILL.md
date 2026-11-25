---
name: slack-inbox-triage
description: Triage unread Slack direct messages, group messages, channels, or threads by voice or text while preserving read state and requiring explicit, recipient-bound reply authorization. Use for interactive Slack inbox triage, not unattended outreach, bulk replies, or general Slack research.
---

# Slack Inbox Triage

Process one frozen unread snapshot at a time. Optimize for the next useful card without weakening read-state, recipient, draft, or send verification.

## Start

- Resolve the whole request from the current conversation. A standalone request to load the process means load these instructions and report that they are ready without opening Slack. A triage request that also asks to load the process means start triage. Pause, stop, and scope changes take precedence.
- Read [triage-protocol.md](references/triage-protocol.md) once per run. In voice mode, also read [voice-mode.md](references/voice-mode.md).
- Use the available documented first-party Slack interface and its supported foreground interaction controls. If the host does not expose a supported interface or JavaScript runtime required by the bridge, report that prerequisite and do not mutate Slack. Do not install dependencies silently.
- Take one shallow, read-only overview of the Slack Unreads or Activity surface. Freeze the visible order and original unread boundaries. Keep a visible badge count separate from the actual inventory; do not delay the first card for exhaustive enumeration.
- Present the first complete safe card before helper setup or manifest bookkeeping. Retain the first card and at most three complete safe successors in volatile memory with their real observation times. Do not open successors merely to prefetch them.
- While the user reviews the first card, initialize the bounded cache and body-free durable bootstrap with the same frozen opaque keys. Keep unavailable identity provisional and block mutation until the exact identity is bound. Never invent timestamps or destination IDs.

## Decision loop

Before routine mutation work after a clear disposition, bind the choice to the card just shown and present an already-observed, complete, fresh successor in the same response when one is available. Say that the prior action is pending, not complete. A preview already present in the current volatile context may be used without rereading Slack; a stale or incomplete preview gets one scoped read-only retrieval.

Load `scripts/foreground_cards.cjs` and then `scripts/slack_cards.cjs` once in the host's documented persistent foreground JavaScript runtime. Initialize `SlackCards` with the frozen run scope and body-free item bindings. The adapter is an in-memory guard only: it has no app, network, persistence, or speech access.

1. Retain all safe successors within the next three frozen keys. Entries expire 90 seconds after their original observation and never persist bodies.
2. Record each decision through `scripts/triage_state.py` before UI work. Use the exact result with `cards.applyResult(result)`.
3. Present `next_card` immediately, then acknowledge it with `cards.presented(key)` in the next existing runtime call. Call `cards.beforeStep(step)` before mutation, refill, setup, or bookkeeping; a false result blocks that step.
4. Drain one foreground mutation at a time. Recheck the actual account, workspace, conversation/thread, audience, and current context immediately before input. Queueing is not completion.
5. Refill only from a fresh shallow read that does not change unread state. If no safe complete preview exists, state that precise limit once; never fabricate text or consume an unread cursor to fill the window.

Read-only connectors may inventory or retrieve only when they are supported and add no recipient-visible attribution. Every Slack mutation, including send and read-state changes, must use the clean first-party interface with rendered post-action verification.

## Cards and choices

Show sender, destination and audience, time, unread content, minimal decision-relevant context, and one recommendation. Read messages of 75 words or fewer verbatim in voice; summarize longer messages faithfully and offer the full text. Ask one question: `Leave unread, mark read, or reply?`

- `leave unread`, `skip`, or `next` retains unread.
- `mark read` or `no reply` marks it read without replying. The voice homophone `mark red` has the same meaning.
- `reply` enters a draft loop. Keep drafts in the conversation, not in Slack's saved drafts.
- `repeat`, `more context`, and `go back` affect only the current frozen snapshot. `go back` is read-only and never reverses a send.
- A process question, complaint, or correction pauses card presentation and UI actions. Use `cards.pause()` only after the cache exists; answer directly, then resume the same run with `cards.resume()`.
- On `stop`, retain the final choice and call `cards.stop()`; show no successor. Use the helper's atomic stop-intent command when combining a choice and stop.
- After a drop, resume the existing manifest, discard stale previews, preserve queued and ambiguous evidence, and never replay a decided card or infer a send from a hash.

## Replies and safety

Drafts follow the user's current instructions. Existing channel style may be used only when the user explicitly authorizes that context; no private tone profile, cross-channel corpus, or history collection is required. Present the complete numbered draft. Positive feedback alone is not a send command. A clear direct instruction for a specific reply authorizes that reply; an explicit review-first request still controls.

Before dispatch, freshly verify the signed-in account, workspace, exact recipient or group/channel audience, thread context, exact composer text, attachment order, and absence of added attribution. Dispatch once. Verify one exact outgoing message in the intended destination, the cleared composer, no failure or duplicate, and no AI attribution before saying sent.

Persist only body-free opaque identity fields, decisions, hashes, operation state, and proof state in a private mode-0600 manifest under a runtime-resolved task directory. Keep raw bodies and drafts only in volatile context. Do not put bodies, names, endpoints, or private paths in command arguments, logs, or durable state.

Only the oldest unresolved mutation owner may control Slack. A semantic operation gets one primary attempt and, only after definitive failure, at most one fresh-read alternate. Success or uncertainty ends retry authority. A bookkeeping error never authorizes a second UI action. Preserve unread boundaries and perform final rendered cursor reconciliation before claiming completion.

Do not spawn a send watcher automatically. If the user separately authorizes a read-only watcher and the host supports it, [async-send-handoff.md](references/async-send-handoff.md) may be used only after one exact dispatch is recorded as acknowledgement-pending. The watcher must never control Slack or retry a send.

Finish only after every promised disposition has rendered proof. Report unresolved items, cursor collateral, and later arrivals separately. Synthetic tests and cached previews do not prove a live send.
