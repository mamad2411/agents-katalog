---
name: launch-ready
description: "Put a deployed, healthy app in front of real users without shipping AI-slop. Owns landing page, positioning, launch-day SEO, Open Graph cards, waitlist and email funnel, launch channels (Product Hunt, Show HN, Reddit, X, IH, dev.to, LinkedIn), press outreach, launch-day telemetry, and the D-7 to D+7 runbook. Refuses AI-slop landings, hero-fatigue copy, spec-sheet positioning, paper waitlists, unrendered OG cards, and silent launches (launch-day signups with no source attribution). Triggers on 'launch my product,' 'build a landing page,' 'Product Hunt,' 'Show HN,' 'waitlist,' 'OG card,' 'launch-day SEO,' 'press kit,' 'launch week plan.' Does not build the app (production-ready), deploy it (deploy-ready), monitor it (observe-ready), pick tools (stack-ready), or own ongoing marketing. Pairs with deploy-ready and observe-ready. Full trigger list in README."
version: 3.1.0
updated: 2026-11-23
changelog: CHANGELOG.md
suite: ready-suite
tier: shipping
upstream:
  - production-ready
  - stack-ready
  - deploy-ready
  - observe-ready
downstream: []
pairs_with:
  - deploy-ready
  - observe-ready
compatible_with:
  - claude-code
  - codex
  - cursor
  - windsurf
  - antigravity
  - pi
  - openclaw
  - any-agentskills-compatible-harness
---

# Launch Ready

This skill exists to solve one specific failure mode. An app is deployed, healthy, green in observe-ready. The founder has eight weeks of runway and one shot at getting people to notice. What ships is a gradient-hero landing page with six shadcn cards whose feature copy uses the word "seamless" three times and "powerful" four times, an OG image that previews at 600x315 on LinkedIn and does not render at all on iMessage, a waitlist form that captures emails but has no nurture sequence queued, a Show HN post titled "Launch HN: We built X for Y" that gets flagged in seven minutes, a Product Hunt post scheduled for 9am ET because nobody mentioned 12:01 AM PT, a launch thread on X that goes out without UTM parameters so the founder cannot tell which post drove the four signups, and a follow-up plan that is a single calendar block labeled "do launch." None of these are bugs. They are launch-mechanics failures, and the tooling that exists (Framer, Carrd, Kit, PostHog, Plausible) has no opinion about any of them.

The job here is the opposite. Produce a landing page whose hero names the audience and the existing workaround specifically enough that a competitor cannot make the same claim, OG cards verified to render in five channels before a single link ships, a waitlist with a written nurture sequence that executes on launch day and again at D+3 and D+7, launch-channel posts that follow each venue's actual etiquette (Show HN title conventions, PH 12:01 AM PT timing, Reddit 9:1 non-promotional ratio, LinkedIn founder-voice format), UTM-tagged every shared link so the D+1 waterfall can answer "where did the fourteen signups come from," and a D-7 to D+7 runbook that names who does what at what hour of what day. If a launch cannot answer "what will the landing page say, who will read it, and how will we know if it worked," it is not ready to ship.

This is harder than it sounds because launch is a *communication* system layered on top of a product system. A single launch day touches the landing page, the copy, the visual identity, the OG render pipeline, the meta tags, the schema.org markup, the sitemap, the waitlist integration, the double opt-in flow, the email service, the analytics stack, the UTM taxonomy, the CDN and cache policy for a traffic spike, the status page, the PH post and hunter, the HN submission, the Reddit thread, the X thread, the LinkedIn post, the IH milestone, the dev.to article, the press kit, and the D+1 through D+7 follow-up cadence. If any one of these is papered over, the whole launch collapses into a cosmetic campaign that looks like a launch and is not one.

## Core principle: every claim must survive the substitution test

Do not design a launch as if attention is the problem. Attention is downstream. The problem is that AI-generated launch surfaces collapse into interchangeable slurry: the hero sentence, the feature cards, the testimonial quote, the OG card, the launch post, the email subject line, are each writable by any model for any product in the category because they say nothing a competitor could not also say. launch-ready's load-bearing discipline is:

> Every user-facing sentence, image, and asset must fail the substitution test: if a direct competitor's name could be swapped in without the sentence becoming false or absurd, the sentence is not specific enough to ship. This applies to the hero, the sub-hero, every feature card, the pricing table's value prop, the waitlist pitch, the OG title, the meta description, the PH tagline, the Show HN title, and the first line of the launch email.

This principle is non-negotiable. An AI-generated landing page with a hero reading "Empower your team with AI-powered productivity" fails this test in one sentence: the same sentence describes Notion, Asana, ClickUp, Monday, Linear, Jira, and every other SaaS in the decade. It is hero-fatigue copy. A landing page shipped with that hero is an AI-slop landing. The skill refuses to accept it as a deliverable.

The substitution test has a corollary in every step of the skill. Positioning (Step 1) fails it when the "who is this for" line names a persona generic enough that any competitor's marketing fits. The feature grid (Step 2) fails it when the six cards could be reordered into any B2B SaaS landing page without breaking meaning. The OG card (Step 6) fails it when the card could be pasted onto a competitor's blog post without visible wrong-ness. The Show HN title (Step 8) fails it when the title does not say what the product does specifically enough for an HN reader to click from the title alone. Launch-ready enforces the substitution test as a grep-testable, sentence-by-sentence discipline; see `references/positioning-and-copy.md` section 2 for the exact procedure.

## When this skill does NOT apply

Route elsewhere if the request is:

- **Building the app** ("wire the users page," "add RBAC to the dashboard," "implement the feature the landing page advertises"). That is `production-ready`. launch-ready reads `.production-ready/STATE.md` to know which features actually ship so the landing page does not promise vapor, and it reads the visual-identity tokens and brand palette as upstream artifacts. It does not change the app.
- **Deploying the app** ("set up the pipeline," "run the migration," "write the rollback plan"). That is `deploy-ready`. launch-ready assumes the app is live. It notes the public URL and the deploy target, nothing else.
- **Monitoring the app** ("add Datadog," "define an SLO," "write a runbook for API down"). That is `observe-ready`. launch-ready consumes observe-ready's alert hooks so the launch-day traffic spike does not collapse undetected, and it reads `.observe-ready/SLOs.md` to know what availability the app actually promises.
- **Picking the landing-page tool or the waitlist tool** ("Framer vs. Webflow," "Kit vs. Loops," "@vercel/og vs. Bannerbear"). That is `stack-ready`. launch-ready assumes the tool choice exists; it enforces what any chosen tool must actually produce.
- **Repo hygiene and CI** ("CONTRIBUTING.md," "CODEOWNERS," "release automation"). That is `repo-ready`. launch-ready's landing-page repo (if separate from the app repo) inherits repo-ready's discipline.
- **Product telemetry inside the app** (feature adoption, retention cohorts, in-app funnels, session replay for the signed-in experience, A/B testing the pricing page). That is `production-ready`'s `references/analytics-and-telemetry.md`. launch-ready owns only the launch-campaign telemetry: where did this visitor come from, did they sign up, did they activate. Keep the line bright: if the question is "did feature X's adoption go up week over week," it is not launch-ready's question. If the question is "of the 4,200 visitors who arrived from the PH post, how many signed up and how many completed onboarding," it is.
- **Transactional email** (password reset, order confirmation, receipt, in-app notification). That is `production-ready`'s `references/notifications-and-email.md`. launch-ready owns only the waitlist and launch email funnel.
- **Ongoing marketing**. Content marketing cadence, SEO-as-practice, sustained email nurturing past the D+14 window, paid acquisition campaigns, influencer partnerships beyond launch week. launch-ready owns the launch. Ongoing marketing is a different discipline and is out of scope for this skill.
- **Pricing strategy** (what to charge, freemium vs. paid, billing model). That is a business decision. launch-ready owns only the *display* of pricing on the landing page and the "is the price visible above the fold" discipline.
- **Brand identity in the deep sense** (logo design, full design system, typography scale). launch-ready assumes `production-ready`'s visual-identity framework has produced the palette and typography tokens. It uses them; it does not redecide them.
- **Customer support tooling** (Zendesk, Intercom, Plain setup). Out of scope.
- **Legal copy** (privacy policy, terms of service, GDPR consent banner text). launch-ready flags the requirement and points at a legal review; it does not draft the text.
- **App Store / Play Store listings.** Mobile app launches share some discipline (screenshot discipline, description specificity) but have venue-specific rules (keyword optimization, subtitle limits, promotional text) that are out of scope. launch-ready focuses on web-app launches.

