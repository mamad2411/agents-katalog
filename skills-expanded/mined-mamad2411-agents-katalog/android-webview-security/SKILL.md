---
name: android-webview-security
description: >
  Authorized Android WebView security review: JavaScript bridges (addJavascriptInterface),
  file URL access, universal access from file URLs, mixed content, SSL error handlers, and
  WebView XSS to native privilege. Use when reviewing owned apps, labs, and CTF APKs —
  not unauthorized third-party apps.
---

# Android WebView Security

## Scope And Authorization

- **In scope:** Owned apps, labs, CTFs, authorized assessments.
- **Out of scope:** Attacking third-party WebViews without permission.
- XSS in WebView can become native RCE-class impact via bridges — handle evidence carefully.
- Pair with `android-intent-security` and `code-quality-standards`.

## When To Use

- App embeds WebView for content, SSO, payments, or hybrid UI.
- Reviewing `addJavascriptInterface` and `@JavascriptInterface` methods.
- file:// origins, mixed content, or `onReceivedSslError` proceeding.
- Token leakage via WebView caches/cookies.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| General exported components | `android-exported-components` |
| Full mobile pentest hub | `android-pentesting-tricks` |
| Classic web XSS only | `xss-cross-site-scripting` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Setting / API | Safe default direction |
| --- | --- |
| `setJavaScriptEnabled` | Only if required |
| `addJavascriptInterface` | Minimal surface; validate origin |
| `setAllowFileAccess` | false unless required |
| `setAllowFileAccessFromFileURLs` | false |
| `setAllowUniversalAccessFromFileURLs` | false (dangerous) |
| Mixed content | Never allow insecure on HTTPS pages |
| SSL errors | Do not `handler.proceed()` |
| Cookies | Secure, HttpOnly where applicable; clear on logout |

## Workflow

### 1. Confirm scope and success criteria

1. Map each WebView: URL allowlist, JS on/off, bridges, file access.
2. Success: no sensitive bridge methods reachable from untrusted content; SSL errors fail closed; file universal access off.
3. Threat: XSS in loaded content + malicious intent loading URL.

### 2. Static inventory

```bash
jadx -d out app.apk
rg -n "WebView|addJavascriptInterface|setJavaScriptEnabled|setAllowFileAccess|onReceivedSslError|shouldOverrideUrlLoading" out/
```

Build table: WebView class → settings → interfaces → URL sources.

### 3. Bridge review

```java
// High risk pattern
webView.addJavascriptInterface(new Bridge(), "Android");
// Bridge methods become JS-callable when annotated
```

| Check | Action |
| --- | --- |
| Method sensitivity | No raw filesystem, no arbitrary intents, no auth tokens return |
| Origin | Verify `WebView` URL host allowlist before privileged ops |
| minSdk | Historical CVE for unannotated methods on old Android — know your minSdk |
| Input | Treat all JS args as untrusted |

### 4. Navigation and URL loading

```kotlin
override fun shouldOverrideUrlLoading(view: WebView, request: WebResourceRequest): Boolean {
    val host = request.url.host ?: return true
    if (host !in allowlist) return true // block
    return false
}
// Never load intent.getStringExtra("url") without allowlist
```

### 5. TLS and mixed content

```kotlin
// Bad
override fun onReceivedSslError(view: WebView, h: SslErrorHandler, e: SslError) {
    h.proceed()
}
// Good: h.cancel(); show error UI
webSettings.mixedContentMode = WebSettings.MIXED_CONTENT_NEVER_ALLOW
```

### 6. Dynamic tests (authorized)

```bash
# Load lab XSS page if WebView points to controllable content
# Frida/hooks only on owned builds to inspect bridge
adb logcat | rg -i webview
```

1. Attempt `javascript:` URLs if app loads untrusted intents.
2. Check cookie theft via XSS if JS enabled.

### 7. Remediate and verify

1. Disable unused JS/file access; shrink bridge API.
2. Prefer Chrome Custom Tabs for external content when embedding not required.
3. Clear WebView data on logout: `clearCache`, cookie manager remove.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Content | HTTPS allowlist | Any URL from Intent |
| Bridge | Few methods + origin checks | `exec(cmd)` bridge |
| SSL | Cancel on error | proceed always |
| Files | No universal file access | `setAllowUniversalAccessFromFileURLs(true)` |

## Output Checklist

- [ ] All WebViews inventoried
- [ ] JS/file/mixed/SSL settings reviewed
- [ ] Bridges origin-checked and minimized
- [ ] URL loading allowlisted
- [ ] SSL error handler safe
- [ ] Dynamic tests on owned builds
- [ ] Logout clears session data
- [ ] `code-quality-standards` applied

## Rules

- Authorized apps only.
- Untrusted web content + bridge = high severity until proven otherwise.
- Never ignore SSL errors in WebView.
- Prefer system browser for arbitrary URLs.
- Redact tokens found in WebView storage.
