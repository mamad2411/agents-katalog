---
name: schedule-social-posts
description: Schedule Social Posts. Queue approved LinkedIn, X, Threads, Bluesky, Instagram, TikTok and YouTube posts through Buffer, with a first comment on LinkedIn and Instagram or a reply thread on X, a per-channel daily cap, and drafts by default so nothing fires until the owner approves the exact text. Also lists the queue, shows open days and pulls post analytics. Use when the user wants to schedule or queue a post, add a link or hashtags as a first comment or X reply, check what is scheduled, find a free slot, or see how scheduled posts did. Buffer is optional. Without a Buffer token it hands over each approved post ready to paste by hand, free.
---

# Schedule Social Posts

Method by Federico De Ponte.

The scheduler is the last step of the content machine: a post reaches it only after it passed `post-draft-gate` and the owner approved the exact text. For finished vertical reels, `reel-machine` has its own scheduler with a pace check; this skill is for text, image, carousel and link posts.

## Setup (optional, once, by the user)

No Buffer? Skip setup. `schedule` then sends nothing and prints the post (channel, time, text, first comment) for the user to paste by hand. Never stop or ask for a token because Buffer is missing.

With Buffer:
1. Connect the channels in Buffer (buffer.com).
2. Create an API token in Buffer's settings and export it in the user's own terminal or secret manager as `BUFFER_TOKEN`. Never ask for the token in chat, never put it in a command argument, a file in the repo or a log.
3. `python3 scripts/buffer_posts.py channels` lists the connected channels with handle and id.

Buffer's API has a daily request budget per token. Each command costs 2 to 4 requests; do not poll.

## Approval rule

- `schedule` saves a **draft** in Buffer unless `--armed` is passed. Draft first, show the owner the text, the channel and the time, then arm it.
- A general "post the launch stuff this week" is not approval of a specific text. Arm only text the owner has seen.
- There is no publish-now command. A post always goes into a slot at least 10 minutes ahead. "Post now" means: the next open slot, shown to the owner.
- If the text changes after approval, it needs approval again.

## Commands

```bash
python3 scripts/buffer_posts.py channels
python3 scripts/buffer_posts.py queue --days 14
python3 scripts/buffer_posts.py slots --channel <handle> --days 14 --cap 1
python3 scripts/buffer_posts.py schedule --channel <handle> --text-file post.txt \
    --at 2026-11-03T08:00:00-08:00 --comment "link or hashtags" --dry-run
python3 scripts/buffer_posts.py schedule ... --armed      # only after the owner approved this text
python3 scripts/buffer_posts.py delete --id <postId>
python3 scripts/buffer_posts.py analytics --days 30
```

- `--at` takes a time with its timezone offset. Use the owner's timezone; say the time in it.
- `--comment` goes where each platform supports it: LinkedIn, Instagram and Facebook get a real first comment; X, Threads, Bluesky and Mastodon get a reply in a thread under the post. Repeat `--comment` for a longer X thread.
- `--image` takes one public https URL, or several separated by commas for a carousel. `--video` takes one public https URL. Buffer has no upload: it fetches the file when the post fires, so the URL must stay reachable until then.
- Instagram posts get a type automatically (reel for video). YouTube needs `--title`.
- `--dry-run` prints the exact request and sends nothing.

## Cadence

- `--cap` is the most posts per channel per calendar day (UTC); default 1. Drafts count as taken, because a draft is a reservation the owner may arm later.
- `schedule` refuses a day that is full and points to `slots`. Never raise the cap on the owner's behalf.
- The check reads Buffer's queue only. If the owner also schedules on the same account with another tool, those posts are invisible here: ask, and count them by hand.
- Before moving or replacing any post, read its text for dates and words like today, tomorrow, this week or an event name. A date-bound post stays on its day.

## After posting

`analytics` reports Buffer's aggregated metrics per channel. Add the per-post numbers to the `post-signals` sheet so the next idea comes from what actually worked.
