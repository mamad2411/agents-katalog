---
name: ios-rest-api
description: Use when adding or changing a backend REST call in the iOS app (AgenticApp), including fixtures for tests.
---

# iOS REST API layer

## Adding an endpoint

1. Define the response model as `Decodable` (and `Equatable` for tests).
2. Add it to `Endpoints` in `Core/Networking/Endpoint.swift`:
   `static func orders(token: String) -> Endpoint<[Order]> { Endpoint(path: "/api/orders", token: token) }`
3. Call it from a repository in `Core/Services`, never from a view or view model:
   `try await apiClient.send(Endpoints.profile)`
4. Add a fixture in `AgenticApp/Resources/Fixtures/`: the path without `/api/`, slashes as dashes (`/api/auth/signin` → `auth-signin.json`). UI and end-to-end tests use it. Endpoints returning `EmptyResponse` need no fixture.
5. Unit test the repository with `MockAPIClient`, and request building with `StubURLProtocol`.

## Rules

- Base URL comes from the environment (`Config/*.xcconfig`, `API_BASE_URL`). Never hard-code URLs.
- Errors surface as `APIError`; view models turn them into user-friendly messages.
- Signed-in endpoints take the token as a parameter and set `token:`; the client adds the `Authorization` header.
- Paths and payloads mirror the .NET backend (`backend/README.md`). Change both in the same pull request.
- Problem responses become `APIError.problem` with `fieldErrors`; show them next to the matching field.
