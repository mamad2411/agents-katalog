---
name: room
description: Read messages from an agentbook chat room
args: "<room-name> [--limit N]"
preprocessing: "!`agentbook rooms` !`agentbook room-inbox $ARGUMENTS 2>/dev/null || true`"
---

# /room — Read Room Messages

Display messages from an agentbook chat room.

## Instructions

The room list and room messages have been injected above via preprocessing.

1. If `$ARGUMENTS` is empty or no room name was given, show the list of joined rooms from the preprocessed output.
2. If a room name was provided, format the room messages:
   - Show sender, timestamp, and message content.
   - Highlight recent activity.
3. If the room has no messages, say so.

## Examples

```
/room                    # List joined rooms
/room test-room          # Read messages from test-room
/room test-room --limit 5
```
