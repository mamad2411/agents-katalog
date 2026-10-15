---
name: linkedin-copywriter
description: Draft LinkedIn posts in YOUR voice. Pulls hook frameworks, structural patterns, and CTA shapes from your real top-performing posts (corpus.md), runs the draft through a strict AI-slop blacklist, and outputs a post that reads like you wrote it. Use when asked to "write a linkedin post", "draft a post about X", "linkedin copy", "post idea", or "/linkedin-copywriter".
---

# linkedin-copywriter

Generate LinkedIn posts that sound like <YOUR_NAME>, not like ChatGPT.

The skill is grounded in <YOUR_NAME>'s actual last 20 posts (see
`corpus.md`), sorted by reactions. The top 5 are the viral anchors and
carry the most weight when picking hook + structure. Every draft is
checked against the slop blacklist below before it ships.

---

## SETUP (run this once before drafting)

This skill ships with `corpus.md.example`. Before the agent can sound
like you, you need a real `corpus.md`:

1. Copy `corpus.md.example` to `corpus.md` in this folder.
2. Populate it with your top 20 LinkedIn posts (sorted by reactions
   desc). Format is documented in the example file.
3. (Optional) Fill in the placeholder tokens in this file:
   `<YOUR_NAME>`, `<YOUR_BRAND>`, `<YOUR_DOMAIN>`, `<YOUR_EMAIL>`,
   `<YOUR_CAL_LINK>`, `<YOUR_LINKEDIN_HANDLE>`. The agent will use them
   verbatim in CTAs and references.
4. Re-read this file. The agent will then infer YOUR vocabulary
   fingerprints from your real posts (see §4).

Refresh the corpus quarterly so the voice stays current. Curl block at
the bottom of this file shows the Unipile pull.

---

## When to invoke

Triggers: "write a linkedin post", "draft a post on X", "linkedin copy
for Y", "post idea", "/linkedin-copywriter".

Do **not** use for: long-form (newsletter, blog, YouTube script),
proposal copy, motion-video voiceover, satire pillar videos.

---

## Workflow

### 1. Dump prompt

Open with one batched ask. Don't trickle questions:

```
Quick brief.

1. What's the post about? (announcement, teardown, framework, story,
   webinar, lead-magnet drop, hot take, ...)
2. The single specific fact, number, or story that anchors it. Be
   concrete. ("85 sales calls / month from 80k emails" beats "we got
   results").
3. Goal: pipeline (CTA → DM/comment), launch (CTA → link), authority
   (no CTA), or community (tag people).
4. Are we name-dropping a real human or company? Names beat abstractions.
5. Anything off-limits? (NDA stuff, pre-launch features, etc.)
```

If the user already gave enough, skip the prompt and parse. Only ask
follow-ups for missing fields.

### 2. Pick a hook from the kill / keep matrix

Read `corpus.md` if you haven't recently. Lock the hook to a pattern
the author already used at scale, not a generic LinkedIn template.

**Working hook patterns (with example posts that prove them):**

| # | Pattern | Example | Use when |
|---|---------|---------|----------|
| H1 | Industry doom claim | "Framer and Webflow are in massive trouble." | Teardown / replacement story |
| H2 | Concrete result + tool | "Claude code booked 85 sales calls / month for a client." | Case study / system reveal |
| H3 | Stat opener with payoff in line 2 | "Startups with co-founders are 3x more likely to succeed." | Personal milestone framed by data |
| H4 | Achievement + timeframe | "We built an AI GTM Engineer in less than 20 hours and won a hackathon." | Hackathon / launch / shipped-thing |
| H5 | "R.I.P. [Role/Industry]" | "R.I.P LinkedIn Agencies" | Lead magnet drop |
| H6 | "Devs have X. Now Y has Z." | "Devs have Claude Code. Now GTM-Teams have <YOUR_BRAND>." | Product positioning |
| H7 | Status update + backstory | "We launched 2 weeks ago. 60+ people jumped in." | Milestone post |
| H8 | Future prediction | "Intent signals will make or break your outbound in 2026." | Webinar / partner spotlight |
| H9 | Used-to-take-hours / now-takes-minutes | "Building cold email campaigns used to take hours. Claude Code builds them in minutes:" (Michel Lieben, 743r) | System reveal with concrete time delta |
| H10 | Identity-list contrarian | "I drink alcohol / I watch trash reality TV / I don't work 80hrs / ... / I take massive action without permission." (Matt Lakajev, 807r) | Counter-guru post, raw self-positioning |
| H11 | Framework declaration | "The 2026 GTM Flywheel.", "The evolution of GTM from 2010-2026." (Fivos Aresti, 290r / 243r) | Branded POV / industry history piece |
| H12 | Screw-it / IP giveaway | "Screw it. Write 8 LinkedIn books in 2 yrs. Comment BOOKS, FREE." (Matt Lakajev, 322r) | Lead magnet drop with raw energy |
| H13 | Diversification story | "We were 100% reliant on Clay. Claude Code gave us a chance to diversify." (Fivos Aresti, 233r) | Tool-switch / build-your-own piece |

