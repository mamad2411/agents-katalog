---
name: playbook-social-posts
description: Fetches the most recent usable LinkedIn post from a company page OR a person's profile and stores the post content itself, with an optional AI personalization line on top. Triggers on "what did they post about", "recent LinkedIn post", "social signal", "reference their content", "they posted about X", "what is this person posting", "engage with their content". Outputs social_post_text (the raw post) plus social_post_url and social_post_days_ago; social_post_line only when the operator asks for one.
---

# Playbook: Recent Social Post

> All rules here are best practice, not law. Override any of them when the campaign calls for it; note the best practice once and move on.

**Use when:** the campaign wants proof you read the account's content and there is no sharper
structural signal (funding, new-in-role, hiring surge).

**Not this playbook:** who *engaged* with a post (`playbook-linkedin-engagement`); a job change
(`playbook-new-in-role`).

**Output:** `social_post_text` + `social_post_url` + `social_post_days_ago` + `social_post_author_type`.
Optional, on request only: `social_post_line` → `Noticed they became an IBM Business Partner.`

## Six decisions that govern every run

**1. The raw post is the product.** The AI line is an optional layer, not the point. A human reading
the actual post writes a better sentence than any generated line, and the post text is reusable for
every future campaign; a generated line is not.

**2. Input is a profile URL, either kind** — a company page or a person. One scraper takes both.

- **Company runs:** dedupe to companies, then **fan the one result out to every contact there.**
- **Person runs: never fan out.**
- **Never guess a slug.** They are frequently not what you would predict from the company name.

**3. The content skip filter is mandatory and fails closed.**

Skip `personal`, `political`, `bereavement`, and `charged` (religious or geopolitical flashpoints).

- **A skip takes the NEXT post. It is not an abstain.**
- **Error, bad parse, or a missing `skip` key all mean SKIP.** Only a literal `"skip": false` keeps
  the post.
- **Never disable it to raise fill.**

Ordinary business content passes: memes, polls, job ads, volunteering, work anniversaries,
regulation commentary.

**4. Blank, never invented.** Nothing usable means `""` everywhere. No guess, no "N/A", **no
sequencer-side fallback value.**

**5. Two operator questions at setup.**
"A written personalization line, or just the post content?" (default: content only.)
"Trust the scrape, or add a verification pass?" (default: trust it — verification checks existence,
never text.)

**6. Empty rows are gated by a LIST SPLIT before upload, never by spintax.**

Spintax picks at random and **cannot see an empty variable.** `{Noticed {{social_post_line}}. |}`
both renders `Noticed .` into inboxes **and** discards personalization you already paid for.

Split the list on `social_post_line != ""`. Segment B has the clause **removed and rewritten** — and
it is your honest A/B control. Never exclude empties, never set a fallback.

**QC:** `grep -c "Noticed \." rendered_preview.csv` must be `0`.

## The best call, and three traps in it

Scrape company posts with an **async 3-call pattern**: start the run, poll for completion, read the
dataset.

⚠️ **Never use a synchronous run-and-get-items endpoint.** It held the client past 120s on a run
that took 25s.

Body: up to ~100 target URLs, `maxPosts: 3`, a 3-month window, reposts off, quote posts on. Then the
skip filter over each post **newest-first**, keeping the first that clears.

- **Batch the URLs.** Each run start bills separately, so a batch of 8 costs the same start fee as a
  batch of 1.
- **Keep reaction and comment scraping off.** You are not building an engagement list here.
- ⚠️ **The profile join key will bite you.** On *person* items the company-style identifier is
  **null**; the slug lives in a different field and the author type differs. **Group on
  `universalName or publicIdentifier`, or every person row silently vanishes.**
- **Low reasoning effort on the skip filter is load-bearing** — at default effort it hung past 180s.
  `finish_reason=length` with empty content means **retry with double the cap, never an abstain.**

## Honesty gates

**Coverage: 71% of company pages had a usable post** in the test — and that is **a floor for the
field and an upper bound for this kind of list**, because the sample was 17 high-frequency B2B SaaS
posters.

**SMB, trades and long-tail: expect 20 to 40%.** Under about 50 employees the company page is usually
dead, and **the founder's personal profile is the intended lever** (fill unmeasured).

**Measure fill on a 100-row sample of YOUR list before writing copy around it.**

**Tests:** skip filter **18/18**. Optional line **8/9 (89%)** held out. Person-URL probe **1/1**.

⚠️ **The reshaped chain has not been run end to end.** Parts tested, composition not. The first
operator to run it at any size owes the file a real fill rate and a re-measured cost — **read the
charged-event count, never estimate.**

## Cost

About **$2.95 per 1,000 unique profiles** in the default content-only shape, rising to about **$3.66**
with the optional line.

⚠️ **Campaign rows are contacts, not profiles.** Dedupe before this playbook and fan the result back
out: a 1,000-contact list covering 620 accounts costs about **$1.83**, not $2.95. Costing this per
contact overstates it by your contacts-per-company ratio.

## Clay implementation

- **`clay-table.md`** — the column build, including the degraded variant for when async polling is
  not available.
- **`clay-workflow.md`** — the CLI-buildable version.

## Edge cases and failure modes

| Symptom | Cause | Fix |
|---|---|---|
| The client times out on a fast run | A synchronous run-and-fetch endpoint | The async 3-call pattern |
| Every person row vanishes at the join | On person items the company-style identifier is **null** | Group on `universalName or publicIdentifier` |
| Cost is much higher than expected | Each run start bills separately | **Batch the URLs.** 8 in a batch cost one start fee |
| The filter passes something you would never send | It was disabled to raise fill | **Never disable it.** A skip takes the next post |
| A row abstains when a later post would have worked | A skip was treated as an abstain | A skip advances to the next post |
| A malformed filter response keeps a bad post | The filter failed **open** | **Fail closed.** Only a literal `"skip": false` keeps a post |
| `Noticed .` in rendered previews | Spintax used as an if-populated gate | **Split the list.** Grep the rendered preview to zero |
| A generated line references a post the account did not write | Reposts were included | Reposts off |
| Fill is 20% on an SMB list and 71% was promised | The 71% came from high-frequency SaaS posters | Measure fill on your own list. Use founder profiles for small companies |
| The scraper is down and the run fails over to another source | There is no fallback by design | The signal **abstains**; it does not fail over |

### Hard rules

- **The raw post is the deliverable. The line is opt-in.**
- **The skip filter is mandatory and fails closed.**
- **Blank, never invented — and no sequencer-side fallback value.**
- **List split, never spintax.**
- **Dedupe to profiles before scraping, fan out after.**
