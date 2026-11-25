---
name: 1password-sdks
description: Integrate 1Password directly into Python, Go, and JavaScript/TypeScript applications using the modern 1Password SDKs for secrets management.
---

# 1Password SDKs

This skill provides information on utilizing the modern 1Password SDKs for building applications that integrate directly with 1Password.

## Overview
1Password provides official, open-source SDKs designed for direct integration into your applications. These SDKs allow you to programmatically manage vaults and items, and natively load secrets into your application runtime.

## Supported Languages
- **Python**: [onepassword-sdk-python](https://github.com/1Password/onepassword-sdk-python)
- **Go**: [onepassword-sdk-go](https://github.com/1Password/onepassword-sdk-go)
- **JavaScript/TypeScript**: [onepassword-sdk-js](https://github.com/1Password/onepassword-sdk-js)

## Key Capabilities
- **Authentication**: Authenticate using the local desktop app (via biometrics) for local development or via Service Account tokens for production/CI environments.
- **Management**: Perform CRUD (Create, Read, Update, Delete) operations on vaults and items directly from code.
- **Environments**: Directly load secrets into your application environment.

## 1Password Connect SDKs vs Modern SDKs
- Use the **Modern SDKs** (listed above) for most new applications and workflows.
- Use the **1Password Connect SDKs** (e.g., `connect-sdk-python`) only if your architecture specifically requires a self-hosted private REST API bridge (1Password Connect Server) for isolated infrastructure environments.
