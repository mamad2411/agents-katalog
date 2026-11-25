# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

Static HTML landing page for **Mano en Mano**, a Mexican secondhand clothing marketplace app (pre-launch). No build system — open `index.html` directly in a browser to develop.

Deployed on GitHub Pages (see `CNAME`).

## Running locally

```bash
# Any static file server works; simplest option:
python3 -m http.server 8080
# then open http://localhost:8080
```

## Architecture

Single-page site: one `index.html`, one `css/style.css`, one `js/main.js`. All third-party libraries are vendored locally (`css/` and `js/`):

| Library | Purpose |
|---|---|
| Bootstrap | Grid and responsive layout |
| jQuery | DOM utilities, smooth scroll |
| Owl Carousel | (currently unused in production — carousel divs are commented out) |
| WOW.js + Animate.css | Scroll-triggered entrance animations (`wow animated fadeIn*` classes) |
| Font Awesome | Icons (loaded from CDN in `<head>`) |
| Google Fonts | Playfair Display (headings) + DM Sans (body), loaded from CDN |

**External dependency**: Typeform beta-signup form embedded via `<script src="https://embed.typeform.com/next/embed.js">` and a `data-tf-live` attribute on the form div. Requires internet to function.

## Color palette & typography

All brand colors are defined as CSS variables at the top of `css/style.css`:

```css
--color-olive: #64723A      /* primary green */
--color-mustard: #F2C330    /* accent yellow */
--color-plum: #6D4A6B       /* secondary purple, used for backgrounds */
--color-blush: #F0B9D2      /* light pink accent */
```

Headings use `"Playfair Display"` serif; body text uses `"DM Sans"` sans-serif.

## Page sections (top to bottom)

Navigation links use jQuery smooth-scroll via `$.fn.goTo()` defined in `js/main.js`. All `<a>` nav items use `onclick="$('#section-id').goTo();return false;"` — there is no router.

| Section ID | Content |
|---|---|
| `#fh5co-hero-wrapper` | Hero + navbar |
| `.custom-container` (first) | Problem statement cards |
| `.fh5co-advantages-outer` | Environmental statistics |
| `#fh5co-features` | How the app works (seller flow) |
| `.custom-container` (subsequent) | Buyer flow, agreement flow, advantages grid |
| `#fh5co-subscribe` | Typeform beta waitlist |
| `#fh5co-team` | Team member cards |

Many sections exist in the HTML as commented-out blocks from the original template — these are safe to ignore or remove.
