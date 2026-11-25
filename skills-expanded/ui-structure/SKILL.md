---
name: ui-structure
description: "Structure before styling: the blueprint written before any interface code (the screen's job, the regions its kind of page needs, their order and why, the layout skeleton in numbers, the components and their states), the anatomy and order of a homepage, a dashboard, a list, a detail page, settings, a form, sign-in, pricing, docs, an article and a checkout, and how to turn the blueprint into code (tokens, layout primitives, components, sections, page). Read first, before building or rebuilding any page or screen."
---

# Structure before styling

A page built from impressions looks like this: a header whose text touches
the window's edge, a strip of figures with no container, a chart in a card
beside a form in another card, a summary floating between them with no
surface at all, a table that bleeds to both edges, three left edges on one
page, controls with no visible state, and a phone width where half of it is
cut off. Every part was made; nothing was decided. Good interfaces are
decided in order: what the screen is for, what it must hold, in what order,
on what grid, from which components, and only then how it looks.

This skill is that order. `ui` sets the look, `ui-layout` and
`ui-layout-grid` go deeper on space, `ui-anatomy` holds each component's
contract, and the `ui-page-*` and `ui-part-*` skills go deeper on one page
or part.

## 1. Write the blueprint first

Before the first file, write the blueprint in your message (and keep the
layout numbers in DESIGN.md so the next change uses them). Short, concrete,
no adjectives:

```
SCREEN    Trading workspace (app screen, signed in, desktop first)
JOB       See one market's price and act on it; know my positions.
PRIMARY   Place an order. One primary button on the screen: "Buy BTC".
REGIONS   (in order, with why)
  1 App header: product, market switcher, theme (icon), account
  2 Page header: instrument, price, 24h change, last update   - what am I looking at
  3 Main: chart (2/3) + order ticket (1/3, sticky)             - see, then act, side by side
  4 Positions summary: 4 KPIs                                  - result of acting
  5 Tabs: Holdings | Orders | History (table)                  - detail, last
SKELETON  container max 1440, gutters 16/24/32, 12 columns gap 24,
          section gap 32 (app), card padding 20, header 56 sticky
          <1024: ticket moves under the chart; <768: KPIs 2x2, table -> rows
COMPONENTS button (primary, secondary, ghost; 32/40), segmented (range,
          buy/sell), tabs, stat, field (number with unit), table, badge,
          icon button (theme), empty state for no orders
STATES    loading (skeleton per region), empty (no holdings), error (quote failed),
          disabled buy until quantity is valid
```

If you cannot fill a line, you are not ready to write code for it. If a
region has no "why", it does not go on the page.

## 2. Page anatomies

The regions each kind of page needs, top to bottom, and why that order:
each region answers the question the reader has at that moment. Required
regions are marked; the rest earn their place from real content (never a
logo strip without real customers, never a testimonial without a real
person, never a stat without a source).

### Homepage / landing page (product, SaaS, developer tool)

The reader arrives asking, in order: what is this, is it for me, does it
work, how does it work, what does it cost, what do I do now.

1. **Header** (required): logo left; 3 to 6 links (Product, Pricing, Docs,
   Blog); one secondary action (Sign in) and one primary (Start free /
   Install). Sticky or not, never two rows.
2. **Hero** (required): headline that names the outcome (not the
   category), one sentence that says how, the primary action and at most
   one secondary, and the product itself (a real screenshot, a working
   demo, the install command). Above the fold at 1440x900 and at 390x844.
3. **Proof strip** (optional, real only): customer logos, a real number
   with its source, or a well-known user quote.
4. **Problem or outcomes**: 3 to 6 things the product changes, each with
   what it replaces. Short.
5. **How it works**: the real steps, as many as there are (2, 3, 5), with
   the product shown at each.
6. **Feature detail**: one section per major capability, text beside a
   product visual, alternating sides only if the content is parallel.
7. **Social proof** (real only): testimonials with name, role, company.
8. **Pricing** (when self-serve): the plans that exist, the recommended
   one marked only if it is truly the default.
9. **FAQ** (real objections only: data, lock-in, price, setup time).
10. **Final call to action**: the same primary action as the hero.
11. **Footer** (required): link groups that exist, legal, contact.

