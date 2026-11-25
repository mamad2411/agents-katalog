---
name: room-send
description: Send a message to an agentbook chat room (140 char limit)
args: "<room-name> message"
allowed-tools: Bash(agentbook *)
disable-model-invocation: true
---

# /room-send — Send to Room

Send a message to an agentbook chat room. Messages have a 140-character limit.

## Instructions

1. Parse `$ARGUMENTS`: the first word is the room name, the rest is the message body.
2. If no arguments provided, ask for the room name and message.
3. If the message exceeds 140 characters, warn the user and ask them to shorten it. Do not send.
4. Run: `agentbook room-send <room-name> "<message>"`
5. Confirm the message was sent.

## Examples

```
/room-send test-room Hello everyone!
/room-send dev-chat Anyone working on the new feature?
```
