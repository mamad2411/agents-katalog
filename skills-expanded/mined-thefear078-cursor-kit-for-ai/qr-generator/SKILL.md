---
name: qr-generator
description: Generate QR codes, WiFi QR strings, and vCard patterns for contact sharing. Use when creating scannable codes for URLs, network credentials, or contact cards.
---

# QR Generator

Generate QR codes and standard payload patterns (WiFi, vCard, URL). Output as ASCII art for terminal preview, SVG/PNG instructions, or raw payload strings for external renderers.

## When to Use This Skill

| Trigger | Example request |
|---------|-----------------|
| URL QR | "Generate QR for https://example.com" |
| WiFi setup | "QR code for WPA2 network Guest / password123" |
| Contact card | "vCard QR for John Doe, john@example.com" |
| Event link | "QR for calendar event or meeting URL" |
| Payment | "Generate UPI or payment link QR payload" |
| Batch codes | "Generate QRs for these 5 URLs" |

## Phase Checklist

```
[ ] 1. Identify payload type (URL, WiFi, vCard, text, etc.)
[ ] 2. Build payload string per format specification
[ ] 3. Validate payload (URL scheme, WiFi auth type, vCard fields)
[ ] 4. Choose error correction level (L/M/Q/H)
[ ] 5. Generate QR (ASCII preview + file command)
[ ] 6. Warn about sensitive data in QR (WiFi passwords, PII)
```

---

## Payload Types

| Type | Prefix / Format | Example use |
|------|-----------------|-------------|
| URL | `https://...` | Website, app link |
| WiFi | `WIFI:T:...;S:...;P:...;;` | Network auto-join |
| vCard | `BEGIN:VCARD...END:VCARD` | Contact sharing |
| Text | Plain string | Any text message |
| Email | `mailto:user@example.com` | Open email client |
| Phone | `tel:+1234567890` | Dial number |
| SMS | `sms:+1234567890?body=Hello` | Send text |
| Geo | `geo:48.8566,2.3522` | Map location |
| Calendar | `BEGIN:VEVENT...` | Event (iCal subset) |

---

## URL QR Code

```bash
pip install qrcode[pil] -q
```

```python
import qrcode

def generate_url_qr(url: str, output: str = "qr.png") -> str:
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    qr = qrcode.QRCode(
        version=None,  # auto-size
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(output)
    return url

url = generate_url_qr("https://example.com/docs", "url_qr.png")
print(f"Generated QR for: {url}")
```

```bash
# CLI with qrencode (if installed)
qrencode -o qr.png "https://example.com"
qrencode -t ANSIUTF8 "https://example.com"   # terminal preview
```

---

## WiFi QR Format

```
WIFI:T:<auth>;S:<ssid>;P:<password>;H:<hidden>;;

Fields:
  T = auth type: WPA, WEP, nopass
  S = SSID (network name)
  P = password (omit for open networks)
  H = hidden: true/false (optional)
```

```python
def wifi_qr_payload(ssid: str, password: str, auth: str = "WPA", hidden: bool = False) -> str:
    auth = auth.upper()
    if auth not in ("WPA", "WEP", "nopass"):
        raise ValueError(f"Invalid auth type: {auth}")
    parts = [f"WIFI:T:{auth}", f"S:{_escape_wifi(ssid)}"]
    if auth != "nopass" and password:
        parts.append(f"P:{_escape_wifi(password)}")
    if hidden:
        parts.append("H:true")
    return ";".join(parts) + ";;"

def _escape_wifi(value: str) -> str:
    """Escape special chars: \\ ; , : \" """
    for ch in ('\\', ';', ',', ':', '"'):
        value = value.replace(ch, f"\\{ch}")
    return value

payload = wifi_qr_payload("GuestNetwork", "SuperSecret123", auth="WPA")
print(payload)
# WIFI:T:WPA;S:GuestNetwork;P:SuperSecret123;;

# Generate image
import qrcode
qr = qrcode.make(payload)
qr.save("wifi_qr.png")
print("Saved wifi_qr.png")
```

### WiFi Auth Types

