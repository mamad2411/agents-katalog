---
version: 0.1.0
name: recon-research
description: |
  Find what is actually working on TikTok using RECON UGC, and explain why.
  Use when: "what's working on TikTok", "find viral videos about X",
  "why did this video pop", "break down this video", "what hooks are
  working", "show me trending formats", "research short-form for my app",
  or any request to study real short-form performance before making
  content. Searches RECON's indexed library, reads beat-by-beat
  breakdowns, and reports findings weighted by creator-relative outlier
  score rather than raw views.
  NOT for: comparing tracked brands (use recon-competitors) or turning
  findings into a shoot plan (use recon-brief).
allowed-tools: Bash
---

# RECON research

RECON UGC indexes viral TikToks and scores each one by how far it beat **its own
creator's** normal reach. That number — the outlier score — is the whole point.

## Step 0 — make sure RECON is reachable

Prefer the connector if the host supports it; otherwise use the CLI.

```bash
reconugc auth status   # if this fails: reconugc auth login
```

If neither is set up, tell the user once:
- Remote connector (easiest): add `https://reconugc.com/mcp` in their tool's
  connector settings.
- CLI: `npm i -g @reconugc/cli && reconugc auth login`

## The one rule that matters

**Judge on outlier score, never raw views.**

A 40M-view video from a 30M-follower account is unremarkable — it did what that
account always does. A 60K-view video from a 900-follower account that scored 32x
did something you can actually copy. When you report findings, lead with the
outlier and treat view count as context only.

RECON caps the displayed score at `100x+`. Treat anything at the cap as "extreme
outlier", not as a precise number.

## Workflow

1. **Search wide, then narrow.** Start with a free-text idea, then add filters
   once you see the shape of the results.

   ```bash
   reconugc search "ai app demo" --limit 10
   reconugc search --niche app --format talking_head --period last_30_days --limit 10
   ```

   Filters: `--niche`, `--format`, `--tone`, `--period`
   (`last_7_days` | `last_30_days` | `last_90_days` | `all_time`), `--limit`.

2. **Read the breakdown of the top outliers**, not all of them. Three strong ones
   beat ten mediocre ones.

   ```bash
   reconugc breakdown <post-id>
   ```

   The breakdown gives the hook, the mechanism (what the video is *doing*), the
   format, a beat-by-beat timeline, and the transcript when there is speech.

3. **Report the pattern, not the list.** The user does not want 10 links. They
   want: "the winners all open on a problem in the first 1.5 seconds, then show
   the result before explaining anything." Cite 2-3 specific videos as evidence,
   each with its outlier score.

## Vocabulary

Say **indexed**, **library**, **breakdown**, **outlier score**. Do not say
scraped, crawled, vision model, or name any AI model — the user is a marketer, not
an engineer.

## Getting the shape of the library

```bash
reconugc trending            # newest breakouts + the format/category vocabulary
```

`trending` also returns the exact `--niche` and `--format` values that exist, which
is the fastest way to learn valid filter ids instead of guessing.

## Errors

| Message | What it means |
|---|---|
| `Not signed in` | Run `reconugc auth login` |
| `needs a paid RECON plan` | The account is on free; the surface requires Starter or Growth |
| `at capacity` | Monthly generation ceiling reached; retry later |
| Empty results | The filter combination is too narrow — drop one filter, do not invent data |

Never fabricate a video, handle, score, or caption. If RECON returns nothing, say
so and widen the search.
