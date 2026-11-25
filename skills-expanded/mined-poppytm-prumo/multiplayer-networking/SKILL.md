# Multiplayer Networking

## Purpose
Implement and audit server-authoritative multiplayer replication with client-side prediction and reconciliation, bandwidth-bounded delta compression, snapshot interpolation, lag compensation, and graceful reconnection over lossy UDP networks.

## Use when
- Implementing client-server state replication, interest management, or entity relevancy for a multiplayer game.
- Adding client-side prediction and server reconciliation to hide round-trip latency.
- Budgeting bandwidth with delta compression, quantization, and MTU-safe packet packing.
- Smoothing remote entities with snapshot interpolation or fixing hit registration with lag compensation.
- Designing disconnect, reconnect, and session-migration flows.

## Do not use when
- Testing lockstep determinism or physics-only determinism without networking (use `physics-testing`).
- Profiling raw CPU, GPU, or memory performance unrelated to network load (use `performance-native`).
- Automating bot playtests or input-replay harnesses without netcode assertions (use `playtest-automation`).

## Required context
- Authority model: dedicated server, listen server, or rollback peer topology with tick rate (e.g., 20 Hz server, 60 Hz client render).
- Entity inventory with replication frequency classes (e.g., player pawn 20 Hz, projectile 10 Hz, static pickup on-change).
- Bandwidth budget per client (e.g., 64 kbps downstream ceiling on broadband floor) and worst-case RTT/loss profile (e.g., 180 ms, 5% loss).
- Transport details: UDP socket layer, reliability layer (e.g., custom ACK bitfield vs ENet), encryption and replay protection.

## Procedure
1. **Fix authority and the simulation contract**: Declare the server the sole writer of gameplay state; clients send only timestamped input commands (`seq`, `dt`, button bitmask). Document the tick pipeline: sample input, simulate at fixed 50 ms server steps, broadcast snapshots.
2. **Implement prediction and reconciliation**: On the client, apply local input immediately to the predicted pawn and buffer inputs in a 64-entry ring. On snapshot receipt, compare authoritative position with prediction; if error exceeds 8 cm, rewind to the acknowledged tick and re-simulate buffered inputs (server reconciliation).
3. **Compress with deltas and quantization**: Replicate only fields changed since the client's last ACKed snapshot (delta bitmask per property). Quantize transforms (position to 1 mm fixed point, rotation to 12-bit yaw) and pack packets to stay under 1200 bytes (safe internet MTU floor); measure mean packet size with `scripts/` packet logger over a 10-minute 8-player soak.
4. **Interpolate remote entities**: Buffer the two most recent snapshots and render remote pawns at `render_time = newest_server_time - 100 ms`, lerping between snapshots; assert interpolation delay stays within 80-120 ms and jitter buffer never underflows above 3% packet loss.
5. **Compensate lag for hits**: On hitscan fire, rewind server hitboxes to `server_time - shooter_RTT/2` using the 1-second position history buffer, then test hit against rewound capsules; log shooter-client vs server hit agreement, targeting at least 98% agreement below 120 ms RTT.
6. **Harden reconnect and bandwidth**: Implement resync via full-state baseline plus delta stream so a client dropping for up to 30 s rejoins without a scene reload; enforce per-client bandwidth caps with relevancy culling (40 m radius, 12-entity cap) and run `scripts/verify.sh` to confirm artifact completeness.

## Decision rules
- **Server authority is absolute**: Clients never write gameplay state; any client-originated state is rejected and logged as a cheat signal.
- **Packets stay under 1200 bytes**: Fragmentation is forbidden; oversized snapshots must be split across ticks by priority, never fragmented at the IP layer.
- **Prediction error has a numeric gate**: Reconciliation snaps only above 8 cm error; below that, smooth-damp toward authority within 150 ms.
- **Bandwidth budget is a hard ceiling**: If mean downstream exceeds 64 kbps per client in soak tests, cut relevancy radius or update frequency before cutting simulation fidelity.
- **Reconnect must not reload**: Any drop under 30 s resumes from baseline-plus-delta; full scene reload on reconnect is a defect.

## Evidence required
- Tick-rate and packet-size histograms from a 10-minute 8-player soak (mean packet, p99 packet, packets over 1200 bytes must be zero).
- Prediction error distribution and reconciliation counts per minute at 80 ms, 150 ms, and 250 ms emulated RTT.
- Shooter-vs-server hit agreement report for lag compensation.
- Reconnect drill log: 5 drops of 10-30 s each, all resuming without reload.
- Passing execution log from `scripts/verify.sh`.

## Output contract
- Netcode specification document following `templates/multiplayer-networking-spec.md` with authority, tick, bandwidth, and reconnect contracts.
- Prediction, reconciliation, interpolation, and lag-compensation implementation with unit and soak tests.
- Bandwidth and hit-agreement reports archived with the build under test.

## Stop conditions
- Soak test holds 20 Hz server tick with zero over-1200-byte packets and per-client downstream within budget.
- Hit agreement at or above 98% below 120 ms RTT and reconnect drills all resume without reload.
- Token budget exhausted.
- Blocked on external dependency.

## Escalation rules
- Escalate to the lead engineer if cheat telemetry shows clients forging state the authority model cannot reject without protocol changes.
- Escalate to backend/infrastructure if RTT/loss profiles exceed the design envelope ( sustained RTT above 250 ms or loss above 8%) and relay or region expansion is needed.
- Escalate immediately on any unauthenticated remote-code-execution or packet-spoofing vector found in the transport layer.
