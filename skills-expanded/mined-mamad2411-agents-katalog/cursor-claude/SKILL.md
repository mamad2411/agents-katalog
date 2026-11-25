# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Cursor IDE account auto-registration system using DrissionPage (Chromium browser automation) with Cloudflare Turnstile bypass. Learned from [wf-cursor-auto-free](https://github.com/wangffei/wf-cursor-auto-free).

**Two-phase workflow:**
1. **Register** - Navigate signup page, fill form, bypass Turnstile, verify email via IMAP
2. **Get Token** - Obtain OAuth tokens via PKCE flow, write to Cursor's local SQLite DB

## Commands

```bash
# Setup
python3 -m venv .venv
source .venv/bin/activate
pip install -r cursor-account-automation/requirements.txt

# Run (recommended: email-code path, skips password-page Turnstile)
python -u cursor-account-automation/main.py --email user@example.com --imap-password xxx

# With proxy (recommended to avoid IP rate-limiting)
python -u cursor-account-automation/main.py --email user@example.com --imap-password xxx --proxy http://127.0.0.1:7890

# Headless mode (server deployment)
python -u cursor-account-automation/main.py --email user@example.com --imap-password xxx --headless

# Password path (not recommended - hits stricter Turnstile)
python -u cursor-account-automation/main.py --email user@example.com --imap-password xxx --use-password
```

No test framework is configured. Testing is done manually via CLI runs.

## Architecture

All source lives in `cursor-account-automation/`. Python 3.10+, dependencies: DrissionPage, python-dotenv, requests.

### Module Responsibilities

- **`main.py`** - CLI entry point (`argparse`), orchestrates two-phase flow with retry logic (3 attempts, exponential backoff)
- **`browser.py`** - Creates DrissionPage Chromium instance, auto-detects Chrome binary (macOS/Windows/Linux), loads `turnstilePatch` extension, supports proxy and headless mode
- **`registration.py`** - Signup/login form filling, Turnstile Shadow DOM traversal (`shadow_root → iframe → body → input`), verification code input via `@data-index` selectors, block detection
- **`cursor_auth.py`** - PKCE OAuth flow (code_verifier/challenge + UUID), polls auth API for tokens, writes to Cursor's `state.vscdb` SQLite DB
- **`email_client.py`** - IMAP SSL connection, polls INBOX every 5s for 120s, extracts 6-digit code via regex from `no-reply@cursor.com` emails
- **`config.py`** - Dataclass config from `.env` (credit card fields required) + CLI args, random name generation
- **`output.py`** - Prints account info, appends `email:password` to `accounts.txt`

### Key Technical Details

**Turnstile bypass** uses two approaches:
1. `.main-content` → nested divs → shadow_root → iframe → body → input (wf-cursor-auto-free style)
2. `@id=cf-turnstile` → child → shadow_root → iframe → body → input (fallback)

**turnstilePatch Chrome extension** (`turnstilePatch/`) overrides `MouseEvent.prototype.screenX/screenY` to inject random coordinates, defeating Cloudflare's CDP `screenX/screenY === 0` fingerprint check.

**Default email-code path** clicks "Continue with email code" button to skip the password page entirely, avoiding the stricter second Turnstile challenge.

**Cursor DB paths:**
- macOS: `~/Library/Application Support/Cursor/User/globalStorage/state.vscdb`
- Windows: `%APPDATA%\Cursor\User\globalStorage\state.vscdb`
- Linux: `~/.config/Cursor/User/globalStorage/state.vscdb`

### DrissionPage Selector Patterns

- `@name=first_name` - by HTML name attribute
- `@data-index=0` - by data attribute (Clerk verification code inputs)
- `@type=submit` - by type attribute
- `text:Continue with email code` - by visible text
- `@id=cf-turnstile` - by ID
- `.shadow_root` / `.sr()` - Shadow DOM piercing
- `tag:div`, `tag:iframe` - by tag name

## Configuration

`.env` file in `cursor-account-automation/` provides static config. Required fields: `CARD_NUMBER`, `CARD_EXP_MONTH`, `CARD_EXP_YEAR`, `CARD_CVV`, `CARD_HOLDER`, `CARD_ZIP`. Optional: `IMAP_HOST` (default: imap.feishu.cn), `IMAP_PORT` (default: 993), `PLAN_NAME` (default: Pro), `PROXY`.

## Language

Code comments and print output are in Chinese. README is in Chinese.
