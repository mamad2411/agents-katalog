---
name: mcp-page-authoring
description: Best practices for authoring a Classic Unbounce landing page from HTML/CSS/JS through Unbounce MCP — create_page_from_html, create_variant_from_html, and update_variant_from_html. Use when the user asks for a Classic or custom-HTML page, when a new page needs a widget the AI Builder catalog cannot express, when the account does not have AI Builder, or to edit or add a variant to a page already authored through these HTML tools; also to personalize page text by URL parameter (Dynamic Text Replacement). Custom page-level JavaScript on an AI Builder page is set_ai_builder_custom_code (mcp-ai-builder-authoring), not this skill. A new page otherwise goes through the mcp-ai-builder-authoring skill. Not for AI Builder pages or pages hand-built in the Unbounce builder.
requires:
  mcpServers:
    - unbounce-mcp
---

# Authoring an Unbounce MCP page

These rules apply when you write the HTML/CSS/JS body for `create_page_from_html`,
`create_variant_from_html`, or `update_variant_from_html`. The page is a full-bleed
custom-HTML page — you own the markup end to end. Design the page to be optimized
for conversions: by default, every layout, copy, and hierarchy decision should
serve the page's single conversion goal.

This covers **MCP-authored pages only**, and the split is exclusive both ways:

- A page hand-built in the Unbounce builder is not editable this way —
  `update_variant_from_html` refuses it. Replicating or modernizing a
  builder-built page is a different, audit-first job.
- An MCP-authored page **cannot be edited in the Unbounce builder**. Never tell
  the user they can open, tweak, swap images, or finish the page "in the
  Unbounce builder/editor" — they cannot. Every edit goes through these MCP
  tools: the user asks for the change, or supplies updated HTML.

AI Builder pages (`create_ai_builder_page`, `edit_ai_builder_page`,
`create_ai_builder_variant`) are a separate
route covered by the `mcp-ai-builder-authoring` skill; they stay editable in the
Unbounce AI builder, so the rule above does not apply to them.

A new Classic page needs the Classic Builder on the account's plan: check
`builders.classic` for the client's account in `list_accounts_and_clients`. When
it is false, take the AI Builder route instead and tell the user why;
`create_page_from_html` refuses such an account before anything is uploaded,
with `create-page-from-html.classic-builder-not-entitled`, or
`create-page-from-html.no-builder-entitled` when the plan has neither builder. A
`create-page-from-html.not-author-or-not-entitled` at the create means the user
is not an author on the client or the plan lacks the Classic Builder; `builders`
tells them apart.

## Updating a variant: HTML/CSS replace, JS is left alone

`update_variant_from_html` full-replaces the body HTML and the stylesheet, so
send every stylesheet the variant should keep on every call. **JavaScript is the
exception: omit `scripts` and the variant's existing custom-JavaScript elements
are kept**, reported back as `scripts_preserved`.

That matters because a variant can carry scripts nobody authored through these
tools — an **Unbounce popup** attaches itself as one. So:

- Editing HTML or CSS? Just omit `scripts`. The popup and anything like it
  survive, and you don't need to know they were there.
- Changing the scripts? Pass `scripts` with the **complete** desired set — it
  replaces all of them, including external includes. Whatever it drops comes
  back in `removed_scripts`. Those entries — and the `scripts_preserved` ones —
  are already in `scripts` entry form: pass one straight back to restore it,
  unchanged, no translation. A plain include appears as `src` (with `async` /
  `defer` if it had them); everything else — including an include whose tag
  carries other attributes, such as a `data-*`-configured analytics embed — comes
  back as verbatim `tag`. Read the variant first
  (`get_variant`) if you don't know what's there.
- Removing every script is deliberate: pass `scripts: []`.

## Writing a `scripts` entry

Each entry is one custom-JavaScript element. Use exactly one of:

- **`ref`** — an `upload://` reference to a .js file. Its text is the script
  body; don't wrap it in `<script>` tags. A bare string entry is shorthand for
  this.
- **`src`** — an absolute http(s) URL to include, for a third-party embed: an
  Unbounce popup (`https://<id>.js.ubembed.com`), a tag manager, a chat widget, a
  pixel. Add `async` / `defer` here if the vendor's snippet has them. This is the
  right form when the user hands you a `<script src=…>` tag.
- **`tag`** — verbatim `<script>` markup, for what the other two can't say: a
  `type="module"` script, a tag with both a `src` and a body, or several tags
  that belong together.

