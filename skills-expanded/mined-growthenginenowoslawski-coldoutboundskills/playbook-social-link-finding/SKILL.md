---
name: playbook-social-link-finding
description: Resolve a company domain to its verified official social profile URLs (LinkedIn, X, Facebook, Instagram, YouTube, TikTok). Triggers on "find their LinkedIn", "get the company LinkedIn URL", "find their Instagram", "we need social handles for this list", "which companies have a TikTok", "social links for the TAM". Outputs one canonical profile URL per platform, or an empty string when the company genuinely has no account.
---

# Playbook: Company Social Link Finding

> All rules here are best practice, not law. Override any of them when the campaign calls for it; note the best practice once and move on.

**Use when:** a campaign or a downstream playbook needs the company's own social profile URL — most
often LinkedIn for engagement scraping, or Instagram and Facebook for a DTC brand angle.

**Do not use when:** you want a **person's** profile, post-level engagement
(`playbook-linkedin-engagement`), or an ad-library readout (`playbook-ad-library`, which consumes
this playbook's Facebook output).

**One-line output:** `company_linkedin_url = "https://www.linkedin.com/company/yampa-precision-manufacturing"`

## 1. Trigger and scope

One bare domain in, up to six verified profile URLs out.

**This is infrastructure, not copy.** Almost nothing here goes into an email directly. What it does
is feed the playbooks that DO produce copy — and every one of them treats the URL you hand over as
ground truth and scrapes whatever is behind it.

**That is the whole reason this playbook is strict:**

> A social URL that points at a similarly named company is **worse than an empty cell**, because the
> empty cell degrades gracefully and the wrong URL produces confident, specific, completely false
> personalization.

Both paid sources in the chain were measured returning **the wrong company's page** on real rows, so
**every value that did not come off the company's own website has to clear an ownership check before
it is written.**

## 2. Output contract

### Inputs

| Field | Type | Required? |
|---|---|---|
| `domain` (bare, lowercase, no scheme, no `www`, no path) | string | yes |
| `company_name` | string | yes — the verifier and the search queries both need it |

### Output fields

One canonical URL per platform, or `""`:

`company_linkedin_url` · `company_x_url` · `company_facebook_url` · `company_instagram_url` ·
`company_youtube_url` · `company_tiktok_url`

Plus, per platform, the **evidence source** that produced it. Keep that column: it is how you decide
later whether a value is trustworthy enough for a new use.

**Abstain value:** `""`. An empty cell means "no account found", which is a real and common answer.

## 3. Source chain (cost-tagged)

| # | Source | Cost | What it gives | Notes |
|---|---|---|---|---|
| 1 | An internal company database, exact `domain:=` lookup | FREE | LinkedIn only | always run — it also supplies `company_name`. **Exact match only, never fuzzy** |
| 2 | A company-search API, **batched by domain** | FREE / cheap | LinkedIn 6/8, X 5/8, FB 5/8, IG 4/8, **YouTube 0/8, TikTok 0/8** (no field exists) | ⚠️ see the batching trap below. **Bind results by PRIMARY domain only** |
| 2b | A domain ↔ company-profile converter | CHEAP | LinkedIn only, **both directions** | the reverse direction is what other playbooks come here for |
| 3 | **Plain website HTML fetch** — `https://<d>`, then `https://www.<d>`, then `http://<d>`, then `/contact`, `/about`, `/contact-us` | FREE | **the winning value on 5/8 rows, and the ONLY source of TikTok** | **the strongest evidence in the whole chain**, because a link in the company's own footer is self-attested ownership. **Pick the best match on the page, never the first one** |
| 3b | Rendering proxy | METERED | recovers bot-blocked sites | 1/1 on the blocked row, returned 4 correct platforms. ⚠️ see the challenge-page trap |
| 4 | SERP search, one simple query per empty platform | CHEAP | 5 correct values plus **4 correct rejections** across 8 rows | never an OR chain |
| 5 | **Model ownership verifier** | CHEAP | **20/20 correct decisions including 4 decoys** | **mandatory** on every search-derived and every secondary-domain candidate. Does not run on a site-footer value, which is self-attested |

### ⚠️ The batching trap

A company-search endpoint that accepts an array of domains may still be **hard-paginated at 25
results per page with no page-size parameter.**

Measured: posting **35 domains** returned `{"current_page":1,"per_page":25,"total_page":2,"total_count":32}`
and **25 results**.

**So a 500-domain body does not return 500 matches. It returns 25, and the other ~475 come back as
nothing — with no error and no warning.** An earlier draft of this playbook claimed "500 domains per
call" and would have **silently dropped roughly 95% of matches on any real backfill.**

Two things, both required:

- **Chunk to the page size** (25 here), and
- **still loop `page` to `total_page`**, because one domain can match more than one company record.

The live test could not catch this, because it used 8 domains — under the page cap — **even though
the raw response already said `"per_page": 25`.** Read the pagination block on your first call, every
time.

### ⚠️ The challenge-page trap

Advance to the rendering proxy on HTTP 403, HTTP 429, **or a 200 whose body is a challenge page.**

**Check the body, not just the status.** A common bot interstitial is served with **HTTP 200**,
yields zero matches, and otherwise looks like a clean legitimate miss.

### ⚠️ X requires company-site evidence, from every path

Accept search-derived evidence for LinkedIn, Facebook, Instagram, YouTube and TikTok. **For X,
require evidence from the company's own site.**

**X handles are short, recycled and squatted.** Measured: searching `site:x.com <brand>` returned a
handle that **matched the brand better than the real account does** — and was titled "Bug Poc".

This bans search-derived X **and** database-derived X, including a secondary-domain match that would
otherwise clear the verifier.

### Bind by primary domain only

A secondary-website match is a **candidate, not an answer.** Company records often list customers,
parents, or acquired brands as additional websites, and matching on those returns the wrong company
with no error.

## 4. Verification

**VERDICT: PASS 8/8.** The ownership verifier scored **20/20 including 4 decoys.**

## 5. Clay implementation

- **`clay-table.md`** — the column build.
- **`clay-workflow.md`** — the CLI-buildable version.

## 6. Locked prompt

Model: a nano-class reasoning model in your own batch; `gpt-4o-mini` in a Clay AI column — **because
a Clay AI column cannot set the completion-token cap, and this prompt truncates on a reasoning model
below 2,500 tokens.**

⚠️ **A cost-comparison mistake worth stealing.** An earlier draft claimed the nano-class model was
~40% cheaper here. **That arithmetic was wrong.** It priced both models on nano's measured **1,270
output tokens — of which 1,216 were reasoning tokens, which a non-reasoning model never emits.**
Priced on the ~55 tokens of JSON actually produced, the mini-class model comes out roughly **4x
cheaper**, the opposite of the original claim.

**Before you act on either number:**

1. **Pin reasoning effort low and re-measure.** Those 1,216 reasoning tokens were measured at
   **default** effort, which is the configuration that makes a reasoning model look ~18x worse than
   it is. **The comparison is only meaningful once effort is pinned.**
2. **Then run a 20-call head-to-head** on the same rows and take the cheaper winner. **Do not switch
   on a back-of-envelope estimate.**

Params: `max_completion_tokens=2500` (a measured floor), no `temperature`, JSON response format.

```text
You verify whether a candidate social media URL belongs to a specific company.

You are given the company name, the company website domain, the social platform, the candidate profile URL, and the evidence that produced it.

Return JSON only, exactly these keys:
{"owned":true|false,"canonical_url":"...","confidence":"high|low","reason":"..."}

Rules:
- "owned" is true only when the profile is the official account of THAT company. An account belonging to a different company with a similar name is false. An unrelated account that merely mentions the company is false. A fan page, a reseller, a news account, a hashtag or discovery page, or an individual employee's personal profile is false.
- Evidence sourced from the company's own website HTML is strong. Treat it as owned unless the handle clearly belongs to a different brand.
- Evidence sourced from a search engine is weak. Require the profile title, the handle, or the URL slug to match the company name or its domain root before returning true.
- A profile title naming a different entity than the company is false, even when the handle looks right.
- A URL that is a post, a photo page, a jobs page, a discovery page, an aggregator page, or a search page is not a profile. Return false. This includes tiktok.com/discover/..., instagram.com/p/..., instagram.com/popular/..., and youtube.com/playlist?...
- A YouTube URL of the form youtube.com/channel/UC... carries an opaque channel id that can never contain the company name. Judge it on the result title alone: when the title is the company name, owned is true and confidence is high.
- canonical_url: strip country subdomains to www, strip query strings, strip trailing path segments after the profile handle, strip the trailing slash. If owned is false, return "".
- confidence is "high" when the handle or slug contains the company name or the domain root, or the evidence came from the company website, or the profile title is exactly the company name.
- Never invent a URL that was not in the input.

PER-ROW DATA (appended last)
Company: <company name>
Domain: <domain>
Platform: <platform>
Candidate URL: <candidate>
Evidence: <evidence source and snippet>
```

Two rules in there are doing unusual work:

- **The evidence-strength distinction.** The same URL is treated differently depending on where it
  came from. **Self-attested footer links are strong; search results are weak.** That is the whole
  design of this playbook expressed in two sentences.
- **The opaque-channel-id rule.** A URL that *structurally cannot* contain the company name would
  fail a naive slug check on every real channel. Judging it on the title instead is the difference
  between 0% and useful YouTube coverage.

**Truncation guard:** `finish_reason=length` means retry, never abstain.

## 7. Edge cases and failure modes

| Symptom | Cause | Fix |
|---|---|---|
| A backfill silently returns ~5% of expected matches | **The batch endpoint is hard-paginated at 25** and a large body returns one page with no error | Chunk to the page size **and** loop pages. Read the pagination block on your first call |
| A clean-looking miss on a site that obviously has social links | A bot **challenge page served with HTTP 200** | Check the body, not the status. Escalate to the rendering proxy |
| An X handle matches the brand better than the real account | **X handles are short, recycled and squatted** | Require company-site evidence for X, from every path |
| The wrong company's profile is written | A match on a **secondary** website field | Bind by primary domain only. Secondary matches are candidates, not answers |
| A post or discovery URL is stored as a profile | `instagram.com/p/...`, `tiktok.com/discover/...` are not profiles | The verifier rejects them. Keep those rules verbatim |
| An employee's personal profile is stored as the company page | Search results mix them freely | The verifier rejects them |
| A YouTube channel never verifies | The channel id is opaque and cannot contain the company name | Judge those on the result title |
| A footer link points at the parent brand | Some sites link the group, not the subsidiary | **Pick the best match on the page, never the first one** — prefer the handle closest to the domain root |
| The verifier truncates | A reasoning model below a 2,500-token cap | Raise the cap, or use a non-reasoning model where the cap cannot be set |
| Nothing found for TikTok or YouTube | **Most company databases have no field for either** | Only the site fetch finds TikTok. Expect low coverage and treat empty as real |

### Hard rules

- **A wrong URL is worse than an empty cell.** Everything downstream scrapes whatever you hand over.
- **Site-footer evidence is self-attested and needs no model check.** Everything else does.
- **Exact domain matching only.** Fuzzy matching returns a different company.
- **Send a browser User-Agent** on every fetch; several of these sources sit behind a CDN that 403s
  default runtime agents.
- **Keep the evidence-source column.** Without it you cannot tell a strong value from a weak one six
  months later.
