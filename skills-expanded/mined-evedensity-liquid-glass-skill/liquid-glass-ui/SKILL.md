---
name: liquid-glass-ui
description: Implement, restyle, or debug interactive liquid glass in web interfaces. Use for refractive buttons, switches, sliders, segmented controls, theme toggles, toolbars, and floating surfaces with press, drag, or merge behavior. Choose CSS glass for arbitrary page content or WebGL2 refraction for a backdrop the app can supply as pixels.
license: MIT
---

# Liquid Glass UI

Apply glass only to the named buttons or controls. Preserve the host background, layout, labels, and behavior. Before editing, state the target controls and confirm any unspecified visual choice. A change to another part of the interface requires a separate agreement.

## Confirm the button design

When the user names the demo's moon/sun theme toggle, use that built-in design directly. For example, ask Codex: `Use $liquid-glass-ui to restyle my existing light/dark toggle with the demo’s pixel moon and sun. Keep my app’s theme state and persistence.` In Claude Code, start the same request with `/liquid-glass-ui`.

Use a design the user has already selected or pasted. Otherwise, open the demo at `http://localhost:58423/demo/` and ask the user to choose a control and click **Copy for AI**. Start `node scripts/serve.mjs` from the skill directory if needed. Before asking for the selection, read the baseline `copiedAt` from `GET http://localhost:58423/api/glass-handoff`. Use a newer handoff or the clipboard payload the user provides. Wait for the choice before editing the target.

Pass the returned configuration directly to the matching runtime. Version 2 uses `createLiquidGlassButton` from `assets/glass-button.js`. Version 3 uses `mountLiquidGlassReplica` from `demo/replica.js` for moving controls or group selections. Use the revision specified in a clipboard handoff. Use the existing page's readable source and preserve the crop, layout, and original actions. See the [handoff integration recipes](references/integration.md#integrate-a-copied-design). When the host pixels cannot be read, explain the available fallback and confirm it before editing the target.

## Choose the rendering path

- **Moon/sun theme toggle** uses `createGlassThemeToggle` from `assets/glass-theme-toggle.js`. Bind it to the host's current theme and existing persistence. Its CSS mode supports ordinary page backgrounds. To reproduce the demo's optical squeeze and fusion with a neighboring glass lens, reuse `demo/theme-toggle.js` and `assets/liquid-glass-renderer.js` with a readable backdrop, following the [theme toggle recipe](references/integration.md#glass-theme-toggle).
- **Dark backdrop adjustment** is available under **Background → Preview theme → Dark** in the demo. If the user wants the same adjustment in a host WebGL scene, pass the chosen opacity (0–1) to `scene.setBackdropDim(opacity)`. Apply it only when the user requests backdrop dimming.
- **CSS glass** fits arbitrary DOM, text, and scrolling content. Copy `assets/liquid-glass.css` for blur, tint, and a rim. Add `assets/liquid-glass.js` only if the user wants pointer highlights. CSS glass cannot bend or merge backdrop pixels.
- **WebGL2 refraction** fits images, video, and canvases controlled by the app. Copy `assets/liquid-glass-renderer.js` and `assets/mount-liquid-glass.js`. Keep the actual controls in HTML above an `aria-hidden` canvas. Use the app's original layout and a permitted backdrop.
- **Exported standalone button** uses `assets/glass-button.js`. Pass the positioned host stage and its decoded pixel source to reproduce the demo optics. Without a source, the same button uses CSS glass.
- **Glass plus an opaque fallback** fits readability or browser constraints. Handle reduced transparency, forced colors, and WebGL context loss. Give the fallback the same native actions and usable contrast.

Read [integration](references/integration.md) for runnable wiring and the shape API. Read [materials](references/design-system.md) when selecting presets or treating different control states. Use [acceptance](references/acceptance.md) to verify the target interface.

## Implement and check

1. Inspect the target markup, source backdrop, stacking order, and native input behavior. Keep actions and labels outside the decorative canvas.
2. Choose the reference states that matter for this component. Separate idle, hold, travel, and release. A clear lens can stay transparent at rest. A selector can use a pale resting fill and reveal its track on hold.
3. In WebGL, use one stage-local canvas. Map the actual visible glass outline to its center and dimensions. Submit only glass to the merge field. Fixed rails and bases can be sampled as background layers without joining the glass contour.
4. Drive shape updates from the app's input and animation state. Keep track positions and hit targets stable. Apply stretch along the direction of travel and ease it out after release. Honor reduced motion.
5. Check the actual target page with contrasting backdrop detail. Inspect idle, press, travel, and release as applicable. Verify keyboard and touch operation, mobile layout, and a readable fallback. Mention any visual or browser limits supported by the checks.

Run `node scripts/serve.mjs` from this folder and open `http://localhost:58423/demo/` to try the bundled switch, slider, segmented control, light/dark theme toggle, and lens with six presets. The materials are independently implemented and tuned against the public Good Machines demo.
