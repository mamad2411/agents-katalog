---
name: inbox
description: Do the requests the user sent to this session from the Layerwright window in Figma (they select layers, pick this session and an action like "Build this in code"), one or several at once. Use for /layer:inbox, or when a tool result contains fromFigma.
---

# Requests from the Figma window

1. `figma_inbox({ takeOver: true })` when the user typed /layer:inbox here: that moves to this session the requests sent to other sessions that haven't started on them. Plain `figma_inbox()` when a Monitor event or `fromFigma` brought you here: then it only adds requests no other session is handling. Requests under `elsewhere` belong to other sessions: leave them alone. Nothing there → say so, and how to send one: in the Layerwright plugin, select layers → choose this session → pick an action.
2. For each request: `figma_reply({ id, status: "working" })`, do it as its text says, then `figma_reply({ id, status: "done", message })` with one line on what you did and where. Can't do it → `status: "failed"` with what you need.
   - Pass `requestId: "<request id>"` on every Figma call for that request. Each request gets its own cursor in Figma, so the user sees who works on what.
   - Work on the layers by the ids the request names, not on "selection": the user keeps working in Figma and may select other things meanwhile.
3. Several requests at once (multitasking): don't make the user wait for one before the next starts.
   - Requests on different layers: do the first yourself and start each other one in a background subagent (Agent tool, `run_in_background: true`), giving it the request text from `figma_inbox` and telling it to pass `requestId: "<id>"` on every Figma call and to finish with `figma_reply`. Edits in Figma still run one at a time; they interleave safely.
   - Requests on the same layers: one after the other, in the order they came. Say so in the window: `figma_reply({ id, status: "working", message: "after <the other request>" })`.
   - A request that arrives while you work (a Monitor event or `fromFigma`): handle it the same way, without dropping what you're doing.
4. Sending it from Figma is the user's approval to change those layers, not others. Anything unclear: ask here in the chat; the Figma window tells the user to come and answer you.
