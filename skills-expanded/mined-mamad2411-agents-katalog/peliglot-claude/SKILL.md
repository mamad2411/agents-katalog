# Peliglot — Claude Code Guide

## Project Overview

Interactive language learning guides built with React 18 + Vite. Each guide collection lives in `src/guides/{slug}/` and is lazy-loaded by React Router.

## Guide Generation Workflow

Generate guides **one at a time** using the per-guide file structure. Never try to generate an entire `components.tsx` monolith in one shot — it will time out.

### Step 1: Create the directory structure

```
src/guides/{slug}/
  meta.ts
  index.tsx
  components.tsx          (barrel file)
  guides/
    _helpers.tsx           (language-specific helper components)
    guide1.tsx             (one file per guide)
    guide2.tsx
    ...
```

### Step 2: Generate `meta.ts`

Small file (~30-50 lines). Contains `guidesMeta` array, `categories`, and `catColors`.

```ts
import type { GuideMeta, CategoryColors } from '../../types/guide';

export const guidesMeta: GuideMeta[] = [
  { id: 1, title: "Title", subtitle: "Subtitle", cat: "Category", color: "#hex", icon: "emoji" },
  // ...
];
export const categories: string[] = ["Cat1", "Cat2", ...];
export const catColors: CategoryColors = { Cat1: "#hex", Cat2: "#hex", ... };
```

### Step 3: Generate `index.tsx` (boilerplate)

Copy from any existing guide and change: storageKey, sidebarTitle, sidebarSubtitle, theme.

```tsx
import { GuideShell } from '../../components/GuideShell';
import { lightTheme } from '../../styles/themes';
import { guidesMeta, categories, catColors } from './meta';
import { guideComponents } from './components';

export function Component() {
  return (
    <GuideShell
      guidesMeta={guidesMeta}
      guideComponents={guideComponents}
      categories={categories}
      catColors={catColors}
      theme={lightTheme}
      storageKey="peliglot-{slug}"
      sidebarTitle="Guide Title"
      sidebarSubtitle="N Interactive Guides"
    />
  );
}
```

### Step 4: Generate `guides/_helpers.tsx`

Language-specific helper components shared across multiple guides. Examples:
- Custom `Insight` wrapper with language-specific emoji
- `CultureNote`, `Trampa`, `Chatt` components
- Shared data constants (pronoun arrays, color maps)

Type all props explicitly; use `interface XProps { ... }` patterns. If a helper takes children, declare `children: ReactNode`.

### Step 5: Generate each guide file individually

Each `guides/guideN.tsx` is a standalone file (~20-80 lines):

```tsx
import { useState } from 'react';
import { Card } from '../../../components/Card';
import { DarkBox } from '../../../components/DarkBox';
import { Insight } from '../../../components/Insight';
import { speak{Language} } from '../../../utils/speech';
import { HelperComponent } from './_helpers';

const data = [ /* guide-specific data */ ];

export function GuideN() {
  // component body using shared components + data
}
```

### Step 6: Update barrel `components.tsx` after each guide

```tsx
import type { GuideComponents } from '../../types/guide';
import { Guide1 } from './guides/guide1';
import { Guide2 } from './guides/guide2';
// ... add new imports as guides are created
export const guideComponents: GuideComponents = [Guide1, Guide2, ...];
```

### Step 7: Register in router and landing page

- Add slug to `guideSlugs` array in `src/router.tsx`
- Add an explicit entry to the `guideImports` map in `src/router.tsx` using `import('./guides/{slug}/index.tsx')`
- Add guide card to `src/LandingPage.tsx`
- Add `speak{Language}` to `src/utils/speech.ts` if needed

## Available Templates

Templates in `src/components/templates/` reduce boilerplate for common guide patterns.

### AlphabetGrid

Interactive letter grid with filters and detail panel. Used for Guide1 in language guides.

```tsx
import { AlphabetGrid } from '../../../components/templates/AlphabetGrid';
import { speakLanguage } from '../../../utils/speech';

const letters = [
  { l: "A", sound: "/a/", note: "Like 'ah'" },
  // ...
];

export function Guide1() {
  return (
    <AlphabetGrid
      letters={letters}
      letterKey="l"
      nameKey="name"       // optional — field for subtitle under letter
      filterGroups={[
        { id: "all", label: "All", filterFn: () => true },
        { id: "vowel", label: "Vowels", filterFn: l => l.type === "vowel" },
      ]}
      detailFields={[
        { key: "sound" },  // first field shown in header
        { key: "note", label: "Tip", bgColor: "#F5F9F5", borderColor: "#D4E8D4", textColor: "#2E7D32" },
      ]}
      primaryColor="#1B5E20"
      speakFn={speakLanguage}
      introTitle="Section Title"
      introContent={<div>Intro text</div>}
      // Advanced props for custom guides:
      // renderDetail={(letter, {primaryColor, highlightColor}) => <JSX/>}  — fully custom detail panel
      // borderFn={l => l.tricky ? "2px solid #E65100" : null}             — per-letter border
      // badgeFn={l => l.tricky ? {color: "#E65100"} : null}               — dot indicator
      // gridProps={{direction: "rtl"}}                                      — extra grid styles (e.g. Arabic RTL)
    />
  );
}
```

