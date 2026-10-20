---

name: websocket-visualization-pattern
description: Canvas/SVG-based frame-level visualization for WebSocket protocol state, handshake phases, and message flow
category: design
triggers:
  - websocket visualization pattern
tags: [design, websocket, visualization, canvas, svg]
version: 1.0.0
---

# websocket-visualization-pattern

WebSocket visualizations benefit from a three-layer rendering model: (1) a connection-lifecycle timeline showing CONNECTING→OPEN→CLOSING→CLOSED states with color-coded transitions, (2) a bidirectional message lane (client↑ / server↓) where each frame is a rectangle whose width encodes payload size and whose fill encodes opcode (0x1 text, 0x2 binary, 0x8 close, 0x9 ping, 0xA pong), and (3) an overlay for control events (masking key, FIN bit, RSV reserved bits). Render with a fixed time axis scrolling left-to-right so live traffic and replay share the same coordinate system.

For handshake visualization specifically, split the HTTP upgrade into discrete animated steps: client GET with `Sec-WebSocket-Key`, server 101 with `Sec-WebSocket-Accept` (= base64(sha1(key + GUID))), then protocol switch. Expose the SHA-1 computation inline so learners see *why* the accept value is derived, not just that it is. Use monospace for headers, highlight the magic GUID `258EAFA5-E914-47DA-95CA-C5AB0DC85B11` as an immutable constant.

Keep the canvas stateless and redraw from an event log on every frame — this makes scrubbing, pause/resume, and deterministic replay trivial, and avoids the mutable-DOM bugs that plague live-updated WS dashboards.
