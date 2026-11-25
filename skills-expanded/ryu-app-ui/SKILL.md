---
name: ryu-app-ui
description: Build or migrate a Ryu Companion app with the fixed Ryu App UI v1 vocabulary. Use when an app needs buttons, forms, lists, detail panes, dashboards, empty states, or any visual polish shared with other Ryu apps.
---

# Ryu App UI

Use the Ryu App UI contract for every Companion surface. The app owns its domain data and behavior;
Ryu owns the visual grammar, generic interaction states, and theme.

`v1` is the stable contract version, not a rollout label. A Companion is not v1-compliant until
its entrypoint uses `RyuAppShell`, its CSS imports the shared contract, and its generic chrome is
made from the fixed Ryu roles below.

## Required foundation

- Mark the mounted root with `markCompanionAppRoot` from `@ryu/app-host/companion-theme`.
- Import `@ryu/ui/app-ui.css` from the app's CSS entrypoint.
- Call `subscribeCompanionTheme()` before mounting when the host bridge is available.
- Use `@ryu/ui` for controls, dialogs, menus, badges, status, loading, and empty states.
- Use `@ryu/blocks/companion/app-ui` for app-level composition primitives.
- A dependency-free static satellite that is mirrored outside the monorepo may use a local
  contract-compatible adapter, but it must keep the same v1 root attributes, semantic tokens, and
  navigation ownership. It may not introduce a second visual vocabulary.
- Do not render a primary navigation sidebar inside the Companion. Declare the app's sidebar items
  in `manifest.json` under `contributes.sidebar_sections` / `contributes.sidebar_buttons`; Ryu
  renders them in the hosted shell and in the standalone Ryu App window.

```tsx
import { markCompanionAppRoot } from "@ryu/app-host/companion-theme";
import { RyuAppShell, RyuAppToolbar } from "@ryu/blocks/companion/app-ui";

const root = document.getElementById("ryu-plugin-root");
if (root) {
	markCompanionAppRoot(root);
	root.replaceChildren();
}

export function App() {
	return (
		<RyuAppShell>
			<RyuAppToolbar title="My app" />
			{/* domain content */}
		</RyuAppShell>
	);
}
```

## Fixed vocabulary

Prefer these roles instead of inventing one-off shells:

- `RyuAppShell` - root surface with `standard`, `editor`, and `canvas` modes.
- `RyuAppToolbar` - title and action row.
- `RyuAppMain` and `RyuAppSection` - page structure and grouping.
- `RyuAppList`, `RyuAppListSection`, and `RyuAppListItem` - selectable collection rows.
- `RyuAppDetail` - selected-item or inspector pane.
- `RyuAppForm` and `RyuAppField` - consistent form structure.
- `RyuAppEmpty` and `RyuAppActions` - recovery and action treatment.

Every app entrypoint must compose the mounted component through `RyuAppShell`, even when the app
uses a specialized editor or canvas renderer inside it. This keeps standalone and hosted rendering
on the same visual root.

Use `@ryu/ui` primitives inside those roles. Do not add a second button, card, input, tab, or
theme implementation in the satellite.

## Rules for generated UI

- Do not invent raw colors, radii, shadows, or typography scales.
- Do not use arbitrary gradient or glass treatment to make a surface feel designed.
- Every async surface needs loading, empty, error, offline, and disabled states where applicable.
- Keep domain-specific graph, canvas, media, and editor rendering inside `surface="canvas"` or
  `surface="editor"`; keep its controls on Ryu primitives.
- A domain inspector or canvas tool rail is allowed when it edits the current object. It is not a
  substitute for app navigation and should not contain the app's top-level sections.
- Check the rendered surface in light and dark themes, narrow widths, keyboard focus, and reduced
  motion. A successful typecheck does not prove App UI contract compliance.

## Source of truth

The implementation is in `packages/ui/src/styles/app-ui.css` and
`packages/blocks/src/companion/app-ui.tsx`. Do not copy the token block into an app. If a pattern
is missing, add it to the shared contract once and migrate all consumers to it.

## App identity

When creating or refreshing an app, load `ryu-app-icon` when available. Author filled, layered artwork and render it with Icon Composer. The host displays completed icons directly. Keep any separately declared Companion glyph consistent and inspect light/dark catalog and detail views.
