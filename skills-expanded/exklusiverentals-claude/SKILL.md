# Exklusive Rentals — working notes

A hand-written static site. No framework, no build step: pushing to `main`
publishes it through GitHub Pages. `css/tokens.css` holds every colour, font,
spacing and motion value; `css/site.css` reads only from those tokens. Keep that
split — a change that hard-codes a colour in `site.css` is a regression.

## Where this stands

This is the starter. It carries the tooling and a holding page, and nothing
about the business beyond its name. The palette and type in `tokens.css` are
neutral placeholders. Before any design work:

- Get the facts from the owner: what is rented, to whom, where, how a booking
  or enquiry happens, contact details, and any brand material (logo, colours,
  photos). Do not invent services, prices, testimonials or claims.
- Run the design pass, then record the direction in a `DESIGN.md` at the root
  so the design skills can read it. There is none yet on purpose.
- Add pages to the `PAGES` lists in `tests/` as they are created, and put the
  measured performance numbers into `tests/vitals.spec.js` once real pages
  exist.

## Verify in a browser, not by eye

`npm test` runs Playwright against the real pages: smoke checks, a performance
budget, a no-horizontal-overflow sweep from 320px to 1920px, pixel-measured
WCAG AA contrast, and an 11px floor on functional text. Run it after any change
to markup, CSS or `js/main.js`.

    npm install        # once
    npm test
    npm run test:report

## Things that are easy to get wrong

- Pages use root-relative paths (`/css/...`), so preview with a server
  (`npm run serve`), never by opening the file directly.
- `.site-footer` paints the dark background, so any text style added to the
  footer needs its on-dark colour set explicitly; `tests/contrast.spec.js`
  measures the result and will fail if it is missed.
- Hover styles live behind `(hover: hover) and (pointer: fine)`, every control
  has an `:active` state, and inputs stay at 16px or more so phones do not zoom.
