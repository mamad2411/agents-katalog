# CLI Module

This module owns the interactive runtime navigator — KOTA's operator-facing
TTY client. It is one of several KotaClient consumers; the daemon-backed
native, web, and mobile clients use the same contract through different
transports.

## Conventions

- The navigator reads and mutates runtime state exclusively through the
  `KotaClient` contract on `ModuleContext.client`. It must not import core
  module services, read `.kota/` files directly, or open its own daemon
  socket.
- Failures from the contract surface in-place. The navigator never falls
  back to a private local path when the daemon is reachable.
- Output flows through the `rendering` module's primitives and shared
  `TerminalTransport`. No bare `console.log` for operator-facing output;
  reserve `process.stderr` for diagnostic banners.
- Composition stays in typed TypeScript. Do not add a screen DSL or a
  template engine; new screens are functions over `RenderNode`.

## Behavior

- Entrypoint: bare `kota` on a TTY and explicit `kota navigate` both launch the
  operator console. Agent chat and one-shot prompts live under explicit
  `kota run`; pipes and scripted callers keep their existing non-TTY path.
- TTY-only. When `process.stdin.isTTY` is false the navigator refuses to
  launch and prints the equivalent one-shot subcommand hint so pipes,
  cron jobs, and scripted callers fail loudly instead of hanging on a
  prompt.
- The first screen is built from `client.ui.listSurfaces()` and groups exposed
  shared UI surfaces by protocol intent: Status, Inbox, Work, Knowledge, and
  Setup. Backend nouns stay inside contributed surfaces instead of becoming a
  second CLI-only navigation model.
- Interaction state is explicit and testable: focus, selected surface/action,
  command palette, keybindings, theme preference, resize width, and live
  event-stream status live in the navigator state reducer.
- Live updates subscribe through `client.ui.watchEvents()` using the
  `log-stream` event metadata declared by shared UI surfaces. Do not open a
  private daemon transport from the navigator.
- Secrets values are never rendered. The screen lists names and sources
  only; the only mutation is removal.
