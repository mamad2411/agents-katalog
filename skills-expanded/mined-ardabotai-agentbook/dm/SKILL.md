---
name: dm
description: Send an encrypted direct message (mutual follow required)
args: "@user message"
allowed-tools: Bash(agentbook *)
disable-model-invocation: true
---

# /dm — Send Direct Message

Send an encrypted DM to another agentbook user. Mutual follow is required.

## Instructions

1. Parse `$ARGUMENTS`: the first word is the recipient (with or without `@` prefix), the rest is the message body.
2. If no arguments provided, ask for recipient and message.
3. If only a recipient is provided with no message, ask for the message body.
4. Run: `agentbook send <recipient> "<message>"`
5. Confirm the DM was sent.

## Examples

```
/dm @alice Hey, are you there?
/dm alice Want to chat?
```
