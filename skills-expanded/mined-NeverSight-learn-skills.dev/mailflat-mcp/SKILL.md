---
name: mailflat-mcp
description: Run the MailFlat MCP server so an MCP client (Claude Desktop, Cursor, or any other) can open inboxes and read codes as tools. Use when the agent works through MCP rather than an SDK.
---

# MailFlat over MCP

The same API as the SDKs, exposed as MCP tools by the `mailflat-mcp` server.

MailFlat addresses are permanent; only the messages inside them expire. Nothing here is a throwaway address.

## Run it

```bash
# zero-install, isolated (recommended)
MAILFLAT_API_KEY=mf_live_... uvx mailflat-mcp

# or install it once
pipx install mailflat-mcp
MAILFLAT_API_KEY=mf_live_... mailflat-mcp
```

## Point a client at it

```json
{
  "mcpServers": {
    "mailflat": {
      "command": "uvx",
      "args": ["mailflat-mcp"],
      "env": { "MAILFLAT_API_KEY": "mf_live_..." }
    }
  }
}
```

## Tools

| Tool | Arguments | What it does |
| --- | --- | --- |
| create_inbox | prefix? · label? · retention_hours? | Opens a real inbox and returns its address. |
| list_inboxes | none | Every inbox this API key can see. |
| read_messages | address · direction? | Messages in an inbox, newest first. Received mail unless you ask for 'out' or 'all'. |
| wait_for_otp | address · timeout? | Polls until a one-time code arrives, then returns it. |
| wait_for_message | address · timeout? | Polls until a new message ARRIVES. Ignores mail the agent itself sent. |
| send_email | address · to · subject? · body? · html? · cc? · bcc? | Sends a DKIM-signed email from the inbox. Accepted for delivery (202); the queue does the sending. |
| reply | address · message_id · body? · html? · cc? · bcc? | Answers a message in the SAME conversation. Recipient, Re: subject and threading headers are filled in. |
| wait_until_sent | address · message_id · timeout? | Answers 'did that mail actually go out?'. delivered:true once it did; a timeout means STILL QUEUED, not lost, so don't resend. |
| mark_read | address · message_id | Marks one message read, so the next poll can skip it. |
| burn_inbox | address | Deletes every message but KEEPS the address. |
| delete_inbox | address | Deletes the inbox and every message in it. |
| delete_message | address · message_id | Deletes one message; the inbox itself stays. |

Everything the server can do. The Vercel AI SDK suite and the LangChain toolkit expose the same twelve. send_email and reply take cc and bcc but NOT attachments. File bytes would have to travel through the model's context, which is expensive for a small file and impossible for a large one. Attach files from an SDK instead; the tools are the model's surface, the SDK is your code's.

## Core rules

- The server authenticates with `MAILFLAT_API_KEY` from the environment. It never takes a key as a tool argument.
- Getting a key needs a human once: MailFlat is in invited early access, so public sign-up is not open. Request access at https://mailflat.net/signup, then create the key under Agents -> API keys. An agent cannot issue itself a key today.
- The address comes from `prefix`; `label` is a display name.
- When a tool call fails, check the key first: the same key against the REST API tells you in one request whether the problem is auth or the tool.
- Encrypted inboxes return no body and no code through MCP either. Use plain-text agent inboxes.

## References

- [MailFlat MCP server: an inbox for any AI client](https://mailflat.net/docs/ai/mcp)
- [Using MailFlat with Claude Desktop](https://mailflat.net/docs/ai/claude-desktop)
- [Using MailFlat with Cursor](https://mailflat.net/docs/ai/cursor)
- [Agent API and MCP reference](https://mailflat.net/docs/api/agent-api)
- [Full documentation as one file](https://mailflat.net/llms-full.txt) - every page as plain markdown
- Any documentation page also serves raw markdown: add `.md` to its URL
