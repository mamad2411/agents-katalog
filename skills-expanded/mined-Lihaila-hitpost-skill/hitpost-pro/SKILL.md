---
name: hitpost-pro
description: Run HitPost (lihaila.si) from your AI agent. It writes X (Twitter) posts, threads, long posts and X Articles from live research (Grok reads what X is saying this week, Brave checks the web and news), polishes drafts with a blind multi-model judge, and posts them to the user's own X account. Uses the user's HitPost account and credits through an API key. Use it whenever the user has a HitPost account or key, mentions HitPost Pro, or wants live X research, an X Article, or a post published to X from the agent, even if they don't say "HitPost".
---

# HitPost Pro

This skill runs the real HitPost pipeline on the user's HitPost account. You don't write the posts yourself here: HitPost researches live and writes them, and you help the user choose, polish and post. You're working for the user, so the posts go to **their own followers**.

Everything goes through one script, `scripts/hitpost.mjs` (Node 18+, no dependencies). It prints JSON and sends progress to stderr. Run it as `node <skill-dir>/scripts/hitpost.mjs <command>`.

## Accounts, credits and keys

- HitPost is for **blue-check X accounts**. The user signs in with X at lihaila.si, then creates a key under **account menu → Use in AI agents**.
- New accounts get free credits once. After that, they **top up with Stripe on the website** (account menu → Top up). Credits are shared between the site and this skill.
- **Costs:** a craft (live research plus three drafts, or one X Article) uses 1 credit. Optimize and format are free within a daily allowance. Posting is free, except that a post containing a link uses 1 credit.
- A craft that fails on HitPost's side is refunded automatically.

## First use

Run `me`. If it exits with code 2, the JSON's `action` says what the user has to do. Tell them in plain words and stop until they've done it:

| action | Tell the user |
|---|---|
| `create_key` | Sign in with X at lihaila.si, open the account menu → **Use in AI agents** → **Create a key**, and paste the key here. Then run `login <key>`. The key is saved to `~/.config/hitpost/key`, readable only by them. |
| `blue_check` | HitPost needs a blue-check X account (X Premium; Basic doesn't include a check mark). |
| `top_up` | They're out of credits: top up at lihaila.si → account menu → **Top up**, then try again. |
| `reconnect_x` | X access expired: sign in with X again at lihaila.si. |

Never ask for, or handle, their X password or card details. Sign-in and payment happen only on the website.

## Writing posts: craft

```bash
node hitpost.mjs craft --idea "<the user's idea, in their words>" [--format single|thread|long|article] [--tone auto|insight|story|bold|funny|pro] [--lang auto|en|zh|…]
```

- **Format:** `single` is the default. Use `thread` for "thread" or 🧵, `long` for a long Premium post, and `article` for an X Article. Tone and language default to `auto`.
- **Pass the idea as the user wrote it.** HitPost decides on its own whether the idea needs research.
- **Tell the user before running it** that a craft takes about 1–2 minutes and uses 1 credit. Show the balance from `me` if you have it.
- **The result:** `craftId`, `research` (what X is saying, angles, top posts and sources), and `variants`. Each variant has `angle`, `why` and `posts`. An article variant has `titles` and a Markdown `body` instead.
- **Show the user** each variant's angle and full text, plus a short "What HitPost found" from `research` with the source links, and the remaining `credits`.
- **Keep the draft text exactly as HitPost returned it**, unless the user asks you to change it.

## Polishing: optimize (free, daily allowance)

Write the posts to a JSON file (an array of strings, one per post), then run:

```bash
node hitpost.mjs optimize --posts posts.json --craft <craftId>
```

DeepSeek and Qwen each rewrite the draft, and Grok scores all versions blind on hook, clarity, value, shareability and how human they sound. Show the winner with its scores and notes, and the other versions in case the user prefers one. Pass `--craft` whenever the draft came from a craft, so the rewrites use its research.

`format --posts posts.json --mode emojis|bullets` adds a few emojis or turns the posts into bullets. The wording stays the same.

## Posting: post

```bash
node hitpost.mjs post --posts posts.json [--craft <craftId>] [--variant <id>]
```

Posting publishes to the user's X account. It's public and hard to take back, so:

1. **Show the exact text** that will be posted, every post of the thread, and **ask for a clear yes**. Approval to post one draft doesn't carry over to the next.
2. If any post contains a link, say that it uses 1 credit per post with a link. Offer to remove the link and keep the source name instead.
3. After posting, give the user the link to each post from `posted`.

The limit is 50 posts a day, counting every post of a thread. Images, replies and likes aren't available through the skill; those stay on the website.

## When something fails

- Exit code 2 means the user has to act: see the table above.
- Exit code 1 is an error. Show the `error` message. A failed craft refunds its credit, so suggest trying again in a minute.
- Don't retry a craft automatically, because each run uses a credit.
