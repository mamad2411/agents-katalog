---
name: tweetytweets
description: Use when automating posts to X/Twitter end to end.
version: 1.0.0
license: MIT
metadata:
  hermes:
    tags: [twitter, x, social, content, automation, research]
    related_skills: [humanizer]
---

# tweetytweets

An autonomous X/Twitter posting pipeline: it finds the day's material itself,
writes posts in **your** voice, publishes them through a real logged-in browser,
and proves each one actually went live.

No X API key. No developer account. No paid scraper. One Python dependency.

```
research  ->  plan  ->  schedule  ->  publish  ->  verify
```

**Nothing here posts anything until you finish Step 0 and explicitly turn the
schedule on.** Do not skip the interview - the whole point is to sound like the
user, not like a content bot.

---

## STEP 0 - THE ONBOARDING INTERVIEW (do this first, always)

Run this as a conversation. Ask the questions, wait for real answers, then write
them into `config.json`. Do not invent answers, and do not proceed on defaults
the user never saw.

### 0.1 Load their voice — ASK FOR THEIR BEST POSTS

**This is the most important step.** Ask, in these words or close to them:

> "Give me 5-20 of your best-performing posts — ideally ones with **100k+
> impressions**, or simply the ones you're proudest of. Paste them raw, include
> the line breaks, and separate each post with a line of `---`. If you have them
> with impression counts, include those too.
>
> I'm not copying them. I'm measuring how you actually write: how you open, how
> long you go, whether you use numbers or questions, what you talk about. Without
> this, anything I write will sound like a generic AI account."

Also ask, if they are willing:

> "Name 2-3 accounts in your space whose posts you admire. Paste 3-5 of their
> posts too — I'll treat those as *structure* references, never as voice."

Then:

1. Save the pasted posts to `scratch/my_top_tweets.txt` (one post per block,
   `---` between them).
2. Run `python scripts/voice_profile.py --in scratch/my_top_tweets.txt`.
3. Read the output *with* them and confirm it matches reality. If the tool says
   "median 138 chars, 3 beats, 4/5 posts lead with a number" and they say "yeah,
   that's me", you have a voice profile. If not, ask what's missing.
4. Write `references/voice-profile.local.md` (git-ignored) containing:
   - the measured stats, verbatim
   - the hook patterns, with 3 real examples of their own
   - their recurring topics, in their own words
   - explicit **do-not** list: words, formats and personas they never use
   - a short "sounds like" paragraph you write, then let them correct

**Every draft from now on is written against that file.** If it is missing, stop
and ask for the posts again rather than guessing at a voice.

### 0.2 The rest of the interview

| Ask | Why it matters | Goes to |
|---|---|---|
| "What's your handle?" | the account guard refuses to post as anyone else | `handle` |
| "Is this account on X Premium, or free? (Not sure is fine.)" | The ceiling decides what content is possible and it **differs per account** — free caps at 280, Premium does not. Ask, then **verify by measuring**: `python scripts/post.py measure --save`. Never hardcode a number. | `premium`, `max_chars`, `max_chars_verified` |
| "What do you post about, in your own words?" | drives research queries and topics | `x_queries`, `subreddits`, `feeds` |
| "What timezone are you in, and when do you want to post?" | slots are local time | `timezone`, `slots` |
| "How many posts a day?" | more is not better — a second post in the same feed only counts 62% | `slots` |
| "Do you want a daily news roundup post?" | the one repeating format; gets its own counter | `ai_update_*` |
| "Anything you never want to say or do?" | bait, politics, emoji, DMs — record it in the voice profile | do-not list |
| "Do you use X on your phone as well?" | replies from mobile raise the post count and will confuse a naive verifier | note it |

### 0.3 Then, in order

```bash
cp config.example.json config.json     # then fill it from the interview
pip install -r requirements.txt
python scripts/doctor.py               # fix anything MISSING before continuing
python scripts/doctor.py --live        # network + browser check
python scripts/browser.py launch       # starts the automation browser
#   -> sign in to x.com IN THAT WINDOW. Use "Email or username", not
#      "Continue with Google", which can silently create a SECOND account.
python scripts/post.py check           # must print your handle
python scripts/post.py measure --save  # measures THIS account's ceiling and stores it
python scripts/post.py limits          # confirm: shows the limit + whether it's verified
```

Do **one** supervised post before scheduling anything:

```bash
python scripts/post.py compose --text "your first real post" --dry-run
# look at shots/compose.png, confirm the text and the account
python scripts/post.py post --text-file scratch/first.txt
python scripts/post.py shot --what profile     # then LOOK at shots/profile.png
```

Only after a real post has gone out and been verified should you set up the
schedule (see README.md → Scheduling).

---

## HARD RULES

These are not style preferences. Breaking them gets posts ignored, or the account
actioned.

