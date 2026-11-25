---
name: component-playground
description: Mount one shared component on an isolated, dev-gated route with knob-style controls generated from its real prop declarations, so edge cases can be probed without touching a real page (Storybook-lite). Framework-adaptive — Vue / React / Svelte / Angular. Invoke on "test this component in isolation", "play with props", "see what X looks like with Y". Do NOT invoke when the repo already has Storybook / Histoire / Ladle or any *.stories.* file — write a story there instead; a second explorer is the anti-pattern. Not for a component already mounted in a real page (that is verify-with-playwright) and not for regression baselines (visual-check).
kind: skill
pack: frontend
allowed-tools: [Read, Write, Edit, Grep, Glob, Bash]
---

# Component Playground

Mounts a single component with prop controls on an isolated, dev-only route. Storybook-lite — no dependency, disposable.

## Premise

**Probe the component in isolation, in the project's own stack — never impose a framework or UI kit the repo doesn't use.** The playground must be built from the component's real prop/emit declarations (read them, don't guess) and wired with the project's own shared input components and router. A playground that hard-codes a different framework's controls is worse than none. Cite the component's actual props at `<file:line>` when generating controls.

**Prior art wins — check before you scaffold.** This skill is Storybook-lite, and "lite" only earns its keep when the heavyweight is absent. If the repo already has a component-explorer (`.storybook/`, `histoire.config.*`, `.ladle/`, or a `*.stories.*` file beside the component), **HALT and route to a story** — write or extend the story instead. Scaffolding a parallel `_playground/` route beside an existing Storybook creates two places to look at the same component, and the one nobody wires into CI rots first. Say which explorer you found, at `<file:line>`, when you halt.

## Adapt to the codebase

Detect the component framework + the shared input components + where dev-only routes live, and mirror them:

