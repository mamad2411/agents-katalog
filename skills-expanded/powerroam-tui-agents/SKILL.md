# AGENTS.md — powerroam-tui

Go CLI + Bubble Tea TUI for controlling the PowerRoam GS600 power station over BLE.

---

## Build & Run

```bash
# Build (CGO_ENABLED=0 required — repo path contains spaces, breaks CGO linker)
CGO_ENABLED=0 go build -o powerroam-tui

# Run (requires a real BLE adapter)
./powerroam-tui tui
./powerroam-tui scan
./powerroam-tui send --device "PowerRoam GS600" --cmd 0x09
```

## Test Commands

```bash
# Run all tests
go test ./...

# Run tests in a single package (verbose)
go test ./internal/protocol -v

# Run a single named test
go test ./internal/protocol -v -run TestCRC16Modbus
go test ./internal/protocol -v -run TestBuildPacket
go test ./internal/protocol -v -run TestParsePackets

# Run with race detector
go test -race ./...
```

Tests live only in `internal/protocol/packet_test.go`. There is no test runner config file; standard `go test` flags apply.

## Format & Lint

```bash
# Format (no config file — standard gofmt)
gofmt -w .

# Vet
go vet ./...

# Lint (if golangci-lint is available)
golangci-lint run
```

There are no `.golangci.yaml`, `.editorconfig`, or other style config files. All style is governed by standard `gofmt` + Go idioms.

---

## Project Structure

```
main.go                      # CLI entry point; all Cobra subcommands
go.mod / go.sum              # Module definition and lockfile
internal/
  ble/ble.go                 # BLE transport: scan, connect, send, notify
  protocol/
    crc.go                   # CRC-16/Modbus algorithm
    commands.go              # Command IDs, constants, request builders
    decoder.go               # Response payload decoders
    packet.go                # Packet builder/parser, utility functions
    packet_test.go           # Unit tests
  state/state.go             # Thread-safe StationState struct
  transport/transport.go     # Transport interface definition
  tui/
    run.go                   # RootModel phase switcher; Run() entrypoint
    connection.go            # ConnectionModel — spinner + BLE scan/connect
    main_model.go            # MainModel — tab bar, notification goroutine, 2s polling
    dashboard.go             # DashboardModel — SOC, power readings
    settings.go              # SettingsModel — 12 settings, ↑↓←→ nav, Enter to send
    device_info.go           # DeviceInfoModel — SN, firmware, WiFi
    flashlight.go            # FlashlightModel — Off/Low/High/Strobe/SOS radio
    auto_shutdown.go         # AutoShutdownModel — stub (TODO)
    messages.go              # All tea.Msg types
    styles.go                # lipgloss palette, named styles, layout constants
```

---

## Code Style Guidelines

### Formatting
- Standard `gofmt`. No exceptions, no custom line-length limit.
- Tabs for indentation (enforced by gofmt).
- Blank lines separate logical sections within a function, not just between top-level declarations.

### Imports
Group imports in this order with blank-line separators (matches `goimports` style):

```go
import (
    "encoding/binary"   // 1. stdlib
    "fmt"

    "github.com/charmbracelet/bubbletea"  // 2. third-party

    "powerroam-tui/internal/protocol"     // 3. internal (module-relative)
)
```

Never dot-import. Never blank-import unless registering a side-effect driver.

### Naming Conventions

| Category | Convention | Example |
|---|---|---|
| Types | PascalCase | `StationState`, `ConnectionModel` |
| Exported functions | PascalCase | `BuildPacket`, `CRC16Modbus` |
| Unexported functions | camelCase | `parseOnePacket`, `dispatchTelemetry` |
| Constants | PascalCase with descriptive prefix group | `CmdBatteryInverter`, `BrightnessHigh` |
| Variables | camelCase | `deviceName`, `notifyChan` |
| Receiver names | Single letter matching type initial | `m` for models, `b` for BLE, `s` for state |
| Test functions | `Test<Subject>` | `TestCRC16Modbus`, `TestParsePackets` |