H9-H13 are imported from 3 reference creators (Matt Lakajev, Michel
Lieben, Fivos Aresti). See `reference-creators.md` for full patterns
and "do not import" lists per creator.

**Hooks to never use (overused on LinkedIn, scream AI):**

- "Most people think X. They're wrong."
- "I used to believe X. Then Y happened."
- "Here's a hard truth nobody wants to hear:"
- "Stop doing X. Start doing Y."
- "X is dead. Long live Y."
- "I just saved my client $50k. Here's how:"
- Any vulnerable confession ("I lost everything in 2019…")
- Any hook ending with `:` and a one-line tease ("Here's the thing:")

### 3. Structure the body

Body shapes that show up in ≥3 viral posts each:

**S1. Setup → mechanics → tool stack → CTA.**
Hook fact → 1-2 line context → numbered or bulleted "here's how" →
tool list with hyphens → CTA.

**S2. Hook → personal story → bullet list of beliefs → close.**
Hook stat → "Met X at Y" → "Here's where we're aligned: → → →" → wry
sign-off.

**S3. Hook → numbered building blocks → CTA.**
Always a "3 things have to be true" or "5 building blocks" framing.

**S4. Industry-frame → product reveal → integration list → CTA.**
"X said it best:" → short framing → integration list with → arrows →
discount-code or free-tier CTA.

**S5. Tool-stack-by-layer (Michel Lieben).** After the body explains a
system, add a categorical "stack by layer" block:

```
The full stack by layer:

- data: Apollo, Clay, Prospeo
- enrich: FullEnrich, CompanyEnrich
- signals: PredictLeads, Trigify
- orchestrate: n8n, Claude Code
- action: Instantly.ai, HeyReach
```

Use when the post is a system reveal and credibility comes from real
category coverage. Closes well with a "your folder structure becomes
your GTM brain" / system-as-brain framing line.

**S6. Era timeline (Fivos Aresti).** For industry-history or POV posts.
Year-range header → `↳` tool list → 1-line summary per era.

```
2017-2019: Revenue Intelligence
↳ ZoomInfo, 6sense, Gong, Clari, Clearbit

GTM got smarter with call recordings, enrichment, and signals
driving rep prioritization.

2020-2022: Intent Data
↳ Bombora, UserGems, Demandbase, G2

Signal-mania started and ABM went mainstream.
```

Close with: "The next era is being built right now. If you're reading
this, you're still early." (Fivos's tested close.)

**S7. Market map (Fivos Aresti).** For tools-roundup posts. Categorize
50-70 tools/companies into 3-4 tiers (Favorites · Rising · Unicorns ·
Others, or your own). Country flag emoji optional. Each line:
`Tool · Description (🇺🇸)`. Close with "What did I miss?".

Length budget: 70-100 entries is the format's expectation. If you only
have 15 tools, use S5 instead (tool-stack-by-layer).

**S8. Client case study (Fivos Aresti).** Hook = named-client +
concrete numbers + time window. Body = numbered breakdown with
sub-headers (`Content engine`, `Automated outbound`, `Flywheel`).
Close = "Full breakdown below" pointing to the visual. Use plain `1)`
not `1️⃣` keycap.

Example shape:
> "We built a Content + Outbound flywheel for [Client] that
> generated [number] in [time window]."
> 1) [What we did, layer 1]
> 2) [What we did, layer 2]
> 3) [The flywheel diagram]
> Results: [3 stats]

**S9. Identity-list / roast-list (Matt Lakajev).** Two flavors of the
same shape. Both rely on a long flat list with no commentary, letting
the reader self-identify.

- **Identity-list (counter-guru):** 5-7 short "I do / I don't"
  statements that flip orthodoxy, then one reframe line.
