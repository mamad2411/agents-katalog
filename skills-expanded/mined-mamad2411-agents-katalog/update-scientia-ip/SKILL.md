---
name: update-scientia-ip
description: Update the Scientia WiFi IP whitelist in Jenkins. Captures the current public IP before VPN, connects OpenVPN, then triggers the Jenkins `change-ip-wifi-scientia` job with the captured IP. Use when your WiFi IP has changed and you need to regain Scientia access.
---

# Update Scientia IP via Jenkins

Whitelists your current WiFi IP in the Scientia environment by triggering the Jenkins job.

## Steps

### 1. Capture current public IP (before VPN)

```bash
curl -s https://ipinfo.io/ip
```

Save this value — it is the `PUBLIC_IP` to pass to Jenkins.

### 2. Connect OpenVPN

Check if VPN is already connected:

```bash
ipconfig | grep -A 4 "OpenVPN Data Channel"
```

If the adapter shows `Media disconnected`, connect it:

```bash
"/c/Program Files/OpenVPN/bin/openvpn-gui.exe" --command connect sultan-laptop
```

Wait ~15 seconds, then verify the adapter has an IP (10.8.0.x):

```bash
sleep 15 && ipconfig | grep -A 4 "OpenVPN Data Channel"
```

> VPN config: `%USERPROFILE%\OpenVPN\config\sultan-laptop\sultan-laptop.ovpn`

### 3. Trigger Jenkins job

Use the Jenkins MCP tool to trigger `change-ip-wifi-scientia` with the IP captured in Step 1:

```
mcp__jenkins__triggerBuild(
  jobFullName: "change-ip-wifi-scientia",
  parameters: { PUBLIC_IP: "<ip-from-step-1>" }
)
```

Job URL: `https://jenkins.bythen.ai/job/change-ip-wifi-scientia/`

## Notes

- The `PUBLIC_IP` parameter must be the **WiFi IP before VPN** — not the VPN exit IP
- VPN must be **connected** when triggering Jenkins (Jenkins is only reachable via VPN)
- If `openvpn-gui.exe --command connect` fails with exit 1, the GUI process may not be running — start it first: `start "" "/c/Program Files/OpenVPN/bin/openvpn-gui.exe"`
- Running `openvpn.exe` directly will fail with netsh errors — always use `openvpn-gui.exe` which routes through the interactive service with admin rights
