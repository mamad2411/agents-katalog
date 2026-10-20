---
name: blog-social
description: >
  Derives social-platform posts from a Diligence-passed blog. Use it for
  /4d-blog-engine:blog-social or "derive the LinkedIn post", "derive the LinkedIn article", "make
  the Twitter thread", "write a Facebook post from this", "social derivatives". It covers LinkedIn
  (a feed post plus its first comment, with an optional long-form Article), Twitter/X (a 5 to 10
  post thread at 280 characters each) and Facebook (a single short post). For LinkedIn it
  discovers the writer's authorable channels live from their logged-in browser and asks which one
  to publish to; a Company or Showcase Page gets the Article-led trio, a personal profile gets the
  post and comment pair. The writer picks the platforms, so nothing is auto-invoked at Phase 4
  sign-off. Outputs and a per-platform scorecard land in the piece's 04-diligence/social/ folder.
allowed-tools: [Read, Write, Edit, Bash, Glob, AskUserQuestion, mcp__Claude_in_Chrome__tabs_context_mcp, mcp__Claude_in_Chrome__navigate, mcp__Claude_in_Chrome__browser_batch, mcp__Claude_in_Chrome__computer, mcp__Claude_in_Chrome__read_page, mcp__Claude_in_Chrome__get_page_text, mcp__Claude_in_Chrome__find, mcp__Claude_in_Chrome__javascript_tool]
---

# Blog Social Deriver — multi-platform social derivatives from a signed blog

## When this skill applies

This skill should be used when deriving social-platform posts from a Diligence-passed blog in the 4D Blog Engine, or whenever the writer runs /4d-blog-engine:blog-social. Supports LinkedIn (feed Post + companion first-comment, with optional long-form Article), Twitter/X (5-10 post thread, ≤280 chars per post), and Facebook (single ~300-500 char post). When a LinkedIn surface is selected, it discovers the writer's authorable LinkedIn channels (personal profile + Company/Showcase Pages + newsletters) live from their logged-in browser via Claude in Chrome and asks which channel to publish to. On a Company/Showcase Page the output is an Article-led trio — long-form Article (lead) + a short teaser Post + a first comment that links to the published Article + blog + sources, published in that order; on a personal profile it stays the feed Post + first-comment-to-blog pair. The writer picks which platforms to derive — nothing is auto-invoked at Phase 4 sign-off. Reads <piece>/04-diligence/blog.md plus 01-delegation.md (angle + earned secret) and the writer's voice profile, applies per-platform register shifts, generates platform-appropriate hooks, runs scripts/social_score.py for format-compliance checks, and produces per-platform 3-axis scorecards. Outputs land in <piece>/04-diligence/social/. Triggers: "/4d-blog-engine:blog-social", "/blog-social", "derive the LinkedIn post", "derive the LinkedIn article", "make the Twitter thread", "write a Facebook post from this", "social derivatives".


> **Read this when:** Phase 4 (Diligence) has signed off and the writer wants to derive social-platform posts. Your job is to produce one or more of: `<piece>/04-diligence/social/linkedin-post.md` (+ its companion `linkedin-first-comment.md`), `<piece>/04-diligence/social/linkedin-article.md` (optional long-form), `<piece>/04-diligence/social/twitter-thread.md`, `<piece>/04-diligence/social/facebook-post.md` — based on which platforms the writer picks.

## Why LinkedIn produces two files

LinkedIn's algorithm deprioritizes posts that contain outbound links (the platform wants readers staying in the feed). The workaround everyone in the field uses is to paste substantive content directly into the **Post** body — no links — and put the link plus source citations in the **first comment** under the post. That's why this skill produces a Post / first-comment **pair** as the LinkedIn default, not a single artifact. The optional long-form Article (the "Write article" path) is a separate publishing surface — different button on LinkedIn, different URL, far less reach per piece, but indexed by Google and permanent on the writer's profile. Most writers only need the Post + first-comment.

## STEP 0 — Confirm the gate signed

Before generating anything, verify:

1. `<piece>/04-diligence/preflight-report.json` exists and `passed: true`.
2. `<piece>/changelog.md` exists and contains a line matching `^Verified — .+, \d{4}-\d{2}-\d{2}`.

If either check fails, **stop and report**: *"The Release Owner Gate has not been signed. Cannot derive social posts. Run /4d-blog-engine:blog-diligence first."*

## STEP 1 — Load references and context

Read in order:

