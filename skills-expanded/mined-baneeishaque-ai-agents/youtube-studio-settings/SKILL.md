---
name: youtube-studio-settings
description: Apply YouTube Studio-only settings via layered browser automation backends. Not available via the YouTube Data API v3.
category: YouTube
---

# YouTube Studio Settings Skill (v2)

This is a **base** skill. It uses layered browser automation backends to apply YouTube Studio web interface settings that the YouTube Data API v3 cannot set. These include disabling comments, setting 18+ age restriction (ID-verified), disabling subscriber feed notifications, disabling remixing, and setting caption certification.

Backend selection is automatic:
- **macOS**: JXA (JavaScript for Automation) → undetected_chromedriver → Playwright stealth
- **Other**: undetected_chromedriver → Playwright stealth

Use `--backend` to force a specific backend.

***

## 1. Scope & Intent

- **In scope**: Navigate to YouTube Studio → select a video → apply:
    - Comments (disable)
    - Age restriction (18+ ID-verified)
    - Subscriber feed (don't publish / don't notify)
    - Remixing (disable)
    - Caption certification (never aired in US)
- **Out of scope**:
    - Uploading videos (delegated to [`youtube-video-upload`](../youtube-video-upload/SKILL.md)).
    - OAuth token management (delegated to [`google-oauth-setup`](../google-oauth-setup/SKILL.md)).
    - Metadata fields settable via Data API v3 (delegated to [`youtube-video-metadata-update`](../youtube-video-metadata-update/SKILL.md)).
    - Any other YouTube Studio features (playlist management, analytics, captions, monetization).

***

## 2. Environment & Dependencies

### 2.1 Runtime — All Backends

- **macOS 14+** (for JXA backend) — requires Google Chrome with "Allow JavaScript from Apple Events" enabled (View → Developer menu). Setup script handles this.
- **Python 3.12+** — for undetected and stealth backends. Verify:

  ```bash
  python3 --version
  ```

### 2.2 Backend-Specific Dependencies

#### JXA (macOS only)
- macOS with `osascript` (built-in). No additional packages.
- Run setup once:

  ```bash
  bash .agents/skills/youtube-studio-settings/scripts/studio-settings--setup.bash
  ```

#### undetected_chromedriver
- Install: `pip install undetected_chromedriver`

#### Playwright stealth
- Install: `pip install playwright playwright-stealth && python3 -m playwright install chromium`

### 2.3 Required Files / Setup

- **Google Chrome** with a logged-in YouTube/Google account. The script reuses the session from a persistent Chrome profile at `~/.cache/studio-chrome-profile/`.
- **YouTube video ID** — the video to modify (obtained from upload output or YouTube Studio).
- Run one-time setup to create the profile directory and symlink:

  ```bash
  bash .agents/skills/youtube-studio-settings/scripts/studio-settings--setup.bash
  ```

### 2.4 Required Skill Loading

Before executing this skill, the agent MUST load:

```text
youtube-studio-settings/SKILL.md  (this file)
```

***

## 3. Protocol

### 3.1 Step 1 — One-Time Setup

```bash
bash .agents/skills/youtube-studio-settings/scripts/studio-settings--setup.bash
```

Creates the persistent Chrome profile at `~/<private-config-repo>/youtube-studio-settings-chrome-profile/` with a symlink at `~/.cache/studio-chrome-profile/`. Enables JXA on macOS.

### 3.2 Step 2 — Run Studio Settings Script

```bash
python3 .agents/skills/youtube-studio-settings/scripts/studio-settings.py \
  <VIDEO_ID> \
  [--comments-off] \
  [--age-restrict-18plus] \
  [--no-subscriber-feed] \
  [--no-remixing] \
  [--caption-cert-not-aired-us] \
  [--backend {auto,jxa,undetected,stealth}] \
  [--dump]
```

The orchestrator:

1. Parses flags into JSON settings payload.
2. Selects the first available backend (auto: JXA on macOS → undetected → stealth; cross-platform: undetected → stealth).
3. Each backend script reads `YT_VIDEO_ID` and `YT_SETTINGS` (JSON) from environment.
4. Navigates to YouTube Studio video editor page.
5. For each active flag, locates the corresponding UI control and interacts with it using text-content selectors.
6. Clicks SAVE if any changes were made.
7. Prints a summary of applied changes.