### Types
- Prefer concrete types over `interface{}` / `any`.
- Byte-level wire format: use `[]byte`, `[2]byte` arrays, `uint16` with explicit endianness via `encoding/binary`.
- Hex constants written as `0xA1`, `0xC0` (never decimal for protocol bytes).
- Use named constants for all protocol command IDs and mode values; never bare magic numbers.

### Error Handling
- `if err != nil { return ..., fmt.Errorf("context: %w", err) }` — always wrap errors.
- Fatal errors inside goroutines: log to `/tmp/tui-debug.log` then send a typed error message (`MsgSendError`) back to the TUI program; do not `log.Fatal`.
- Never swallow errors silently.
- Use `t.Fatalf` in tests when subsequent assertions would be meaningless; `t.Errorf` otherwise.

### Concurrency
- `StationState` fields are protected by `sync.RWMutex`; always acquire the appropriate lock.
- Only the `startNotificationListener` goroutine (in `main_model.go`) may call `sendMsg()` (a `func(tea.Msg)` closure).
- The `sendMsg` closure is created in `Run()` and passed to `MainModel` via `NewMainModel()`. This closure captures `p *tea.Program` by reference, allowing safe message injection from background goroutines without the chicken-and-egg problem of assignment-after-construction.
- Use buffered channels (`chan []byte`) for BLE notification delivery.
- Cancel goroutines via `context.Context`; drain channels before closing.
- Non-blocking operations: call cleanup functions (e.g., `transport.Disconnect()`) in a fire-and-forget goroutine before returning a final event (e.g., `tea.Quit`) to avoid blocking the event loop.

### Comments
- All exported types and functions must have a doc comment (`// TypeName ...`).
- Protocol byte layouts belong in a comment directly above the relevant `case` block in `decoder.go`.
- Inline comments explain *why*, not *what*.

---

## TUI Architecture

The `tui` package implements the Elm architecture (Model / Update / View) via Bubble Tea.

```
main.go  →  tui.Run(addr)
              │
              └─ RootModel
                   ├─ phase: "connecting"  →  ConnectionModel
                   └─ phase: "main"        →  MainModel
                                                 ├─ DashboardModel
                                                 ├─ SettingsModel
                                                 ├─ DeviceInfoModel
                                                 ├─ FlashlightModel
                                                 └─ AutoShutdownModel
```

### Data flow

```
BLE device
    │  raw bytes
    ▼
transport.Notifications() channel
    │
    ▼  (goroutine: startNotificationListener)
protocol.ParsePackets → DecodePayload → state.StationState.Update*()
    │
    └─ sendMsg(MsgTelemetry{})  [closure safe from any goroutine]
              │
              ▼  (Bubble Tea loop)
         MainModel.Update()
              │
              └─ dispatchTelemetry() → all tab models updated
```

### Tab model contract

Every tab model must satisfy value-receiver methods:

```go
func (m TabModel) Init() tea.Cmd
func (m TabModel) Update(msg tea.Msg) (TabModel, tea.Cmd)
func (m TabModel) View() string
```

`MsgTelemetry` is dispatched to **all** tab models via `dispatchTelemetry()` regardless of which tab is active. Only view rendering is skipped for inactive tabs.

---

## Architecture Invariants (do not break)

### Two-phase root
`RootModel` holds either a `ConnectionModel` or a `MainModel`. On `MsgConnected` it swaps. Do not collapse these phases — the connection spinner needs its own independent update loop.

**Critical:** When transitioning to a new model in `RootModel.Update()`, return the new model's `Init()` as the command, not a call to its `Update()`:
```go
// ✗ WRONG: skips Init(), background goroutines never start
return m.mainModel.Update(msg)

// ✓ CORRECT: schedules Init() so all tea.Cmd are scheduled
return m, m.mainModel.Init()
```

