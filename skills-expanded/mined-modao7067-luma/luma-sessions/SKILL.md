---
name: luma-sessions
description: Create, attach, monitor and message CLI sessions in the current Luma App.
---
`luma-sessions '<JSON>'` or JSON stdin. App running; auth automatic, never inspect/export binding.
- list → clis,nativeProtocols,sessions. Use exact cli names and returned local id. Antigravity attach requires nativeProtocol from list; create may select it, defaults to agy CLI. Protocol identity never changes.
- create(cli,cwd,requestId[,model,title,nativeProtocol]); attach(cli,cwd,nativeId[,title,nativeProtocol,externalSocket,id]) → session. Background; keeps current page. Attach reuses native identity, never copies history. Kimi Code defaults to kimi-web-v1 and falls back to kimi-acp when Web capabilities are incompatible (or when kimi-acp is explicitly selected); release any idle observer before switching protocols, and never run both owners concurrently. Root Codex may explicitly join an existing Unix AppServer with externalSocket (Ubuntu absolute socket path); the thread must already be loaded on every connect. No other CLI/environment accepts it. Optional id explicitly repairs a never-bound, disconnected failed reference with no outbox and matching CLI/nativeId; bound references never change owner.
- send(id,text,requestId) → delivery. status(id OR requestId) → current state. accepted = native admission, not task completion; pending = queued/awaiting native ACK; unknown = unconfirmed, no time-based failure. New user instruction → new ID; retry/query → same requestId+payload, never blind resend. Default steer, otherwise FIFO.
- read(id[,limit=20,max100,before=messageId]) → messages,requests,queue. Approvals stay with user.
- rename(id,title) → local manual alias; nonblank. Names: manual alias > native title > first message.
create/send require a unique requestId (1–128 letters/digits/_/-). No cross-App/environment control; no foreground selection or draft editing.
