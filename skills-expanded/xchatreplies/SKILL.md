---
name: xchatReplies
description: Answer people who write to matt on X - X pushes each X Chat message over one socket (no polling), the inbox hook says who wrote, then read the thread, draft from matt's own writing guide, gate it with log voice, show matt, send only when he says. Use when a >>> NEW MESSAGE note arrives, when matt asks who messaged, or asks to reply, follow up or take over a conversation.
---

# xchatReplies

X's own chat app never polls: it holds one socket and X pushes every message
down it (`docs/platforms/x/xchat/live.md`, issue #68). log does the same, so
replies show up the second they land and no inbox read ever hits X's 429.

## Hard boundaries

1. **Never poll the inbox to find replies.** The inbox hook keeps
   `log twitter chat watch --inbox` running per signed-in X account. Read a
   thread only to answer it.
2. **Claim the chat before drafting** (rule 133): `log inbox claim --platform
   twitter --account <a> --chat <conversation id> --event <event id>` (MCP
   `inboxClaim`), and read `log inbox actions --chat <id>` to see what was
   already done there. Another session holding it means leave it; the send
   releases the claim.
3. **Read everything with the person first:** `log twitter dms --account
   <a> --with <handle>` (the old DM thread and X Chat are one conversation,
   rule 88).
3. **Draft from matt's guide, with his facts only.** Read
   `C:/Users/0/.buzz/GUIDES/MATT_WRITING_STYLE.md` before drafting. Lowercase,
   no commas or full stops, his words, almost never end on a question, no
   praise-then-pitch, nothing he didn't say (rules 39-41).
4. **Gate every draft:** `log voice --to <handle> --text "<draft>"
   --context "<what they said>"`. Rewrite until it says PASS.
5. **Show matt and send only when he says**, unless he has handed you the
   conversation (2026-10-28: "let the ai take over the conversation"). Then
   gate each reply and send it, and stop the moment he says it's over.

## The routine

```bash
# who wrote: the hook says it, pushed by X. To watch by hand:
log twitter chat watch --account matthewsoldit --seconds 600
# read them
log twitter dms --account matthewsoldit --with <handle>
# gate the draft
log voice --to <handle> --text "<draft>" --context "<what they said>"
# send, once matt says
log twitter dm --account matthewsoldit --userId <id> --text "<draft>" --approvedBy matt --live
```

## When it goes wrong

- `(could not open: … no matching key found …)`: the conversation's key
  wasn't primed. The watch re-reads the newest inbox page once and retries;
  if it still fails, restart the watch (it primes every key at start).
- `socket closed` / `connectFailed`: the watch takes a new token and
  reconnects on its own (2 s, doubling to 60 s).
- Nothing arriving: check `~/.logCli/inbox/twitter/<a>/watch.log` and
  `watch.pid`; delete the pid file and the next hook starts a fresh watch.
- X changed its code: re-read it with rea, the steps are in
  `docs/platforms/x/xchat/live.md`.
