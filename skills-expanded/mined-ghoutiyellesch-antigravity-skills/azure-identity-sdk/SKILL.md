---
name: azure-identity-sdk
description: Consolidated Azure Identity SDK skill covering DefaultAzureCredential and authentication patterns across Dotnet, Java, Python, Rust, and TypeScript.
allowed-tools: Read Write Edit Glob Grep Bash WebSearch WebFetch
---

# Azure Identity SDK (Multi-Language)

This skill unifies authentication guidance for Azure services using the `azure-identity` package across multiple languages.

## Core Concepts

The `@azure/identity` (or equivalent) package is the standard way to authenticate Azure SDK clients. It abstracts away the complexity of handling tokens, service principals, and managed identities.

### DefaultAzureCredential

The cornerstone of the identity package is `DefaultAzureCredential`. It provides a simplified authentication experience by trying multiple authentication methods in order until one succeeds:

1. Environment variables (Client ID, Client Secret, Tenant ID)
2. Managed Identity (when running in Azure)
3. Developer tools (Azure CLI, VS Code, Azure PowerShell, Developer CLI)

**Always prefer `DefaultAzureCredential` over hardcoding keys or connection strings.**

## Language-Specific Package References

### Python
- **Install**: `pip install azure-identity`
- **Usage**: `from azure.identity import DefaultAzureCredential; credential = DefaultAzureCredential()`

### TypeScript / Node.js
- **Install**: `npm install @azure/identity`
- **Usage**: `import { DefaultAzureCredential } from "@azure/identity"; const credential = new DefaultAzureCredential();`

### Java
- **Install**: `com.azure:azure-identity`
- **Usage**: `TokenCredential credential = new DefaultAzureCredentialBuilder().build();`

### .NET (C#)
- **Install**: `Azure.Identity`
- **Usage**: `var credential = new DefaultAzureCredential();`

### Rust
- **Install**: `azure_identity`
- **Usage**: `let credential = azure_identity::DefaultAzureCredential::default();`
