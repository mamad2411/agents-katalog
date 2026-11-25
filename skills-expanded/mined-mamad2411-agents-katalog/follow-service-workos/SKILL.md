---
name: follow-service-workos
description: Use WorkOS for SSO, Directory Sync, and Authentication
argument-hint: "[scope]"
related:
  - follow-secret-manager
  - open-web-for-config-secret
  - follow-create-product
  - follow-lib-better-auth

---

## Goal

Configure and use WorkOS APIs for authentication and identity management

## Scope

Use in projects that need WorkOS SSO, SCIM, User Management, or Admin Portal

## Execute

### Workflows

> Goal: dispatch to the workflow matching the topic

- Setup: SDK install, `WORKOS_API_KEY`/`WORKOS_CLIENT_ID`, client init → `workflows/setup-workos/SKILL.md`
- Config: AuthKit/SSO, redirect URIs, organizations/connections, Directory Sync webhooks → `workflows/config-workos/SKILL.md`
- Verify: API key/client id valid, organizations reachable → `workflows/verify-connection/SKILL.md`

### 1. Install SDK

Prepare the SDK for WorkOS
> Goal: Install the SDK and prepare credentials to be ready

Latest: `@workos-inc/node@10.14.0` (verified 2026-09-24) — AuthKit/User Management API is the modern path, `sso.*` is the legacy flow

1. Install the package per runtime (`bun add @workos-inc/node`, `workos-python`, etc.)
2. Create an API key from the WorkOS Dashboard
3. Store `WORKOS_API_KEY` and `WORKOS_CLIENT_ID` in `/follow-secret-manager`, then inject them into the environment

### 2. Configure WorkOS

Configure WorkOS to be ready to use
> Goal: Set the environment, redirect URI, and organization

1. Set `WORKOS_API_KEY` and `WORKOS_CLIENT_ID`
2. Set the redirect URI and allowed origins
3. Create organizations and connections per provider (SAML, OIDC, Microsoft, Google)

### 3. Implement SSO

Use SSO with WorkOS APIs
> Goal: Create the authorization flow and manage the user session

1. Create the `authorization_url` with `workos.sso.getAuthorizationURL`
2. Receive the `code` callback and call `workos.sso.getProfileAndToken`
3. Create/update the user session
4. Validate `state` and `code_challenge` for PKCE

### 4. Directory Sync

Manage Directory Sync and webhook events
> Goal: Directory Sync

1. Create a directory for the connection
2. Set a webhook endpoint for events
3. Handle users/groups from the `dsync.*` APIs
4. Verify the webhook signature

## Rules

### 1. Security

- Do not hardcode the API key in code
- Store `WORKOS_API_KEY` in `/follow-secret-manager`
- Validate webhook signatures every time
- Handle state securely

### 2. Configuration

- Use environment-based config

- Use /open-web-for-config-secret if needed (service workos)
- Use /follow-create-product if needed
- Use /follow-lib-better-auth if needed


## Expected Outcome

- WorkOS SDK ready and configured correctly
- SSO/Dsync ready to use
- Credentials secure
- User data syncs correctly
