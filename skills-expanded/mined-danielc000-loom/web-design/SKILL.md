---
name: web-design
description: Apply when designing, building, or reviewing web UI / frontend — visual polish, typography, color, layout, spacing, motion, accessibility, and UX copy. Use to avoid the generic "AI default" look and to make deliberate, restrained design choices. Shipped and kept current by Loom.
---

# web-design

Guidance for producing web UI that looks **deliberately designed**, not auto-generated. The single
failure mode this skill exists to prevent: shipping something a viewer can immediately tell an AI
made. If it reads as the AI default — purple gradients, beige hero, three equal cards, em-dashes,
Inter on slate-900 — it failed, regardless of how clean the code is.

Three ideas run through everything here:

- **Taste is trained, not innate.** Good design is a stack of small, defensible decisions.
- **Unseen details compound.** The 75ms exit animation, the 1px focus ring offset, the tinted neutral
  instead of pure gray: individually invisible, collectively "considered" rather than "fine."
- **Restraint beats expression by default.** One accent, one type scale, one corner-radius scale,
  motion only where it earns its place. Reach for more only when the brief asks.

## When to use this

Use it whenever you design or review web UI (a landing page, dashboard, component, form, marketing
section), and before you call a screen "done." **Don't** treat it as always-on: it's a lens for
visual/frontend work, not a tax on every code change.

## Workflow

1. **Read the brief** (below) — infer intent, write a one-line Design Read, set the dials.
2. **Apply the fundamentals** — type, color, spacing, the interactive states. Pull depth from
   `references/` as needed.
3. **Avoid the anti-patterns** — `references/anti-patterns.md` is the load-bearing don't-list.
4. **Look at it in a browser** — screenshot and eyeball. Do not ship on faith (see *Iterate by eye*).
5. **Run the pre-ship checklist** (below) before declaring done.

## The brief read

Before writing any CSS, infer from what you were asked:

- **Page kind** — product UI / dashboard / landing page / form / docs / editorial. This dominates
  every other choice (a dashboard and an Awwwards landing page want opposite densities).
- **Audience & register** — internal tool / consumer / enterprise / public-sector.
- **Vibe words & references** — anything the brief implies about feel ("calm", "punchy", "premium").
- **Hard constraints** — accessibility requirements, regulated/public-sector rules, brand assets.
  **These override aesthetic preference, always.**

