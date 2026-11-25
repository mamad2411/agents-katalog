---
name: tia-frontend-design-site
description: House UI and UX rules for the Tertiary Infotech Academy CMS — dark sci-fi/robotics look, dense layouts with no dead space or gaps, no chips or pills, no template-looking layouts, plus the rules for the navbar, footer, robot/WhatsApp chat launcher, forms, mobile and accessibility. Load before building, changing or reviewing ANY UI in this repo, including small spacing, layout, copy-placement, footer, nav or chatbot changes.
---

# Tertiary Infotech Academy — UI and UX Rules

One design direction, kept consistent across every page. Do not invent new palettes, fonts or moods. The hard rules below come from repeated owner corrections, so do not undo them to make something "breathe".

This is our own skill, not a stock template. It is the `ai-cms` edition of the group-wide `tia-frontend-design` skill: `tia-frontend-design` sets the standard for all our sites, and this file adds this site's theme, components and file paths. Everything needed for this repo is written out here, so it also works where `tia-frontend-design` isn't installed.

When an older component breaks a rule here, this file wins. Do not copy the old pattern; see [Known violations](#known-violations).

## The five hard rules

1. **No dead space.** Every part of the viewport should be doing something. Empty bands and empty columns are bugs.
2. **No gaps.** Spacing stays tight between sections, between a heading and its content, and between cards.
3. **No chips.** No pills, tags or badges used as labels. See [the replacements](#no-chips).
4. **No standard layout look.** Nothing should read as a template. See [Layout](#layout).
5. **One footer, one navbar, one chat launcher.** Extend the shared components; never fork them per page.

## Spacing

The owner has asked for tighter spacing again and again ("reduce the gap", "remove all the gaps", "make it neat and compact"). Use this scale:

| Where | Use | Never |
|---|---|---|
| Homepage section | `py-4` to `py-6` | anything above `py-10` |
| Inner-page section | `py-6` to `py-10` | `py-16` and up |
| Inner-page hero | `py-10 md:py-14` at most | `pt-24`, `pt-32` |
| Blog post banner | `BlogBanner` strip, ≈3.5:1 (240px tall at 1440px, 152px at 375px) | the full 16:10 card cover |
| Section header to its grid | `mb-6` to `mb-8` | `mb-12` and up |
| Kicker to heading | `mb-3` to `mb-4` | `mb-6` and up |
| Heading to paragraph | `mt-3` to `mt-4` | `mt-8` and up |
| Paragraph to CTA row | `mt-6` | `mt-10` and up |
| Card grid | `gap-4`, or `gap-px` for joined panels | `gap-8` and up |
| Split (text + panel) columns | `gap-8` to `gap-10` | `gap-14` and up |
| Card padding | `p-5` to `p-7` | `p-10` and up |
| Above the footer | the footer's own `mt-10` only | extra `mb-*` on the last section |

**The first block on a page must not add top padding.** The navbar is `sticky`, so it already takes up its own height. [globals.css](src/app/globals.css) sets one offset for `body > main > *:first-child` using `!important`. Never add `pt-16` to `<main>` or use a large top padding to "clear the navbar".

**What counts as dead space:**

- An empty horizontal band over about 80px tall between pieces of content at 1440px wide.
- A column of text capped by `max-w-*` with nothing beside it, leaving the rest of the row blank.
- An **orphan row**: a card grid whose last row has empty cells. Choose a column count that divides the items evenly, or add `fill-2`, `fill-md-2`, `fill-lg-2` or `fill-2-3` from globals.css so the last card spans the remainder.
- A `flex-1` spacer or `min-h-screen` that pushes content apart on tall screens.
- Unequal columns in a split, where one side ends far above the other. Add content or use `items-center`.

Fill a gap with real content: a KPI strip, a status list, a screenshot or a proof point. Never fill it with filler copy or a decorative blob alone.

## Layout

**Width.** Use `Container` from [Container.tsx](src/components/layout/Container.tsx). Its default `wide` (1600px) is the standard, and `full` is for full-bleed heroes. Do not add narrower wrappers such as `max-w-5xl mx-auto` around whole sections. Long-form reading text (blog body, legal pages) is the one place a narrow measure is correct.

**Banned template looks:**

- Centred kicker, headline and subtitle above three equal cards.
- Hero with text on the left and a stock illustration on the right.
- Every section having the same structure, or a page that stacks one identical card grid after another.
- Generic feature rows of icon, title and one line, used as the main content of a page.

**Approved patterns, already on the site:**

| Pattern | Example | How |
|---|---|---|
| Asymmetric split, mirrored in the next section | [AILmsTmsShowcase.tsx](src/components/sections/AILmsTmsShowcase.tsx), [ELearningShowcase.tsx](src/components/sections/ELearningShowcase.tsx) | `lg:grid-cols-[1.05fr_0.95fr]`, then flipped |
| Right-aligned section header | [Services.tsx](src/components/sections/Services.tsx) | `max-w-5xl ml-auto text-right` |
| Joined panel with hairline dividers | [WhyChooseUs.tsx](src/components/sections/WhyChooseUs.tsx), hero KPI strip | `gap-px bg-white/5` with `overflow-hidden` |
| Console-style status list | "Ready on day one" panel | Rows of label, description and a mono `✓ READY` |
| Header with an action on the far right | [FeaturedEdTools.tsx](src/components/sections/FeaturedEdTools.tsx) | `flex items-end justify-between` |

Two neighbouring sections must not use the same pattern with the same alignment.

**Hero.** [HeroCircuit.tsx](src/components/sections/HeroCircuit.tsx) is this site's bespoke visual: our services wired into one agentic core, with each node linking to its page. Keep proof (the KPI strip) in the first viewport. Do not use a 2×2 grid of boxes. `ai-pei`'s fibre-optic globe sets the level of ambition, but it belongs to that site; this one needs its own idea.

## No chips

"Chip" means any small rounded label: `rounded` or `rounded-full` with small padding, a tinted background or a border, wrapping a short word. That includes status, category, tag, platform and "new" labels, and pills around kickers.

| Instead of | Use |
|---|---|
| Kicker in a pill | Plain `.kicker` text: `[ FLAGSHIP PRODUCT ]` |
| Row of tags or tech labels | Mono text with separators: `WSQ · TPQA · SSG API` |
| Status pill | Mono coloured text: `✓ READY` |
| Blog category and tag filters | Plain text links; mark the active one with colour and an underline |
| Store or platform labels | Real store badges from [StoreBadges.tsx](src/components/sections/StoreBadges.tsx), or plain text |
| Step labels on process cards | Mono text above the step title: `STEP 02 · 2 WEEKS` |

**Not chips, and allowed:** round icon buttons (social links, close), avatars, the orbiting WhatsApp badge, and the `.prose-dark` list markers the [blog-post skill](.claude/skills/blog-post/SKILL.md) relies on. The kicker pill inside blog cover images is also separate; the [blog-cover-image skill](.claude/skills/blog-cover-image/SKILL.md) owns it.

## Visual language

Tokens live in [globals.css](src/app/globals.css). Use them as `(--color-cyan)`, and do not add off-palette colours.

```
--color-bg            #060A14   page background
--color-bg-elevated   #0C0D1A   cards, footer
--color-bg-deeper     #03060E   image wells
--color-border        rgba(255,255,255,0.08)
--color-muted         #AAA8B1   secondary text
--color-cyan          #59EBFD   main accent
--color-amber         #F6AE64   warm accent
--color-green         #01C982   ready and success
--color-purple        #5C00E5   fills and gradients only
--color-purple-light  #8757F2   purple TEXT and icons
```

**Type.** Fonts are already loaded in [layout.tsx](src/app/layout.tsx); never import more.

- Exo 2 (`font-display`) for headings, Inter for body and UI, JetBrains Mono for kickers, data and code.
- `h1`: `clamp(2.25rem, 4.5vw, 4.5rem)`, `font-extrabold`, `leading-[1.02]`.
- `h2`: `clamp(2rem, 4.5vw, 3.25rem)`, `font-extrabold`, `leading-[1.05]`.
- One `.gradient-text` keyword per headline at most.

**Reuse these classes before writing new CSS:** `glass`, `card-hover`, `btn-primary`, `btn-secondary`, `kicker`, `gradient-text`, `gradient-text-warm`, `grid-bg`, `glow-blob`, `reveal`.

**Texture.** Use `grid-bg`, `glow-blob` or a gradient hairline where a section would otherwise look flat. It decorates content and never replaces it. Blobs sit inside a section with `overflow-hidden`.

**Icons.** Use `react-icons` (`hi2` outline, `fa6` for brands), coloured from the palette. No emoji in public UI.

**Light mode.** There is none. Everything is dark, including admin.

**Motion.**

- Animate `transform` and `opacity` only, with hover transitions of 200–300ms.
- Use `reveal` for entrance stagger, not scroll-jacking, parallax or bouncy springs.
- Every looping animation needs a `prefers-reduced-motion` fallback in globals.css.

## Navbar

[Navbar.tsx](src/components/layout/Navbar.tsx) is the only header.

- Height is `h-16`, sticky, and always on one line (`whitespace-nowrap`).
- The full menu shows at `xl` and up. Below 1280px, show the hamburger plus the phone and WhatsApp icons.
- Links containing `#` must be plain `<a>`, because `next/link` doubles the hash on repeat clicks. Target sections need `scroll-mt-20`.
- Renaming a menu item means changing the DB row, `FALLBACK` and [reset-header-menu.ts](scripts/reset-header-menu.ts).

## Footer

[Footer.tsx](src/components/layout/Footer.tsx) is the only footer, and it is compact (`py-8`).

- **Five columns:** brand with blurb and socials, `[ COMPANY ]`, `[ SSG SERVICES ]` with `[ SSG TOOLS ]` below it, `[ NAVIGATE ]`, `[ CONTACT ]`. Do not add a column unless asked.
- **New links** go in the `COMPANY_LINKS`, `SSG_TOOLS_LINKS` or `NAVIGATE_LINKS` arrays, or in `SERVICES` for SSG services, with external links opening in a new tab. Navigate labels must not wrap at `xl`.
- **Contact details** always come from `getCompanyContact()` and socials from `getSocialLinks()`. Never hardcode them.
- **Contact rows** each have a cyan icon: address, email, phone, WhatsApp.
- **The bottom strip stays:** copyright with UEN, plus the "Powered by Tertiary Infotech Academy Pte Ltd" credit link.
- **No gaps:** no tall spacers, no sparse columns stretched across the page, no newsletter or CTA block unless asked.

## Chat launcher

Public and admin chat are separate, so do not merge them or add a second floating button.

**Public: [WhatsAppWidget.tsx](src/components/ui/WhatsAppWidget.tsx)**, mounted once in the root layout and hidden on `/admin`.

- **Mascot:** the robot is this site's own. `ai-pei` has a female course assistant and `ai-kids` has Pip, so do not swap or reuse them across sites.
- **Launcher:** the animated [RobotAvatar.tsx](src/components/ui/RobotAvatar.tsx) in a purple-to-cyan ring, `w-16 h-16`, fixed `bottom-6 right-6`, `z-50`. It floats, blinks, has a glowing antenna, and tilts its head when a tip shows.
- **WhatsApp badge:** a small WhatsApp icon orbiting the ring and staying upright. Never go back to a plain status dot. With reduced motion it rests at the top-right.
- **Service tips:** first at 6s, then every 18s, each visible for 8s, at most 4 per visit. They stop while the panel is open, and dismissing one mutes tips for the browser session.
- **Tip bubble:** fully opaque, so page content never shows through. Tapping it opens WhatsApp with a pre-filled message.
- **Panel:** one-tap topics that deep-link to WhatsApp with a pre-filled message, plus a "Start a chat" button.
- **Green:** `#0B6E4F` for panel buttons and hovers, `#25D366` for the orbit badge only. These are the only permitted off-palette colours.
- **Content:** tips and topics name real services only, in the voice of Tertiary Infotech Academy.

**Admin: [ChatBot.tsx](src/components/ui/ChatBot.tsx) (Nemo)** renders only on `/admin` and its panel is hidden below `md`. Do not mount it on public pages. Any AI logic must follow the Claude Agent SDK policy in [CLAUDE.md](CLAUDE.md).

## UX requirements

**Conversion**

- Every public page ends in a clear next step and has at least one CTA in the first viewport.
- Use one `btn-primary` per view, with `btn-secondary` for the rest.
- CTA labels say what happens: "Request a demo", not "Submit" or "Click here".
- Every form posts to `/api/contact` with a page-specific `source`. Follow the [lead-magnets skill](.claude/skills/lead-magnets/SKILL.md) for fields and page anatomy.
- Do not remove the WhatsApp, phone or contact routes from any page.

**Content and hierarchy**

- Lead with the visitor's outcome, and keep paragraphs short and scannable.
- Keep bold service keywords when restyling copy; they are deliberate for SEO. Render them through `RichText`.
- Use the short name "Tertiary Infotech Academy" and British/Singapore spelling.
- Check where copy lives before editing it. Homepage text, menus and brand are DB-driven, often with a code fallback (see [CLAUDE.md](CLAUDE.md)).
- Do not add placeholder claims, statistics or client names.

**Navigation and links**

- Internal links open in the same tab. External links use `target="_blank" rel="noopener noreferrer"`.
- Whole-card links need a full-card hit area and a visible hover state.
- Keep legacy anchors working when renaming sections. `Services.tsx` keeps `#services` for this reason.

**States and forms**

- Every data view has loading, empty and error states. A section with no data renders nothing, never an empty shell.
- Buttons show progress and disable during submit. Errors appear beside the form and keep what the user typed. Success states say what happens next.
- Inputs are dark with a cyan focus ring and a real label, with no placeholder-only fields.
- Use the correct input types (`email`, `tel`) so phones show the right keyboard.

**Mobile**

- Test at 375px. No horizontal scrolling, and no text clipped or overlapping.
- Keep spacing tight on mobile too; columns stack but padding does not grow.
- Touch targets are at least 44px for new controls.
- Confirm the chat launcher and tip bubble do not cover a form's submit button or a primary CTA.

**Accessibility**

- One `h1` per page, with headings in order.
- Text is at least 12px, except `.kicker`. Secondary text uses `--color-muted` or `text-white/60` and above.
- Use `--color-purple-light`, never `--color-purple`, for text and icons; the darker purple is unreadable on the dark background.
- Icon-only controls need `aria-label`. Images need descriptive `alt` text.
- Everything works by keyboard, with a visible `focus-visible` state.
- Do not signal status by colour alone; add text or an icon.

## Admin UI

Admin shares the tokens and buttons, but is optimised for working through data.

- **One entry, one row.** Tables are compact, with truncated long values and at most two lines per row.
- **Full width.** Do not cap admin tables to a narrow page width.
- **Bulk actions** (checkboxes, selection controls) sit above the table, not inside it.
- **Show plenty per page** rather than paginating short lists.
- **Check contrast** on every control against the dark background.

## Lead-generating service pages

Every service page should earn an enquiry, not just describe the service. New SSG services go in `SERVICES` ([site-content.ts](src/lib/site-content.ts)), with page content in [ssg-service-pages.ts](src/lib/ssg-service-pages.ts), a route and a sitemap entry. `SERVICES` feeds the homepage, footer and related links.

**Page order:** outcome headline and form in the first viewport → what goes wrong → what we do → why us → process → what's included → FAQ → form again with links to related services.

- **Name the offer.** Replace "Book a consultation" with a specific free check, such as "Free TPQA Grade 1 readiness review", and list the questions it answers beside the form. Deliver it inside the free 30-minute consultation.
- **Lead with the buyer's fear or goal.** Use real pains from regulator rules and real cases: a deadline, a rejection reason, a funding tier. Generic benefits do not convert.
- **Say what we provide that they can't.** Examples: the Assessor Coach and financial-sector SME for IBF, the mock-up website for SWDA ATO, boards for a PEI, job placement consultancy for SCTP, approval advice for TAEPP and societies.
- **Show real proof** beside the pitch, from our own record, such as a grade or live app counts. Calculate counts from data rather than typing them in.
- **Qualify in the form.** Keep the standard fields and use the message placeholder to ask the one question that matters, such as the due date. Do not add budget or company-size fields.
- **Tag each form** with a page-specific `source`, and add that source's label to the lead-email settings.
- **Keep a form on the homepage too**, beside the full services list, so visitors don't have to pick a page first.
- **Link sideways.** Each service page lists related services. Add every service to the footer and to the chat widget's topics and pop-ups.

**Compliance beats persuasion.** Regulated copy must stay true:

- Check claims against the regulator's current wording, and link the conditions: "up to 90%" for funding, not "90%".
- Never promise an approval, a pass or a grade. Say who decides.
- Never claim to attend something consultants are barred from, such as the TPQA on-site assessment.
- Do not name clients or reveal their applications.
- Use the regulator's current name: SWDA, not SSG, except in search keywords.
- Do not fake urgency, statistics or testimonials.
- Check the same claim in the chatbot's knowledge and quick answers, not just the page.

## Before you finish

1. Run this over the files you changed. Any match must be fixed or have a clear reason:

   ```bash
   grep -nE '(^|[" ])(py|pt|pb|mt|mb)-(1[6-9]|[2-9][0-9])\b|(^|[" ])gap-(1[2-9]|[2-9][0-9])\b|rounded[^"]*\bpy-(0\.5|1|1\.5)\b|\bpy-(0\.5|1|1\.5)\b[^"]*rounded|text-\[1[01]px\]|text-\(--color-purple\)' <files>
   ```

2. Run `npm run dev` and open `http://localhost:3070/`, not another port. Check the changed page at **1440px** and **375px**.
3. Look at a full-page screenshot and check for empty bands, blank columns, orphan grid rows and anything that looks like a template.
4. Check hover and focus states, form states, and that the chat launcher covers nothing important.
5. Test forms with `/api/contact` mocked in the browser, so that no real lead or Gmail notification is sent.
6. Run `npm run build`, which is the type-check gate.

**The dev server arms an hourly local-to-production DB sync** (`db_sync_enabled`, on the hour). Stop it before the hour unless you mean to sync.

Report what you checked in the browser, not just that the build passed.

## Known violations

The November 2026 clean-up fixed the hero, orphan grids, chips, oversized spacing, touch targets and purple text across public pages. Do not reintroduce them. What remains:

- `LikeButton` and the store links in `MobileAppCard` are small rounded **buttons**, not labels, so they stay.
- Legal pages and CMS `[slug]` body text keep a narrow reading width on purpose.
- Admin screens were not part of the clean-up. Bring them up to [Admin UI](#admin-ui) when working in them.
