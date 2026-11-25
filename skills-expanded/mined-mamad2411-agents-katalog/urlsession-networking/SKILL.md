---
name: urlsession-networking
description: Project-specific networking conventions — the `APIClient` protocol boundary, DTO/domain separation, where `APIError` stops and `DomainError` starts, the `AuthTokenProvider` contract, and the `URLProtocol` testing seam. Load when adding or editing any API call, request interceptor, or `Codable` model.
---

# Networking (project delta)

For URLSession fundamentals — `data(for:)`, `URLRequest` construction, `URLComponents`, `Codable` / `JSONDecoder` strategies, `URLSessionConfiguration` — read [Apple's URL Loading System documentation](https://developer.apple.com/documentation/foundation/url_loading_system). This file documents only this project's decisions. The canonical `URLSessionAPIClient` template lives in `.claude/skills/ios-app-skeleton/references/app-target.md`.

## When this applies

`URLSession` + `async`/`await` + `Codable`, behind an `APIClient` protocol. On an existing app:

- **Alamofire** (`import Alamofire`, `AF.request`, `Session`) → skip the client shape below. The framework-agnostic rules still hold: one injected client protocol, DTOs separate from domain models, errors mapped at the repository boundary.
- **Apollo / GraphQL** (`import Apollo`) → generated query types replace DTOs; the repository still maps into `Outcome<T>` and `DomainError`.
- **Moya** → same as Alamofire; the `TargetType` enum is that project's endpoint definition, don't replace it.
- **A hand-rolled client that isn't behind a protocol** → the testability argument is worth making, but retrofitting the seam is its own change, not a drive-by.

## The pipeline

```
AppCore.Repository protocol      # domain types, returns Outcome<T>
        ↓
App.LiveRepository               # calls the client, maps DTO → domain, APIError → DomainError
        ↓
App.URLSessionAPIClient          # URLSession wrapper, JSON encode/decode, auth header
        ↓
URLSession                       # system networking
```

**`APIClient` is a protocol in `AppCore`; only `App` knows `URLSession` exists.** That's the seam that makes `AppFeatures` testable without a network stub.

## Where errors stop

**`APIError` is a data-layer type and never crosses into the domain.** It may carry status codes and `URLError`s; `DomainError` may not.

```swift
private func map(_ error: APIError) -> DomainError {
    switch error {
    case .invalidResponse:       return .unknown("invalid response")
    case .status(let code, _):
        switch code {
        case 401:      return .unauthorized
        case 404:      return .notFound
        case 500...599: return .server(code: code)
        default:       return .unknown("HTTP \(code)")
        }
    }
}
```

A `URLError` or `DecodingError` reaching a view model is a bug the reviewer flags every time. So is a repository that maps `CancellationError` into a failure — see `swift-style`.

## DTOs

Named `…DTO`, `Decodable` + `Sendable`, living in the data layer, **never exposed upward**.

- **Nullability reflects the wire format, not what the domain wants.** If the server can omit it, the DTO field is optional and the mapper decides the domain default.
- **Mapping is a one-way `toDomain()`** function in an extension next to the DTO. No shared `Mapper` protocol — it buys nothing.
- Unknown enum values: give the DTO enum a fallback case, or let the decoder throw and handle it at the boundary. Don't crash on an server-side addition.

Decoder configuration is shared, not per-call:

```swift
extension JSONDecoder {
    static let api: JSONDecoder = {
        let d = JSONDecoder()
        d.keyDecodingStrategy = .convertFromSnakeCase
        d.dateDecodingStrategy = .iso8601
        return d
    }()
}
```

## Authentication

Token access goes through a protocol, backed by the Keychain (see `keychain-secure-storage`):

```swift
protocol AuthTokenProvider: Sendable {
    func current() async throws -> String?
    func refresh() async throws -> String
    func clear() async throws
}
```

**Refresh logic lives in the token provider, not the client.** The client asks for a token before each request and knows nothing about expiry, retry, or the refresh endpoint. That keeps the "401 → refresh → retry once" policy in one testable place instead of smeared across call sites.

## Testing seam

Inject the `URLSession`. Production passes `.shared`; tests pass a session configured with a custom `URLProtocol` subclass — the pattern is in `ios-testing`. **`URLSession.shared` is not untestable; hard-coding it is.**

## Logging

- DEBUG builds only, and never request or response bodies.
- `Authorization` headers are redacted, always. So is any body field that could carry PII.
- `Logger` from `os` with explicit privacy modifiers — see `swift-style`.

## Common pitfalls

- **`Data(contentsOf:)` for HTTP** — synchronous, swallows errors, blocks whatever thread it's on. Never.
- **Missing `Content-Type` on POST/PUT** — many APIs reject the request with an unhelpful error.
- **A new `JSONDecoder` per call** — cheap, but the shared configured one is both cheaper and consistent.
- **Force-unwrapping `URLComponents.url`** — a path with an unescaped character makes it `nil` and crashes in production. `guard` and return a `DomainError`.
