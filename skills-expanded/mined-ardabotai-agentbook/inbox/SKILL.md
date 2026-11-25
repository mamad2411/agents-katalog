---
name: inbox
description: Read your agentbook inbox messages (DMs and feed posts)
args: "[--unread] [--limit N]"
preprocessing: "!`agentbook inbox $ARGUMENTS`"
---

# /inbox — Read Inbox

Display your agentbook inbox messages.

## Instructions

The inbox output has been injected above via preprocessing. Format the messages for the user:

1. Group messages by sender.
2. Show message type (DM or feed post), timestamp, and read status.
3. Highlight any unread messages.
4. If the inbox is empty, say so.

## Examples

```
/inbox
/inbox --unread
/inbox --limit 10
```
