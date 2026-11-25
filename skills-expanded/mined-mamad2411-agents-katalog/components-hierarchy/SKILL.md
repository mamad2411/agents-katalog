---
name: components-hierarchy
description: React/TypeScript UI component conventions, atomic hierarchy, classNames utility, variant/size dictionaries, polymorphic `as` prop, icon usage, composition slots, and Tailwind styling. Use when authoring or reviewing any `*.tsx` component.

---

# Component Conventions (React + TypeScript + Tailwind)

Use this skill when creating, modifying, or reviewing any UI component (`*.tsx`). It captures an atomic-design hierarchy, a shared `classNames` utility, variant/size dictionaries, polymorphic component patterns, icon usage, composition slots, and Tailwind styling conventions.

> **Notation.** Wherever a path appears as `<components>/`, `<utils>/`, or `<types>/`, treat it as a placeholder. Resolve to the project's existing paths and aliases (`src/components`, `app/components`, `~/lib/utils`, `@/types`, etc.). The **shape** of the convention matters; the exact location does not.

> **Precedence.** These rules apply only where they don't contradict the project's own enforced rules, ESLint / Biome / Prettier configs, `tsconfig`, `CLAUDE.md` / `AGENTS.md`, contributing guides, or stylelint. If a project rule conflicts, the project rule wins; defer to it and (if it makes sense) note the deviation in your PR description.

> **Framework / runtime.** §1-§10 and §13 are **framework-agnostic**, they apply to any React + TypeScript + Tailwind setup, including a plain **Vite + React SPA** with no SSR, no RSC, and no router opinions. §11 (SSR-unsafe components), §12 (multilingual), and parts of §14 (RSC / App Router / Server Components / form actions / `next/*` performance helpers) are **optional** and clearly flagged, skip them on SPAs. The core idioms (atomic hierarchy, `classNames`, variant tokens, dictionaries, polymorphic `as`, slots, React 19 `ref` prop, hooks discipline) are universal.

TRIGGER when: adding a new atom/molecule/organism, refactoring an existing `*.tsx`, wiring up icons, choosing between `as`/variant/size props, or reviewing component PRs.

---

## 1. Atomic Hierarchy

```
<components>/
  atoms/        single-purpose primitives (Button, Input, Text, Card, Badge, ...)
  molecules/    small compositions of atoms (ModalDialog, DropdownButton, ...)
  organisms/    domain-aware blocks (grouped by domain subfolder)
  layouts/      page chrome (NavBar, Footer, SideBar, ...)
  sections/     marketing/landing page sections (Hero, Features, ...)
```

### Rules

- A component **must** import only from its layer or below: `atoms ← molecules ← organisms ← layouts ← sections`. Never go upward.
- Filename pattern: `PascalCase.tsx`. If the project uses a category suffix (e.g. `Button.ui.tsx`), keep it consistent across the layer.
- Each folder has an `index.ts` barrel re-exporting every `.tsx`. Add new files to the barrel in the same change.
- Organisms are typically grouped by domain subfolder (`organisms/<domain>/`) with their own `index.ts`.
- Test files live in `__tests__/` next to the component (e.g. `molecules/__tests__`).
- Domain-aware components live in `organisms/` or below, never in `atoms/molecules`.

### Imports

```ts
// Always root-relative; never "../../"
import { Button, Tooltip, type ButtonProps } from "components/atoms";
import { ModalDialog } from "components/molecules";
import { classNames } from "utils";
import { SizeVariants, ColorVariants, type SizeVariant, type ColorVariant } from "types/variants";
```

Use `import { type Foo }` for type-only imports. Respect the project's import grouping (typically external → internal alias → local).

---

## 2. The `classNames` Utility (NOT `clsx`)

Defined at `<utils>/classNames.ts`:

```ts
export function classNames(...classes: (string | undefined | null | false)[]) {
  return classes.filter(Boolean).join(" ");
}
```

### Rules

- **Never** import `clsx` or `classnames` from npm in a project that uses this convention. Always use the local `classNames` from `<utils>`.
- Pass each Tailwind class as its **own argument**, do not pre-join with spaces.
- Conditional classes: ternary returning a string or `""` / `false`.
- Spread arrays produced by Size/Color dictionaries: `...SizeDict[size]`.
- Always pass the user's `className` prop **last** so consumers can override.

```tsx
className={classNames(
  "inline-flex",
  "items-center",
  "rounded-lg",
  ...SizeDict[size],
  ...ColorDict[variant],
  disabled ? "cursor-not-allowed opacity-50" : "",
  block ? "w-full" : "",
  className          // consumer override, always last
)}
```