Add `name` (what the user calls it — it labels the element in Unbounce's Custom
JavaScripts panel) and `placement` (`head`, `body_top`, or `body_bottom`,
default). Consent managers, tag managers, and anti-flicker snippets belong in
`head`; most other things are fine at the default.

`get_variant` returns every script in the matching form, so you can read, edit,
and re-submit any of them unchanged.

**A `<script>` in the body HTML does run on the published page** — it is stored
verbatim in the Custom HTML block and served as real markup. But it lands
body-placed, unnamed, and invisible in the builder's Custom JavaScripts panel, so
prefer a `scripts` entry whenever the user names the script or asks for a
particular placement.

## Conversion-focused structure

A landing page exists to convert — design toward that goal affirmatively, not
just by obeying constraints. Treat the bullets below as the default posture: if
the user explicitly asks for something that works against conversion (a nav menu,
multiple offers, a long form), note the trade-off briefly once, then build what
they asked for.

- **Benefit-led headline.** The headline states the visitor's payoff and matches
  the offer and traffic intent — not the company name or a clever tagline.
- **CTA prominence and hierarchy.** One primary call to action, visible without
  scrolling; size, contrast, and whitespace should point the eye at it. On longer
  pages, repeat the CTA as anchor links.
- **Minimal form friction.** Ask only for the fields the offer genuinely needs —
  every extra field costs conversions. Label the submit button with the payoff
  ("Get the guide"), not "Submit".
- **Real social proof near the ask.** Place testimonials, numbers, or logos the
  user supplied next to the form or CTA. **Never fabricate trust signals** — no
  invented testimonials, star ratings, customer logos, statistics, or scarcity
  claims ("Only 3 spots left!"). If the user hasn't supplied any, ask for it while
  you're still gathering requirements; once you're already generating the page,
  leave social proof out and mention the omission so the user can supply proof
  for a follow-up edit.
- **One form.** A lead-gen page has exactly one `<form>`. Never render two. CTA
  buttons in sections where the form isn't visible are anchor links
  (`<a href="#form">`) that scroll to the single form — not extra forms. Pages
  with no form (click-through pages) are exempt.
- **No navigation.** No nav bars, menus, or footer link lists. Every outbound
  link is an exit that costs conversion. The only acceptable links are the primary
  CTA anchors and legally required links (privacy/terms), placed quietly in the
  footer.
- **Responsive, clean HTML.** Use normal document flow (flexbox/grid), relative
  units, and `max-width` — not absolute positioning. The page must reflow on
  mobile.

## Assets

- **Prefer `upload` over fat data URIs.** Base64 data URIs work but bloat the
  payload (~33% larger) and count against the 1 MB tool-input cap. Upload real
  images/fonts first and reference the returned CDN URL. Relative refs in your
  bundle and data URIs are rehosted for you; identical bytes are de-duplicated
  automatically against the client's asset library.

- **Rehosting does not reach every data URI — check `inline_assets`.** An image or
  font data URI is extracted from your markup, your CSS, and from a plainly quoted
  JavaScript string literal (`img.src = "data:image/png;base64,…"`). It is **not**
  extracted from a template literal, a value built by concatenation, a comment, or
  the verbatim markup of a `{ tag }` script entry — a rewrite there cannot be proven
  safe, and `{ tag }` markup is yours, supplied whole, so it is never edited for
  you. **Audio and video are never extracted** either, because the asset store
  refuses them (BD-13366 tracks the upstream change that would allow it, and fonts
  are blocked on the same map). Anything left inline is listed in the result's
  `inline_assets`, with a note telling you what to do. Treat a non-empty list as
  work: those bytes ship inside the page on **every** request, cannot be cached or
  served by the CDN, and are billed as egress for as long as the page is live.
  Upload the file and reference its URL instead.

- **One upload call per bundle.** Every `upload` / `upload_inband` call creates a
  fresh upload folder, and a relative reference inside your HTML/CSS (e.g.
  `src="page.js"`, `url(images/hero.png)`) resolves only within the HTML's own
  folder — so upload the HTML together with everything it references by relative
  path in one call. Refs from different calls still work anywhere a tool takes an
  explicit `upload://` reference (`html_ref` / `css_refs` / a `scripts` entry's
  `ref`, or written
  in full inside the markup); refs are immutable snapshots, so re-uploading a file
  never changes what an earlier ref points to.

