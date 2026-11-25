---
name: ui-part-avatars
description: "Avatars for people and organisations: photo or initials, a colour from a stable id, sizes and shapes, alt text, groups with a +N count, status dots, fallbacks and uploads. Read before showing a person, a team or an organisation in an interface."
---

# Avatars

The generated version: a stock or AI-made face beside an invented name, a
grey silhouette on every row, initials on a colour that changes with every
render, a gradient ring round a circle that says nothing. An avatar exists
to tell people apart at a glance. This is how it does that with real
photos, honest fallbacks and a name a screen reader hears once. One part of
an interface: the principles (direction, spacing, type, colour, icons,
states, accessibility) are in the `ui` skill, the measures in `ui-layout`.

## 1. When to use one

- Where the question is who: the author of a comment, the assignee of a
  task, the members of a workspace, the account in the top bar, a message
  thread, an activity feed.
- Beside the name, not instead of it. Alone only where space forces it (an
  assignee column, a stack of reviewers), and then the name is its
  accessible name and its tooltip.
- Not on rows that are not about people, not on every row when every row
  is the same person, and not as a large avatar with an invented name in
  the sidebar's account block (`ui-part-sidebar`).
- A person is a circle; an organisation, a workspace or a project is a
  rounded square with its logo or its initial. In a mixed list the shape
  alone tells them apart.

## 2. Sizes and anatomy

| Size | Where | Initials |
|---|---|---|
| 24px | mentions, dense table cells, stacks inside a row | one letter, 10 to 11px |
| 32px | comments, list rows, the account button in the top bar | two letters, 13px |
| 40px | two-line rows, cards, chat messages | two letters, 16px |
| 64px | a profile panel, the head of a member's page | two letters, 26px |
| 96px | a profile page, the upload preview | two letters, 38px |

- A size from this scale, as tokens, nothing in between. Initials at about
  40% of the size, weight 500 to 600, `line-height: 1`, centred in the box.
- The rounded square's radius is about 20% of the size, from the radius
  scale (6px at 32px, 12px at 64px).
- A 1px inner ring at about 10% of the text colour, drawn over the photo,
  so a portrait on a white background keeps its edge on a white page, and a
  dark one on a dark page.
- 8px between avatar and name up to 32px, 12px from 40px. In a two-line
  row the avatar aligns with the top of the name; in a one-line row it is
  centred.
- `flex: none` on it, so a long name never squeezes it into an oval.

## 3. Photo, initials, colour

- The person's photo when there is one, and only a real one: the photo
  they uploaded, or the one from the identity provider they signed in with
  (Google, GitHub, Microsoft) when the product uses it. Square, served at
  twice the shown size (128px for 64px), WebP or AVIF, `width` and
  `height` set, `object-fit: cover`.
- Otherwise their initials: the first letter of the first and the last
  word of the display name, two at most; one letter for a one-word name
  (common in Indonesia and elsewhere) and at 24px. Take graphemes with
  `Intl.Segmenter`, not string indexes, so accented and non-Latin letters
  stay whole. No name yet: the first letter of the email, or a neutral
  person icon from the product's set.
- The colour is derived from a hash of a stable key (the user id; the name
  only when there is no id), so a person has one colour on every screen
  and after every reload. A set of 6 to 8 background and text pairs as
  tokens, each checked at 4.5:1 in both themes: a light tint with dark text
  of the same hue on light, a deep tint with light text on dark. Leave out
  the accent (it means action) and red and green (they mean status).
- The photo fails (404, blocked, offline): the initials take its place,
  never a broken-image icon or an empty circle. While a photo is on its
  way, wait 300 to 500ms before drawing the initials, so a photo that
  arrives quickly does not flash them first.
- Gravatar only when the product already uses it, with `d=404` so a
  missing one falls back to your initials rather than a generated pattern.
  It sends a hash of the email to a third party; the privacy notice says so.

## 4. Names for screen readers

- The name printed beside it: the avatar is decoration. `aria-hidden="true"`
  on it (or `alt=""` on a plain image), so the name is not read twice and
  the initials are not read as a word.
- The avatar alone: an alt of the person's name, because it now carries
  information. `role="img"` with `aria-label` on the avatar covers the
  initials too when the photo fails; never "Avatar of" or "Photo of".
- An avatar that opens something is a button or a link with its own name
  ("Account menu", "Profile of [name]"), the picture inside it decoration;
  32px visible inside a 44px target on touch.

## 5. Groups

- An overlapping stack answers "who is on this": 3 to 5 avatars at most,
  then a "+N" disc of the same size on a neutral surface. Three on a phone.
- Overlap about a quarter of the size (-8px at 32px), with a 2px ring in
  the page's surface colour round each, so the edges read.
- A stable order by relevance (the owner, then the most recent), the same
  on every render.
- Every name reachable: a tooltip on each for the pointer, and the stack
  as one button that opens the full list, for keyboard, touch and screen
  readers. Its name gives the total: "5 members: [name], [name] and 3
  more".

