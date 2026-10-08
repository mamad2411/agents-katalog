---
name: manage-apps-and-sounds-headless
description: Control the pushover.net web dashboard headlessly for things the HTTP API cannot do - log in, list applications, CREATE or DELETE Pushover applications (returning the new app's API token), and ADD or REMOVE custom notification sounds (with a sourcing+loudness pipeline for free MP3 jingles). Drives system Google Chrome via Playwright. Use when the user wants to automate the Pushover website/dashboard rather than send notifications (that is send-notification). TRIGGERS - pushover dashboard, create pushover app, delete pushover app, new api token, add custom sound, upload pushover sound, remove custom sound, find jingle, pushover web automation.
---

# manage-apps-and-sounds-headless

> **Self-Evolving Skill**: This skill improves through use. If instructions are wrong, parameters drifted, or a workaround was needed — fix this file immediately, don't defer. Only update for real, reproducible issues.

Headless dashboard automation via `pushover_headless_web_control.ts` (function/enum-driven Bun
TypeScript — run directly, no build; needs `bun install` in `skills/_lib/` for `playwright-core`).
pushover.net login is a plain email/password form (**no anti-bot / CAPTCHA / 2FA** — verified
2026-05-30), so plain Playwright + system Chrome works.

```bash
export PO_EMAIL="$(bash "$(cc-plugin-root pushover-commander)/skills/_lib/resolve_pushover_secret.sh" login_email)"
export PO_PW="$(bash "$(cc-plugin-root pushover-commander)/skills/_lib/resolve_pushover_secret.sh" login_password)"
export PO_USER="$(bash "$(cc-plugin-root pushover-commander)/skills/_lib/resolve_pushover_secret.sh" user_key)"   # create-app token disambiguation
WEB() { env -u HTTPS_PROXY -u HTTP_PROXY \
  bun "$(cc-plugin-root pushover-commander)/skills/_lib/pushover_headless_web_control.ts" "$@"; }

WEB apps                                              # list application names
WEB create-app --name "My App" --desc "..." --reveal # create app, print its API token (--reveal = full)
WEB delete-app --name "My App"                        # delete app (by --name or --slug)
WEB list-sounds                                       # list custom sound names
WEB add-sound --name po_fanfare --file x.mp3 --desc "..."   # upload a custom sound
WEB remove-sound --name po_fanfare                   # delete a custom sound
```

## Custom sounds: constraints + sourcing pipeline (verified 2026-05-30)

Pushover custom sounds: **MP3 only, < 500 KB, ≤ 30 s** (iOS won't play longer). Sweet spot for
"loud + as long as possible": **~29 s at 128 kbps ≈ 454 KB**. Two helpers automate sourcing/processing:

```bash
# 1) discover free MP3 jingles (Mixkit free license, attribution optional)
bash "$(cc-plugin-root pushover-commander)/skills/_lib/find_jingles.sh" win        # or game musical alarm celebration
bash "$(cc-plugin-root pushover-commander)/skills/_lib/find_jingles.sh" tag/happy  # stock-music tags (longer tracks)

# 2) trim + LOUDNESS-NORMALIZE + size-fit to a compliant sound (loudnorm I=-10, peak -1dB, <500KB)
bash "$(cc-plugin-root pushover-commander)/skills/_lib/make_custom_sound.sh" <url|file> out.mp3 [start_s] [dur] [bitrate]
#   -> JSON {kb, dur, max_db, mean_db, under_500kb}; non-zero exit if >=500KB (then lower bitrate)

# 3) upload it
WEB add-sound --name my_jingle --file out.mp3 --desc "loud 29s jingle"
```

Always analyze with `make_custom_sound.sh` output (or `ffmpeg -af volumedetect`) to confirm **loud** (max ≈ 0 dB)
and **long** (≈29 s) before upload. Loaded so far: `po_fanfare`, `po_uplift`, `po_celebrate`
(all 29 s / 454 KB / peak ≈ -1 dB). Pre-existing custom: `dune, piano, toy_story, vibe20sec`.

## Verified autonomous capability (full lifecycle)

- **create-app**: `application[short_name]` + terms checkbox + submit; captures the 30-char API token
  from the app page (excludes `PO_USER`). **delete-app**: `/apps/edit/<slug>` → `/apps/destroy/<slug>`.
- **add-sound**: `/sounds/build` (`sound[name]`, `sound[description]`, file `sound[sound_data_file]`).
  **remove-sound**: `/sounds/edit/<name>` → `/sounds/destroy/<name>`. Rails `data-method=post`;
  the script auto-accepts the confirm dialog. Both verify the result by re-listing.

## Tooling notes

- Default: Playwright + `channel="chrome"` (no browser download). Scrapling/Obscura unnecessary here.
- Network: prefix `op`/HTTP with `env -u *PROXY*` (and curl `--noproxy '*'`) to bypass the sandbox proxy.

## Post-Execution Reflection

After this skill completes, check before closing:

1. **Did the headless Playwright flow log in and mint/delete the app token without a selector break?** A pushover.net UI change silently breaks selectors — fix them immediately if so.
2. **Did the returned token work on a test send?** A minted-but-dead token means the create flow needs fixing.

Only update if the issue is real and reproducible — not speculative.