1. **Never hardcode a character ceiling - it belongs to the user's account.**
   Free tiers cap at 280; Premium does not. The ceiling decides what content is
   even possible, so it gets **asked for and then measured**, never assumed:
   1. ask the user whether the account is on Premium (free / Premium / not sure)
   2. run `python scripts/post.py measure --save` — it types into the composer and
      reads the Post button's state; **it never clicks Post, so it cannot publish**
   3. that writes `max_chars` + `premium` + `max_chars_verified` into config.json
   `post.py limits` reports what is configured and whether it is verified;
   `settings.limit()` returns `verified: false` when it is not, and both `due.py`
   and `doctor.py` will warn rather than quietly assume. Until it is measured the
   tool falls back to the free-tier minimum, so a long draft gets trimmed instead
   of a post failing at publish time.
1b. **A high ceiling is permission, not instruction.** Length is not the goal and
   never fill the limit: if one sharp idea fits in two sentences, ship two
   sentences - that is a finished post. Vary length deliberately across posts.
   Longer is justified by more substance, never more words.
2. **No engagement bait.** No "like + comment X and I'll DM you", no "must be
   following", no follow-for-follow. X's own ranking notes single out engagement
   bait as the one category where even big accounts get no pass. If the user asks
   for it, show them that and let them decide — but do not add it silently.
3. **No fabricated numbers, results or quotes.** Every figure in a post must
   trace to a source the agent actually read. If it can't be verified, drop the
   post, not the standard. This is the rule that separates this from the spam
   accounts.
4. **Never post the same text twice**, and never post several times back to back.
5. **The account guard is absolute.** If the signed-in handle is not the
   configured one, refuse and say so. Check before every single post.
6. **The daily roundup number comes from `post.py day`**, never hand-counted. It
   advances only when that post verifies, so a missed day burns no number.

## WHAT THE ALGORITHM ACTUALLY REWARDS

Worth reading before writing anything. Current weights (from X's published
source):

- A tap is worth 0.3. **Staying 10+ seconds after the tap is worth 0.4.** So the
  body must pay off the hook — clickbait got weaker, delivered value got stronger.
- "Not interested" costs about -47. Never write something your audience wants to hide.
- **Original posts are the only thing that reaches non-followers.**
- A copy-link share is the largest single signal (20). A DM share is 5.
- A post that wins a follower is worth 4.
- Your second post in the same feed counts only 62% — 3 good posts beat 8 filler ones.
- Under 1,000 followers there is a lift toward ~16th in a stranger's feed. Use it
  while you have it.
- Don't chain-reply to yourself, don't stuff hashtags, don't tag strangers.

## THE DAILY FLOW

1. `python scripts/research.py collect --hours 36` → `swipe/<date>.json`
2. Pick stories — prefer real engagement and **read the actual source** before
   making any claim about it (`web_extract`, or curl the page).
3. Write each post against `references/voice-profile.local.md`, then check the
   length. Rule of thumb: one idea, short lines, blank line between thoughts,
   hook in the first 6-8 words, end on the payoff.
4. `python scripts/due.py fill --slot 13:00 --file scratch/x1.txt` for each slot
   (it rejects anything over the limit, so you learn now rather than at post time)
5. The schedule publishes each slot. Then **verify by looking**:
   `python scripts/post.py shot --what profile`, then read `shots/profile.png`
   with a vision tool and confirm the topmost post is the text you wrote.

## PITFALLS ALREADY PAID FOR

Do not relearn these the hard way.

- **Creating a CDP target on `about:blank` then `Page.navigate` drops the
  websocket** ("no close frame received or sent") on heavy pages like X and
  Reddit. Create the target with the final URL.
- **`Input.insertText` is the only way to fill the composer.** Setting `innerText`
  leaves React state stale and the Post button disabled forever.
- **The profile timeline renders stale for up to a minute after sending.** A real,
  successful post was once reported as failed because the read-back ran 6 seconds
  too early and saw a five-month-old post. Always poll the read-back.
- **A green "Your post was sent" toast is not proof.** Read the profile back.
- **Screenshot the viewport, not the whole page**, for anything a vision model
  must read — a tall image gets downscaled into illegibility, and a vision model
  has been observed claiming a composer was empty (quoting its placeholder) while
  simultaneously reporting the Post button as enabled.
- **On a profile, scroll the newest post into view AND back off ~110px.**
  Otherwise the screenshot stops above the timeline, or the post's first line —
  the hook — hides under the sticky header.
- **Vision is reliable for post text, line breaks and whether a link card
  rendered. It is NOT reliable for numbers.** It has misread a profile's post
  count and invented navigation items. Never let a vision reading override the
  DOM or `state.json` for counts.
- **A rising post count is often a REPLY from the user's phone** — replies don't
  appear in the Posts tab. Check before assuming something posted itself.
- **Never drive the user's everyday browser profile.** Only the dedicated one.
- **Don't name a file in `scripts/` after a Python stdlib module** — the script
  directory is on `sys.path`, so `inspect.py` or `queue.py` silently breaks imports.

## FILES

```
scripts/   settings.py browser.py research.py post.py due.py voice_profile.py doctor.py
config.json         your install (git-ignored); config.example.json is the template
state.json          the ledger: every post, its URL, whether it verified
swipe/  drafts/  shots/  scratch/
references/voice-profile.local.md   your measured voice (git-ignored)
README.md           full setup, scheduling and troubleshooting
```

Full documentation — including how to wire the schedule with a monitor so idle
ticks cost nothing, and the cost model — is in **README.md**.