## 6. Status dots

- Only where the product really tracks presence (a chat, a support desk).
  Never a green dot on everyone.
- 8 to 12px, about a quarter of the avatar, at the bottom right (bottom
  left in right-to-left), with a 2px ring in the surface colour.
- Colour, shape and words: filled for online, a hollow ring for away,
  nothing for offline; the state in the accessible name ("[name], away")
  and the tooltip. No pulsing or breathing dot.

## 7. Uploading one

- In the profile settings: the current avatar at 96px, with "Change photo"
  and "Remove photo" beside it; removing goes back to the initials.
- JPEG, PNG and WebP up to a stated size (5 MB is plenty), said before the
  file is chosen. Crop to a square in the browser (react-easy-crop,
  Cropper.js) with a preview at 32 and 96px; resize to 256px on the server
  and strip EXIF data, which can hold where the photo was taken.
- Progress on the button; the error in words: "That file is 12 MB. The
  limit is 5 MB."

## 8. Phones, themes, motion

- Sizes do not shrink on a phone; stacks show fewer. Anything tappable is
  44px.
- Themes: every colour pair and the ring have a value per theme; photos
  stay as they are (`ui-themes`).
- Motion: none beyond the photo fading in over 160ms when it replaces the
  initials (`motion-interface`).

## 9. A sketch

React with Radix Avatar (shadcn's Avatar is the same primitive).
`nameShown` says whether the name is printed beside it.

```tsx
import * as Avatar from "@radix-ui/react-avatar";

const PAIRS = 8; // --avatar-1-bg, --avatar-1-fg ... --avatar-8-fg: each pair 4.5:1 in both themes

function pairFor(id: string): number {
  let h = 2166136261; // FNV-1a: the same number on every render and machine
  for (const ch of id) h = Math.imul(h ^ ch.codePointAt(0)!, 16777619);
  return ((h >>> 0) % PAIRS) + 1;
}

function initials(name: string, max: number): string {
  const words = name.trim().split(/\s+/).filter(Boolean);
  const picked = words.length > 1 ? [words[0], words[words.length - 1]] : words;
  const seg = new Intl.Segmenter();
  return picked.slice(0, max)
    .map((w) => [...seg.segment(w)][0]?.segment ?? "")
    .join("").toLocaleUpperCase();
}

export function PersonAvatar({ id, name, src, size = 32, nameShown = false }: {
  id: string; name: string; src?: string; size?: 24 | 32 | 40 | 64 | 96; nameShown?: boolean;
}) {
  const n = pairFor(id);
  const style = { "--size": `${size}px`, "--bg": `var(--avatar-${n}-bg)`,
    "--fg": `var(--avatar-${n}-fg)` } as React.CSSProperties;
  const a11y = nameShown ? { "aria-hidden": true } : { role: "img", "aria-label": name };
  return (
    <Avatar.Root className="avatar" style={style} {...a11y}>
      {src && <Avatar.Image src={src} alt="" width={size} height={size} />}
      <Avatar.Fallback delayMs={src ? 400 : 0}>
        {initials(name, size === 24 ? 1 : 2)}
      </Avatar.Fallback>
    </Avatar.Root>
  );
}
```

```css
.avatar {
  position: relative; flex: none;
  display: inline-grid; place-items: center;
  inline-size: var(--size); block-size: var(--size);
  border-radius: 50%; overflow: hidden;
  background: var(--bg); color: var(--fg);
  font-size: calc(var(--size) * 0.4); font-weight: 600; line-height: 1;
}
.avatar img { inline-size: 100%; block-size: 100%; object-fit: cover; }
.avatar::after { /* the inner ring, over the photo */
  content: ""; position: absolute; inset: 0; border-radius: inherit;
  box-shadow: inset 0 0 0 1px var(--avatar-ring);
}
.avatar[data-kind="org"] { border-radius: calc(var(--size) * 0.2); } /* organisations */
```

## Check it

- `preview` at 360px: an avatar button in "controls without a name" or
  "touch targets under 44px", or an avatar in "images without alt", is a
  finding to fix.
- `ui_check`: `image-without-alt`, and `placeholder-content` for "John
  Doe" and the like under an avatar.
- Break a photo's URL: the initials appear in the same box, nothing jumps.
- Show one person on two screens: the same colour on both. Compute every
  pair's contrast in both themes.
- With a screen reader, a row with an avatar and a name reads the name
  once; a stack reads its total and opens the full list from the keyboard.
- Search the code for `pravatar`, `randomuser`, `thispersondoesnotexist`
  and stock portrait URLs, and take them out.

## Avoid

Stock or generated faces presented as people, and any face for a
placeholder user; invented names under avatars; a colour that changes on
every render; white initials on a mid-tone colour that fails 4.5:1; a
broken-image icon where the initials belong; the name read twice; a stack
whose hidden names no keyboard can reach; a green dot on everyone; a
gradient or glowing ring as decoration; avatars on rows that are not about
people.
