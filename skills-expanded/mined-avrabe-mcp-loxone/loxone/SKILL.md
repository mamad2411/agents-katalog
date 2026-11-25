---
name: loxone
description: Control Loxone smart home devices — lights, blinds, climate, security, audio, and more.
---

You have access to a Loxone smart home via the `loxone-cli` command. It connects to a running MCP server that maintains a persistent connection to the Loxone Miniserver.

## Commands

### Discovery
```bash
loxone-cli rooms                          # List all rooms
loxone-cli devices                        # List all devices
loxone-cli devices --room "Kitchen"       # List devices in a room
loxone-cli device "Living Room Light"     # Get device details
loxone-cli status                         # Server and connection status
```

### Lighting
```bash
loxone-cli lights                         # Show all lights status
loxone-cli lights on --target "Kitchen"   # Turn on kitchen lights
loxone-cli lights off --target "Bedroom"  # Turn off bedroom lights
loxone-cli lights dim --target "Living Room" --brightness 50
```

### Climate
```bash
loxone-cli climate                        # Show all climate status
loxone-cli climate --set 22 --room "Bedroom"
loxone-cli climate --set 20 --room "Office" --mode heat
```

### Blinds
```bash
loxone-cli blinds                         # Show all blinds status
loxone-cli blinds up --target "Living Room"
loxone-cli blinds down --target "Bedroom"
loxone-cli blinds stop --target "Kitchen"
```

### Audio
```bash
loxone-cli audio                          # Show audio zones
loxone-cli audio play --zone "Kitchen"
loxone-cli audio pause --zone "Kitchen"
loxone-cli audio --volume 60 --zone "Living Room"
```

### Sensors
```bash
loxone-cli sensors                        # All sensor readings
loxone-cli doors                          # Door/window status
loxone-cli motion                         # Motion detectors
loxone-cli weather                        # Weather station
loxone-cli energy                         # Energy consumption
```

### Security
```bash
loxone-cli security                       # Show security status
loxone-cli security arm                   # Arm alarm
loxone-cli security disarm --code 1234    # Disarm with code
loxone-cli lock "Front Door" lock         # Lock door
loxone-cli lock "Front Door" unlock       # Unlock door
```

### Scenes
```bash
loxone-cli scenes                         # List available scenes
loxone-cli scene "Good Night"             # Activate scene
loxone-cli scene "Movie" --room "Living Room"
```

### Advanced
```bash
loxone-cli tools                          # List all available MCP tools
loxone-cli call get_weather               # Call any tool by name
loxone-cli call set_temperature room="Kitchen" temperature=21.5
loxone-cli --json rooms                   # Get raw JSON output
```

## Safety Rules

1. **Temperature**: Only set values between 16-28C unless the user explicitly requests otherwise
2. **Security**: Always confirm with the user before disarming alarms or unlocking doors
3. **Scenes**: Describe what a scene will do before activating it
4. **Blinds**: Warn if closing all blinds (could block emergency exits)
5. **Audio**: Don't set volume above 80% without confirmation

## Notes

- The CLI auto-starts the MCP server if it's not running
- Add `--json` for machine-readable output
- The server maintains a persistent connection to the Miniserver for fast responses
