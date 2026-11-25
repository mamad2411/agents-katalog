---
name: security-headers
description: Configure HTTP security headers to protect against XSS, clickjacking, MIME sniffing, and other browser-based attacks. Outputs CSP policies, HSTS, X-Frame-Options, and scanning/testing configuration.
argument-hint: [application type, CDN/proxy, third-party resources, browser support requirements]
allowed-tools: Read, Write, Bash
---

# Security Headers

HTTP response headers are your last line of browser-side defense. A strong security header configuration protects users even when application code has vulnerabilities, blocks common attack vectors, and signals security maturity to partners and auditors.

## Process

1. **Audit current headers** — scan with securityheaders.com or curl.
2. **Start with non-breaking headers** — X-Content-Type-Options, X-Frame-Options, Referrer-Policy.
3. **Build CSP in report-only mode** — collect violations without blocking, iterate until clean.
4. **Enable CSP enforcement** — after 2-4 weeks of report-only with zero violations.
5. **Enable HSTS** — short max-age first, increase after confirming no mixed content.
6. **Add to CI** — header regression tests in automated pipeline.
7. **Score and track** — monthly SecurityHeaders.com scan, target A+.

## Output Format

### Recommended Header Set

```
Content-Security-Policy: default-src 'self'; script-src 'self' 'nonce-{NONCE}'; style-src 'self' 'nonce-{NONCE}'; img-src 'self' data: https://cdn.example.com; font-src 'self'; connect-src 'self' https://api.example.com; frame-ancestors 'none'; base-uri 'self'; form-action 'self'; upgrade-insecure-requests; report-uri /csp-report
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), microphone=(), geolocation=(), payment=()
Cross-Origin-Opener-Policy: same-origin
Cross-Origin-Resource-Policy: same-origin
Cross-Origin-Embedder-Policy: require-corp
```

### Nginx Configuration

```nginx
# /etc/nginx/conf.d/security-headers.conf
# Include in server blocks or http context

# Never send server version
server_tokens off;

# ── Core Security Headers ─────────────────────────────────

# Prevent MIME type sniffing
add_header X-Content-Type-Options "nosniff" always;

# Clickjacking protection — DENY prevents all framing
add_header X-Frame-Options "DENY" always;

# Referrer policy — send origin only for cross-origin requests
add_header Referrer-Policy "strict-origin-when-cross-origin" always;

# HSTS — HTTPS only (start with short max-age, increase after validation)
# Phase 1 (first week): max-age=300
# Phase 2 (first month): max-age=86400
# Phase 3 (stable): max-age=31536000; includeSubDomains; preload
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;

# Disable browser features not used by this app
add_header Permissions-Policy "
    camera=(),
    microphone=(),
    geolocation=(),
    payment=(),
    usb=(),
    bluetooth=(),
    serial=()
" always;

# Cross-Origin Isolation (required for SharedArrayBuffer)
add_header Cross-Origin-Opener-Policy "same-origin" always;
add_header Cross-Origin-Resource-Policy "same-origin" always;

# ── Content Security Policy ───────────────────────────────
# Adjust allowlist based on your actual resource sources

# Phase 1: Report-only (doesn't block, just reports)
add_header Content-Security-Policy-Report-Only "
    default-src 'self';
    script-src 'self' 'nonce-$request_id';
    style-src 'self' 'nonce-$request_id';
    img-src 'self' data: https://cdn.example.com https://www.gravatar.com;
    font-src 'self' https://fonts.gstatic.com;
    connect-src 'self' https://api.example.com https://analytics.example.com;
    media-src 'none';
    object-src 'none';
    frame-src 'none';
    frame-ancestors 'none';
    base-uri 'self';
    form-action 'self';
    upgrade-insecure-requests;
    report-uri /api/csp-report;
" always;

# Phase 2: Enforce (after report-only shows clean for 2+ weeks)
# add_header Content-Security-Policy "..." always;

# ── Cache Control for Sensitive Pages ────────────────────
location /account {
    add_header Cache-Control "no-store, no-cache, must-revalidate, max-age=0";
    add_header Pragma "no-cache";
}
```

### Apache Configuration

```apache
# .htaccess or VirtualHost
Header always set X-Content-Type-Options "nosniff"
Header always set X-Frame-Options "DENY"
Header always set Referrer-Policy "strict-origin-when-cross-origin"
Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains; preload"
Header always set Permissions-Policy "camera=(), microphone=(), geolocation=()"

# CSP with nonce (requires mod_unique_id or custom nonce generation)
Header always set Content-Security-Policy "default-src 'self'; script-src 'self' 'nonce-%{UNIQUE_ID}e'"

# Remove server identification
ServerSignature Off
ServerTokens Prod
```

### Application-Level (FastAPI/Python)

