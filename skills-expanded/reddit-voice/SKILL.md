---
name: reddit-voice
description: >
  Sample what a subreddit actually upvotes and write in that register, so a post doesn't read as
  machine-written. Use before drafting any Reddit post or comment, and whenever someone asks how to
  write for a specific subreddit, why their post got downvoted, how to sound less like AI, how to
  match a community's tone, or what format a subreddit expects. Also use when a post was
  rule-compliant and well-targeted but still flopped — that is usually a register problem, not a
  targeting one. Measures title shape, body formatting, comment length, distinctive vocabulary, and
  recurring phrases from live top posts, then hands the raw samples over for judgement. Research and
  drafting only; it never posts.
---

# Writing in a subreddit's register

A post can be on-topic, correctly flaired, rule-compliant, and still get downvoted for how it
reads. That happened to this project: a well-targeted announcement drew *"Even your title reeks of
the AI sentence construction"* and settled at score 0. Targeting was fine. Register was wrong.

Existing tone skills derive a voice from **your** brand — a questionnaire, a guidelines file. This
derives it from **the community's own top posts**, because that's the thing you actually have to
match.

```bash
node scripts/rdtx.mjs voice ai_agents --sample 20 --sort top --time month
```

## Verify the installed runtime without Reddit

Run `node scripts/verify-synthetic.mjs` with no arguments. It sends fabricated posts and comments
through the production aggregation contract, confirms that post and comment registers remain
separate, and proves the verifier does not emit its source-text canary. It makes no Reddit request.
A pass proves aggregate behavior only; it does not evaluate a live community or the quality of a
draft written from real samples.
Overall `passed` is the AND of all five shared checks; inspect `functional.reddit_voice` for this
skill's evidence.

An independent tester can submit the exact named verifier result through the
[structured installed-run report](https://github.com/L4A-ai/reddit-skills/issues/new?template=reddit-skill-installed-run.yml).
Select the `reddit-voice` zero-input synthetic option only after running the installed copy. This
proves installation and aggregate-register contracts, not live community fit or writing quality.

Live sampling requires Node.js 18+, `agent-browser`, and the user's own logged-in Chrome profile;
see `references/browser-session.md`. The synthetic verifier needs only Node.js 18+.

## What comes back, and why each number matters

| signal | what it tells you |
|---|---|
| `self_post_pct` | **Check this first.** Some subreddits are almost entirely link posts; a text post there is wrong on format before anyone reads a word. |
| `pct_first_person` | Whether the community writes "I built" or describes things impersonally |
| `pct_headers` / `pct_bullets` / `pct_bold` | The strongest AI tell. Heavy markdown structure in a subreddit that writes plain prose reads as machine output. |
| `median_chars` (title, body, comment) | Length expectations, which differ far more between subreddits than people assume |
| `distinctive_words` / `recurring_phrases` | Shared vocabulary and running references — the closest programmatic proxy for in-jokes |
| `samples` | The actual titles, openings, and top comments. **These matter more than the statistics.** |

## Three real profiles, measured the same day

```
r/ai_agents    60% first-person   5% headers   0% bullets   body ~1400ch
               titles are opinions: "Trucking's gonna be fully automated in like
               2-3 years. I'm not even joking."

r/cli          0% SELF-POSTS      titles ~53ch, 55% use a colon or dash
               showcase culture: "Made a terminal-style text-only social network
               like it's 1987 :)" — the artifact is the post

r/SideProject  80% first-person   50% headers   50% bullets   body ~1400ch
               personal-story framing: "I built a speed/distance tracker for my
               hamster wheel"
```

Same topic, three incompatible formats. Structure that reads as effort in r/SideProject reads as
AI slop in r/ai_agents, and neither belongs in r/cli, where you post the thing itself.

## How to use the output

Read the samples, then write. Do **not** compute an average and imitate it — that produces a
different flavour of synthetic. Specifically:

1. **Match the format before the words.** Self-post vs link post, and the formatting percentages.
   Getting this wrong is unrecoverable.
2. **Steal the opening move, not the sentences.** Notice how top posts start — a claim, a result, a
   complaint — and open the same way with your own material.
3. **Write at their length.** A 1400-character community will not read your 4000-character post.
4. **Use their nouns.** `distinctive_words` is the vocabulary the community actually uses; borrowed
   jargon from elsewhere marks you as an outsider.
5. **Lead with the finding, not the tool.** In every sample set, the top posts share something
   useful on its own terms. A post whose payload is "I made a thing" ranks below one whose payload
   is "here's what I learned", even when they describe the same work.

## Tells to strip

These correlate with the downvoted-as-AI reaction and are worth removing on sight:

- Bold-headed sections in a subreddit that writes prose
- Tricolon everywhere — "faster, cleaner, and more reliable"
- "It's not X, it's Y" and "Here's the thing:" constructions
- Em-dash-heavy sentences stacking three clauses
- A tidy summary paragraph that restates what was just said
- Hedged conclusions where the community states opinions flatly

## Honest scope

This helps you write *appropriately for a community* — the same thing a person does when they read
a room before speaking. It does not make promotional content welcome where promotion isn't welcome,
and it will not rescue a post with nothing to say. If the sampled community rewards genuine
findings and you have none, the register fix won't help; get a finding first.

Pair with `reddit-scout` (where you may post) and `reddit-post` (writing and verifying it).

## Related

- `reddit-scout` — rank subreddits and check whether promotion is allowed
- `reddit-post` — post, with visibility verification
- `reddit-seo` — confirm the post is indexable
