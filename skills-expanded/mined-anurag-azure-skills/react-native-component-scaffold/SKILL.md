---
name: "react-native-component-scaffold"
description: "Translate Figma design_source into Expo Router screens: theme, FigmaCanvas layouts, components, API hooks, navigation wiring. Use when scaffolding screens from Figma for family-plan or similar epics."
version: 2
created: "2026-06-27"
updated: "2026-07-06"
---

# React Native Component Scaffold (Figma → Expo)

**Input:** `tsa.design_source` (screens[], components[], navigation_graph, design_tokens) + `figma_screens.json` + optional `assets/layouts/{screen}.json`.

## Procedure

### 1. Theme
Generate `src/theme/index.ts` from `design_tokens`. All visual values flow through theme.

### 2. Shared components
For each `design_source.components[]` entry, scaffold typed presentational components in `src/components/`.
- Figma auto-layout → flexbox (`flexDirection`, `justifyContent`, `alignItems`, `gap`).
- Text → `<Text>` with typography tokens.
- Domain components: `MemberCard`, `PlanBanner`, `SwipeToConfirm`, `ConfirmationModal`, `SkeletonLoader`, `EmptyState`, `ErrorToast`.

### 3. Screens (Expo Router)
For **each** `design_source.screens[]` entry (all N stories — no deferrals):
- Route file: `app/(family-plan)/<expo_route>.tsx` (from TSA).
- Screen component: thin wrapper using `FamilyPlanScreenContainer` pattern when applicable.
- Layout: import `assets/layouts/<ScreenName>.json` into `FigmaCanvas` when present; else flex scaffold from `component_tree` / reference `image_ref`.
- Wire `ctaRoutes`, `navigateTo`, `successRoute`, `modal` flags from requirement + navigation_graph.

### 4. Navigation (Expo Router)
- `app/_layout.tsx`: providers + root stack.
- `app/(family-plan)/_layout.tsx`: stack; FP-MODALS routes with `presentation: 'modal'`.
- Each `navigation_graph` edge → `router.push(href)` or `router.replace(href)` on the matching trigger/CTA label.
- Maintain `src/navigation/storyRegistry.ts` (story ID → component → route) for traceability and tests.
- Modal parent: stack `[parentRoute, modalRoute]` per `modal_parent` in TSA.

### 5. Data binding
Per `api_integration.screen_bindings`: hooks in `src/hooks/`; screens never call axios directly.

## Batch implementation (agentic workflow)
When `taskplan/manifest.json` defines batches:
- Implement **only** story IDs in the current batch.
- Register routes in `_layout.tsx` for that batch before marking complete.
- Do not stub unassigned screens with empty `<View />`.

## Fidelity rules
- Do not invent or drop screens; `len(screens) === service.total_screens`.
- No hardcoded colors/spacing outside theme (Figma canvas JSON is sanctioned design data).
- Honor `fidelity_directives` and per-screen acceptance criteria in requirement.txt.
- Compile-clean TypeScript; paired `__tests__/screens/<Screen>.test.tsx` per screen.
