---
name: reddit-scout
description: >
  Find which subreddits are worth posting to for a topic — and, unlike every other prospecting
  tool, check whether posting is actually permitted there before you spend a post on it. Use
  whenever someone wants to find relevant subreddits, scout Reddit communities, research where to
  post or launch, find threads to reply to, do Reddit lead generation or ICP monitoring, or asks
  "where should I post this on Reddit". Also use before any Reddit promotion or launch, since it
  surfaces self-promotion bans, flair requirements, and karma or account-age gates that silently
  waste a post. Outputs a ranked, rules-checked target list with transparent scoring. Research
  only — it never posts; pair it with reddit-post for that.
---

# Scouting subreddits — with the permission check

Every Reddit prospecting tool finds threads. Almost none tell you whether you're allowed to post
in them. That gap is expensive: a post into a subreddit that bans self-promotion is removed within
minutes, and it costs account standing on the way out.

`reddit-scout` ranks candidate subreddits **and** reports the rules that decide whether posting is
viable at all.

```bash
node scripts/rdtx.mjs scout "claude code agent skills" --limit 10 --time year
```

## Verify the installed runtime without Reddit

Run `node scripts/verify-synthetic.mjs` with no arguments. It feeds fabricated candidates through
the production ranking contract to confirm that metadata opens the topical gate, example-only hits
do not, and an explicit promotion ban wins. It also checks the shared runtime without Chrome or a
Reddit request. A pass does not prove any current subreddit is relevant or permits promotion; live
rules still require the read-only workflow below.
Overall `passed` is the AND of all five shared checks; inspect `functional.reddit_scout` for this
skill's evidence.

An independent tester can submit the exact named verifier result through the
[structured installed-run report](https://github.com/L4A-ai/reddit-skills/issues/new?template=reddit-skill-installed-run.yml).
Select the `reddit-scout` zero-input synthetic option only after running the installed copy. This
proves installation and ranking contracts, not current rules or permission to promote.

Live scouting requires Node.js 18+, `agent-browser`, and the user's own logged-in Chrome profile;
see `references/browser-session.md`. The synthetic verifier needs only Node.js 18+.

## What comes back

```
✅  32  r/AIAgentsInAction     34,798  hits=2   avgC=55   flair=True
        no explicit promotion restriction
⚠️  20  r/LocalLLaMA          789,143  hits=3   avgC=113  flair=True
        allowed with conditions — read the rules
        rules: Limit Self-Promotion
🚫      r/programming       6,906,051
        DO NOT POST — promotion banned
        rules: No Product Promotion/"I Made This" Project Demo Posts
```

Each result carries `subscribers`, `search_hits`, `avg_comments`, `flair_required`, `promo_rules`,
`bans_promo`, `recommended`, an auditable `topical_fit`, three example threads, and the score's
components.

## The scoring is deliberately transparent

```json
"components": {
  "relevance": 0.78, "engagement": 0.55, "reach": 0.86,
  "permitted": 0.55, "topical_fit": 1
}
```

- **relevance** — share of search hits landing in this subreddit, normalised to the top one; this
  measures where matching posts appeared, not whether the community is about the topic
- **engagement** — average comments per matching thread, capped at 40
- **reach** — log-scaled subscriber count, so a 6M subreddit doesn't automatically dominate
- **permitted** — `1` if nothing restricts promotion, `0.55` if there are conditions, `0` if banned
- **topical_fit** — hard `1|0` gate from the subreddit's display name, title, and public
  description. A distinctive query-token match passes. For API/developer queries, developer-topic
  metadata such as `code`, `workflow`, or `automation` also passes.

`topical_fit` and `permitted` are independent gates. Search-result examples are reported separately
as supporting evidence and can never establish community fit by themselves. Thus a celebrity or
gaming subreddit does not become a target because one post happens to mention TikTok or an API,
and “rules do not ban promotion” never means “this community is relevant.” Every component and
reason is reported so you can disagree with the ranking rather than trust a number.

## Reading the verdicts

| verdict | meaning | what to do |
|---|---|---|
| `NOT RECOMMENDED — community topic mismatch` | matching posts exist, but the community metadata does not support the topic | do not use it as a campaign target |
| `no explicit promotion restriction` | no rule matched the promo patterns | still read the sidebar; absence of a rule is not an invitation |
| `allowed with conditions` | a self-promo/disclosure/ratio rule exists | read `promo_rules` and comply — often a disclosure line or a 90/10 ratio |
| `DO NOT POST — promotion banned` | an explicit ban matched | don't. The post gets removed and the removal is recorded |

Rule text is matched by pattern, so treat it as a filter that catches the obvious cases, not as
legal reading. `promo_rules` gives you the actual rule names to check yourself.

For backward compatibility, the top-level `postable` count still means only “not rule-banned.”
Campaign selection must use `recommended_count` and each result's `recommended: true`; the output
also reports `not_recommended` separately.

## The workflow this belongs in

```bash
# 1. Where is this conversation happening, and where may I join it?
node scripts/rdtx.mjs scout "your topic" --limit 10

# 2. What exactly does the best candidate demand?
node scripts/rdtx.mjs requirements <subreddit>

# 3. Draft, and confirm before writing (dry run is the default)
node scripts/rdtx.mjs submit <sub> "<title>" --text "<body>" --flair "<flair>"

# 4. Post, then confirm it wasn't silently filtered
node scripts/rdtx.mjs submit … --yes      # reports visibility
```

Steps 3–4 are `reddit-post`; step 4's visibility check is `reddit-seo`. Scout only reads.

## What good targeting looks like

The highest-value result is usually not the biggest subreddit. Scouting "claude code agent skills"
surfaced r/claudeskills — 48K subscribers, with a rule reading *"Sharing your own skill? Show your
work"* — ranked below r/ClaudeAI at 1M but a far better fit, because the community exists for
exactly that. Large general subreddits tend to have the strictest promotion bans; small on-topic
ones often welcome the thing outright.

Two heuristics worth holding:

- **`avg_comments` beats `subscribers`.** A subreddit where matching threads average 100+ comments
  is alive; one with a million subscribers and 3 comments a thread is a broadcast channel.
- **`search_hits` is conversation evidence, not community fit.** A post may mention a term for an
  incidental reason. Require `recommended: true`, then inspect `topical_fit.metadata_evidence`;
  `example_evidence` is deliberately supporting-only.

## Post distinct content, not the same post many times

The output is a ranked list, and the tempting move is to post the same thing down it. That is the
exact pattern spam detection is built to catch — and the damage compounds, because filtered posts
accumulate against the account rather than the post.

If a topic genuinely fits several subreddits, write for each one separately, space them out, and
check with `reddit-seo` that the first survived before considering a second. One post that stays
`live` and earns comments is worth more than five that get filtered.

## Setup

Needs a logged-in Chrome the human launched — Reddit's search endpoint returns 403 to
unauthenticated clients:

```bash
node scripts/rdtx.mjs launch && node scripts/rdtx.mjs login && node scripts/rdtx.mjs doctor
```

Scouting is read-only and paced (a jittered wait between requests). It examines ~18 subreddits per
run, which takes a minute or two — that pacing is deliberate, not slowness to optimise away.

## Related

- `reddit-post` — write, once you know where
- `reddit-seo` — confirm the post is actually visible
- `reddit-archive` — capture a thread and its media
