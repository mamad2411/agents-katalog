# Totem Newsletter Site - Standing Instructions

## Formatting

**Always use markdown hyperlinks for URLs.** Never output a bare URL in chat replies. Format every link as `[descriptive text](url)` so it is clickable. This applies to live deploy URLs, GitHub links, Vercel inspection links, article URLs, and any other hyperlink.

Examples:
- Correct: [totem-newsletter-site.vercel.app/market_pulse_july30_2026.html](https://totem-newsletter-site.vercel.app/market_pulse_july30_2026.html)
- Wrong: `https://totem-newsletter-site.vercel.app/market_pulse_july30_2026.html`

**Every clock time carries AM or PM and the time zone.** Write "8:30 AM ET," "2:00 PM ET," "11:00 AM ET." Never "8:30 ET," "8:30," "10am," or "2 PM" without the zone. The reader should not need to know that jobs data is a morning release to read the time. Applies to the article, the email, post-cards, and chat replies. (JJ, 2026-09-02.)

## Vercel environments

There are three Vercel projects. Never confuse them.

| Project | URL | Purpose |
|---|---|---|
| `totem-challenge-preview` | totem-challenge-preview.vercel.app | **Live site** - what email links point to. Phase 2 deploy target. |
| `totem-editorial-review` | totem-editorial-review.vercel.app | Editorial review - auto-deploys on every `git push origin main`. |
| `totem-newsletter-site` | totem-newsletter-site.vercel.app | **Do not use for live deploys.** This was mistakenly used on 2026-08-03. |

### Morning deploy authorization (locked 2026-08-31)

**The site deploys automatically. No approval gate.** After Phase 1 completes (build + push to editorial), proceed immediately to Phase 2 without stopping to ask JJ.

**The one exception:** JJ reviews email copy on his own schedule before sending in Mailchimp. The agent does not send email and does not wait. After Phase 2, send JJ a push notification with the live article URL and the email copy review link - then stop.

**Reaffirmed 2026-09-02 (JJ): "You can always go live after you build the site. I don't need to review this before we go live anymore."** If the scheduled-task prompt still says to stop after Phase 1 and wait for "approved" or "go live," that wording is superseded by this file. Build, push to editorial, run Phase 2, verify the live page, notify. Do not ask.

### Phase 2 live deploy sequence (exact commands)

```bash
# 1. Strip editorial nav links from ALL public HTML files (Email Copy + Emergency PO <li> items).
#    The script is in the repo. Never sed (sed has corrupted files before).
#    It exits non-zero if any public file still carries a link.
python3 scripts/nav_links.py strip

# 2. Link CLI to the correct live project
npx vercel link --yes --project totem-challenge-preview --token "$VERCEL_TOKEN"
# 3. Deploy
npx vercel --prod --yes --token "$VERCEL_TOKEN"
# 4. Restore editorial nav links in ALL files. Exits non-zero unless every
#    public file carries both links again. If it fails, restore from git:
#    git checkout <pre-strip commit> -- *.html
python3 scripts/nav_links.py restore
# 5. Relink CLI back to the editorial project (keeps .vercel/project.json tidy)
npx vercel link --yes --project totem-newsletter-site --token "$VERCEL_TOKEN"
# 6. Commit and push the restored files so the editorial site stays in sync
git add -A && git commit -m "Restore editorial nav links" && git push origin main
```

Always verify the aliased URL in the deploy output reads `totem-challenge-preview.vercel.app` before declaring Phase 2 complete. Then `curl` the live article and confirm: the new headline, no `email_copy.html` link, anchors `open-1` through `open-5` present.

**Lesson from 2026-09-02:** the first restore script anchored on the Archive `<li>` being on its own line. In 58 older files it shares a line with The Challenge link, so those files were committed to main without the editorial links. The repo script now inserts before the nav's `</ul>` and refuses to exit clean unless every file is restored. Do not replace it with a scratchpad one-off.

**Why all files, not just today's article:** Every page on the site (index, archive, all articles, all challenge issues) shares the same nav. Stripping only the new article leaves Email Copy and Emergency PO visible to readers on every other page.

## Market Pulse Article Format v2 (locked 2026-09-02 - JJ approved after a full live-data run)

**This is the article template. Every morning run builds the page this way. No exceptions, no reverting to the pre-September-2 format.** The newest article file is the template; copy its full `<style>` block (the `.sec-v2` rules are the format) and its section markup exactly. The September 2, 2026 article is the reference implementation.

### Why it exists

Before September 2 the article ran 5,752 words (25 minutes). Every section said each fact three times: an italic gray intro, then semicolon-chained data lines in colored semi-bold, then a bottom line. JJ's verdict: an hour-long read that looked like contract fine print. The fix is not fewer facts. It is each fact said once, plainly, with the source named. September 2 closing edition: 3,499 words, every data line intact.

### The opening (replaces headline + dek + Quick Read + bullets)

1. **Kicker**: `Market Pulse • [Day], [Month D, YYYY]`. Centered.
2. **Headline**: **12 words max, two sentences**, centered, Spectral 800 at `clamp(34px,4.6vw,46px)`, sitting 56px below the kicker. **Identical, word for word, to the email hero headline** so the click lands on the sentence the reader just read. Opportunity Frame applies (see the email rules): lead with what is available for the reader, never with the conflict.
3. **No dek.** Retired 2026-09-02. Its job (the day's tension) is the first sentence of Quick Read paragraph 1.
4. **The Quick Read**: three paragraphs, **250 words hard cap**, Work Sans title, drop cap on paragraph 1. Paragraph 1 = the tension, then the cause and its mechanism, ending on the mechanism. Paragraph 2 = what today (or Friday) decides, with the thresholds. Paragraph 3 = what keeps building underneath. Closes with a `Curated from` sources line.
5. **How [Day] Opens** (or **Closed** for a post-close edition): **exactly five bullets, and they are the five answers to the five email bullets, in the same order.** Each `<li>` has `id="open-1"` through `id="open-5"`. Each opens with the email bullet's text **verbatim in bold**, gives the answer in 40 to 50 words, and ends with an `<a class="more" href="#section">Section name →</a>` link to the section that carries the full data. The email bullets deep-link to `...html#open-1` through `#open-5`. This is the email-to-web handoff; it is not optional.

### Every topic section (11 of them, same skeleton, in this order: Stock Market, Interest Rates, Savings & CD Rates, Energy & Gas Prices, Commodities, Crop Weather, Real Estate, Household Finance, Crypto, Around the World, The Week Ahead)

Wrapped in `<div class="sec-v2">`:

1. **Title** `h2.section-title` (Work Sans 800, 24px).
2. **Stat strip** `div.strip`: three cells, each `k` (label) / `v` (rounded figure, tabular numerals) / `d` (direction: `up`, `down`, or `flat`, with ▲ ▼ and the change or "Unchanged"). This is the section's headline. Fixed contents:

| Section | Strip cells |
|---|---|
| Stock Market | S&P 500 · Nasdaq · Dow |
| Interest Rates | Fed funds · 2-year · 10-year |
| Savings & CD | Top 1-yr CD · Top HYSA · Nat'l avg 1-yr CD |
| Energy | Brent · WTI · Gas (AAA) |
| Commodities | Gold · Silver · Copper |
| Crop Weather | Corn G/E · Soybeans G/E · Corn futures (or drought share) |
| Real Estate | 30-yr mortgage (Freddie Mac) · 10-year · Canada lumber tariff day |
| Household Finance | Layoffs or real wages · Card delinquency 90+ · Gas (AAA) |
| Crypto | Bitcoin · Ethereum · XRP |
| Around the World | Nikkei · Hang Seng · Yen (swap in the day's mover) |
| The Week Ahead | Next three dated catalysts |

3. **Setup paragraph** `p.setup`, **italic** (the CSS does it), 40 to 70 words, one or two bold phrases max. What moved and why, once. Never a list of the numbers that follow.
4. **Data lines** `div.lines > div.line`: gold dot bullet (CSS), then `span.lb` label with the date in parentheses (e.g. "S&P 500 (September 2 close):"), `span.num` the **precise figure to the decimal**, `span.d` direction, then `span.why` on its own line: one to three plain sentences, **regular weight, body color**, saying why it moved and what it means. **Keep every data line readers come for. Never chain clauses with semicolons. Never restate the setup.**
5. **Bottom line** `div.bottom`: gold left rule, `span.lbl` label, one `<p>` of one to three sentences. The call, not a summary.
6. **Sources line** `div.src`: `<b>Curated from</b> Source · Source · Source`. Only sources actually used. This is the "we went to ten places so you don't have to" promise, printed on every section.

### Typography and emphasis rules

- Bold is for labels, numbers, and at most two key phrases per section. Nothing else. If everything is bold, nothing is.
- Muted gray (`--muted`) is for metadata only: dates, strip labels, sources, sidebar. **Never for a content sentence.** The `.flat` direction marker is the one exception.
- Colored text is for direction markers only (`.up` green, `.down` red). Never color a sentence.
- Bullets are the 5px gold dot, 22px indent, vertically centered on the first line. Same dot on How [Day] Opens and on every data line.
- Times: always AM/PM plus zone (see Formatting).
- Hyphens for asides, never em dashes.

### Word budget

| Unit | Cap |
|---|---|
| Headline | 12 words |
| Quick Read | 250 |
| How [Day] Opens | 5 × 65 (bold lead + answer + link) |
| Each topic section | 200 to 380 |
| Whole article | 3,000 to 3,600 |

Under 3,000 means data lines were dropped; over 3,600 means something is being said twice. A section whose data has not moved says so in the setup line and keeps its data lines; it does not pad.

### Data accuracy (the ADP lesson, 2026-09-02)

The morning article carried ADP at 47K. That was the consensus; the release was 38K. **Use the released figure, never the forecast.** When a figure is not yet released, say "due at [time]" and do not put a number in the strip. When a figure cannot be found, write "not available" or carry the last reading with its date; never carry a stale number as if it were today's. Mark estimates as estimated (WTI). Every strip figure and data line needs a source that appears in the section's Curated from line.

### Disclaimer

See "Article disclaimer" below. Two paragraphs, verbatim General Disclaimer plus the as-of line. Nothing else.

## The Attention Rules (locked 2026-08-20; opening-block sequence superseded by Article Format v2 on 2026-09-02 - the dek is retired, the Subject Variety Rule and the Bullet Rule still apply)

These govern the **opening block** of every article and every email - the first thing the reader sees. They exist because 11,000-word briefings with the correct data still get archived unread when the top of the page fails to earn the scroll. Length was never the real problem; **sequence** was. Each opening unit must earn its place by being different from the one before it.

### The Subject Variety Rule (the one that actually governs attention)

**No two consecutive opening units may lead with the same subject.** The opening units are, in order: headline → dek → Quick Read paragraphs → How Thursday Opens bullets. If unit N is about the buyback, unit N+1 is not. This is not a length rule - a 30-word dek that restates the headline is worse than a 90-word paragraph that opens a second front.

Test: read only the first 8 words of every opening unit in order. If more than one leads with the same subject or keyword, restructure. On Aug 20 the pre-fix count was 5 of 6 opening units framed by Treasury; 42 Treasury mentions before the bullets even started. That is the failure mode.

### The Five Opening Jobs

Each of these appears exactly once. Never in the same unit, never repeated.

1. **Headline** - the 2-3 biggest facts (2-3 sentences, hyphen for asides). Rule below on length.
2. **Dek** - the day's tension, not a summary. Two sentences. It must add the read rather than restate the headline. Test: if it could sit under any headline this week, rewrite it.
3. **Quick Read paragraph 1** - the cause and its full downstream chain, said once. Ends with the mechanism ("that is the whole mechanism") so nothing downstream needs to re-explain it.
4. **Quick Read paragraph 2** - what today actually decides. The scheduled event, the number the market is watching, the stakes.
5. **Quick Read paragraph 3** - what keeps building underneath. The slow pressure the market hasn't priced yet.

Quick Read caps at 250 words across the three paragraphs combined. Section-intro lines that restate the bullets beneath them are forbidden.

### The Bullet Rule

Every "How Thursday Opens" bullet must **add information the Quick Read did not carry**, not retell it in longer form. Good bullet openings: "What the buyback means past this week." "The crypto flows say institutions, not retail." "Why these three dissenters, specifically." Bad bullet openings: "Treasury doubled long-bond buybacks to $4 billion..." (restatement).

Test: strike the Quick Read from the draft and re-read each bullet. If a bullet loses its point, it was a restatement; rewrite it.

### Headline length

Headline: 2-3 sentences, 40-word ceiling. Same discipline as the post-card rule below. The August 20 headline before the fix ran 96 words across 6 sentences. Ship at 30-40.

### Dek length

Dek: 30 words maximum, two sentences. Anything longer is a lead paragraph in the wrong slot.

### Rounding

Use precise figures the first time only. Every subsequent mention rounds: $71,751 becomes $71.8K, 26,331.09 becomes 26,331 or "the Nasdaq." Decimals signal a data dump; round numbers signal a point of view.

### Standing sections only appear when something changed

The 13 deep sections (Stock Market, Interest Rates, Savings & CD, Energy, Commodities, Crop Weather, Real Estate, Household Finance, Crypto, Around the World, This Week's Events) are the product and stay. But a section whose data has not moved since yesterday runs as a two-line "no change" note rather than three paragraphs of restatement. Crop Weather when corn is flat, Around the World when China's number is unchanged - those get compressed, not padded.

## Article disclaimer (locked 2026-09-02)

The article ends with **exactly two paragraphs** in the `.disclaimer` block, and nothing else:

1. The General Disclaimer from the Totem Compliance Manual, verbatim, never paraphrased:
   > This material is provided for informational purposes only and does not constitute legal, tax, securities, lending, investment, or financial advice. Participation in commercial transactions involves risk, including possible loss of capital. Historical performance does not guarantee future outcomes.
2. One as-of line: "Figures reflect the latest readings available as of [Day, Month D, YYYY], before the US market open. Sources are listed at the end of each section."

**Never append a data recitation to the disclaimer.** Before Sept 2 the block restated every figure in the article (closes, rates, crypto, crop data, the week's calendar) as a 600-word "citation" paragraph. That is not a disclosure; it is the article a second time. Sourcing lives in each section's "Curated from" line. The site footer carries the Website Disclaimer verbatim ("This material is provided for informational purposes only and does not constitute legal, tax, lending, securities, investment, or financial advice."). Do not shorten either to "general information only, not investment advice"; the manual lists that paraphrase as an anti-pattern.

## Post-card and hero headline length

**Keep post-card and hero cap-title headlines to 2-3 sentences max.** Pick the 2-3 most important data points - the ones that would stop a reader mid-scroll. Do not dump the full article headline into the post-card. The article itself carries the detail.

- Good: "July CPI Matched Consensus at 3.4% - September Hike Odds Fall to 38%. S&P 500 7,748 in Relief Rally. Oil Retreats to WTI $82.11 on Hormuz Deal Signals."
- Too long: "July CPI Matched Consensus at 3.4% - September Hike Odds Fall to 38%. S&P 500 7,748 in Relief Rally. Oil Retreats to WTI $82.11 on Hormuz Deal Signals. USDA Corn Yield 180.7 BPA Misses Estimates. PPI + Jobless Claims at 8:30 AM ET Today. Retail Sales Tomorrow."

This applies to: index.html post-cards, archive.html post-cards, and the hero `cap-title` on index.html.

## Market Pulse Email Format

**Never change the email format without JJ's explicit instruction.** Content updates only - dates, data, links. The structure is locked.

### THE CLICK RULE (locked 2026-09-02 - overrides every other email rule below)

**The email's only job is the click.** It is not a briefing. It is not a summary. It is a hook. Success is measured on two numbers only: open rate and click rate. 90-day Mailchimp baseline (Jun-Aug 2026): 32.5% open, **2.0% click**. The best-performing send (June 5) hit 16.4% click; the worst dozen sends hit 0.0%. The 0.0% sends had 30%+ opens - people opened, read, and had no reason to leave the inbox. **That is the failure mode: an email that answers its own questions.**

JJ has flagged this repeatedly. Every time the email carries the "why," the reader gets the payoff in the inbox and never clicks. The website carries the answers. The email carries only the questions.

**Hard caps - not targets, caps. Count the words before pushing.**

| Unit | Cap | Form |
|---|---|---|
| Preheader | 12 words | One line that creates a gap, not a summary |
| Hero headline | 20 words, 2 sentences | The two biggest facts, nothing else |
| Lead paragraph | 25 words, 1-2 sentences | A tension or a question. Never an explanation. |
| Data snapshot | 5 items max | Rounded figures only |
| Each of the Five Things | **15 words, one bold sentence, NO context sentence** | Names what the article explains and withholds the explanation |
| Total body copy (preheader + lead + snapshot + five bullets) | **120 words** | If it is over, cut - do not tighten, cut |

**The Curiosity Gap Test (run on every bullet before pushing):** Read the bullet alone. Does it make the reader ask "why?" or "what?" - and is the answer *only* on the website? If the bullet contains its own answer, it has failed. Cut the answer, keep the question.

- Failed (Sept 2 before fix, 58 words): "The 'tanker for tanker' doctrine targets Iran's revenue, not just its weapons. Each struck tanker reduces Tehran's immediate hard currency flow from crude exports - a pressure that secondary sanctions haven't touched directly. The Bessent secondary-sanctions lever remains undeployed..."
- Passed (11 words): "Why the tanker strikes hit Iran's wallet harder than its missiles."

**Every bullet is a link to the article.** The five bullets are five click targets, not five paragraphs. The bottom CTA button sits directly under them.

**Never write these into the email:** a mechanism, a scenario table ("a miss below 100K does X, a beat above 150K does Y"), a second-order consequence spelled out, a number the reader could not have guessed. Those are the article. If it would make a reader say "got it" instead of "wait, why?", it belongs on the website.

### THE OPPORTUNITY FRAME (locked 2026-09-02 - JJ's instruction, applies to every email)

**Less war. Less fear. Lead with what is available *for* the reader, not what is happening *to* them.** JJ's words: news defaults to Crisis News Network energy, and that is not what people want to wake up to. A threat headline earns one open and then trains the reader to dread the email. An opportunity headline carries its own reason to click.

This is **not spin**. The facts do not change and nothing is hidden - the reality check stays in the email as data (snapshot line) and the article carries the full story. What changes is the **order and the verb**: the first eight words of every opening unit are about the reader's money, not Tehran.

**Rules:**

1. **Headline test.** Does the hero's first sentence describe a threat to the reader or an opening for the reader? Lead with the opening. If the day's biggest fact is a conflict event, frame it by its consequence for the reader (rates, a price that got cheaper, a sector that held) - never by the event itself.
2. **Bullet ratio.** Of the five bullets, at least **three** point at something the reader can use, gain, or act on. At most **one** leads with a conflict or fear word. The war, if it appears, is one bullet, never the frame.
3. **First-eight-words ban list** for subject line, preheader, hero headline, and lead: *strikes, war, crisis, collapse, crash, fear, plunge, panic, attack, escalation.* These words may appear in the article; they do not open the email.
4. **The "what's working" pass.** Before writing the email, list the five most constructive facts in today's article (a rate on savings going up, a price that got cheaper, a state crop reading that beat, a sector that held while the index fell, a legislative window still open). That list is the bullet pool. Sept 2 proof: all five opportunity bullets were already inside the article - Iowa corn 77%, energy and defense holding the Dow, gold cheaper, the CD wait decision, four CLARITY Act days. They were just never surfaced.
5. **Compliance stays on.** Opportunity framing is not a promise. "Savers are 66% likely to get a raise" passes; "savers will get a raise" does not. Never a buy, never a guarantee. Run the totem-compliance-screen posture on every hero.

**Sept 2 example - same facts, both frames:**

| Threat frame (shipped first) | Opportunity frame (what JJ asked for) |
|---|---|
| US Strikes Iranian Tankers - Brent Surges to $94.86. September Hike Odds Hit 66%. | Savers Are 66% Likely to Get a Raise This Month. Gold Just Got 2.9% Cheaper. |
| Why the tanker strikes hit Iran's wallet harder than its missiles. | The one move CD savers should wait to make before September 15. |
| What gold falling on a war day says about where institutions are positioned. | Gold got cheaper on a day it should have gotten expensive - what that opens up. |

**Measure it.** Mailchimp subject-line A/B: run the opportunity subject against the threat subject on each send for two weeks and tag the sends. Ten sends decide it with data, not opinion.

### Schedule
- **Monday - Thursday:** Market Pulse email only. Member and non-member use the same structure (see below). No additions, no extra sections.
- **Friday:** Different format (Challenge lead + Market Pulse). Do not apply Friday's structure to Mon-Thu.

### Structure (Mon-Thu, both member and non-member)

**LOCKED FORMAT (confirmed Aug 25, 2026 — do not change without JJ's explicit instruction):**

1. **Masthead** - TOTEM LC GROUP + tagline
2. **Gold 1px `<hr>` rule** - between masthead and hero block
3. **Navy hero block** (navy gradient, `border-radius: 4px`) - self-contained, contains ALL of: kicker line, "Market Pulse" logo text, short headline (2 sentences, 20 words max, white Spectral bold), and gold CTA button. Links to today's article on totem-challenge-preview.vercel.app. **No separate white card below the hero.**
4. **Gold CTA button** (`#fcb900` background, dark text `#16181d`, `border-radius: 3px`) - inside the hero block. Label: "Read Today's Briefing".
5. **Lead paragraph** (Spectral 21px bold) - **the tension frame, not a teaser of the top story.** 25 words max. It must open a second subject to whatever the hero headline led with. See the Subject Variety Rule.
6. **Data snapshot** (Inter 14px) - one line, 5 items max. Rounded figures. **Gold left border: 3px gold `<td>` + 14px padding-left.** Never restates the lead paragraph in prose.
7. **Divider**
8. **"Five Things Only Totem Will Tell You Today"** - gold-bullet label, then 5 bullets. **Each bullet is ONE bold sentence, 15 words max, linked to the article. No context sentence.** Every bullet opens a distinct subject; no bullet may re-tell the hero story. See The Click Rule and the Bullet Rule.
9. **Bottom CTA button** - same gold button, directly under the five bullets. Added 2026-09-02 on JJ's click-rate instruction; it is the click target for a reader the bullets just hooked.
10. **Footer** - disclaimer + Totem LC Group sig

**What is NOT in this email (do not add):** inline link row, separate white article card below the hero, navy date bar as a separate element (it is baked into the hero kicker), any explanatory sentence after a bullet.

### The lead paragraph is the tension frame

The lead in the email is not a teaser of the top story - the hero headline already carries that. Its job is to name **the day's hinge**: the question the day is about to answer, or the tension the market is holding. 25 words max, one or two sentences. If the reader could guess what your top story is by the end of sentence one, the lead is not doing its job. If the lead *explains* the hinge instead of naming it, it is too long.

**Correct (tension frame, Aug 20):**
> "Rates fell, crypto ripped, and equities bounced. Walmart opens its books at 6am against a consumer 13.1% behind on credit cards - the number that says whether any of it holds."

**Wrong (retelling the hero story):**
> "Bessent doubled Treasury long-bond buybacks to $4 billion per operation, pulling the 30-year yield from 5.33% to 5.19%. The move triggered a crypto rally with Bitcoin at $71,751 and Ethereum at $2,280..."

### The Subject Variety Rule (applies to the email too)

Read only the first 8 words of each of these opening units in order:
1. Preheader
2. Hero headline
3. Lead paragraph
4. Data snapshot
5. Each of the five bullets

**No two consecutive units may lead with the same subject.** On Aug 20 before the fix, 8 of 9 email units opened with or landed on Treasury. That is the failure mode. If the hero is the buyback, the lead is the consumer, bullet 1 tells the reader something they can't get on CNBC about the buyback's *consequence*, not its facts.

### The Bullet Rule

The bullet label was changed from "Also in Today's Briefing" to **"Five Things Only Totem Will Tell You Today"** to enforce the standard. Every bullet must *point at* an editorial read - the "why," the "so what," or the second-order consequence - without delivering it. The bullet is the question; the article is the answer.

Bad bullet: "Treasury doubles long-bond buybacks to $4B - 30-year falls to 5.19%." (data restatement)
Also bad: "The rate ceiling has an expiration date. Buybacks at $4B/operation exhaust Treasury's authority in 6 weeks, after which..." (the read, fully delivered - no reason to click)
Good bullet: "The rate ceiling has an expiration date." (the read, withheld - 7 words, one sentence, links to the article)

Two tests, both must pass:
1. Strike the article's Quick Read from the email and re-read each bullet. If a bullet loses its point, it was a restatement; rewrite it.
2. Read each bullet alone. If it answers its own question, it is too long; cut it to the question.

### Rounding in the email

Data snapshot uses rounded figures. $71,751 → $71.8K. 7,707.98 → 7,708. 26,331.09 → 26,331. The article carries the decimals; the email is the map, not the terrain.

### Member vs. non-member differences (only these two)

| Element | Member | Non-member |
|---|---|---|
| `<title>` | `Market Pulse - [Date] - Member Edition` | `Market Pulse - [Date]` |
| Hero kicker | `[Day], [Date] · Member Edition` | `[Day], [Date] · [Day] Briefing` |
| Footer line | "You are receiving this email as a member of Totem LC Group." | "A free weekly snapshot for the Totem community." |

Both footers then carry the General Disclaimer **verbatim** (locked 2026-09-02, JJ's instruction): "This material is provided for informational purposes only and does not constitute legal, tax, securities, lending, investment, or financial advice. Participation in commercial transactions involves risk, including possible loss of capital. Historical performance does not guarantee future outcomes." Never the "general information only, not investment advice" paraphrase; the compliance manual lists it as an anti-pattern.

Everything else is identical. Do not add member-only sections, greetings, transaction alerts, or Challenge blocks to Mon-Thu emails without explicit authorization.

## Market Pulse — Tracked Assets

### Crypto (always research and include data lines for all of these)

| Asset | Ticker | Notes |
|---|---|---|
| Bitcoin | BTC | Price, ETF inflows (IBIT etc.), rate-path sensitivity |
| Ethereum | ETH | Price, regulatory backdrop (CLARITY Act), support levels |
| XRP | XRP | Price, ETF inflows, CLARITY Act legislative status, on-chain metrics (DAA, network growth), escrow unlocks |

Search for each asset's price every morning. For XRP specifically: check ETF inflows (cumulative and monthly), CLARITY Act Senate status, on-chain metrics (Daily Active Addresses, network growth from Santiment), and Ripple escrow unlock schedule.

## Agent skills

### Issue tracker

Issues live in GitHub Issues on `navajosouljah/totem-newsletter-site` (via the `gh` CLI). See `docs/agents/issue-tracker.md`.

### Triage labels

Default vocabulary: `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`. See `docs/agents/triage-labels.md`.

### Obsidian memory

JJ's vault is local (`~/Vaults/BOLT/`, not reachable from cloud sessions). The standing-decisions note for Market Pulse is kept vault-ready in the repo at `docs/obsidian/Totem_Market_Pulse_MEMORY.md` with its target vault path in the frontmatter. **Whenever a rule in this file changes, update that note in the same commit.** A local session with vault access copies it to `~/Vaults/BOLT/20_Businesses/Totem/MEMORY.md`.

### Domain docs

Single-context: one `CONTEXT.md` at the repo root plus `docs/adr/`. See `docs/agents/domain.md`.
