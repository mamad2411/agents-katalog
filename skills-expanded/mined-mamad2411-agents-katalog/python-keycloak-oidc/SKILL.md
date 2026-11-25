---
name: python-keycloak-oidc
description: Use when integrating Keycloak (or generic OIDC) into Python — token validation with python-jose, DRF auth backend, JWKS rotation, common pitfalls.
metadata:
  added: 2026-05-18
  last_reviewed: 2026-05-18
  type: domain
  languages: [python]
  status: active
  invokes_shell: false
  shell_reviewed: "valksor 2026-05-18"
  related: [python-essentials, python-django, python-fastapi, security]
---

# Python Keycloak / OIDC

**Iron Law: pin the algorithm. ALWAYS pass `algorithms=["RS256"]` (or whatever your realm uses) — never read the algorithm from the token header. Verify `aud`, `iss`, and `exp`. A single-algorithm allow-list closes alg-confusion and "alg: none" attacks at the door.**

**Versions:** python-jose `3.3` · cryptography `43+` · Keycloak `26.x` (current LTS line) — _python-jose is the de-facto standard but slow-moving; consider `pyjwt[crypto]` 2.10+ if you need PS256 perf and active maintenance. Keycloak 26 supports the `oauth2-device-code` and `urn:ietf:params:oauth:grant-type:token-exchange` flows out of the box._

## OIDC refresher (auth code + PKCE)

```
Browser ──(1) /authorize?response_type=code&code_challenge=...─▶ Keycloak
        ◀──(2) 302 with ?code=&state=──────────────────────────
Browser ──(3) /token  code=...&code_verifier=...──────────────▶ Keycloak
        ◀──(4) { access_token, id_token, refresh_token }──────
Browser ──(5) Authorization: Bearer <access_token>───────────▶ Your API
                                                     Your API verifies sig + claims
```

