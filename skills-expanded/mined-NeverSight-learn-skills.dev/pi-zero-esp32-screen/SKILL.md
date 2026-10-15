---
name: pi-zero-esp32-screen
description: "Orange Pi Zero 2W + ESP32-S3 (FNK0104) USB CDC peripheral platform. Use when working on the OPi+ESP32 hardware setup: Jarvis voice assistant, opi-peripheral firmware, ESP32 serial protocol, TFT display rendering, mic capture, sprite animation, delta rendering, or deploying Go apps to the Orange Pi. Triggers on ~/projects/jarvis/, opi-peripheral firmware, CMD_FRAME_RECT, RSP_MIC_DATA, serial protocol debugging, or any OPi+ESP32 peripheral work. This is a general-purpose compute+display+audio platform -- not just Jarvis. DO NOT trigger for general Go questions (use effective-go), generic ESP32 projects (use cyd-app), or web/frontend work."
---

# Jarvis Device Development

Orange Pi Zero 2W (ARM64, Armbian) + ESP32-S3 (FNK0104) connected via USB CDC. The OPi runs a Go binary that orchestrates voice + display. The ESP32 is a dumb peripheral exposing hardware over a binary serial protocol.

## Architecture

```
[OPi Go binary] --USB CDC--> [ESP32 firmware]
                               |- TFT 320x240 (ILI9341, BGR565)
                               |- ES8311 mic+speaker (I2S)
                               |- WS2812B LED (1x)
                               |- 4 buttons (GPIO 2,3,14,21)
```

- **Go app**: ~/projects/jarvis/ -- wake word, VAD, STT, Claude session, TTS, sprite rendering
- **Firmware**: ~/projects/raspdeck-learning/builder-area/devices/opi-peripheral/
- **Brain workspace**: ~/jarvis/ (CLAUDE.md + fleet scripts, where `claude -p` runs)
- **Sprites**: ~/projects/jarvis/sprites/ (go:embed, RGB565 LE .raw files from clawd-art)
- **Config**: ~/.config/jarvis/config.json on the Orange Pi

## Serial Protocol

Binary packets: `[CMD:1][LEN:4 LE][PAYLOAD:LEN bytes]`

| Command | Code | Payload |
|---------|------|---------|
| CMD_FRAME_RECT | 0x02 | RectHeader(x,y,w,h as u16 LE) + pixel data |
| CMD_BACKLIGHT | 0x03 | brightness: 1 byte (0-255) |
| CMD_MIC_START | 0x12 | empty |
| CMD_MIC_STOP | 0x13 | empty |
| CMD_LED_SET | 0x20 | r,g,b bytes |
| CMD_RESET | 0xFF | empty |

| Response | Code | Payload |
|----------|------|---------|
| RSP_MIC_DATA | 0x81 | PCM16 mono ~1600 bytes |
| RSP_BTN_EVENT | 0x80 | gpio:1, state:1 (0=pressed) |
| RSP_READY | 0xF0 | version string (null-terminated) |
| RSP_ACK | 0xA0 | cmd_acked:1 |
| RSP_ERROR | 0xE0 | error string |

## Hard Constraints (Break These = Hours of Debugging)

1. **NEVER send display commands while mic is active.** Mic data (RSP_MIC_DATA) and display writes (CMD_FRAME_RECT) share the same USB CDC serial port. Concurrent access corrupts packets. Display only when mic is off.

2. **Use delta rendering for sprite animation.** Diff at the 16x16 source pixel level, send only changed 8x8 blocks as tiny CMD_FRAME_RECT packets (~136 bytes). Full 32KB frames are too slow and 32KB single packets timeout.

3. **8-row strips (2056 bytes) with 12ms pacing** for full frame draws. 16-row strips (4104 bytes) garble -- they exceed SMALL_PAYLOAD_MAX. Single 32KB packets cause firmware read timeouts.

4. **Firmware must NOT call Serial.flush()** in send_packet(). Blocks on every ACK response, kills throughput. Removed in v1.4.

5. **I2S mic reads must happen on Core 1** (same core as i2s.begin() in setup()). Core 0 returns garbage. I2S is core-affine on ESP32-S3.

6. **Serial port number increments on USB replug** (ttyACM0 -> ACM1 -> ACM2). Always auto-detect: scan /dev/ttyACM* and use the highest-numbered.