> Exception: A component can use a template literal because its class set is trivial. Prefer `classNames` for anything non-trivial, hard limit is 4 css classes applied or more 

---

## 3. Shared Variant Tokens

Defined at `<types>/variants.ts` as **`const` objects + literal-union types** (not TypeScript `enum`, `enum` emits runtime code, is rejected by TS 5.5+ `--erasableSyntaxOnly` and Node's native TS loader, and adds no value here since prop types are string-literal unions anyway):

```ts
export const ColorVariants = {
  primary:  "primary",
  secondary:"secondary",
  plain:    "plain",
  outlined: "outlined",
  danger:   "danger",
  warning:  "warning",
  success:  "success",
  info:     "info"
} as const;
export type ColorVariant = (typeof ColorVariants)[keyof typeof ColorVariants];

export const SizeVariants = {
  tiny:   "tiny",
  small:  "small",
  base:   "base",
  medium: "medium",
  large:  "large"
} as const;
export type SizeVariant = (typeof SizeVariants)[keyof typeof SizeVariants];
```

### Rules

- Use **these tokens** for any prop that conceptually maps to color/intent or size.
- Prop type is the derived `ColorVariant` / `SizeVariant` union (or `keyof typeof ColorVariants` if you prefer the key form). Both are equivalent for string-valued const objects.
- **Never** invent new local size/color string unions when these would fit. If you need a subset, narrow with `Extract<ColorVariant, "info" | "danger" | "warning" | "success">`.
- Default values reference the const object: `size = SizeVariants.medium`, `variant = ColorVariants.primary`.

> **Migrating from `enum`?** A string-valued `const` object with literal-union type is a drop-in replacement at all call sites that already used `keyof typeof X`, no consumer changes needed.

---

## 4. Size & Color Dictionaries

Map variant keys to **arrays of Tailwind classes**, declared at module scope (not inside the component):

```tsx
const SizeDict: Record<SizeVariant, string[]> = {
  tiny:   ["px-3", "py-2", "text-xs"],
  small:  ["px-3", "py-1"],
  base:   ["text-sm", "px-5", "py-2.5"],
  medium: ["text-sm", "px-5", "py-2.5"],
  large:  ["px-2", "py-1"]
};

// Example tokens for a dark-mode-only baseline. For a light/dark project,
// pair every surface/text class with a `dark:` counterpart.
const BadgeColorTypeMap: Record<BadgeType, string[]> = {
  info:    ["bg-blue-900",   "text-blue-300"],
  dark:    ["bg-gray-700",   "text-gray-300"],
  success: ["bg-green-900",  "text-green-300"],
  warning: ["bg-yellow-900", "text-yellow-300"],
  error:   ["bg-red-900",    "text-red-300"],
  main:    ["bg-indigo-600", "text-white"]
};
```

### Color via switch (when conditional / depends on other props)

When color depends on more than the variant key alone (e.g. needs base styles merged in), use a `getXStyle()` closure that returns `string[]`:

```tsx
const getButtonColorStyle = (): string[] => {
  const baseStyle = group ? baseGroupButtonStyle : baseButtonStyle;
  switch (variant) {
    case ColorVariants.primary:
      return [...baseStyle, "bg-indigo-700", "hover:bg-indigo-900", "focus:ring-indigo-900"];
    case ColorVariants.danger:
      return [...baseStyle, "bg-red-700", "hover:bg-red-900", "focus:ring-red-900"];
    case ColorVariants.plain:
      return ["text-white"];
    default:
      return [...baseStyle, "text-white", "bg-slate-700", "hover:bg-slate-600"];
  }
};
```

### Rules

- Dict name: `SizeDict`, `ColorDict`, or `XColorTypeMap`, singular, scoped to the component file.
- Values are `string[]` so they can be spread (`...SizeDict[size]`).
- Static base class arrays use `SCREAMING_CASE` or `baseXStyle` and live above the dict.
- Prefer dictionaries over switches when the lookup is purely keyed; reserve `switch` for cases that need to combine bases or share fallthroughs.

---

## 5. Standard Prop Conventions

Every visual component supports:

| Prop          | Type                                  | Notes                                        |
| ------------- | ------------------------------------- | -------------------------------------------- |
| `className`   | `string` (optional)                   | Always merged **last** in `classNames(...)`  |
| `variant`     | `ColorVariant`                        | Default `"primary"` (or local subset)        |
| `size`        | `SizeVariant`                         | Default `SizeVariants.medium` or `.base`     |
| `disabled`    | `boolean`                             | Adds `cursor-not-allowed opacity-50`         |
| `block`       | `boolean`                             | Adds `w-full`                                |
| `as`          | discriminated literal union           | See §7 Polymorphism                          |
| `children`    | via `PropsWithChildren<...>`          | Default rendering slot                       |
| `<Slot>`      | `ReactNode` (PascalCase prop name)    | Composition slots, see §8                   |

### Native attribute extension

Always extend the matching native HTML attributes interface so the component is a drop-in:

```tsx
export interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: ColorVariant;
  size?: SizeVariant;
  group?: boolean;
  block?: boolean;
}

export interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  label: string;
  labelVisible?: boolean;
  invalid?: boolean;
  inputSize?: SizeVariant;
}
```

Spread `...attributes` / `...inputProps` onto the underlying element so handlers, `aria-*`, `data-*`, `name`, `id`, etc., all just work.

### Discriminated optional groups

When a feature requires multiple props together, model it as a discriminated union, not multiple optional props:

```tsx
type BadgeProps = {
  type?: BadgeType;
  size?: SizeVariant;
} & (
  | { handleRemove: (id: string) => void; badgeId: string; removeTextStyle: string }
  | { handleRemove?: never; badgeId?: never; removeTextStyle?: never }
);
```

This forces consumers to provide either the whole group or none of it.

### `ref` as a regular prop (React 19)

`ref` is a normal prop on function components, **do not use `forwardRef` in new code**. Type it as `Ref<HTMLElement>` on the props interface:

```tsx
export interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  ref?: Ref<HTMLButtonElement>;
  variant?: ColorVariant;
  size?: SizeVariant;
}

export function Button({
  ref,
  variant = "primary",
  size = SizeVariants.medium,
  className,
  children,
  ...rest
}: PropsWithChildren<ButtonProps>) {
  return <button ref={ref} {...rest}>{children}</button>;
}
```

Migrate existing `forwardRef` atoms opportunistically when you touch them. Use callback refs (with optional cleanup return) when the parent needs to react to mount/unmount.

---

## 6. Defaults & `Readonly`

- Provide defaults in the destructuring signature: `variant = "primary"`, `size = SizeVariants.medium`, `bold = false`.
- Wrap props in `Readonly<PropsWithChildren<...>>` when the component does not mutate its props, most components qualify.

---

## 7. Polymorphism via `as` Prop

When a component should render as different elements depending on context (link vs button vs section), use a **discriminated `as` union** rather than `ElementType`:

```tsx
type CardProps = (
  | (ButtonHTMLAttributes<HTMLButtonElement> & { as: "button" })
  | (AnchorHTMLAttributes<HTMLAnchorElement>  & { as: "a" })
  | (HTMLAttributes<HTMLElement>              & { as: "section" })
) & PropsWithChildren<{
  size?: SizeVariant;
  variant?: ColorVariant;
  // ...other shared props
}>;

export function Card({ as, children, ...otherProps }: CardProps) {
  const CardWrapper: ElementType = as ?? "section";
  return <CardWrapper {...otherProps}>{children}</CardWrapper>;
}
```

Each branch carries the **correct** HTML attribute set, so consumers get autocompleted `href` only when `as="a"` and `onClick` typed for the right event when `as="button"`.

### Rules

- Limit `as` to a small set of literals (`"button" | "a" | "section"`). Don't accept arbitrary `ElementType` at the prop boundary, that defeats type narrowing on the union.
- Pick a default branch (typically `"section"` or `"div"`) via `as ?? "section"` and assign to a `Capitalized` local typed as `ElementType` so JSX accepts it.
- Native attribute interface **must** match the literal (`"a"` ↔ `AnchorHTMLAttributes<HTMLAnchorElement>`).

---

## 8. Composition Slots

For non-trivial components, expose **named slot props** of type `ReactNode` instead of cramming everything into `children`. Convention: slot prop names are **PascalCase**.

```tsx
interface ModalDialogProps {
  Title?: ReactNode;     // header content
  Actions?: ReactNode;   // footer content
  visible: boolean;
  // ...
}

<ModalDialog
  visible={open}
  Title={<h2>Confirm</h2>}
  Actions={
    <>
      <Button variant="plain" onClick={cancel}>Cancel</Button>
      <Button variant="danger" onClick={confirm}>Delete</Button>
    </>
  }
>
  Are you sure?
</ModalDialog>
```

### Rules

- PascalCase slot prop names (`Title`, `Actions`, `TitleElement`), distinguishes them from primitive props.
- `children` is reserved for the body / primary content.
- For compound components (`Tabs`/`Tab`, `Accordion`/`AccordionItem`), share coordination state via a **React Context** scoped to the parent, read with `useContext` or React 19's `use()`. This is what Radix, Headless UI, React Aria, shadcn/ui, and the React docs all do. Reach for `Children.map` + `cloneElement` only as a last resort when you specifically need positional info (`isFirst` / `isLast`) and the children are guaranteed to be direct, non-wrapped, non-conditional `<Tab>` elements.

---

## 9. Icons

Two parallel systems, pick the right one per case.

### 9.1 FontAwesome (default)

```tsx
import { FontAwesomeIcon, type FontAwesomeIconProps } from "@fortawesome/react-fontawesome";
// Use whichever icon package(s) the project licenses.
import { faCheck, faTimes, faSpinner } from "<primary-icon-pkg>";
import { faPlus } from "<secondary-icon-pkg>";

<FontAwesomeIcon icon={faCheck} className="text-green-400" />
<FontAwesomeIcon icon={faSpinner} spin />
<FontAwesomeIcon icon={faTimes} size="lg" />
```

### Rules

- Pick one default icon set and use it everywhere. Use a secondary set only when the default lacks the right glyph or the alt set is the right semantic.
- Don't mix paid and free tiers of the same library, pick one source per project.
- Forward icon props through wrappers via `FontAwesomeIconProps["icon"]` and `FontAwesomeIconProps["size"]`:

  ```tsx
  interface ButtonIconTooltipProps {
    icon: FontAwesomeIconProps["icon"];
    size?: FontAwesomeIconProps["size"];
  }
  ```

- Color via Tailwind `className` (`"text-green-400"`, `"text-red-400"`), not the FontAwesome `color` prop.
- For loading states use the library's spin variant (e.g. `<FontAwesomeIcon icon={faSpinner} spin />`). Don't combine `spin` with `pulse`, `pulse` is FA4's legacy 8-step jump and produces a stuttery animation when paired with `spin`.
- When an icon-only button needs accessible text, add `<span className="sr-only">{label}</span>`.

### 9.2 Inline SVG illustrations

Brand illustrations and bespoke graphics live in `<components>/atoms/icons/` as React components. They:

- Export a zero-prop function returning a single `<svg>` JSX literal.
- Are **not** parameterized by size/color, they're large brand SVGs.
- Are imported from a separate barrel from regular atoms.

Use these for marketing/illustration only. For action/status icons always use the icon library.

---

## 10. Styling Conventions

- **Tailwind only**, no CSS Modules, no styled-components, no inline `style` except for genuinely dynamic values (e.g. `objectFit`, computed colors).
- **Pick a theme baseline.** If the app is dark-mode-only, default to `bg-gray-700/800/900`, `text-white`, `text-gray-300/400`, `border-gray-600/700` and don't add `dark:` prefixes. If the app supports both themes, define the baseline in light tokens and pair every surface/text token with a `dark:` counterpart.
- **Brand color, pick one of two Tailwind-native paths and stick to it:**
  1. **Use a built-in palette directly** (`indigo`, `emerald`, `blue`, `slate`, …). Simplest, matches the Tailwind UI / Tailwind Plus convention. Examples in this doc use `indigo`.
  2. **Extend the theme** with a project-named palette via `theme.extend.colors.<name>` (v3) or `@theme { --color-<name>-50…950: … }` (v4). Common names: `primary`, `accent`, or the brand's own name. Avoid `brand` only if your design system already uses it for something else.

  Whichever path you pick, primary actions use the `700` / `900` shades: `bg-<palette>-700` / `hover:bg-<palette>-900` / `focus:ring-<palette>-900`. Don't mix paths within one project.
- Focus states: `focus:outline-none focus:ring-4 focus:ring-<color>`.
- Disabled state: `cursor-not-allowed opacity-50`.
- Radius: `rounded-lg` for buttons/cards/dialogs, `rounded-full` for pills/avatars, `rounded` for tags.
- Spacing scale anchors: padding `px-5 py-2.5` (medium control), `p-2.5` (input), `p-4 md:p-6` (modal section).
- Typography: prefer a `Text` atom over hand-written `text-2xl font-bold` on raw `<h2>` in new code, `<Text as="h2" variant="headline" bold>`.

---

## 11. SSR-unsafe components (optional)

**Plain Vite SPAs and other SPA-only setups can skip this entire section**, there's no server-render pass, so `window` / `document` access at module load is harmless.

For SSR / SSG / RSC frameworks, any component depending on libraries that touch `window` / `document` at module load (`leaflet` / `react-leaflet`, MapLibre, certain charting libs, etc.) must be loaded as a client-only chunk:

```tsx
// Next.js
const Map = dynamic(() => import("components/molecules/Map").then((m) => m.Map), {
  ssr: false
});

// TanStack Start
const Map = lazy(() => import("components/molecules/Map").then((m) => ({ default: m.Map })));
// ...render under <ClientOnly fallback={<MapSkeleton />}>{<Map />}</ClientOnly>

// Plain React.lazy works too, just don't render the lazy component on the server pass.
```

Such components should also be excluded from any barrel that is imported on the server.

---

## 12. Multilingual Text (optional)

Skip if the project is single-language.

If the project stores i18n content as a per-language map (`{ text: { en, es, ... } }`), pick one language as the **required** default and treat all others as nullable. Inside components, read the current language from the project's i18n source (Redux, Context, `next-intl`, `react-i18next`, etc.) and **always fall back** to the required language, never render `undefined`.

```tsx
// Shape only, wire to whichever i18n source the project actually uses.
const language = useCurrentLanguage();
const label = entity.text[language] ?? entity.text[DEFAULT_LANGUAGE];
```

If the project uses message-catalog i18n (`t("key")`) instead of per-record maps, this section does not apply, use the catalog API.

---

## 13. Worked Example, A Button Wrapper Atom (React 19)

```tsx
import { type PropsWithChildren, type ButtonHTMLAttributes, type Ref } from "react";
import { FontAwesomeIcon, type FontAwesomeIconProps } from "@fortawesome/react-fontawesome";

import { Button, type ButtonProps } from "components/atoms";
import { ColorVariants, SizeVariants, type SizeVariant } from "types/variants";
import { classNames } from "utils";

// Reuses the base `Button` atom (defined in §5).
export interface IconButtonProps extends Omit<ButtonProps, "size" | "ref"> {
  ref?: Ref<HTMLButtonElement>;
  icon: FontAwesomeIconProps["icon"];
  iconPosition?: "left" | "right";
  size?: SizeVariant;
  label: string; // sr-only fallback when icon-only
}

const IconGapDict: Record<SizeVariant, string> = {
  tiny: "gap-1",
  small: "gap-1.5",
  base: "gap-2",
  medium: "gap-2",
  large: "gap-2.5"
};

export function IconButton({
  ref,
  icon,
  iconPosition = "left",
  size = SizeVariants.medium,
  variant = ColorVariants.primary,
  label,
  children,
  className,
  ...rest
}: PropsWithChildren<IconButtonProps>) {
  return (
    <Button
      ref={ref}
      size={size}
      variant={variant}
      className={classNames("inline-flex", "items-center", IconGapDict[size], className)}
      {...rest}
    >
      {iconPosition === "left" ? <FontAwesomeIcon icon={icon} /> : null}
      {children ? <span>{children}</span> : <span className="sr-only">{label}</span>}
      {iconPosition === "right" ? <FontAwesomeIcon icon={icon} /> : null}
    </Button>
  );
}
```

This example demonstrates: React 19 `ref` as a normal prop, native attribute extension via `Omit<ButtonProps, "size" | "ref">`, FontAwesome icon prop forwarding, size dictionary, accessible fallback label, no manual memoization (compiler handles it), and `className` merged last.

---

## 14. React 19 Patterns

Author components against **React 19**. The React Compiler handles most memoization, the new ref/form/transition APIs replace several legacy patterns, and `forwardRef` is no longer needed for new components.

> **Applies to any React 19 setup**, Vite SPA, Next.js (App or Pages Router), Remix, TanStack Start, etc. Subsections labeled *"App Router / RSC only"* are framework-specific; skip them on a plain Vite SPA. Everything else (compiler, refs, hooks, `use()`, accessibility, performance, TypeScript) is universal.

### Compiler-first mindset

> **Applies only if the React Compiler is actually enabled in the build** (`babel-plugin-react-compiler` wired into Babel/SWC, or the Next.js `experimental.reactCompiler` flag, etc.). On a vanilla React 19 project *without* the compiler, the rules below will produce real perf regressions, keep your existing memoization until the compiler is turned on.

- With the compiler enabled, components and hook outputs are auto-memoized. **Stop hand-rolling `useMemo` / `useCallback` / `React.memo`** for normal cases, write straightforward code and let the compiler optimize it.
- Only reach for manual memoization when:
  - The compiler **bails out** (verified via the `react-compiler-runtime` warnings or React DevTools "✨" badge absence) and a profiler shows a real regression.
  - You're integrating with a non-compiled third-party that requires referential stability.
- Inline object/array/function props as children **are fine** under the compiler, don't contort code to hoist them.
- Keep components **idempotent** (the compiler assumes purity): no mutation of props/state in render, no `Math.random()` / `Date.now()` in render bodies, no side effects outside event handlers / effects / refs. These purity rules also matter under React 19 Strict Mode regardless of the compiler.

### `ref` as a regular prop (drop `forwardRef`)

In React 19, `ref` is a normal prop on function components. **Do not use `forwardRef` in new code.** Migrate atoms opportunistically.

```tsx
// React 19 idiom, no forwardRef
export interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  ref?: Ref<HTMLButtonElement>;
  variant?: ColorVariant;
  size?: SizeVariant;
}

export function Button({
  ref,
  variant = "primary",
  size = SizeVariants.medium,
  className,
  children,
  ...rest
}: PropsWithChildren<ButtonProps>) {
  return (
    <button ref={ref} className={classNames(/* ... */, className)} {...rest}>
      {children}
    </button>
  );
}
```

- Use **callback refs with cleanup** (React 19 supports a returned cleanup function) for DOM measurement / external library attach:
  ```tsx
  <div ref={(node) => {
    if (!node) return;
    const obs = new ResizeObserver(/* ... */);
    obs.observe(node);
    return () => obs.disconnect();
  }} />
  ```
- `useImperativeHandle` is still valid when exposing a curated handle, but prefer plain `ref` forwarding.

### Hooks discipline

- Treat `useEffect` as a last resort. Before reaching for it, ask:
  - Can this be derived during render? (compute from props/state)
  - Can this be done in an event handler?
  - Is it server state? → Use the project's data-fetching layer (TanStack Query, SWR, RSC `await`, etc.).
  - Is it shared UI state? → Use the project's existing store (Redux, Zustand, Context). Don't introduce a new mechanism for trivial cases.
- Use **`useId()`** for label/`htmlFor`/`aria-describedby`/`aria-labelledby` pairings. Never roll counters or `Math.random()` ids.
- Use **`useSyncExternalStore`** for non-React stores (`matchMedia`, custom event buses). Don't reimplement with `useEffect` + `useState`.
- Use **`useDeferredValue`** / **`useTransition`** to keep input responsive when derivation/list filtering is expensive. Wrap the derivation, not the input.
- `useState` setter accepts a function for derived updates: `setCount((c) => c + 1)`, required when the next value depends on the previous and updates may batch.

### `use()`, read promises and context conditionally

React 19's `use()` reads a promise or context **and can be called inside conditionals/loops** (unlike other hooks).

```tsx
import { use, Suspense } from "react";

function Title({ promise }: { promise: Promise<{ title: string }> }) {
  const data = use(promise); // suspends until resolved
  return <h1>{data.title}</h1>;
}

// Wrap with Suspense for loading UI:
<Suspense fallback={<SkeletonCard />}>
  <Title promise={titlePromise} />
</Suspense>
```

- Prefer the project's data-fetching layer for client data caching. `use()` is for promises produced by the server (RSC) or for one-shot client work that shouldn't go through a cache.
- `use(SomeContext)` is the new way to read context conditionally; `useContext` still works for unconditional reads.

### Actions, transitions, and form hooks

> **`useActionState` / `useFormStatus` / `useOptimistic` are usable in any React 19 environment** (Vite SPA included), they don't strictly require RSC. They shine brightest with Server Actions, but in a plain SPA you can pass any `(state, formData) => Promise<state>` reducer and get the same pending/state ergonomics. **`useTransition`** is fully framework-agnostic.

In a form, prefer the React 19 primitives over hand-rolled loading state.

- **`useActionState`**, bind a `(state, formData) => newState` reducer to a `<form>`; React handles pending state and (in RSC frameworks) progressive enhancement.
  ```tsx
  // "use client" is needed only in RSC frameworks (Next.js App Router, etc.).
  // Plain SPA (Vite, etc.): drop the directive, the file is already a client module.
  import { useActionState } from "react";

  export function Subscribe({ action }: { action: (s: State, fd: FormData) => Promise<State> }) {
    const [state, submit, isPending] = useActionState(action, { error: null });
    return (
      <form action={submit}>
        <input name="email" required />
        <Button type="submit" disabled={isPending}>Subscribe</Button>
        {state.error ? <Alert variant="danger">{state.error}</Alert> : null}
      </form>
    );
  }
  ```
- **`useFormStatus`**, read the parent `<form>`'s pending state from a child without prop-drilling.
  ```tsx
  import { useFormStatus } from "react-dom";
  export function SubmitButton({ children }: PropsWithChildren) {
    const { pending } = useFormStatus();
    return <Button type="submit" disabled={pending}>{children}</Button>;
  }
  ```
- **`useOptimistic`**, show optimistic UI while a mutation is in flight.
  ```tsx
  const [optimisticItems, addOptimistic] = useOptimistic(items, (state, next: Item) => [...state, next]);
  ```
- **`useTransition`**, wrap async non-urgent updates: `startTransition(async () => { await save(); /* navigate or refresh */ })`.

> If the project has both an App Router and a Pages Router (or equivalent split), apply these hooks where the React 19 runtime is wired up. For non-React-19 trees, drive submit buttons off the project's existing mutation state (e.g. `mutation.isPending`).

### Server vs Client Components, *Next.js App Router / RSC frameworks only*

Skip entirely if the project is a plain SPA (Vite, etc.) or Pages-Router-only, every component is a Client Component by definition; the `"use client"` / `"use server"` directives don't apply.

- Default App Router files are **Server Components**, no hooks, no event handlers, no browser APIs. They can `await` data and render directly.
- Add `"use client"` only when the file uses hooks, event handlers, browser APIs, or imports a client-only lib.
- Keep `"use client"` boundaries as **leaves**. Server Components can render Client Components, but Client Components can only render Server Components passed as `children`/slot props (`<ClientShell>{serverNode}</ClientShell>`).
- **Server Actions** (`"use server"`) live in App Router action files only. Plain async functions in your data layer are not Server Actions, don't add the directive there.

### Suspense & errors

- Wrap lazy-loaded chunks (`React.lazy`, `next/dynamic`, framework equivalents), `use()` promises, and data-loading subtrees in `<Suspense fallback={<SkeletonCard />} />`, never bare spinners.
- Wrap risky subtrees (map, payment iframe, third-party widgets) in an **error boundary** that reports to the project's error-tracking tool (Sentry, etc.). React 19's `onUncaughtError` / `onCaughtError` `createRoot` options can centralize reporting.
- Don't throw promises manually, let `use()`, the lazy loader, or the data-fetching layer manage suspension.

### Document metadata, stylesheets, preloading

- React 19 hoists `<title>`, `<meta>`, `<link>`, and `<style>` rendered inside components into `<head>`, use this for per-component metadata in any framework, including Vite SPAs.
- For preconnects / preloads, use the `react-dom` resource APIs: `import { preconnect, preload, prefetchDNS } from "react-dom"`. Call from event handlers, or (in RSC frameworks) Server Components, not in render of Client Components.

### Accessibility (enforced)

- Every interactive element has an accessible name: visible label, `aria-label`, or `<span className="sr-only">…</span>` (icon-only buttons).
- `<button>` always has explicit `type="button" | "submit" | "reset"`, default to `"button"`.
- Modals use native `<dialog>`, keep `aria-modal`, `aria-label`, and `Escape` handling.
- Focus rings are mandatory: `focus:outline-none focus:ring-4 focus:ring-<color>`, never strip without replacement. `:focus-visible` is preferred over `:focus` for ring states.
- Honor reduced motion: gate animations behind `motion-safe:` or `prefers-reduced-motion` when using motion libraries.
- Color is never the sole signal, pair status colors with an icon or label.
- Image components require `alt`; for decorative images pass `alt=""` explicitly.

### Performance

- For content images, use the framework's optimized image component if there is one (`next/image`, `unpic`, `@unpic/react`, etc.). On a plain Vite SPA without such a component, raw `<img>` is acceptable, pair it with `loading="lazy"`, explicit `width`/`height` to avoid CLS, and `decoding="async"`.
- Lazy-load below-the-fold organisms and trees that touch `window`, `document`, or heavy client-only libs. Use the framework's dynamic-import helper if it has one (`next/dynamic`), otherwise plain `React.lazy(() => import("./Heavy"))` + `<Suspense>` works in any setup.
- **Named-import** icons (and other tree-shakeable libs), namespace imports defeat tree-shaking.
- Trust the compiler for memoization. Profile before manual `memo`.
- Avoid synchronous expensive work in render, wrap with `useDeferredValue` or move to a worker.
- Stable list keys, never array index for reorderable / filterable / paginated lists.

### TypeScript ergonomics

- Recommended `tsconfig`: `strict` + `noUncheckedIndexedAccess`, array/dict access is `T | undefined`. Guard with `?? fallback` or `if`.
- Prefer `ReactNode` for children/slot props; `ReactElement` when you need to `cloneElement`.
- `PropsWithChildren<T>` for children; `Readonly<PropsWithChildren<T>>` when the component does not mutate.
- Type event handlers explicitly: `MouseEventHandler<HTMLButtonElement>`, `ChangeEventHandler<HTMLInputElement>`. Never `(e: any) => void`.
- Discriminated unions over `Partial<T>` when props travel together (see §5).
- `ref` prop type is `Ref<T>` (which is `RefObject<T> | RefCallback<T> | null`). Don't use the legacy `LegacyRef` / `MutableRefObject`.

### State colocation

- Lift state only as far as needed.
- Shared UI state across siblings → the project's existing store. Don't spin up a new context for trivial toggles.
- Never mirror server data into a client store, the data-fetching layer is the cache.

---

## 15. Anti-Patterns (Never Do)

- ❌ `import clsx from "clsx"` in a project that has the local `classNames`, use `classNames` from `"utils"`.
- ❌ Pre-joined class strings: `classNames("flex items-center")`. Each class is its own arg.
- ❌ Inventing local `"sm" | "md" | "lg"` size unions, use `SizeVariants`.
- ❌ Inventing local color string unions, use `ColorVariants` (or narrow with `Extract<>`).
- ❌ `as: ElementType`, use a discriminated literal union.
- ❌ Mixing icon libraries within a single project without a documented reason.
- ❌ Setting icon color via `color="red"`, use Tailwind `className`.
- ❌ Domain logic / data fetching inside `atoms/` or `molecules/`. Hooks belong in organisms or pages.
- ❌ Adding `dark:` Tailwind classes in a dark-only project (or omitting them in a light/dark project).
- ❌ Skipping the `__tests__` directory or barrel update when adding a new component.
- ❌ Calling raw `fetch()` from a component, use the project's data-fetching layer.
- ❌ Passing `className` before `...SizeDict[size]` / `...ColorDict[variant]` in `classNames(...)`, consumer override must come last.
- ❌ `forwardRef` in **new** components, `ref` is a regular prop in React 19.
- ❌ Hand-rolled `useMemo` / `useCallback` / `React.memo` without a profiler showing a regression, let the React Compiler do its job.
- ❌ `useEffect` for derived values, event-handler work, or server data fetching.
- ❌ Wrapping form-hook usages with `"use client"` in non-RSC frameworks (plain Vite SPA, Pages Router, etc.), the directive is meaningless there. `useFormStatus` / `useActionState` / `useOptimistic` work in any React 19 environment.
- ❌ Adding `"use server"` to plain async data-layer functions, only RSC framework action files take that directive.
- ❌ Class components, legacy lifecycle methods, `defaultProps` on function components, `propTypes`.
- ❌ Reading `window` / `document` / `localStorage` at module scope or in render *in any code path that runs on the server* (SSR / SSG / RSC), guard with `useEffect`, callback ref, or a client-only dynamic import. (Pure SPAs without SSR are fine to read these freely, but `useSyncExternalStore` is still cleaner for reactive sources like `matchMedia`.)
- ❌ Array index as `key` for reorderable / filterable lists.
- ❌ Hand-rolled ids (`Math.random()`, counters) for label/aria associations, use `useId()`.
- ❌ Namespace imports of icons, always named imports.
- ❌ Stripping `:focus` / `:focus-visible` rings without an accessible replacement.
- ❌ `<button>` without an explicit `type`.
- ❌ Hidden interactive elements (`<div onClick={...}>` without `role` + keyboard handlers), use `<button>`.
- ❌ Mutating props or state during render (breaks compiler assumptions and Strict Mode).
- ❌ `LegacyRef` / `MutableRefObject` in prop types, use `Ref<T>`.

---

## 16. New Component Checklist

When adding `<components>/<layer>/Foo.tsx`:

1. Filename matches the project's convention; prefer **named** `export function Foo` over default exports.
2. Props interface extends matching native `HTMLAttributes<...>`; include `className?` and `variant`/`size` if visual.
3. Module-scope `SizeDict` / `ColorDict` if the component varies by enum.
4. `classNames(...)` with each Tailwind class as own arg; `className` prop merged last.
5. Spread `...rest` props onto the underlying element.
6. Default values in the destructuring signature.
7. Use `PropsWithChildren<...>` (and `Readonly<...>`) where appropriate.
8. Add export line to the layer's `index.ts` barrel.
9. If the layer/component has nearby tests, add a `__tests__/Foo.test.tsx`.
10. For polymorphic components, use a discriminated `as` union.
11. If on React 19, use `ref` as a regular prop (no `forwardRef`).
