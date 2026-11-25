---
name: esp32
description: Build, flash, and troubleshoot camera/AP web-streaming sketches for the Seeed XIAO ESP32S3 Sense using arduino-cli
---

# esp32

Instructions for building and flashing XIAO ESP32S3 Sense sketches with
arduino-cli, and getting the onboard camera streaming to a browser over
the board's own Wi-Fi access point (AP mode, no router needed).

## When to use

- The user wants to flash/build a sketch for a Seeed XIAO ESP32S3 Sense
  (or closely related XIAO ESP32-S3 boards) via arduino-cli.
- The user wants to view the onboard camera in a browser, with the board
  itself acting as the Wi-Fi hotspot (AP mode) rather than joining an
  existing router's network.
- The user reports the stream is unreachable, laggy, or disconnecting.

## Environment facts (this machine)

- arduino-cli is installed with core `esp32:esp32` (Arduino ESP32 core 3.x).
- Board fqbn: `esp32:esp32:XIAO_ESP32S3`.
- The board enumerates as a Windows COM port — **do not assume it's COM3**.
  Verify with `arduino-cli board list` or PowerShell
  `[System.IO.Ports.SerialPort]::getportnames()` /
  `Get-CimInstance -ClassName Win32_PnPEntity | Where-Object Name -match 'COM\d+'`
  every time, since the assigned port can change between reboots/cables.
- camera_config_t field names in this core version are `pin_sccb_sda` /
  `pin_sccb_scl` (the old `pin_sscb_*` names are deprecated aliases).

## Camera pin map — XIAO ESP32S3 Sense (OV2640)

```
PWDN  -1        XCLK  10       SIOD  40      SIOC  39
Y9    48        Y8    11       Y7    12      Y6    14
Y5    16        Y4    18       Y3    17      Y2    15
VSYNC 38        HREF  47       PCLK  13
```

## Reference implementation

`esp32/xiao_webcam_ap/xiao_webcam_ap.ino` in this repo is a working,
compile-verified sketch: it starts a Wi-Fi AP (`WiFi.softAP`), inits the
camera, and serves an MJPEG stream via `esp_http_server` at `/` (viewer
page) and `/stream` (raw multipart JPEG stream), reachable at
`http://192.168.4.1/` once connected to the AP.

Edit `AP_SSID` / `AP_PASSWORD` at the top of the file for the user's
desired network name/password.

## Instructions

1. Confirm the actual board port (see "Environment facts" above) — never
   hardcode COM3.
2. Compile: `arduino-cli compile --fqbn esp32:esp32:XIAO_ESP32S3 <sketch-dir>`
3. Upload: `arduino-cli upload -p <COMx> --fqbn esp32:esp32:XIAO_ESP32S3 <sketch-dir>`
4. Verify boot succeeded by reading raw serial output for ~10s (arduino-cli
   monitor's own reset timing is unreliable on this board's native
   USB-CDC/JTAG port — a direct PowerShell read is more dependable):
   ```powershell
   $port = New-Object System.IO.Ports.SerialPort COM4,115200,None,8,one
   $port.Open(); Start-Sleep -Milliseconds 200
   $sw = [System.Diagnostics.Stopwatch]::StartNew(); $buf = ""
   while ($sw.Elapsed.TotalSeconds -lt 10) { $buf += $port.ReadExisting(); Start-Sleep -Milliseconds 200 }
   $port.Close(); $buf
   ```
   Expect to see `AP started. SSID: ...` and `Camera stream ready at: http://192.168.4.1`.
5. Confirm the AP is actually broadcasting from the host machine:
   `netsh wlan show networks` (Windows) and look for the SSID.
6. Have the user join that Wi-Fi network from a **phone**, not the same PC
   that's driving this session — see "Known gotcha" below. Tell them to
   accept "no internet, stay connected / use without internet" if prompted
   — this warning is expected since the AP has no upstream internet.
7. Browse to `http://192.168.4.1/`.

## Known gotcha: Windows auto-switches away from the AP

A PC already on a normal Wi-Fi network (with internet) will silently roam
back to it, because the AP has no internet access and Windows prefers a
working connection. Symptoms: browser/`curl`/`ping` to 192.168.4.1 all
time out with no response at all, even though the ESP32's serial log and
`netsh wlan show networks` both confirm the AP is up. `netsh wlan set
profileparameter name="<home-ssid>" connectionmode=manual` is **not**
reliable enough to stop this roam-back on its own.
**Recommended fix: verify/use the stream from a phone instead of the PC.**
If you must use the PC, expect to have to reconnect repeatedly and check
`netsh wlan show interfaces` / `Get-NetIPConfiguration` right before each
test to confirm it's actually still on the AP.

## Known gotcha: stuttering / disconnects over the AP link

If the stream connects but is choppy or drops:
- Lower resolution/quality (e.g. `FRAMESIZE_QVGA`, `jpeg_quality` ~14)
  instead of VGA — smaller frames tolerate a weak link far better.
- `WiFi.setSleep(false)` after `WiFi.mode(WIFI_AP)` — AP-mode modem sleep
  causes mid-stream stalls.
- `WiFi.setTxPower(WIFI_POWER_19_5dBm)` after `WiFi.softAP(...)` — maxes
  transmit power for better range/margin.
- Physical distance/2.4GHz congestion also matters — ask the user to move
  the client closer to the board to isolate RF issues from firmware bugs.

## Security note

Never write a user's Edge Impulse (or other service) API key into files,
sketches, or memory unless the task explicitly requires calling that
service. If a user pastes a key into chat, tell them it wasn't stored
anywhere and recommend they rotate it from the provider's dashboard.