This section is the scope fence. Every plausible trigger overlap with a sibling has a route-elsewhere line.

## Workflow

Follow this sequence. Skipping steps produces the exact class of failure this skill exists to prevent: a launch that ships and nobody notices, or worse, a launch that gets noticed and collapses under its own lack of specificity.

### Step 0. Detect launch state and mode

Read `references/launch-research.md` and run the mode detection protocol.

- **Mode A (Pre-launch, greenfield).** No landing page, no waitlist, no prior launch. Start from positioning.
- **Mode B (AI-slop landing exists).** A landing page has been generated by Claude / Cursor / Lovable / v0 / Bolt / Framer AI and it fails the substitution test. The ask is "fix this before the launch." Rewrite positioning, rewrite copy, keep structure only if it survives the specificity audit.
- **Mode C (Re-launch / pivot).** A prior launch happened. Positioning has shifted. The ask is "launch the new story without confusing the old audience." Treat as Mode A with a legacy-messaging audit added.
- **Mode D (Rescue / no traction).** Launched to silence. Diagnose: was it positioning (nobody knew what it was), venue (posted to the wrong channel or at the wrong hour), amplification (no thread, no hunter, no list), or capture (waitlist was not wired, no follow-up). Then remediate the dominant cause before re-launching.
- **Mode E (Quiet launch / B2B direct).** No broad launch channels. Positioning and landing page matter; PH / HN / Reddit do not. Skip Steps 8 and 9 for launch channels; keep everything else.

**Passes when:** a mode is declared and the corresponding research block from `launch-research.md` is produced. For Mode D, the dominant failure cause is named in writing before any remediation step.

### Step 1. Positioning and the substitution test

Read `references/positioning-and-copy.md`. Positioning is upstream of every surface in the launch; no landing page or OG card or launch post can outperform weak positioning.

Produce, in writing:

1. **Who is this for.** One sentence. Must name a role or a context specific enough that a competitor cannot use the same sentence. "For small teams" fails. "For three-person engineering teams whose first hire quits on a Friday and whose runway is eleven months" passes the substitution test.
2. **What it replaces.** One sentence. The existing workaround the audience is using today. "A Notion page and a Slack channel." "Five rows in a Google Sheet." "A cron job and a prayer." Replacement-framed positioning is what April Dunford's *Obviously Awesome* calls the competitive alternative frame; it beats feature-framed positioning in every test published on marketingexamples.com and julian.com/guide/growth.
3. **What it does differently.** One sentence. The thing the replacement cannot do. Must be concrete. "Faster" fails; "runs the eight-step checklist as one command" passes.
4. **The differentiator test.** For the sentence in (3), write the competitor's rebuttal. If the competitor's rebuttal is "we do that too," the sentence is not a differentiator. Rewrite until the rebuttal is either "we do not do that" or "we do the opposite."
5. **Tone of voice.** One paragraph on how the product speaks. Bullet the three adjectives that describe the voice (e.g., "direct, technical, quietly funny"). Bullet the three anti-adjectives (the tones the launch deliberately does not use; e.g., "corporate, breathless, aspirational").

**Substitution test gate.** Paste each of the four sentences into the template: "[COMPETITOR NAME] also [the sentence]." If the resulting sentence is plausible for two or more named competitors, rewrite. The skill does not accept a positioning document where the four sentences survive this substitution.

**Mode B shortcut:** the existing landing page's hero copy, sub-hero, and feature headlines each go through the substitution test first. Anything that fails is rewritten before any other step.

**Passes when:** the four positioning sentences are written, the tone paragraph is written, the substitution test has been applied to each sentence with the competitor rebuttal recorded, and every sentence has survived.

### Step 2. Landing page anatomy

Read `references/landing-page-anatomy.md`. The landing page has five canonical sections. They are not optional and they are not rearrangeable.

1. **Hero.** Above the fold on a 1366x768 viewport. Contains: headline (one sentence, survived Step 1), sub-headline (one sentence, adds the differentiator), one primary CTA, optional social-proof micro-row (logos, user count, "as seen in"). That is the complete list. No hero illustration clusters. No scrolling carousel. No three-CTA choose-your-adventure.
2. **Social proof.** Single row. User count with a date, three to eight customer logos (only if actually using), one pull quote with a real name and a real company. If none of those three are available, this section is a single line: "Built by [named founder] after [specific frustration]." Do not fabricate logos. Do not use generic "as seen in" badges for publications that have not covered the product.
3. **Feature grid.** Three to six tiles. Not seven. Not eight. Not twelve. Each tile has: an icon (from the installed icon library, not an emoji and not a gradient-filled blob), a headline (substitution-test-passing), one-sentence description. No "Learn more" links that go nowhere. If more than six features matter, the landing page is trying to do the job of the product's documentation; split them out.
4. **Pricing (if applicable).** Visible above the scroll, not buried. Real numbers. Max three tiers. Each tier names the one audience it serves. No "Contact us" on a self-serve product's public pricing.
5. **CTA.** Primary action: sign up, join waitlist, or start trial. Single verb. Named outcome. Below the fold, a secondary CTA can appear (demo, docs, pricing); above the fold, one CTA.

Anti-patterns to reject in this step (each covered in `landing-page-anatomy.md`):

- **Gradient hero with no headline specificity.** The aesthetic dominates; the sentence says nothing.
- **Three-column icon grid with no differentiation per tile.** Each tile is a category ("Fast," "Secure," "Scalable") rather than a capability specific to this product.
- **Carousel above the fold.** Moving visual content steals attention from the headline and punishes slow connections.
- **Video-first hero with autoplay.** Increases bounce; defeats the substitution test because the sentence the viewer reads is whatever the video captions happen to freeze on.
- **Stock illustrations of abstract people pointing at charts.** Swipe Files' running critique of the shadcn-default aesthetic applies.
- **Five-plus-CTA hero.** "Sign up, demo, pricing, docs, blog" all above the fold. No action is emphasized; all are diluted.

**Passes when:** the five sections exist in the correct order; the hero fits above the 1366x768 fold; the feature grid has three to six tiles, each substitution-test-passing; pricing (if applicable) is visible above the scroll with real numbers; a single primary CTA dominates the hero.

### Step 3. Copy discipline (the banned-word audit)

Read `references/positioning-and-copy.md` section 4.

Run the banned-word audit against every word on the landing page. The banned-or-flagged words below are the AI-slop signature set:

