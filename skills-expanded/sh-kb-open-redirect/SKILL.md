---
name: sh-kb-open-redirect
description: "Knowledge base for finding open/unvalidated redirects - user-controlled redirect targets that send victims to attacker sites, enabling phishing, token leakage, and OAuth/SSO abuse. Use when hunting open redirects. CWE-601, OWASP A01:2021-Broken Access Control."
---

# Open Redirect - Hunter Knowledge Base

The app redirects to a URL taken from user input without restricting the destination. On its own it's a
phishing/trust-abuse issue; chained (OAuth `redirect_uri`, token in URL, SSO), it can leak credentials or
tokens.

## When to hunt this
Login/logout `?next=`/`?return_to=`/`?redirect=`/`?url=` params, post-action redirects, OAuth/OIDC
`redirect_uri`, SSO relay-state, "continue to" links, URL shorteners/proxies, `Location` set from input.

## Sinks (grep targets)
- **Python**: `redirect(request.args.get(...))`, Flask `redirect(url)`, Django `HttpResponseRedirect(user)`,
  `return redirect(next)`.
- **JS/TS**: `res.redirect(userUrl)`, `window.location = user`, `location.href = user`, `location.assign`,
  Next.js `redirect(user)`.
- **Java**: `response.sendRedirect(user)`, Spring `"redirect:" + user`, `RedirectView`.
- **PHP**: `header("Location: " . $user)`. **Go**: `http.Redirect(w, r, userURL, ...)`.
- Grep: `sendRedirect|res.redirect|HttpResponseRedirect|\bredirect\(|Location:\s|location.href|window.location`.

## Detection recipe
1. `graft grep "redirect\(|sendRedirect|HttpResponseRedirect|Location:|location.(href|assign)" --json`.
2. Trace the redirect target to user input.
3. Check for a validity check: is the target constrained to a relative path or an allowlisted host? Naive
   checks (`startswith("/")`, `contains("mysite.com")`) are often bypassable.

## Payloads / PoC
- `?next=https://evil.com`, `?url=//evil.com` (scheme-relative), `?url=https:evil.com`,
  `?next=/\evil.com`, `?url=https://mysite.com.evil.com`, `?url=https://mysite.com@evil.com`,
  backslash/whitespace/CRLF tricks, `?url=javascript:alert(1)` (if it reaches a DOM sink).
- Bypass of `startswith("/")`: `//evil.com`, `/\evil.com`, `/%2f%2fevil.com`.
- PoC: request the endpoint with the crafted target and observe a redirect to the attacker host.

## False-positive filters
- Target is forced relative (leading single `/` **and** not `//`/`/\`) after normalization, or resolved
  against the app origin and re-checked.
- Destination validated against a strict host allowlist (exact host match, not substring/`endsWith`).
- Redirect target is server-chosen (not user input) or an opaque id mapped to a known URL.

## CWE / OWASP / severity
CWE-601. OWASP A01:2021. Usually **medium** standalone; **high** when it leaks OAuth codes/tokens or is a
step in account takeover.

## Chaining hints
Open redirect + OAuth `redirect_uri` -> steal authorization code -> account takeover; + token/Referer leak
-> session theft (`auth`); + `ssrf` allowlist bypass (redirect from allowed host to internal); boosts
phishing credibility. Frequently the first hop in takeover chains.

## Mitigation
Avoid user-controlled redirect targets; if needed, allowlist exact destination hosts or force
same-origin/relative paths (reject `//`, `/\`, absolute URLs, and non-http schemes) after canonicalization;
for OAuth, exact-match `redirect_uri` against pre-registered values; show an interstitial for external links.
