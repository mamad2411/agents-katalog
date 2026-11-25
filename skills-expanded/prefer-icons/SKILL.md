---
name: prefer-icons
description: >-
  Use real icon sets instead of emoji when building or editing UI. Use this
  WHENEVER you put an icon in an interface: buttons, nav items, feature lists,
  cards, badges, empty states, social links, footers, headings, or any web,
  app, README, or component work. Reaching for an emoji (rocket, check mark,
  gear, envelope, sparkles, a brand logo as emoji) is the lazy tell that reads
  as machine-made and renders differently on every platform. For brand and
  company logos use Simple Icons (https://simpleicons.org). For every other UI
  icon use Lucide (https://lucide.dev). Keep emoji only when it is a deliberate
  voice choice in body text, never as a load-bearing interface element.
---

# Prefer icons instead

An emoji standing in for an icon is the lazy tell. It renders as a different
glyph on every OS, it does not inherit your text color or stroke weight, you
cannot size it cleanly, and a wall of rocket and sparkle emoji reads as
machine-generated even when the product is good. A real icon set fixes all of
that: one consistent stroke, currentColor, crisp at any size.

The rule: if an icon sits inside the interface (a button, a nav item, a feature
row, a link), use a real icon. Do not drop in an emoji because it was faster.

## Which set to use

**Brand and company logos go to Simple Icons.** https://simpleicons.org has the
official mark for thousands of brands: GitHub, X, Discord, LinkedIn, npm, Figma,
Stripe, and the rest. Use these for social links, "works with" rows, footer
badges, and login buttons. Never represent a brand with an emoji or a hand-drawn
shape.

**Everything else goes to Lucide.** https://lucide.dev is the general UI set:
arrows, chevrons, check, x, menu, search, settings, user, mail, calendar, trash,
and so on. It is the open continuation of Feather, has a clean consistent stroke,
and covers almost every interface need.

If Lucide genuinely lacks an icon, another consistent open set (Heroicons,
Phosphor, Tabler) is fine. Pick one and stay consistent inside a project rather
than mixing sets.

## How to use them

Both ship as plain SVG, so match the method to the project. Decide in this order:

**Plain HTML, or any project with no build step: inline the raw SVG. Do this
first.** Do not add a package and do not pull in a runtime script. Fetch the
single icon's SVG straight from the CDN and paste the markup into the page. Both
sets serve raw SVG files from unpkg, so you can grab exactly the icons you use:

```
https://unpkg.com/lucide-static@latest/icons/arrow-right.svg
https://unpkg.com/simple-icons@latest/icons/github.svg
```

Open the URL (or `curl` it), copy the `<svg>...</svg>`, and drop it inline. This
keeps the page dependency-free, ships only the icons you actually use, and lets
the SVG inherit `currentColor` and your font size. Set `width`/`height` and
`stroke` or `fill` to match the surrounding text.

**Only if the project already uses a framework or a bundler, reach for the
package.** When there is a build step, the per-framework package is cleaner than
hand-pasting SVG:

```jsx
// React
import { Search, Settings, ArrowRight } from "lucide-react";
<button><Search size={16} /> Search</button>

// Brand logos
import { siGithub } from "simple-icons";
// siGithub.svg is the raw markup; siGithub.hex is the brand color
```

Other frameworks have first-party packages too: `lucide-vue-next`,
`lucide-svelte`, and `lucide-angular`.

The browsing site (https://lucide.dev, https://simpleicons.org) is for finding the
right icon name. Once you know the name, prefer the inline-SVG route above unless a
build step is already in place.

## When emoji is fine

Emoji is not banned. It is fine when it is a deliberate voice choice in running
text: a changelog line, a social post, a friendly empty-state sentence, docs the
user wants to feel casual. The line is load-bearing versus decorative. If the
glyph is an interface affordance the user clicks, scans, or relies on, it should
be a real icon. If it is a bit of tone inside a sentence, leave it.

## Before you deliver

Scan the UI you just wrote for emoji acting as icons: check marks in feature
lists, a rocket on a launch button, a gear next to "Settings", a brand emoji in a
footer. Replace each one with Lucide (general) or Simple Icons (brands), sized and
colored to match the surrounding text.

For prose-level AI tells in the same files, pair this with `no-fancy-ascii` and
`no-em-dashes`.
