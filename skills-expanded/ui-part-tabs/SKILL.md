---
name: ui-part-tabs
description: "Tabs: when to use them and what instead, route tabs as links versus in-page tabs, anatomy and the selected state, the APG tabs keyboard pattern with automatic or manual activation, tab state in the URL, lazy panels that keep their state, overflow on phones, and motion. Read before building tabs or a row of sub-navigation."
---

# Tabs

The generated version: pill tabs in a grey track where the selected one is
only a shade lighter, tabs standing in for the site's navigation, a
wizard's steps dressed as tabs, counts that were made up, and seven tabs
running off the side of a phone. Tabs switch between views of one thing,
show which view is open beyond doubt, and move with the arrow keys. The
principles are in the `ui` skill, the measures in `ui-layout`, the motion
in `motion-interface` (section 7).

## 1. When tabs, and when not

- Use them for switching between views of the same thing (Details,
  Activity, Settings), two to six of them, when people need one view at a
  time.
- Not for:
  - steps that must be done in order: a stepper (`ui-part-steps`);
  - content people compare side by side, or read from top to bottom:
    sections on one page;
  - two or three modes of the same content (List, Board): a segmented
    control (`ui-part-choices`);
  - sections a reader may want open together on a phone: an accordion
    (`ui-part-faq`);
  - the site's main navigation (`ui-part-navigation`).
- Tabs hide content: find in page does not reach a hidden panel (except
  where `hidden="until-found"` is supported), and print shows one panel.
  What everyone needs goes in the first tab or outside the tabs.

## 2. Two kinds

- **Route tabs**: each tab is its own URL (`/projects/42/activity`). They
  are links in a `nav` with a label ("Project"), the current one with
  `aria-current="page"`. No `tablist` role and no arrow keys: they are
  links, and Tab moves through them. Use them when each view is large,
  loads its own data, or should be bookmarked and shared.
- **In-page tabs**: the APG tabs pattern (`tablist`, `tab`, `tabpanel`) for
  views that live in one page.
- Avoid tabs that navigate to other pages: the `tablist` role on links that
  load new pages, or tab-styled links to unrelated places. Views of the
  same object at their own URLs are route tabs, as above.

## 3. Anatomy and measures

- The row of tabs sits on a 1px `--border` baseline, directly above its
  panel, as wide as the content.
- Each tab: 40 to 48px tall (44px on touch), 12 to 16px of side padding, 14
  to 16px text in sentence case, one or two words; a 16 to 20px icon only
  when every tab has one.
- The selected tab marked by more than colour: a 2px indicator on the
  baseline in `--accent` or `--text`, and its label in `--text` at weight
  600 while the others are in `--text-muted` (still 4.5:1).
- A count only when it is real and useful ("Comments 12"), in a quiet
  badge, kept up to date with the data.
- The panel starts 16 to 24px below the row, on the same left edge.
- Vertical tabs (a settings page with many sections): a list at the left on
  wide screens, the panel at the right; on phones a select or a list of
  links.

## 4. States

- **Hover**: the label to `--text`, or a surface step, under
  `@media (hover: hover)`.
- **Focus-visible**: a 2px ring around the tab, inset when the row clips
  it.
- **Selected**: the indicator and the weight, with `aria-selected="true"`.
- **Disabled**: rare. Remove a tab that never applies here, or keep it and
  explain in its panel why it is empty.
- **Loading**: the panel shows its own skeleton; the row never waits
  (`ui-part-loading`).
- **Error**: inside the panel, with a retry; the other tabs keep working.

## 5. Keyboard and ARIA (in-page tabs)

- One Tab stop: Tab lands on the selected tab (a roving `tabindex`: the
  others have `-1`), and the next Tab moves into the panel.
- Left and Right Arrow move between tabs, wrapping at the ends; Home and
  End jump to the first and the last. Vertical tabs take Up and Down, with
  `aria-orientation="vertical"`.
- Automatic activation (the arrow selects the tab) when panels show at
  once; manual activation (the arrow moves focus, Enter or Space selects)
  when a panel is heavy or fetches data: Radix `activationMode="manual"`,
  React Aria `keyboardActivation="manual"`.
- Each tab has `aria-controls` naming its panel; each panel has
  `aria-labelledby` naming its tab, and `tabindex="0"` when nothing inside
  it can take focus at its start.
