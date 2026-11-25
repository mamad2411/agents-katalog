---
name: resolve-cloudflare-protected-download-url
description: Use Playwright in headless stealth mode to bypass Cloudflare and capture the final download URL from network requests. Derive secondary-architecture URLs by pattern substitution from the resolved primary URL, then verify with HEAD requests.
category: automation
version: 1.0.0
tags: [playwright, cloudflare, download, url-resolution, stealth, automation, python]
source_type: extracted-from-git
source_url: https://github.com/aaddrick/claude-desktop-debian.git
source_ref: main
source_commit: 2fd9faf9db4eaa409b88310bdce397f8bdb0e916
source_project: claude-desktop-debian
imported_at: 2026-04-18T00:00:00Z
version_origin: extracted
confidence: medium
---

# Resolve Cloudflare-Protected Download URL

## When to use

Use this pattern when:
- A download URL is hidden behind a Cloudflare-protected redirect that returns 403 to direct HTTP clients.
- You need to resolve the final CDN/storage URL for use in a CI pipeline, version checker, or build script.
- The download service only exposes a per-architecture "latest" redirect rather than version-pinned URLs.
- A secondary architecture (arm64) URL can be derived from the primary (amd64) URL by string substitution, saving a second browser request.

## Pattern

### Approach

1. Launch Playwright Chromium in headless mode with stealth settings (hide `navigator.webdriver`, spoof `navigator.platform`).
2. Register a `request` event listener to capture URLs matching the expected CDN pattern.
3. Register a `download` event listener as a backup.
4. Navigate to the redirect URL with `wait_until="commit"` (triggers the redirect without waiting for full page load).
5. Wait 2 seconds for the download to start, then close the browser.
6. Extract version from the resolved URL with a regex.
7. For arm64: derive from amd64 by substituting architecture strings; verify with a HEAD request.

### URL derivation pattern

```
amd64: https://cdn.example.com/releases/win32/x64/1.0.1234/App-abc123.exe
arm64: https://cdn.example.com/releases/win32/arm64/1.0.1234/App-abc123.exe
                                              ^^^^
                                         x64 → arm64
```

## Minimal example

```python
#!/usr/bin/env python3
"""
Resolve download URLs behind Cloudflare by using a stealth Playwright browser.
"""
import re
import sys
import argparse
import requests
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout

# Redirect URL template per architecture
REDIRECT_URLS = {
    "amd64": "https://example.com/download/redirect/win32/x64/latest",
    "arm64": "https://example.com/download/redirect/win32/arm64/latest",
}

USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
)


def resolve_download_url(arch: str, timeout_ms: int = 30000) -> str | None:
    redirect_url = REDIRECT_URLS.get(arch)
    if not redirect_url:
        return None

    resolved_url = None

    def handle_request(request):
        nonlocal resolved_url
        url = request.url
        # Match the CDN pattern for the final download
        if "storage.googleapis.com" in url and url.endswith(".exe"):
            resolved_url = url

    def handle_download(download):
        nonlocal resolved_url
        resolved_url = download.url

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent=USER_AGENT,
            viewport={"width": 1920, "height": 1080},
            accept_downloads=True,
        )
        # Stealth: hide automation indicators
        context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
            Object.defineProperty(navigator, 'platform',  { get: () => 'Linux x86_64' });
            Object.defineProperty(navigator, 'vendor',    { get: () => 'Google Inc.' });
        """)
        page = context.new_page()
        page.on("request", handle_request)
        page.on("download", handle_download)
        try:
            page.goto(redirect_url, timeout=timeout_ms, wait_until="commit")
            page.wait_for_timeout(2000)  # let download trigger
        except PlaywrightTimeout:
            pass
        except Exception as e:
            if "Download is starting" not in str(e):
                print(f"Navigation error: {e}", file=sys.stderr)
        finally:
            browser.close()

    return resolved_url


def extract_version(url: str) -> str | None:
    m = re.search(r"/(\d+\.\d+\.\d+)/", url)
    return m.group(1) if m else None


def derive_arm64_url(amd64_url: str) -> str | None:
    if not amd64_url:
        return None
    arm64_url = amd64_url.replace("/win32/x64/", "/win32/arm64/")
    arm64_url = arm64_url.replace("-x64.exe", "-arm64.exe")
    return arm64_url if arm64_url != amd64_url else None


def verify_url(url: str, timeout_s: int = 10) -> bool:
    try:
        r = requests.head(url, timeout=timeout_s, allow_redirects=True)
        return r.status_code == 200
    except requests.RequestException:
        return False


def main():
    parser = argparse.ArgumentParser(description="Resolve protected download URLs")
    parser.add_argument("arch", choices=["amd64", "arm64", "all"])
    parser.add_argument("--timeout", type=int, default=30000)
    parser.add_argument("--format", choices=["url", "version", "both"], default="url")
    args = parser.parse_args()

    archs = ["amd64", "arm64"] if args.arch == "all" else [args.arch]
    results = {}

    for arch in archs:
        print(f"Resolving {arch}...", file=sys.stderr)
        url = resolve_download_url(arch, args.timeout)
        if url:
            results[arch] = {"url": url, "version": extract_version(url)}
            print(f"  {arch}: {url}", file=sys.stderr)
        else:
            results[arch] = None

    # Derive arm64 from amd64 if arm64 resolution failed
    if args.arch == "all" and not results.get("arm64") and results.get("amd64"):
        derived = derive_arm64_url(results["amd64"]["url"])
        if derived and verify_url(derived):
            results["arm64"] = {"url": derived, "version": extract_version(derived)}
            print(f"  arm64 (derived): {derived}", file=sys.stderr)

    # Output results
    for arch, result in results.items():
        if not result:
            continue
        prefix = f"{arch.upper()}_" if len(archs) > 1 else ""
        if args.format in ("url", "both"):
            print(f"{prefix}URL={result['url']}")
        if args.format in ("version", "both") and result.get("version"):
            print(f"{prefix}VERSION={result['version']}")

    if any(r is None for r in results.values()):
        sys.exit(1)


if __name__ == "__main__":
    main()
```