Then write a one-line **Design Read** ("Internal analytics dashboard, dense, calm, a11y-first —
restrained/standard/dense") so the intent is explicit and checkable. **Ask at most one clarifying
question, and only when the brief is genuinely ambiguous** — otherwise pick sensible defaults and
proceed.

## The intent dials

Three orthogonal knobs, each at **three named levels**. Set them from the brief; they bias every
later choice. They are set conversationally — say what they are, don't write them into a file.

| Dial | Levels (low → high) | What it controls |
|---|---|---|
| **EXPRESSIVENESS** | restrained · balanced · expressive | asymmetry, decoration, type personality, layout variety |
| **MOTION** | minimal · standard · rich | how much animates and how present it is |
| **DENSITY** | airy · standard · dense | information per screen, whitespace, sizing |

**Default = `restrained / standard / standard`.** This is restraint-biased on purpose: most real
work is product UI and dashboards, where high expressiveness actively harms usability. Move a dial up
only when the brief earns it — an expressive marketing hero is legitimate; an expressive settings
page is not. Whatever the dials, a **mobile single-column override** and the accessibility constraints
still apply.

## The fundamentals (the spine)

The corroborated core. Compact here; full treatment in `references/`.

- **Type** — one modular scale, one ratio ≥1.25 (1.25 / 1.333 / 1.5); ~5 sizes cover most needs;
  body ≥16px; measure 45–75ch (cap 65–75ch); heading line-height 1.1–1.2, body 1.5–1.7; ≤3 font
  families. → `references/typography.md`
- **Color** — work in OKLCH, not HSL; 60-30-10 weight split; tinted neutrals, never pure gray;
  dark mode is a surface-lightness scale, not an inversion; commit to one accent. → `references/color.md`
- **Layout & space** — a 4pt spacing scale (4/8/12/16/24/32/48/64/96); tight grouping 8–12px,
  section separation 48–96px; deliberate hierarchy (combine size + weight + space); a semantic
  z-index scale (never `9999`); ≥44×44px touch targets; pass the squint test. → `references/layout-spacing.md`
- **Interaction** — design all **eight states** (default / hover / focus / active / disabled /
  loading / error / success); a visible `:focus-visible` ring always; placeholders aren't labels;
  undo beats confirm; skeletons beat spinners. → `references/interaction.md`
- **Motion** — short and motivated. UI animations <300ms, exits ~75% of the enter; custom
  decelerating easing, never bounce/elastic, never `ease-in` for UI; animate only `transform`/`opacity`;
  respect `prefers-reduced-motion`. Decide *whether* to animate before *how* — and motion you commit to
  must actually ship: a page that reads as animated but sits static is broken, so if you can't land it
  cleanly, dial motion down and ship clean static. → `references/motion.md`
- **Copy** — buttons are verb+object (never OK/Submit/Yes); errors say what happened, why, and how to
  fix; no em-dashes; no marketing buzzwords. → `references/ux-writing.md`
- **Accessibility** — WCAG AA minimum (4.5:1 body text, 3:1 large text and UI); this is a floor, not
  a goal.

## Avoid the AI default

The highest-value content in this skill is the **don't-list** in `references/anti-patterns.md` — a
cross-corroborated catalogue of the tells that mark generated UI (AI-purple gradients, reflexive
beige/cream, gradient text, eyebrow chips, numbered section markers, three equal feature cards,
em-dashes, overused fonts). Read it before building and check against it before shipping. The framing:
**if you can tell an AI made it, it failed.**

## If a real design system fits, use it

If the project already uses — or the brief clearly calls for — an established design system, adopt its
**official** package rather than hand-rolling CSS that approximates it. **One system per project;** don't
recreate its tokens by hand, and don't import a system and then override most of it. Match the brief to
the ecosystem it lives in:

| Brief reads as… | Reach for its official system |
|---|---|
| Microsoft / enterprise SaaS / dashboards | Fluent UI |
| Google-flavored / Material product | Material 3 (Material Web) |
| IBM-style B2B / data-dense analytics | Carbon |
| Shopify app surface | Polaris |
| Atlassian / Jira-style product | Atlaskit |
| GitHub-style devtool or marketing | Primer (Brand variant for marketing) |
| UK / US public-sector service | GOV.UK Frontend / USWDS — often legally expected |

If the brief is an *aesthetic* (glassmorphism, bento, brutalist, editorial) rather than a system, there's
no official package: build it with native CSS and be honest about what's borrowed inspiration vs.
official material. If nothing fits, build restrained native CSS on the fundamentals above.

The same holds for a toolkit that copies primitives into the project rather than shipping as a
dependency (e.g. shadcn/ui): when one is present, compose its primitives and retheme its tokens rather
than hand-rolling new ones or overriding per-component styles piecemeal. Its default theme is itself a
recognizable "default look," so retheming (not fighting) it keeps the anti-AI-default goal intact.

## Output modes

- **Build / enhance** — apply the rules directly to the work.
- **Review / fix** — emit a focused `| Before | After | Why |` table, one row per change. This is the
  default review format: concrete, scannable, each change justified.
- **Full critique** (on request) — a deeper pass using the compressed review lens in
  `references/anti-patterns.md` (heuristics + cognitive-load + persona lenses).

## Redesigning an existing UI

A redesign is not a greenfield build — misclassifying the mode is the biggest source of bad redesign
output. First decide: **preserve** (modernise without breaking the brand) or **overhaul** (a new visual
language over the same content and IA). If genuinely ambiguous, ask once.

**Audit before you touch anything.** Record the current brand tokens (accent, type stack, radii), the
information architecture (page tree, nav labels, conversion paths), and the SEO/analytics baseline —
**SEO and analytics migration is the #1 redesign risk.** Extract the existing brand accent *before*
applying the color rules: a brand that is already purple stays purple (the anti-AI-purple rule governs
your defaults, not an established identity).

**Apply the levers in priority order and stop when the brief is satisfied** — each is more risk than the
last: (1) typography, (2) spacing & rhythm, (3) color recalibration (unify neutrals, keep the brand
accent), (4) a motion layer, (5) hero / key-section recomposition, (6) full block replacement (only for a
block that's unsalvageable). Targeted evolution (1–4) is most of the value at a fraction of the risk.

**Never change silently** — get explicit sign-off before touching URL slugs / anchor IDs, primary nav
labels, form field names or order (breaks analytics + autofill), the brand logo/wordmark, or legal /
consent copy.

## Iterate by eye

**Looking at the rules is not the same as looking at the result.** If this session has browser
testing available (a browser-testing-capable profile — a QA or web-design rig with a Playwright/browser
MCP — spawns with one), use it:

1. Render the page or component at the dev server's **actual bound URL**. Read the bound port from the
   tracked server process itself (the framework's startup banner, when captured, e.g. vite's
   `Local: http://…:PORT`, is one way); never assume a default port. If the default is held by another
   process, the dev server binds another port or fails, and the default URL would render a *stale* server.
   For a **static on-disk HTML file** with no dev server (a CV, a rendered report), don't navigate
   `file://` (Playwright's `browser_navigate` blocks it) and don't hand-roll a web server per render.
   Serve its directory over loopback with the bundled helper: `node
   .claude/skills/web-design/scripts/serve-static.mjs start <dir>` prints the URL + the exact tracked
   pid and returns immediately (the server keeps running); eyeball via Playwright at the printed URL,
   then `node .claude/skills/web-design/scripts/serve-static.mjs stop <dir>` tears down EXACTLY that
   tracked pid, after re-checking that pid's command line still matches (pids get reused); never a
   `netstat`/`taskkill` port hunt.
2. **Screenshot it and actually look**: squint test, hierarchy, spacing rhythm, contrast, the eight
   states, dark mode, a narrow (mobile) viewport.
   - For a **throwaway** shot, pass **no filename/path**; the screenshot tool auto-names it into your
     session's out-of-tree scratch/output dir, keeping the working tree clean.
   - To deliberately **persist** a shot (to attach or diff), pass an **absolute path under the directory
     the Playwright client itself allows writes to**. That is not necessarily your generic session
     scratch/temp dir; a path outside Playwright's allowed roots is rejected ("… is outside allowed
     roots"), and a bare or relative name resolves against the repo root, litters the tree, and risks an
     accidental commit.
   - **The auto-naming and `$LOOM_SCRATCH_DIR` mechanics are `@playwright/mcp`-specific:** only a session
     that mounts Playwright gets that allowed root as the `$LOOM_SCRATCH_DIR` env var. A session on a
     DIFFERENT browser tool (e.g. claude-in-chrome) has neither; use that tool's own capture flow.
   - claude-in-chrome `save_to_disk` renders the inline base64 but writes no reachable file. To persist a
     shot as a file, use Playwright `page.screenshot({ path })` against the loopback page (launch with
     `{ channel: 'chrome' }` to reuse system Chrome), or decode the base64 from the transcript for a
     shot already captured.
3. Compare what you see against the fundamentals and the don't-list.
4. Fix what's visibly wrong and repeat. One or two iteration loops catch what reading the code never
   will.

Do not declare a visual task done without having looked at the rendered result. If no browser is
available in this session, say so explicitly rather than implying you eyeballed it.

## Pre-ship checklist

A short gate — not an exhaustive audit. Run it before calling any screen done:

1. **Squint test** — the most important element is obvious within ~2 seconds.
2. **Contrast** — body ≥4.5:1, large/UI ≥3:1; placeholders counted.
3. **Type** — one scale, body ≥16px, measure ≤~75ch, ≤3 families.
4. **Color** — one accent; OKLCH; tinted neutrals; no AI-purple, no reflexive beige, no gradient text.
5. **Spacing** — consistent 4pt rhythm; grouping vs separation is varied, not uniform.
6. **States** — focus ring visible; hover/active/disabled/loading/empty/error all real.
7. **Motion** — motivated, <300ms, custom easing, `prefers-reduced-motion` honored.
8. **Copy** — verb+object buttons, useful errors, no em-dashes, no buzzwords.
9. **Layout tells** — no nested cards, no eyebrow chips, no numbered section markers, no three-equal-cards.
10. **Responsive** — single-column mobile works; nothing overflows or touches the viewport edge.
11. **A11y** — headings not skipped, images have alt text, touch targets ≥44px.
12. **Image framing** — for any embedded photo/portrait, faces/heads are not cropped or cut off by
    `object-fit: cover` or a fixed container aspect ratio. Verify against the ACTUAL rendered crop in the
    browser, not the source image: a center-crop that looks fine full-bleed can decapitate a portrait
    once constrained to its container. Don't apply an optional, IRREVERSIBLE transform (a square/center
    crop, a destructive resize) unless the layout truly needs it; the shown subject's correctness comes
    before a marginal layout gain.
13. **Eyeballed** — you looked at the rendered result, not just the code.
14. **E2E** — if the project has an end-to-end test suite, a new or changed screen ships with (or
    updates) a test in it, run green — see the project's own docs for the harness.

## Provenance

This skill distills three public design skills into Loom's own guidance. See the `NOTICE` file in this
directory for full attribution: **Impeccable** (Apache-2.0, Paul Bakaus — itself building on
Anthropic's frontend-design skill and ehmo's typecraft additions), **taste-skill** (MIT, Leonxlnx —
including its v2 "design-taste-frontend" rewrite), and **Emil Kowalski's** design-engineering skill (MIT).