- **Roast-list:** 20-30 numbered things (worst niches, worst hooks,
  worst tools), no analysis, optional "you on the list?" close.

Use sparingly. Build-in-public energy and snark are different brands.
One per month max unless the author's voice is already snark-heavy.

Pick **one** shape and commit. Don't mix S1 + S3 in the same post.

S5-S9 are imported from the reference creators. See
`reference-creators.md` before using one for the first time.

### 4. Voice profile (what makes a sentence sound like the author)

**Vocabulary fingerprints.**

After you populate `corpus.md` with YOUR last 20 posts (see SETUP),
the agent infers YOUR vocabulary fingerprints from your real posts.
The patterns below are placeholders to give the agent a starting point.
Yours will replace them.

Placeholder examples (until your `corpus.md` is loaded):

- Casual fillers and abbreviations the author actually uses (e.g.
  `ofc`, `hmu`, `deets`, `hehe`)
- Domain-native slang (e.g. `cracked dev`, `vibe coding`, `lock in`)
- Recurring nicknames for archetypes the author calls out (e.g.
  `Lead Gen Bros`, `Agency Bros`)
- Smiley or emoji habits (e.g. trailing `:)` after a CTA)
- Tool names with proper casing the author uses repeatedly
- Numerals over words always (3x, 85, 80k, $480, +33%)
- Casual, lowercase fragments after a period if the corpus shows them

**Sentence shape:**

- One thought per paragraph. Most paragraphs 1-3 lines.
- Mix of bullet markers across posts: `→`, `-`, `•`, `1)`, `[1]`.
  Within a single post, **stay consistent**. (Viral posts pick one
  marker and hold it.)
- Numbered framework lists use `1)`, `2)`, `3)` (not `1.`).
- Walking-CTAs use `[1]`, `[2]` brackets.
- Asides go in parentheses. (Parens carry tone.)
- Full stops are heavy. Use them where most LinkedIn writers would use
  commas. Lean into that rhythm.

**Casing and punctuation:**

- Sentence case for everything except product names.
- Straight quotes only.
- Ellipsis as `...` (not `…`) when used at all.
- No bold, no italics. LinkedIn doesn't render them and faking them
  with Unicode is slop.

### 5. CTA patterns (verbatim shapes that work)

**CTA-A. Lead magnet:**
```
If you want [thing]:

[1] Connect with <YOUR_NAME>
[2] Comment '<KEYWORD>'

and then I'll send it over to you:)
```
The keyword is short, on-topic, slightly cringe-fun ("Claude GTM",
"cool stuff", "AGI", "Growth Vault"). Pick a new one each time.

**CTA-B. Webinar / event:**
```
[Day/date] [time] CET

Drop your questions in the comments. <Cohost> is answering them live.
```
Or: "Grab your spot and drop your questions in the comments."

**CTA-C. Product:**
```
If you want to test it, we have a very generous free tier. Link in
the comments.
```
Or with a discount-code variant:
```
If you want 30% off our launch deal, here's how to get one of the 50
available discount codes:

[1] Connect with <YOUR_NAME>
[2] Comment "AGI"

I'll DM you a discount code so you can start the 7-day free trial.
```

**CTA-D. None.** Authority posts often have no CTA, or just a soft
"What's your X?" question. Don't force a CTA on every post.

**CTA-E. 24-hour link drop (Matt Lakajev).** When the lead magnet
needs build-up, defer the link.
```
Comment '<KEYWORD>' and I'll send the [thing].

I'll share the link in 24 hrs.
```
Mechanic: comments compound during the wait window, the follow-up
post 24h later carries its own algo lift, and the keyword filters out
casual asks. Use 1-2x per month max so it stays special.

**CTA-F. Double-offer P.S. (Michel Lieben).** Main offer in body,
second offer in P.S. Each offer requires a different action.
```
[main body offer: Comment 'AGI' for the discount code]

P.S. We also recorded a 40-min video walkthrough. Comment 'WALKTHROUGH'
if you want that one too. I'll DM both.
```
Tradeoff: longer post, but you double the surface area for engagement
and capture both casual and high-intent readers in one shot.

**CTA-G. "You're still early" close (Fivos Aresti).** Soft authority
close with no ask. Frames the reader as ahead of the curve.
```
Out of [big number], only [small percent] are doing this.
You're still early to win.
```
Use on framework / era / market-map posts where the implicit ask is
"adopt this before everyone else does".

