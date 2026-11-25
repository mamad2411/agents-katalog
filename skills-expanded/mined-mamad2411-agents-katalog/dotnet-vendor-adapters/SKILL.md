---
name: dotnet-vendor-adapters
description: Apply when implementing or modifying integration adapters for external third-party services — typed HttpClient, OAuth2 token caching, HMAC verification, Options binding, secret provenance.
metadata:
  stack: [dotnet]
  requires: [dotnet-clean-architecture]
---

# .NET vendor adapters (security-critical)

Vendor integrations live in `Infrastructure/Adapters/<Vendor>/`. Each adapter implements an Application-layer port. The following rules are security-load-bearing.

## Typed HttpClient adapters

- Register via `services.AddHttpClient<IPort, Adapter>()` — never `new HttpClient()`.
- The adapter's primary constructor takes the resolved `HttpClient` plus its `Options` class.
- `HttpClient` is scoped per request; connection pooling is managed by `IHttpClientFactory`. Manually `new`-ing breaks socket reuse and exhausts ports.

```csharp
public class VendorXAdapter(HttpClient httpClient, IOptions<VendorXOptions> options) : IVendorXPort
{
    // use httpClient directly; do not field-shadow
}
```

## OAuth2 client-credentials token caching

- Cache access tokens in `IMemoryCache`.
- TTL = `expires_in - 30s` to absorb clock skew and pre-empt expiry mid-request.
- One cache key per vendor (e.g. `oauth:vendor-x`, `oauth:vendor-y`).
- Refresh **lazily on cache miss**; never proactively poll.

## HMAC verification (webhooks)

- Always `HMACSHA256`. No other algorithms.
- Compare with `CryptographicOperations.FixedTimeEquals` on UTF-8 byte arrays — never `string.Equals` (timing attack).
- Defensively parse `sha256=<hex>` prefixes: split on `=`, validate the prefix, validate hex length, validate hex chars.
- Reject on **any** parse failure with `UnauthorizedAccessException`. Do not throw — the middleware will translate to 401 with no body (see `dotnet-api-design` skill).

```csharp
var expected = HMACSHA256.HashData(sharedSecret, payload);
if (!CryptographicOperations.FixedTimeEquals(expected, providedBytes))
    throw new UnauthorizedAccessException();
```

## Options bind + validate

Every vendor integration has its own Options class:

```csharp
services
    .AddOptions<VendorXOptions>()
    .Bind(configuration.GetSection("VendorX"))
    .ValidateDataAnnotations()
    .ValidateOnStart();
```

Missing or malformed values must fail the **host boot**, not the request. `ValidateOnStart()` is mandatory.

## Secret provenance

Distinguish in `docs/design/<feature>.md`:

| Class | Provenance | Examples |
|---|---|---|
| **Internal secrets** | Generated locally, never shared externally, common across all instances of the API | State-signing keys, internal HMAC keys for our own state-passing |
| **Shared secrets** | Issued by the vendor / partner, held in both places | Webhook shared secrets, vendor client secrets, API keys |

Document which class each secret belongs to. This drives:

- **Rotation procedure** — internal secrets we rotate ourselves; shared secrets require coordinating with the vendor.
- **Storage layout** — internal secrets in our Key Vault scoped to API; shared secrets in a vendor-specific section.

## Anti-patterns

- `new HttpClient()` — breaks pooling, leaks sockets.
- Caching OAuth tokens with the vendor's `expires_in` value verbatim — token expires mid-request.
- HMAC comparison via `==` or `string.Equals` — timing attack.
- Options bound without `ValidateOnStart()` — misconfiguration explodes at first request instead of boot.
- Echoing `ex.Message` from a `ProviderException` — message may include the vendor's response body which can leak internals (see `dotnet-api-design`).
- Storing vendor client secrets in `appsettings.json` (even Development) — always Key Vault.