```python
# middleware/security_headers.py
import secrets
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Inject security headers on every response."""
    
    def __init__(self, app, csp_policy: str = None, enforce_csp: bool = False):
        super().__init__(app)
        self.enforce_csp = enforce_csp
        self.csp_policy = csp_policy
    
    async def dispatch(self, request: Request, call_next):
        # Generate per-request nonce for CSP
        nonce = secrets.token_urlsafe(16)
        request.state.csp_nonce = nonce
        
        response: Response = await call_next(request)
        
        # Core headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Strict-Transport-Security"] = (
            "max-age=31536000; includeSubDomains; preload"
        )
        response.headers["Permissions-Policy"] = (
            "camera=(), microphone=(), geolocation=(), payment=()"
        )
        response.headers["Cross-Origin-Opener-Policy"] = "same-origin"
        response.headers["Cross-Origin-Resource-Policy"] = "same-origin"
        
        # Remove information-leaking headers
        response.headers.pop("X-Powered-By", None)
        response.headers.pop("Server", None)
        
        # Content Security Policy
        csp = self._build_csp(nonce)
        header_name = "Content-Security-Policy" if self.enforce_csp else "Content-Security-Policy-Report-Only"
        response.headers[header_name] = csp
        
        return response
    
    def _build_csp(self, nonce: str) -> str:
        directives = {
            "default-src": ["'self'"],
            "script-src": ["'self'", f"'nonce-{nonce}'"],
            "style-src": ["'self'", f"'nonce-{nonce}'"],
            "img-src": ["'self'", "data:", "https://cdn.example.com"],
            "font-src": ["'self'"],
            "connect-src": ["'self'", "https://api.example.com"],
            "media-src": ["'none'"],
            "object-src": ["'none'"],
            "frame-src": ["'none'"],
            "frame-ancestors": ["'none'"],
            "base-uri": ["'self'"],
            "form-action": ["'self'"],
            "upgrade-insecure-requests": [],
            "report-uri": ["/api/csp-report"],
        }
        
        return "; ".join(
            f"{directive} {' '.join(values)}" if values else directive
            for directive, values in directives.items()
        )


# CSP violation report endpoint
from fastapi import FastAPI, Request
import logging

app = FastAPI()
logger = logging.getLogger("csp")

@app.post("/api/csp-report")
async def csp_report(request: Request):
    body = await request.json()
    report = body.get("csp-report", {})
    
    logger.warning(
        "CSP violation",
        extra={
            "blocked_uri": report.get("blocked-uri"),
            "violated_directive": report.get("violated-directive"),
            "document_uri": report.get("document-uri"),
            "source_file": report.get("source-file"),
        }
    )
    return {}

app.add_middleware(SecurityHeadersMiddleware, enforce_csp=False)
```

### CDN Configuration (CloudFront)

```python
# cloudfront_security_headers.py — Lambda@Edge function
import secrets

def handler(event, context):
    response = event["Records"][0]["cf"]["response"]
    headers = response["headers"]
    
    nonce = secrets.token_urlsafe(16)
    
    headers["x-content-type-options"] = [{"value": "nosniff"}]
    headers["x-frame-options"] = [{"value": "DENY"}]
    headers["referrer-policy"] = [{"value": "strict-origin-when-cross-origin"}]
    headers["strict-transport-security"] = [{
        "value": "max-age=31536000; includeSubDomains; preload"
    }]
    headers["permissions-policy"] = [{
        "value": "camera=(), microphone=(), geolocation=()"
    }]
    headers["content-security-policy-report-only"] = [{
        "value": (
            f"default-src 'self'; "
            f"script-src 'self' 'nonce-{nonce}'; "
            "object-src 'none'; "
            "base-uri 'self'; "
            "report-uri https://csp.example.com/report"
        )
    }]
    
    # Remove identifying headers
    headers.pop("server", None)
    headers.pop("x-powered-by", None)
    
    return response
```

### Testing Headers

```bash
# Scan with curl
curl -I https://example.com | grep -i "content-security\|strict-transport\|x-frame\|x-content"

# Test CSP with Mozilla Observatory
curl -s "https://http.observatory.mozilla.org/api/v1/analyze?host=example.com" \
  -X POST | jq '.score, .grade'

# Validate HSTS preload eligibility
curl -s "https://hstspreload.org/api/v2/status?domain=example.com" | jq .

# Python test in CI
import httpx
import pytest

class TestSecurityHeaders:
    @pytest.fixture
    def response(self):
        return httpx.get("https://staging.example.com/")
    
    def test_x_content_type_options(self, response):
        assert response.headers.get("x-content-type-options") == "nosniff"
    
    def test_x_frame_options(self, response):
        assert response.headers.get("x-frame-options") == "DENY"
    
    def test_hsts_present(self, response):
        hsts = response.headers.get("strict-transport-security", "")
        assert "max-age=" in hsts
        assert "includeSubDomains" in hsts
    
    def test_csp_present(self, response):
        csp = (
            response.headers.get("content-security-policy") or
            response.headers.get("content-security-policy-report-only", "")
        )
        assert "default-src" in csp
        assert "object-src 'none'" in csp
    
    def test_no_server_header(self, response):
        assert "server" not in response.headers or response.headers["server"] == ""
```

## Rules

- **Start with report-only CSP** — never enforce untested CSP in production; it will break things.
- **Nonces over `unsafe-inline`** — `'unsafe-inline'` defeats XSS protection; use per-request nonces.
- **`object-src 'none'`** — Flash and plugins are dead; block them explicitly.
- **`base-uri 'self'`** — prevents `<base>` tag injection for open redirects.
- **HSTS max-age 1 year minimum** — shorter values don't protect returning users.
- **`includeSubDomains` only if all subdomains are HTTPS** — it will break HTTP subdomains.
- **Test headers in CI** — add to your smoke test suite so regressions are caught.
- **Monitor CSP violation reports** — violations indicate real attacks or policy gaps.
- **Remove `X-Powered-By` and `Server`** — don't tell attackers your stack.
- **Separate CSP for APIs** — JSON APIs don't need script-src; a tighter policy reduces attack surface.