| Type | When to use |
|------|-------------|
| WPA | WPA/WPA2/WPA3 (most common) |
| WEP | Legacy — discouraged |
| nopass | Open network, no password |

**Security warning:** WiFi QR codes embed plaintext passwords. Only share with trusted recipients. Do not commit QR images with credentials to git.

---

## vCard Format

```
BEGIN:VCARD
VERSION:3.0
N:Last;First;;;
FN:First Last
ORG:Company Name
TITLE:Job Title
TEL;TYPE=CELL:+1234567890
EMAIL:john@example.com
URL:https://example.com
ADR;TYPE=WORK:;;123 Main St;City;State;12345;Country
END:VCARD
```

```python
def vcard_payload(
    first: str,
    last: str,
    email: str = "",
    phone: str = "",
    org: str = "",
    title: str = "",
    url: str = "",
) -> str:
    lines = [
        "BEGIN:VCARD",
        "VERSION:3.0",
        f"N:{last};{first};;;",
        f"FN:{first} {last}",
    ]
    if org:
        lines.append(f"ORG:{org}")
    if title:
        lines.append(f"TITLE:{title}")
    if phone:
        lines.append(f"TEL;TYPE=CELL:{phone}")
    if email:
        lines.append(f"EMAIL:{email}")
    if url:
        lines.append(f"URL:{url}")
    lines.append("END:VCARD")
    return "\n".join(lines)

vcard = vcard_payload(
    first="John", last="Doe",
    email="john@example.com",
    phone="+1-555-123-4567",
    org="Acme Corp", title="Engineer",
)
print(vcard)

import qrcode
qr = qrcode.make(vcard)
qr.save("contact_qr.png")
```

### vCard Version Notes

| Version | Support |
|---------|---------|
| 3.0 | Widest QR scanner compatibility |
| 4.0 | Modern, UTF-8 native |
| 2.1 | Legacy, avoid for new codes |

Prefer v3.0 for maximum scanner compatibility.

---

## Error Correction Levels

| Level | Recovery | Use case |
|-------|----------|----------|
| L (Low) | ~7% | Clean print, large codes |
| M (Medium) | ~15% | Default general use |
| Q (Quartile) | ~25% | Logo overlay in center |
| H (High) | ~30% | Damaged labels, logo overlay |

```python
import qrcode

def generate_with_ec(payload: str, level: str = "M", output: str = "qr.png"):
    levels = {
        "L": qrcode.constants.ERROR_CORRECT_L,
        "M": qrcode.constants.ERROR_CORRECT_M,
        "Q": qrcode.constants.ERROR_CORRECT_Q,
        "H": qrcode.constants.ERROR_CORRECT_H,
    }
    qr = qrcode.QRCode(error_correction=levels[level.upper()])
    qr.add_data(payload)
    qr.make(fit=True)
    qr.make_image().save(output)
    print(f"Saved {output} (EC level {level})")
```

**Rule:** Use Q or H if placing a logo in the center of the QR code.

---

## ASCII Terminal Preview

```python
import qrcode

def ascii_qr(payload: str) -> str:
    qr = qrcode.QRCode(border=1)
    qr.add_data(payload)
    qr.make()
    matrix = qr.get_matrix()
    lines = []
    for row in matrix:
        lines.append("".join("██" if cell else "  " for cell in row))
    return "\n".join(lines)

print(ascii_qr("https://example.com"))
```

```bash
# qrencode terminal output
qrencode -t ANSIUTF8 "Hello World"
qrencode -t UTF8 "Hello World"
```

---

## SVG Output (Scalable)

```python
import qrcode
import qrcode.image.svg

def generate_svg(payload: str, output: str = "qr.svg"):
    factory = qrcode.image.svg.SvgPathImage
    qr = qrcode.QRCode(image_factory=factory)
    qr.add_data(payload)
    qr.make(fit=True)
    img = qr.make_image()
    with open(output, "wb") as f:
        img.save(f)
    print(f"Saved {output}")

generate_svg("https://example.com")
```

---

## Custom Colors