### VerbConjugation

Pronoun-based verb conjugation table. Supports full Card mode and compact mini-table mode.

```tsx
import { VerbConjugation } from '../../../components/templates/VerbConjugation';

// Full mode — Card with title/subtitle
<VerbConjugation
  pronouns={["yo","tú","él/ella","nosotros","vosotros","ellos"]}
  stem="habl"
  endings={["o","as","a","amos","áis","an"]}
  verb="hablar"
  meaning="to speak"
  color="#D84315"
/>

// Compact mode — smaller rows, no Card wrapper
<VerbConjugation
  pronouns={["yo","tú","él","nos.","vos.","ellos"]}
  stem="habl"
  endings={["é","aste","ó","amos","asteis","aron"]}
  title="Pretérito"
  color="#B71C1C"
  compact
/>
```

### QuizSection

Multiple-choice quiz with scoring, visual feedback, and results screen.

```tsx
import { QuizSection } from '../../../components/templates/QuizSection';

const items = [
  { question: "It's hot", answer: "Hace calor", icon: "🌡️" },
  { question: "It's raining", answer: "Está lloviendo", icon: "🌧️" },
  // ...
];

<QuizSection
  items={items}
  answerKey="answer"         // field name for correct answer (default: "answer")
  renderQuestion={(q) => (   // custom question display
    <div>
      <div style={{fontSize:56}}>{q.icon}</div>
      <div style={{fontSize:17,fontWeight:700}}>{q.question}</div>
    </div>
  )}
  optionCount={4}            // number of choices (default: 4)
  color="#0277BD"            // accent color
  resultMessages={{          // optional custom result messages
    high: "¡Excelente!",
    mid: "¡Bien! Keep practicing.",
    low: "Review and try again."
  }}
/>
```

## Shared UI Components

All in `src/components/`:

| Component | Purpose | Usage |
|-----------|---------|-------|
| `Card` | Content section with colored header | `<Card color="#hex" title="Title">children</Card>` |
| `DarkBox` | Highlighted concept/intro box | `<DarkBox title="Title">children</DarkBox>` |
| `Insight` | Tip/hint callout with emoji | `<Insight text="tip text" emoji="emoji" />` |
| `SimpleGuide` | Q&A list from data array | `<SimpleGuide items={[{h:"heading",b:"body"}]} />` |
| `ExpandSection` | Collapsible section | `<ExpandSection title="Title" color="#hex">children</ExpandSection>` |
| `GuideShell` | Navigation wrapper (used in index.tsx only) | See Step 3 above |

## Conventions

- All styles are inline (no CSS modules, no Tailwind)
- Use `useState` for interactivity within guides
- Import speech functions from `../../utils/speech` (or `../../../utils/speech` from guide files)
- Guide functions are named `Guide1`, `Guide2`, etc. and exported as named exports
- The `guideComponents` array order must match `guidesMeta` order (indexed by page number)
- Hawaiian guide (`src/guides/hawaiian/`) is the reference implementation for the per-guide file structure

## CI Constraints

- Bundle size: each JS asset must be < 500KB
- Guide count: `meta.ts` must have entries matching `{ *id:` pattern
- Build must produce `dist/index.html`

## Quick Validation Commands

| Command | What it does |
|---------|-------------|
| `npm run lint` | ESLint check — catches unused vars, missing imports, hooks violations |
| `npm run build` | Production build — verifies all imports resolve and produces `dist/` |
| `npm run validate` | Guide structure check — meta entries match file counts, all slugs registered |
| `npm run check` | Runs lint + build + validate in sequence |

## Bundle Size Debugging

- After build, check sizes: `ls -lh dist/assets/*.js`
- Each JS asset must be < 500KB (enforced by CI)
- Each guide collection lazy-loads independently via React Router, so adding guides to one collection doesn't affect other chunks
- `react-vendor` chunk is split out in `vite.config.ts` via `manualChunks`
- If a chunk is too large, check for oversized inline data arrays or unnecessary imports in that guide's files

