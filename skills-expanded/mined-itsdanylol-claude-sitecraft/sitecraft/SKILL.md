---
name: sitecraft
description: Builds a complete website from brief to a verified result, around one original idea. It researches the product, writes three concepts and keeps the boldest that fits, invents the layout with no templates, builds every page and state with a real motion layer, makes the imagery from the concept, then has a fresh critic judge screenshots and motion filmstrips blind before checking accessibility, SEO and speed. On a redesign it captures the old site first and ends with diagonal before/after PNGs. It opens Base44 apps to a public landing page with the app's own login. Use when the user asks to make, build, design, launch or redo a website, landing page, portfolio, product site or one-page app front end, or says a site looks generic, boring or AI-made.
license: CC-BY-4.0
metadata:
  composes: marketing, unslop, dataviz, run, built-in-browser
  credits: >-
    Shape from unslop by Damir Sokolovsky (@heydamir, heydamir.design/unslop, CC BY 4.0). Concept method from
    juliobsz/skills awwwards (MIT); design dials from tdimino minoan-frontend-design, and the variety idea from Leonxlnx taste-skill and
    bencium impact-designer (MIT); generative art from anthropics/skills algorithmic-art and canvas-design, testing
    from webapp-testing (Apache-2.0); audit method from addyosmani/web-quality-skills (MIT). All paraphrased; scripts
    are independent rewrites.
---

# Sitecraft

Nobody remembers a tidy site. They remember one that *is* something: the idea is the product's own, and every page grows from it. Sitecraft finds that idea first, then builds every section from it, and only then polishes.

Clean is the floor, not the goal. A page with no slop and no idea is just a better template.

And it is the whole site, not a hero. Every page, every button and link state, every menu, form, empty and error state, the 404, and how the site loads and moves between pages. A beautiful first screen with default inner pages is a mock-up.

## The run

0. **Choose and connect.** If the user has not said what they have, ask them to choose: a Base44 app, existing code (a project folder or repo), a live URL, or a new site. Then say what must be connected. Base44 app: the Base44 connector. Existing code: the code base, by opening Claude Code in the folder or adding the repo. Live URL or new site: nothing. If it is not connected, say so, explain how, and wait.

1. **Learn the product, and capture the before.** On a redesign, first run `scripts/beforeafter.mjs capture <url> --out sitecraft-output/.before`, before you change anything, so the old site is kept. If it is a Base44 app (an `@base44/sdk` dependency, a `base44Client` file, or a `*.base44.app` address), follow [base44.md](references/base44.md) all the way through. A Base44 app needs the Base44 connector: if it is not connected, tell the owner to connect it and stop. Any app that is not Base44 has no connector, so its project folder or repo must be connected to the code base; if it is not, ask for that. Then read what exists before asking anything: the repo, files, live site, the web, competitors, and the words customers use. Follow [research.md](references/research.md). Write `site-brief.md`, with a source on every fact. Map the whole site: every page and template, plus a state list covering every control and screen state. For an existing site, run `scripts/states.mjs` to crawl it and capture what is there today. Ask only about the gaps that are left, with a best guess for each.

2. **Find the idea, then stop.** Use [concept.md](references/concept.md):
   - Write three concepts from three territories: the name, the material, the place, the process, or a formal system.
   - Kill any concept that a competitor could use, that only touches the hero, or that blocks the action.
   - Keep the boldest one that survives.
   - Set the dials and invent the layout from the concept. There are no layout templates, and the layout must not repeat an earlier site's.
   - Write the vibe: a feeling, five sense words, and a scene.
   - Build a one-screen style tile.

   Show the concept, the vibe and the tile, then wait. If the user said to just do it, judge the tile yourself and go on.

3. **Words.** Invoke `marketing`, and give it the concept and the brief so it does not re-ask. The copy goes into the page before the layout. No invented customers, numbers or reviews. Mark anything unknown as `[needs: ...]`.

4. **Build the concept, on every page and in every state.** Work through the site map and the state list, not just the home page:
   - Inner page templates, the nav open and closed, and the footer.
   - Hover, focus, active, visited and disabled states.
   - Forms in error and in success.
   - Empty and loading states, the first-load moment, page transitions, and the 404.

   The concept carries into every one of them. Every site ships a motion layer: an entrance, scroll motion, micro-interactions on every control, page transitions and one signature move, all written to [craft.md](references/craft.md) even though you cannot watch them. Build its structure across every section, its signature moment, and its imagery: real material, generated images, or generative art made from the product's data. Push each section once to its bolder version, then edit out what does not serve the idea. Use [craft.md](references/craft.md) for the grid, type, color and stack. If there are charts, invoke `dataviz`.

5. **Clean up.** Invoke `unslop` in cleanup mode. It fixes spacing, type and details and removes slop. Its restraint (quiet chrome, one accent) applies to the chrome only; it never flattens a concept move.

6. **Blind review.** Run `scripts/design-audit.mjs`, adding `--bold` if the concept is loud on purpose. Run `scripts/states.mjs` for every page's state sheets, the loading frames and the 404, and `scripts/motion.mjs` for the motion filmstrips. Then send a fresh critic only the screenshots, per [review.md](references/review.md). It names the feeling before it learns the vibe, says whether it would stop scrolling, and scores thirteen criteria, including the whole site. Fix what it ranks highest. It passes with an average of 4 or more, Vibe and Originality at 4 or more, and nothing under 3. Allow at most three rounds. If Originality is below 4, the fix is a stronger idea, not more polish.