- **An image's bytes must match its extension.** The file extension declares the
  type an asset is stored and served as, so the bytes are checked against it: a PNG
  named `.svg`, or anything that isn't a real image, is refused rather than stored
  under the wrong type. Name files for what they actually are.

- **SVGs must be static artwork.** An SVG is served as a live document, so one
  carrying `<script>`, an `on…=` event handler, a `<foreignObject>`, a
  `javascript:` URL, or an external `href` is refused. Ordinary exported artwork —
  including animated SVG — is fine. If an SVG is rejected, flatten it on export or
  use a PNG.

## Authoring from a client that can't run shell commands

`upload` and `download` hand you `curl` commands to run locally. If your client
has no shell or filesystem (a web/desktop chat that only calls tools), you can't
run them — use the **in-band** pair instead:

- **`upload_inband`** — pass each file's **text content inline** (an array of
  `{ path, content }`); it returns the same `upload://` references you'd get from
  `upload`. Wire those to `create_page_from_html` / `create_variant_from_html` /
  `update_variant_from_html`'s `html_ref` / `css_refs` / `scripts` exactly as
  usual — those tools don't change.
- **`download_inband`** — pass the `upload://` references from `get_variant` (or
  `upload_inband`) and it returns the content **inline in the result**, so you can
  read a variant back and iterate.

Constraints, because the bytes travel through the conversation:

- **Text only.** HTML/CSS/JS. **Images and fonts must be external `http(s)`
  URLs** — you can't upload binary bytes this way. Host the image elsewhere and
  reference its URL, or reuse an existing asset's `cdn_url` from `list_assets`;
  `create_page_from_html` leaves external URLs untouched. `download_inband`
  refuses a binary or over-2 MiB object and tells you to use `download`.
- **Keep files small.** The request rides the normal transport, so a very large
  paste will fail — author lean pages.
- Because your images are always external URLs, keep `check_external_refs` at its
  default (`fatal`) so a dead image URL is caught before the page is created,
  not after publish.

## Scripts, forms, and the auto-injected bits — don't fight them

- **Don't hand-wrap JS in `<script>`.** Provide raw JavaScript, not a `<script>`
  block — it's wrapped for you, so wrapping it yourself double-wraps it. (This is
  the opposite of what you'd do writing a static HTML file.)
- **Form submission works out of the box; the confirmation is a customizable
  fallback.** Submission is wired up automatically from the form fields you
  author — no plumbing needed. If you don't handle the post-submit experience
  yourself, a default confirmation dialog is shown. To customize it, register a
  post-submit handler — see the next bullet for the one way that works.
- **Register post-submit handlers with `.push(fn)`, never `= fn`.** The published
  runtime stores `window.ub.hooks.afterFormSubmit` as an **array** and invokes it
  with `Promise.all(hooks.map(h => h(...)))`. Assigning a function replaces the
  array, so the first submit throws `TypeError: hooks.map is not a function`, the
  post-submit promise rejects, and **neither your custom confirmation nor the
  default dialog ever shows**. Always push:

  ```js
  window.ub = window.ub || {};
  window.ub.hooks = window.ub.hooks || {};
  window.ub.hooks.afterFormSubmit = window.ub.hooks.afterFormSubmit || []; // defensive
  window.ub.hooks.afterFormSubmit.push(function () {
    // reveal your confirmation panel here
  });
  ```

  This is independent of whether the form is multi-step. When reviewing a page,
  grep the controller for `afterFormSubmit =` and rewrite any assignment to a push.

- **Never intercept the submit yourself.** Do not add a `submit` listener to the
  form (or to `document`), set `onsubmit`, or call `form.submit()` /
  `requestSubmit()`: the runtime's own listener does the validation and the
  POST, and yours either stops it (no lead) or races it. The authoring tools
  reject all of these at write time (rule E6), in inline `<script>` blocks and
  `scripts` entries alike. A `click` listener on the button for analytics is fine.
- **Never POST to the gateway yourself.** No `fetch`, `XMLHttpRequest` or
  `navigator.sendBeacon` to `/fsg`, `/fsn`, `/fs` or the form's `action` — a
  request without the runtime's `lp-form-submit-method=ajax` marker is flagged
  `Form/NonAjax` by spam filtering and lands in spam, never in leads. Also
  rejected at write time. Mirroring the lead to your own webhook is fine — do it
  from inside `afterFormSubmit.push(...)`, to your third-party URL.