## Common Pitfalls

- `guideComponents` array in `components.tsx` must match `guidesMeta` order in `meta.ts` (indexed by page number)
- After adding a new guide file, update **both** `components.tsx` (barrel import) and `meta.ts` (metadata entry)
- New guide collections need entries in three places: `src/router.tsx` (`guideSlugs`), `src/LandingPage.tsx`, and optionally `src/utils/speech.ts`
- All styles are inline — no CSS files, no Tailwind, no CSS modules
- Speech functions use the Web Speech API; available voices vary by platform

## Mastery Layer

The spaced-repetition engine. Full contract in `src/mastery/ARCHITECTURE.md`.

### `useMastery` hook

```ts
import { useMastery } from '../../hooks/useMastery';

const {
  getCardState, rateCard, streak, todaysReviewCount, dailyGoal, isHydrated,
  xpToday, xpAllTime,
} = useMastery(adapter); // adapter is optional; defaults to defaultMasteryAdapter
```

- `getCardState(cardId)` — synchronous read from in-memory cache; returns `CardState | undefined`.
- `rateCard(cardId, rating)` — persist a review result; returns `Promise<CardState>`.
- `streak` — `{ current, longest, lastReviewDate }` (DST-safe local-date string).
- `todaysReviewCount` — count of cards reviewed today (local date).
- `dailyGoal` — configurable via `setDailyGoal(n)`.
- `isHydrated` — false until the initial `bulkExport()` resolves; gates render.
- `xpToday` — XP earned in the current local day; resets to 0 at midnight. Rollover
  is detected both on hydration (user opens app next day) and inside `rateCard` (in-session
  midnight crossing).
- `xpAllTime` — monotonic total XP; never decreases.

XP formula lives in `src/mastery/xp.ts` — see `computeXp(rating, difficulty)`. Base XP:
Again=1, Hard=4, Good=8, Easy=10; multiplied by `clamp(difficulty/5, 0.5, 2.0)`; minimum 1.

**Components never read XP off the adapter directly.** Always use `xpToday` / `xpAllTime`
from the hook return. See the hard rule below.

**When to use:** any component or route that needs to display or update mastery
state. Currently only the Spanish practice route (`/guides/spanish/practice`)
uses it.

### `MasteryStorageAdapter` interface

Defined in `src/mastery/adapter.ts`. Methods: `read`, `write`, `listDue`,
`bulkExport`, `bulkImport`, `writeMeta`. All return `Promise`s — even
`LocalStorageMasteryAdapter`, which is synchronous internally. This makes the
Phase 2d cloud-backend swap a single-file addition.

See `src/mastery/ARCHITECTURE.md` for the full contract, LWW semantics, and
sign-in migration story. **Do not import the adapter concrete class directly in
components.** Always go through `useMastery`.

### Pure recommendation function — `src/mastery/recommendation.ts`

A pure, side-effect-free function for use by landing-page widgets (Phase 2b.2):

```ts
import { getRecommendation } from '../mastery';
// or from '../mastery/recommendation' if importing from inside src/mastery/

const rec = getRecommendation({ cardCount, dueCount, reviewedToday });
// rec.kind: 'cold-start' | 'has-due' | 'caught-up'
// rec.message, rec.ctaLabel, rec.ctaTarget
```

Zero React imports, zero adapter imports, zero clock reads. The caller supplies
all inputs. Priority: cold-start (cardCount=0) → has-due (dueCount>0) → caught-up.

### Hard rule: components never touch the adapter directly

The `defaultMasteryAdapter` singleton lives in `src/mastery/index.ts`.
`useMastery.ts` is the only non-test file that imports it.
**No component, guide, or extractor should import `LocalStorageMasteryAdapter`
or any concrete adapter class.** This ensures Phase 2d's cloud-swap is one
file, not a codebase-wide hunt.

XP is persisted via `writeMeta({ xp })` (same adapter method that streak uses).
Components read XP only from `xpToday` / `xpAllTime` on the hook return — never
from `adapter.bulkExport()` directly.

### `ReviewCard` extraction pattern

Each guide that supports mastery has extractors in
`src/guides/{slug}/mastery/extractors/guide{N}.ts`. Each extractor exports a
single `extract(): ReviewCard[]` function. The aggregator
(`src/guides/{slug}/mastery/index.ts`) concatenates all extractor outputs.