| Banned | Replace with |
|---|---|
| **seamless** | "in one step," "without switching tabs," or name the specific integration. |
| **powerful** | the specific capability. "Queries Postgres and S3 in the same request." |
| **revolutionary** | the specific new thing. "First tool to run schema migrations inside the same transaction as the backfill." |
| **effortless** | the number of clicks or steps eliminated. "Two fewer clicks than the incumbent workflow." |
| **intelligent** | the specific technique. "Uses the customer's prior responses to pre-fill the form." |
| **cutting-edge** | the version or year. "Built on the OpenAI December 2025 completions API." |
| **game-changing** | the metric that changed. "Reduces median onboarding from three days to eleven minutes." |
| **unlock** | the thing unlocked. "Gives every engineer their own staging environment without the DevOps ticket." |
| **supercharge** | the before and after. "One prompt replaces a forty-line YAML config." |
| **elevate** | the specific upgrade. "Turns the weekly ops review into a one-click dashboard." |
| **streamline** | the removal. "Removes the approval step entirely." |
| **empower** | the action enabled. "Non-engineers ship changes without filing a ticket." |
| **robust** | the threshold. "Survives the 50K QPS the prior system collapsed at." |
| **solution** (as a noun for the product) | name the product or the action it performs. |
| **best-in-class, leading, enterprise-grade, world-class** | drop entirely or replace with a specific number. |

The banned-word list is not a style guide. It is a signature of AI-slop copy that grep can detect. An AI-generated landing page that uses three or more words from this list above the fold ships in Mode B shape; it is rewritten before the launch proceeds.

Additional copy rules:

- **Active voice, second person.** "You ship faster" beats "Your team will be enabled to ship faster."
- **Named subjects.** The founder's voice beats the company-we voice. "I built this after [specific incident]" beats "Our team is passionate about solving [category]."
- **Concrete over abstract.** Numbers, dates, names, before/after contrasts. If a sentence would survive unchanged in a pitch deck for a different product, rewrite.
- **No AI self-reference in the hero.** Unless the product is explicitly an AI product *and the differentiator is the AI itself*, the hero does not mention AI. "AI-powered" in the hero of a non-AI product is a 2024 tell.

**Passes when:** a grep across the landing page HTML / content source against the banned-word list returns zero hits above the fold, or each surviving hit has a one-line justification in the copy review notes. Every hero sentence passes the substitution test. The tone matches the Step 1 tone paragraph.

### Step 4. Visual identity and the aesthetic test

Read `references/visual-identity.md` (packaged inline within `landing-page-anatomy.md`).

launch-ready does not redecide brand; it consumes `.production-ready/visual-identity.md` if present. If absent, launch-ready produces a minimum viable visual identity:

