---
name: ui-part-social-proof
description: "Testimonials, customer logos, ratings, case studies and figures: only real, attributed and dated proof, what makes each kind credible, placing it beside the claim it supports, quote and logo layout and markup, phones without carousels, and the honest and legal limits. Read before adding any quote, logo row, rating or number meant to persuade."
---

# Testimonials, logos and numbers

The generated version: "Trusted by 10,000+ teams" over a scrolling strip of
famous logos, three five-star quotes from "Sarah K., Marketing Lead" with
stock headshots, and a counter that spins up to "99.9% uptime". All of it
invented, all of it seen a thousand times, and in many places unlawful.
Proof persuades because it can be checked: a named person, a real
customer, a number with its source and date. The principles are in the
`ui` skill, the measures in `ui-layout`, the words in `writing`.

## 1. Only what is real

- Use them for evidence that exists: a quote with the person's real name
  and permission, logos of real customers who agreed, figures with a
  source.
- Never invented testimonials, avatars, logo rows, ratings or counters, and
  no stock or generated faces beside real quotes. Fake reviews and
  testimonials are unlawful in many places (the US FTC's 2024 rule, EU
  consumer law).
- When the content is missing, leave the section out, or mark a
  placeholder: `[Customer quote]`, `[Name, role, company]`, `[Logo:
  customer]`, `[Figure, source, date]`, and list each in your report.
- Permission in writing for names, photographs and logos; quotes in the
  person's own words, shortened only with their approval; a paid or gifted
  endorsement says so.

## 2. What makes each kind credible

| Proof | Credible when |
|---|---|
| A quote | specific (the problem, the result, a number the customer gave), with a full name, role and company, and a link to the public source when there is one |
| Customer logos | real customers who agreed, under a heading that states the relation ("Clients include", not "Trusted by") |
| A number | its unit, source and date: "1,240 clinics use it, March 2026", and large enough to matter to a stranger |
| A rating | from a real platform, with the average, the count, the date and a link: "4.7 of 5 from 312 Google reviews" |
| A case study | the customer, the problem, what they did, the outcome in numbers over a stated period, a quote |
| Press, awards, certificates | real, with the year, linked to the article or the certificate |

- One figure, one source, the same everywhere on the site; updated or
  removed when it dates.
- Integrations and partners ("Works with") are not customers: do not dress
  them up as proof.
- For a person or a small studio, the work is the proof: a shipped project
  with its outcome beats any quote (`ui-part-sections`).

## 3. Placement and layout

- Beside the claim it supports: a quote about speed next to the speed
  feature, logos near the claim they back or the call to action. Not a
  detached "What our customers say" section by default.
- One strong quote beats six weak ones: set it large (20 to 25px, up to
  60ch, with room around it), the attribution under it; two or three side
  by side at most; never a grid of nine short ones.
- Attribution: the name at 16px weight 600, role and company at 14px in the
  muted colour; a 40 to 48px photograph only when it is real and
  permitted, with `alt=""` since the name is printed beside it
  (`ui-part-avatars`).
- Typographic quotation marks around the words, or none; not a giant
  decorative quote icon.
- Logos: four to eight, greyscale or one colour (SVG in `currentColor`, the
  muted text colour), at equal optical size rather than equal height (a
  wide wordmark lower, a square mark taller, each inside about 120 by
  40px), on one baseline, each with the company's name as its alt, linked
  only to a case study.
- Stars: a row of icons with a text alternative ("Rated 4.7 out of 5"),
  next to the source and its link; no stars without a source.

## 4. Markup

```html
<figure class="quote">
  <blockquote>
    <p>[Customer quote, in their own words, about one concrete result]</p>
  </blockquote>
  <figcaption>
    <span class="quote-name">[Name]</span>
    <span class="quote-role">[Role], [Company]</span>
  </figcaption>
</figure>

<section aria-labelledby="clients-title">
  <h2 id="clients-title">Clients include</h2>
  <ul class="logos" role="list">
    <li><img src="/logos/[customer].svg" alt="[Customer name]" width="120" height="40"></li>
  </ul>
</section>
```

```css
.logos {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: var(--space-6) var(--space-8);
}
.logos img { height: 32px; width: auto; } /* then adjust each by eye to an equal weight */
.quote blockquote p { font-size: var(--font-xl); max-width: 60ch; }
.quote-role { color: var(--text-muted); }
```

- `<cite>` marks the title of a work (an article, a review site), not the
  person's name.
- Review and rating structured data only for real reviews shown on the page;
  Google shows no review stars for reviews a business publishes about
  itself (`frontend-seo`).

## 5. Words

- Headings state the relation plainly: "Clinics using it", "What changed
  for [Customer]"; not "Loved by thousands" or "Don't just take our word
  for it".
- Numbers exact, or honestly rounded down, with their date; no "10k+",
  "99.9%" or "10x faster" without a source.
- An anonymous quote only at the customer's request, and then say so:
  "Name withheld at the customer's request".

## 6. Phones, themes and motion

- Phones: quotes stacked in one column; logos in a wrapping grid of two or
  three to a row. Not a carousel that autoplays: show two quotes and link
  to the case studies. A carousel that moves by itself needs a pause
  control (WCAG 2.2.2), and hides most of its content anyway.
- Themes: logos per theme, or single-colour SVGs in `currentColor`;
  `filter: invert(1)` only for single-colour marks; photographs never
  inverted (`ui-themes`).
- Motion: none by default. No endless logo marquee, no counters spinning
  up; a real number may count once, in under 800ms, with the final value
  in the markup (`motion-interface`, section 14).

## Check it

- Trace every quote, name, logo, rating and figure to a source you were
  given; list what is still a placeholder in your report.
- `ui_check`: `invented-figure` ("10,000+ customers", "99.9%", "10x
  faster"), `placeholder-content` ("John Doe", "Acme Inc"). Search the code
  for `testimonial`, `rating`, `stars`, `trusted` and `logos` (`ui-audit`).
- `preview`: "images without alt" catches unnamed logos; contrast of the
  role lines and greyscale logos in both themes; with `motion: true`,
  anything repeating forever (a marquee).

## Avoid

All of them when they are not real: leave the section out, or mark a
placeholder such as `[Customer quote]`. "Trusted by" over logos of
companies that never agreed; stock or generated headshots; "Sarah K.,
CEO"; five stars with no source; "10,000+" with no date; a marquee of
logos; autoplaying testimonial carousels; nine short quotes in a grid; a
giant quote icon; logos at equal height so the wide ones shout; a figure
that differs from page to page.