```ts
// Extractor skeleton
import type { ReviewCard } from '../../../../mastery/cards';
import { myData } from '../../guides/dataN';

export function extract(): ReviewCard[] {
  return myData.map(item => ({
    cardId: `{slug}-{N}-{stable-slug}`,
    guideId: N,
    guideSlug: '{slug}',
    kind: 'noun-gender',        // must match prompt.kind
    prompt: { kind: 'noun-gender', noun: item.noun },
    answer: item.answer,
    speakText: item.noun,
  }));
}
```

Card IDs must be stable across data reorders (slug from content, not index).
Every extractor in `src/guides/spanish/mastery/extractors/` has a matching
`guide{N}.test.ts` that verifies ID uniqueness, `kind` consistency, and
non-empty answers.

## BYOK Layer

Bring-Your-Own-Key LLM access. Powers the Spanish conversation surface
(`/guides/spanish/conversation`); future conversation surfaces should reuse
the same `getProvider` entry point so they inherit the safety wrappers.

Full architecture, safety levers (daily cap, sliding window, unpriced-model
warning, custom-host confirm), and the "adding a new provider" recipe live
in `docs/byok.md`. Read that before touching `src/byok/`,
`src/components/ApiKeysSection.tsx`, `src/components/CostSection.tsx`, or
the conversation route.

**Hard rule: components never call `makeAnthropicProvider` /
`makeOpenAIProvider` / `makeOpenAICompatibleProvider` directly.** Always
go through `getProvider(id)` from the byok barrel — that's the only call
site that wraps the provider with `withDailyCap`. Bypassing it skips the
USD cap.

## Verifying Changes

Run `npm run check` before considering any change complete. This catches:
- Syntax errors and broken imports (via build)
- Unused variables and hooks violations (via lint)
- Missing guide files or registration gaps (via validate)

## Shared Component Contracts

> **Authoritative source:** As of Phase 3 of the foundations plan, prop contracts are defined as TypeScript interfaces in the `.tsx` component files. The signatures below remain accurate but the `.tsx` source is the canonical type definition.

The authoritative source of truth is always the component file itself. This section is a
quick-reference for anyone generating new guide content.

### `Card({ color, title, children })`

`src/components/Card.tsx` — a content section with a colored header bar.

```tsx
<Card color="#1B5E20" title="Section Title">
  {/* body content */}
</Card>
```

- `color` (string, required) — header background color.
- `title` (string, required) — header text.
- `children` — body content.

---

### `DarkBox({ title, children })`

`src/components/DarkBox.tsx` — a dark-background concept callout used at the top of a guide.

```tsx
<DarkBox title="Key Concept">
  <p>Explanation text…</p>
</DarkBox>
```

- `title` (string, optional) — callout heading. Omit for an untitled callout.
- `children` — body content.

---

### `Insight({ text, emoji })`

`src/components/Insight.tsx` — a tip/hint callout with an emoji.

```tsx
<Insight text="Remember: adjective agrees in gender." emoji="💡" />
```

- `text` (string, required) — tip text.
- `emoji` (string) — leading emoji; defaults to 💡 if omitted.

---

### `SimpleGuide({ items })`

`src/components/SimpleGuide.tsx` — a Q&A / definition list from a data array.

```tsx
<SimpleGuide items={[
  { h: "¿Cómo estás?", b: "How are you?" },
]} />
```

- `items` (array, required) — each item has `h` (heading) and `b` (body).

---

### `ExpandSection({ title, color, children })`

`src/components/ExpandSection.tsx` — a collapsible section with a toggle button.

> **Note:** The prop was renamed from `label` → `title` (Phase 1 infrastructure commit).
> If you encounter old code using `label=`, rename it.

```tsx
<ExpandSection title="Advanced Notes" color="#1B5E20">
  {/* hidden content */}
</ExpandSection>
```

- `title` (string, required) — button label.
- `color` (string) — background color when open; defaults to `#1a1a1a`.
- `children` — revealed content.

---

### `GuideShell({ guidesMeta, guideComponents, categories, catColors, theme, storageKey, sidebarTitle, sidebarSubtitle })`

`src/components/GuideShell.tsx` — the full navigation wrapper. Used only in `index.tsx` files; never inside guide components.

- `guidesMeta` (array) — from `meta.ts`; see Step 2.
- `guideComponents` (array) — from `components.tsx`; must be same order as `guidesMeta`.
- `categories` (array of strings) — from `meta.ts`.
- `catColors` (object `{ [cat]: "#hex" }`) — from `meta.ts`.
- `theme` (object) — from `src/styles/themes.ts`; default `lightTheme`.
- `storageKey` (string) — e.g. `"peliglot-spanish"`.
- `sidebarTitle` (string) — collection name shown in sidebar header.
- `sidebarSubtitle` (string) — e.g. `"30 Interactive Guides"`.

