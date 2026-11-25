---
name: build-game-ui-ux
description: Builds responsive game UI and HUD architectures featuring multi-resolution canvas scaling, 9-slice anchors, mobile and ultrawide safe-area margins, gamepad and keyboard focus navigation, and reactive dialogue or HUD overlays. Use when implementing game menus, HUD widgets, inventory grids, or controller-navigable interfaces.
allowed-tools:
  - read_file
  - write_file
  - edit_file
  - create_file
  - search_code
  - run_build
  - run_tests
  - run_linter
  - execute_command
version: "1.0.0"
---

# Build Game UI UX

Architect and implement resolution-independent game HUDs, menu stacks, and interactive overlays that support ultrawide and mobile aspect ratios, safe-area cutouts, and seamless gamepad/keyboard focus navigation.

## Core Rules

- **Event-Driven UI Decoupling**: Never poll gameplay entities inside UI `Update()` loops. Bind HUD widgets (health bars, ammo counters, cooldown radials, quest trackers) to explicit gameplay events or observable view-models so UI only redraws when state changes.
- **Resolution & Safe-Area Conformance**: Configure reference canvas scaling (e.g. $1920\times 1080$ or $2560\times 1440$ with expand/match width-or-height modes), 9-slice border sprites, and dynamic safe-area insets (`Screen.safeArea`, title-safe margins) across $16:9$, $21:9$, $32:9$, and notched mobile viewports.
- **Unbroken Focus Navigation Loops**: Every interactive screen must assign an explicit default focused element on open, maintain deterministic 4-way directional navigation (`Up`, `Down`, `Left`, `Right`), and restore focus to the invoking control when modal popups close.
- **Contract Adherence**: Emit `contracts/schemas/implementation-result.json` upon completing game UI/UX implementations.

## Suggested Process

### 1. Canvas Hierarchy, Anchors & Safe-Area Layout
Structure UI into layered sorting canvases (`WorldSpaceIndicators`, `GameplayHUD`, `ModalMenus`, `SystemNotifications`, `TransitionOverlay`). Pin HUD corners to a Safe-Area container node and use 9-slice sprite borders so panels scale cleanly without distorting corners.

### 2. Focus Graph & Multi-Device Navigation
Configure explicit focus neighbors for buttons, sliders, and scrollable inventory grids. Ensure opening any menu immediately calls `GrabFocus()` / `Select()` on the primary action button and blocks pointer-hover theft when operating in gamepad mode.

### 3. Reactive HUD & Pooled Floating Overlays
Drive health/mana bars with secondary delayed damage-trail bars and pooled floating combat text (FCT) widgets. Separate static background frames from frequently dirtied dynamic text/fill canvases to prevent full-canvas UI batch rebuilds every frame.

### 4. Accessibility & Scaling Verification
Expose text scaling ($100\%\text{--}150\%$), high-contrast HUD backgrounds, and colorblind-safe status iconography (pairing distinct shapes with colors). Test layouts headlessly or across simulated aspect ratios ($4:3$, $16:9$, $21:9$, mobile portrait/landscape).

## Output Contracts

When completing game UI and UX implementation, emit:
- `contracts/schemas/implementation-result.json`

## Checklist

- [ ] HUD widgets update reactively via event subscriptions with zero per-frame polling
- [ ] Canvas anchors, 9-slice panels, and safe-area margins adapt cleanly to $16:9$, $21:9$, and mobile notches
- [ ] Gamepad and keyboard focus navigation operates deterministically without focus loss on modal close
- [ ] Dynamic HUD elements are isolated from static UI layers to minimize canvas batch rebuilds
- [ ] Floating combat text and transient notification popups use pre-warmed object pools
- [ ] UI supports text scaling and shape-reinforced indicators for colorblind accessibility

## Failure Modes

- **Per-frame UI polling**: HUD widgets poll gameplay entities inside `Update()` loops, burning CPU and redrawing unchanged state. Mitigation: bind widgets to gameplay events or observable view-models so redraws fire only on state change.
- **Focus loss on modal close**: a popup closes and focus is not returned to the invoking control, stranding keyboard/gamepad users. Mitigation: restore focus to the invoking control on close and call `GrabFocus()`/`Select()` on the default element when any screen opens.
- **Notch and ultrawide clipping**: HUD elements pinned to raw screen corners hide behind notches or fall outside $21:9$/$32:9$ safe areas. Mitigation: parent HUD to a Safe-Area container with 9-slice borders and test across $4:3$, $16:9$, $21:9$, and mobile viewports.
- **Pointer-hover focus theft**: mouse movement steals focus from gamepad navigation mid-menu, desyncing the focus ring. Mitigation: block pointer-hover focus claims while operating in gamepad mode.
- **Full-canvas batch rebuild**: frequently updated combat text lives on the same canvas as static frames, forcing full-canvas UI rebuilds every frame. Mitigation: separate static background layers from dirty dynamic text/fill canvases.
- **Unpooled overlay churn**: floating combat text and notification popups allocate widgets per event, causing GC spikes. Mitigation: pre-warm object pools for FCT and transient popups.
- **Color-only status coding**: status effects rely on color alone and become unreadable for colorblind players. Mitigation: pair distinct shapes with colors and verify layouts at $100\%\text{--}150\%$ text scaling.

## Security Guardrails (OWASP ASI)

- **ASI01 Goal Hijack**: gameplay events must drive UI presentation only; reactive bindings must never let UI-side handlers re-author gameplay decisions. Mitigation: keep the event flow one-directional (gameplay → UI) and route player intents back through the input action layer.
- **ASI05 RCE Guard**: never render networked or user-supplied strings (player names, chat, floating combat text) as raw rich text or format templates. Mitigation: escape markup and render through safe text nodes only.
- **ASI06 Context & Memory Poisoning**: HUD view-model state cached across scene changes can be stale or tampered with. Mitigation: validate event payloads against view-model schemas before display and reset cached HUD state on scene transitions.
- **ASI07 Inter-Agent Communication**: UI results are consumed by input, dialogue, and game-feel roles. Mitigation: emit the schema-valid `implementation-result.json` contract so peers validate before wiring focus graphs or glyph prompts.
- **ASI09 Human-Agent Trust Exploitation**: do not claim accessibility conformance without evidence. Mitigation: report text scaling and colorblind support only after simulated-viewport and scaling verification passes.

## Related Skills

- **abstract-input-actions**: routing UI navigation contexts and dynamic controller glyph prompts
- **integrate-dialogue-narrative**: rendering typewriter dialogue boxes, speaker portraits, and choice menus
- **tune-game-feel**: animating snappy UI transitions, button press juice, and audio feedback