- **One brand color** (not three). Saturated enough to survive on the OG card thumbnail.
- **Two supporting grays.** One for body text, one for muted UI.
- **One typeface for headlines, one for body** (can be the same). Default font stack should include the system fallback so the page is readable before the webfont loads.
- **Icon library chosen** (Lucide, Heroicons, Phosphor, Tabler, Radix). No emojis as UI markers. See production-ready's emoji discipline; launch-ready enforces the same rule for the landing page.
- **One hero image or pattern, or none.** If the hero includes an illustration, it is either (a) a real screenshot of the product or (b) a custom illustration that survives the substitution test (a competitor's site could not drop it in). Stock illustrations of people pointing at laptops fail.

**The aesthetic test.** Screenshot the landing page hero and show it to a person who has never seen the product. Ask: "What does this product do?" If the answer is generic ("some SaaS tool") rather than specific, the aesthetic is not doing its job. The skill records this test as a single-person, one-question check in the launch notes.

**Passes when:** the five tokens are declared (color, two grays, typeface(s), icon library); no emojis appear as UI markers; any hero illustration survives the substitution test; the aesthetic test has been run on at least one naive viewer.

### Step 5. Launch-day SEO fundamentals

Read `references/seo-fundamentals.md`. launch-ready owns launch-day-correct SEO, not ongoing SEO practice.

Checklist (each a hard gate):

- **One `<h1>` per page.** Exactly one. Contains the product name or the positioning's main verb.
- **`<title>` under 60 characters.** Contains the product name and the differentiator. Not "Home | Product" as the title; the title is a piece of launch copy, not a navigation label.
- **Meta description under 160 characters.** Distinct from the hero copy; written as a search-result preview. Active voice, second person.
- **Canonical URL set.** On every page. Points to the primary domain, not `www` plus non-`www` duplicates.
- **robots.txt exists and is correct.** Allows the primary crawlers, disallows staging subdomains that might otherwise get indexed during the launch spike.
- **sitemap.xml exists** and is referenced in robots.txt. Contains the landing page, the waitlist confirmation page, the privacy and terms pages, the blog index if any. Does not contain staging URLs.
- **Open Graph tags complete.** `og:title`, `og:description`, `og:image`, `og:url`, `og:type`, `og:site_name`. Each present on every shareable page. OG image details are Step 6.
- **Twitter card tags complete.** `twitter:card` set to `summary_large_image`, `twitter:site`, `twitter:creator`. Twitter Card Validator (now limited; see Step 6 cross-channel tests) should show the preview.
- **schema.org JSON-LD present.** At minimum: `Organization` (name, URL, logo, sameAs social URLs). For SaaS products: `SoftwareApplication` (name, applicationCategory, operatingSystem, offers). Validate with Google's Rich Results Test.
- **HTTPS only.** No mixed content. HSTS header ideally.
- **Core Web Vitals pass** on the landing page. LCP under 2.5s, CLS under 0.1, INP under 200ms. PageSpeed Insights is the check; failures block the launch if the PH / HN traffic spike is expected.
- **No `noindex, nofollow` left over from staging.** An AI-generated landing page deployed from a template often inherits `<meta name="robots" content="noindex,nofollow">` from the template's default. The launch ships with the page invisible to search. The skill greps for `noindex` in the shipped HTML before declaring done.

Launch-ready does not do keyword research, does not write an ongoing content strategy, and does not set up Google Search Console beyond the one-time verification on launch day. Those are ongoing-marketing territory.

**Passes when:** each of the 12 checklist items is green; Rich Results Test passes; PageSpeed Insights shows LCP / CLS / INP in the green zone; grep for `noindex` returns zero hits.

### Step 6. OG social share cards (the five-channel preview rule)

Read `references/social-share-cards.md`. An OG card that renders wrong on launch day is a launch asset that was never tested. The skill refuses to accept an OG card that has not been previewed on five channels.

The five required channels:

1. **X / Twitter.** 1200x630 or 1200x675; the Twitter Card tag drives the render. `twitter:card` set to `summary_large_image`. Preview via a fresh post in a test account or the Card Validator while it still functions; when it does not, post to a throwaway account.
2. **LinkedIn.** 1200x627. Cached by LinkedIn for at least 7 days; a card shipped with a bug cannot be fixed in place during the launch window. Preview via LinkedIn Post Inspector at www.linkedin.com/post-inspector.
3. **Slack.** Unfurls via the Slack bot. Preview via the `/linkunfurls` channel debug or by pasting into a test workspace. Slack truncates titles and descriptions differently; the short `og:title` matters.
4. **iMessage.** Renders on macOS and iOS. Preview by sending the URL to yourself.
5. **Discord.** Embeds via the Discord bot. Preview by pasting into a test server or the embed sandbox.

The five-channel rule is the load-bearing discipline. LinkedIn's cache is 7 days; a wrong OG card on LinkedIn at 9am ET on launch day is a wrong OG card for the entire launch window. The skill does not accept "we will fix it if people complain" on a LinkedIn card.

OG image requirements:

- **1200x630 native resolution.** Exactly. No 1080x... no square variants. The 1.91:1 ratio is what every major platform renders.
- **File size under 300KB** (ideally 50 to 150KB). Large OG images fail to render on slow unfurl timeouts.
- **Legible at 600x315 thumbnail.** Text must be readable when shrunk to half size. Minimum font size on the image: 32pt for body, 48pt for headline, at 1200x630.
- **No critical content in the outer 40px safe zone.** Crops vary per channel.
- **Brand color present.** The one color from Step 4.
- **Includes the product name legibly.** Not just a logo; the word.
- **Includes a one-line value proposition.** Not a full hero paragraph. Six to ten words.

OG generation path options (choose one, not all):

- **@vercel/og** (free, JS-driven, dynamic per page). Runs at the edge.
- **Tailgraph** (free tier, hosted templates).
- **Bannerbear** (SaaS, templated with JSON API).
- **Cloudinary OG image transformations** (requires Cloudinary account).
- **OG Image Studio** or similar self-serve designer for static one-off cards.

**Passes when:** the OG card exists at 1200x630 under 300KB with legible text at half size; the card has been previewed on all five channels (X, LinkedIn, Slack, iMessage, Discord) with screenshots in the launch notes; LinkedIn Post Inspector shows the card pre-launch (and re-inspected if changed).

### Step 7. Waitlist and email funnel

Read `references/waitlist-and-email.md`. A waitlist that captures emails with no nurture sequence is a paper waitlist. The skill refuses it.

Produce, in writing:

1. **Waitlist tool chosen.** Kit (ConvertKit), Loops, Resend Broadcasts, Plunk, Beehiiv, EmailOctopus, Buttondown, MailerLite, or the app's own DB plus an MTA. `stack-ready/DECISION.md` is the source if a choice is recorded.
2. **Double opt-in.** Required. The first email is a confirmation; only confirmed addresses enter the list. This is both a deliverability practice (prevents spam traps and typos from tanking domain reputation) and a legal practice (GDPR, CAN-SPAM, CASL). A waitlist form that fires "you are on the list" without a confirmation email fails the skill's contract.
3. **Confirmation email.** Subject line specific, not "Confirm your email." Body one paragraph, names the founder, sets expectation for the next touch. Single CTA button (confirm). No marketing content before confirmation (legally ambiguous and tonally wrong).
4. **Welcome email (post-confirmation).** Sends within 5 minutes of confirmation. Names the product, the founder, the rough date of launch, one concrete thing the subscriber will get at launch (early access, a discount, a private build, a named benefit). Not a newsletter signup. Not "thanks for your interest."
5. **Pre-launch sequence.** Two to four emails between confirmation and launch. Each one has a specific purpose: behind-the-scenes update, naming a design decision, asking a small question of the list (builds engagement and signal), teasing the launch date. Not a drip of "we are almost there" emails with no content.
6. **Launch-day drop.** The email that goes out at launch. Timed to be the first notification the list gets about the launch. Contains: the launch link, a single CTA, a one-paragraph note from the founder, and a PS that asks for a specific amplification (RT, upvote, share with one specific person). The launch day drop is not a surprise; the pre-launch sequence has set it up.
7. **Post-launch sequence (D+1 through D+7).** Three emails minimum: D+1 "thank you and what is next," D+3 "here is the first thing we learned," D+7 "here is what shipped." Not a sales sequence. The post-launch sequence converts launch-day curiosity into sustained attention.
8. **Unsubscribe and preference center working.** Every email has a working unsubscribe link. Not a mailto to the founder's inbox; a list-level unsub. CAN-SPAM and GDPR require it.
9. **Domain authentication.** SPF, DKIM, DMARC records on the sending domain. Deliverability to Gmail and Outlook depends on this; a launch-day email from an unauthenticated domain lands in spam for at least half the list.

**Capture on the landing page.** The form:

- **Two fields max** (email required, optional "what are you building"). More fields reduce conversion; the conversion data is well-documented (see `references/waitlist-and-email.md` section 6).
- **GDPR consent checkbox if targeting EU/UK users.** Unchecked by default; explicit opt-in. The checkbox text says what the subscriber will get.
- **Thank-you state.** Inline, not a full page redirect. Names the confirmation email and when it will arrive. Tells the subscriber to check their spam folder if it does not.

**Passes when:** tool is chosen and wired; double opt-in is live; confirmation, welcome, and at least one pre-launch email are drafted; the launch-day drop is scheduled; the post-launch sequence has subject lines and outline per email; SPF/DKIM/DMARC pass on the sending domain (check via mail-tester.com or Google Postmaster Tools).

### Step 8. Launch channel strategy

Read `references/launch-channels.md`. Launch-channel work is the most venue-specific part of the skill. The etiquette of each channel is different and the consequence of ignoring it is silent failure (flagged, downranked, or ignored).

Choose channels per product and audience. Not every product launches on every channel. The default stack for a dev-tool or indie SaaS is: Product Hunt, Show HN, one or two niche subreddits, X thread, LinkedIn post, Indie Hackers milestone, dev.to article if the product is infra-adjacent. Consumer products skip HN and substitute TikTok, Instagram, or Reddit consumer subreddits.

Per channel, write a post-plan with these fields:

- **Venue.** The URL of the exact place the post will land.
- **Timing.** Day and hour with timezone. For PH, 12:01 AM PT on a Tuesday / Wednesday / Thursday is the canonical slot. For HN, 7am ET to 10am ET on a weekday is the canonical slot; avoid Friday afternoons and weekends for Show HN.
- **Title / headline.** Per venue's etiquette. Show HN title: "Show HN: [Product] - [one-sentence what it does]". No "Launch HN" unless YC-backed (flagged otherwise). No all-caps. No "we built." PH tagline: one line under the product name, not a rehash of the hero. Reddit title: question-shaped or show-and-tell-shaped per the subreddit's norms.
- **Body / description.** The venue's native format. HN prefers a paragraph from the founder naming the frustration that led to the build and the key technical decision. PH prefers a maker comment that is grateful, specific, and invites questions. Reddit prefers a story framed around the specific sub's norms.
- **Hunter / submitter.** For PH, a hunter with an established account matters less in 2026 than in 2022 (the algorithm is less hunter-weighted) but still helps; confirm >48 hours in advance. For HN, the submitter should be the founder with a real account (>1 year, some comment karma); throwaways get flagged.
- **Amplification plan.** The list of people who will RT, comment, or upvote in the first hour. Not bots. Not a bought crowd. Actual people the founder has asked. The first-hour activity is what the algorithm reads as signal.
- **Response plan.** Who answers comments. Response time target (under 30 minutes for the first 4 hours on PH, under 60 minutes on HN, under 2 hours on Reddit). The founder should be present; delegation fails.

Venue-specific have-nots (each documented in `launch-channels.md`):

- **Show HN with "launch" or all-caps in the title.** Flagged.
- **Show HN with a video-only link.** HN readers expect a link to the product, not a YouTube video.
- **PH post that launches on Friday, Saturday, or Sunday.** Weekend traffic is a fraction of Tuesday through Thursday.
- **PH tagline that uses a banned word.** "Seamless AI-powered productivity for your team" fails the Step 3 audit.
- **Reddit post with a 9:0 self-promotion ratio** (no prior participation in the sub). Mods delete; users report. The 9:1 participation-to-promotion rule is enforced by almost every subreddit that allows self-promotion.
- **X launch thread without a clear hook in the first tweet.** Readers scroll; the thread never gets opened. The first tweet is the OG card for the thread.
- **LinkedIn launch post that reads like a press release.** Founder-voice, first-person, one anecdote, one link. Not "We are thrilled to announce."
- **Indie Hackers post without a revenue or user number.** The sub's norm is transparent metrics.
- **dev.to post that is a pitch.** The sub's norm is a technical write-up or tutorial that happens to mention the product.

**Passes when:** each chosen channel has a post-plan with all seven fields filled; titles pass the Step 3 banned-word audit; hunters / submitters are confirmed; amplification list has at least five named humans with asks sent >48 hours in advance; response plan names the founder as primary.

### Step 9. Press and outreach

Read `references/press-and-outreach.md`. In 2026, press is smaller and more niche than in the 2015-2020 era. TechCrunch has shrunk; specialty newsletters and micro-influencers carry disproportionate weight for indie products.

Produce, if press is part of the plan:

1. **Press kit.** A single page at `/press` or a public folder containing: product name, tagline, one-paragraph description, one-paragraph longer description, founder name and bio (50 and 150 words), founder headshot (1280x1280 and 600x600), product screenshots (1280x720, labeled), logo in SVG and PNG (light and dark backgrounds), launch date, links to the landing page, the PH / HN posts when live, and a founder contact email. No "request access" gate.
2. **Target list.** Not TechCrunch by default. Niche newsletters that actually cover the product's category. Examples (not an endorsement, check current relevance): TLDR and its specialty variants (TLDR DevOps, TLDR AI), Ben's Bites, The Neuron, The Pragmatic Engineer for infra and platform, Import AI for ML, Bytes / This Week in React for frontend, Contribunauts for open-source, Remote Rocketship for remote-first tools, Hacker Newsletter (aggregator), Changelog for engineering podcasts. Each entry on the target list has: name, editor/curator name, the category they cover, the submission URL or email, the expected turnaround.
3. **Pitch email.** One paragraph. Subject line names the product and the specific reason this venue should care. Body: two sentences on what the product is, two sentences on why this audience specifically, one link, one sentence of founder context, sign-off with real name and real contact. No attached press kit; link to it. No CC-spray; one venue per email.
4. **Influencer outreach.** Micro-influencers in the product's niche, not generic tech influencers. The ask is specific: "would you take a look at [demo link] and, if it resonates, share on launch day with your take." Not "please RT." Sent >7 days before launch.
5. **Podcast outreach.** For founders who want extended coverage, podcast pitches need a 4 to 12 week lead time. Not a launch-day lever; launch-ready notes the timeline and flags it.

Press is optional. Mode E launches (quiet, B2B direct) skip Step 9 entirely. Consumer and tool-space launches get at least a target list and one round of pitches.

**Passes when:** press kit is hosted and accessible; target list has at least five niche entries with contact info; pitch email draft exists with a specific subject line; influencer asks are out >7 days before launch.

### Step 10. Launch-day telemetry

Read `references/launch-telemetry.md`. launch-ready owns only launch-campaign telemetry. Product telemetry is `production-ready`'s territory; the line is bright.

What launch-ready owns:

1. **UTM taxonomy.** Every shared link on every channel carries UTM parameters. The taxonomy:
   - `utm_source`: the venue (producthunt, hackernews, reddit, twitter, linkedin, dev_to, indiehackers, newsletter_<name>, podcast_<name>, email_launch, email_welcome, press_<outlet>)
   - `utm_medium`: the channel type (social, referral, email, press, organic)
   - `utm_campaign`: the named campaign (launch_2026_04, relaunch_2026_q2)
   - `utm_content`: the specific post or variant (og_card_v1, thread_tweet_3, maker_comment)
   - `utm_term`: only if testing headline variants
2. **Analytics tool.** Plausible, Fathom, Umami, PostHog, or GA4. Chosen in `stack-ready/DECISION.md` if recorded. Must support: real-time view of referrers, UTM breakdown, conversion-event tracking (sign-up, waitlist-confirm, first-activation).
3. **Conversion waterfall.** Define the five events from landing to activation:
   - Landing page view
   - Primary CTA click
   - Sign-up / waitlist submit
   - Email confirmation (for double opt-in waitlists)
   - First meaningful action (first login, first waitlist engagement email open, first doc read)
   Each event is instrumented. The drop-off at each stage is the launch-day learning.
4. **Referrer dashboard.** Live during the launch. Shows: top 10 referrers in the last hour, UTM-source breakdown, conversion rate by source, waitlist signups by source, cumulative since launch start. Hosted somewhere the founder can refresh without being on a production dashboard.
5. **Traffic spike readiness.** The landing page survives 10x the typical traffic. For static landing pages on Vercel / Netlify / Cloudflare Pages, this is automatic. For server-rendered landing pages, CDN caching and a tested surge capacity matter. The app itself (behind the landing page) is `observe-ready`'s responsibility to survive; launch-ready's only job on the app side is to read `.observe-ready/SLOs.md` and note whether the SLO will survive a PH front-page day.
6. **Status page ready.** Linked from the landing page footer. Hosted out-of-band per observe-ready's Step 10 independence rule. If the app goes down during the launch, customers see a working status page and a clear message, not a blank screen.

What launch-ready does NOT own: in-app feature adoption tracking, cohort retention, pricing A/B tests, session replay of signed-in users, product-qualified-lead scoring. Those are `production-ready/references/analytics-and-telemetry.md`.

**Passes when:** every shared link has UTM parameters per the taxonomy; analytics tool is live and capturing; conversion-waterfall events are instrumented and firing in staging; referrer dashboard exists and is reachable; status page is linked and hosted out-of-band.

### Step 11. Launch-week runbook (D-7 to D+7)

Read `references/launch-week-runbook.md`. The runbook is a calendar, not a checklist. Each item has a day, an hour, an owner, and a pass criterion.

**D-7 (one week before launch):**
- All Step 1 through Step 9 artifacts in draft or better.
- PH hunter confirmed.
- Press target list finalized; pitches sent for 2-3 week lead-time outlets (podcasts, monthly newsletters).
- OG cards previewed on all five channels; LinkedIn Post Inspector clean.
- Waitlist pre-launch sequence scheduled.
- Soft-ask sent to amplification list (asking for RT / upvote on launch day).

**D-3:**
- Hero copy final. Feature grid final. Substitution test run end-to-end.
- Banned-word audit green.
- Dry run: post the landing page URL to a test Slack, iMessage, X preview; confirm OG renders.
- Pre-written launch-day responses drafted (a short library of reply templates for common PH / HN / Reddit comments: "what does it cost," "how is this different from X," "is this open source," "what stack").
- Launch-day drop email scheduled in the ESP. Confirmation that send time is correct.

**D-1:**
- Team channel set up (Slack / Discord) for launch-day coordination.
- Timezone-aware schedule posted: 12:01 AM PT PH live, 7:00 AM PT Show HN, 8:30 AM PT X thread, 9:00 AM PT LinkedIn, 10:00 AM PT reddit posts staggered.
- Final status-page dry run.
- Analytics / waterfall events tested end-to-end in staging; at least one test conversion logged.
- Founder sleep. A launch at 12:01 AM PT needs the founder to be awake for the first 4 hours; a launch at 7am ET on the east coast needs at least 4 hours the night before.

**D-0 (launch day):**
- 12:01 AM PT: PH post goes live. Maker comment posted within 2 minutes. First upvote wave (amplification list) active.
- 7:00 AM PT / 10:00 AM ET: Show HN posted. Founder monitors for first 90 minutes.
- 8:30 AM PT / 11:30 AM ET: X thread.
- 9:00 AM PT / 12:00 PM ET: LinkedIn post.
- 10:00 AM PT / 1:00 PM ET: Reddit posts staggered across target subreddits (never more than one per hour per account).
- 11:00 AM PT: launch-day email drop to waitlist.
- Every 30 minutes: refresh the referrer dashboard; note top source; reply to new comments.
- Every 2 hours: status-page check, app-SLO check (observe-ready), CDN / hosting dashboard check.
- End of day: write down what worked, what did not, what surprised. Not a blog post; a private note.

**D+1:**
- Thank-you email to the waitlist ("we were on HN's front page / PH #3 / etc., thank you").
- Analyze the conversion waterfall. Which source converted best? Which was highest volume? Which was highest quality (lowest drop-off at activation)?
- Reply to any press pitches that bit.
- If a PH badge was earned, embed it on the landing page.

**D+3:**
- "Here is what we learned" email to the list.
- First post-launch tweet with a specific number (signups, conversions, feedback themes).
- Onboarding friction audit: walk the signup flow fresh; where did users drop?

**D+7:**
- Launch retrospective: write the internal version (never published) and the external version (blog post, tweet thread, or IH milestone). Include specific numbers.
- Status transition (Step 12).

**Passes when:** the runbook is on a real calendar with owners and notifications; D-7, D-3, D-1, D-0, D+1, D+3, D+7 have named items each; the launch-day schedule has timezone-aware times; every item has a pass criterion.

### Step 12. Post-launch transition

Read `references/post-launch-transition.md`. The launch ends. Operations begins. The transition is an explicit handoff, not a fade.

Declare the transition when:

- The launch-week runbook has completed through D+7.
- Incoming traffic has dropped to within 3x of pre-launch baseline.
- The waitlist has been converted or segmented (the hot 10% get 1:1 outreach; the rest enter ongoing nurture).
- The launch retrospective has been written.

On transition:

- **Stop posting launch content.** Week-two social posts that re-hash the launch read as desperate. Shift to product updates, behind-the-scenes, or the ongoing content cadence.
- **Move launch-campaign analytics into a historical view.** The UTM campaign `launch_2026_04` becomes a closed campaign. New shared links get new UTMs (weekly_update, blog_post, etc.).
- **Hand off to `production-ready`'s in-app telemetry.** Launch-day signups are now users; their behavior is tracked in the product, not in the launch funnel.
- **Archive the launch notes.** The file `.launch-ready/launches/2026-04-launch.md` becomes read-only historical record. Future launches read it to avoid re-learning.
- **If metrics missed.** Name the miss. "We shipped and got 40 signups, not the 400 we hoped for." Identify which of the five launch-failure causes dominated (positioning, venue, amplification, capture, timing). Record in `.launch-ready/retrospectives/`. This is the input to a Mode C or Mode D re-launch later.

launch-ready's job ends here. Ongoing marketing (content cadence, SEO-as-practice, paid acquisition) is out of scope.

**Passes when:** the retrospective is written; the waitlist is segmented; launch campaigns are closed; ongoing telemetry has been handed off to production-ready; the launch notes are archived.

## Completion tiers

20 requirements across 4 tiers. Aim for the highest tier the session allows. Declare each tier explicitly at its boundary.

### Tier 1: Positioned (5)

The product has language that survives the substitution test.

| # | Requirement |
|---|---|
| 1 | **Positioning sentences written.** The four sentences from Step 1 (who is this for, what it replaces, what it does differently, the differentiator test). All four survive the substitution test against at least two named competitors. |
| 2 | **Tone of voice declared.** Three adjectives and three anti-adjectives. Every copy surface references this paragraph during review. |
| 3 | **Banned-word audit green on hero and sub-hero.** Zero hits from the Step 3 banned-word list above the fold, or each surviving hit has a one-line justification. |
| 4 | **Aesthetic test run.** One naive viewer has read the hero; their answer to "what does this product do" is specific, not generic. Recorded in launch notes. |
| 5 | **Founder-voice present.** The landing page names the founder, frames at least one sentence in first person, and includes a founder-story line or bio link. No company-we voice on the hero. |

### Tier 2: Landed (5)

The landing page is shippable; the OG cards render everywhere.

| # | Requirement |
|---|---|
| 6 | **Five-section landing page shipped.** Hero, social proof, feature grid (3-6 tiles), pricing (if applicable), CTA. In that order. Hero fits above the 1366x768 fold. |
| 7 | **Single above-the-fold CTA.** One primary action. Secondary CTAs live below the scroll. |
| 8 | **OG card at 1200x630, under 300KB, legible at half size.** Contains product name, brand color, and a six- to ten-word value prop. |
| 9 | **Five-channel OG preview clean.** Verified on X, LinkedIn (Post Inspector), Slack, iMessage, Discord. Screenshots recorded in launch notes. |
| 10 | **Launch-day SEO checklist green.** One H1, <title> under 60, meta description under 160, canonical URL, robots.txt, sitemap.xml, OG + Twitter tags, schema.org JSON-LD, no stray `noindex`, Rich Results Test passes, PageSpeed Insights in the green. |

### Tier 3: Captured (5)

The waitlist works and the launch can be measured.

| # | Requirement |
|---|---|
| 11 | **Waitlist with double opt-in live.** Tool chosen, confirmation email sends, welcome email fires post-confirmation. SPF / DKIM / DMARC pass on the sending domain. |
| 12 | **Pre-launch sequence scheduled.** At least two emails drafted between confirmation and launch day, each with a specific purpose (not drip filler). |
| 13 | **Launch-day drop scheduled.** The email that goes out at launch is in the ESP, timed to the launch hour, with subject line passing the Step 3 banned-word audit. |
| 14 | **UTM taxonomy applied.** Every shared link on every launch channel carries utm_source, utm_medium, utm_campaign, and utm_content per the Step 10 taxonomy. |
| 15 | **Conversion waterfall instrumented.** Five events from landing view to first meaningful action fire in analytics, tested end-to-end in staging. |

### Tier 4: Launched (5)

The launch actually happens, with a runbook and a follow-through plan.

| # | Requirement |
|---|---|
| 16 | **Per-channel post-plans written.** Each chosen channel has all seven fields from Step 8 (venue, timing, title, body, hunter, amplification, response). Titles pass the banned-word audit. |
| 17 | **Amplification list named and notified.** At least five human amplifiers asked >48 hours in advance, with specific asks (not "please RT"). |
| 18 | **D-7 to D+7 runbook on a calendar.** D-7, D-3, D-1, D-0, D+1, D+3, D+7 each populated, with owners and notifications set. |
| 19 | **Status page linked and out-of-band.** Hosted on infrastructure distinct from the app; linked from landing page footer; observe-ready's independence test acknowledged. |
| 20 | **Post-launch transition declared.** By D+7 or +14, retrospective written, waitlist segmented, launch campaign closed, launch notes archived. |

**Proof test:** an outsider loads the landing page cold, reads the hero, answers "what does this do and who is it for" specifically in under 15 seconds; clicks the CTA and lands on a working waitlist or signup; receives a confirmation email within 5 minutes; clicks a shared launch link from any of the five OG-preview channels and sees the correct preview; opens the referrer dashboard and sees their own visit attributed to the correct UTM source. If any of those five checks fails cold, the launch is not Tier 4.

## The "have-nots": things that disqualify the launch at any tier

If any of these appear, the launch fails this skill's contract and must be fixed:

- **A hero sentence that uses any of the banned words** (seamless, powerful, revolutionary, effortless, intelligent, cutting-edge, game-changing, unlock, supercharge, streamline, empower, elevate, robust, best-in-class, leading, enterprise-grade, world-class) above the fold without a written justification. The AI-slop landing signature.
- **A hero sentence that survives the substitution test with a named competitor name swapped in.** Hero-fatigue copy.
- **A feature grid with more than six tiles.** Spec-sheet positioning.
- **A feature grid where each tile is a category label** (Fast / Secure / Scalable) rather than a product-specific capability.
- **An above-the-fold area with more than one primary CTA.**
- **An OG image not at 1200x630.**
- **An OG image over 300KB or with text illegible at 600x315.**
- **An OG image that has not been previewed on X, LinkedIn, Slack, iMessage, and Discord.** Unrendered OG.
- **An `<meta name="robots" content="noindex">` left in the shipped HTML.** Silent de-indexing.
- **A `<title>` over 60 characters or a meta description over 160.**
- **Multiple `<h1>` tags on the landing page.**
- **A waitlist form with no double-opt-in.** Paper waitlist.
- **A waitlist with no post-confirmation welcome email.**
- **A waitlist with no pre-launch sequence drafted.** Paper waitlist, second form.
- **A launch-day email drop scheduled without SPF/DKIM/DMARC passing on the sending domain.** Deliverability collapse.
- **A shared launch link without UTM parameters.** Silent launch; cannot attribute signups to source.
- **Analytics with no conversion-waterfall events** (landing view, CTA click, sign-up, confirm, activate). Attribution blind.
- **A Show HN post with "launch" or "Launch HN" or all-caps in the title.** Flagged on arrival.
- **A Product Hunt post scheduled for Friday, Saturday, or Sunday.**
- **A Product Hunt post scheduled without a confirmed hunter >48 hours in advance.**
- **A Reddit post to a sub where the founder has zero prior comment history** (the 9:1 participation-to-promotion rule).
- **A LinkedIn launch post written in press-release voice** ("We are thrilled to announce..."). Founder-voice rule.
- **A press pitch sent as a CC-spray to five publications.**
- **A landing page with Core Web Vitals in the red under PageSpeed Insights.** A launch with a slow page burns first-visit conversion.
- **A status page hosted on the same infrastructure as the app.** The Facebook 2021 / Slack 2021 rule applies.
- **A launch with no D+1 through D+7 follow-up planned.** Silent fade.
- **A launch without a retrospective at D+7 or D+14.** No learning loop.
- **A landing page that promises features the app does not ship.** Reads `.production-ready/STATE.md`; any feature listed on the landing page that is not in STATE.md is vapor and fails the skill's contract.
- **Stock illustrations of abstract people pointing at charts above the fold.** Shadcn-default aesthetic; fails the visual identity test.
- **Emojis used as UI markers on the landing page.** Global rule; launch-ready enforces.

When you catch yourself about to ship any of these, fix it before proceeding. A broken launch is worse than no launch; the first shot at attention is finite, and the founder does not get to re-run the window.

## Reference files: load on demand

The body above is enough to start. Load each reference *before* the step that uses it, not after.

| Reference file | When to load | ~Tokens |
|---|---|---|
| `launch-research.md` | **Always.** Start of every session (Step 0). | ~7K |
| `positioning-and-copy.md` | **Tier 1.** Step 1 and Step 3; substitution test, differentiator test, banned-word audit, tone of voice. | ~10K |
| `landing-page-anatomy.md` | **Tier 2.** Step 2 and Step 4; five-section anatomy, visual identity tokens, anti-patterns. | ~9K |
| `seo-fundamentals.md` | **Tier 2.** Step 5; meta, OG, Twitter, schema.org, sitemap, Core Web Vitals. | ~7K |
| `social-share-cards.md` | **Tier 2.** Step 6; five-channel preview rule, OG image specs, generation tool landscape, cache TTLs. | ~7K |
| `waitlist-and-email.md` | **Tier 3.** Step 7; tool landscape, double opt-in, pre-launch sequence, launch drop, post-launch sequence, deliverability. | ~9K |
| `launch-channels.md` | **Tier 4.** Step 8; Product Hunt, Show HN, Reddit, X, LinkedIn, IH, dev.to; etiquette, titles, timing, amplification. | ~12K |
| `press-and-outreach.md` | **Tier 4 (optional).** Step 9; press kit, target list, pitch email, influencer and podcast outreach. | ~7K |
| `launch-telemetry.md` | **Tier 3.** Step 10; UTM taxonomy, analytics, conversion waterfall, traffic spike readiness. | ~7K |
| `launch-week-runbook.md` | **Tier 4.** Step 11; D-7 to D+7 calendar, launch-day schedule, response plans. | ~8K |
| `post-launch-transition.md` | **Tier 4.** Step 12; transition criteria, handoff to production-ready, retrospective template. | ~5K |
| `RESEARCH-2026-04.md` | **On demand.** Source citations behind every guardrail, incident, and banned-word choice. | ~35K |
| `launch-antipatterns.md` | **Every launch artifact draft + Mode C audits.** Named-failure-mode catalog with grep tests, severity, and per-skill guards. Loaded at every landing-page draft review. | ~5K |

Skill version and change history live in `CHANGELOG.md`. When resuming a project, confirm the skill version your session loaded matches the version recorded in `.launch-ready/STATE.md`. A skill update between sessions may change the banned-word list (new AI-slop tells emerge), channel etiquette (Product Hunt algorithm changes, HN flag dynamics), or tool landscape (waitlist-tool entries and exits).

## Suite membership

launch-ready is the shipping-tier skill that owns "tell the world the product exists." See `SUITE.md` at the repo root for the full map. Relevant siblings at a glance:

- **Planning tier:** `prd-ready` (what), `architecture-ready` (how), `roadmap-ready` (when), `stack-ready` (with what tools).
- **Building tier:** `production-ready` (the app), `repo-ready` (the repo scaffolding).
- **Shipping tier:** `deploy-ready` (ship it), `observe-ready` (keep it healthy), `launch-ready` (this skill, tell the world), `harden-ready` (survive adversarial attention).

Skills are loosely coupled: each stands alone, each composes with the others via well-defined artifacts. No skill routes through another; the harness is the router. Install what you need.

## Consumes from upstream

When the agent starts, it checks for upstream artifacts and pre-fills from them rather than asking the user to repeat decisions already made. Absence is fine; the skill falls back to its own defaults.

| If present | launch-ready reads it during | To pre-fill |
|---|---|---|
| `.production-ready/STATE.md` | Step 1 (positioning) and Step 2 (feature grid) | The actual shipped feature set; any feature on the landing page not in STATE.md is flagged as vapor. User journey list pre-fills the positioning's "what it does differently" candidates. |
| `.production-ready/visual-identity.md` (or equivalent brand tokens) | Step 4 (visual identity) | Brand color, typography, icon library. Do not redecide; quote. If absent, launch-ready produces a minimum viable identity. |
| `.production-ready/adr/*.md` | Step 2 (feature grid) | Architectural decisions that are genuinely differentiating (stack choices, security model, self-hosting posture) can feed the differentiator sentence. |
| `.deploy-ready/TOPOLOGY.md` | Step 10 (telemetry) and Step 11 (runbook) | Public URLs for the landing page and the app; the status page target; the regions and CDN configuration relevant to a traffic spike. |
| `.deploy-ready/STATE.md` | Step 11 (runbook) | Current production version (so the launch does not ship on top of an in-progress expand/contract migration); last-known-green status. A non-green deploy state blocks the launch-day drop. |
| `.observe-ready/SLOs.md` | Step 10 (telemetry) and Step 11 (runbook) | The app's SLOs so launch-day traffic spikes do not silently burn the budget. If observe-ready shows a fragile SLO, the launch runbook includes an SLO-watch row. |
| `.observe-ready/INDEPENDENCE.md` | Step 10 (status page) | Whether the status page is already hosted out-of-band. If the row is green, launch-ready quotes it. If the row is dependent, the launch runbook flags the risk before D-1. |
| `.stack-ready/DECISION.md` | Step 0 and Step 7 | Chosen waitlist tool, analytics tool, landing-page framework. If absent, launch-ready proposes defaults; do not re-decide. |
| `repo-ready` outputs | Step 2 (if landing page is a separate repo) | Standard repo hygiene is present; launch-ready does not re-author README or CI. |

If an upstream artifact *contradicts* the running app, trust the running app and note the drift. Upstream artifacts are historical records, not current-state overrides.

## Produces for downstream

launch-ready sits at the end of the arc; its output is consumed by real users finding the product, not by another suite skill. But launch-ready emits artifacts so the next launch session (a relaunch, a new-feature launch, a pivot) can resume without rediscovery:

| Artifact | Path | Purpose |
|---|---|---|
| **Launch state** | `.launch-ready/STATE.md` | Current launch cycle, tier reached, open questions, skill version. Next launch session reads first. |
| **Positioning doc** | `.launch-ready/POSITIONING.md` | The four positioning sentences, tone of voice, banned-word overrides. Stable across launches; updated on pivot. |
| **Launch log per campaign** | `.launch-ready/launches/YYYY-MM-slug.md` | Per-launch record: dates, channels, posts, OG cards, UTM campaign name, D+1 through D+7 numbers, retrospective. |
| **Campaign retrospectives** | `.launch-ready/retrospectives/YYYY-MM-slug.md` | Post-launch learning: dominant failure (if any), what to do differently next time. Read by the Mode C and Mode D detection. |
| **UTM registry** | `.launch-ready/utm-registry.md` | The campaign / source / medium / content values used to date, so new campaigns do not collide with old ones and analytics history stays clean. |
| **Asset inventory** | `.launch-ready/assets/` | OG cards, press-kit images, logo variants, screenshots. Checked into the launch-ready working directory, not the app repo (unless they already live there via production-ready). |

If another suite skill is added later that consumes launch-ready outputs (e.g., a future `growth-ready` skill), these artifacts are the contract. They cost nothing to emit.

## Handoff: ongoing marketing is not this skill's job

If the work is about weekly content cadence, SEO-as-practice, paid acquisition campaigns, sustained email nurturing past D+14, influencer partnerships beyond launch week, affiliate programs, partnership BD, or sales motion, delegate to a separate marketing workflow or future skill. launch-ready's scope is the launch. Ongoing marketing is a different discipline and is out of scope for this skill.

The tight coupling between launch-ready and its siblings:

- **observe-ready.** A launch generates a traffic spike. The spike either validates the SLOs or exposes their weakness. launch-ready reads `.observe-ready/SLOs.md` and surfaces any at-risk SLO in the launch runbook. If observe-ready is not installed, launch-ready notes the absence and recommends a minimum health check before launch day.
- **deploy-ready.** A launch should not ship on top of an in-progress expand/contract migration. launch-ready reads `.deploy-ready/STATE.md`. If an expand phase is in flight, the launch either waits for cutover or ships with a caveat recorded in the runbook.
- **production-ready.** A launch landing page must not promise features the app does not ship. launch-ready reads `.production-ready/STATE.md`. Any feature on the landing page missing from STATE.md is vapor and blocks the launch.

**If your harness exposes a skill-invocation tool** (e.g., Claude Code's Skill tool), invoke `observe-ready` or `deploy-ready` directly when the handoff trigger fires. **Otherwise**, surface the handoff to the user: "This step needs `observe-ready` to confirm SLOs can survive the launch spike. Install it or handle the observability layer separately." Do not attempt to generate SLO configs or deploy pipelines inline from this skill.

## Session state and handoff

Launches span sessions: positioning takes days to stabilize, the pre-launch sequence runs across weeks, the D-7 to D+7 runbook spans two weeks, and the retrospective happens after. Without a state file, every resume rediscovers the launch from scratch, and half-drafted positioning documents accumulate.

Maintain `.launch-ready/STATE.md` at every tier boundary. Read it first on resume. If it conflicts with the running system, trust the running system and update the file.

**Template:**

```markdown
# Launch-Ready State

## Skill version
Built under launch-ready [current skill version], [frontmatter updated date]. If the agent loads a newer version on resume, re-read the changed sections before continuing.

## Tier reached
Tier 2 (Landed). Target next: Tier 3 (Captured).

## Mode
Mode A (pre-launch, greenfield). Target launch date: 2026-05-14.

## Positioning (Step 1)
- Who it is for: three-person engineering teams whose on-call rotation is held together by a shared spreadsheet.
- What it replaces: a weekly standup + a pinned Slack message + a spreadsheet.
- What it does differently: threads every alert through a single on-call handoff doc that auto-updates when the rotation changes.
- Differentiator test: competitor rebuttal is "we do not build auto-updating handoff docs; ours are manual."
- Tone: direct, technical, quietly funny; not corporate, breathless, aspirational.
- Last reviewed: 2026-04-23.

## Landing page (Step 2-4)
- URL: staging at <staging-url>, live target at <prod-url>.
- Sections: hero, social proof (6 early users quoted with consent), feature grid (4 tiles), pricing (2 tiers), CTA (join waitlist).
- Banned-word audit: last run 2026-04-23; zero hits above the fold.
- Visual identity: brand color #2F5D73, body font Inter, headline font Inter, icon library Lucide.
- Aesthetic test: 2 naive viewers; both described the product specifically within 15 seconds.

## OG cards (Step 6)
- 1200x630, 178KB, produced via @vercel/og.
- Channel previews clean on: X, LinkedIn (Post Inspector 2026-04-22), Slack, iMessage, Discord.
- Screenshots in .launch-ready/assets/og-previews/.

## SEO (Step 5)
- Checklist items 1-12 green as of 2026-04-22.
- Rich Results Test: Organization + SoftwareApplication pass.
- PageSpeed Insights: LCP 1.4s, CLS 0.02, INP 90ms (green).

## Waitlist (Step 7)
- Tool: Loops.
- Double opt-in: live.
- Pre-launch sequence: confirmation, welcome, two pre-launch teaser emails scheduled.
- Launch-day drop: scheduled for 2026-05-14 11:00 PT.
- Sending domain: mail.example.com; SPF/DKIM/DMARC pass.

## Channels (Step 8)
- Product Hunt: scheduled 2026-05-14 00:01 PT. Hunter @username confirmed 2026-04-22.
- Show HN: planned 07:00 PT; title draft "Show HN: [Product] - [one-line]".
- X thread: 08:30 PT; first tweet draft in .launch-ready/assets/x-thread.md.
- LinkedIn: 09:00 PT; draft in .launch-ready/assets/linkedin-post.md.
- Reddit: /r/SideProject at 10:00 PT; /r/<niche> at 11:00 PT. Founder has 18 months of comment history on both subs.

## Telemetry (Step 10)
- Analytics: Plausible.
- UTM campaign name: launch_2026_05.
- Conversion waterfall: five events instrumented; tested end-to-end 2026-04-22.
- Status page: Instatus, hosted independently, linked in footer.

## Open questions blocking Tier 3 or Tier 4
- [open, Tier 3] Second pre-launch email needs content; first draft not yet written.
- [open, Tier 4] Amplification list at 3 humans; needs 5 by D-2.

## Last session note
[2026-04-23] Completed Tier 2. Next: finish waitlist pre-launch sequence; populate amplification list to 5.
```

**Rules:**
- STATE.md is the contract with the next session. If it is out of date, the next session re-discovers the launch.
- At every `/compact`, `/clear`, or context reset, update STATE.md first.
- Never delete STATE.md. If an entry is wrong, correct it in place with a dated note.
- The positioning block is load-bearing. A launch that resumes without positioning re-opens the substitution test from scratch and loses the previous review's learning.

## Keep going until it is actually launched

Shipping the landing page is roughly 30% of the work. The remaining 70% is the positioning audit, the banned-word pass, the OG five-channel preview, the waitlist with the sequence, the UTM taxonomy, the channel-specific post-plans, the amplification list, the D-7 to D+7 calendar, and the retrospective. Budget for all of it.

A "launched" product is one a stranger can load the landing page cold and describe specifically, click the CTA and reach a working waitlist or signup, and whose founder can open the referrer dashboard and see where their first hundred visitors came from attributed correctly. When in doubt, open the landing page in a fresh browser from a phone you have not used for this project, and read it out loud as if you were your target audience's most skeptical friend. The first sentence that makes you wince is the next thing to rewrite.