7. **Verify.** Run `scripts/with-server.mjs` around `scripts/verify.mjs` (every page, at six widths) , `scripts/states.mjs` (every control and state) and `scripts/motion.mjs` (motion is present, smooth, and stops with reduced motion), then do the checks in [quality.md](references/quality.md): keyboard, contrast, SEO, page weight and security. Fix the most severe issues first. If a fix changes the look, render again.

8. **Before and after, and the output folder.** Capture the new site with `scripts/beforeafter.mjs capture <url> --out sitecraft-output/.after`, then run `compose --before sitecraft-output/.before --after sitecraft-output/.after --out sitecraft-output/before-after --title "<site>"`. That gives a diagonal before/after PNG for every page at desktop and phone width. Gather every image into `sitecraft-output/`: `before-after/`, `screenshots/` (before and after), `states/`, `motion/` and `loading/`. Give the user the full path to that folder.
9. **Report.** Cover the concept, what was built, the stack, the scores for each round with screenshots, the checks with their results, what was not verified, and what the user must supply. Do not publish, deploy, buy anything or create accounts without the user's yes.

To improve an existing site, capture the before and score it first (step 6). Keep its brand, find the idea it is missing, and then follow steps 3 to 8.

## Quick mode

The full run is long: research, three concepts, every page and state, up to three critic rounds and checks at six widths. Before starting, say so in one line, and offer quick mode when the job is small. Use quick mode when the user asks for it ("quick", "just a landing page", "rough draft", "one page"), or the site is a single page with no existing site to redesign. Quick mode keeps the idea and drops the volume:

- **Research:** read what the user gave you and the live site, if any. Skip competitor and customer-language searches. The brief can be short, with sources still marked.
- **Concept:** write two concepts, not three, and still kill the swappable one. Skip the ASCII wireframes and the style tile; show the concept and vibe in a few lines, and wait only if the user is present.
- **Build:** one page, its nav (open and closed on phones), its form states and the 404. Motion: an entrance, control feedback and the one signature move.
- **Review:** one critic round, not three. Same pass bar; if it fails, report the scores and the top fixes instead of looping.
- **Verify:** `verify.mjs` and `states.mjs` on the page. Skip `motion.mjs` and before/after unless it is a redesign.

Tell the user what quick mode skipped, so they can ask for the full run later.

## What makes it good

- **One idea, everywhere.** It can be said in five words, it fails with a competitor's name, and it shapes every section.
- **The whole site.** Every page in the map and every state in the list is designed. None is left on browser defaults, and the concept is still there on page 12.
- **One moment people screenshot.** Everything around it is calm, so it lands.
- **Imagery from the idea.** No stock photos, no empty frames, and no product card standing in for a visual.
- **Type with a voice.** Real scale contrast, chosen families, and the product's own notation used as design.
- **A feeling on purpose.** The critic's blind words match the vibe.
- **It moves.** It has an entrance, motion as you scroll, a response from every control, and transitions between pages, all in the concept's motion verb. Motion is smooth, uses only transform and opacity, and stops completely with reduced motion.
- **Works for everyone.** It reads with no JavaScript and with reduced motion, works by keyboard, at 375px and on slow connections, and meets 4.5:1 contrast.
- **Honest.** Placeholders are marked, demo data is labelled, and nothing is claimed that was not checked.

## Never

- Purple-to-blue gradients, glow, glassmorphism or blobs.
- Uppercase eyebrow labels, "01 / 02" on things that are not steps, or a fade-and-rise on every section.
- A bento grid or a three-card row as the default layout.
- Fake stats, logos or testimonials.
- Scroll-jacking or a hidden cursor.
- Copying another site's look. The idea comes from the product, not from a gallery.
- Layout templates. Every layout is invented from the concept.
- Making a Base44 app public, or changing its login, without the owner's yes.

## Tools

The sibling skills `marketing`, `unslop`, `dataviz` and `run` ship in the same repo. Installed as the Claude Code plugin, they are named `sitecraft:marketing`, `sitecraft:unslop`, `sitecraft:dataviz` and `sitecraft:run`; invoke whichever name the session lists. The scripts need Node 18+ and Playwright with Chromium.


| Need | Use |
| --- | --- |
| Inventory a repo | `scripts/scan.sh` |
| Start and stop a server around a check | `scripts/with-server.mjs --server "<cmd>" --port N -- <check>` |
| Design renders and metrics | `scripts/design-audit.mjs <url> [--bold]` |
| Layout, accessibility, SEO, weight and 404 checks on every page | `scripts/verify.mjs <url> [--max-pages 40]` |
| Every control's hover, focus and click; menus, forms, loading, 404 | `scripts/states.mjs <url> [--max-pages 40]` |
| Motion filmstrips, animation audit, smoothness, reduced motion | `scripts/motion.mjs <url> [--pages /,/about]` |
| Capture the old or new site; diagonal before/after PNGs | `scripts/beforeafter.mjs capture <url> --out <dir>`, `... compose --before <dir> --after <dir> --out <dir>` |
| Base44 app: public landing page, the app's own login, data safety | [base44.md](references/base44.md) |
| A sibling skill is missing | [fallbacks.md](references/fallbacks.md) |
