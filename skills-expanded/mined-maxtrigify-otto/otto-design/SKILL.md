---
name: otto-design
description: How Otto UI is designed before it is built. Use whenever a task adds or changes anything a person sees in Otto (a place, card, sheet, flow, Home card, browser chrome, onboarding), or asks for a mockup, redesign or design review. Design happens in Paper on Otto's real frame and tokens, is shown to Max on his theme, and only then becomes SwiftUI.
---

# Designing for Otto

Otto's interface is translucent surfaces over a live themed backdrop, two fonts, nine colour
slots and quiet controls. Mockups that ignore that look wrong immediately, however polished.
This skill is the process; `DESIGN.md` at the repo root is the system; `docs/DESIGN_SYSTEM.md`
is how the system is consumed in SwiftUI. Read `DESIGN.md` before any design work.

## 1. Where design happens

**Paper first.** All screen design is done in Paper (the Paper MCP server, `paper-desktop`),
on an artboard that reproduces Otto's real frame, so the person reviewing sees something that
looks like the app, not a web page. Load the guide once per session with
`get_guide({ topic: "paper-mcp-instructions" })`, then `get_basic_info` and
`get_font_family_info`.

- If Paper is not running, say so and ask for it to be opened. Do not substitute an HTML
  mockup unless the person asks for one. (An HTML page in Otto's browser is a fallback for
  quick layout questions only, and must still use the token block below.)
- One Paper file per feature, under a page named for the feature. Keep an "Otto kit" page in
  the same file with the frame, tokens and components so variants are duplicated, not redrawn.
- Make two or three variants that differ in structure, not colour. Name artboards
  `Feature · Variant · Theme`.

**Frame.** Desktop artboard 1440×900 (or 1440×1040 for tall pages). Reproduce:
top bar 40 high with the Home | Chat pill; sidebar 232 wide on `ink` at 60% with search, New,
the places list, `BOTS` and `SESSIONS` groups and the Voice footer; the content pane on
`surface` at 55%. Put a backdrop image under everything. For Shorelight use a sunlit
Mediterranean shore (see `references/screens/home-shorelight.jpg`); never leave the backdrop
flat or black. Reference captures of the real app are in `references/screens/`.

**Theme.** Review with Max happens on **Shorelight**. Design on Shorelight, then check the
same artboard on Field Notes (dark, acid signal) and Highfell (light) before calling it done.
Light themes invert `paper` and `ink`; make sure nothing relies on "text is light".

## 2. Token block for Paper and HTML

Paste this into the first `write_html` of a session (or the `<style>` of an HTML fallback) and
use the variables only. Values are Shorelight; swap the block for another theme from
`DESIGN.md` §2.

```css
:root{
  --ink:#081A1C; --surface:#0D2426; --raised:#143033; --paper:#F2EBD6; --muted:#94B2AB;
  --signal:#FAC24C; --amber:#EB8C4C; --red:#F26954; --cyan:#61CCD1;
  --hair: rgba(242,235,214,.08);
  --font-display: "Inter Variable", Inter, -apple-system, sans-serif;
  --font-mono: "SF Mono", ui-monospace, Menlo, monospace;
}
.sidebar{background:rgba(8,26,28,.60)} .pane{background:rgba(13,36,38,.55)}
.card-home{background:rgba(8,26,28,.88);border:1px solid var(--hair);border-radius:12px}
.card{background:rgba(20,48,51,.92);border:1px solid var(--hair);border-radius:12px}
.row{background:rgba(20,48,51,.55);border-radius:10px}
.input{background:rgba(8,26,28,.48);border-radius:9px}
.micro{font:800 8px/1 var(--font-mono);letter-spacing:.12em;text-transform:uppercase;color:var(--muted)}
.pill{background:var(--raised);border-radius:7px;padding:6px 12px;font:600 12.5px var(--font-display);color:var(--paper)}
.primary{background:var(--signal);color:var(--ink);border-radius:8px;padding:6px 12px;font:600 12.5px var(--font-display)}
```

Fonts in Paper: use Inter for display text and SF Mono for labels. If Paper cannot offer
SF Mono, use the closest monospace it lists and say so in the artboard note.

## 3. The process

1. **Read** `DESIGN.md`, the relevant Swift view (`Sources/OttoApp/…`) and the latest real
   screenshot of the surface. If no screenshot exists, capture one from Otto Dev first
   (`scripts/dev-app.sh`, DEBUG probe `go:<place>`), so the frame you draw is current.
2. **Decide the job of the screen in one sentence** and what the person must be able to do
   without reading. Write it as the artboard's note.
3. **Draw in Paper** on the Otto frame. Reuse the kit page. Two or three structural variants.
   Apply the craft rules in the `frontend-design` skill (type scale, concentric radii, layered
   shadows, interruptible motion) under `DESIGN.md`'s choices.
4. **Check** against the review list below, on Shorelight, Field Notes and Highfell.
5. **Show Max** a Paper screenshot (`get_screenshot`) on Shorelight with realistic content
   (real bot names, real copy, real counts), in chat, with the one or two decisions you need
   from him. Do not start SwiftUI before he has seen it. He has rejected UI changed as a side
   effect of a fix before; keep every change scoped to the surface in question.
6. **Build** in SwiftUI through `@Environment(\.ottoPalette)`, `ottoDisplay` and `ottoMono`,
   literal sizes from `DESIGN.md` §3, no new materials. Then confirm with a Dev snapshot on
   Shorelight beside the Paper artboard.

## 4. Review list

- Backdrop visible through every surface; no opaque panels, no blur materials.
- Nine slots only; one accent doing the work; semantics not hues.
- Inter + SF Mono only; micro-labels for structure; sentence case copy in Otto's voice.
- Quiet controls: `raised` pills with symbols for card actions; `signal` fill for the single
  primary action; `red` text for destructive.
- Radii from the clusters, concentric when nested; hairlines not borders; shadows layered.
- Empty, loading, error and "needs you" states drawn, not implied.
- Works on a light theme. Works at font scale 1.3. Reduce-motion and reduced-transparency
  branches described.
- Nothing generic: no purple gradients, stock card grids, emoji icons, or web-app chrome.

## 5. Other skills in this repo and when they apply

- `frontend-design` (from cult-ui, MIT): craft doctrine for type, surfaces and motion. Always
  applies, underneath `DESIGN.md`.
- `components-build` (from cult-ui, MIT): React component architecture. Only for web code
  under `Web/` or the public site; never for the SwiftUI app.
- `superdesign` (from superdesign.dev, MIT): a hosted design agent driven by its CLI. Needs
  `superdesign login` and spends credits. Optional, for web pages, slide decks and graphics
  when Paper is not the right tool. Not for app screens.
- Component registries (cult-ui, canvas-ui via the shadcn MCP) are for web surfaces only.