---

### `AlphabetGrid({ letters, letterKey?, nameKey?, filterGroups, detailFields, primaryColor, speakFn?, introTitle, introContent, renderDetail?, borderFn?, badgeFn?, gridProps?, ... })`

`src/components/templates/AlphabetGrid.tsx` — interactive letter grid with filter buttons and a detail panel.

- `letters` (array, required) — letter objects (any shape).
- `letterKey` (string, default `"l"`) — field for the displayed glyph.
- `nameKey` (string, default `"name"`) — field for the small subtitle under each letter.
- `filterGroups` (array `[{ id, label, filterFn }]`) — filter buttons above the grid.
- `detailFields` (array `[{ key, label?, bgColor?, borderColor?, textColor? }]`) — fields shown in the detail panel.
- `primaryColor` (string) — accent color for selection + header.
- `speakFn` (function `(text) => void`) — called on letter tap.
- `speakKey` (string) — field passed to `speakFn`; defaults to `letterKey`.
- `introTitle` / `introContent` — optional `DarkBox` shown above the grid.
- `renderDetail` (function `(letter, { primaryColor, highlightColor }) => JSX`) — fully custom detail panel.
- `borderFn` (function `(letter) => string | null`) — per-letter border override.
- `badgeFn` (function `(letter) => { color } | null`) — small dot badge on letter.
- `gridProps` (object) — extra styles on the grid container (e.g. `{ direction: "rtl" }`).

---

### `VerbConjugation({ pronouns, stem, endings, verb?, meaning?, color, title?, compact? })`

`src/components/templates/VerbConjugation.tsx` — pronoun-based conjugation table.

```tsx
// Full Card mode
<VerbConjugation pronouns={["yo","tú","él"]} stem="habl" endings={["o","as","a"]}
  verb="hablar" meaning="to speak" color="#D84315" />

// Compact mode (no Card wrapper)
<VerbConjugation pronouns={["yo","tú","él"]} stem="habl" endings={["é","aste","ó"]}
  title="Pretérito" color="#B71C1C" compact />
```

- `pronouns` (array, required) — pronoun labels.
- `stem` (string, required) — verb stem.
- `endings` (array, required) — one ending per pronoun.
- `verb` / `meaning` (strings) — shown in the Card header (full mode).
- `color` (string, required) — accent color.
- `title` (string) — used in compact mode instead of verb/meaning.
- `compact` (boolean) — omit the Card wrapper; render a smaller table.

---

### `QuizSection({ items, answerKey?, renderQuestion, optionCount?, color, resultMessages? })`

`src/components/templates/QuizSection.tsx` — multiple-choice quiz with scoring.

> **Always pass `resultMessages`** for non-English collections so the result text
> matches the collection language or is at least appropriate.

```tsx
<QuizSection
  items={items}
  answerKey="answer"
  renderQuestion={(q) => <div>{q.question}</div>}
  optionCount={4}
  color="#0277BD"
  resultMessages={{ high: "¡Excelente!", mid: "¡Bien!", low: "Sigue practicando." }}
/>
```

- `items` (array, required) — quiz items (any shape).
- `answerKey` (string, default `"answer"`) — field name for the correct answer string.
- `renderQuestion` (function `(item) => JSX`, required) — custom question renderer.
- `optionCount` (number, default `4`) — number of choices.
- `color` (string, required) — accent color.
- `resultMessages` (object `{ high, mid, low }`) — result screen text.

---

### `FlashcardDeck({ items, color?, title?, speakFn?, speakKey? })`

`src/components/templates/FlashcardDeck.tsx` — swipeable flashcard deck with got-it / again flow.

```tsx
<FlashcardDeck items={[{ front: "hola", back: "hello" }]} color="#1565C0" />
```

- `items` (array, required) — each item has `front` (displayed before flip) and `back` (shown after flip).
- `color` (string, default `"#1565C0"`) — accent color.
- `title` (string) — optional label above the deck.
- `speakFn` (function `(text) => void`) — called when card flips.
- `speakKey` (string, default `"front"`) — field passed to `speakFn`.

---

### `ProgressRing({ progress, size?, strokeWidth?, color? })`

`src/components/ProgressRing.tsx` — circular SVG progress indicator.

```tsx
<ProgressRing progress={0.75} size={48} color="#2E7D32" />
```

- `progress` (number 0–1, required) — fill fraction.
- `size` (number, default `36`) — SVG width/height in px.
- `strokeWidth` (number, default `3`) — ring thickness in px.
- `color` (string, default `"#2E7D32"`) — ring fill color.
