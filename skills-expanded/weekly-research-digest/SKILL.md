---
name: weekly-research-digest
description: >
  Produces a curated weekly research digest tailored to a researcher's profile — covering papers,
  tools, industry news, and ecosystem moves across their active research areas. Use this skill
  whenever the user asks for their weekly digest, says things like "qué hay esta semana",
  "make my weekly digest", "research roundup", "weekly update", "novedades", "what dropped
  this week", or any variation indicating they want a curated summary of recent developments
  in their field. Also trigger when the user asks to "run the digest" or "do the digest".
  Requires the user to have configured a PROFILE.md (see references/profile-template.md).
---

# Weekly Research Digest

A skill for producing a ruthlessly filtered, high-signal weekly research digest tailored
to a researcher's specific profile. The digest covers the last 7 days and spans papers,
tools, blog posts, and industry news.

---

## Step 0 — Load the user's profile

Before doing anything else, check whether the user has provided a profile. The profile
can live in any of these places (check in order):

1. A `PROFILE.md` file uploaded or referenced in the current conversation
2. A profile block pasted directly in the chat
3. Memory/context from previous conversations in this project

If no profile is found, **do not proceed**. Instead, show the user the template from
`references/profile-template.md` and ask them to fill it in. The digest cannot be
meaningfully filtered without a profile.

---

## Step 1 — Search broadly and systematically

Search across **all** source categories below. Do not skip categories — a good digest
requires broad coverage before ruthless filtering. Use parallel or sequential searches
as needed. Aim for 15–25 candidate items before filtering down.

### Source categories

**Academic papers (arXiv / Semantic Scholar / ACL Anthology)**
- Search each of the user's research areas as explicit queries
- Focus on cs.CL, cs.AI, cs.HC, cs.LG and any domain-specific categories from the profile
- Prioritize papers from the last 7 days; accept up to 14 days if the week was slow

**GitHub trending**
- Check what's trending this week in the user's tech stack and research areas
- Look for new repos with significant traction (stars, forks, recent activity)
- Prioritize repos that are tools, frameworks, or datasets — not just demos

**Technical blogs**
- Check blogs listed in the user's profile sources
- Also check: Simon Willison's blog, Lilian Weng, The Gradient, Ahead of AI, Sebastian Raschka
- Look for substantive posts, not announcements or link roundups

**Industry / applied**
- Check sources listed in the user's profile (e.g., industry blogs, conference channels)
- Focus on items with technical or empirical substance, not pure marketing

**Framework changelogs / releases**
- Check release notes for tools in the user's tech stack
- Only include if the release changes something meaningful for the user's work

### Search query construction

For each research area in the user's profile, generate 2–3 specific search queries.
Combine area keywords with recency signals ("2025", "new", "released this week").
Do not rely on a single broad query per area.

---

## Step 2 — Filter ruthlessly

Apply the user's relevance vectors from their profile. An item earns a place in the
digest if it connects clearly to **at least one** of the user's defined vectors.

**Automatic exclusions (regardless of profile):**
- Generic model benchmarks with no relevance to the user's methods or domain
- Duplicate coverage of items already in recent digests (check conversation history)
- Marketing content with no technical or empirical substance
- Papers that cite relevant-sounding terms but whose actual contribution is unrelated

**Quality bar:**
- A paper must contribute a method, dataset, finding, or framing that the user could
  cite, replicate, or build on
- A tool must have a clear use case for the user's current or near-term work
- An industry item must contain technical detail or signal a meaningful ecosystem shift
- A blog post must teach something, not just announce something

**Target:** 3–5 items. If after filtering you have fewer than 3 strong items, expand
the search window to 14 days or lower the threshold slightly — but never include
filler. If you genuinely have fewer than 3 high-signal items, say so and explain why.

---

## Step 3 — Format the digest

Write the digest in the user's preferred language (from their profile; default: English).
Keep technical terms in English regardless of digest language.

Use this exact template:

```
## 🗞️ [DIGEST TITLE] — Week of [start date]–[end date] [year]

---

### [N]. **[TITLE IN ORIGINAL LANGUAGE]** — [source / author if relevant]
[URL] | **Category: [paper | tool | industry | blog]**

[What it is and why it matters this week — 2–3 sentences, direct, no filler]

**Relevance to your work:** [How it connects to the user's specific vectors — 1 precise sentence]

---
[repeat for each item]

## 📌 To follow
[1–2 threads, accounts, or repositories that gained traction this week and are worth watching]
```

**Digest title:** Use the user's preferred digest name from their profile, or default to
"RESEARCH DIGEST".

**Ordering:** Most relevant to least relevant based on the user's primary research vector.

**Tone rules:**
- Direct. No "this week has been exciting" or similar filler openers.
- Each item starts by stating what it *is*, then why it *matters*.
- Relevance line must be specific — reference the user's actual methods, concepts, or
  goals. "Connects to your research" with no further detail is not acceptable.
- Match the user's preferred register (formal/informal) from their profile.

---

## Step 4 — Self-check before sending

Before sending, verify:

- [ ] Every item has a working URL (not guessed or hallucinated)
- [ ] Every item is genuinely from the last 7 days (or 14 if noted)
- [ ] No item repeats coverage from recent digests in the conversation history
- [ ] Relevance lines are specific, not generic
- [ ] Item count is 3–5 (not inflated with filler)
- [ ] "To follow" section has 1–2 items with clear signal

If a URL cannot be verified, flag it explicitly in the digest entry rather than omitting
or silently guessing.

---

## Editorial principles

These apply regardless of the user's specific profile:

**Signal over completeness.** A digest with 3 strong items is better than one with 5
mediocre ones. Do not pad.

**Primary sources when possible.** Link to the arXiv paper, the GitHub repo, the
official changelog — not to a tweet about the tweet about the paper.

**No hallucinated papers.** If you cannot find a paper via search and retrieve a real
URL, do not include it. It is better to have a shorter digest than a fabricated one.

**Industry items earn their place through technical detail.** A studio announcing
"we're using AI for NPCs" is noise. A studio explaining the architecture, the failure
modes, or the production constraints is signal.

---

## Reference files

- `references/profile-template.md` — Template for the user to configure their research
  profile. Show this to new users or users who haven't configured a profile yet.