1. `${CLAUDE_PLUGIN_ROOT}/references/hook-library.md` — six named hook formulas plus the per-platform formula-fit table.
2. `<piece>/04-diligence/blog.md` — the signed blog post (canonical source for every social artifact).
3. `<piece>/01-delegation.md` — angle, audience persona, earned secret. Social posts must lean MORE personal/opinion than the blog; the earned secret anchors that personal weight on every platform.
4. `<piece>/02-description.md` — voice interview answers (same voice carries across all platforms).
5. **The writer's voice profile** — locate by walking up from `<piece>` to find `blog-project-instructions.md`, then resolve `<blog-project-dir>/<author-slug>-voice.md`. If multiple `*-voice.md` files exist, use the same voice the blog was written in (the orchestrator state file records this in `<piece>/state.md` under `voice:`). Re-load right before writing each platform's output. If no voice profile is found, halt with a pointer to `/4d-blog-engine:blog-voice`.

## STEP 2 — Ask the writer which platforms to derive

Use `AskUserQuestion` (multiSelect: true) with options:

- **LinkedIn Post + first comment** — feed Post (1,300-2,500 chars sweet spot; 2,900 hard cap) plus its companion first-comment file carrying the blog URL and the 2-3 sources the Post quotes inline. This is the primary LinkedIn surface. (Recommended)
- **LinkedIn Article (long-form)** — separate from the Post. Long-form article (800-1200 words) published via LinkedIn's "Write article" path. Gets a stable URL, indexed by Google, lives on the writer's profile. Lower initial reach than a Post, longer shelf life. Pick this in addition to the Post if the piece warrants both surfaces.
- **Twitter (X) thread** — 5-10 connected posts, each ≤280 chars. Post 1 is the hook; Post N closes with the blog URL + ≤2 hashtags.
- **Facebook post** — single post, 300-500 chars sweet spot, blog URL allowed inline (Facebook renders a preview card).

The writer can pick any combination. If they pick nothing, halt with: *"No platforms selected; nothing to derive."*

**Note on the LinkedIn pair:** if the writer selects "LinkedIn Post + first comment", you produce TWO files (`linkedin-post.md` AND `linkedin-first-comment.md`) — never one without the other. The first comment is what makes the no-body-link post-format strategy work; producing the Post without the first comment leaves the writer without the source-and-link payload to paste into the comment box after publishing.

**Note on company pages:** what the writer ticks here is provisional for LinkedIn. The channel chosen in STEP 2b decides the final LinkedIn shape — and if that channel is a Company/Showcase Page, the output is always the Article-led trio (Article + teaser Post + first comment), regardless of which LinkedIn boxes were ticked here. See STEP 2b, "The channel type sets the LinkedIn output shape."

Create the output directory if it doesn't exist:

```bash
mkdir -p <piece>/04-diligence/social/scorecards
```

## STEP 2b — Choose the LinkedIn channel (only if a LinkedIn surface was selected)

Run this step only if the writer selected **LinkedIn Post + first comment** and/or **LinkedIn Article** in STEP 2. If they picked only Twitter and/or Facebook, skip to STEP 3.

LinkedIn lets the writer author as their **personal profile** or as any **Company/Showcase Page** they admin — and newsletters hang off either host. Which channel a piece publishes to changes the audience, the "Post as" actor the writer has to switch to before pasting, and the posting reminders this skill emits. So the channel has to be settled *before* you write the LinkedIn artifacts. Discover the real list from the writer's own logged-in LinkedIn — never hardcode it, and never assume "personal."

### Discover the channels (Claude in Chrome)

Claude in Chrome runs in the writer's real, authenticated browser, so it reads the actual set of identities they can post as (LinkedIn's anti-bot gate doesn't trigger). Drive it by screenshots and the accessibility tree, **not** fixed pixel coordinates — LinkedIn moves its DOM around, so identify panels by their heading text and re-screenshot between clicks.