**Banned closers (AI bait):**
- "Agree?"
- "Thoughts?"
- "What do you think? Drop a comment 👇"
- "Tag someone who needs this."
- "Save this for later."
- "Like and follow for more."

### 6. Slop scrub (mandatory pre-output check)

Before showing the draft, scan it against this list. Any hit → rewrite.

**Punctuation:**
- ❌ Em dash `—`. **Hard ban.** Replace with period, comma, colon,
  parens, or middot `·`.
- ❌ Smart/curly quotes (`"…"` `'…'`). Straight only.
- ❌ Ellipsis character `…`. Use `...` if needed at all.
- ❌ Non-breaking spaces, en dashes used as ranges in prose.

**Banned phrases (kill on sight):**
in today's fast-paced world, in today's digital age, dive in, deep
dive into, delve into, navigate the landscape, navigate the
complexities, unlock the power, unlock the potential, unleash your
potential, at its core, it's important to note, it's worth noting,
a testament to, game changer, move the needle, stay ahead of the
curve, cutting-edge, state-of-the-art, next-gen, robust, scalable,
seamless, world-class, leverage (verb), synergy, embark on a journey,
foster a culture, drive impact, drive value, take a moment to,
buckle up, here's the kicker, here's the catch, let that sink in,
read that again, spoiler:, plot twist:, I'm thrilled to announce,
I'm humbled to announce, couldn't be more proud, trust the process,
your network is your net worth, soft skills are the new hard skills,
hope this helps.

**Single-word flags (replace with the plainest word that works):**
delve, dive (into), embark, unlock, unleash, harness, elevate,
transform, revolutionize, foster, navigate, journey, landscape,
realm, ecosystem, tapestry, fabric, paradigm, multifaceted,
intricate, intricacies, complexities, nuanced, comprehensive,
holistic, robust, seamless, scalable, dynamic, vibrant, profound,
pivotal, crucial, vital, essential, meticulous, unwavering,
transformative, innovative, cutting-edge, groundbreaking,
revolutionary, leverage, utilize, optimize, streamline, empower,
amplify, spearhead, underscore, resonate, illuminate, shed light,
beacon, testament, treasure trove, labyrinth, symphony, notably,
arguably, indeed.

Fixes: "use" not "leverage", "help" not "empower", "strong" not
"robust", "many parts" not "multifaceted", "show" not "underscore",
"big" not "transformative".

**Structural slop:**

