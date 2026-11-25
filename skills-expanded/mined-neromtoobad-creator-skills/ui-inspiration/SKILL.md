---
name: ui-inspiration
description: Find real design references before styling any UI — landing pages, app screens, portfolios, hackathon frontends, navbars, footers, 404s, dark mode, motion/scroll effects. Uses the 30 curated galleries listed on mkdir.directory, grouped by what each is good for, then pulls concrete tokens and patterns from the best live examples. Use whenever the user asks for UI inspiration, a redesign, "make it look better/premium/less basic", a new frontend, or before the first styling pass on any page, even if they don't mention inspiration.
---

# UI inspiration (via mkdir.directory)

Source: https://mkdir.directory/ — a curated index of 30 design-inspiration directories. Re-check it occasionally; the list grows.

## Pick galleries by job

| Need | Go to |
|---|---|
| Award-tier, experimental, "wow" sites | Awwwards `awwwards.com`, The FWA `thefwa.com`, CSS Design Awards `cssdesignawards.com`, Okay Dev `okaydev.co/gallery` |
| Broad curated web galleries | SiteInspire `siteinspire.com`, Inspora `inspora.design`, Recent `recent.design`, A1 Gallery `a1.gallery`, Maxibestof `maxibestof.one`, Klikkenthéke `klikkentheke.com`, Best Designs on X `bestdesignsonx.com`, Save.design `save.design/explore` |
| SaaS / product landing pages | Saaspo `saaspo.com`, SaaS Landing Page `saaslandingpage.com`, Land-book `land-book.com`, One Page Love `onepagelove.com` |
| Minimal / restrained | Minimal Gallery `minimal.gallery` |
| Brutalist / raw | BrutalWeb `brutalweb.com`, Brutalist Websites `brutalistwebsites.com` |
| Dark themes | Dark Mode Design `darkmodedesign.com` |
| Single components & sections | Navbar Gallery `navbar.gallery`, Footer.design `footer.design`, 404s `404s.design`, Unsection `unsection.com`, Collect UI `collectui.com` |
| Motion, scroll, micro-interactions | GSAP Showcase `gsap.com/showcase`, Lenis Showcase `lenis.dev/showcase`, Codrops Creative Hub `tympanus.net/codrops/hub`, Movin `movin.design`, Daily Delights `delights.design` |

For demo/promo **videos**, use prompt-motion.com instead (see the ui-motion-reel skill / demo-video memory).

## Workflow

1. **Frame the brief**: product type, audience, mood (playful game / premium fintech / minimal tool / sponsor-matched), light or dark. Default light unless the brief or sponsor says otherwise.
2. **Pick 2–3 galleries** from the table that match the brief, plus one component gallery if a specific section (nav, footer, pricing, empty state) matters.
3. **Browse with the built-in browser** (`mcp__Claude_Browser__*`). Filter by category/tag where the gallery allows. Shortlist 4–6 live sites, not screenshots.
4. **Extract real tokens** from each shortlisted live site with `javascript_tool`: computed `font-family`/weights/letter-spacing of h1, body and labels; background, surface, text and accent colours; border radii; button shape and padding; shadow style; section spacing; nav shape. Note any signature motion (scroll-linked, hover, page transitions).
5. **Write a short direction note** (in the project folder): what's shared across the references (principles), the token set you'll use, and the product's *own* metaphor/identity.
6. For high-stakes visual work (portfolio, hero, full redesign), **render 2–3 direction mockups** and let the user pick before building.

## Rules

- Borrow principles and structure (hierarchy, restraint, spacing rhythm, type scale), never a site's signature pieces (logo, exact font pairing + palette + layout combo, distinctive nav). Each product gets its own metaphor.
- Never imitate a real brand's identity.
- Link the references you used in the direction note so the user can see them.
- Galleries add `?ref=` tracking from mkdir; strip it when citing.