- Use the library's tabs where there is one: Radix `Tabs` (shadcn/ui),
  React Aria `Tabs`, Headless UI `TabGroup`, Ark UI or Bits UI `Tabs`.

## 6. State and content

- Tab state in the URL when it should survive a reload or a shared link:
  `?tab=activity` with `history.replaceState` (push only when people expect
  Back to return to the previous tab); an unknown value opens the first
  tab.
- The default tab is the one most people need; the order follows use.
- Lazy panels: render a panel the first time it opens, then keep it
  mounted and `hidden`, so a half-filled form or a scroll position survives
  switching. Libraries that unmount hidden panels (Radix does) need
  `forceMount` on panels that hold input.
- Labels are the product's nouns ("Invoices", "Members"), never truncated;
  counts only when real.

## 7. Phones and touch

- On a phone the tab row scrolls sideways or becomes a select.
  - Scrolling: `overflow-x: auto` on the row (never the page), a fade at the
    edge where more tabs wait, `scroll-snap-type: x proximity`, and the
    selected tab scrolled into view on load and on change
    (`scrollIntoView({ block: "nearest", inline: "nearest" })`).
  - More than four or five tabs at 360px: a select named like the row, or
    route tabs as a list of links.
- Targets 44px tall; nothing revealed on hover only.

## 8. Themes and motion

- The indicator reaches 3:1 and the selected label 4.5:1 in both themes
  (`ui-themes`).
- The indicator slides between tabs (`translateX` and `width`, `--m-base`),
  placed without a transition on the first paint and after a resize; the
  panel changes at once or with a 100 to 160ms crossfade, never sliding
  sideways; no slide under reduced motion (`motion-interface`, section 7).

## 9. A sketch (plain HTML and JavaScript, automatic activation)

```html
<div role="tablist" aria-label="Invoice">
  <button type="button" role="tab" id="tab-details" aria-controls="panel-details"
          aria-selected="true">Details</button>
  <button type="button" role="tab" id="tab-activity" aria-controls="panel-activity"
          aria-selected="false" tabindex="-1">Activity</button>
</div>
<div role="tabpanel" id="panel-details" aria-labelledby="tab-details" tabindex="0">…</div>
<div role="tabpanel" id="panel-activity" aria-labelledby="tab-activity" tabindex="0" hidden>…</div>
```

```js
const tabs = [...document.querySelectorAll('[role="tab"]')];

function select(tab, focus = true) {
  for (const t of tabs) {
    const on = t === tab;
    t.setAttribute("aria-selected", String(on));
    t.tabIndex = on ? 0 : -1;
    document.getElementById(t.getAttribute("aria-controls")).hidden = !on;
  }
  if (focus) tab.focus();
  const url = new URL(location.href);
  url.searchParams.set("tab", tab.id.replace("tab-", ""));
  history.replaceState(null, "", url);
}

tabs.forEach((tab, i) => {
  tab.addEventListener("click", () => select(tab));
  tab.addEventListener("keydown", (event) => {
    const to = { ArrowRight: i + 1, ArrowLeft: i - 1, Home: 0, End: tabs.length - 1 }[event.key];
    if (to === undefined) return;
    event.preventDefault();
    select(tabs[(to + tabs.length) % tabs.length]);
  });
});

const fromUrl = document.getElementById(`tab-${new URLSearchParams(location.search).get("tab")}`);
if (fromUrl?.getAttribute("role") === "tab") select(fromUrl, false);
```

## Check it

- Keyboard: one Tab stop into the row, the arrows, Home and End, then Tab
  into the panel; a screen reader says "tab, 2 of 4, selected".
- Reload with `?tab=activity`: that tab is open; an unknown value opens the
  first.
- `preview` at 360px: the row scrolls inside itself and the page does not
  overflow, tabs reach 44px, unselected labels pass contrast in both
  themes.
- Type into a field in one tab, switch away and back: the text is still
  there.

## Avoid

Tabs for steps that must be done in order (use a stepper); tabs that
navigate to other pages; the selected tab marked by colour alone or by a
slightly lighter pill; seven tabs off the edge of a phone; counts that are
not real; panels sliding sideways; a heavy panel fetched on every arrow
press; what everyone needs hidden in the third tab; a half-filled form
lost on switching.