```python
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer

def colored_qr(payload: str, fg: str = "#1E3A5F", bg: str = "#FFFFFF", output: str = "qr.png"):
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
    qr.add_data(payload)
    qr.make(fit=True)
    img = qr.make_image(
        image_factory=StyledPilImage,
        module_drawer=RoundedModuleDrawer(),
        fill_color=fg,
        back_color=bg,
    )
    img.save(output)
    print(f"Saved {output} (fg={fg}, bg={bg})")

colored_qr("https://example.com", fg="#6366F1", bg="#FFFFFF")
```

For color contrast validation on QR codes, see `color-convert` — ensure sufficient contrast between modules and background.

---

## Other Payload Patterns

### Email

```python
payload = "mailto:john@example.com?subject=Hello&body=Message%20here"
```

### Phone

```python
payload = "tel:+380501234567"
```

### SMS

```python
payload = "sms:+380501234567?body=Hello"
```

### Geo Location

```python
payload = "geo:50.4501,30.5234?q=Kyiv"
```

### Calendar Event (VEVENT subset)

```
BEGIN:VEVENT
SUMMARY:Team Meeting
DTSTART:20240615T100000Z
DTEND:20240615T110000Z
LOCATION:Conference Room A
DESCRIPTION:Weekly sync
END:VEVENT
```

---

## Batch Generation

```python
import qrcode
from pathlib import Path

def batch_qr(items: list[dict], output_dir: str = "qr_codes"):
    Path(output_dir).mkdir(exist_ok=True)
    for item in items:
        payload = item["payload"]
        name = item["name"]
        path = f"{output_dir}/{name}.png"
        qrcode.make(payload).save(path)
        print(f"  {path}: {payload[:50]}...")

batch_qr([
    {"name": "homepage", "payload": "https://example.com"},
    {"name": "docs", "payload": "https://example.com/docs"},
    {"name": "github", "payload": "https://github.com/org/repo"},
])
```

---

## Worked Examples

### Example 1: Restaurant menu QR

```
Payload: https://menu.restaurant.com/table/12
EC Level: M
Output:  menu_qr.png (300×300 px recommended for print)
Print:   Minimum 2cm × 2cm for reliable scanning
```

### Example 2: Office WiFi onboarding

```
SSID:     CorpWiFi-5G
Auth:     WPA
Password: (provided separately — do not log)
Payload:  WIFI:T:WPA;S:CorpWiFi-5G;P:••••••••;;

⚠ Password embedded in QR — share securely
⚠ Do not commit generated PNG to git
```

### Example 3: Conference speaker vCard

```
Name:     Jane Smith
Email:    jane@company.com
Phone:    +1-555-987-6543
Org:      Tech Corp
Title:    CTO
Output:   jane_smith_vcard.png
Format:   vCard 3.0 for max compatibility
```

---

## Output Template

```markdown
## QR Code: {type}

| Property | Value |
|----------|-------|
| Type | URL / WiFi / vCard |
| Payload | `{payload}` |
| Error correction | M (15%) |
| Output file | `qr.png` |
| Size | 290×290 px (version 4) |

### Payload (raw)
```
{full_payload_string}
```

### Generate Command
```bash
qrencode -o qr.png "{payload}"
```

⚠ **Security:** {warnings about embedded credentials or PII}
```

---

## Anti-Patterns

- Embedding WiFi passwords in QR without security warning
- Using error correction L with logo overlay (won't scan)
- vCard 4.0 when scanner compatibility is unknown
- QR codes too small to scan (< 2cm print size)
- Committing QR images with credentials to version control
- Low contrast colors (light gray on white won't scan)
- Very long payloads without checking QR version capacity
- Using HTTP URLs when HTTPS is available

---

## Cross-References

| Related need | Skill |
|--------------|-------|
| QR brand colors / contrast | `color-convert` |
| URL parsing before QR | `network-utils` |
| URL encoding in query params | `encode-decode` |
| vCard JSON → vCard text | `format-convert` |
| Generate unique IDs in URL | `token-generator` |
| WiFi MAC address info | `network-utils` |
