---
name: android-rest-api
description: Use when adding or changing a backend REST call in the Android app (AgenticApp), including fixtures for tests.
---

# Android REST API layer

## Adding an endpoint

1. Define the response model as a `@Serializable data class`.
2. Add it to `Endpoints` in `core/network/Endpoint.kt`:
   `fun orders(token: String) = Endpoint("/api/orders", ListSerializer(Order.serializer()), token = token)`
3. Call it from a repository in `core/services`, never from a screen or view model:
   `apiClient.send(Endpoints.orders(token))`
4. Add a fixture in `app/src/main/assets/fixtures/`: the path without `/api/`, slashes as dashes (`/api/auth/signin` → `auth-signin.json`). Use the same file as the iOS app. Endpoints returning `Unit.serializer()` need no fixture.
5. Unit test the repository with `FakeApiClient`, and request building with the interceptor-based OkHttp client in `ApiClientTest`.

## Rules

- Base URL comes from the flavor (`src/<flavor>/kotlin/.../FlavorConfig.kt`). Never hard-code URLs.
- Errors surface as `ApiError`; view models turn them into user-friendly messages with `userMessage`.
- Signed-in endpoints take the token as a parameter and set `token =`; the client adds the `Authorization` header.
- Paths and payloads mirror the .NET backend (`backend/README.md`). Change both in the same pull request.
- Problem responses become `ApiError.Problem` with `fieldErrors`; show them next to the matching field.
- Network work runs on `Dispatchers.IO` inside `OkHttpApiClient`; view models just call `suspend` functions.