## Why this works

### `wait_until="commit"` vs `"load"`

Cloudflare-protected download redirects trigger a file download before the page "loads". Using `wait_until="load"` would hang waiting for a page that never loads. `wait_until="commit"` returns as soon as the navigation is committed (HTTP response headers received), which is right when the download starts.

### `page.wait_for_timeout(2000)` after navigation

The `request` event fires when the browser makes the request. After the navigation is committed, the download redirect happens asynchronously. A brief `wait_for_timeout(2000)` ensures the browser has time to follow the redirect chain and emit the `request` event for the final CDN URL before the browser is closed.

### Stealth `add_init_script`

Cloudflare's bot detection checks `navigator.webdriver`. Setting it to `undefined` (not `false` — `undefined` is the value in a real browser) passes the check. Spoofing `navigator.platform` and `navigator.vendor` rounds out the browser fingerprint. `add_init_script` runs on every new page before any page scripts, so it applies to the redirect target as well.

### URL derivation avoids a second browser session

Starting a second browser session for arm64 takes 5-10 seconds. Architecture-specific download URLs typically differ only in the architecture string in the path. Substituting `x64` → `arm64` in the path and verifying with a `HEAD` request (which is fast and does not need Playwright) is far cheaper.

### Catching `"Download is starting"` exception

Playwright raises an exception with the message "Download is starting" when a download begins. This is not an error — it's expected. Catching it and checking for this string prevents false failure reporting while still logging genuine navigation errors.

## Pitfalls

- **Cloudflare bot detection changes** — stealth techniques may stop working as Cloudflare updates its detection. If this happens, consider using a real browser profile, cookies, or a service like Browserless.
- **`requests.head` may not be sufficient for all CDNs** — some CDNs return 403 to HEAD requests but 200 to GET. Use `requests.get(stream=True)` and immediately close the response if HEAD fails.
- **`playwright.sync_api` is not thread-safe** — do not share a browser context across threads. Each call to `resolve_download_url` should create its own Playwright context.
- **The `handle_request` callback matches on a CDN domain** — if the CDN changes (e.g., moves from Google Cloud Storage to S3), the pattern will not match. Make the CDN domain configurable.
- **`wait_for_timeout(2000)` is a fixed sleep** — on slow connections, 2 seconds may not be enough. Consider using `page.wait_for_event("download")` with a timeout instead of a fixed sleep.
- **This requires Playwright and its browser binaries** — not suitable for minimal CI environments. Install with `pip install playwright && python -m playwright install chromium`.

## Source reference

`scripts/resolve-download-url.py` — full implementation
