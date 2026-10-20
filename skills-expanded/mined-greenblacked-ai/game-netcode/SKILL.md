---
name: game-netcode
description: "Choose and implement a multiplayer networking model that survives real latency and dishonest clients. Picks the authority model first from genre and player count — server-authoritative, client-authoritative, deterministic lockstep or rollback — then builds client-side prediction, server reconciliation, entity interpolation and lag compensation in that order, sizes tick rate, interpolation buffer and per-player bandwidth against numbers, and validates on the server everything a client could lie about. Use whenever someone is adding multiplayer, debugging it, or asks \"players rubber-band\", \"should the server be authoritative\", \"my fighting game needs rollback\", \"what tick rate\", \"why do my shots not register\", \"UDP or WebSockets for a browser game\", or \"the clients desync\". Not for building the game itself, for frame rate or frame budget, or for a web API that is not game state."
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(git:*), Bash(tc:*), Bash(npm:*), Bash(node:*), Bash(godot:*), Bash(dotnet:*)
---

# Game Netcode

Netcode is right when a player on a 120 ms connection cannot tell what their latency is from playing, and when nothing they send the server is believed without being checked.

Two mistakes account for most broken multiplayer, and both are made in the first week. The first is choosing the authority model by convenience: the prototype sends positions between clients because that was the smallest change, the game ships, and every fix afterwards — hit registration, cheating, joining late, spectating — is blocked on a rewrite of the thing the whole codebase now assumes. The second is treating latency as a defect to be removed. It cannot be removed; the speed of light across a continent is tens of milliseconds before a single router queues anything, and a player in another region will be at 150 ms no matter what you buy. Latency is a constant, and the job is to hide it, in a specific order, with each technique covering a specific visible artefact. A third mistake follows from working on one machine: localhost has a sub-millisecond round trip, no jitter and no loss, so every bug this skill exists to prevent is invisible until someone else plays.

## Scope

Use for: choosing an authority model, adding multiplayer to a game, diagnosing rubber-banding, warping, desync or missing hit registration, sizing tick and send rates, cutting bandwidth, picking a transport, deciding what the server must validate, and building a network test rig.

Do not use for: building or reviewing the game itself, including its feel and its frame budget — that is `game-builder`. A backend HTTP or RPC interface that happens to belong to a game is `api-design`. How many machines the fleet needs at launch is `capacity-planning`. A crash or logic bug that happens to show up in a networked build, with no networking in the causal chain, is `debugging`.

## Scale and game type

Scale here means what the work requires rather than a headcount or a budget: indie/A is one small team wearing every hat; AA adds specialised roles, several platforms and a publisher's milestones; AAA adds many specialised disciplines, external studios and a simultaneous multi-platform launch.

| | Indie/A | AA | AAA |
| --- | --- | --- | --- |
| Topology (step 1) | A listen server or peer connections — nobody is paying for a dedicated fleet | A small dedicated fleet, sized with `capacity-planning` | A global dedicated fleet, sized for a simultaneous launch |
| What's at stake (step 1) | Friends in a private lobby — client-authoritative is often acceptable | Ranked or monetised play, so server-authoritative is close to mandatory | Ranked, monetised and publicly scrutinised — anti-cheat investment scales with it |
| Testing (step 8) | Run the degraded-network profiles yourself before launch | A network QA pass runs the profile table per milestone build | The same, per platform, against a certification calendar |

Competitive multiplayer and live-service games are what this skill exists for — pick the authority model from step 2's table before writing a line of code. Rollback is specifically for fighting games and small-count reaction games, per the same table, and is the wrong choice for anything else.

## Workflow

### 1. Establish the five facts that decide the model

Ask for all five at once. Each one rules out at least one model, and getting them after the code exists is what makes netcode a rewrite.

- **Genre and its action class.** What does the player do that latency could ruin: aim at a moving target, issue an order, press a button on one frame of a 60 Hz animation, or take a turn? This decides the latency budget more than anything else.
- **Players per session.** Two, eight, sixty-four, or ten thousand. The determinism models get expensive fast with player count; the server-authoritative model gets expensive with server cost.
- **Topology.** Dedicated servers you run, a listen server hosted by one player, or peers connecting directly. Somebody pays for a dedicated fleet, and if nobody will, say so now rather than designing for one.
- **Platform.** A browser cannot open a UDP socket, which narrows the transport before anything else is decided. Consoles bring certification requirements for matchmaking and voice.
- **What is at stake.** Ranked play, real money, or friends in a private lobby. This is the only input that decides how much cheating costs, and it is the one people skip.