Variants: a **developer tool** puts the install command and a code sample
in the hero and Docs in the header; a **local business** puts hours,
address, phone and booking above the fold; a **portfolio** leads with work,
not a bio; a **store** leads with products and search, not a slogan.

### Dashboard / application overview

The user arrives asking: is everything all right, what changed, what needs
me, and where is the detail.

1. **App shell** (required): navigation (a sidebar of 5 to 9 sections, or a
   top bar for 3 to 5), the product, global search, notifications, account.
   The shell never scrolls with the content.
2. **Page header** (required): page title, the scope (date range, account,
   environment), filters that apply to the whole page, the page's one
   primary action on the right.
3. **KPI row**: 3 to 5 stats that answer "is it all right": label, value,
   change against a named period ("+12% vs last week"), and a link to the
   detail. Not 8, not decorative.
4. **Primary visualization**: the one chart that answers the main
   question, full width or two thirds.
5. **Secondary panels**: breakdowns that explain the primary (by channel,
   by region), in a 2 or 3 column grid of equal-height cards.
6. **Activity or worklist**: what needs the user (the latest items, the
   queue), as a table or list with a "View all" link to the list page.

For a tool where the user acts on what they see (trading, editing,
scheduling): the object and its state first, the action panel beside it
(right, sticky) on desktop and below it on a phone, the consequences
(positions, history) after.

### List / table page

Page header (title, count, primary "New"), toolbar (search, filters,
sort, view), active filter chips, the table or grid, pagination or "load
more", and an empty state for no results that offers clearing filters.
Bulk actions appear in place of the toolbar when rows are selected.

### Detail page

Breadcrumbs, the object's header (name, status badge, key facts, actions:
primary right, the rest in an overflow menu), tabs or sections for its
parts (overview first), and a side column for metadata on desktop.
Destructive actions last, behind confirmation.

### Settings

Sections in a left list (or tabs) by what they configure, not by
technical module: Profile, Account, Notifications, Billing, Team, Danger
zone last. Each section is a form with its own save, or saves on change
with confirmation; a field's description says what it changes.

### Form or wizard

Title and why; the fields in the order a person answers them (who, what,
when, how much); one column; groups with headings; the primary action at
the end, aligned with the fields; errors inline at the field and summarized
at the top on submit. A wizard shows the steps and where you are, keeps
what was entered when you go back.

### Sign-in / sign-up

The product's mark, one heading, the fields (email first), the primary
button full width of the form, the alternative (SSO buttons) above or
below with a divider, the link to the other form, nothing else on the page.

### Pricing

The plans that exist side by side (one column on a phone), each: name, who
it is for, price with period, the primary action, what it includes (the
differences first). A comparison table below for detail, then FAQ.

### Docs

Header with search (Cmd+K), left navigation by section, the article with
its title, a short lede, headings, and code blocks with copy; on the
right, the page's contents; previous and next at the end.

### Article / blog post

Title, author and date, reading time, the lead image if it adds
something, the body at 60 to 75 characters a line, headings, then author,
related posts.

### Checkout

Steps (cart, details, payment, review), the form on the left, the order
summary on the right (sticky on desktop, collapsible on a phone), the total
and the primary action visible without scrolling at the last step, trust
details (secure payment, returns) near the button.

## 3. The skeleton, in numbers

Decide these once, write them into DESIGN.md, and build every section on
them. A page without them gets a different edge per section.

- **Container**: one container component for every section's content.
  Marketing: max 1200 to 1280px. App screens: fluid with a max of 1440 to
  1600px. Text columns: max 65 to 75 characters.
- **Gutters**: the space between the window's edge and any content: 16px
  on a phone, 24px on a tablet, 32px on a desktop. Content never starts at
  x=0. Full-bleed backgrounds may reach the edge; their content may not.
- **One left edge**: every section's content starts on the container's
  edge. Cards align to the grid, not to each other by eye.
- **Grid**: 12 columns with 24px gaps (16 on a phone), or a fixed sidebar
  plus a fluid main. Spans: 12, 8+4, 6+6, 4+4+4, 3x4.
