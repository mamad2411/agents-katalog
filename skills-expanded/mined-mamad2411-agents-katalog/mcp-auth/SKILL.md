---
name: mcp-auth
description: Establish or repair the ReadMe API key behind execute-request. Use when a ReadMe call fails with "Missing Security Schemes", "The API key couldn't be located", or "An unknown error has occurred", when the user asks which project their key reaches, when they say they set a key but it is not working, and before the first write to their project.
---

# The key behind execute-request

Public reads of ReadMe's documentation need no key; anything touching the user's own project does,
and it travels on the MCP server registration rather than in the tool call. See the `mcp-server`
skill for which calls land where.

Cursor prompts for `README_API_KEY` on install. Claude and Codex ship anonymous, so those users
still have to register the server themselves.

## Tools

- `execute-request`

## Assume the registration may be empty

Do not spend a call proving auth unless you need the user's project. Go straight to the work:

- ReadMe documentation questions — `search` and `fetch`, no key involved.
- The user's project, and they have not mentioned a key — go to **No key yet** below.
- The user says they set a key, or an `execute-request` call fails — verify with the probe.

## Verify

`execute-request`, spec title `ReadMe API`, with no `Authorization` header of your own:

```json
{
  "title": "ReadMe API",
  "harRequest": {
    "method": "get",
    "url": "https://api.readme.com/v2/projects/me"
  }
}
```

| Response | Means | Next |
| --- | --- | --- |
| A project object | The registration carries a working key | Name the project and subdomain, carry on. Ask for nothing |
| `Missing Security Schemes` | No `Authorization` header at all — the server is anonymous | **No key yet** |
| `"title": "The API key couldn't be located."`, status 401 | A key is being sent, but it is not a real key | **A key is set but wrong** |
| `"title": "An unknown error has occurred."`, status 500 | The bearer is empty — the variable resolved to nothing | **A key is set but wrong** |

Resolve this once per session. Having seen a project object, send no `Authorization` header of your
own for the rest of the session.

## No key yet

If the user has not named a project, ask, and wait. Pick no project, infer none from open files or
earlier turns, and read no guides to narrow it down. Ask which project, and whether they would rather
register the key with the server or paste it in chat.

Offer the better option first:

- **Preferred:** they put the key on the server registration, so it stays out of the chat. They
  create the key under **Configuration → API Keys** in ReadMe, then follow **Registering the key**
  below.
- **Otherwise:** they paste it and you send it as a header on each call:

  ```json
  {
    "title": "ReadMe API",
    "harRequest": {
      "method": "get",
      "url": "https://api.readme.com/v2/projects/me",
      "headers": [{ "name": "Authorization", "value": "Bearer rdme_..." }]
    }
  }
  ```

  This works, and it also puts the key in the transcript. Say so, and tell them to rotate it.

Send a header of your own **only** when the probe returned `Missing Security Schemes`. A header on the
server registration overrides anything you set in `harRequest`, so against a registered server a
pasted key is silently ignored and the call lands in whichever project the registration owns — no
error, just the wrong project.

## A key is set but wrong

Both failures mean an `Authorization` header is reaching the API and the API is rejecting it. The
usual cause is the registration referring to an environment variable the client resolved to nothing,
or passed through as literal text, because the variable is unset where the client launched from:

- **Status 500, `An unknown error has occurred.`** — the header arrived empty.
- **Status 401, `The API key couldn't be located.`** — a value arrived, but no such key exists.
  Also what a revoked or mistyped key returns.

Say that plainly before asking them to paste anything. Ask them to confirm the variable is exported
in the environment the client launched from, then reconnect as the **Registering the key** row for
their client describes. If the key is genuinely gone, they create a new one under **Configuration →
API Keys**.

Do not work around either failure by probing with `curl` or by retrying against the `Legacy API`
spec. One key maps to one project; if the call reaches the wrong project, the registration is the
thing to change.

## Registering the key

On Cursor, set the plugin variable. On Claude and Codex, registering a `readme` server of their own
replaces the plugin's anonymous one. The server name stays the same, so the skills and tools keep
working.

Find the row for the client you are running in. If you cannot tell which one that is, ask the user —
the wrong row sends them to a config file their client never reads.

| Client | How |
| --- | --- |
| Claude Code | `export README_API_KEY=rdme_…`, then `claude mcp add --scope user --transport http readme https://docs.readme.com/mcp --header 'Authorization: Bearer ${README_API_KEY}'`. Keep the single quotes: the variable is expanded when Claude Code starts, so the key never lands in a config file. Restart afterwards |
| Codex, and the ChatGPT desktop app that shares its config | `export README_API_KEY=rdme_…`, then `codex mcp add readme --url https://docs.readme.com/mcp --bearer-token-env-var README_API_KEY`. Codex reads the variable at startup, so the key never lands in a config file. Start a new session afterwards |
| Cursor | Open **Customize**, find **ReadMe**, and set **ReadMe API key** under **Plugins → Configure** (also the install prompt). Create the key under **Configuration → API Keys**. Restart if the server was already connected. Do not also add a `readme` entry in `~/.cursor/mcp.json`: a user-level server with the same name overrides the plugin, including a blank or `${env:README_API_KEY}` header that never resolved |
| Claude Desktop, Cowork, claude.ai, ChatGPT web | Not possible. The connector is read-only on these surfaces and cannot take a key. Say so, and offer to carry on in a CLI or editor |