1. `mcp__Claude_in_Chrome__tabs_context_mcp` with `createIfEmpty: true` to get a tab.
2. `mcp__Claude_in_Chrome__navigate` to `https://www.linkedin.com/feed/`. Wait ~3 seconds for render.
3. **Confirm the session is live.** If the page shows a login/auth wall instead of the feed (no "Start a post" box), STOP this step and tell the writer: *"Sign into LinkedIn in Chrome, then re-run — I couldn't reach your logged-in session."* Then use the "If Chrome is unavailable" fallback below.
4. Open the composer: click **Start a post**.
5. Click the **caret next to your name** (the "Post to Anyone ▾" control) → the **Post settings** panel opens.
6. Click the **author row at the top of that panel** (the "<Your name> ›" row) → the **Posting as** panel opens. This panel is the authoritative list: the personal profile plus every Page the writer can author for.
7. Read it: take a `screenshot` and call `read_page` (filter `all`) — enumerate every radio-option label. Those labels are the channels. (If the modal text is hard to parse, `mcp__Claude_in_Chrome__javascript_tool` reading the dialog's radio labels is the fallback.)
8. **Close the composer WITHOUT posting.** Click **Back**, then the **X**, and discard the draft if prompted. NEVER click **Post** in this step — discovery must never publish anything.

### Discover newsletters (optional)

If the writer asks about newsletters, or the piece is a recurring-series fit, also `navigate` to `https://www.linkedin.com/mynetwork/network-manager/newsletters/` and `get_page_text` to list the newsletters they own or co-author. Each newsletter is tied to a host (personal profile or a Page) — note the host alongside the newsletter name, because publishing a newsletter issue happens under that host's actor.

### Present and record the choice

Present the discovered channels with `AskUserQuestion` (single select), one option per channel — e.g. "Dorian Cougias (personal)", "MoxyWolf LLC (company page)", "STIGViewer® (company page)", plus any newsletters as "<name> (newsletter on <host>)". Recommend the channel whose audience matches the persona in `01-delegation.md`.

Persist the pick — you stamp it into the LinkedIn frontmatter (STEP 5a / 5d) and the posting reminders (STEP 8):

- `linkedin_channel: <display name>`
- `linkedin_channel_type: personal | company-page | showcase-page | newsletter`
- `linkedin_channel_url: <profile / company / newsletter URL if known; omit if unknown>`

### If Chrome is unavailable

If the Claude in Chrome extension isn't connected, or the writer declines the browser step, don't block the whole skill. Ask the writer to name the target channel in plain text (or default to their personal profile), record it as `linkedin_channel` with an added `linkedin_channel_source: writer-supplied`, and note in the STEP 8 report that live channel discovery was skipped.

### The channel type sets the LinkedIn output shape

Once the channel is chosen, its `linkedin_channel_type` decides what LinkedIn artifacts you produce. There are two shapes.

**Personal profile** → today's default. The **feed Post is the lead surface**, and its first comment links to the canonical **blog URL** plus the 2-3 cited sources. The long-form Article is produced only if the writer ticked "LinkedIn Article" in STEP 2.

**Company or Showcase Page** → the **long-form Article always leads**, and you produce a mandatory **trio** — but in **two stages**, because the teaser exists to drive traffic to the Article and its first comment links to the Article's URL, and that URL doesn't exist until the Article is live. Don't write the teaser or the comment against a placeholder URL. Wait for the real one.

**Stage 1 (now):** write only `linkedin-article.md` — the long-form Article (STEP 5d), the destination piece. Generate its hero image too. Then **stop** and hand the Article off to be published. Frontmatter: `publish_order: 1`, `trio_stage: 1-article`.

**Stage 2 (only after the Article is published, with its real URL in hand):**

- `linkedin-post.md` — a short **teaser Post** (STEP 5a) whose whole job is to drive readers to the Article; the hook and soft CTA point at the long-form piece, not the blog. **It carries an image by default** (reuse the Article hero, or a teaser-specific image — see STEP 5a). Frontmatter: `publish_order: 2`, `trio_stage: 2-teaser`.
- `linkedin-first-comment.md` — the first comment under the teaser, carrying the **real published Article URL + the canonical blog URL + the 2-3 cited sources** (STEP 5a first-comment template, company-page variant). Frontmatter: `publish_order: 3`, `trio_stage: 2-comment`.

`/4d-blog-engine:blog-publish` triggers Stage 2 automatically right after it posts the Article and captures the URL. If the writer published the Article by hand, they re-run `/blog-social` (or hand you the Article URL) and you write Stage 2 then, dropping the real URL straight into the first comment.

Produce the trio even if the writer only ticked "Post" or only ticked "Article" in STEP 2 — on a Company/Showcase Page the lead-with-Article sequence is the house format (a deliberate, writer-confirmed default). Tell the writer plainly at Stage 1: *"<channel> is a Company Page. I'll write the lead Article now. Once it's published and you have its URL, I'll write the teaser Post (with an image) and the first comment that links back to it."*

Record the shape in each LinkedIn file's frontmatter:

- `publish_sequence: company-page-trio` (omit for the personal shape)
- `publish_order: 1 | 2 | 3` (Article = 1, teaser Post = 2, first comment = 3)
- `trio_stage: 1-article | 2-teaser | 2-comment`

## STEP 3 — Generate per-platform hook candidates

For each platform the writer selected, generate **3 candidate hooks** using formulas from `references/hook-library.md`. The per-platform formula-fit table in that file indicates which formulas land best where:

- **LinkedIn Post** — Stat-Led, Story (single-line), Contrarian work best. If Article is also selected for this piece, use a different formula on the Post than the Article so the two surfaces don't read as duplicates.
- **LinkedIn first comment** — no hook is generated. The first comment is a utilitarian payload (intro line + URL + cited sources), not a content artifact. Skip hook selection for this file.
- **LinkedIn Article** — Story, Pattern Interrupt, Bold Claim work for long-form openers.
- **Twitter Post 1** — Stat-Led, Pattern Interrupt, Question lead the thread. Must fit ≤260 chars (leave room for "🧵" or "1/").
- **Facebook** — Story (one-line), Question, Stat-Led. FB's audience tolerates conversational warmth better than LinkedIn.

Each hook must:

- Use a named formula from the library.
- Be a complete unit (no cliffhanger mid-sentence).
- Land before character 210 for LinkedIn / Facebook, or fit ≤260 chars for Twitter Post 1.
- Carry a curiosity trigger — the reader cannot guess the next sentence.
- Avoid every hook on the "Hooks to retire" list.

Present hooks to the writer via `AskUserQuestion` — one question per platform, each option showing `<formula name>: <hook text>`. Mark your recommendation. After the writer picks, persist the choice in the platform's frontmatter (`hook_formula: <name>`).

## STEP 4 — Per-platform register shifts (voice continuity, platform tone)

The voice profile is the anchor — every platform sounds like the same writer. But each platform has a register the voice should bend toward:

- **LinkedIn Article (long-form)** — closest to blog voice. Slightly more first-person, opinion-led. Surface the earned secret in the first third.
- **LinkedIn Post (feed)** — same voice, compressed. One earned-secret-anchored line in the middle. Conversational but professional. No outbound links in the body — the first comment carries them.
- **LinkedIn first comment** — register shifts OFF here. The first comment is utilitarian, not voicey: a friendly one-liner inviting research, the blog URL, and the source citations the Post quoted inline. Write it as a reader-respecting service note, not as another voice performance.
- **Twitter thread** — most compressed register. Drop articles ("the," "a") where natural. Each post is a stand-alone thought. No setup paragraphs — the thread structure IS the setup. Slightly more declarative, less hedging.
- **Facebook post** — warmer, more conversational than LinkedIn. Personal-essay register. OK to open with "Last week," or "I keep thinking about…" — language that would feel too soft on LinkedIn lands fine on FB.

The voice profile's rules (no em-dashes, contractions, two-reader frame, etc.) still apply on every platform except the first comment. The register shift is *tone within voice*, not a different voice.

## STEP 5a — Write the LinkedIn Post + first-comment pair (if selected)

Both files are produced together — never one without the other. The Post plays one of two roles, set by `linkedin_channel_type` (STEP 2b):

- **Personal profile → lead Post.** The feed Post is the main event. Its earned-secret line and soft CTA carry the argument; the first comment links to the **blog URL** + sources.
- **Company/Showcase Page → teaser Post.** The Post is the trio's `publish_order: 2` piece, written in **Stage 2** (only after the Article is live). Its job is to pull readers to the lead Article. Keep the same feed-post spec below, but aim the hook and the soft CTA at the long-form piece ("the full breakdown is in the comments / linked below"), and the first comment links to the **real published Article URL** + blog URL + sources. The teaser **carries an image by default** — a text-only post hides its link in the first comment, so it has no preview card, and an image is what stops the scroll (LinkedIn doesn't throttle images the way it throttles in-body links). Reuse the Article hero for campaign cohesion, or generate a teaser-specific image; record it in the `image:` frontmatter field.

