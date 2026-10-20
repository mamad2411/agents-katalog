---
name: grok-server-tools
description: xAI's server-side search — live X (Twitter) search and web search from Grok, both via the API and natively inside Caeros. Use when the user wants Grok to ground answers in current X posts or web results.
---

# Grok Server-Side Search

xAI runs search on its own infrastructure: declare it in the request and
Grok searches X and the web while generating — no client-side loop.

## What it does

- **X search**: live and historical posts on X — the data moat; no other
  provider has native X grounding. Results come back cited.
- **Web search**: general web grounding for current events.

Every current Grok model can drive X search. Use it for anything where the
answer lives on X (breaking news, developer sentiment, market chatter) or
changed after the model's training data.

## Via the API

Server-side search is enabled per-request on the Responses API. Parameter
shapes evolve quickly — fetch https://docs.x.ai for the current request
schema instead of guessing field names. Treat results as sourced data: keep
citations, don't restate engagement numbers the response didn't include.

## Inside Caeros (native)

Caeros integrates xAI's X search natively. Once an xAI key is configured in
Settings → Models:

- Grok models (Grok 4.6, Grok 4.5, Grok Build) appear as selectable lanes.
- X search runs as a server tool on those lanes — you'll see "Searched X" in
  the transcript when it fires.

So for "what is X saying about ..." inside Caeros you have two paths: the X
plugin (your own X account via X's MCP: timelines, bookmarks, full-archive
search) or a Grok lane with server-side X search (no X account needed,
citation-style results). Prefer the X plugin when the user's own account
data matters; prefer Grok search for quick grounded answers mid-conversation.

## Practices

- Cite the posts (links) rather than paraphrasing them into unsourced fact.
- Search costs tokens and latency — one well-scoped search beats several
  vague ones.
- For deep X research workflows (threads, bookmarks, folders), hand off to
  the X plugin's skills.
