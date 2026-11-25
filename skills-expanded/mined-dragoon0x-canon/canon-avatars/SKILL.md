---
name: canon-avatars
description: Use when designing, auditing, or refactoring avatars, profile images, user pictures, avatar stacks, initials fallbacks, or any user-identifying image. Covers sizing, shape (circle vs square), initials logic, fallback color assignment, alt text, placement conventions, stacked avatar overflow, and the "anonymous user" state. Trigger when the user mentions avatar, profile image, user picture, initials, profile photo, or avatar stack.
---

# CANON · Avatars

Avatars identify a person or entity at a glance. They fail when users can't distinguish them from each other or from generic placeholders.

## Sizing

Avatars have a **small, fixed scale**. Random sizes break visual rhythm.

| Size | Use |
|---|---|
| XS — 16–20px | Inline with text (comment attribution) |
| SM — 24px | Dense lists, table rows |
| **MD — 32px** | Default (nav bars, lists) |
| LG — 40–48px | Profile cards, user headers |
| XL — 64–80px | Profile pages, detail views |
| XXL — 128px+ | Hero profile view |

Pick 3–4 sizes for your system. Avoid one-off in-between values.

## Shape — circle by default

| Shape | When |
|---|---|
| **Circle** | People (default) |
| Rounded square (6–8px radius) | Organizations, teams, workspaces |
| Square | Product/brand logos, less common for people |

Circle avatars differentiate user identity from brand identity — worth preserving.

## Initials fallback

When no image exists, show initials.

```
┌────────┐
│   AB   │
└────────┘
```

- **One or two letters max.** "JJ" (John Jacobson) not "JAJ".
- Logic: first letter of first name + first letter of last name. Single name → one letter.
- Font size: avatar diameter × 0.4 (rough rule). 32px avatar → 13px initials.
- Font weight: 500–600 (semibold).
- Center-aligned both axes.

## Background color — deterministic, not random

Each user gets a consistent color across the app. Random colors per render = visual identity breaks every refresh.

```js
function avatarColor(id) {
  const hash = id.split('').reduce((acc, c) => c.charCodeAt(0) + acc, 0);
  const hue = hash % 360;
  return `oklch(55% 0.15 ${hue})`;
}
```

- Hash the user ID (stable, unique) to pick a hue.
- Keep lightness and chroma constrained so all colors feel unified (same lightness, similar chroma).
- 12–20 hues max in the rotation — prevents near-identical variants.

## Text contrast on initials

White text on colored background: minimum 4.5:1 contrast. With medium-lightness backgrounds (L ≈ 50–60%), use:
- Lightness 40–55% → white text
- Lightness 60–80% → dark text (near-black tinted with the background hue)

Test the whole palette for contrast. WCAG 1.4.3.

## Image fallback chain

```
1. Custom uploaded image   →  use it
2. Gravatar or OAuth image →  use it
3. Initials with color     →  generate
4. Anonymous placeholder   →  generic user icon
```

Failed image loads should gracefully degrade through these states. `<img onError>` handler swaps to initials. Use `loading="lazy"` on non-critical avatars (outside viewport).

## Alt text

```html
<img src="/avatar/456.jpg" alt="Alex Rivera" width="32" height="32">
```

- Name of the person, not "User photo" or "Avatar of Alex".
- If the avatar is purely decorative and the name appears next to it, empty alt: `alt=""`.
- Initials fallback: `aria-label="Alex Rivera"` on the container.

## Stacked avatars

Used to show multiple participants in limited space.

```
┌───┬───┬───┬─────┐
│ ● │ ● │ ● │ +4  │
└───┴───┴───┴─────┘
```

- Negative margin so avatars overlap: each offset by 25–40% of its width.
- White or background-colored **ring around each avatar** (2px) separates them visually.
- Max 3–5 visible, then "+N" counter.
- Counter is a neutral color (muted background, dark text) — distinct from the named users.

```html
<ul class="avatar-stack" aria-label="3 participants">
  <li><img src="..." alt="Alex Rivera"></li>
  <li><img src="..." alt="Bianca Ostra"></li>
  <li><img src="..." alt="Chen Li"></li>
  <li aria-label="2 more"><span>+2</span></li>
</ul>
```

Clicking the stack opens the full list.

## Presence indicator (optional)

Dot in a corner (bottom-right usually) indicates online/offline/busy.

- 25–30% of avatar diameter.
- Ring around it matching the background (so it reads as a separate element, not a bite out of the avatar).
- Colors: green (online), yellow (away), red (busy/do not disturb), gray (offline).
- Add `aria-label="online"` or equivalent.

Don't use color alone — consider pairing with shape (filled dot for online, ring for offline) or text on hover.

## Group / team avatars

Represent a group with:
- The group's logo if it has one.
- 2×2 grid of member avatars (top-left, top-right, bottom-left, bottom-right + overlap).
- Icon representing the group type.
- Text initials for the group name.

Visually distinct from individual avatars (usually rounded-square shape).

## Upload and edit

- Accept JPG, PNG, WebP; enforce square crop.
- Preview before upload.
- Show the circular crop mask even when the source file is square — so users understand the final shape.
- File size warning at 2MB+.
- Automatic resize server-side to 512×512 for the master, downsized variants for other uses.

## Anti-patterns

| Anti-pattern | Why it fails |
|---|---|
| Random color per page load | Visual identity flickers |
| Three-letter initials | Illegible at small sizes |
| No alt text or "User photo" alt | Screen readers don't know who |
| Giant avatars in dense lists | Overwhelms content |
| Square avatars for people without a reason | Feels corporate / off |
| Stacked avatars with no ring separator | Blend into each other |
| Counter styled identical to user avatars | Looks like another user |
| Online indicator without aria-label | Color-only signal |
| Gravatar hash without fallback | Users without Gravatar show default |
| Initials text black on too-dark background | Contrast fail |
| Avatar grows on hover | Layout shift, pointer drifts |

## Decision tree

```
Individual or group?
  ├─ Individual → Circle, user image or initials
  └─ Group → Rounded square, logo or composite

Image available?
  ├─ Yes → Use it, alt=name
  └─ No → Initials on hashed color

Multiple participants to show?
  └─ Stacked avatars with ring separator, +N counter

Presence state matters?
  └─ Corner indicator with background ring + aria-label
```

## Audit checklist

- [ ] Avatar sizes come from a small fixed scale
- [ ] Circle shape for people, rounded-square for groups
- [ ] Initials logic: first letter of first + last name
- [ ] Background color is deterministic (hash of ID)
- [ ] Contrast ≥ 4.5:1 between initials and background
- [ ] `alt` contains the person's name
- [ ] Fallback chain: image → initials → generic
- [ ] Stacked avatars have 2px separating ring
- [ ] "+N" counter styled distinctly from user avatars
- [ ] Presence indicator has `aria-label`, not color-only
- [ ] Mobile hit target ≥ 44px if interactive
- [ ] Avatar doesn't grow/shift on hover

## Sources

- WCAG 2.2 · 1.1.1 Non-text Content, 1.4.3 Contrast (Minimum)
- Material Design 3 · Avatars
- Atlassian Design System · avatar color generation
- Apple HIG · Profile images