> **Important**: YouTube Studio's DOM changes frequently. If a setting cannot be located, the script reports an error and continues. Apply the setting manually via YouTube Studio.

### 3.3 Arguments

| Argument | Required | Description |
|---|---|---|
| `video_id` | Yes | YouTube video ID (positional) |
| `--comments-off` | No | Disable comments for the video |
| `--age-restrict-18plus` | No | Set age restriction to 18+ (ID-verified) |
| `--no-subscriber-feed` | No | Don't publish to subscriber feed / don't notify |
| `--no-remixing` | No | Don't allow remixing |
| `--caption-cert-not-aired-us` | No | Set caption certification to "never aired in United States" |
| `--backend` | No | Force backend: `auto` (default), `jxa`, `undetected`, `stealth` |
| `--dump` | No | Dump all visible interactive elements and exit (debugging) |

### 3.4 Backend Scripts

| Script | Language | Platform | Purpose |
|---|---|---|---|
| [`scripts/studio-settings.py`](scripts/studio-settings.py) | Python | All | Orchestrator — auto-selects and delegates |
| [`scripts/studio-settings--jxa.jxa`](scripts/studio-settings--jxa.jxa) | JXA | macOS | Controls real Chrome via macOS automation (zero detection) |
| [`scripts/studio-settings--undetected.py`](scripts/studio-settings--undetected.py) | Python | Cross-platform | undetected_chromedriver (Selenium) fallback |
| [`scripts/studio-settings--stealth.py`](scripts/studio-settings--stealth.py) | Python | Cross-platform | Playwright + playwright-stealth last-resort fallback |
| [`scripts/studio-settings--setup.bash`](scripts/studio-settings--setup.bash) | Bash | All | One-time Chrome profile + symlink setup |

***

## 4. Edge Cases

- **Not logged in**: The browser will show the login page. Log in manually and the script will continue. Use `--backend` flag to run visible (non-JXA) if login is needed, then switch to JXA on subsequent runs.
- **DOM changes**: YouTube Studio is a dynamic web app. Text-content selectors are used (not CSS classes) because labels change less frequently than class names. If a setting cannot be applied, the script prints an error and continues.
- **Video not found**: If the video ID is invalid or the user does not have edit access, the Studio page will show an error. The script will time out waiting for the page to load.
- **Concurrent edits**: Ensure no other Studio session is editing the same video. YouTube warns about conflicting edits.
- **JXA not working**: If JXA fails (e.g., "Allow JavaScript from Apple Events" not enabled), run `studio-settings--setup.bash` or force `--backend undetected`.
- **Chromium for Testing blocked**: Google blocks "This browser or app may not be secure" for Chromium for Testing. Use real Chrome (set `channel="chrome"`).
- **No changes to save**: If all requested settings are already in the desired state, the SAVE button is not clicked.

***

## 5. Studio-Only Settings Reference

The following settings are NOT available via the public YouTube Data API v3 and require this skill (or manual Studio usage):

| Setting | Studio Location | Data API Available |
|---|---|---|
| Disable comments | YouTube Studio → Video → Comments | No |
| Age restriction (18+ ID-verified) | YouTube Studio → Video → Audience | No (basic age gate via API, but not 18+ verification) |
| Don't publish to subscriber feed | YouTube Studio → Video → Advanced | No (`notifySubscribers` set at upload time only) |
| Don't allow remixing | YouTube Studio → Video → Advanced | No |
| Caption certification (never aired in US) | YouTube Studio → Video → Advanced → Caption certification | No |

***

## 6. Composition by Higher-Level Skills

| Composer Skill | Composition Mechanism |
|---|---|
| [`youtube-video-upload`](../youtube-video-upload/SKILL.md) | Calls `scripts/studio-settings.py` as a final post-upload step to apply Studio-only settings. |

***

## 7. Composition Rationale

This skill is a **base** skill: it owns only the browser automation logic for YouTube Studio settings that the Data API cannot touch. It is composed by:

- [`youtube-video-upload`](../youtube-video-upload/SKILL.md) — invokes `scripts/studio-settings.py` as a final post-upload step with user-selected flags.

The multi-backend architecture (JXA → undetected_chromedriver → Playwright stealth) is a single atomic concern: detecting and controlling available browser runtimes. No other skill in the ecosystem duplicates this primitive — keeping it in one place means DOM changes, new backends, and login-flow fixes are maintained in a single SSOT rather than patched across multiple composers.