Write the answers down and state which model they imply before writing code.

### 2. Pick the authority model, and pick it from the table

| Model | Fits | Players | What it costs |
| --- | --- | --- | --- |
| Server-authoritative with prediction | Shooters, action, MMO, anything ranked, monetised or open to strangers | 2 to thousands | A server per session that you pay for, plus prediction and reconciliation code on the client. The default. |
| Deterministic lockstep | RTS and simulation games where world state dwarfs input — thousands of units, one order per second | 2 to 8 | Bit-exact determinism on every platform and build. Input delay is at least the slowest peer's one-way latency. One desync ends the match. |
| Rollback (deterministic plus speculation) | Fighting games and small-count action where reaction time is the game | 2, occasionally 4 | Determinism as above, plus saving and restoring complete game state every frame, cheaply enough to do it several times inside one 16 ms frame. |
| Client-authoritative | Co-op with friends, jam entries, anything with nothing to win | 2 to 8 | Every client can lie about everything it owns. Acceptable only when nobody cares if they do. |

Default to server-authoritative. The two deterministic models are not a better grade of netcode; they are a trade that buys tiny bandwidth and perfect responsiveness by spending determinism, and determinism is expensive in ways that surface late. Floating-point results differ across architectures, compiler flags, fused multiply-add contraction and library versions of `sin` and `pow`; a hash set iterated in insertion-dependent order desyncs as surely as arithmetic does.

Read `references/authority-models.md` before committing to a model. It carries the per-genre detail, the determinism checklist, what each migration between models actually costs, and the topology decision that goes with it.

### 3. Fix the three rates before writing the loop

They are three separate numbers and conflating them is the usual cause of either a bandwidth bill or a mushy game.

| Rate | What it decides | Where to start |
| --- | --- | --- |
| Simulation tick | Correctness and feel; the granularity of every collision and cooldown | 60 Hz for action, 30 Hz if the genre is forgiving, 120 Hz only if the physics needs it |
| Server send rate | Bandwidth, and the floor on the interpolation buffer | Equal to or a whole divisor of the tick; start at 20 to 30 Hz and raise it if the game is competitive |
| Client input rate | How stale the newest input the server has is | At the simulation tick, never below it, batched so a lost packet does not lose an input |

Shipped numbers, each from a source you can check:

- **Quake III Arena** runs the server at `sv_fps` 20, clients request 20 snapshots per second with `snaps`, and send up to 30 input packets per second with `cl_maxpackets`, under a `rate` cap of 3000 bytes per second. All four defaults are in the GPL source, `code/server/sv_init.c` and `code/client/cl_main.c`.
- **Valorant** targets a 128 Hz tick, described with its reasoning on the Riot Games tech blog in "VALORANT's 128-Tick Servers".
- **Overwatch** simulates at 62.5 Hz and originally sent updates at 20.8 Hz, one tick in three, before the high-bandwidth option raised the send rate to match the simulation — Tim Ford, GDC 2017, "Overwatch Gameplay Architecture and Netcode".
- **Rocket League** runs its physics at 120 Hz, which is why its prediction rewinds so much per frame — Jared Cone, GDC 2018, "It IS Rocket Science! The Physics of Rocket League Detailed".
- A **rollback fighting game** runs lockstep at the game's own 60 Hz and sends inputs only; there is no separate send rate.

Raising the tick rate is the expensive answer to almost every netcode complaint, and it is usually the wrong one. Halving the interpolation buffer or fixing a missing reconciliation step buys more responsiveness per unit of cost.

### 4. Hide the latency, in this order, and name the artefact each step removes

Build them in this order. Each one is only meaningful once the one before it exists, apart from interpolation, which is independent and the cheapest thing on the list.

1. **Client-side prediction.** The client applies its own input immediately to its own character instead of waiting for the server. Without it, every movement responds one round trip late, which is the "input lag" players report even at a good ping.
2. **Server reconciliation.** Every input carries a sequence number; the server acknowledges the last one it processed along with the resulting state; the client rewinds to that state and replays every input after it. Without it, prediction drifts from the server and the correction arrives as a snap — a character that walks into a wall on the client and is yanked back, which is rubber-banding.
3. **Entity interpolation.** Remote entities are rendered in the past, between the last two snapshots received, rather than at the newest one. Without it, other players move in discrete jumps at the send rate and teleport whenever a packet is late.
4. **Lag compensation.** When a client fires, the server rewinds the other entities to where that client saw them and resolves the shot there. Without it, players must lead their targets by their own ping, and shots that visually connect do nothing.

