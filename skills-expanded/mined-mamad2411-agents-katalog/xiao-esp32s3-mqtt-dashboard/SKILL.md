---
name: xiao-esp32s3-mqtt-dashboard
description: >
  Build a multi-board dashboard for XIAO ESP32S3: each board joins WiFi (STA
  mode), publishes its touch sensor value over MQTT, and accepts LED on/off
  commands, while a browser dashboard shows every board live and lets you
  toggle each LED. Use this skill whenever the user wants several ESP32S3
  boards reporting to one web page, an MQTT-based sensor dashboard, "여러
  esp32s3 대시보드", "MQTT로 여러 보드 연결", or mentions Mosquitto/Eclipse
  MQTT with an ESP32S3. For a single board with no broker, use the
  `xiao-esp32s3` skill's own SoftAP + web server example instead.
---

# XIAO ESP32S3 multi-board MQTT dashboard

Architecture: N boards (STA mode, same WiFi) → MQTT broker (Mosquitto, one PC
on that WiFi) → browser dashboard (MQTT-over-WebSocket, `mqtt.js`). Each board
runs the *same* compiled firmware — no per-board edits — because it derives a
unique ID from its own MAC address.

Read the `xiao-esp32s3` skill (same repo) first for base arduino-cli workflow
and pitfalls (PSRAM flag, DTR reset-stuck recovery, bounded serial reads).
This skill adds the broker + networking + dashboard layer on top.

## Step 1 — ALWAYS ask the user first

Never invent credentials or assume where the broker runs. Ask for:

1. **WiFi SSID / password** — must be a network every board and the broker PC
   can join (2.4 GHz; ESP32 cannot see 5 GHz networks).
