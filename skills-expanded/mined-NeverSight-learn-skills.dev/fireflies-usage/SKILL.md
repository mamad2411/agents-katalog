---
name: fireflies-usage
description: >
  Search meeting transcripts and extract action items from Fireflies.ai. Use when checking what
  was discussed on a call, finding a client's meeting notes, pulling action items assigned to the
  team, or getting a transcript summary before campaign work. Triggers on "meeting notes", "call
  transcript", "what did we discuss", "Fireflies", "action items", "meeting summary", "what was
  said on the call". Do NOT use for cold email copy (see cold-email-copy), enrichment/search (see
  coldiq-search-enrich), or campaign work (see campaign-delivery). NOTE: the ColdIQ marketplace
  has no Fireflies endpoint — this skill connects to Fireflies directly via its MCP server.
---

# Fireflies Usage

Pull meeting transcripts, summaries, and action items from Fireflies.ai to ground campaign work
in what the client actually said.

> No ColdIQ substitute: the ColdIQ marketplace does not resell Fireflies, so this skill is the one
> exception that stays on the provider directly. Connect Fireflies through its MCP server (below)
> rather than re-routing through `api.coldiq.com`. There is no `## ColdIQ Marketplace Endpoints`
> table here on purpose.

## Setup (MCP)

Add the Fireflies MCP server to your Claude config, then use its tools — no raw HTTP needed:

```json
{ "fireflies": { "command": "npx", "args": ["-y", "fireflies-mcp-server"],
  "env": { "FIREFLIES_API_KEY": "your-key-here" } } }
```

Available MCP tools: `fireflies_search`, `fireflies_get_transcripts`, `fireflies_get_transcript`,
`fireflies_get_summary`, `fireflies_get_user_contacts`.

> Direct API alternative (if you can't use MCP): Fireflies exposes a GraphQL endpoint at
> `https://api.fireflies.ai/graphql` with `Authorization: Bearer <key>`. Prefer the MCP server.

## How to use

1. **Find meetings** by client name, participant email, date, or keyword → `fireflies_search`.
2. **Get a summary** (action items, key points, overview) → `fireflies_get_summary`.
3. **Get the full transcript** (word-by-word with timestamps) → `fireflies_get_transcript`.
4. **Extract action items** assigned to the ColdIQ team from the summary.

## Use cases for GTMEs

- Before writing copy: pull the kickoff call to extract the client's ICP language, pains, and
  customer stories (feeds [crawford-method](../crawford-method/SKILL.md)).
- Before a QBR: summarize the last N calls for the client.
- Track commitments: extract action items and who owns them.

## Gotchas

- Transcripts can be large — request the **summary** first, the full transcript only when needed.
- Search by participant **email** is more reliable than by name.
- Recent meetings may take a few minutes to finish processing after the call ends.
