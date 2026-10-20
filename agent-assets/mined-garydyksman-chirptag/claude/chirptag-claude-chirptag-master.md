
# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## First-time setup

Both `ChirpTag/LocalConfig.cs` and `ChirpTagFlagNode/LocalConfig.cs` are gitignored because they hold device-specific secrets (WiFi SSID/password, API URL). Each project ships a `LocalConfig.template.cs` with the required constants stubbed out. Before building, copy the template to `LocalConfig.cs` in each project folder and fill in the values for your device.

## Build

**Do not run `dotnet build`, `msbuild`, or any compile command on the `.nfproj` files** unless the user explicitly requests a build. Build and flash in Visual Studio using its nanoFramework extension. Use code review and static analysis to validate changes instead.

There are no automated tests in this repo.

## Architecture

### Target hardware

Two device types, both ESP32-S3, both running **.NET nanoFramework** (not standard .NET):

**Game device — Heltec Vision Master E219 (HT-VME213)**
- **SPI2** — LCM EN2R13 e-Paper display
- **SPI1** — SX1262 LoRa radio
- WiFi and LoRa cannot be active simultaneously — WiFi is torn down (`WiFiBootstrap.TearDownRadio()`) before LoRa starts. During gameplay, `WifiHttpBridge` briefly re-enables WiFi (pausing LoRa polling via callbacks) for HTTP calls, then tears it down again.

**Flag node — Heltec WiFi LoRa 32 V4**
- SSD1306 OLED display (I2C, 128×64) — lighter on heap than the e-Paper framebuffer
- SX1262 LoRa radio
- Pin mapping differs from the game device; `ChirpTagFlagNode` will have its own `Program.cs`

### Project layout

| Project | Role |
|---|---|
| `ChirpTag` | Game device firmware: hardware pin setup, boot sequence, button ISRs (Heltec Vision Master E219) |
| `ChirpTagFlagNode` | Flag node firmware: to be added (Heltec WiFi LoRa 32 V4) |
| `IOD.CaptureTheFlag.NanoFramework` | All game logic: state, LoRa messaging, display, HTTP client |
| `LoRaLib` | Low-level SX1262 driver (pre-built DLLs also in `ref/`) |

### Boot sequence (`Program.cs`)

1. **Phase 1** — power VEXT, init display + font (framebuffer allocated first to claim heap before WiFi/LoRa), connect WiFi, create HTTP client, poll server until a game exists.
2. **Phase 2** — register player name with server (or rejoin from the Active roster on mid-game reboot); poll until game is Active.
3. **Phase 3** — tear down WiFi radio, init LoRa, construct `GamerDevice`, call `OnGameStart()`, enter the main button-poll loop (25 ms sleep).

### Threading model in `GamerDevice`

Three background threads start at `OnGameStart()`:
- **HeartbeatLoop** — broadcasts a `Heartbeat` LoRa packet every 5 s while the player is alive.
- **TxLoop** — drains `TxQueue` (capacity 8) to LoRa every 500 ms.
- **UiLoop** — refreshes the e-Paper HUD every 1 s; diffs the combat list snapshot to avoid unnecessary redraws.

The main thread polls `_attackRequested` / `_cycleTargetsRequested` (set in GPIO ISRs) at 25 ms and dispatches to `GamerDevice`.

Cross-thread signalling uses `_crossThreadSignalLock` + plain `bool` fields — nanoFramework does not support `volatile`.

### LoRa packet wire format

```
[ fromDeviceId (1) | msgType (1) | targetId (1) | ...data | crc (1) ]
```

`targetId == 0x00` means broadcast. `MessageHandler` validates exact length (per `PacketParser.ExpectedLength`) and CRC before routing. All packet types are constants in `PacketType.cs`.

During a combat radio window (`IsCombatRadioWindow == true`), non-combat packets are silently dropped in `OnLoRaPacketReceived` to keep the LoRa channel clean for `AttackAck` / `CombatResult` / `RespawnAck`.

### Configuration

Two-layer merge, evaluated at boot:
1. **`AppSettingsBuiltIn.cs`** — a single minified JSON string compiled into the firmware. This is the canonical default for a given device build.
2. **`I:\appsettings.json`** on device flash (SPIFFS) — optional overlay; only non-empty/non-false fields overwrite built-in values.

When changing device defaults, edit `AppSettingsBuiltIn.cs` **and** keep `appsettings.sample.json` in sync (same logical content). The sample file is not loaded at runtime; it exists for reference and tooling.

Settings fields: `playerName`, `wifiSsid`, `wifiPassword`, `gameApiBaseUrl`, `gameApiSslNoVerify`, `allowHudWithoutValidDeviceId`, `ignoreAttackRangeLimit`.

### Flag node responsibilities

`IFlagNode` is already defined in `IOD.CaptureTheFlag.NanoFramework`. The flag node implementation needs to handle these LoRa packets: `Capture` (send `KeyGrant` back to player), `Deliver` (accept key + report to server), `RespawnReq` (fetch respawn number via HTTP + send `RespawnAck`). The key is issued by the HTTP server — the flag node fetches it at game start, not generates it locally.

### Key implementation notes

- **Memory budget is tight on game devices.** All hot-path arrays in `GameStateManager` and `GamerDevice` are pre-allocated at construction (`MaxPlayers = 16`, `MaxDeviceId = 256`). Avoid `new` in loops or LoRa RX callbacks.
- **Combat resolution** — higher `CombatScore` wins; wraparound rule: score 1 beats score 10.
- **Device types** — `DeviceType.Player` (`0x01`) and `DeviceType.FlagNode` (`0x02`). Pressing the attack button against a flag node triggers a Capture or Deliver interaction instead of combat.
- **`GameStateManager._playerNames`** — populated from the HTTP roster at game start; heartbeat-supplied names only fill gaps (roster takes precedence).
- **Conditional logging** — `[Conditional("GAMER_DEVICE_TRACE")]` gates `GamerDevice` verbose logs; `[Conditional("VERBOSE_GAMESTATE")]` gates `GameStateManager` logs. `CombatListDiagnostics.Enabled` is a runtime boolean for combat list tracing.