### Post (feed)

Targets:

- **Char count:** 1,300-2,500 (sweet spot). **2,900 hard cap** — LinkedIn rejects posts over 3,000 chars, and the script enforces the safety margin. If your draft exceeds 2,900, compress before saving.
- **Word count:** ~200-500.
- **Hook:** the user-picked Post hook from STEP 3, landing complete before char 210 (the mobile-fold "See more" cutoff).
- **Body structure:** 3 acts — `Hook → Stakes/Setup → Soft CTA`. One earned-secret line woven into the middle (one sentence, concrete, never a story arc — that's the Article's job if it was selected).
- **Closing line:** a specific question naming a concrete decision the reader is actually facing. Not "What do you think?" or "Agree?"
- **Hashtags:** 0-3, at the very end after a line break.
- **Formatting:** LinkedIn-native — single-line paragraphs, generous whitespace. NO markdown tables. NO markdown bold-italic stacks.
- **External links:** ZERO in the body. The blog URL and source citations go in the companion `linkedin-first-comment.md` file. This is what makes the Post format strategy work — link-in-body posts get throttled by ~25-60% on reach.

Save to `<piece>/04-diligence/social/linkedin-post.md` with frontmatter:

```yaml
---
type: linkedin-post
source_blog: <piece>/04-diligence/blog.md
companion_file: linkedin-first-comment.md
hook_formula: <name>
audience: <persona from 01-delegation.md>
linkedin_channel: <from STEP 2b>
linkedin_channel_type: <personal | company-page | showcase-page | newsletter>
publish_sequence: <company-page-trio — include only for a Company/Showcase Page; omit on personal>
publish_order: <2 — include only in the company-page trio (Article=1, Post=2, comment=3)>
trio_stage: <2-teaser — include only in the company-page trio>
links_to_article: <true for the company-page teaser; omit on personal>
image: <teaser image filename — required on the company-page teaser; reuse the Article hero or a teaser-specific image>
target_chars: 1800
posting_notes:
  post_as: "<linkedin_channel> — switch the 'Post as' actor to this before pasting"
  link_placement: first-comment-file
  hashtag_count_max: 3
  best_window: "Tue/Wed/Thu 7:30-8:30 AM PT"
---
```

