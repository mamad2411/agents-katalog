---
name: social-scrape
description: Collect public posts and discussion from X, LinkedIn and Hacker News through a local signed-out browser, then report them in chat or write them to a document. Use when the user wants to scrape, monitor or research specific accounts, topics, hashtags or discussions on social platforms.
---

# Social scrape

Collect what specific accounts and specific topics are actually saying, using the
`subio-scrape` MCP tools, and hand back either a chat summary or a document.

Every read happens in a local browser that is **never signed in**. Say so if the
user asks whether it will touch their account: it does not, it clears session
cookies before every run, and it does not solve challenges or disguise itself as
a human. That is also the reason for the ceiling in step 2 — work within it
rather than around it.

## 1. Find out what to read

If the user already named accounts, a topic or a hashtag, skip straight to step 2.

Otherwise ask with `AskUserQuestion` — one question, these options:

- **Accounts** — specific people or companies on X
- **Topic or hashtag** — a subject, wherever it is being discussed
- **A company** — one organisation across X and LinkedIn
- **Open discussion** — what Hacker News is saying

Then ask for the handles or the topic itself in a normal follow-up question.
Also settle **how far back** (default: last 7 days) and **how many items per
source** (default: 20) unless the user already said.

## 2. Pick the right tool for each kind

This is the part that decides whether the scan works, so read it before calling
anything.

| The user wants | Call | Why this and not something else |
| --- | --- | --- |
| Named X accounts | `x_account_posts` | Signed out, X serves account timelines in full, with exact counts |
| A topic or hashtag **on X** | `x_account_posts` with `match: ["term", "#tag"]` over the accounts likely to discuss it | **X does not serve search, hashtags or explore to a signed-out browser.** There is no search tool because there is no signed-out search. Reading the accounts and filtering is the way |
| A topic, hashtag or discussion generally | `hackernews_search` | Hacker News publishes discussion openly through a real API — no browser, no session, no ceiling |
| A company | `linkedin_page` for the profile, `x_account_posts` for what it posts | LinkedIn's public page carries the firmographics; X carries the posting |
| A company's posts | `linkedin_company_posts` | Best effort — LinkedIn often withholds these signed out |

If the user asks for a topic on X and has not named accounts, say plainly that
signed-out X has no search, propose 5–10 accounts that plausibly cover the topic,
and confirm the list before reading.

Reading is deliberately slow — a few seconds between pages, one page at a time,
in a single reused browser tab. Ten accounts is about a minute. Tell the user
before starting, not after.

The window closes itself a few minutes after the last read, so `browser_close` is
a courtesy rather than a requirement.

## 3. Read the notes, not just the items

Every collector tool returns `{ items, notes, partial }`. **Read `notes`.** A
source that was blocked, walled or challenged reports `FAILED — …` there while
still returning zero items, and zero items is also what a quiet week looks like.

- Never describe a `FAILED` source as quiet. Name it and say what it did.
- `partial: true` means the report is incomplete. Say so in the output.
- A `STOPPED after a block` note means the run ended early and the accounts it
  lists were never read. **Do not call the tool again for them.** Report what was
  collected, name what was skipped, and say the read can be resumed later.
  Retrying a block is what turns a pause into a ban.
- `not-found` on an X handle usually means a typo — X redirects a handle that
  does not exist into its signup flow. Check the spelling with the user rather
  than reading it again.
- If a scrape fails before anything is read, call `browser_status` and report the
  actual setup rather than guessing.

## 4. Deliver

Ask with `AskUserQuestion` whether they want it **in chat** or **as a document**,
unless they already said. Default to chat for one or two sources, document for a
scan across several.

**In chat:** what stood out across sources, then the notable posts grouped by
theme — each with the author, the post's own words, engagement, and a link.
Do not paste every item; select. End with one line on what was collected and any
source that failed.

**As a document:** write a markdown file (default `./scrape-<topic>-<date>.md`)
with a summary at the top, sections per theme, and every item as a bullet with
author, date, engagement and link. Then say in chat what is in it and where.

Whichever way: quote posts as their authors wrote them, attribute every claim to
the account that made it, and keep your own reading of it separate from theirs.

## 5. Close

Call `browser_close` when the scan is done. The window would close itself a few
minutes later anyway, but a user watching it should see it end with the scan.