- **Assigning over a hook is rejected too** — `= fn` or `= [fn]` on any of the
  three `window.ub.hooks` arrays. The init guard from the snippet above —
  `window.ub.hooks.afterFormSubmit = window.ub.hooks.afterFormSubmit || [];` — is
  the one assignment that passes. Only a `.push(` counts as "the author handles
  the confirmation"; an assignment does not suppress the default dialog.

- **A signature comment is auto-injected** at the top of every variant body
  (Unbounce MCP version · client · timestamp). It's re-stamped on each write — don't
  duplicate it, don't strip it, and don't treat it as page content when you read a
  variant back.

## Conversion goals — ask the user what should count

A page converts when a visitor does the thing it exists for. Unbounce counts
that through **conversion goals**: the form submission (on by default) and any
links you nominate. After creating or updating a page, the tool result's
`conversion_goals` block lists every candidate — the form plus each distinct
link/phone URL with its anchor texts (`get_variant` shows the same for an
existing page). Use it to have the goal conversation:

- **Ask the user which candidates should count**, then call
  `set_conversion_goals` with the **complete** desired set (it replaces, not
  adds). Recommend the goal that matches the page's purpose: a click-through
  page's goal is its CTA link, not an incidental newsletter form.
- **Goals are URL-identified.** Every anchor pointing at a chosen URL converts —
  the candidate's `anchor_texts` length shows how many places that is. Two
  near-identical URLs (trailing slash, query param) are separate candidates;
  point that out if they look like the same destination.
- **A trackable CTA must be a real `<a href>`** (http(s) or `tel:`). JS-driven
  buttons can't be tracked — goal tracking rewrites the href. `#anchors` and
  `mailto:` can't be goals (platform rule).
- **Turning the form goal off** (`form_submission: false`) still captures every
  lead; it just stops counting submissions as conversions.
- **Link/phone goals don't show in the Unbounce builder's Conversion Goals
  panel** — but they _are_ tracked. That panel lists only builder-native elements
  (form, button, image, linked text box), and an MCP-authored page is a single
  custom-HTML element, so its anchors never appear there even though a click on
  the published page counts as a conversion. If a user asks why a link goal is
  "missing" in the builder, that's expected: manage these goals here with
  `set_conversion_goals`, not in the builder (editing goals in the builder can
  drop them). The form goal is unaffected — a form is builder-native.
- **Changing goals on a published page** redefines its conversion rate
  mid-history. Relay the tool's stats note: `reset_page_stats` gives a clean
  baseline if the user wants one (destructive — their call).
- Goals persist across edits automatically — updates re-apply them and report
  any new candidate URLs or orphaned goals; you only need `set_conversion_goals`
  when the _set_ should change.

## Google Analytics click tracking — add it on every page

When a page's domain has the Google Analytics integration on, the published page
already tracks pageviews and form submissions — but **not clicks on links**,
because Unbounce's built-in GA link tracker only attaches to elements the Unbounce
builder produces, which an MCP page (hand-written `<a>` tags) doesn't have. Close
that gap on every page you author:

- **Include [`scripts/ga-click-tracking.js`](scripts/ga-click-tracking.js) as a
  `scripts` entry** (name it e.g. "GA click tracking", default `body_bottom`).
  Upload the file (`upload`, or `upload_inband` without a shell) and pass the
  returned `upload://` reference as the entry's `ref` — see
  [Writing a `scripts` entry](#writing-a-scripts-entry); never hand-roll your
  own. It wires every `<a>` and emits builder-matching GA events.
- **It's safe by default.** The script feature-detects `gtag`/`ga` and no-ops when
  the domain has no GA integration, so add it unconditionally — that's why it's
  default-on, not something to ask about.
- **But only ever one copy.** When editing a page that already carries a GA
  click-tracking entry — a modernized page will — re-send it unchanged if you
  are passing `scripts` at all, rather than adding a second, which would
  double-count every click. Unconditional means don't ask the user, not don't
  look first. ("Leave it alone" is the wrong instruction here: passing the array
  replaces the whole set, so leaving an entry out deletes it.)
- **Never add the GA loader** (`gtag.js` / `analytics.js` / a `gtag('config', …)`
  call). GA is injected by Script Manager; a second loader double-counts
  pageviews. This script only sends events.

The why, the guardrails, and the maintenance note live in
[rules/google-analytics.md](rules/google-analytics.md) — read it if you need to
explain the behaviour or hit an edge case.

## Third-party form endpoints (Insightly, Marketo, HubSpot, Pardot, …)

Sometimes the form must POST leads to an external system — the user is cloning a
page with an existing vendor-hosted form handler, or their CRM owns the lead
flow. That is the one case where you deliberately bypass the built-in form
handling described above.

- **A literal `<form>` gets taken over.** Submission of any `<form>` you author
  is wired to Unbounce lead capture automatically — the `action` you wrote is
  not what handles the submit. To preserve an external endpoint, don't put the
  `<form>` in the HTML: leave a mount point (`<div id="form-mount"></div>`) and
  **inject the form markup at runtime from your JavaScript** (build the markup
  as a string, set the mount's `innerHTML`, then load the vendor's scripts in
  the order the reference page loads them). The runtime leaves JS-injected
  forms alone. The injected string must be the vendor's documented embed
  snippet (or the reference page's markup) reproduced verbatim — never
  interpolate unsanitised user-supplied or URL-derived values into it.
- **Say what the user gives up.** A JS-injected form bypasses Unbounce lead
  capture entirely: no leads in Unbounce, no
  conversion tracking, and `get_variant` reports `has_form: false`. Submissions
  exist only in the external system. (`has_form` is derived from the authored
  HTML source, so it is deterministically false for an injected form — that's
  expected, not a defect.) State this trade-off when you propose the approach —
  the user may prefer the built-in form plus a separate CRM integration
  instead.
- **`afterFormSubmit` hooks never fire for an external form.** The
  `window.ub.hooks` machinery only runs for Unbounce-captured forms. Build the
  post-submit experience (thank-you message or redirect) into your own code, the
  way the vendor's embed does it.
- **Expect domain allowlists — the top cause of "the button does nothing".**
  reCAPTCHA site keys and vendor form handlers are typically locked to approved
  domains. On a preview or test-domain URL the key fails domain validation, no
  token is issued, the submit callback never runs, and clicking the button
  silently no-ops — the form is not broken, the domain isn't approved. Warn the
  user up front that the form can't fully work until the page's final domain is
  added to the reCAPTCHA key and the vendor's allowed domains.
- **Verifying before go-live.** Have the user open the browser console and click
  submit — a reCAPTCHA "Invalid domain for site key" error confirms the
  allowlist diagnosis. To exercise the rest of the flow on a test domain, they
  can temporarily swap in Google's public reCAPTCHA **test** site key, then
  restore the real key before publishing to the approved domain. Never leave
  the test key on a live page — it returns a passing token for **every**
  request, including automated bots, so spam and abuse submissions flow
  straight through to the vendor endpoint unchallenged.
- **The one-form rule still applies.** The injected form is the page's single
  form; other CTAs anchor-link to its section.

## Dynamic Text Replacement (DTR)

DTR personalizes page text from a URL query parameter, so the same page shows
different words depending on how it was reached — e.g. visiting with
`?city=Portland` shows "Portland" where the page would otherwise read "Vancouver".
Common for paid-search keyword insertion and location/audience personalization.

There is no DTR tool: you add it by writing a `ub:dynamic` tag directly in the
HTML you author; it takes effect when the page is served.

```html
<ub:dynamic method="titlecase" parameter="city">Vancouver</ub:dynamic>
```

- **`parameter`** — the URL query-string key that supplies the replacement value
  (`parameter="city"` → `?city=Portland`). Pick a short, lowercase name that
  matches the meaning of the text.
- **Default text** — the tag's inner text (`Vancouver` above) is shown when the
  page is visited without that parameter. Always make it a sensible standalone
  value; most visitors arrive with no parameter and see exactly this.
- **`method`** — casing applied to the incoming value: `titlecase` (the right
  default for display text), `uppercase`, `lowercase`, or `capitalized`. Omit
  `method` to insert the value exactly as passed.
- **`wrap`** (optional) — set `wrap="true"` to wrap the substituted value in a
  `<span class="ub-dynamic">…</span>` so you can style or target just the dynamic
  text with CSS. Omitted, the value is inserted inline. Rarely needed.
- **Testing** — resolution happens at serve time on the **published** page (editor
  previews show the default, not a substituted value). To verify, publish, then
  load the page with `?<parameter>=SomeValue` appended — and give the user that
  test URL so they can check it.

**Ask before adding DTR.** Do not add it on your own initiative. When creating or
editing a page, ask the user whether they want any text personalized by a URL
parameter; if so, confirm which text and which parameter name(s), and wrap only
the text they approve. If they decline, author plain text.

**DTR is a paid feature — it may be plan-gated.** If the client's account isn't
entitled to Dynamic Text Replacement, the content-write tools reject HTML
containing a `<ub:dynamic>` tag with a `…dynamic-text-not-entitled` error (the
`bulk_edit_variants` batch reports it as a per-variant `error`). When that
happens, either remove the `<ub:dynamic>` tag(s) and author plain text, or tell
the user their plan needs Dynamic Text Replacement to use it — check the plan
with `get_account_plan`. Already-published DTR pages keep working regardless.

**DTR also works in the page title and meta fields.** `set_page_metadata`'s
`title`, `description`, and `keywords` accept `<ub:dynamic>` tags — e.g. a
`<title>` that echoes the ad keyword for paid-search campaigns. The same
ask-first rule and plan gate apply. The Open Graph fields do **not** take DTR
(social scrapers fetch the page without campaign parameters anyway).

## Page metadata (SEO & social sharing)

The page `<title>`, meta description, robots noindex, favicon, and Open Graph
(`og:*`) tags are **page settings, not page HTML** — your authored HTML becomes
the page **body**, where search engines and social scrapers never look for
them. Set them with `set_page_metadata`; read them back via `get_variant`'s
`metadata` block (on an AI Builder page, via `get_ai_builder_document` — see
the `mcp-ai-builder-authoring` skill). As a safety net, the HTML-authoring tools **auto-extract**
these head tags from submitted markup and apply them as metadata (reported
under `head_metadata` in the result) — but on `update_variant_from_html` /
`create_variant_from_html` that lands on **one variant only**, so prefer
`set_page_metadata` for deliberate metadata work and to converge variants.

- **Always set a title and description** on a page the user intends to publish
  — a page without them shows the platform default (or nothing) in search
  results and social shares. Derive them from the page's offer; keep the title
  ≲60 characters and the description ≲160 (search results truncate past that).
- **Open Graph drives the social share card** (Facebook, LinkedIn, Slack,
  iMessage, …). `type: "website"` is right for landing pages; give it a
  `title`, `description`, and an `image` (1200×630, under 5 MB, https) — a
  card without an image renders as bare text. X/Twitter reads these `og:*`
  tags too, but shows the small card without a `twitter:card` meta tag — which
  the platform cannot store, so don't promise a large Twitter card.
- **Skip `keywords`.** Google has ignored meta keywords since 2009 and heavy
  keyword lists can read as a spam signal. Leave it unset unless the user
  insists.
- **`hide_from_search_engines: true`** emits a robots noindex — right for
  campaign pages the user doesn't want in organic search results; ask rather
  than assume.
- **Metadata is applied to every active variant by default** (variants share
  one URL, so divergent titles/OG make the search snippet and share card
  depend on the traffic split). Target one variant with `letter` only when the
  user deliberately wants that.
- **Staged like content**: on a published page the live head keeps its old
  values until the next `publish_page` — say so when you set metadata on a
  live page.
- **Head tags with no platform slot** — `twitter:*`, `<link rel="canonical">`,
  hreflang alternates, `og:*` beyond type/title/description/image/url — cannot
  reach the published `<head>`; the authoring tools warn when submitted HTML
  contains them. Don't promise them to the user.

## Reviewing your work

- Read a variant's current content back with `get_variant`.
- **Previewing locally:** the source refs `get_variant` returns (`html_ref` /
  `css_refs` / a `scripts` entry's `ref`) are streams of one page and do **not** render
  individually — `body.html` opened alone shows an unstyled fragment. For a
  local preview, fetch the also-returned **`preview_ref`** (`preview.html`, via
  `download` or `download_inband`) and open that file: it is a standalone
  composed document (images load from their CDN URLs; form submission is
  disabled in it). It is **view-only** — never edit it or submit it back as
  `html_ref`; make edits in the source files and resubmit those.
- Content is **staged** by the create/update tools; it goes live on `publish_page`.
- `list_page_variants` returns a `preview_url` per variant — a logged-in link for
  a human to **review** a staged variant before publish. It is a viewing
  affordance only, not an editing path — don't present it as a way to edit.
