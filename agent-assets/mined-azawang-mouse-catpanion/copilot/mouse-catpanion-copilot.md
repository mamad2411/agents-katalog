# Mouse Companion repository instructions

This repository is for a macOS-only MVP desktop app called **Mouse Companion**.

## Product intent

- The app is a lightweight desktop companion, not a general chat app.
- Its core interaction is mouse-hover-triggered micro-interaction.
- Replies must feel short, gentle, playful, and low-interruption.
- Each reply must be at most 3 sentences.
- Prefer 1 sentence by default.

## MVP scope

- Platform: macOS only.
- Primary trigger: user hover in one place for a configurable duration.
- Allow low-frequency proactive "heartbeat" popup, but suppress it during high activity.
- Recognition priority:
  1. direct text capture
  2. OCR fallback
- Do not build full image understanding in the MVP.
- Do not build long chat history, voice, cloud sync, accounts, or complex personality systems.

## Implementation strategy

- Build in small vertical slices.
- Do not implement the whole product at once.
- Prefer mock implementations first, then replace with real integrations.
- Keep the code runnable after each slice.
- Minimize unrelated refactors.

## Architecture rules

- Organize code by feature / module, not generic layers alone.
- Keep module boundaries clear.
- Prefer modules such as:
  - app-shell
  - hover-monitor
  - popup-overlay
  - text-capture
  - ocr
  - llm
  - feedback
  - heartbeat
  - settings
  - usage-tracking
- Add TODO markers for deferred work.
- Keep provider integrations behind a small abstraction layer.

## UX rules

- The product should feel ambient, calm, and slightly alive.
- Popup UI should be lightweight and not block the user's main task.
- Do not produce large modal flows for core interaction.
- Keep settings simple and minimal.
- Feedback controls (👍 / 👎) should be subtle.

## Cost and privacy rules

- Avoid full-screen continuous capture.
- Prefer minimal local region capture only when needed.
- Upload the minimum necessary context.
- Track lightweight usage statistics locally.
- Respect cooldowns, throttling, and token / API usage limits.

## Settings MVP

The first settings view should include only:

- language
- start / pause
- add API
- API usage visualization

## Coding rules

- Choose the simplest implementation that satisfies the current slice.
- Avoid unnecessary dependencies.
- Keep files small and readable.
- Use clear naming.
- If context is missing, preserve current behavior and leave a short TODO instead of inventing a complex system.

## Delivery rules

For each task:

- implement only the requested slice
- keep the app runnable
- update README milestone checklist if relevant
- briefly note assumptions in comments or README when needed