7. **Sprite pixel format**: Raw files are RGB565 LE. Display needs byte-swapped (swap byte ORDER, not color channels). Magenta 0xF81F = transparent sentinel -> replace with black (0x0000).

## Display Rendering Patterns

### Delta rendering (the fast path)
```go
// Compare source pixels (16x16 uint16 array) against last rendered frame
// Only send 8x8 blocks for changed pixels
for i := 0; i < 256; i++ {
    if src[i] != lastSrc[i] {
        // Send CMD_FRAME_RECT for this 8x8 block (136 bytes)
    }
}
```
Typical frame diff: 2-3KB instead of 32KB. Enables ~15-20fps animation.

### Full frame draw (initial render / pose change)
```
16 strips of 8 rows * 128 pixels * 2 bytes = 2056 bytes per strip
12ms sleep between strips
Total: ~200ms per full frame
```

### Sprite animation architecture
- 6 poses: idle, listening, thinking, working, speaking, error
- Sprites are 16x16 source pixels scaled 8x to 128x128 on screen
- Pre-loaded from go:embed at startup, source pixels parsed for delta diffing
- Animation pauses during mic capture, resumes when mic stops
- Thinking -> working transition after 3 seconds (indicates tool use)

## Build & Deploy

```bash
# Go app (cross-compile on omarchy)
cd ~/projects/jarvis && GOOS=linux GOARCH=arm64 go build -o /tmp/jarvis-arm64 .

# Deploy
ssh root@192.168.1.174 "systemctl stop jarvis; sleep 1; rm -f /usr/local/bin/jarvis"
scp /tmp/jarvis-arm64 root@192.168.1.174:/usr/local/bin/jarvis
ssh root@192.168.1.174 "chmod +x /usr/local/bin/jarvis && systemctl start jarvis"

# Firmware (must swap USB cable to raspdeck)
esp-flash opi-periph

# Logs
ssh root@192.168.1.174 "journalctl -u jarvis --no-pager -n 20"
```

## Voice Pipeline Flow

1. Wake word ("hey jarvis") detected -> stop mic -> animate listening during MacBook greeting
2. Play Tink ready sound -> start mic -> record with VAD (800 RMS, 1800ms silence)
3. Stop mic -> animate thinking (switches to working after 3s)
4. STT (Wyoming Whisper at ubuntu-homelab:10300) + Claude (`claude -p --resume` via SSH to omarchy)
5. Animate speaking during TTS (`ssh sonia@100.75.170.108 "say '...'"`)
6. Draw idle frame -> 8s cooldown -> restart mic + wake word

## Network

| Machine | IP | Role |
|---------|-----|------|
| Orange Pi (jarvis) | 100.67.186.114 / 192.168.1.174 | Jarvis body, Go binary |
| omarchy | 100.85.150.110 | Claude runs here (~/jarvis/) |
| ubuntu-homelab | 100.109.211.128 | Whisper STT :10300 |
| sonias-mbp | 100.75.170.108 | TTS speaker |

SSH from OPi to omarchy: key auth as willy, config at ~/.ssh/config on OPi.

## Reference Docs

Read these BEFORE making hardware changes:
- `~/projects/raspdeck-learning/builder-area/references/orangepi-zero2w-h618-reference.md` -- OPi full manual (GPIO, WiFi, USB, SPI flash)
- `~/projects/raspdeck-learning/builder-area/references/freenove-fnk0104-reference.md` -- ESP32-S3 board reference (pinout, libraries, gotchas)
- `~/projects/raspdeck-learning/builder-area/devices/opi-peripheral/CLAUDE.md` -- firmware dev guide
- `~/projects/raspdeck-learning/builder-area/devices/opi-peripheral/protocol.h` -- full protocol spec

## Orange Pi 40-Pin Header

All GPIO pins on the OPi are still available (UART broken in Armbian, but GPIO/I2C/SPI work). The ESP32 connects via USB-C only -- no GPIO wiring between OPi and ESP32.

## Known Issues

- ESP32 speaker audio (CMD_AUDIO_PLAY) doesn't produce sound -- amp enable may need debugging
- Handshake (RSP_READY) fails ~50% after power cycles -- reader goroutine recovers but initial sprite may not render
- openwakeword venv at /root/wakeword-venv on OPi -- Python 3.13, openwakeword 0.4.0
