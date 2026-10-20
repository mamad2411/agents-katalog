# AGENTS.md

## Scope
Configuration and secret management for the iOS target. Applies to `RefWatchiOS/Config/`.

## Conventions
- Do not commit real secrets. Use `Secrets.example.xcconfig` as the template and keep `Secrets.xcconfig` local.
- Reference keys from code via build settings or a local `Secrets.swift` living in platform adapter modules (e.g., `Core/Platform/AI`), but keep OpenAI credentials on the server-side assistant proxy instead of the iOS config layer.
- Keep names consistent so agents can wire them automatically.

## Setup
1) Duplicate `Secrets.example.xcconfig` → `Secrets.xcconfig` and fill in local values.
2) Ensure the iOS target inputs this file via the project’s build settings.