Size the interpolation buffer against jitter, not against taste. The floor is one send interval; two covers a single lost packet, which is the number Source uses as `cl_interp_ratio 2` over `cl_updaterate` — at a 64 Hz send rate that is 31 ms, and at the 20 Hz send rate of the older default it is the 100 ms that `cl_interp 0.1` encodes. Add the measured jitter of the connection on top, and adapt it per client rather than shipping one number for everyone.

Lag compensation is the one technique that makes somebody's experience worse. It is fair to the shooter and unfair to the target, who is shot after reaching cover, and it is the mechanism behind peeker's advantage — Riot's "Peeking into VALORANT's Netcode" works the geometry through. Cap the rewind window and refuse to compensate beyond it, because past a few hundred milliseconds the target is paying more than the shooter gains.

Read `references/prediction-reconciliation.md` while implementing any of the four. It has the input-sequencing protocol, the reconciliation loop, error smoothing, the rollback variant with its frame-delay trade, and the buffer arithmetic.

### 5. Fit a bandwidth budget you have actually computed

Three kinds of replication, and most games need all three:

- **Snapshot.** The full state of everything relevant, every send. Simple, stateless, and it recovers from loss for free because the next one is complete. Expensive.
- **Delta.** The difference against the last snapshot the client acknowledged. Quake III does exactly this: the server encodes against the frame the client acked, and falls back to a baseline when that ack is older than 29 of the 32 frames it keeps, or when its entity ring buffer has wrapped. The fallback is the part people leave out, and without it a client that drops packets for a second never recovers.
- **Event.** Things that happened rather than state that is: a door opened, a shot fired, an item picked up. These need reliable delivery, and they are where a reliable channel earns its place.

Compute the budget before optimising. Twenty visible entities at twenty bytes each, sent twenty times a second, is 8 KB/s to each client — about 64 kbit/s down, which is fine. The same server sending that to sixty-four players is 512 KB/s up per instance, which is a hosting decision. Do the multiplication for the real entity count before deciding anything is a problem.

The largest lever by far is area of interest: do not send what a player cannot perceive. After that comes quantisation — positions as fixed-point at the smallest unit that affects play, orientations as a compressed quaternion, velocity derived rather than sent — and then prioritisation, sending the most important objects that fit in the packet rather than everything late. `references/replication-and-transport.md` has the schemes and the numbers.

### 6. Choose the transport for what the data is

Use UDP for state. TCP's head-of-line blocking is the disqualifier: one lost packet stalls delivery of every newer packet that already arrived, and by the time the retransmission lands, the state it carried has been superseded. The correct recovery for state is to send the newer state, which TCP cannot be told to do.

Reliable ordered delivery is still right for authentication, matchmaking, chat, level load, economy and inventory transactions, and any event whose loss changes the outcome. Build those as reliable channels over the same UDP connection rather than opening a TCP socket alongside it; two connections means two congestion states and two failure modes for one session.

A browser cannot open a UDP socket at all. WebSockets are TCP and carry the head-of-line problem into a game loop. WebRTC data channels give unreliable unordered delivery when configured for it, at the cost of ICE, STUN, TURN and a signalling server. WebTransport over HTTP/3 gives both datagrams and streams on one connection with far less machinery, at the cost of needing HTTP/3 and a certificate the browser trusts, and of narrower browser support — check support for the actual target browsers before committing. Keep any datagram under about 1200 bytes of payload, because a fragmented UDP datagram is lost entirely when one fragment is.

### 7. Assume every client is lying

Anything the client is authoritative over is a thing the client can lie about. The rule that follows is that the server accepts intent and never results: an input, an aim direction, a request to pick something up.

