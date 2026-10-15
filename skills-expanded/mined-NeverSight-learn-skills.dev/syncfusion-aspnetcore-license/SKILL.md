---
name: syncfusion-aspnetcore-license
description: "**LICENSE REGISTRATION GUIDE** — Assist with Syncfusion ASP.NET Core EJ2 license key generation, registration, troubleshooting, and error resolution. Use when: registering license keys, handling licensing errors, upgrading from trial to paid, generating version-specific keys, or handling platform-specific licensing."
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Syncfusion ASP.NET Core — License Registration

Concise guidance for license generation and registration. Detailed troubleshooting steps, code examples, and environment recommendations live in the concern's references.

## When to Use
- Registering or updating Syncfusion license keys for ASP.NET Core
- Troubleshooting license validation, version, or platform mismatches
- Configuring license registration for build servers and CI/CD

## Quick Checklist
- Generate the license key for the exact Syncfusion version and platform
- Register the key early in `Program.cs` before initializing controls
- Ensure `Syncfusion.Licensing` NuGet package matches Syncfusion package versions
- Store keys securely (env var, Key Vault) and avoid committing to repo

## References
- License registration and troubleshooting: [references/references-license-registration.md](references/syncfusion-license-registration.md)
