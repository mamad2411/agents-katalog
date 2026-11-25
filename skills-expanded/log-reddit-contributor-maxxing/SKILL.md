---
name: log-reddit-contributor-maxxing
description: "Contributor maxxing: finding talented builders through what they share. A log play (docs/useCases/reddit/contributorMaxxing.md): Find talented people who are into the same things as the owner, through the GitHub repos they post on Reddit. Read a subreddit's last few days through the owner's Reddit account, keep the posts that link to GitHub, and rank them. It reads only. It posts, votes and messages nothing."
when_to_use: "Use when matt asks for this, in words like: \"contributormaxxing\", \"find talented people who are out there who are interested in the same things that we're interested in\", \"use our reddit to load up gotomarketengineering\", \"find people who are posting on github inside of that subreddit\", \"find me all of the best githubs that have been posted in the past 7 days\""
metadata:
  summary: "Contributor maxxing: finding talented builders through what they share"
---

# Contributor maxxing: finding talented builders through what they share

This is the log play `reddit/contributorMaxxing`. Before anything else, call the log MCP tool `getGuide({ useCase: "reddit/contributorMaxxing" })`: it returns this page and makes it the session's play, so every log tool's answer says which step you are on and a send with no play loaded is refused (rules 157, 158). Then follow the steps in order.

Draft every message from that person's own thread and matt's real replies (`voice` with no text, `search`), never from memory, and never send two that read alike (`sameAsSent`).

Find talented people who are into the same things as the owner, through the GitHub repos they post on Reddit. Read a subreddit's last few days through the owner's Reddit account, keep the posts that link to GitHub, and rank them. It reads only. It posts, votes and messages nothing.

How the owner asks for it: "contributormaxxing", "find talented people who are out there who are interested in the same things that we're interested in", "use our reddit to load up gotomarketengineering", "find people who are posting on github inside of that subreddit", "find me all of the best githubs that have been posted in the past 7 days"

## Run it from a fresh context

Say: **"go on docs/useCases/reddit/contributorMaxxing.md for r/<subreddit>"**. The agent reads this page and runs the steps.

## The steps


| # | Step | Tool | Done when |
| --- | --- | --- | --- |
| 1 | Check the owner's Reddit account still has its session | `redditSessionCheck` { account } | Reddit's own answer says loggedIn; anything else is said to the owner and nothing more runs |
| 2 | Find the subreddit the owner named (he may spell it loosely: "gotomarketengineering" is r/gtmengineering) | `redditReadSubreddits` { account, query }, or `tregCall` { id: "tinyfish.web.search", include_domains reddit.com } (free) when the account can't read | one subreddit, named with its link and what it's about |
| 3 | Read its posts back the days asked, keeping only the ones that link to GitHub, ranked by score then comments | `redditReadPosts` { account, subreddit, days: "7", linksTo: "github.com" } | each post with its author, score, comments, date, Reddit link and GitHub links; a 429 or reset stops the read and keeps what was read (rule 94) |
| 4 | Find who else builds on the same internals: search GitHub's code for the internal Reddit API names `vendor/reverseChud` uses (`svc/shreddit/token`, `svc/shreddit/search-typeahead`, `gql-fed.reddit.com` ...), about 7 s apart, then read each repo and its owner in parallel. Reddit is never called again for this | `gh api search/code`, `gh api repos/<repo>`, `gh api users/<login>` | every repo with the names it uses, stars, last push, and its owner's name, bio and X handle, saved in `RESEARCH/CONTRIBUTOR_MAXXING/` |
| 5 | Show the owner the list, best first: the Reddit posts, then the repos closest to ours (most rare names), each with the person behind it | the answers from steps 3 and 4 | the owner has every repo with the person behind it |

## What the runs taught

- **r/gtmengineering is the GTM engineering subreddit** (found 2026-11-08 by TinyFish search). r/GTMbuilders ("GitHub commits over slide decks") sits next to it.
- **Reddit's whoami can pass while its token step fails.** On 2026-11-08 `/api/me.json` answered for the account, then loading reddit.com gave no `token_v2`, then the engine's connection was reset twice while plain HTTPS to Reddit still worked. That is a refusal: stop, tell the owner, and don't read again until he says so.
