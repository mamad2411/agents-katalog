---
name: brief2motion
description: Turn a plain brief into a website with professional motion, measured in a real browser. Use to build or animate a website, landing page, portfolio, scroll or data story, or a whole site or page that must convert (site mode: discovery, content, routes, wireframes, tokens, design, then layout, accessibility, journey and meta checks); to add a hero or scroll animation, scrollytelling, parallax, page transitions, kinetic type, micro-interactions, a 3D product viewer, particles or dust that form a logo, face or words, SVG, Lottie or Rive; to pick a style such as neubrutalism, glassmorphism, neumorphism, claymorphism, bento, Swiss or minimal; or to "make my site feel alive". Picks the stack (CSS and JavaScript, GSAP with ScrollTrigger and Lenis, Motion, three.js or React Three Fiber, SVG, Lottie, Rive) and the style with reasons, builds and serves the page, checks frame rate, phone layout, reduced motion, focus, contrast and no-WebGL and no-JS fallbacks, fixes what fails, and can hand it to brief2mp4 for video.
---

# brief2motion 1.1.0

A brief goes in. A working site comes out in `site/`, with `REPORT.md` proving every line of the brief with a measured number or a named screenshot, and an `http://localhost` address the user can open.

Work in this order every time: **route, spec, build, check, fix, deliver.** A page that looks right on your screen is not a page that works on a phone, with a keyboard, or for someone who has motion switched off.

## 0. Before you start

Run the doctor once per machine:

```bash
bash <this skill's folder>/scripts/doctor.sh
```

