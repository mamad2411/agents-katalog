# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

A Unity LAN co-op game ("Psychedelia"). Two friends land in a desert, find a suitcase full of drugs, and after taking them the trip turns into a surreal adventure. The design centers on two-player cooperation and exploring the "other side of reality." UI strings, comments, and log messages are in Polish.

- **Engine:** Unity `6000.3.11f1` (Unity 6). Open the project folder in the Unity Editor that exact version; there is no command-line build/test setup — building, running, and Play-mode testing all happen through the Editor.
- **Render pipeline:** URP 17.3 (`DefaultVolumeProfile.asset`, custom `ScriptableRendererFeature`s).
- **Networking:** Netcode for GameObjects 2.0 over Unity Transport (UTP), LAN only.
- **Scenes:** `Assets/Scenes/Menu.unity` (entry, hosts the LAN menu + `NetworkManager`) and `Assets/Scenes/Pustynia.unity` (the desert gameplay scene, value of `gameSceneName`).

All gameplay code lives in `Assets/Scripts/`. Everything else under `Assets/` is art/material/scene data. `Library/` is committed but is Unity's regenerable cache — ignore it. Note the loose `*CommandBuffer*.cs` / `I*CommandBuffer.cs` files in the repo root are Unity SRP auto-generated artifacts accidentally committed; they are not part of the game.

## Networking architecture

The connection/session flow is the most important cross-file concept:

1. **`Networking/LanMainMenu.cs`** — IMGUI (`OnGUI`) main menu. Configures `UnityTransport.SetConnectionData(address, port, listenAddress)`, enables scene management + connection approval, then calls `StartHost()`/`StartClient()`. The host loads `gameSceneName` via the networked `SceneManager`.
2. **`Networking/NetworkSessionManager.cs`** — server-authoritative session controller. Registers a `ConnectionApprovalCallback` that caps the lobby at `maxPlayers` (2). It does **not** use `CreatePlayerObject`; instead it queues connected clients (`pendingClients`) and manually spawns a per-role prefab (`hostPlayerPrefab` vs `clientPlayerPrefab`) once the game scene is active, assigning spawn positions by sorted client-id index. Spawn points are taken from the `spawnPoints` array, or auto-discovered from **`NetworkSpawnPoint`** components in the scene if that array is empty.
3. **`Networking/NetworkSpawnPoint.cs`** — marker component for spawn locations.
4. **`Networking/PsychedeliaNetworkTransform.cs`** — custom `NetworkTransform` for syncing player/object movement.
5. **`Networking/InGameMenu.cs`** — in-game pause/disconnect UI.

**Ownership pattern:** player-controlled `NetworkBehaviour`s (e.g. `PlayerInteractor`, `PlayerMovement`) disable themselves on non-owners in `OnNetworkSpawn` (`if (!IsOwner) enabled = false;`), so input/camera/UI logic only runs for the local player. Client→server actions go through `ServerRpc`s.

## Interaction & co-op mechanics (`Assets/Scripts/Interaction/`)

- **`PlayerInteractor.cs`** — owner-only. Center-screen raycast for interactables; drives FOV zoom, a procedurally generated vignette overlay, and Polish IMGUI prompts. Two interaction types: collecting "żaba" (frog) collectibles, and "ready"-gated interactables.
- **`InteractableSync.cs`** — networked interactable requiring **both players** to signal ready (`SetReadyServerRpc`) before it triggers — the core co-op gating primitive.
- **`ZabaCollectible.cs` / `ZabaLocal.cs`** — networked vs local frog objects.
- **`ZabaCounterManager.cs`** — tracks collected frogs and gates whether collecting is active (`IsActive`); found via `FindInScene()`.
- **`ZabaRainManager.cs`** — lazy singleton (`Instance`, `DontDestroyOnLoad`) managing a pooled "frog rain" effect.

When adding interactables, follow the existing split: server-authoritative state on a `NetworkBehaviour`, owner-only input/UI on the player, mutations via `ServerRpc`.

## Boss arena — "Odrealnienie" (`Assets/Scripts/Boss/`)

A second gameplay scene: a surreal, effect-saturated boss fight. **The host presses `P` in `Pustynia`** and `BossArenaTeleport.cs` triggers a networked `SceneManager.LoadScene("Odrealnienie", Single)`, so both players' (persistent, migrated) `NetworkObject`s follow.

- **`BossArenaController.cs`** — in-scene `NetworkObject`, server-authoritative state machine (`NetworkVariable<ArenaState>` Fighting/GameOver/Victory). On scene load it repositions both players onto the scene's `NetworkSpawnPoint`s (same sorted-client-id logic as `NetworkSessionManager`) facing the boss, resets their down state, tracks all-downed → GameOver, boss death → Victory, and exposes a host-only `RetryServerRpc` that reloads the arena scene for a clean reset. `static Instance` for discovery.
- **`BossController.cs`** — `NetworkBehaviour` on the in-scene boss (`Human.fbx`). HP `NetworkVariable`, takes damage from `ShotgunBall`, and on a timer telegraphs + fires a laser at a random non-downed player (`PlayerDownState.DownServer()`); dodge-able during the telegraph. Laser visual = runtime `LineRenderer` via `ClientRpc`.
- **`PlayerDownState.cs`** / **`ShotgunWeapon.cs`** / **`ShotgunBall.cs`** — added to the **player prefabs** by the builder. Down/revive (hold `E` near a downed teammate → `ReviveServerRpc`, no bleed-out); owner-only left-click fires one large **networked ball** projectile (`ShotgunBall`, a registered network prefab) via `FireServerRpc`; the shotgun model/weapon is active only while a `BossArenaController` exists. `PlayerDownState` also provides the server→owner teleport used for repositioning.
- **`BossArenaHud.cs`** — in-scene IMGUI: boss HP bar, GAME OVER / "Wygraliście!" overlay, host-only "Spróbuj jeszcze raz" button.

**Scene/prefab assembly is done by an Editor builder, not hand-authored:** run **`Psychedelia ▸ Build Boss Arena`** (`Assets/Scripts/Editor/BossArenaBuilder.cs`). It creates `Odrealnienie.unity` + arena geometry/materials (kaleidoscope shader), builds `Boss.prefab` + `ShotgunBall.prefab` (registering the ball in `DefaultNetworkPrefabs.asset`), injects the combat components + shotgun viewmodel into both `Player - *.prefab`s, adds the `BossArenaTeleport` to `Pustynia`, and registers both scenes in Build Settings. **Re-run it after pulling these scripts fresh** — without it the scene/prefab wiring does not exist.

## Rendering (`Assets/Scripts/Rendering/`)

Custom URP `ScriptableRendererFeature`s using the **RenderGraph** API (`RecordRenderGraph`), the Unity 6 path — not the legacy `Execute` API:
- **`ScreenBlurFeature.cs`** — fullscreen blur driven by the global shader property `_PsychedeliaBlurStrength`.
- **`OutlineHighlight.cs`** — interactable outline highlighting.

## Conventions

- Code and identifiers are English; user-facing text and many `Debug.Log` messages are Polish — keep that split.
- Prefer `FindObjectsByType(..., FindObjectsSortMode.None)` (Unity 6 API) over the obsolete `FindObjectsOfType`.