| Framework | Read props from | Emits / events | Prop-control widget (prefer the project's shared inputs) |
|---|---|---|---|
| **Vue 3** | `defineProps<{…}>()` | `defineEmits<{…}>()` | its `<Switch>` / `<InputText>` / `<InputNumber>` / `<Select>` / `<Textarea>` (or the UI kit in use) |
| **React** | the props `type` / `interface` (or `Props` param) | callback props (`onX`) | the design-system `Switch` / `Input` / `NumberInput` / `Select` / `<textarea>` |
| **Svelte 5** | `$props()` (runes) or `export let` (legacy) | `createEventDispatcher` / callback props | project inputs or native `<input>` |
| **Angular** | `input()` signals or `@Input()` | `output()` / `@Output()` | project inputs / Angular Material |

Control mapping by prop type (same across frameworks): `boolean` → toggle/switch · `string` → text input · `number` → number input · enum/union → select · object/array → JSON `<textarea>`. Log every emit/event to a visible list so the user sees them fire.

## Location

- Put playgrounds in the project's dev-only routes area — reuse an existing `_dev/` / `_playground/` / `dev/` convention if one exists; otherwise create `<routes-root>/_playground/` next to the app's routes.
- Route path `/_playground/<kebab-component-name>`; **gate behind the framework's dev flag** (`import.meta.env.DEV` for Vite/Nuxt/SvelteKit, `process.env.NODE_ENV !== 'production'` for Next/Angular) so it never ships.
- Register the playground route in the project's router the same way real routes are registered.

## Steps

0. **Prior-art check (mandatory).** `ls -d .storybook .ladle histoire.config.* 2>/dev/null` and `rg --files -g '*.stories.{ts,tsx,js,jsx,mjs,svelte,mdx}' -g '*.story.{vue,svelte}' -g '!**/node_modules/**' . | head -5`. Any output → HALT and route to a story; do not scaffold. `rg --files` takes **globs**, not a pattern: given a regex beside `--files`, ripgrep reads it as a path, exits 2 ("No such file or directory") and prints nothing, so the halt never fired on a repo full of stories.
1. Resolve `$COMPONENT` (path or name) and **read it** to extract the real prop + emit/event declarations (see the Adapt table for where they live).
2. Generate a playground page that: imports the component; binds a reactive/stateful `bindings` object built from the props; renders one control per prop (mapped by type, using the project's shared inputs); and logs each emit/event to a list beside the component.
3. Register the route (dev-gated) in the project's router.
4. Run `visual-check` on the playground route to confirm it renders, and drive one interaction plus one a11y assertion (keyboard reach + accessible name on the primary control) — a playground that has never been interacted with proves only that the import resolved. **Carry `visual-check`'s artifact path into the Output block.** That skill halts unless every row cites a frame path, so a `PASS` reported here with no path is a claim it never made; a `_playground/` route also has no baseline, so the run generates one rather than verifying against one, and the frame is the whole of the evidence.
5. Emit the Output block below and share the URL.

## Output

```
component-playground — <ComponentName>

Prior art:   none found (no .storybook/ .ladle/ histoire.config.* / *.stories.*)
Source:      src/components/orders/StatusChip.vue:12-28  (6 props, 2 emits read from source)
Controls:    variant (select: neutral|success|danger) · label (text) · dense (switch)
             count (number) · icon (text) · meta (JSON textarea)
Events:      logged to the panel beside the component — click, update:modelValue
Route:       /_playground/status-chip   (dev-gated via import.meta.env.DEV)
Render:      visual-check PASS — 1 interaction driven, accessible name asserted
             .playwright-mcp/playground-status-chip.png   (artifact path — required)
Cleanup:     disposable; delete once the prop API stabilizes
```

## False positives / gotchas

- **A repo with no explorer is not the same as a repo that rejected one.** If a `*.stories.*` file exists anywhere, the project has already chosen — route there even if the target component has no story yet.
- **Import `_playground/` from nowhere except the router.** It is disposable; any real code importing it makes it permanent by accident.
- **Use the project's shared input components** so controls feel native (fall back to native `<input>` only if there is no shared kit) — a playground built from a foreign UI kit teaches the wrong shape.
- **Gate behind the dev flag** — a playground route reachable in production is a leak of internal component surface, and the bundle cost ships with it.
- **Union/enum props inferred from TypeScript are only as good as the type** — a `string`-typed prop that is really an enum renders as a free-text box. Read the component's usage before trusting the control mapping.
- **Delete the playground once the component's API stabilizes.** A stale playground bound to removed props is a broken dev route nobody owns.

## Failure modes

- Props invented because the declaration was hard to parse → controls that do not correspond to the component. Read the source or halt.
- A parallel playground scaffolded next to an existing Storybook → two explorers, one maintained. This is the failure the step-0 halt exists to prevent.
- Playground route registered outside the dev gate → ships to production.
- Playground registered in the router but never rendered → the skill reports success on code that was never executed; step 4 is not optional.

## When to run

- A shared primitive's edge cases (long label, empty state, RTL, extreme counts) need probing and the repo has **no** component explorer.
- Before extracting a prop into a wrapper API — see how the component behaves across the prop's full range first.
- `/add-component` routed here from its intent gate ("test in isolation", "play with props").

## Related

- `visual-check` — renders the playground route and owns the render harness contract (session file, gitignored artifact dir, blocked-render HALT).
- `verify-with-playwright` — the ad-hoc live-drive sibling for a component already mounted in a real page.
- `/add-component` — the command that scaffolds the component this skill probes; its intent gate is the main entry point.
- `@design-system-guardian` *(ui-ux pack, when co-installed)* — owns whether the primitive should exist at all and whether its variants belong to the system. This skill only looks at one component; it makes no system-level claim.
- `/setup-storybook` — where a repo goes when it wants the heavyweight instead: Storybook, a story per shared component, and the Storybook MCP. On a repo that already has Storybook, this skill's step-0 halt routes a missing story there (UPDATE mode writes only the gap).

## Halt conditions

- Halt if the component's props/emits cannot be read from source — do not invent controls for props you have not seen at `<file:line>`.
- Halt if the generated playground uses a framework or UI kit the project does not use (mirror the detected stack from the Adapt table).
- Halt if no dev-only gating is applied to the route (would leak the playground to production).
- Halt if the repo already ships a component explorer (`.storybook/`, `histoire.config.*`, `.ladle/`, any `*.stories.*`) — route to a story instead of scaffolding a second explorer. Name the file you found.
- Halt if the playground route was generated but never rendered — an unrendered playground is unverified code, not a delivered probe.
- Halt if the render is reported as PASS with no artifact path from `visual-check`. Its contract is that every row cites a frame or a "no diff"; a bare PASS relayed through this skill launders a claim across a boundary.
