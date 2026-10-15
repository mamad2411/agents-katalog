---
name: lemonslice-widget
description: Embed and control the Lemon Slice widget.
license: MIT
---

# Lemon Slice Widget Integration

## Official docs
- https://lemonslice.com/docs/widget/overview.md
- https://lemonslice.com/docs/widget/control.md

## Use this skill when
> **Guardrail:** Use only after `lemonslice-integration-choice` has explicitly selected this path.
The developer wants the simplest integration path: dropping a prebuilt web component onto a website with minimal custom coding.

## Do not use this skill when
- The developer needs deep customization of the UI (use `lemonslice-hosted` or `lemonslice-self-managed`).
- The developer is building a custom LiveKit or Pipecat integration.

## Agent workflow
1. **HTML Embed:**
   - Use the web component: `<lemon-slice-widget agent-id="agent_id"></lemon-slice-widget>`.
   - Include the script: `<script type="module" src="https://unpkg.com/@lemonsliceai/lemon-slice-widget"></script>`.
2. **Next.js Integration:**
   - Keep the widget in the root layout so it persists across page navigation.
3. **Customization Attributes:**
   - The `<lemon-slice-widget>` component supports these customization attributes:
     - `initial-state`
     - `controlled-widget-state`
     - `custom-active-width`
     - `custom-active-height`
     - `custom-minimized-width`
     - `custom-minimized-height`
     - `inline`
     - `hide-ui`
     - `controlled-show-minimize-button`
     - `show-minimize-button`
     - `video-button-color-hex`
     - `video-button-color-opacity`
4. **Programmatic Control:**
   - The widget exposes the following supported methods via its API:
     - `mute()`
     - `unmute()`
     - `isMuted()`
     - `canUnmute()`
     - `micOn()`
     - `micOff()`
     - `isMicOn()`
     - `canTurnOnMic()`
     - `sendMessage(message)`
5. **Metadata:**
   - To retrieve widget call metadata, query the `/api/liveai/rooms` endpoints using the session ID.

## Common mistakes
- Adding unsupported attributes or trying to guess methods that aren't documented above.
- Re-mounting the widget on every page load in a single-page application (SPA). It should sit at the root layout level.

## Validation checklist
- [ ] Is the web component tag using supported customization attributes only?
- [ ] Are programmatic controls limited to the documented `mute()`, `micOn()`, etc. methods?
- [ ] Is the metadata lookup using the `/api/liveai/rooms` endpoint?
