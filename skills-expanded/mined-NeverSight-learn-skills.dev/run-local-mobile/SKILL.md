---
name: run-local-mobile
description: Run the local dev server exposed to the local network (LAN WiFi) for desktop and mobile phone access. Use when the user wants to test on mobile, run the app on local WiFi, access dev server from phone, or share local server across devices.
---

Expose the project's local dev server to the LAN WiFi network, allowing mobile phones and other local devices to access it via LAN IP and QR code.

## Workflow

### Step 1: Framework & Port Legwork

Inspect workspace files (`package.json`, `vite.config.*`, `next.config.*`, `astro.config.*`, `expo`, `Makefile`, etc.) to determine:

- Framework type and target port (default Vite: `5173`, Next.js: `3000`, React Native/Expo: `8081`, Astro: `4321`, Python: `8000`).
- The host binding parameter required (`--host 0.0.0.0`, `-H 0.0.0.0`, `HOST=0.0.0.0`, or `--host`).

Completion criterion: Target port and host flag identified for the project stack.

### Step 2: Port Pre-Check (Process Reuse)

Before launching a new command, check if the target port is already open and listening:

```bash
node -e "const net=require('net'); const s=net.connect(PORT, '127.0.0.1', ()=>{console.log('OCCUPIED'); process.exit(0);}); s.on('error', ()=>{console.log('FREE'); process.exit(0);});"
```

- If **OCCUPIED**: Do not launch a duplicate dev server. Log that the server is already active and proceed directly to Step 4 (QR Broadcast).
- If **FREE**: Proceed to Step 3.

Completion criterion: Active state of the target port determined.

### Step 3: Launch LAN Dev Server

Run the dev server command as a background process with `IsDaemon: true` and host flag set to `0.0.0.0`:

- **npm / yarn / pnpm / bun (Vite / Next / Astro)**:
  `npm run dev -- --host 0.0.0.0` or `npx vite --host 0.0.0.0`
- **Expo / React Native**:
  `npx expo start --lan`
- **Python**:
  `python -m http.server 8000 --bind 0.0.0.0`

Completion criterion: Dev server launched in background listening on `0.0.0.0`.

### Step 4: Resolve LAN IP & QR Broadcast

1. Extract the host machine's primary IPv4 address on the local network:

```bash
node -e "const os=require('os'); const nets=os.networkInterfaces(); for(const name of Object.keys(nets)){for(const net of nets[name]){if(net.family==='IPv4' && !net.internal){console.log(net.address); process.exit(0);}}}"
```

2. Render the ASCII QR code in terminal for mobile scanning:

```bash
npx -y qrcode-terminal "http://<LAN_IP>:<PORT>"
```

3. Display the exact LAN URL `http://<LAN_IP>:<PORT>` clearly in the output.

Completion criterion: LAN URL printed and ASCII QR code displayed in terminal output.
