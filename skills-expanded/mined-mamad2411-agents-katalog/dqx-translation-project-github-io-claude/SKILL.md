# dqx-translation-project.github.io

documentation site for the DQX Translation Project — tools that let players experience Dragon Quest X Online in English.

## what this site is

a pure static HTML site. no build tool, no framework, no markdown preprocessor. every page is a hand-written `.html` file with shared CSS and JS.

deployed via GitHub Actions: on push to `main`, the CI deploys the `site/` directory to the `gh-pages` branch using `peaceiris/actions-gh-pages`.

live at: https://dqx-translation-project.github.io

## file structure

```
site/
  index.html           main landing page
  dqxclarity.html      install guide for dqxclarity
  troubleshooting.html common issues + fixes
  faq.html             frequently asked questions
  apis/
    deepl.html         DeepL API setup guide
    google.html        Google Translate API setup guide
  css/
    style.css          all styles (single shared stylesheet)
  js/
    main.js            sticky nav, mobile menu, accordion, scroll reveal, lightbox

.github/
  workflows/
    ci.yml             deploy workflow
```

## how to edit

- **content**: edit the relevant `.html` file directly. all pages share the same nav and footer structure.
- **styles**: everything is in `site/css/style.css`. uses CSS custom properties (`--cap`, `--ink`, etc.) defined in `:root`.
- **images**: screenshots live in `site/assets/`. reference them in HTML as `assets/...` (root pages) or `../assets/...` (pages in `apis/`).
- **new pages**: copy the structure of an existing page, add a nav link in all other pages.

## components

- **`.eyebrow`** - small pill label (used in hero section)
- **`.section-label`** - large teal display-font header for sections (Features, Get started)
- **`.card` / `.card-grid`** - feature cards with hover lift
- **`.link-card`** - navigation cards in the "get started" section
- **`.callout--warning/info/success/note`** - admonition boxes
- **`.accordion-item` + `.accordion-trigger` + `.accordion-body`** - collapsible Q&A (FAQ and Troubleshooting pages)
- **`.api-chip`** - pill tags for listing API options
- **`.jump-nav`** - pill anchor links at the top of long pages
- **`.reveal`** - add to any element to get a fade-in on scroll

## fonts

loaded from Google Fonts:
- **Baloo 2** (weights 500-800) - display/headings, nav, buttons, labels
- **Nunito** (weights 400-800) - body text

## writing rules

- never use em-dashes (—). use hyphens (-) instead.
- keep wording concise and direct.
