---
name: browser-network-interception
description: Open a URL in Chrome and intercept network responses matching user-specified patterns. Generic base skill for any web automation needing to capture API responses, video manifests, or streamed data. Supports Playwright and JXA backends.
category: Browser Automation
---

# Browser Network Interception Skill (v1)

This is a **base** skill. It opens a URL in Google Chrome (using an existing
profile for authentication), monitors network traffic, and outputs URLs of
responses matching user-specified substring patterns. Domain-agnostic —
usable by any workflow needing to capture network-level data from a web page.

***

## 1. Scope & Intent

- **In scope**:
    - Launch Chrome with persistent profile (existing login sessions)
    - Navigate to a specified URL
    - Monitor all HTTP/HTTPS responses
    - Match response URLs against substring patterns
    - Output matched URLs to stdout (one per line)
    - JXA backend: Open URL in existing Chrome (macOS, zero detection risk)
- **Out of scope**:
    - DOM interaction (clicking, typing, form submission)
    - Screenshot or visual testing
    - Authentication flow management
    - Any domain-specific logic (delegated to composer skills)

***

## 2. Environment & Dependencies

### 2.1 Runtime

- **macOS 14+**, Linux, Windows
- **Python 3.12+**

### 2.2 Dependencies

```bash
pip install playwright playwright-stealth
```

### 2.3 Required Setup

- **Google Chrome** with logged-in sessions for target web apps.
  Uses the default Chrome profile at
  `~/Library/Application Support/Google/Chrome/Default/`.

### 2.4 Required Skill Loading

Before executing this skill, the agent MUST load:

```text
browser-network-interception/SKILL.md (this file)
```

***

## 3. Protocol

### 3.1 Step 1 — Run Interception Script

```bash
python3 .agents/skills/browser-network-interception/scripts/intercept-network.py \
  --url "<target-url>" \
  --pattern "<substring>" \
  [--profile default] \
  [--timeout 30] \
  [--wait-after 5] \
  [--headless]
```

### 3.2 Arguments

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--url` | Yes | — | URL to navigate to |
| `--pattern` | Yes | — | Substring to match in response URLs (repeatable) |
| `--profile` | No | `default` | Chrome profile: `default` or absolute path |
| `--timeout` | No | `30` | Max seconds to wait for first match |
| `--wait-after` | No | `5` | Seconds to wait after page load before checking |
| `--headless` | No | false | Run headless (no visible browser) |
| `--backend` | No | `playwright` | Backend: `playwright` (default) or `jxa` (macOS, opens existing Chrome) |

### 3.3 Output Contract

- **stdout**: One matched URL per line
- **Exit 0**: One or more matches found
- **Exit 1**: No matches found within timeout
- **Exit 2**: Error (missing profile, Playwright failure, etc.)

### 3.4 Script

| Script | Language | Purpose |
|--------|----------|---------|
| [`scripts/intercept-network.py`](scripts/intercept-network.py) | Python | Playwright/JXA backend — opens URL, intercepts responses, outputs matched URLs |

### 3.5 Backends

**Playwright backend** (default):

- Launches Chrome via Playwright with user's profile
- Works on macOS, Linux, Windows
- Opens a new Chrome instance

**JXA backend** (macOS only):

- Opens URL in user's existing Chrome via JXA (zero detection risk)
- Connects Playwright via Chrome DevTools Protocol (CDP)
- Requires [`macos-app-control`](../macos-app-control/SKILL.md) skill
- Preserves all existing Chrome tabs, extensions, and sessions

***

## 4. Edge Cases

- **Chrome profile not found**: Playwright backend exits with code 2.
- **JXA backend on non-macOS**: Exits with code 2 (JXA requires macOS).
- **JXA backend: Chrome not running**: Launches Chrome with remote debugging.
- **JXA backend: CDP connection fails**: Exits with code 2.
- **Not logged in**: Browser shows login page. Script continues monitoring
  network — login-related URLs may match if pattern is broad.
- **Multiple patterns**: All patterns are checked against each response.
  First match per response is printed.
- **No matches within timeout**: Script exits with code 1.
- **Page triggers redirects**: All response URLs (including redirects)
  are checked.

***

## 5. Composition by Higher-Level Skills

| Composer Skill | Composition Mechanism |
|----------------|----------------------|
| [`teams-recording-download`](../teams-recording-download/SKILL.md) | Calls `scripts/intercept-network.py` with `--pattern videomanifest` to capture Teams video manifest URLs from network traffic during recording playback. |

***

## 6. Composition Rationale

This skill is a **base** skill: it owns only the generic browser network
interception primitive. It delegates Chrome launching to the Playwright
backend or to [`macos-app-control`](../macos-app-control/SKILL.md) for
the JXA backend. All video download logic is delegated to
[`video-download-manifest`](../video-download-manifest/SKILL.md).
Separating network interception from domain-specific navigation
(Teams, YouTube, etc.) allows reuse by any web automation task needing
to capture API responses or streamed data URLs.

## Related Skills

- [`macos-app-control`](../macos-app-control/SKILL.md) — base skill for
  macOS app control via JXA (used by JXA backend)
- [`video-download-manifest`](../video-download-manifest/SKILL.md) — base skill for
  downloading video from a manifest URL via ffmpeg
- [`teams-recording-download`](../teams-recording-download/SKILL.md) — composer skill
  that orchestrates Teams-specific workflow using this base skill
