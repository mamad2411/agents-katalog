---
name: ryai-plan
description: Turn a vague project idea into a concrete page-and-block build plan, then source each block from the RYAI library instead of generating from scratch. Use when someone describes a site or app they want to build ("I want to make a site for...", "build me a landing page") and has not yet decided what pages or sections it needs — especially non-developers. Also use on "plan my site", "what pages do I need", "/ryai-plan".
---

# RYAI Plan

Turn "I want to build X" into a build plan, then fill it from real components.

**Speak the user's language.** If they write Chinese, ask in Chinese. Never make them
switch. Internal identifiers (categories, slugs) stay English — those are lookup keys,
not user-facing text.

## Rules

1. **Five questions maximum.** Ask one at a time with `AskUserQuestion`, always with
   options. More than five and a non-developer walks away.
2. **No jargon.** Never ask about SSR, routing, or state management. Ask what the site
   *does*, and decide the technical parts yourself.
3. **Never invent slugs.** Every block in the plan comes from `search_prompts`. A slug
   you made up will fail at build time.
4. **At most 3 searches** for the whole plan. Batch by `kind`, never one call per block.

## Step 1 — Ask

| # | Ask | Options | Determines |
|---|---|---|---|
| 1 | What do you want to build? | free text | search terms |
| 2 | What is it mainly for? | get customers / sell something / show your work / internal tool | page list |
| 3 | Do people need to log in or save data? | no, just pages / yes | static pages vs scaffold |
| 4 | What feel are you after? | clean & modern / bold & colorful / dark & technical / warm & editorial | style terms |
| 5 | Do you have a project already? | empty folder / adding to existing | scaffold vs sections only |

Q3 replaces "do you need a backend". Q4 options must read as plain description, never
as design jargon ("neumorphism", "brutalism").

## Step 2 — Derive the page list

Map answer 2 to blocks. These are real `category` values in the library:

| Purpose | Blocks, in page order |
|---|---|
| get customers | `header` `hero` `features` `how-it-works` `testimonials` `pricing` `faq` `cta` `footer` |
| sell something | `header` `hero` `product` `categories` `benefits` `testimonial` `pricing` `contact-us` `footer` |
| show your work | `header` `hero` `projects` `about-us` `process` `stats` `contact-us` `footer` |
| internal tool | `dashboard` `form` `stats-metrics` `table` — use `kind: "apps"` |

Trim to what they actually need. Nine blocks is an upper bound, not a target.

Other useful categories: `about` `benefits` `bento` `blog` `brands` `calls-to-action`
`case-studies` `integration` `marquee` `services` `slider` `team` `use-case`
`why-choose-us` `404`. Pass any of these straight to `search_prompts`.

`kind` selects the shape: `sections` for page blocks (largest set), `sites` for whole
pages, `backgrounds` for background visuals, `apps` for tool UIs.

## Step 3 — Search

Batch by kind. Translate the user's wording into English keywords — the library is
indexed in English, so a literal non-English query returns nothing.

```
search_prompts({ keywords: ["saas", "course", "education"], kind: "sections",
                 category: "hero", limit: 12 })
```

`search_prompts` is free and needs no account, so run it before asking anyone to sign up.

Pick per block, in this order:
1. `hasCode: true` — ships real component code, far more reliable than generating
2. matches the style from Q4
3. lowest `tier` — do not put a premium-tier block in the plan when a lower-tier one fits

## Step 4 — Write PROJECT.md

```markdown
# <project name>

Stack: <decided from Q3 — do not ask>
Style: <from Q4>
Pages: <list>

## Home
- [ ] hero — `slug-from-search` (code)
- [ ] features — `slug-from-search` (prompt)
- [ ] pricing — `slug-from-search` (code)
```

Mark each `(code)` or `(prompt)` from `hasCode` — the build step needs it to choose
between downloading files and generating.

## Step 5 — Confirm, then stop

Show the plan. Ask if it looks right. Fix what they want changed.

**Do not start building here.** Building is `ryai-build`. Tell them the plan is saved
in `PROJECT.md` and building is the next step.

If any chosen block is locked, say plainly which membership tier it needs and let them
decide. Never quietly swap in a worse block to dodge the paywall.
