---
name: termux-mobile-bridge
description: Inspect hardware, capture camera photos, send notifications, query GPS, or manage Android devices via Termux SSH or wireless ADB.
---

# Termux Mobile Bridge

Use this procedure when querying telemetries from, capturing media on, or sending alerts to an Android device running Termux and Termux:API over SSH.

## 1. Verifying Connectivity
Verify device reachability and Termux:API IPC responsiveness before dispatching hardware commands:
```bash
ssh celular "termux-battery-status"
```
Check that output returns a JSON object containing `"health"` and `"percentage"`. If the connection times out, verify Tailscale or local network routing.

## 2. Capturing Camera Photos
Capture and retrieve camera images using explicit camera IDs (0 for back, 1 for front):
1. Execute capture specifying output file path:
   ```bash
   ssh celular "termux-camera-photo -c 0 /sdcard/Download/capture.jpg"
   ```
2. Copy the photo to local workspace media:
   ```bash
   mkdir -p /home/user/.openclaw/workspace/media/camera
   scp celular:/sdcard/Download/capture.jpg /home/user/.openclaw/workspace/media/camera/capture.jpg
   chmod 644 /home/user/.openclaw/workspace/media/camera/capture.jpg
   ```
3. Attach the photo to chat using `MEDIA:/home/user/.openclaw/workspace/media/camera/capture.jpg`.

## 3. Querying Device Location
Android background restrictions require Termux and Termux:API to have location permissions set to "Allow all the time" with device GPS active.
Apply bounded timeouts to prevent hung sessions when indoor satellite lock is unavailable:
1. Query last cached location first to obtain instant coordinates without hardware warmup:
   ```bash
   ssh celular "termux-location -r last"
   ```
2. If fresh coordinates are required, query network provider first before GNSS:
   ```bash
   ssh celular "timeout 8 termux-location -p network"
   ```
3. For outdoor satellite precision:
   ```bash
   ssh celular "timeout 12 termux-location -p gps"
   ```
If response is `{"API_ERROR": "Failed to get location"}` or times out, verify global Android location switch and background location permissions on both Termux and Termux:API apps.
4. Translate coordinates to street address via reverse geocoding:
   ```bash
   python3 -c "import urllib.request, json; req=urllib.request.Request('https://nominatim.openstreetmap.org/reverse?lat=<lat>&lon=<lon>&format=json', headers={'User-Agent': 'Homelab/1.0'}); print(json.loads(urllib.request.urlopen(req, timeout=5).read().decode()).get('display_name'))"
   ```

## 4. Sending Push Notifications and Alerts
Send high-priority system alerts with audible notification, vibration pattern, and explicit ID:
```bash
ssh celular "termux-notification -t 'Title' -c 'Message body' --priority high --sound --vibrate 200,200,200 -i <unique_id>"
```
To dismiss or remove an active notification:
```bash
ssh celular "termux-notification-remove <unique_id>"
```

## 5. Clipboard and UI Toasts
- Invalidate or set clipboard contents:
  ```bash
  ssh celular "termux-clipboard-set '<text>'"
  ```
- Android background execution restrictions return empty on `termux-clipboard-get` from non-foreground processes; avoid depending on background clipboard reads.
- Display transient on-screen toast:
  ```bash
  ssh celular "termux-toast '<text>'"
  ```

## 6. Telemetry and Sensors
- Internal storage status: `ssh celular "df -h /storage/emulated"`
- Wi-Fi link parameters: `ssh celular "termux-wifi-connectioninfo"`
- Audio volume levels: `ssh celular "termux-volume"`

## 7. Android Wireless Debugging (ADB Bridge)
When Termux SSH is unreachable, asleep, or untrusted, use Android 11+ Wireless Debugging:
1. Pair using the 6-digit pairing code and ephemeral pairing port:
   ```bash
   adb pair <ip>:<pair_port> <code>
   ```
2. Connect to the active ADB service port (the pairing port closes immediately after authentication; the active service listens on a distinct high port):
   Check the main Wireless Debugging screen for the active service port, or scan candidate high ports concurrently:
   ```bash
   python3 -c '
   import socket
   from concurrent.futures import ThreadPoolExecutor
   ip = "<ip>"
   def check(p):
       with socket.socket() as s:
           s.settimeout(0.2)
           return p if s.connect_ex((ip, p)) == 0 else None
   with ThreadPoolExecutor(max_workers=200) as ex:
       print("Open ports:", [p for p in ex.map(check, range(32000, 48000)) if p])
   '
   adb connect <ip>:<service_port>
   ```
3. Pin ADB to persistent standard port 5555 so future connections avoid ephemeral port discovery:
   ```bash
   adb -s <ip>:<service_port> tcpip 5555
   sleep 2
   adb connect <ip>:5555
   ```
4. Query device telemetry via ADB shell:
   ```bash
   adb -s <ip>:5555 shell dumpsys battery
   ```
