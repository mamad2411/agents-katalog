---
name: use
description: Bind the current Claude session to one Research Peer room. Use only when the local owner explicitly invokes /research-peer:use.
disable-model-invocation: true
---

# Use a room

If `$ARGUMENTS` is empty, run `research-peer room list`, show active rooms, ask which room to use, and stop.

Require `RESEARCH_PEER_SESSION_ID`; if absent, tell the owner to reopen Claude once with the terminal command `research-peer`. Otherwise run `research-peer session register --session-id "$RESEARCH_PEER_SESSION_ID" --alias "${RESEARCH_PEER_SESSION_ALIAS:-research-peer}" --room "$ARGUMENTS"` and summarize the binding. If `RESEARCH_PEER_AUTO_ANSWER=full`, note that the `rp` session-scoped auto-answer opt-in follows this binding without changing the room's persistent policy.
