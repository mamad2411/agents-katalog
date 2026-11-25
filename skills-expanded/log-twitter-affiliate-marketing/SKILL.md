---
name: log-twitter-affiliate-marketing
description: "Affiliate marketing through your DMs. A log play (docs/useCases/twitter/affiliateMarketing.md): You use a tool, you make content about it, and people message you about it. This page turns those conversations into affiliate income without sounding like a pitch: each person gets a reply about their own thread, an update on what you've built, and the tool with your affiliate credit only where it actually helps them. The other side of the page is the tool companies themselves: getting onto their partner, referral or creator program and booking the call."
when_to_use: "Use when matt asks for: affiliate marketing through your dms."
metadata:
  summary: "Affiliate marketing through your DMs"
---

# Affiliate marketing through your DMs

This is the log play `twitter/affiliateMarketing`. Before anything else, call the log MCP tool `getGuide({ useCase: "twitter/affiliateMarketing" })`: it returns this page and makes it the session's play, so every log tool's answer says which step you are on and a send with no play loaded is refused (rules 157, 158). Then follow the steps in order.

Draft every message from that person's own thread and matt's real replies (`voice` with no text, `search`), never from memory, and never send two that read alike (`sameAsSent`).

You use a tool, you make content about it, and people message you about it. This page turns those conversations into affiliate income without sounding like a pitch: each person gets a reply about their own thread, an update on what you've built, and the tool with your affiliate credit only where it actually helps them. The other side of the page is the tool companies themselves: getting onto their partner, referral or creator program and booking the call.

Inbound and outbound are on other pages: [dmInbox.md](../log-twitter-dm-inbox/SKILL.md) reads who is waiting, [engagerDms.md](../log-twitter-engager-dms/SKILL.md) opens new conversations.

## Run it from a fresh context

Say: **"go on docs/useCases/twitter/affiliateMarketing.md for `<tool>`, link `<affiliate link>`"**. The agent then reads this page and [README.md](https://github.com/matthewdonsemail-lab/log/blob/main/docs/useCases/twitter/README.md) and runs the steps.

## The steps


| # | Step | Tool | Done when |
| --- | --- | --- | --- |
| 0 | Session check | `twitterSessionCheck` | `loggedIn` |
| 1 | Read every conversation, X Chat included, and index it | `searchIndex` { account } (`log search index`) | "N conversations, M messages" and the chunk count |
| 2 | Find the conversations worth a follow-up: anyone who asked about the tool, offered work, a call or a collaboration, or went quiet on an open thread | `search` { query: "<tool> enrichment", with, after } (several queries: the tool, "call", "consulting", "affiliate", "role") | a short list of people and conversation ids |
| 3 | Read each person's whole history before writing a word: the old DM thread and the X Chat thread merged into one timeline | `twitterDms` { account, with: "<handle>" } | you know the last thing each side said, and what was promised |
| 4 | Sort them: **owes you an answer**, **you owe them something** (a doc, a look, a reply), **left hanging**, **competitor** (building a rival tool), **tool company** (their partner program) | a table for the owner | the owner agrees the list |
| 5 | Write one message per person: pick up exactly where the thread left off, one line on what you've built since, then the offer framed as something for them. The link goes only to people who don't use the tool yet, and never to a rival's founder | house style | the owner approves each line |
| 6 | Tool companies: ask for the partner, referral or creator program, show the reach (views, who follows you), and offer two concrete call times in their mornings or a calendar link | `twitterDm` / `twitterDmLive` | a time agreed |
| 7 | Send, dry run first. Two or more people go through the queue as dms | `twitterDm` then `twitterDmLive` { userId, text, approvedBy, confirmLive }, or the README queue with `action: "dm"` | X's answer is `sent` |
| 8 | Watch for replies. The inbox hook flags a new message with its text, X Chat included | the inbox watcher (agent hooks) | each reply read with `twitterDms` { with } before answering |

## What a message looks like

> hey `@someone` sorry this slipped past me. since we spoke i've been building `<what you built>` all in public `<your site>`. you were asking about `<their question>` so this might help, `<tool>` gives you `<credit>` free here `<affiliate link>`

> hey `<partner contact>` the referral route works for me and i'm keen to hop on a call and plan it out. would `<day>` or `<day>` at `<time>` your time work, or send a calendar link and i'll grab a slot

## The lessons that shaped it

- **Read the X Chat side first.** A person's newer messages often live in X's encrypted Chat, not the old DM thread. Replying from the old thread made the account apologise for "sorry this got buried" to people it had already had calls with. `twitterDms` with `with` merges both; never answer without it.
- **If a reply missed the context, own it at once:** one line of apology, the real context in your own words, then the actual follow-up (the doc you owe, the video they haven't watched, the role they already turned down).
- **Collaboration, not a pitch.** The link is the last line, for people who'd use it. A rival's founder gets an honest "i'll try yours", never your link.
- **Partner programs move on proof.** Views, signups you drove and who follows you (decision makers) beat follower counts. When the affiliate program is paused, ask for the referral fee and a call.
- **Keep the promises visible.** Anything you said you'd send goes into the owner's list so it isn't lost the next time.

## What to know

- X Chat opens with the account's X Chat PIN, saved once in a masked terminal prompt (`log twitter chat pin --account <account>`). Without it, X Chat messages show who and when, not what.
- Every DM counts as a write against the account's 240 a day. `--force` goes past it only when the owner says so.
- A DM only lands if the person accepts DMs from accounts they don't follow.

## Next

- [#35](https://github.com/matthewdonsemail-lab/log/issues/35) tracks which affiliate link went to whom and which turned into a signup, per person, in Twenty.