2. **Where Mosquitto runs** — this PC (skill sets it up, see Step 2), or an
   existing broker elsewhere (get host + port, skip Step 2's local setup).
3. Whether more than one physical board will be flashed now (affects nothing
   in the firmware — it self-assigns IDs — but changes how you phrase the
   "flash this to every board" instruction back to the user).

## Step 2 — set up the broker (skip if one already exists elsewhere)

Find the broker machine's LAN IP on the shared WiFi (Windows):
```powershell
Get-NetIPAddress -AddressFamily IPv4 | Where-Object {$_.InterfaceAlias -eq 'Wi-Fi'} | Select-Object IPAddress
```

Check whether Mosquitto is installed and what's listening:
```powershell
netstat -an | findstr "1883 9001"
Get-Service -Name mosquitto -ErrorAction SilentlyContinue
```

If nothing is listening on `0.0.0.0:1883`/`0.0.0.0:9001` (see pitfalls 1–3
below for why this is the default), copy `assets/mqtt-broker/setup_broker.ps1`
and `assets/mqtt-broker/setup_firewall.ps1` next to each other in the user's
workspace, then run **both elevated** (see pitfall 2 for why a plain shell
silently fails):

```powershell
Start-Process powershell -ArgumentList '-NoProfile','-ExecutionPolicy','Bypass','-File','<path>\setup_broker.ps1' -Verb RunAs -Wait
Start-Process powershell -ArgumentList '-NoProfile','-ExecutionPolicy','Bypass','-File','<path>\setup_firewall.ps1' -Verb RunAs -Wait
```

This triggers a Windows UAC consent prompt — tell the user it will appear and
that they need to click "Yes"; you cannot click it for them. Both scripts
write a `setup_result.txt` next to themselves — read it back to confirm
success instead of assuming the elevated window's own output was captured.

Verify LAN exposure actually worked (not just that the process is listening):
```powershell
netstat -an | findstr "1883 9001"   # expect 0.0.0.0:1883 and 0.0.0.0:9001, not 127.0.0.1
```

## Step 3 — generate the sketch from the template

`assets/esp32s3_mqtt_dashboard.ino.tpl` is verified working code — do not
rewrite it. Copy it to `<workspace>\<name>\<name>.ino` (folder name must match
the `.ino` name) and replace the placeholders literally:

| Placeholder | Meaning | Example |
|---|---|---|
| `__WIFI_SSID__` | WiFi SSID (2.4 GHz) | `myhome` |
| `__WIFI_PASS__` | WiFi password | `pass1234` |
| `__MQTT_HOST__` | broker machine's LAN IP | `192.168.0.42` |

Install the one extra library the sketch needs (`WiFi`/`WiFiClient` ship with
the esp32 core already):
```powershell
arduino-cli lib install "PubSubClient"
```

## Step 4 — compile, upload

```powershell
arduino-cli compile --fqbn esp32:esp32:XIAO_ESP32S3 <SKETCH_DIR>
arduino-cli upload -p COM4 --fqbn esp32:esp32:XIAO_ESP32S3 <SKETCH_DIR>
```

To add more boards, flash the exact same compiled sketch to each one — no
edits needed between boards.

## Step 5 — verify WITHOUT living in the serial monitor

Read serial ONCE right after flashing to confirm WiFi + MQTT connect (use the
base skill's `read_serial.ps1`, never `arduino-cli monitor`). After that,
**stop opening the serial port** and verify ongoing behavior purely over MQTT
(pitfall 6 explains why re-opening it can look like a regression that isn't
one):

```powershell
# expects: <topic-prefix>/<id>/status online, then a touch value every ~0.5s
mosquitto_sub -h <broker-ip> -p 1883 -t "xiao/#" -v

# flip a board's LED from the command line the same way the dashboard does
mosquitto_pub -h <broker-ip> -p 1883 -t "xiao/<id>/led/set" -m "ON"
```

(If `mosquitto_sub`/`mosquitto_pub` aren't on PATH, they ship next to
`mosquitto.exe`, typically `C:\Program Files\Mosquitto\`.)

## Step 6 — run the dashboard

`assets/dashboard_web/` (`index.html`, `app.js`, `styles.css`) is a static
site — no build step, no placeholders to fill (the broker address is typed
into the page itself, not baked into the JS). Serve it any way the user
likes, e.g.:
```powershell
cd assets/dashboard_web
python -m http.server 8080
```
Then open `http://localhost:8080` (or `http://<broker-ip>:8080` from another
device on the same WiFi). Type the broker's LAN IP into the "브로커 주소" box
and click 연결 — it remembers the value in `localStorage` after that. Boards
appear as cards automatically as their `status`/`touch` messages arrive; no
per-board dashboard configuration exists or is needed.

## MQTT topic scheme

`<id>` is the board's own MAC-derived hex ID (auto-generated, e.g. `4b4cf4`)
so many boards never collide on one broker.

| Topic | Direction | Payload | Notes |
|---|---|---|---|
| `xiao/<id>/touch` | board → dashboard | integer string | every 500 ms |
| `xiao/<id>/led/set` | dashboard → board | `ON` / `OFF` / `TOGGLE` | command |
| `xiao/<id>/led/state` | board → dashboard | `ON` / `OFF`, retained | current state |
| `xiao/<id>/status` | board → dashboard | `online` / `offline`, retained | LWT — broker auto-publishes `offline` on ungraceful disconnect |

Touch baseline is roughly 16,000–18,000 on bare wire/pad; values RISE well
past 40,000 when touched (ESP32-S3 touch direction — see base skill).

## Known pitfalls — read before "debugging"

1. **Mosquitto 2.x binds to loopback ONLY when no listener is configured** —
   this is a deliberate security default, not a bug. A fresh Windows install
   with the stock `mosquitto.conf` (all comments, no `listener` line) will
   show `127.0.0.1:1883` in `netstat`, never `0.0.0.0:1883`, until you add an
   explicit `listener 1883 0.0.0.0`.
2. **The Windows Mosquitto service runs as `LocalSystem`.** A normal
   (non-admin) shell gets a silent `Access is denied` from
   `Stop-Service`/`Restart-Service`, and cannot write
   `C:\Program Files\Mosquitto\mosquitto.conf` either. Use
   `Start-Process powershell -Verb RunAs -Wait` to run the two setup scripts
   elevated (Step 2) — this is a legitimate, narrowly-scoped use of UAC
   elevation for a config change the user already asked for; it is not a
   privilege-escalation workaround, and it still requires the user to click
   "Yes" on the consent prompt themselves.
3. **Windows Firewall blocks LAN-inbound to a newly opened port by default**,
   especially when the WiFi adapter's network profile is "Public" (check with
   `Get-NetConnectionProfile`). Opening the Mosquitto listener alone is not
   enough — add explicit `New-NetFirewallRule -Direction Inbound` rules for
   both ports (Step 2's `setup_firewall.ps1`). **False-positive warning**:
   `Test-NetConnection <own-LAN-IP> -Port 1883` run FROM the broker machine
   itself can report `TcpTestSucceeded: True` even when the firewall would
   block a genuinely remote device — self-to-self tests over your own LAN IP
   are not a reliable substitute for testing from the actual board.
4. **`PubSubClient::connect()` returning `rc=-2`** (`MQTT_CONNECT_FAILED`)
   means the TCP connection itself failed — broker unreachable or firewalled
   — not a credentials/auth rejection. Chasing `allow_anonymous`/username
   config for this code wastes time; check pitfalls 1 and 3 first.
5. **Opening the ESP32S3's serial port resets the board every time** (DTR
   toggle, same as the base skill's pitfall 1) — but for a board that's
   already connected to WiFi/MQTT, this doesn't just cost a reboot: closing
   the port afterward can leave it in the reset-stuck state (base skill
   pitfall 8), which drops the MQTT session a few seconds later. The broker
   then reports that board `offline` via its LWT even though the firmware
   itself has no bug. **Once you've confirmed the WiFi+MQTT connect log
   once, stop opening the serial port** — verify ongoing liveness with
   `mosquitto_sub` or the dashboard instead, never by reopening serial to
   "just double check."
6. **Browsers cannot speak raw MQTT over TCP.** The dashboard needs
   Mosquitto's separate `listener 9001 ... protocol websockets` — the same
   `allow_anonymous`/firewall requirements from pitfalls 1–3 apply to it
   independently of port 1883. "Firmware connects fine, dashboard shows
   nothing" almost always means the websockets listener was forgotten.
7. **Never hardcode one user's WiFi SSID/password or one machine's LAN IP
   into a shared template.** Ask (Step 1), template it in (Step 3) per
   deployment. Also warn that a DHCP-assigned broker IP can change on that
   PC's reboot — a router-side DHCP reservation avoids having to re-flash
   every board afterward.
8. **Each board must derive its own topic-unique ID** (MAC-based, as the
   template does) rather than using a fixed client ID/topic — two boards with
   the same MQTT client ID will fight over the connection (repeated
   disconnects) and two boards on the same topic will stomp each other's
   `touch`/`led/state` values on the dashboard.
