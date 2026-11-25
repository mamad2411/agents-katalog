---
name: ui-part-faq
description: "An FAQ: where real questions come from and where they belong, writing the question and its answer, the disclosure markup and headings, several open at once, deep links, search for long lists, structured data, and the contact route. Read before adding questions and answers to a page."
---

# FAQ

The generated version: "Is my data secure?", "How does it work?" and "Can
I cancel any time?", answered in phrases that fit any product, eight of
them in an accordion that closes one as another opens, above the footer
of every page. An FAQ earns its space only when it answers questions real
people ask, briefly and specifically. One part of an interface: the
principles (direction, spacing, type, colour, icons, states,
accessibility) are in the `ui` skill, the measures in `ui-layout`.

## 1. Where the questions come from

- Questions real users ask: support tickets and chats, sales calls,
  reviews, the site's search log, the brief. Ask the user for them when
  you have none.
- Template questions that fit any product ("Is my data secure?") are out,
  unless the answer is specific: where the data is stored, who can read
  it, how long it is kept.
- No known questions means no FAQ. For a new product, answer the likely
  doubt where it arises instead: billing beside the prices, delivery
  beside the button that buys.
- A fact you were not given (a refund window, parking, insurance) stays a
  visible placeholder in the answer ("[Cancellation policy]") and goes in
  your report; never a plausible guess.

## 2. Where it goes

- Near the decision it supports: billing questions under the pricing
  (`ui-part-pricing`), delivery and returns on the product page, booking
  questions on the booking page.
- A help page of its own past about 15 questions, grouped, with search,
  linking into the documentation (`ui-page-docs`).
- Not the same generic block above the footer on every page.

## 3. Writing each one

- The question in the user's words, as they would ask it: "Can I change my
  plan later?", not "Plan flexibility".
- The answer starts with the answer (yes, no, the number, the date), then
  the detail: a few sentences, 40 to 80 words, with a link onward to the
  full page.
- Specific and checkable: "Refunds within 14 days of purchase" only when
  that is the policy. No selling in the answers.
- One question per item, in the product's own terms (`writing`).
- Grouped by topic (Billing, Delivery, Accounts) when there are more than
  about 8, each group under its own heading.

## 4. Markup and keyboard

- `<details>` and `<summary>` by default: the keyboard, the open state and
  find in page come with them (Chromium opens a closed `details` when find
  in page matches inside it). Or an accordion: a `button` with
  `aria-expanded`.
- Screen reader users move by headings: put each group's heading (`h2` or
  `h3`) above its questions. A heading inside `summary` is not announced
  as a heading by every screen reader; when each question must be a
  heading, use the APG accordion: an `h3` holding a `button` with
  `aria-expanded` and `aria-controls`, the answer in the element after it
  (`hidden="until-found"` keeps a closed answer findable where supported).
- Enter and Space open and close; each question is one Tab stop.
- Several may be open at once: no `name` attribute on the `details` (it
  makes them exclusive) and no script closing the others.
- "Expand all" and "Collapse all" on a long page, opening everything at
  once.
- Each question has an `id` so support can link to it (`/help#refunds`); a
  few lines of script open the one the URL names, and `scroll-margin-top`
  keeps it clear of the sticky header.

## 5. Anatomy and measures

- The question 16 to 18px, weight 600; the row at least 48px tall, all of
  it clickable, a hairline between items.
- The open state visible: a chevron turning 180 degrees, or a plus
  becoming a minus, 16 to 20px, at the row's end, `flex: none`, in
  `currentColor`.
- The answer in the text colour (not faded), at body size, at most 65
  characters a line, with 16 to 24px under it.
- The default marker hidden and replaced: `list-style: none` on `summary`,
  and `summary::-webkit-details-marker { display: none; }` for Safari.

## 6. Search for long lists

- Past about 20 questions, a labelled search field above the groups that
  filters as the user types, opens the matches, and says how many match
  ("4 questions match refund", in a `role="status"` region).
- No match: say so, and give the contact route right there
  (`ui-part-search`).

## 7. Structured data

- `FAQPage` JSON-LD only when every question and answer in it is visible
  on the page, word for word.
- Since August 2023 Google shows FAQ rich results only for well-known
  government and health sites; add the markup when it is accurate, not in
  the hope of a richer search listing.

## 8. The contact route

- At the end: where to ask what is not answered, with the real channel
  and the real reply time ("Email [support address]; we reply within
  [time]"). A form or a chat only when one exists.

## 9. Phones, themes, motion

- Full width on a phone; the question wraps, the icon keeps its size; the
  whole row is the 44px target (`preview` measures `summary` elements).
- Themes: hairlines and the icon from tokens, in both themes (`ui-themes`).
- Motion: the answer opens to its height in 240ms (the grid-rows trick, or
  `::details-content` with `interpolate-size`), the chevron turns in the
  same time, and both are instant under reduced motion
  (`motion-interface` 8).

## 10. A sketch

```html
<section aria-labelledby="billing-faq">
  <h2 id="billing-faq">Questions about billing</h2>
  <div class="faq">
    <details id="change-plan">
      <summary>Can I change my plan later?</summary>
      <div class="faq__answer">
        <p>[The answer, from the billing policy.] <a href="/docs/billing">How billing works</a></p>
      </div>
    </details>
  </div>
  <p>Not answered here? <a href="/contact">Ask us directly</a>.</p>
</section>
```

```css
.faq details { border-block-end: 1px solid var(--border); }
.faq summary {
  display: flex; align-items: center; justify-content: space-between; gap: 16px;
  min-block-size: 48px; padding-block: 12px;
  font-weight: 600; cursor: pointer; list-style: none;
}
.faq summary::-webkit-details-marker { display: none; }
.faq summary::after {
  content: ""; flex: none; inline-size: 16px; block-size: 16px; background: currentColor;
  mask: url(/icons/chevron-down.svg) center / contain no-repeat;
}
.faq details[open] > summary::after { rotate: 180deg; }
.faq summary:focus-visible { outline: 2px solid var(--focus); outline-offset: 2px; }
.faq__answer { max-inline-size: 65ch; padding-block-end: 16px; }
```

```js
// Open the question the URL names: /help#change-plan
const id = decodeURIComponent(location.hash.slice(1));
const target = id && document.getElementById(id);
if (target instanceof HTMLDetailsElement) target.open = true;
```

## Check it

- Trace each question to where it was asked, and each answer to a fact you
  were given; placeholders are visible and listed in the report.
- Keyboard only: Tab through the questions; Enter opens and closes; several
  stay open.
- Open `/page#question-id`: that answer is open, below the sticky header.
- Find in page (Ctrl or Cmd+F) a word from a closed answer: in Chromium it
  opens.
- `preview` at 360px: no `summary` in "touch targets under 44px", answers
  at 4.5:1 in both themes; `ui_check` for buzzwords in the answers.
- If there is `FAQPage` markup, every item in it is on the page.

## Avoid

Template questions that fit any product ("Is my data secure?"); invented
policies; answers that sell; an accordion that closes one as another
opens; forty questions with no groups or headings; answers faded to a grey
that fails contrast; the same FAQ above every footer; `FAQPage` markup for
questions that are not on the page; no way to ask what is not answered.