| Cheat | What made it possible | What the server does instead |
| --- | --- | --- |
| Speed hack | The client integrated its own movement and reported the result | Re-simulate the move from the input with the server's own constants, and clamp displacement per tick |
| Teleport | The server accepted a position | Accept inputs; positions are output, never input |
| Rate of fire | The server trusted the client's timestamp | Enforce cooldowns against the server's tick counter, and clamp the client's claimed tick into an accepted window |
| Inflated damage | The client computed the damage | The client sends aim and fire; the server resolves the hit and the damage |
| Item and currency duplication | The client asserted an inventory change | The inventory lives on the server; the client's message is a request that can be refused |
| Wallhack and maphack | The client was sent state it should not be able to see | Not fixable by validation. Cull by visibility before sending, which is the same area-of-interest work as step 5 |

Validation decides what you accept; culling decides what you send; they cover different cheats and you need both. Rejecting an invalid input is better than correcting it silently, because a legitimate client hitting the rejection path is a bug you want to see. `references/cheating-and-testing.md` has the validation patterns per class and what to log.

### 8. Test on a degraded network, because localhost proves nothing

Two processes on one machine share a loopback with a sub-millisecond round trip, no jitter and no loss. Every artefact in step 4 is invisible there, which is why netcode bugs are found by players.

Run against a fixed set of profiles and keep them in the repository so results compare across builds:

| Profile | RTT | Jitter | Loss |
| --- | --- | --- | --- |
| Same city | 20 ms | 2 ms | 0% |
| Cross-country | 80 ms | 10 ms | 0.5% |
| Cross-ocean | 180 ms | 30 ms | 1% |
| Bad mobile | 250 ms | 80 ms | 5% |
| Broken | 120 ms | 20 ms | 10%, with reordering and duplicates |

Also test asymmetry — one client at 20 ms against one at 200 ms is where lag compensation's fairness cost becomes visible — and a two-second total freeze, which is what a Wi-Fi roam looks like.

The shaping is done outside the game. On Linux, `tc` with `netem` on the egress qdisc; on macOS, Network Link Conditioner from Apple's Additional Tools for Xcode, or `dnctl` with `pfctl`; on Windows, `clumsy`, which uses WinDivert and is the one tool here that shapes loopback, so two clients on one machine can be tested honestly. `comcast` wraps `tc` and `pfctl` behind one set of flags across Linux and macOS, and `pumba netem` does it for containers. `references/cheating-and-testing.md` carries the exact commands, including the `ifb` redirect that `netem` needs to shape inbound traffic, and the desync detector to run under these profiles for a deterministic model.

## Anti-patterns

**Deciding the authority model after the prototype works.** Sending positions between clients is the smallest change that makes two players see each other, and it is the one that costs a rewrite. Decide at the first line.

**Trusting a client-supplied position.** It is the single vulnerability that produces speed hacks, teleports and hit-registration exploits at once, and no amount of plausibility checking recovers it once the protocol carries positions.

**Prediction without reconciliation.** A predicted client that never replays against an authoritative state diverges continuously and is corrected in jumps. The rubber-banding players report is almost always this, not the network.

**Raising the tick rate to fix responsiveness.** It multiplies server cost and bandwidth for a linear improvement, and it hides the missing technique that was actually responsible.

**One interpolation buffer for everyone.** A fixed 100 ms penalises every player on a good connection to protect the worst one. Measure jitter per client and adapt.

**Lag compensation with no cap.** Rewinding a full second means a player on a deliberately bad connection kills people who have been behind cover for a second.

**TCP for game state.** It looks like it works in testing, because testing has no loss. The first 2% loss turns head-of-line blocking into a freeze.

**Determinism assumed rather than tested.** A lockstep or rollback game without a state hash compared every few frames does not find its desync until a match is lost. Build the detector before the netcode.

**Testing on localhost.** The whole class of bugs this skill addresses cannot occur there.

**A reliable channel for everything.** Reliability applied to position updates reintroduces head-of-line blocking over UDP, having paid for UDP.

## References

- `references/authority-models.md` — read at step 2, before committing to a model: the four models per genre and player count, the determinism checklist, topology and host migration, and what changing model later costs.
- `references/prediction-reconciliation.md` — read at step 4 while implementing any of the four latency-hiding techniques: the input-sequencing protocol, the reconciliation and rollback loops, error smoothing, and interpolation buffer arithmetic.
- `references/replication-and-transport.md` — read at steps 5 and 6: snapshot, delta and event replication, area of interest, quantisation, priority, budget arithmetic, and the transport options including the browser ones.
- `references/cheating-and-testing.md` — read at steps 7 and 8: server validation per cheat class, and the network conditioning commands per platform with the desync detector.
