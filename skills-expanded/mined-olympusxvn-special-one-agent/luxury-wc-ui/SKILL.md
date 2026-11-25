---
name: luxury-wc-ui
description: >-
  Premium "Luxury World Cup 2026" UI system for the Walrus Memory app. Use when
  building or restyling any page/component so it stays consistent: obsidian +
  gold + platinum palette, glassmorphism cards, Sora display type, stadium
  imagery backgrounds, and gold-glow hover states. Triggers on phrases like
  "make this tab luxury", "match the home design", "redesign UI", "góc bo tròn".
---

> **Cursor (all projects):** portable copy at `~/.cursor/skills/luxury-wc-ui/`
> (`SKILL.md` + `reference.md`). Use that skill when bootstrapping a new repo.

# Luxury World Cup 2026 — UI Skill

A portable design system. Every screen in this app must read as a **premium VIP
lounge for the 2026 World Cup final**: dark obsidian base, metallic gold
accents, frosted glass, elegant geometric calm. Never neon, never cluttered.

## When to use

- Building a new page or tab.
- Restyling an existing surface to match Home / Schedules / Media / Chat.
- Any request mentioning luxury, premium, gold, glass, rounded corners, or
  "make it like the other tabs".

## Strict invariants

1. **Title lock:** the hero/brand line is always `Session 4: Walrus Memory`
   (nav shows `Session 4 · Walrus Memory`). Never rename it.
2. **Palette:** obsidian/midnight base, gold (`#FFD700`) + champagne/platinum
   accents only. No bright neon.
3. **Type:** `Sora` for display/headlines (`luxe-display`), `Inter` for body.
4. **Glass everywhere:** cards, panels, nav, badges use `.luxe-glass`.
5. **Rounded corners:** glass cards 22px, flags/tiles 16px, pills/buttons full.
6. **Backgrounds:** original WC imagery, full color, NOT blurred/dimmed. Only a
   light top/bottom scrim for legibility (`StadiumBackground`).
7. **Motion is honest:** entrance reveals via CSS `animate-fade-in` (never JS
   `initial=hidden` gating), and respect `prefers-reduced-motion` /
   `prefers-reduced-transparency` (already handled in CSS).

## The building blocks (already in the repo)

### Layout shells
- `components/luxury/LuxuryNav.tsx` — sticky glass top bar. Pass
  `active="/route"` to highlight the tab. Put it on every page.
- `components/world-cup/StadiumBackground.tsx` — full-bleed WC imagery backdrop.
  Render first inside a `relative overflow-hidden` page wrapper.
- `components/luxury/LuxuryHero.tsx` — reference hero (avatar + strict title +
  flag strip + chips + CTAs) in a `luxe-glass luxe-glass-strong` panel.

### CSS utility classes (`app/globals.css`)
| Class | Purpose |
|---|---|
| `luxe-display` | Sora headline, tight tracking |
| `luxe-eyebrow` | uppercase gold-muted label above titles |
| `luxe-gold-text` | gold gradient text clip (use inside headings) |
| `luxe-hairline` | thin gradient divider |
| `luxe-glass` | frosted glass card (22px radius, gold-glow hover) |
| `luxe-glass-strong` | denser glass background for hero panels |
| `btn-luxe` | primary gold gradient pill button |
| `btn-luxe-ghost` | secondary glass outline pill button |
| `luxe-flag` | glass flag tile (16px) — via `<TeamFlag variant="glass" />` |
| `luxe-chip` / `luxe-chip-gold` | status/metadata pills |
| `luxe-navlink` / `luxe-navlink-active` | nav + tab buttons |
| `luxe-connect` | wrapper that gold-skins the dapp-kit `ConnectButton` |

### Tokens
- Tailwind: `bg-gold`, `text-gold`, `obsidian`, `midnight`, `champagne`,
  `platinum`, `font-display`.
- CSS vars: `--gold`, `--gold-soft`, `--gold-deep`, `--gold-glow`,
  `--glass-bg`, `--glass-bg-strong`, `--glass-border`, `--glass-highlight`,
  `--text-gold`, `--text-muted`.

### Taste engine (motion/spacing dials)
`lib/skills/taste` exposes `useTasteSkill(LUXURY_WC_TASTE)` returning resolved
`tokens.motion` (`enabled`, `stagger`) and spacing. Use it to drive staggered
`animate-fade-in` reveals (see `LuxuryHero`).

## Page recipe (copy this skeleton)

```tsx
export default function SomePage() {
  return (
    <div className="relative min-h-screen overflow-hidden">
      <StadiumBackground />
      <LuxuryNav active="/some" />
      <main className="relative z-10 mx-auto max-w-walrus px-5 py-10 sm:px-6 sm:py-14">
        <header className="mb-10 text-center">
          <p className="luxe-eyebrow">FIFA World Cup 2026</p>
          <h1 className="luxe-display mt-4 text-5xl sm:text-6xl">
            Some <span className="luxe-gold-text">Title</span>
          </h1>
          <p className="mx-auto mt-5 max-w-2xl text-muted">Subhead…</p>
        </header>
        <section className="luxe-glass luxe-glass-strong p-6">…</section>
      </main>
    </div>
  );
}
```

## Wallet gating pattern (Chat)
When `!account`, show a `luxe-glass` hero with the avatar, strict copy, and a
gold-skinned connect button:

```tsx
<div className="luxe-connect">
  <ConnectButton connectText="Connect Sui wallet" />
</div>
```

After connect, a signature verification runs automatically (see
`ChatContainer.verifyWallet`). Keep the connected chat surface in `luxe-glass`.

## Do / Don't
- DO keep generous whitespace, one accent (gold) per view, subtle hover lift.
- DO reuse `LuxuryNav` + `StadiumBackground` on every tab for consistency.
- DON'T blur/darken background imagery, add neon, or use square `walrus-card`
  on luxury pages (prefer `luxe-glass`).
- DON'T gate content behind JS-only animations.

## Detach / reuse in another project

**Preferred:** use the Cursor personal skill at `~/.cursor/skills/luxury-wc-ui/`
(read `reference.md` for bootstrap checklist).

Or copy manually:

1. Copy `app/globals.css` luxe blocks (search `luxe-`) + the
   `@media (prefers-reduced-transparency)` fallback.
2. Copy the Tailwind color/`fontFamily.display` extensions.
3. Copy `components/luxury/*`, `components/world-cup/StadiumBackground.tsx`,
   `TeamFlag.tsx`, and `lib/skills/taste/`.
4. Load the `Sora` + `Inter` fonts in the root layout.
