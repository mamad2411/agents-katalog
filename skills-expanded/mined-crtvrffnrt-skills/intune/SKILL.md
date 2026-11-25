---
name: intune
description: Manage and inspect Microsoft Intune resources using Microsoft Graph and an Azure CLI service principal. Use for Intune policies, configuration profiles, devices, apps, assignments, and related administrative tasks.
---

# Intune with Azure CLI

Use this skill together or alongside with `pentest-gemini-az` for Azure CLI and Microsoft Graph operations. Follow the user's requested scope; a configured credential does not authorize unrelated changes.

## Authentication and context

Authenticate Azure CLI as the configured service principal using `$AZURE_CLIENT_ID` and `$AZURE_CLIENT_SECRET` from the environment.If they are not inherited, load them in the command shell without printing their values. Use tenant currently logged in via az cli for this configured application, unless the user explicitly specifies a different confirmed tenant. Never print, copy into artifacts, or commit the secret.  If credentials are absent, expired, or lack permissions, report the issue and the required permission; do not silently change consent or permissions.

Use `az login --service-principal` with the configured client ID and tenant, and `--allow-no-subscriptions` when needed. Supply the secret through Azure CLI's password prompt or another supported secure input mechanism, never as a command argument; do not enable tracing or expose credentials in output. Preserve existing CLI state and configuration as required by the runtime; use an isolated configuration directory only when permitted. Confirm the resulting tenant and service-principal identity before querying, and run subsequent `az rest` calls in that same authenticated context. Do not fall back silently to an interactive user account. Azure CLI login may briefly fail immediately after a newly created secret; retry only for a short propagation delay.
