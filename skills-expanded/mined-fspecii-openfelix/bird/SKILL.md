---
name: bird
description: Post, read, search, and reply on X (Twitter) using your browser cookies — no API key required.
metadata: {"openclaw":{"emoji":"🐦","requires":{"bins":["bird"]},"os":["darwin"],"install":[{"kind":"node","package":"@steipete/bird","bins":["bird"],"label":"Install bird via npm"}]}}
---

# bird

Use `bird` to interact with X (Twitter) via your existing browser session.

## Auth setup

Bird reads cookies from your browser automatically (Firefox or Chrome).
Run `bird check` to verify authentication sources are working.

For headless use, set `SWEETISTICS_API_KEY` or pass `--engine sweetistics`.

## Reading

```bash
bird whoami                          # show authenticated user
bird read <url-or-tweet-id>          # read a single tweet
bird thread <url-or-tweet-id>        # read full thread
bird timeline -n 20                  # home timeline (default 10)
bird mentions -n 10                  # your mentions
bird search "query" -n 5             # search tweets
```

## Posting (always confirm with user first)

```bash
bird tweet "text"                    # post a tweet
bird reply <id-or-url> "text"        # reply to a tweet
```

## Rules

- Always confirm with the user before posting, replying, or any write action
- Never post on behalf of the user without explicit confirmation in the conversation
- Use `bird check` first if auth errors occur
