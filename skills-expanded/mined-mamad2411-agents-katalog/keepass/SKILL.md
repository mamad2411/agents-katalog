---
name: keepass
description: KeePassXC cursor.kdbx — natywny keyring per OS, keepass-db.path bez fallbacków, agent instaluje brakujące narzędzia.
compatibility:
  - windows
  - wsl
  - linux
---

# Skill: keepass

Wywołanie: **`/keepass`**

Baza **`cursor.kdbx`** (sync: OneDrive / Google Drive) + **keyring = tylko hasło master**. Wszystkie sekrety w KeePass — nie w repo / `.env`.

---

## Zasady (agent)

1. **Natywny keyring danego OS** — nie mieszaj mechanizmów między systemami.
2. **Brakuje narzędzia → doinstaluj** (patrz tabela); przy `sudo` poproś użytkownika.
3. **Brak `~/.cursor/keepass-db.path`** → **poproś użytkownika o ścieżkę** (jedna linia absolutna). Nie zgaduj ścieżek.
4. **Nie loguj** wartości sekretów.

---

## Krok 1 — Ścieżka bazy

```bash
test -f ~/.cursor/keepass-db.path && head -1 ~/.cursor/keepass-db.path
test -f "$(grep -v '^#' ~/.cursor/keepass-db.path | head -1)"
```

Jeśli pliku brak lub pusty → **stop** i poproś:

> Utwórz `~/.cursor/keepass-db.path` z jedną linią: absolutna ścieżka do `cursor.kdbx` (OneDrive lub Google Drive). Wzór: `keepass-db.path.example`.

**WSL:** ten sam plik może być w `~/.cursor/` (Linux home) **albo** `/mnt/c/Users/<user>/.cursor/keepass-db.path` (Windows home) — skrypt sprawdza oba.

**WSL + Cursor Remote:** agent często czyta **`/home/<user>/.cursor`**, nie `C:\Users\...\`. Po zmianach na Windows uruchom:
`wsl bash /mnt/c/Users/janja/.cursor/scripts/sync-keepass-to-wsl-home.sh`

Opcjonalnie na sesję: `export KEEPASS_DB_PATH="/pełna/ścieżka/cursor.kdbx"`.

### Przykłady ścieżek (użytkownik wybiera jedną)

| Sync | Windows | WSL | Linux |
|------|---------|-----|-------|
| OneDrive | `C:\Users\<u>\OneDrive\...\cursor.kdbx` | `/mnt/c/Users/<u>/OneDrive/.../cursor.kdbx` | `~/OneDrive/.../cursor.kdbx` |
| Google Drive | `...\Google Drive\My Drive\...\cursor.kdbx` | `/mnt/c/.../Google Drive/My Drive/...` | `~/Google Drive/My Drive/...` |

---

## Krok 2 — Platforma i natywny keyring

| Gdzie agent pracuje | Natywny keyring | Skrypt odczytu | Setup (jednorazowo) |
|---------------------|-----------------|----------------|---------------------|
| **Windows** (PowerShell) | **SecretStore** `KeePassXC-Cursor-DB` | `get-keepass-secret.ps1` | `setup-keepass-keyring.ps1` |
| **Linux / WSL** (bash) | **secret-tool** (`service=keepassxc`, `attribute=cursor-db`) | `get-keepass-secret.sh` | `setup-keepass-keyring-linux.sh` |

**WSL = Linux** → używaj **bash + secret-tool**, nie `powershell.exe` / Windows SecretStore.

### Brak narzędzia — agent instaluje

| OS | Pakiet / moduł | Komenda |
|----|----------------|---------|
| Linux / WSL | `libsecret-tools`, `gnome-keyring`, `dbus-x11` | `sudo apt install -y libsecret-tools gnome-keyring dbus-x11` |
| Linux / WSL | `keepassxc-cli` | `sudo apt install -y keepassxc` |
| Windows | `Microsoft.PowerShell.SecretManagement`, `.SecretStore` | `Install-Module -Name Microsoft.PowerShell.SecretManagement -Scope CurrentUser` (+ SecretStore) |

Skrypt bash: `lib/keepass-platform.sh` → `keepass_ensure_secret_tool` (próbuje `sudo -n`, inaczej prośba do użytkownika).

---

## Krok 3 — Test

| OS | Komenda |
|----|---------|
| Linux / WSL | `~/.cursor/scripts/test-keepass-read.sh` |
| Windows | `.\get-keepass-secret.ps1 "hosts/euk-sl01/sudo" "Password"` (bez echo hasła w logu) |

Oczekiwane: odczyt bez promptu. Jeśli błąd keyringa → `KEEPASS_DB_PASSWORD='…'` + odpowiedni `setup-*`.

---

## Krok 4 — Sekrety

```bash
# Linux / WSL — sudo na EUK-SL01 (janja)
~/.cursor/scripts/get-keepass-secret.sh "hosts/euk-sl01/sudo" "Password"
```

```powershell
# Windows
.\get-keepass-secret.ps1 "hosts/euk-sl01/sudo" "Password"
```

**Check-before-add:** `keepassxc-cli search "$KEEPASS_DB_PATH" "term"` → `mkdir` / `add` / `edit`.

### Struktura wpisów

| Typ | Ścieżka |
|-----|---------|
| Host SSH | `hosts/<hostname>/<username>` |
| Host sudo | `hosts/<hostname>/sudo` (np. `hosts/euk-sl01/sudo`) |
| Projekt | `<project>/<env>/<title>` |
| MCP API keys | `API Keys/<Service>` (np. `API Keys/Context7`) — patrz [doc/mcp-secrets.md](../doc/mcp-secrets.md) |
| Eureka POC | `EurekaCloud/poc/SL01/paperclip-ceo-api-key`, … |

---

## Skrypty

| Skrypt | OS |
|--------|-----|
| `lib/keepass-db-path.sh` / `.ps1` | rozwiązywanie ścieżki (wymagany plik) |
| `lib/keepass-db-password.sh` | Linux/WSL → secret-tool |
| `lib/keepass-secretstore.ps1` | Windows → SecretStore |
| `get-keepass-secret.sh` | Linux / WSL |
| `get-keepass-secret.ps1` | Windows |
| `save-keepass-password-to-keyring.sh` | Linux / WSL |
| `save-keepass-password-to-keyring.ps1` | Windows |
| `setup-keepass-keyring-linux.sh` | Linux / WSL |
| `setup-keepass-keyring.ps1` | Windows |
| `add-host-entry.sh` | nowy host (bash) |
| `keepass_ops.py` | get/add/update |

Runbook: `~/.cursor/doc/keepass.md`  
MCP keys → `.env`: `~/.cursor/doc/mcp-secrets.md`

---

## Architektura

- Keyring = **tylko** hasło master `cursor.kdbx`
- KeePass = **wszystkie** sekrety aplikacji
- **Brak** fallbacków ścieżki i **brak** plikowych kopii haseł w `~/.cursor`
