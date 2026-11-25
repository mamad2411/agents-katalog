---
name: ryu-app-icon
description: Design layered Ryu app and plugin artwork and render it with Icon Composer's iOS 27 material system. Use when creating an app, choosing its visual identity, or replacing catalog icons.
---

# Ryu app icons

Design the object first. A small outline glyph on a glossy gradient tile does not resemble the current Apple app icons, even if it has shadows and rounded corners. Avoid double borders, inset plaques, a universal white foreground, and decorative shine across the enclosure.

Read and visually inspect [Apple's app icon examples](https://developer.apple.com/icon-composer/) and [app icon guidance](https://developer.apple.com/design/human-interface-guidelines/app-icons). Compare actual images, not just their descriptions.

## Compose an identity

Choose a recognizable object related to the app: a folded envelope, a page of dates, overlapping browser windows, a globe with a navigation pointer, or translucent drawing shapes. Let the subject occupy about 70–80% of the canvas. Use filled masses, negative space, and a few clearly separated parts. Color belongs to the artwork as well as the background; unrelated apps should not share identical artwork. Related variants can share an object when color or a clear detail distinguishes them.

Author foreground parts as separate SVGs on a 1024×1024 canvas. Let Icon Composer create the enclosure and material lighting. Do not bake an outer rounded square, bevel, inset border, or shadow into the foreground artwork. Preserve supplied third-party identity and colors.

Use native glass on the actual artwork layers. Vary translucency between the supporting mass and front detail. Keep small details subordinate and avoid stroke-dominated silhouettes. Keep source artwork editable; a flattened PNG alone is not the authoring master.

## Ryu source workflow

`tools/design-app-icons.py` authors complete `.icon` documents and uses Apple's `ictool` with `--design-generation 27`. Bespoke compositions are defined there; filled subject mappings and licensed SVG sources are in `tools/icons/composer/`. The source documents retain ordered groups and editable SVG assets. Existing documents are the editable masters: normal runs preserve their artwork and rerender it. `--refresh-defaults` deliberately replaces those masters from the seed recipes; use it only when that replacement is intended. The `groups` array is front-to-back, unlike SVG painting order.

When introducing a new manifest glyph, select a filled subject and supporting mass or author a bespoke composition. Update `glyph-subjects.json` and vendor the corresponding SVGs when using the existing subject library. Retain its license. For new branded listings, use public stable artwork URLs and run `bun tools/vendor-icon-art.mjs` before seeding the document, or import the artwork directly into its editable master. Do not silently map an unknown subject to a generic icon.

Prototype representative objects first:

```sh
python3 tools/design-app-icons.py --only browser,calendar,mail
```

Inspect those at 256px and real 40px catalog size against Apple's examples. Fix composition and material problems before applying the set broadly. Then render and wire the complete catalog:

```sh
python3 tools/design-app-icons.py
python3 tools/design-app-icons.py --check
```

The tool discovers an installed Xcode Icon Composer that supports generation 27. Set `RYU_ICTOOL` to an explicit executable when needed. Check `ictool --help` and `--version`; do not assume an older renderer supports generation 27. On a host without Icon Composer, retain the supplied PNGs and arrange rendering on a Mac. Do not replace native rendering with a CSS approximation and claim equivalent quality.

The generator writes native documents, rendered light/dark/tinted PNGs, source fingerprints, renderer metadata, and the client asset registry. Complete icons are displayed directly by `AppIcon`, with no additional tile or glyph painted over them. End users do not need Xcode. The existing PNG export tool reuses these shipped assets.

For apps authored outside the source checkout, render a complete icon with Icon Composer, host the exported image, and declare `iconUrl` with `iconPadding: "none"`. Omit a competing top-level glyph in `icon`. Keep your `.icon` source alongside the app's authoring files. Follow the public [Icon documentation](https://docs.ryuhq.com/docs/extend/develop/ui-package/icon).

## Judge the result

Inspect light and dark variants at 20, 40, 80, and 256px. Check the set for duplicate identities; a shared vendor mark can be intentional, but unrelated apps should not reuse identical art. Annotate dark fills so white-on-color artwork retains its identity on a dark enclosure. Check silhouette recognition, useful overlap between layers, clean edges, and restrained shadows. Tinted artwork uses Apple's TintedDark rendition; it is not a full-color icon with a CSS filter.

Test all affected catalog entries offline, card/detail consistency, supplied artwork, and narrow layout. Retain product screenshots and actually inspect them before claiming completion. Tests establish rendering and behavior; they do not establish design quality. Update public documentation for changed authoring or display behavior.