Required: Node.js 22+ and a Chrome or Chromium the checker can start (Google Chrome, `chromium` on PATH, Playwright's Chromium, or a path in `BRIEF2MOTION_CHROME`). If something required is missing, give the user the command the doctor printed and stop. The first check downloads `playwright-core` 1.65.1 (about 14 MB, install scripts off) into `~/.cache/brief2motion/deps`. Python 3 is optional (the preview server has a Node twin). ffmpeg and the brief2mp4 skill are only for a video.

Work inside one project folder. Never write outside it.

## 1. Route: pick the stack and the style from the brief

Save the brief as `BRIEF.md`, word for word, then:

```bash
node <this skill's folder>/scripts/route.mjs BRIEF.md
```

It prints a stack, a style, the phrases in the brief that led there, and the reference files to read. It is a keyword scorer and has never seen the product, so treat it as a first proposal: read the brief again, agree or overrule, and write the choice and the reason in `SPEC.md`. Anything the brief states outright overrides the router: a library, a style or colours it names are used as given.

It also prints **patterns**: recipe pages in `references/patterns/` that match the motion words in the brief (a hero sequence, a marquee, a pinned scene, a magnetic button, a page transition, a 3D product that turns as you scroll, and 21 more; the index is `references/patterns/README.md`). Each pattern says when to use it and when not to, the stack, a minimal sketch written for the kit, its performance and accessibility budget, its reduced-motion form and how the checkers verify it. `references/web-references.md` is the verified library of galleries, component libraries, platform docs and canonical demos to study before you build (study, never copy), and `references/motion-doctrine.md` holds the timing and easing rules every motion plan follows. A pattern is a starting sketch, not a template and not a tested page (the tests only check that its script parses and its kit imports exist): rewrite it for the brief's words, then the checkers test the page you built.

The stacks, and when each is right:

| The brief wants | Stack | Read | Study |
|---|---|---|---|
| nothing that needs a library: reveals, hovers, a simple scroll effect | plain CSS and JavaScript with the kit (**the default**) | `references/stacks/vanilla.md` | `examples/sprout/` |
| dust, dots or particles that form a product, logo, face or word | the dust engine (config only) | `references/stacks/particles.md` | `examples/copper-no-7/` |
| a story told by scrolling: pinned scenes, scrubbing, a sideways gallery, a picture sequence | GSAP, ScrollTrigger, Lenis | `references/stacks/gsap.md`, `scroll-story.md` | `examples/tidewater/` |
| headlines that move, springs, a type-led landing page | Motion (vanilla) | `references/stacks/motion.md`, `kinetic-type.md` | `examples/relay/` |
| interface motion in a React or Next.js app: layout changes, drag, lists, presence | Motion for React | `references/stacks/motion.md` | `examples/mise/` |
| a real 3D object: a product to turn, an exploded view, a shader | three.js (React Three Fiber in a React project) | `references/stacks/three.md` | `examples/halden-one/` |
| moving between pages, or a grid that rearranges | View Transitions API | `references/stacks/view-transitions.md` | `examples/halvorsen/` |
| lines, icons and charts that draw; data told step by step | SVG with the kit (D3 for scales) | `references/stacks/svg-players.md`, `scroll-story.md` | `examples/keeling/` |
| an animation file from a designer (Lottie, Rive) | the players in the kit | `references/stacks/svg-players.md` | `examples/sprout/` |
| heavy per-frame computation | read the note first | `references/stacks/wasm.md` | |

Use the lightest stack that does the job, and one stack per page where you can. Two are fine when the brief needs both (GSAP for the scroll, three.js for the object). A React stack needs the project's own bundler: never ship React Three Fiber or a real React app from CDN modules.

The style: `references/styles.md` indexes 32 visual styles and approaches (neubrutalism, glassmorphism, Liquid Glass-inspired, neumorphism, claymorphism, skeuomorphism, flat, Material, Swiss, minimalism, maximalism, bento, editorial, Y2K, Frutiger Aero, vaporwave, synthwave, Memphis, Art Deco, cyberpunk, glitch, aurora, grain, duotone, dark-first, isometric and more). Each has its own page with tokens, tested CSS, the motion that fits, accessibility traps and sources. Open only the page for the style you chose. A style is a starting point: a brand's own colours and type replace its tokens. If the brief asks for a style that is not on the list, check the "names that are not styles" section before inventing one.

Always read, whatever the stack: `references/design-fundamentals.md` (hierarchy, type, space, colour, landing structure, motion principles), `references/motion-doctrine.md` (smooth over bouncy, vary eases and durations, build and breathe and resolve, enter slower than exit, transitions that mean something, the one SVG-draw rule), `references/accessibility.md` and `references/performance.md`.

## 2. Spec: write SPEC.md before any code

Copy `templates/SPEC.md` and fill it in:

1. **Stack and style**, with one sentence each on why, from step 1.
2. **Design plan**: a small palette (each colour named, each text pair's contrast checked), which typeface does which job, the layout in one line, and the single element a visitor should remember. Then test each part against the brief: if it would fit a different product just as well, it is a default, so replace it with something this subject suggests.
3. **Motion plan**: three lists. On load, on scroll, on input. Each item says what moves and why, which pattern page it comes from if any, and what it does with reduced motion. If you cannot say why, cut it. Put the effort into one planned entrance; the same fade repeated on every block is noise.
4. **Copy**: every word on the page, exactly as the brief gives it. If the brief gives none, write plain copy from what it says and mark it as drafted. Never invent reviews, ratings, customer names, logos or numbers. Made-up examples say that they are made up.
5. **Done when**: one checkable line per requirement, each naming the number or screenshot that will prove it.

If the brief leaves a choice open, make it, write it under **Decisions**, and continue.

## 3. Build

Start from the closest thing that already passes the checks:

- **Dust and particles**: copy `templates/site/` to `site/` and edit only `config.js`, the title and description in `index.html`, and colours in `style.css`. `references/stacks/particles.md` and `references/brief-words.md` map phrases to settings. Do not edit the engine files.
- **Everything else**: read the example for your stack, then build `site/` with its structure: `index.html`, `style.css`, one script, and a copy of the `kit/` folder. Take the pattern, never the example's words, pictures or look. Hand-installed without the repo? The examples are at `https://github.com/qualixar/brief2motion/tree/main/examples`.

What every page has, whatever the stack (the checker tests each one):

- Real content in the HTML: one `<h1>`, a `<title>`, a description, `lang`, a skip link, `<main>`, `alt` on images. The page reads with JavaScript off.
- `kit/kit.css` loaded first: focus ring, reduced-motion rule, `.sr-only`.
- The motion state reported once setup is done: `signal('ready')`, `signal('reduced')` or `signal('static')` from `kit/motion-core.js`.
- A reduced-motion branch that shows the finished state: no travel, no loops, no parallax.
- A still picture for every WebGL canvas (`<canvas data-webgl>` with `<img data-fallback>`), shown when WebGL is missing, a library fails to load, or a runtime error is caught.
- Libraries from `cdn.jsdelivr.net` only, at pinned versions, loaded after the text is on screen. System font stacks unless the brief supplies a font.
- A motion plan as a comment at the top of the script, matching SPEC.md.
- Nothing wider than a 320 px screen, and tap targets of at least 24 px.

Tuning by hand (optional, dev only): `kit/tune.js` opens a Tweakpane panel for easing, duration, stagger and colour when the address ends in `?tune`, and "Copy values" gives the numbers back as JSON to paste into the code. Wrap the loader line between `/* tune:start */` and `/* tune:end */`. It is never part of the shipped page: before step 4 run `node <this skill's folder>/scripts/strip_tune.mjs site`, which removes `kit/tune.js` and every marked block, and `check_site.mjs` fails a page that still has either. Examples do not carry `tune.js`; copy it from `kit/` when you want it.

Images: only ones the user owns or that carry a licence allowing reuse. Put the credit in `site/CREDITS.md` and in REPORT.md. Prefer drawing in code (SVG, canvas, three.js primitives) to borrowing. Size pictures for the 1.5 MiB budget.

## 4. Check (do not skip)

```bash
node <this skill's folder>/scripts/check_site.mjs site --out check
```

For a site with several pages add `--pages about.html,work/a.html`. For the dust engine also run `check_motion.mjs site --out check --make-fallback`, then `check_motion.mjs site --out check`.

| Check | Budget |
|---|---|
| Desktop 1440 x 900, p95 frame time, idle and scrolling | 20 ms or less |
| Emulated phone, 390 x 844, touch, CPU slowed 4x, p95 frame time | 40 ms or less |
| Sideways scroll at 1440, 390 and 320 px | none |
| Tap targets on the phone | 24 px or more |
| Reduced motion | the page says so; nothing animates; the picture holds still; all text visible; scrolling works |
| WebGL off | headline readable; a still stands in for each WebGL canvas |
| JavaScript off | the page still reads |
| Text contrast | WCAG AA: 4.5:1, or 3:1 for large text |
| Keyboard | every stop has a visible focus ring and is on screen |
| Basics | one `<h1>`, `lang`, real title and description, zoom allowed, `alt` text, `<main>` and a skip link |
| Page weight from the project, per page | 1.5 MiB or less |
| Third-party requests | `cdn.jsdelivr.net` only |
| Dev tuning panel | not in the shipped page: no `kit/tune.js`, no tune block, no Tweakpane request |
| Console errors, every run | 0 |

The frame numbers only mean something on a machine with a real GPU; elsewhere pass `--no-perf`. Then open the screenshots in `check/shots/` and look at them against every **Done when** line and against the design plan. A checker cannot see that a layout is dull, that text sits on a busy picture, or that the hero says nothing. Text over pictures, gradients and canvas is not measured for contrast: look at it.

## 5. Fix

Fix the page, not the budget, and check again. Slow frames: `references/performance.md`. Reduced-motion or fallback failures: `references/accessibility.md`. Layout: find what is wider than the screen (the checker names it). Stop after three rounds on the same failure and say what is still failing in REPORT.md.

## 6. Deliver

**Preview first.** Browsers refuse to load ES modules from `file://`, so opening `site/index.html` from the file shows a blank page. Start the preview server in the background and give the user the address it prints:

```bash
python3 <this skill's folder>/scripts/serve.py site        # or: node <this skill's folder>/scripts/serve.mjs site
# prints  Open  http://localhost:8421/
```

Say that Ctrl-C stops it. Never tell the user to open the file directly. For a real site, upload `site/` to any static host.

`REPORT.md` in the project root: the brief; the stack and style with the reason; every **Done when** line with its proof; the check table; credits and the licence notice (`references/licences.md` has the template); what you decided; what you could not verify.

Pictures or a video of the page:

```bash
node <this skill's folder>/scripts/capture_site.mjs site --out media                    # screenshots and a frame sheet of a scroll-through
bash <this skill's folder>/scripts/to_video.sh site final.mp4 --seconds 12              # the dust engine's frame-exact capture
```

## Site mode: a whole site, or a page that must convert

Use it when the brief asks for a site with several pages, or for one page whose job is to get a visitor to do something (sign up, buy, book, register). It puts the work a studio does first in front of steps 1 to 6: design before motion. Every stage writes one short file that a person and an agent can both read; `templates/site-mode/` holds a filled-in copy of each (README there has the commands), and `examples/larkspur/` is a SaaS site built through all of it.

| Stage | File | Checked by |
|---|---|---|
| 1. Discovery: visitors, their tasks, the owner's goal and how it is observed, constraints, open questions with the assumption taken | `DISCOVERY.md` | `check_plan.mjs` |
| 2. Content: every word per route; each claim has an ID and a source, or is marked DRAFTED | `CONTENT.md` | `check_plan.mjs` |
| 3. Routes: id, path, parent, template, title, description, primary action, states, links | `routes.json`, `SITEMAP.md` (`build_sitemap.mjs`) | `check_plan.mjs`, `check_meta.mjs` |
| 4. Wireframes: phone-first grey boxes with real copy and a reachable primary action | `wireframes/<template>.html` (`index.html` when there is one template) | `check_layout.mjs --wireframes` (a missing file FAILs) |
| 5. Tokens: primitives, light and dark roles, text pairs | `tokens.json` -> `site/tokens.css` (`build_tokens.mjs`) | the same script: references, cycles, AA contrast for every text pair declared in `tokens.json` (only declared pairs are measured, so declare every pair the design uses) |
| 6. Visual design: one idea from the subject, type, grid, colour, imagery, a single signature element; then the router and `SPEC.md` as before | `DESIGN.md`, `ASSETS.json` | `check_plan.mjs` (rights records) |
| 7. Motion: per movement its intent, trigger, states, interruption, reduced form, pattern page | `MOTION.md` | `check_site.mjs` |
| 8. Build: semantic HTML first, motion on top, with steps 3 to 5 above | `site/` | everything |
| 9. Checks and a second reader | `journeys.json`, `check/qa.json`, `REVIEW.md` | `check_layout`, `check_a11y`, `check_journeys`, `check_meta`, `check_site` |

Rules: the brief's own facts are the only facts (no invented reviews, logos, customers or numbers: `check_plan` fails a drafted claim that looks like proof and sends a drafted figure to review); phone first; states (empty, loading, error, success) are declared in `routes.json` and each one is loaded by the checkers. Read `references/page-blueprints.md` for the page type, `references/design-review.md` for the second reader, and sections 10 to 15 of `design-fundamentals.md` for the numbers.

The commands, from the project root (`S` is this skill's `scripts` folder; `templates/site-mode/README.md` says what each one reads):

```bash
node $S/build_sitemap.mjs . && node $S/build_tokens.mjs tokens.json --qa check
node $S/check_plan.mjs .                  # stages 1 to 4; after the build also links and the dev panel
node $S/check_layout.mjs . --wireframes   # stage 4
node $S/check_layout.mjs . --themes light,dark && node $S/check_a11y.mjs . --themes light,dark
node $S/check_journeys.mjs . && node $S/check_meta.mjs .
node $S/check_site.mjs site --out check   # motion, fallbacks, weight: site mode does not replace it
```

Every checker writes records into `check/qa.json`: `PASS` (measured, within threshold), `FAIL` (blocks), `REVIEW` (a person must look) or `PENDING` (no evidence yet: a site not built, a sign-up that ends at a fixture, axe-core offline). Each run ends with `RESULT: PASS`, `FAIL` or `INCOMPLETE`. INCOMPLETE means nothing failed but some checks are PENDING, so it is not a pass: say so, and do not report that stage as checked. Exit 1 means a FAIL (or nothing was checked); exit 0 covers both PASS and INCOMPLETE, so read the RESULT line, or run with `--strict`, which also exits 1 on PENDING and REVIEW. qa.json carries the same `verdict`, `complete: false` while anything is PENDING, and marks records measured on an older build of `site/` as stale. `check_a11y.mjs` fetches axe-core 4.14.1 (MPL-2.0) from cdn.jsdelivr.net when it runs, verifies its hash and injects it into the checker's own page; the site never carries it. A green report does not replace the second reader or a screen-reader pass.

Compress for a small brief: a one-page site keeps one short entry in each file and may skip stages 4 and 7 when the page has no template choice and no motion; a site with several page types writes one entry per route or template. Never skip 1 to 3 and 9: without them nothing says what the page is for or whether it worked.

## Licences in one paragraph

This skill's code is MIT. Sites it builds load libraries from a CDN at pinned versions and bundle none of them: three.js, Lenis, Motion, React, lottie-web, the Rive runtime and htm are MIT or Apache-2.0; D3 is ISC; Tweakpane (the dev-only `?tune` panel, never shipped) is MIT; axe-core (fetched by `check_a11y.mjs` at check time, never part of a page) is MPL-2.0; GSAP 3.15.1 is free under GSAP's own "no charge" licence, which allows commercial use and AI-written GSAP code but not use inside no-code animation builders that compete with Webflow. Pages use system fonts and send no request to a font service. `references/licences.md` has the detail and the notice to write into each project.
