---
name: master-design-doc-illustrations
description: Create and verify explanatory figures and interactive studies for the Master Design documentation site. Repository authoring only; not a capability of the public master-design skill.
metadata:
  internal: true
---

# Master Design documentation illustrations

Help a reader understand a relationship, choose between alternatives or predict an interaction. This is a repository maintenance tool. Keep its methods, templates, drawing assets and implementation outside `skills/master-design`.

## Establish the explanation

Write the intended inference before drawing. Read the canonical reference and relevant implementation or standard. Identify what is measured, derived or judged. An arrow must have a clear meaning; containment must not accidentally imply DOM ownership, modality or a platform guarantee.

Choose prose or a table when it already explains the decision. Use an annotated construction for geometry, a controlled comparison for a variable, a sequence for state changes, or a responsive composition for changing space. Use a working specimen when actual text rendering or behavior is the evidence. There is no figure quota.

Keep unrelated variables constant in a comparison. If multiple relationships change, name them. Numeric values are contextual specimens; magnification is not device density. A schematic cannot prove actual raster quality or accessible behavior.

## Compose for this site

Prefer flowing HTML/CSS for labels and real interface content, and SVG for paths and geometry. Use Canvas only for a demonstrated continuous-drawing need. Reuse the site's fonts and semantic roles for annotation chrome, and Master UI for functional study controls. Diagram geometry is local teaching content, not a second component library or a consumer style profile.

Wrap every figure and interactive teaching specimen in the shared `@master/internal-site/demo/Demo.svelte` tray, matching the UI and CSS documentation: title in the tray head, drawing in its `sheet sheet-flat` stage, and explanation in its caption. Static figures also provide a native Text description disclosure. Use `GuideFigure.astro` or `StudyFrame.astro`; do not draw a separate outer card, frame or token system. This is a site presentation requirement, never a rule for consumer projects.

Use direct labels, distinguish meaning without color alone, and reflow panels before reducing text. Give each figure a useful title and caption. Label schematic and enlarged views. Do not expose decorative drawings to assistive technology when adjacent text gives an equivalent explanation. Real controls remain accessible.

## Integrate without changing the public package

Read `site/figures/catalog.mjs`, `site/components/GuideFigure.astro` and the nearest existing study. Register the figure's stable ID, canonical source and section heading. The Markdown adapter inserts its presentation at that section; missing sources, headings and renderers must fail preparation.

Keep every essential design conclusion in ordinary Markdown under `skills/master-design/references/`. Do not put internal authoring instructions, component invocations or site asset paths in those sources. The public skill and downloaded Markdown must remain complete without the illustration. Drawing labels and local interaction instructions live with the site.

The registry and existing renderers are the reusable templates. Extend a nearby specimen when its mechanism fits; add a dedicated renderer when it does not. Do not force unrelated lessons into a universal scene graph. Existing research examples retain their source and evidence history.

## Verify the claim and the artifact

Read the drawing without its caption, then the reference without its drawing. Both must support the same conclusion. Check ordinary and narrow reading widths, both themes, long text, labels and connectors at actual size. For geometry, also inspect relevant native densities. For interaction, check keyboard, first touch, hydration, reset, interruption, reduced motion and unavailable enhancement.

Run the affected site and study checks, then inspect screenshots. Search and downloadable Markdown must contain the important knowledge; images alone do not make it searchable. Generated output belongs in ignored `artifacts/` or site output. Record reviewed evidence and actual limitations in `docs/verification/`.

Public installation and release checks must exclude this skill. Do not change the public skill's description to advertise diagram authoring.