- ❌ Negation pivot in 3+ places. ("It's not X. It's Y. It's not
  about A. It's about B.") Use **at most once per post**, and only
  when the contrast is real. Three of them = AI.
- ❌ Tricolons of parallel verbs/adjectives ("Listen, adapt, deliver.
  Faster, cheaper, better.") on every other line.
- ❌ Throat-clearing transitions: Furthermore, Moreover, Additionally,
  That said, Importantly, Ultimately, Subsequently.
- ❌ Cringe transition questions: "The result?" "The catch?" "Why
  does this matter?"
- ❌ Symmetric paragraphs (every paragraph the same length and shape).
  Real human posts are uneven.
- ❌ One-sentence-per-paragraph for the entire post. Mix paragraph
  lengths.
- ❌ Bold/italics fake formatting (Unicode bold characters like
  `𝗧𝗵𝗲 𝗳𝗼𝘂𝗻𝗱𝗮𝘁𝗶𝗼𝗻`). Even when high-engagement creators use it,
  it reads as fake.
- ❌ Keycap emoji as numbered headers (1️⃣ 2️⃣ 3️⃣). Reads as
  template slop. Use plain `1)` `2)` `3)` or `1.`. Same applies to
  `🔟`, `1️⃣1️⃣` and friends.
- ❌ TL;DR / In summary / Key takeaways headers.
- ❌ Emoji bullets (🚀 ✨ 💡). One or two emojis is fine, almost
  always a single `:)` at the end of a CTA, occasionally `🚀`, `🔥`
  in mentions, never as bullet markers.

**Why it works:** the LLM is performing competence instead of
communicating a thought. If a sentence is signaling that the author is
smart rather than transferring information, cut it.

### 7. Length

Viral posts cluster in two sizes. Match one:

- **Short (60-150 words).** Hook + 2-3 short paragraphs + CTA.
- **Long (250-450 words).** Hook + body with one structural device
  (numbered list or → bulleted beliefs) + CTA.

If the brief doesn't dictate length, default to **long** for
authority/launch posts and **short** for event reminders / partner
shouts.

### 8. Output

Show the draft in a fenced code block (so the user can copy-paste
without LinkedIn's formatter mangling spaces). Below the block, give:

- Word count
- Hook pattern used (e.g. "H2 · Concrete result + tool")
- Body shape used (e.g. "S1 · Setup → mechanics → tool stack → CTA")
- Slop scrub: "0 hits" or list any flags caught + how I rewrote them
- Two alternative hooks the user can swap in (one shorter, one
  bolder), each one line

Do **not** add commentary like "I hope this helps!" or "Let me know
if you want changes." Just the draft + the metadata block.

---

## Content graph (close the loop)

This skill writes to `content/posts/`, which feeds the content knowledge
graph (`content/CONTENT-WIKI.md`).

**Before drafting:** find the durable idea this post expresses and open
its note in `content/concepts/`. Reuse its canonical lines and proof and
push the idea one beat further, instead of starting from a blank page.
This is what makes content compound: you remix your own canon, not the
feed.

**After the draft is saved:** for the post's 1-3 core ideas, add the post
to each concept's `## Appears in` (`- [[<post-slug>]] · <short angle>`),
lift any sharp new line into `## Canonical lines`, and bump `appears_in`
+ `updated`. If an idea has no concept note yet and is genuinely durable,
create one from the template in `CONTENT-WIKI.md` and list it in
`content/index.md`. Update any `content/entities/` or `content/mocs/` the
post touches, and append a line to `content/log.md`.

Edges live in the concept notes; Obsidian backlinks make them
bidirectional, so you do **not** edit the post body to add them.

---

## Editing mode

If the user pastes an existing draft and asks to "fix the slop" or
"make this sound more like me":

1. Read the draft.
2. Run the slop scrub (§6). Flag every hit inline.
3. Rewrite to the matched hook + body shape from §2-§3.
4. Output the rewrite + a diff-style list of what changed and why.

---

## Repurpose context (when called from a `/repurpose` orchestrator)

If invoked with a `source` reference (master Notion row, transcript
excerpt, or external URL):

1. Treat the source as the **insight bank**. Pick one specific hook /
   data point / quotable line from it · don't rephrase the whole thing.
2. Open the post with that anchor (a number, a quote, a moment), not
   with "I just published a webinar on X."
3. Soft-reference the master at the end if it adds value (e.g.,
   "Going deeper on this in <webinar / article / podcast>") · skip
   if the post stands alone.
4. Output the draft as usual. The orchestrator handles creating the
   Notion row and pasting `Source: <URL>` at the top of the page body
   · don't include that line yourself.

---

## Reference files

- `corpus.md`. The author's last 20 posts (sorted by reactions desc).
  The top 5 are the strongest voice anchors. Re-read before drafting
  if you've been off-task for a while. **Voice ground truth.**
- `reference-creators.md`. Pattern library extracted from 3 high-
  performing GTM creators (Matt Lakajev, Michel Lieben, Fivos Aresti).
  H9-H13 hooks, S5-S9 body shapes, and CTA-E/F/G are sourced here.
  Each section has a "do not import" list. **Pattern library, not
  voice anchor.** Read when a brief calls for a structure outside
  the author's existing patterns (era timeline, market map,
  identity-list, etc.).
- This SKILL.md. Voice rules + slop blacklist.

---

## Refresh the corpus (run quarterly)

If you use Unipile to read your own LinkedIn account, the curl below
pulls your last 20 posts. Set the env vars in your shell or `.env`:

```bash
source .env && \
curl -s "https://${UNIPILE_DSN}/api/v1/users/<YOUR_LINKEDIN_PROFILE_ID>/posts?account_id=${UNIPILE_ACCOUNT_ID}&limit=20" \
  -H "X-API-KEY: ${UNIPILE_API_KEY}" -H "accept: application/json"
```

Required env vars:

- `UNIPILE_DSN` · the Unipile DSN host (e.g. `api12.unipile.com:14229`)
- `UNIPILE_ACCOUNT_ID` · your Unipile account id for the LinkedIn
  connection
- `UNIPILE_API_KEY` · your Unipile API key
- `<YOUR_LINKEDIN_PROFILE_ID>` · your public LinkedIn profile id (the
  URN that Unipile returns for your account)

Then re-sort by `reaction_counter` desc and overwrite `corpus.md`.

If you don't use Unipile, just paste your top 20 posts manually using
the format in `corpus.md.example`.
