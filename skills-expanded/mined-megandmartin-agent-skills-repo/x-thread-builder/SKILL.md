---
name: x-thread-builder
description: Builds an X (Twitter) thread — one scroll-stopping opener, 5–9 self-contained body tweets, a CTA close — with a python3 character-count check on every tweet. Use when the user asks for an "X thread", "Twitter thread", "thread about [topic]", "tweetstorm", or wants long-form content broken into tweets. Don't use for single tweets (draft directly), LinkedIn posts (linkedin-content-pack), or fanning one piece across many platforms (content-repurposer).
version: 1.0.0
author: Gen AI Hub
license: MIT
metadata:
  hermes:
    tags: [Content & Marketing, X, Twitter, Threads, Social]
    related_skills: [linkedin-content-pack, brand-voice-guardian, content-repurposer]
---

# X Thread Builder

Builds threads where every tweet earns its place: an opener that stops the scroll on substance (not bait), 5–9 body tweets that each stand alone when quoted out of context, and a close with one clear CTA. Every tweet is machine-verified under 280 characters before delivery. Output is always a draft — nothing gets posted.

## When to Use

- The user wants a thread from a topic, article, brief, or set of notes.
- A `deep-research-brief` or long-form piece needs an X-native breakdown.
- **Not for:** single tweets (draft directly), LinkedIn posts (`linkedin-content-pack`), or fanning one piece across many platforms (`content-repurposer`).

## Quick Reference

| Action | Command / Call |
|---|---|
| Count one tweet | `python3 -c "print(len('''TWEET TEXT'''))"` |
| Count whole thread | Write tweets to `/tmp/thread.txt` separated by `---`, then run the step 5 script |
| URL length rule | Any URL counts as 23 chars regardless of actual length |
| Thread size | 1 opener + 5–9 body + 1 close = 7–11 tweets total |
| Numbering | `2/` style on body tweets; opener unnumbered or `1/` |

## Procedure

1. **Precheck** — confirm `python3` is available (`python3 --version`). Confirm you have the source material, the audience, and the one thing the reader should do at the end (follow, read, reply, sign up). One CTA only — ask if unstated.
2. **Outline** — list 5–9 points, one per body tweet, in an order that builds (setup → payoff, or list of escalating value). Each point must survive alone: assume any tweet may be someone's first contact with the thread.
3. **Draft the opener** — a concrete claim, result, number, or tension in ≤280 chars. It must promise exactly what the thread delivers. Banned: "🧵👇" as the whole hook, "You won't believe", "Most people don't know this", curiosity gaps with no payoff, "A thread on threads".
4. **Draft body tweets** — one idea each, ≤280 chars, self-contained (restate the subject; no bare "It also..." referencing a previous tweet). Line breaks inside a tweet are fine and free. Numbers, specifics, and short sentences over adjectives. No mid-thread hashtags.
5. **Character check (hard gate)** — save the thread to `/tmp/thread.txt` with tweets separated by lines containing only `---`, then run:
   ```
   python3 -c "
   import re
   ts=[t.strip() for t in open('/tmp/thread.txt').read().split('\n---\n')]
   for i,t in enumerate(ts,1):
       n=len(re.sub(r'https?://\S+','x'*23,t))
       print(f'{i}: {n} chars', 'OK' if n<=280 else 'OVER')
   "
   ```
   Expected: every line prints `OK`. Any `OVER` tweet gets trimmed (cut adjectives and hedges first) and the script rerun until clean.
6. **Close with CTA** — final tweet: one-line recap of the payoff + the single CTA + at most one link. Optionally "If this was useful, RT the first tweet" — once, plainly, no begging.
7. **Deliver** — output the template below with the verified character counts shown per tweet. Recommend a `brand-voice-guardian` pass if a voice profile exists. Do not post.

## Output Template

```
# X Thread: [topic]
**Audience:** [who] | **CTA:** [the one action] | **Tweets:** [n]

1/ [opener]  (xxx chars ✓)

2/ [body tweet]  (xxx chars ✓)

...

n/ [close + CTA]  (xxx chars ✓)

## Notes
- [attachment suggestion for tweet 1, if any: image/screenshot/chart]
- [best posting window + timezone assumption]
```

## Pitfalls

- **Eyeballed character counts** — a "looks fine" tweet at 293 chars breaks on posting. Recovery: the step 5 script is mandatory, not optional; rerun after every edit, including "tiny" ones.
- **Dependent tweets** — tweet 4 reads "It also does this" and means nothing when quoted alone. Recovery: reread each body tweet in isolation; restate the subject noun in any tweet that fails the standalone test.
- **Opener overpromises** — hook says "10x your output", thread delivers three mild tips. Recovery: rewrite the opener DOWN to what the thread proves, or upgrade the weakest body tweets with concrete numbers/examples until the promise is honest.
- **Multi-CTA close** — follow me, AND read the blog, AND join the list. Recovery: keep the CTA chosen in step 1; move the rest to a reply-to-self suggestion in Notes.

## Verification

- [ ] Step 5 script run on final text; every tweet printed `OK` (counts shown in output)
- [ ] 7–11 tweets total; each body tweet passes the standalone read test
- [ ] Opener contains a specific claim/number and none of the banned patterns
- [ ] Exactly one CTA in the close; no mid-thread hashtags
- [ ] Delivered as a draft; no posting performed