This ensures all background tasks (e.g., `startNotificationListener`, `fetchInitialData`) are scheduled properly in the Bubble Tea event loop. Skipping `Init()` is a common source of silent bugs where goroutines never start and the UI displays stale or zero data.

### Goroutine → sendMsg closure
`MainModel` spawns one long-running goroutine (`startNotificationListener`) that reads BLE notifications, decodes packets, updates `*StationState`, sends `MsgTelemetry`, and polls every 2 s for `CmdBatteryChargingInfo`. This is the **only** place allowed to call the `sendMsg` closure captured from `Run()`.

### Tab models are value types
All tab models use value receivers and return updated copies. `MainModel` stores them as plain struct fields (`m.dashboard`, `m.settings`, …) and **must reassign** after every `Update()` call.

### dispatchTelemetry must update ALL tabs
`dispatchTelemetry()` passes `MsgTelemetry` to every tab model and returns the updated `MainModel`. The caller must do `m = m.dispatchTelemetry(msg)`. Updating only the active tab is a bug (was fixed once already).

### Send command lifecycle
Tab emits `tea.Cmd` → closure calls `transport.Send()` → returns `MsgSendDone{}` or `MsgSendError{}` → `Update()` clears `m.sending`. A send closure that returns `nil` will leave `m.sending = true` permanently. Always return one of the two message types.

### Enum settings: using the same constants for send and receive
All enum settings (Operating Mode, Brightness, Screen Timeout, DC Charge Current, Low Battery Alert) must use the **exact same protocol constants** defined in `internal/protocol/commands.go` for both sending and receiving. This is critical to prevent mismatches where the UI label order differs from the wire byte order.

**Pattern for sending enum settings** (`internal/tui/settings.go` → `sendSettingCommand`):

1. Get the selected UI label string: `selectedValue := setting.options[setting.index]`
2. Define a map from UI label string to the protocol constant byte:
   ```go
   brightnessMap := map[string]byte{
       "Low":      protocol.BrightnessLow,      // 0x02
       "Standard": protocol.BrightnessStandard, // 0x01
       "High":     protocol.BrightnessHigh,     // 0x00
   }
   ```
3. Look up the label in the map: `b, ok := brightnessMap[selectedValue]`
4. Pass the constant to the `Set*Req()` function: `protocol.SetDisplayBrightnessReq(b)`

**Never use `byte(setting.index)` as a wire value.** The UI option list order is determined by UX (e.g., grouping Low before High), not by protocol byte values. Blindly casting index to byte creates silent bugs when the list order doesn't match the wire constants.

**Receiving side** (`internal/protocol/decoder.go`):
Uses the same constants in reverse (byte → string map) when decoding responses. The `syncStateToUI()` function in `SettingsModel` then finds the matching UI label via `syncEnumSetting()`, which does an exact string match with the constant-derived values.

This dual-mapping approach ensures the UI label always round-trips correctly: label (send) → constant byte → wire → constant byte (receive) → label (display).

### Transport interface
```go
type Transport interface {
    Connect(ctx context.Context) error
    Disconnect() error
    Send(data []byte) error
    Notifications() <-chan []byte
    IsConnected() bool
    Name() string
}
```
All new transports (mock, WebSocket) must satisfy this interface. BLE is the only current implementation.

---

## Known Incomplete Areas

- `cmd/` directory — empty placeholder for a future command split from `main.go`.
- Debug logging to `/tmp/tui-debug.log` is present in `main_model.go` and `settings.go`; remove before shipping.

---

## Key Dependencies

| Package | Purpose |
|---|---|
| `github.com/spf13/cobra` | CLI subcommand framework |
| `tinygo.org/x/bluetooth` | BLE (BlueZ D-Bus on Linux) |
| `github.com/charmbracelet/bubbletea` | TUI event loop (Elm architecture) |
| `github.com/charmbracelet/bubbles` | Spinner component |
| `github.com/charmbracelet/lipgloss` | Terminal styling and layout |
| `github.com/godbus/dbus/v5` | BlueZ backend (indirect) |