- **Spacing scale** (4px base): 4, 8, 12, 16, 24, 32, 48, 64, 96. Inside a
  component 4 to 16; between components in a group 16 to 24; between
  sections 32 to 48 in an app, 64 to 128 on a marketing page. Never two
  different gaps for the same relation.
- **Surfaces**: decide what is a card. In an app, every panel of the same
  level is the same surface (all cards, or none with dividers). A region
  without a surface beside regions with one reads as an accident.
- **Heights**: controls share a height scale: 32 (compact), 40 (default),
  48 (large). A button beside an input has the input's height.
- **Type scale**: body 14 to 16px in an app, 16 to 18 on a marketing page;
  labels and captions 12 to 13 at the smallest, never the main text.
  Numbers that change use tabular figures.
- **Breakpoints**: 640, 768, 1024, 1280. For each, say what changes: a side
  panel moves below, a grid goes from 4 to 2 to 1, navigation collapses to
  a menu, a table becomes rows or scrolls inside its own container. The
  page itself never scrolls sideways.

## 4. From the blueprint to code

Build in this order; each step uses only what the steps before it made.

1. **Tokens**: colours (by role: background, surface, text, muted, border,
   accent, success, warning, danger), the spacing scale, radii, type sizes,
   control heights, shadows, both themes. CSS custom properties, or the
   Tailwind theme mapped to them. No literal colour or size below this.
2. **Layout primitives**: `Container` (max width + gutters), `Stack`
   (vertical gap), `Cluster` (wrapping row with gap), `Grid` (columns and
   spans), `Section` (vertical spacing between sections). Every page
   composes these; no section invents its own padding.
3. **Components** from `ui-anatomy`, each with all its variants, sizes and
   states (hover, focus-visible, active, disabled, loading, selected,
   error) and its keyboard behaviour. Variants through one function (`cva`
   or a variant map), not booleans scattered across call sites.
4. **Sections**: one component per region of the blueprint, fed by data
   (arrays of items), not copy-pasted markup.
5. **The page**: the regions in the blueprint's order, inside `Container`,
   spaced by `Section`, nothing else.
6. **States**: loading (a skeleton the shape of the content), empty (what
   it is, why it is empty, the action), error (what failed, retry), per
   region, not one spinner for the page.
7. **Responsive**: the breakpoint changes from the skeleton, then check
   360, 768 and 1440.

```tsx
// Layout primitives: every section uses these and nothing else for space.
export function Container({ children, className }: Props) {
  return <div className={cn("mx-auto w-full max-w-[1440px] px-4 md:px-6 lg:px-8", className)}>{children}</div>;
}
export function Section({ children }: Props) {
  return <section className="py-8 lg:py-12">{children}</section>;
}

// The page is the blueprint, in order.
export function TradingPage() {
  return (
    <>
      <AppHeader />
      <Container>
        <Stack gap="8">
          <InstrumentHeader />
          <Grid cols={12} gap="6">
            <Panel className="col-span-12 lg:col-span-8"><PriceChart /></Panel>
            <Panel className="col-span-12 lg:col-span-4 lg:sticky lg:top-20"><OrderTicket /></Panel>
          </Grid>
          <PositionsSummary />
          <PositionsTabs />
        </Stack>
      </Container>
    </>
  );
}
```

## 5. Check before you say it is done

Measure; do not eyeball. With `preview` on, run it and fix what it reports
at 360, 768 and 1440. Then check these against the page:

- Nothing touches the window's edge at any width; nothing is cut off or
  scrolls sideways at 360.
- Every section starts on one left edge; the same relation has the same
  gap everywhere.
- Panels of one level share one surface treatment.
- One primary action per screen (or per card in a list of choices).
- Every control shows hover, focus-visible, active, disabled and selected;
  a segmented control or tab shows which is selected without colour alone.
- A form's submit is disabled or explains itself until the input is valid;
  inputs have labels, units and help where needed.
- Text is 14px or more for reading, 12px only for captions; no more than
  the token colours.
- Loading, empty and error exist for every region that loads.
- The blueprint's order is the page's order.

When `preview` is off, say in your report that the page was not seen in a
browser, and which of these you could only check in the code.
