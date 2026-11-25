---
name: browser-extension-security
description: >
  Authorized browser extension security review: manifest permissions, content scripts,
  background/service workers, messaging, web_accessible_resources, update and store
  packaging risks. Use when assessing Chrome/Firefox/Edge extensions you own or are
  scoped to review, MV2/MV3 manifests, or extension XSS and privilege-escalation patterns
  in lab or engagement work.
---

# Browser Extension Security

## Scope And Authorization

- **In scope:** Extensions you own, enterprise-deployed extensions you are authorized to assess, or store listings under RoE.
- **Out of scope:** Publishing malicious extensions, stealing user sessions from third-party extensions without authorization, or drive-by abuse.
- Prefer static review + local sideload dynamic tests; do not mass-install on employee browsers without approval.
- Redact OAuth secrets, API keys in `storage`, and user PII from reports.
- Pair MV3 engineering migration with `browser-extension-mv3-migration`; token storage with `browser-storage-security`.

## When To Use

- Security design review before Chrome Web Store / add-on store submission.
- Audit of high privileges: `<all_urls>`, `debugger`, `webRequest`, `nativeMessaging`, `cookies`.
- Threat model for content script XSS → extension privilege escalation.
- Review of message passing (`runtime.sendMessage`, `externally_connectable`).
- Incident: compromised extension update or malicious dependency in extension bundle.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| MV2→MV3 engineering migration | `browser-extension-mv3-migration` |
| Site XSS not involving extensions | `xss-cross-site-scripting` |
| Generic web session storage | `browser-storage-security` |
| Supply chain for npm packages broadly | npm supply-chain skills |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Surface | Risk |
| --- | --- |
| `permissions` / `host_permissions` | Over-broad read/modify of all sites |
| Content scripts | Share DOM with page → XSS into extension if unsafe |
| Background / SW | Trusted high privilege; entry via messages |
| `web_accessible_resources` | Pages can load extension assets; fingerprint + XSS gadgets |
| Messaging | Spoofed senders if not validated |
| Updates | Store account takeover → malicious update to all users |
| Native messaging | Bridge to OS-level agents |

## Workflow

### 1. Confirm scope and success criteria

1. Record extension IDs, browsers, distribution (store, enterprise CRX), data handled (cookies, tokens).
2. Success: least permissions; no critical XSS-to-privilege paths; messaging locked down; secrets not in client code; findings ticketed.
3. Agree dynamic test boundaries (which accounts/sites).

### 2. Static manifest review

```bash
# Unpack CRX/XPI or use source
python -m json.tool manifest.json
rg -n "permissions|host_permissions|content_scripts|web_accessible|externally_connectable|content_security_policy" manifest.json
```

**Checklist:**

| Item | Ask |
| --- | --- |
| Host permissions | Can matches be narrowed to exact origins? |
| Sensitive perms | Why `tabs`, `cookies`, `history`, `debugger`, `proxy`? |
| Content scripts | Matches least? `all_frames`? `run_at` document_start necessity? |
| WAR | Resources exposed to which sites? |
| CSP | `script-src 'self'` only? No remote script? |
| Update URL | Self-hosted updates integrity? |
| externally_connectable | Which external IDs/origins can message? |

### 3. Map trust boundaries

```text
Web page (untrusted DOM)
  → content script (isolated world, but DOM shared)
    → runtime messages
      → background/SW (privileged APIs)
        → extension storage / native host / network
```

1. Assume page can call exposed `window` hooks if you inject them — do not put privileged APIs on `window`.
2. Assume DOM XSS in page can attack content scripts that read `innerHTML` unsafely or execute page-controlled strings.
3. Treat network responses as untrusted unless pinned and schema-validated.

### 4. Review code sinks

```bash
rg -n "innerHTML|outerHTML|insertAdjacentHTML|document\\.write|eval\\(|new Function|setTimeout\\([\\\"']" -g '*.{js,ts}'
rg -n "chrome\\.(cookies|tabs|debugger|webRequest|scripting)" -g '*.{js,ts}'
rg -n "onMessage|sendMessage|connect|externally_connectable" -g '*.{js,ts}'
```

**High-risk patterns:**

| Pattern | Issue |
| --- | --- |
| Content script `element.innerHTML = pageData` | XSS in isolated world may still escalate via messages |
| Background accepts message without `sender.id` / URL checks | Any site/extension may trigger privileged actions |
| `chrome.tabs.executeScript` with string from message | Remote code execution in page/extension context |
| Storing session tokens in `storage.local` world-readable to XSS | Token theft if extension XSS exists |
| Logging tokens to central server without need | Privacy + breach impact |

**Message handler hardening sketch:**

```js
chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  if (sender.id !== chrome.runtime.id) return; // same-extension
  // For tabs: validate sender.url against allowlist origins
  if (!msg || msg.type !== "ALLOWED_TYPE") return;
  // Prefer capability-limited commands, not generic "eval this"
});
```

### 5. Dynamic tests (authorized)

1. Sideload extension; open a controlled HTML page that attempts to:
   - Load `chrome-extension://<id>/` WAR assets.
   - PostMessage / call exposed hooks.
   - Reflect XSS into a DOM the content script reads (lab page you own).
2. Confirm missing host permission blocks API calls.
3. Intercept update package (enterprise lab) for integrity process review.
4. Check popup/options pages for XSS (extension pages are privileged).

### 6. Supply chain and packaging

1. Lockfile + `npm audit` / OS SVR; pin build toolchain.
2. Reproducible build notes; no postinstall scripts from untrusted deps without review.
3. Store account: 2FA, security contacts, minimum publishers.
4. Privacy policy matches actual data collection (store compliance is security-adjacent).

### 7. Report and remediate

| Severity guide | Examples |
| --- | --- |
| Critical | Page → background RCE / arbitrary cookie exfil all hosts |
| High | Over-broad hosts + XSS in extension page |
| Medium | WAR overexposure, weak message validation |
| Low | Excess permission unused, verbose errors |

1. Prefer permission reduction and message allowlists over “we trust our site”.
2. Retest after fixes; ship MV3-safe patterns.
3. Apply `code-quality-standards` on patches.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Permissions | Exact origins + optional grants | `<all_urls>` + `cookies` unused |
| Content scripts | Minimal DOM read; no privileged window API | `window.doAdmin = ...` |
| Messaging | Type allowlist + sender checks | `eval(msg.code)` in background |
| WAR | Narrow matches + non-sensitive assets | Expose all JS to every site |
| Tokens | Ephemeral; HttpOnly site cookies when possible | Long-lived secrets in `storage.local` |
| Updates | 2FA store + signed pipeline | Shared store password in 1Password “Team” |

## Output Checklist

- [ ] Scope, extension IDs, distribution model recorded
- [ ] Manifest permission matrix completed
- [ ] Trust boundary diagram (even brief) written
- [ ] Sink review (XSS, messaging, scripting) done
- [ ] Dynamic abuse cases on lab pages executed
- [ ] WAR / externally_connectable reviewed
- [ ] Supply chain and store account checked
- [ ] Findings severity-rated with repro
- [ ] Retest plan after fixes
- [ ] Cross-links to MV3 / storage skills as needed

## Rules

- Authorized assessment and owned extension development only.
- Least privilege permissions; justify each for store and users.
- Never execute untrusted strings in background/SW.
- Assume web pages are hostile to content scripts.
- Focus here on security review; migration mechanics live in `browser-extension-mv3-migration`.