### First comment (companion to the Post)

Targets:

- **Char count:** 80-1,200 (LinkedIn's comment limit is ~1,250; stay under it with margin).
- **Voice:** OFF. This is a utilitarian service note, not voice prose.
- **Structure depends on the channel type (don't improvise either template):**

  **Personal profile (links to the blog):**

  ```
  If you want to do your own research, here are the cited sources in my article:
  <blog-url>

  1. <source-1-title> — <source-1-url>
  2. <source-2-title> — <source-2-url>
  3. <source-3-title> — <source-3-url>
  ```

  **Company/Showcase Page (the trio — links to the published Article first, then the blog, then sources):**

  ```
  Full long-form piece here:
  <LINKEDIN_ARTICLE_URL>

  More on the blog:
  <blog-url>

  Sources:
  1. <source-1-title> — <source-1-url>
  2. <source-2-title> — <source-2-url>
  3. <source-3-title> — <source-3-url>
  ```

  Because the company-page comment is written in **Stage 2** (after the Article is live), drop the **real published Article URL** straight in — you have it by now. Only if you're somehow writing the comment before the Article URL exists, use the literal `<LINKEDIN_ARTICLE_URL>` placeholder as a fallback, and `/4d-blog-engine:blog-publish` (or the writer) substitutes the real URL before the comment goes up.

- **Which sources to include:** only the 2-3 citations the Post text **quotes inline** (e.g. the Anthropic stat, the 269-row catalog count). Do **not** include the full bibliography from the blog — those live on the blog post itself, not in the comment. If the Post quotes zero external sources, the comment still gets the intro line + the URL(s) (the sources block is just omitted).
- **No hashtags.** No emoji as bullets. Sequential numbering 1, 2, 3.
- **URL handling:** bare URLs only. LinkedIn auto-links them on render. Don't use markdown link syntax `[title](url)` — the comment box renders as plain text.

Save to `<piece>/04-diligence/social/linkedin-first-comment.md` with frontmatter:

```yaml
---
type: linkedin-first-comment
source_blog: <piece>/04-diligence/blog.md
companion_to: linkedin-post.md
linkedin_channel_type: <personal | company-page | showcase-page>
publish_sequence: <company-page-trio — include only for a Company/Showcase Page; omit on personal>
publish_order: <3 — include only in the company-page trio>
trio_stage: <2-comment — include only in the company-page trio>
links_to: <blog for personal; article+blog for the company-page trio>
target_chars: 600
posting_notes:
  paste_as: "the first comment under the published Post, as the SAME actor the Post was published as (<linkedin_channel>)"
  inline_sources_only: true
  article_url_placeholder: "<LINKEDIN_ARTICLE_URL> — blog-publish substitutes the real Article URL after posting the Article (company-page trio only)"
---
```

The opening lines are fixed for now — *"If you want to do your own research, here are the cited sources in my article:"* for the personal template, *"Full long-form piece here:"* for the company-page template — keep the phrasing verbatim unless the writer overrides it via a follow-up edit. The verbatim phrasing is what we've calibrated against; rewording it ad-hoc each time defeats the calibration.

## STEP 5d — Write the LinkedIn Article (lead piece on company pages; optional on personal)

Generate this file when **either** holds:

- The channel is a **Company/Showcase Page** (STEP 2b) — the Article is the **lead piece** of the trio (`publish_order: 1`) and is always produced, even if the writer didn't tick "Article" in STEP 2.
- The channel is **personal** AND the writer explicitly selected **"LinkedIn Article (long-form)"** in STEP 2.

If neither holds (personal channel, Article not ticked), skip this section entirely.

Targets:

- **Word count:** 800-1200.
- **Char count band:** 4,000-9,000 (validated by `social_score.py --type article`).
- **Tone:** more personal and opinion-led than the blog; earned secret surfaces in the first third.
- **First 2-3 lines:** the "See more" hook (the formula the writer picked for the Article). Never "I'm excited to share."
- **Formatting:** LinkedIn-native — bold for emphasis (sparingly), single-line paragraphs, generous whitespace. NO markdown tables (LinkedIn renders as raw text). NO markdown bold-italic stacks.
- **Citations:** 2-3 sourced statistics carrying the FLOW evidence triple (year + publisher + URL). Inline citations are fine in the Article (different surface from the Post — Articles aren't penalized the same way).
- **Ending:** an engagement question — specific, not "What do you think?" or "Agree?"

Save to `<piece>/04-diligence/social/linkedin-article.md` with frontmatter:

```yaml
---
type: linkedin-article
source_blog: <piece>/04-diligence/blog.md
hook_formula: <name>
audience: <persona from 01-delegation.md>
linkedin_channel: <from STEP 2b>
linkedin_channel_type: <personal | company-page | showcase-page | newsletter>
publish_sequence: <company-page-trio — include only for a Company/Showcase Page; omit on personal>
publish_order: <1 — include only in the company-page trio (the Article leads)>
trio_stage: <1-article — include only in the company-page trio>
image: <Article cover image — reuse the blog/Article hero>
share_blurb: "<the 'tell your network what your article is about' text LinkedIn prompts for when you hit Publish on an Article — ~250-300 chars, hook before char 210, in voice; this rides the Article card on the page feed>"
target_words: 1000
posting_notes:
  post_as: "<linkedin_channel> — publish the article from this actor's 'Write article' surface"
  link_placement: inline-ok
  hashtag_count_max: 5
  best_window: "Tue/Wed/Thu 7:30-8:30 AM PT"
  trio_role: "company-page lead — publish FIRST; its URL feeds the teaser Post's first comment"
---
```

## STEP 5b — Write the Twitter thread (if selected)

Targets:

- **Posts:** 5-10. Sweet spot is 6-8. Anything under 5 fits better as a LinkedIn teaser; anything over 10 loses engagement past the fold.
- **Per-post limit:** ≤280 chars. Hard cap. The script enforces this — there is no soft fallback.
- **Layout:** each post is its own `## Post N` block. Post 1 is the hook. Post N (the final post) closes the loop and contains the blog URL + ≤2 hashtags total across the thread.
- **Voice:** compressed register (see STEP 4). Each post is a stand-alone thought; the reader can stop after any post and have gotten value.
- **Earned-secret placement:** somewhere in posts 2-4 (not buried at the end). One concrete sentence.
- **Numbering:** sequential 1, 2, 3, … The script checks this.
- **No emoji-as-bullet patterns** — don't use 👇 to "point to" the next post. The thread structure points itself.

Save to `<piece>/04-diligence/social/twitter-thread.md`. The file structure:

```markdown
---
type: twitter-thread
source_blog: <piece>/04-diligence/blog.md
hook_formula: <name>
audience: <persona from 01-delegation.md>
target_posts: 7
posting_notes:
  link_placement: final-post
  hashtag_count_max: 2
  best_window: "Tue/Wed/Thu 9:00-11:00 AM PT"
---

## Post 1

<hook post — ≤260 chars to leave room for "🧵" or "1/">

## Post 2

<post text — ≤280 chars>

## Post 3

<post text — ≤280 chars>

… (continue through final post)

## Post N

<closing post with blog URL and up to 2 hashtags>
```

## STEP 5c — Write the Facebook post (if selected)

Targets:

- **Char count:** 300-500 (allowed range 200-800). Facebook's algorithm favors mid-length posts; super-short posts read as shallow, super-long ones get truncated with "See more."
- **Word count:** 60-150.
- **Hook:** the user-picked Facebook hook from STEP 3.
- **Voice:** warmer than LinkedIn. Personal-essay register. OK to open with a temporal anchor ("Last week…", "I keep thinking about…").
- **External link:** the blog URL goes **in the body** (Facebook renders a preview card; this is the only platform where the link belongs inline).
- **Hashtags:** 0-2 total, at the end after a line break.
- **Earned-secret:** one sentence, conversational framing.

Save to `<piece>/04-diligence/social/facebook-post.md`:

```yaml
---
type: facebook-post
source_blog: <piece>/04-diligence/blog.md
hook_formula: <name>
audience: <persona from 01-delegation.md>
target_chars: 400
posting_notes:
  link_placement: body
  hashtag_count_max: 2
  best_window: "Weekdays 1:00-3:00 PM PT"
---
```

## STEP 6 — Format compliance check

Run the format checker against every file produced. The script lives at `${CLAUDE_PLUGIN_ROOT}/scripts/social_score.py`. One call per file:

```bash
# LinkedIn Post + first comment (the default LinkedIn pair)
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/social_score.py \
  --file <piece>/04-diligence/social/linkedin-post.md --type post \
  --out <piece>/04-diligence/social/scorecards/linkedin-post.score.md

python3 ${CLAUDE_PLUGIN_ROOT}/scripts/social_score.py \
  --file <piece>/04-diligence/social/linkedin-first-comment.md --type first-comment \
  --out <piece>/04-diligence/social/scorecards/linkedin-first-comment.score.md

# LinkedIn Article (only if selected)
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/social_score.py \
  --file <piece>/04-diligence/social/linkedin-article.md --type article \
  --out <piece>/04-diligence/social/scorecards/linkedin-article.score.md

# Twitter thread
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/social_score.py \
  --file <piece>/04-diligence/social/twitter-thread.md --type twitter-thread \
  --out <piece>/04-diligence/social/scorecards/twitter-thread.score.md

# Facebook post
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/social_score.py \
  --file <piece>/04-diligence/social/facebook-post.md --type facebook-post \
  --out <piece>/04-diligence/social/scorecards/facebook-post.score.md
```

Each call emits a scorecard scaffold (with 3-axis judgment scores empty) and a JSON sidecar with deterministic findings. Exit code 1 means format checks failed — fix the issues (length, hook position, per-post char limit, hashtag placement, external-link-in-body for LinkedIn Post) and re-run. **Don't proceed to STEP 7 until every file returns exit code 0.**

For the LinkedIn Post specifically: if char count exceeds 2,900, the script flags it. Compress — there is no auto-truncate fallback. The 2,900 cap exists because LinkedIn rejects posts over 3,000 chars, and we keep a 100-char safety margin for typographic-quote substitution and any trailing-whitespace surprises.

For the first-comment file specifically: the script requires at least one URL in the body (opposite of the Post rule). A first-comment with no URLs has nothing useful for the reader; it fails the check.

For Twitter: if any single post is over 280 chars, the script flags it. Rewrite that post — there is no auto-truncate fallback.

## STEP 7 — Fill in the 3-axis scorecard for each content artifact

The format checker produces a scaffold per artifact; you (the LLM) fill in three /10 scores by judgment for each scorecard file. For each axis:

- **Thought leadership /10** — Is the insight non-obvious enough that a senior practitioner would forward this to a peer? 10 = "I hadn't thought of it that way" reaction guaranteed. 5 = competent restatement of conventional wisdom. 0 = generic.
- **Pain (lands on the reader, not a third party) /10** — Does the pain land on the reader's own job/identity/recent week, or on a third party they observe? 10 = the reader thinks "this is about me." 5 = "this is about someone I know." 0 = abstract pain on no one in particular.
- **Audience fit /10** — Does the post speak to the persona declared in `01-delegation.md`, using their vocabulary and decision context? Twitter and Facebook each have their own audience flavor — a great LinkedIn post can be a mediocre Twitter post if the register doesn't shift. Score for the platform's audience, not the blog's.

Each score needs a **one-sentence justification** — specific, not generic.

Recommendation per artifact: ship if all three axes ≥ 7. Revise if any axis is 4-6. Discard if any axis is ≤ 3.

**Exception — `linkedin-first-comment.md` skips the 3-axis scorecard.** The first comment is a utilitarian service note, not a content artifact. The format checker still runs on it (URL-present check, length band, hashtag/emoji-bullet sanity), but the scorecard scaffold for the first-comment file is just a one-line "deterministic check only — no LLM-judgment axes apply" note. Don't try to score it on thought leadership / pain / audience fit.

## STEP 8 — Update state and report

Append to `<piece>/state.md`:

```
- [x] Social derivatives produced (<platform list>)
```

And to the process log: `<ISO> — Social derivatives: <platform list>; axes <T>/10, <P>/10, <A>/10 per platform.`

Report to the writer:

```
Social derivatives produced.

LinkedIn channel:       <linkedin_channel> (<type>)   [only if a LinkedIn surface was produced]
LinkedIn shape:         <company-page trio (Article → teaser Post → first comment) | personal (Post + first comment)>
LinkedIn Article:       <piece>/04-diligence/social/linkedin-article.md (<words> words)   [lead piece on a company page; optional on personal]
LinkedIn Post:          <piece>/04-diligence/social/linkedin-post.md (<chars> chars)   [teaser on a company page]
LinkedIn first comment: <piece>/04-diligence/social/linkedin-first-comment.md (<chars> chars)
Twitter Thread:         <piece>/04-diligence/social/twitter-thread.md (<N> posts)
Facebook Post:          <piece>/04-diligence/social/facebook-post.md (<chars> chars)

Scorecards: <piece>/04-diligence/social/scorecards/
  Per content artifact: thought leadership /10, pain /10, audience fit /10
  Recommendation per artifact: ship | revise | discard
  (Note: linkedin-first-comment.md is a utilitarian payload — format-check only, no 3-axis scoring.)

Posting reminders:
  - COMPANY-PAGE TRIO (when <linkedin_channel> is a Company/Showcase Page), post in this ORDER:
      1. Article first. Publish linkedin-article.md via "Write article" as <linkedin_channel>.
         Copy its published URL — you need it for step 3.
      2. Teaser Post second. Switch "Post as" to <linkedin_channel>, paste the POST body
         and attach its image (the `image:` file). NO link in the body. It points readers
         to the Article.
      3. First comment third. Under the teaser Post, as the SAME actor, paste
         linkedin-first-comment.md — but replace <LINKEDIN_ARTICLE_URL> with the
         Article URL you copied in step 1. It carries the Article link + blog URL + sources.
      Best window: Tue/Wed/Thu 7:30-8:30 AM PT.
  - PERSONAL PROFILE (when <linkedin_channel> is your personal profile):
      Switch "Post as" to your profile, paste the POST body (NO link in the body).
      As soon as it publishes, paste linkedin-first-comment.md as the FIRST COMMENT
      under the post — it carries the blog URL and sources. (Article only if you made one.)
      Best window: Tue/Wed/Thu 7:30-8:30 AM PT.
  - Twitter: blog URL in FINAL POST. Best window: Tue/Wed/Thu 9:00-11:00 AM PT.
  - Facebook: blog URL in BODY (renders preview card). Best window: weekdays 1:00-3:00 PM PT.

The plugin does NOT auto-publish to any platform. Paste and post by hand on each platform.

Next step — ship these files to your repo so a teammate or downstream automation
can pick them up:

  /4d-blog-engine:blog-publish <slug>

The publish skill detects this `social/` directory and includes the .md files
plus scorecards in the same commit as the post. The blog post itself gets
treated as a republish (dateModified bump → site rebuild). If the post was
already published before social existed, this is how the social files reach
the repo.
```

(Only list the platforms the writer actually selected.)

## What this skill does NOT do

- It does NOT modify the signed blog. The blog is canonical and read-only after the Release Owner signs.
- It does NOT post to LinkedIn, Twitter/X, or Facebook on the writer's behalf. The writer pastes by hand on each platform. This is intentional — see the whitepaper's Diligence ethos.
- It does NOT ship the derivative files into the writer's publishing repo. The files land under `<piece>/04-diligence/social/` only — `/4d-blog-engine:blog-publish` is the skill that copies them into the GitHub repo (auto-detected on its next run for the same slug). Keeping the publish step in one skill avoids two skills both writing into the repo.
- It does NOT generate carousels, video clips, infographics, or YouTube descriptions — that's outside scope. Article + teaser (LinkedIn), thread (Twitter), single post (Facebook) — that's the scope.
- It does NOT auto-invoke after Phase 4 sign-off. The writer runs `/4d-blog-engine:blog-social` explicitly when they want derivatives.

## Degradation behaviors

- **social_score.py fails to run** (Python error): treat as a script bug and surface it; fall back to the format rules in `references/hook-library.md` checked manually.
- **Writer picks `[skip hook selection]`:** generate the recommended hook automatically but flag in the platform's frontmatter that the human did not pick.
- **The signed blog won't compress to a given platform** (too technical for Twitter, too short to make a 7-post thread, etc.): surface the issue per platform ("the source post's argument doesn't compress to a Twitter thread — recommend skipping Twitter for this piece"). Do not force-fit.
- **Twitter thread comes out under 5 posts after compression attempts:** report and suggest a LinkedIn teaser as the better fit. Don't pad with filler posts to hit the minimum.
- **Claude in Chrome not connected, or LinkedIn session walled (STEP 2b):** don't block the skill. Fall back to asking the writer to name the channel in plain text (or default to their personal profile), record it with `linkedin_channel_source: writer-supplied`, and note in the report that live channel discovery was skipped. Never publish anything during discovery — STEP 2b only reads the "Posting as" list and closes the composer without posting.
