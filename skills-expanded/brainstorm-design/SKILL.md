---
name: brainstorm-design
description: "DESIGN.md at the project's root, as the plan starts it: direction, concept, audience and theme from what the user decided, the inventory of pages or screens with their one job and main action, the key flows step by step, the states each screen must handle, content and placeholders, and what the frontend decides later. Read when planning anything with an interface."
---

# DESIGN.md: the look and the screens, before anyone builds them

`DESIGN.md` at the project's root is the file every interface agent reads
before a change and keeps to after it (`ui`). When the work is planned, the
orchestrator starts it from what the user decided, so the page agents
running side by side share one direction and one list of screens. The
frontend agents then fill in what is theirs: the palette values, the type
scale, the tokens.

The naive version either says nothing ("modern and clean") or decides for
the specialist ("a hero with three feature cards"). This one fixes what the
parts must agree on and leaves the composition to them.

## 1. The template

```markdown
# Design

Direction: <what it is and the feeling, in one line: "a booking page for a neighbourhood physio clinic, calm and plain">
Concept: <the idea the look comes from, when the user chose one: "the clinic's own appointment card">
Audience: <who, on what device: "adults booking a first visit, many on phones">
Theme: <light | dark | both, and why>
Look decided: <anything the user chose: colours, a brand, fonts, a reference site, "no photos">
Left to the frontend: palette values, type scale, spacing and radii tokens, icons, motion.

## Screens
| Screen | URL / route | Its job | Main action |
|---|---|---|---|
| Catalogue | /catalogue | Browse and filter products | Open a product |
| Product | /products/[slug] | Decide to buy | Add to cart |
| Cart | /cart | Review and change the order | Check out |

## Flows
1. Buy: Catalogue → Product → Add to cart → Cart → Checkout → Confirmation.
2. <other flows, each a line of steps>

## States
| Screen | Empty | Loading | Error | Other |
|---|---|---|---|---|
| Catalogue | No products in a category: say so, offer to clear the filter | Skeleton grid | "Couldn't load products", retry | Filter with no results |

## Content
- Language: <Indonesian>. Tone: <plain, friendly>.
- From the user: <what they gave>. Placeholders: <what is sample, and where it lives>.

## Navigation
- <Header links, footer links, what the logo goes to. Only links to screens that exist.>
```

## 2. Writing each part

- **Direction, concept, audience, theme** come from the brainstorm. When
  the user said "you decide", write what was decided and that it was
  yours ("Theme: light; decided here, the audience reads in daylight").
- **Look decided** records only the user's choices. Palette values and
  fonts the user did not choose are left to the frontend, which picks them
  with its `ui` skills and writes them back into this file.
- **Screens**: every page or screen the first version has, with a route,
  one job and one main action. A screen with two main actions is two
  screens or a decision to make. This table is how the plan splits
  interface work: usually one `fe` part per screen or group.
- **Flows**: the paths that cross screens, step by step. They tell the
  page agents where their page sends the user and what it receives.
- **States**: the empty, loading, error and edge states per screen, in
  words, with the copy when the user gave it. They go into the page's
  acceptance.
- **Navigation**: the real links only; a link to a page not in Screens is
  a planning error.

## 3. What it does not say

No layouts ("hero with stats and three cards"), no component lists, no
spacing values, no animation specs. Those are the frontend's and the
motion agent's, from their skills. The plan says what each screen is for;
they decide how it looks within the direction.

## 4. In an existing project

Read the existing `DESIGN.md` first. Add the new screens, flows and states
under their headings; never rewrite the direction because a new page is
being added. If there is no `DESIGN.md` but the site exists, write down the
look it already has (read the stylesheet and a page) before planning new
screens.

## Check it

- Every screen has a route, one job and one main action.
- Every flow's steps are screens in the table.
- Every screen lists its empty, loading and error states.
- Nothing in it was decided for the user without saying so; nothing
  prescribes a layout.

## Avoid

"Modern, clean, sleek"; layouts and sections decided for the page agents;
palette values the user never chose written as decisions; screens without
states; navigation to pages that do not exist.
