---
name: aggregator-widget
description: Integrate and configure the `@minswap/aggregator-widget` package in React apps or plain HTML pages. Use when needs to add the Minswap swap widget, explain or choose widget props, wire in a CIP-30 wallet-compatible object, limit selectable assets or protocols, customize button or full display mode, or apply theming for the aggregator widget.
---

# Aggregator Widget

## Overview

Integrate the Minswap aggregator widget with the smallest setup that matches the user's app: React for normal app code, or HTML import-map setup for static pages and quick demos.

Use the official widget docs as the authoritative external reference:

- `https://docs.minswap.org/developer/aggregator-widget`

Read [references/widget-reference.md](references/widget-reference.md) when you need exact installation commands, prop details, protocol values, wallet type shape, or theming options.

## Integration Flow

Follow this order:

1. Identify whether the user needs React integration or plain HTML embedding.
2. Add the package and render `<Widget />` with only the props the user actually needs.
3. Configure wallet, assets, protocols, and display mode based on the request.
4. Pull extra details from the reference file only for the specific props or theme settings involved.

## Choose The Setup

- Use React setup for Next.js, Vite, or other React applications.
- Use HTML setup only when the user explicitly wants a no-build embed, a static demo page, or import-map usage.
- Default to `displayMode="full"` unless the user asks for a launcher-style button.

## Implement The Widget

Start from the simplest React shape:

```tsx
import { Widget } from "@minswap/aggregator-widget";

export function SwapWidget() {
  return <Widget partnerCode="your-partner-code" displayMode="full" />;
}
```

Adjust props only when requested:

- Add `wallet` when the app already manages wallet connection externally.
- Add `defaultAsset` when the initial token must be preselected. Do not use ADA here.
- Add `selectableAssets` when the asset list must be constrained. ADA remains available.
- Add `allowedProtocols` when routing must be restricted. Keep in mind Minswap protocols remain included.
- Add `trigger` only when `displayMode="button"` is used.

## Wallet Guidance

Pass a wallet object only when the host app already has one. Otherwise let the widget handle wallet connection internally.

When the user provides a wallet integration request:

- Preserve the widget's expected wallet shape from the reference file.
- Keep the wallet object stable enough for widget updates by including its `id`.
- Do not invent extra CIP-30 methods that the widget does not require.

## Asset And Protocol Guidance

Use asset strings in the `policyId + tokenNameHex` format for native tokens.

Remember these constraints:

- `defaultAsset` cannot be `lovelace`.
- `selectableAssets` may include `"lovelace"`.
- `allowedProtocols` limits routing, but Minswap protocol variants are still available.

## Theming And Display

Prefer built-in themes for straightforward requests. Read the reference file for the available preset theme names and advanced theming details before documenting or implementing custom styling.

If the user asks for a popup or launcher interaction:

- Set `displayMode="button"`.
- Pass a custom `trigger` node when they want branded button UI.

## Response Style

Keep answers implementation-first:

- Show the minimal install command for the user's package manager.
- Give one focused code snippet instead of listing every prop.
- Mention only the props that solve the request at hand.
- Load the reference file for exact prop tables, wallet type details, HTML embed markup, or theming specifics.