**Use Authorization Code + PKCE for everything**, including SPAs and mobile. Implicit flow is dead. Password grant is dead (Keycloak still supports it, don't). For service-to-service: **Client Credentials** with a confidential client; never use a real user's password from a backend.

## Token verification — the safe pattern

```python
# python-jose; equivalent in pyjwt is parallel
from jose import jwt, JWTError
import httpx, time, threading

JWKS_URL = "https://kc.example.com/realms/myrealm/protocol/openid-connect/certs"  # replace myrealm
ISSUER   = "https://kc.example.com/realms/myrealm"                                # replace myrealm
AUDIENCE = "myapp"                    # client_id you're protecting
ALGS     = ["RS256"]                  # pin — never trust header alg

class JWKSCache:
    """Thread-safe JWKS cache with a 1-hour TTL and on-miss refresh for kid rotation.
    Double-checked locking: hold the lock ONLY for cache check + swap, never across the network
    fetch — otherwise every concurrent caller serializes during JWKS rotation and a slow
    Keycloak amplifies latency under load. NOTE: the lock-free 1st check relies on CPython GIL
    atomicity for attribute reads. Under free-threaded Python 3.13+ (`python3t`), wrap the 1st
    check in the lock too OR use `asyncio.Lock` for async stacks."""
    def __init__(self, ttl: float = 3600):
        self._lock = threading.Lock()
        self._ttl = ttl
        self._fetched_at = 0.0
        self._keys: dict = {"keys": []}

    def get(self, kid: str | None = None) -> dict:
        # 1st check — no lock
        if not self._needs_refresh(kid):
            return self._keys
        # Fetch OUTSIDE the lock; multiple racing fetches are fine, only the final swap is locked
        fresh = httpx.get(JWKS_URL, timeout=5).raise_for_status().json()
        with self._lock:
            # 2nd check inside the lock: another thread may have just swapped
            if self._needs_refresh(kid):
                self._keys = fresh
                self._fetched_at = time.time()
            return self._keys

    def _needs_refresh(self, kid):
        stale = time.time() - self._fetched_at > self._ttl
        unknown = kid is not None and not any(k["kid"] == kid for k in self._keys["keys"])
        return stale or unknown

_jwks = JWKSCache()

def verify(token: str) -> dict:
    try:
        header = jwt.get_unverified_header(token)              # safe — used only to pick a key
        keys = _jwks.get(kid=header.get("kid"))
        return jwt.decode(
            token, keys,
            algorithms=ALGS,                                   # PIN — closes alg-confusion
            audience=AUDIENCE,                                 # required — refuses tokens for other clients
            issuer=ISSUER,                                     # required — refuses tokens from other realms
            options={"verify_at_hash": False},                 # access tokens don't carry at_hash. NEVER set False when verifying an ID token — at_hash binds it to the access token issued in the same flow.
        )
    except JWTError as e:
        raise PermissionError(f"invalid token: {e}") from e
```

**Guards that matter** (each closes a real attack):

| Guard                                     | Stops                                                                                |
| ----------------------------------------- | ------------------------------------------------------------------------------------ |
| `algorithms=["RS256"]` (single-item list) | `alg: none` forgery; HS-vs-RS confusion (signing with the public key as HMAC secret) |
| `audience=AUDIENCE`                       | Token issued for another client of the same realm                                    |
| `issuer=ISSUER`                           | Token from another realm / KC instance                                               |
| JWKS-by-`kid` + refresh on miss           | Silent key-rotation breakage; key-substitution                                       |
| `httpx.get(JWKS_URL)` timeout + raise     | DoS via a slow JWKS endpoint hanging the verifier                                    |

**Never** `jwt.decode(..., verify=False)`. **Never** trust `jwt.get_unverified_claims()` for anything beyond picking a key.

## DRF authentication backend

```python
# apps/auth/backends.py
from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model
from .keycloak import verify           # function above

User = get_user_model()

class KeycloakAuthentication(BaseAuthentication):
    keyword = b"bearer"
    def authenticate(self, request):
        auth = get_authorization_header(request).split()
        if not auth or auth[0].lower() != self.keyword: return None
        if len(auth) != 2: raise AuthenticationFailed("malformed Authorization header")
        try: claims = verify(auth[1].decode("ascii"))
        except PermissionError as e: raise AuthenticationFailed(str(e))
        user, _ = User.objects.get_or_create(username=claims["sub"], defaults={"email": claims.get("email", "")})
        request.keycloak_claims = claims                      # views read roles without re-decoding
        return (user, claims)
```

```python
# settings.py
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "apps.auth.backends.KeycloakAuthentication",
        # keep SessionAuthentication only if the Django admin shares this API
    ],
}
```

## Roles, groups, and authorization

Keycloak emits roles in two places — know which your client uses:

| Claim                               | Use                                                         |
| ----------------------------------- | ----------------------------------------------------------- |
| `realm_access.roles`                | realm-level (cross-application: `admin`, `support`)         |
| `resource_access.<client_id>.roles` | client-level (per-app: `reports:read`, `orders:write`)      |
| `groups`                            | group membership (needs "Group Membership" protocol mapper) |

```python
def has_client_role(claims, role, client=AUDIENCE):
    return role in claims.get("resource_access", {}).get(client, {}).get("roles", [])
```

Map permissions per-endpoint server-side every request; only trust the validated token's claims.

## Access vs ID vs refresh token

- **Access token** → your API; you verify. Carries authorization (roles, scope).
- **ID token** → for the client (SPA verifies, not your API). Carries identity (`email`, `name`, `at_hash`).
- **Refresh token** → opaque to client; `/token` mints new access tokens. HttpOnly cookie only; never `localStorage`.

## Logout / session termination

`POST /realms/<realm>/protocol/openid-connect/logout` with the refresh token revokes the SSO session. For multi-app SSO use back-channel logout (`backchannel_logout_url` pushes `logout_token` to your service) — it's the only way to invalidate one app when the user logs out of another.

## Common pitfalls

- Skipping `audience` check (token from app-A accepted by app-B in the same realm); accepting `alg: none`
- HS-vs-RS alg-confusion — pin `algorithms=["RS256"]`; no `leeway` for clock skew (`options={"leeway": 30}`)
- Logging raw `Authorization` header (tokens in log aggregators); extending Keycloak's 5-min access-token TTL
- JWKS fetch every request (DoSes Keycloak); JWKS over HTTP (MITM swaps keys — HTTPS only, pin issuer)
- Realm-vs-client role confusion (`realm_access.roles` vs `resource_access.<client>.roles`)
- Trusting `preferred_username` as a primary key (users can change it; use `sub`)

## Anti-patterns

- `jwt.decode(verify=False)` to "peek at claims"; custom JWT verifier (see `Skill(security)`)
- Access tokens in `localStorage` (XSS) — HttpOnly cookies or in-memory; client secrets in SPA bundles
- Refresh tokens > 30 days without rotation; skipping `state`/`nonce` in callback (CSRF)
- `mark_safe` on token claims rendered in templates (XSS via crafted `name`)

## Red flags

| Thought                             | Reality                                                         |
| ----------------------------------- | --------------------------------------------------------------- |
| "We'll add audience check later"    | Cross-client token replay works today                           |
| "Leeway isn't needed in containers" | NTP drift happens; 30s leeway costs nothing                     |
| "Cache the JWKS forever"            | Key rotation breaks silently — TTL + on-miss refresh            |
| "Password grant for mobile"         | Apple/Google reject this; Auth Code + PKCE on custom URL scheme |
| "JWT in `localStorage` is easier"   | Until the first XSS — HttpOnly cookies                          |

## Hand-off

Django + DRF viewsets/permissions: `Skill(devkit:python-django)` (full DRF patterns in `references/drf.md`). FastAPI auth: `Skill(devkit:python-fastapi)`. Broader auth/crypto rules: `Skill(devkit:security)`. OWASP A02/A07 context: `Skill(devkit:security)`.
