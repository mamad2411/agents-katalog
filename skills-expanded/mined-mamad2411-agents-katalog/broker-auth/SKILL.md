---
name: broker-auth
description: Platform account binding for C2C resale. Use when the user needs to authorize Claude to act on their behalf on resale platforms (Xianyu/闲鱼, Zhuanzhuan/转转, eBay, Depop). Opens a browser for one-time login; session cookies are persisted to disk and reused until expiry. Trigger: "bind account", "authorize", "login to Xianyu", "connect my account". Also invoke before broker-price and broker-card when no valid session exists for the target platform.
---

# broker-auth: Bind Platform Accounts

Handles the "bind once, reuse" account authorization flow.

## How It Works

1. User selects platform(s) to bind (Xianyu, Zhuanzhuan, eBay, Depop)
2. Script opens a Chromium browser to the platform's login page
3. User logs in manually (scan QR code, enter credentials)
4. Browser closes → cookies are persisted to `~/.broker/sessions/<platform>_session.json`
5. Subsequent skills reuse the session transparently
6. Sessions auto-expire after 30 days; when expired, user is prompted to re-bind

## Script

```bash
python3 -m broker_core.session_manager login <platform>
    # Opens browser, captures cookies, saves session

python3 scripts/auth.py          # Wrapper for broker-auth flow
```

## Important Notes

- This is NOT web scraping. The user authorizes Claude to use their own account session for search and publish operations.
- Cookie files are stored locally in `~/.broker/sessions/`. Never shared.
- No passwords are stored — only browser cookies.
- The session is used exclusively for: searching listings, publishing items, checking listing status, and delisting.
