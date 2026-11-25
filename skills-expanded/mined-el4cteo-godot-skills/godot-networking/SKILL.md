---
name: godot-networking
description: Networking in Godot 4.7 - high-level multiplayer (ENet, WebSocket, WebRTC), server-authoritative design, @rpc / [Rpc] modes, MultiplayerSpawner and MultiplayerSynchronizer replication, authority, authentication, dedicated headless servers, interpolation, security rules, plus HTTPRequest/REST, raw TCP/UDP/WebSocket. Use for online or LAN multiplayer, co-op, lobbies, or calling web APIs.
license: MIT
compatibility: Godot 4.7+ (GDScript and C#).
metadata:
  author: godot-agent-skills
  version: "1.1.0"
---

# Networking (4.7)

## Architecture first
- **Server-authoritative.** The server (or listen host) owns game state. Clients send *inputs and requests*, never results ("I picked up item 42", not "my gold is 9999").
- Peer IDs: the server is always `1`. `multiplayer.get_unique_id()`, `multiplayer.is_server()`, `multiplayer.get_peers()`. Signals: `peer_connected/peer_disconnected` (all) and `connected_to_server/connection_failed/server_disconnected` (clients).
- Transports (all are `MultiplayerPeer`, so swapping is trivial): `ENetMultiplayerPeer` (UDP, desktop and mobile, the default choice), `WebSocketMultiplayerPeer` (web clients; host needs TLS for https pages), `WebRTCMultiplayerPeer` (P2P, needs signaling), and Steam through the GodotSteam extension.
- Dedicated server: export with the `dedicated_server` feature (Export → Resources → "Dedicated Server" strips visuals) and run with `--headless`. Branch with `OS.has_feature("dedicated_server")` or `DisplayServer.get_name() == "headless"`.

## RPCs
- GDScript: `@rpc("any_peer" | "authority", "call_local" | "call_remote", "reliable" | "unreliable" | "unreliable_ordered", channel)`. Call with `rpc(&"method", args)` (everyone) or `rpc_id(peer, &"method", args)`. The default `@rpc` is authority-only, call_remote and reliable.
- C#: `[Rpc(MultiplayerApi.RpcMode.AnyPeer, CallLocal = true, TransferMode = MultiplayerPeer.TransferModeEnum.Reliable)]`, then `Rpc(MethodName.Fire, dir)` / `RpcId(1, MethodName.Fire, dir)`.
- The method must exist with the same RPC config on every peer, at the **same node path**. Spawn replicated nodes through MultiplayerSpawner so names and paths match.
- Inside an RPC, `multiplayer.get_remote_sender_id()` tells you who called. **Validate every `any_peer` RPC on the server**: is the sender allowed, is the value sane, is it rate-limited?
- Use `unreliable` for frequent state (positions), `reliable` for events (damage, chat, spawn requests) and `unreliable_ordered` for streams where old packets are useless. Use separate channels for unrelated reliable streams so they don't block each other.

## Replication nodes (prefer them to hand-written RPC sync)
- `MultiplayerSpawner`: set `spawn_path` (the parent node) and `add_spawnable_scene("res://player.tscn")`, or a `spawn_function` for custom data. Only the authority adds children (or calls `spawn(data)`), and clients get them automatically. The `spawned` signal fires on clients.
- `MultiplayerSynchronizer`: set `root_path` and a replication config with properties such as `.:position` and `Sprite2D:flip_h`. Each property has a mode: spawn-only, `ON_CHANGE` (watch) or `ALWAYS` (sync). Tune `replication_interval`/`delta_interval`. Control interest with `public_visibility = false` + `set_visibility_for(peer, true)` or `add_visibility_filter(callable)`.
- **Authority:** call `set_multiplayer_authority(peer_id)` on a player's node (recursive by default) so that client's input synchronizer sends its data. Check `is_multiplayer_authority()` before reading local input. A common split is client authority over an input-only synchronizer node while the server keeps authority over state.
- Smooth remote entities: interpolate received positions toward the latest snapshot in `_process`, or buffer two snapshots. Never snap.

## Auth and safety
- `SceneMultiplayer.auth_callback` + `send_auth`/`complete_auth` runs a handshake (version check, token) before a peer counts as connected.
- Keep `SceneMultiplayer.allow_object_decoding = false` (the default). Never send Objects or Resources over the network.
- Never `load()` paths or `str_to_var` data that came from peers. Don't `call()` method names received from the network.
- Limit how many players can connect (`create_server(port, max_clients)`), and handle disconnects mid-game: despawn their nodes on the server.

## HTTP and web APIs
- `HTTPRequest` node: `request(url, headers, method, body)`, then `request_completed(result, code, headers, body)`. Parse with `JSON.parse_string(body.get_string_from_utf8())`. Use one request at a time per node (create more nodes for parallel requests), and set `timeout`.
- TLS is automatic for https. For custom CAs use `TLSOptions.client(trusted_cert)`.
- Lower level: `HTTPClient` (streaming), `WebSocketPeer` (`connect_to_url`, call `poll()` every frame), `StreamPeerTCP` (4.6+: `poll()`/`get_status()` live on `StreamPeerSocket`), `PacketPeerUDP` and `StreamPeerUDS` (Unix sockets, 4.6+).
- Never ship secret API keys in the client. Route them through your own backend.

## Testing locally
Debug → "Customize Run Instances" in the editor can launch several instances with different arguments (`--server`, `--client`). From the CLI, start one headless server process plus GUI clients. `run_godot.py smoke` covers a headless server boot.

Lobby (ENet host/join), spawner + synchronizer player, validated RPCs, HTTP client, C# RPCs (compiled by the tests): [references/patterns.md](references/patterns.md)
