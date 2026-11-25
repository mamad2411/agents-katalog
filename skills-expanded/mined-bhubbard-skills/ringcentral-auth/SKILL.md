---
name: ringcentral-auth
description: "Authentication with the RingCentral API using JWT and OAuth 2.0"
---

# RingCentral Authentication Skill

This skill provides guidelines and best practices for authenticating with the RingCentral API using JWT (JSON Web Tokens) and OAuth 2.0.

## Overview
RingCentral supports robust authentication mechanisms to secure API access. The recommended approach for server-to-server or backend applications is JWT auth, while user-facing applications should use the standard 3-legged OAuth 2.0 flow (Authorization Code Flow).

## JWT Authentication (Server-to-Server)
1. **Prerequisites**: Ensure the application is created in the RingCentral Developer Console and JWT is enabled.
2. **Generating a JWT**: Generate a personal JWT token from the developer console for the specific user/extension.
3. **Exchanging JWT for Access Token**:
   Use the `/restapi/oauth/token` endpoint.
   - `grant_type`: `urn:ietf:params:oauth:grant-type:jwt-bearer`
   - `assertion`: `<your_jwt_token>`
   - `client_id` & `client_secret` (passed via Basic Auth header or body depending on setup).

## OAuth 2.0 (User-Facing Apps)
1. **Authorization Request**: Redirect users to `https://platform.ringcentral.com/restapi/oauth/authorize` with `response_type=code`, `client_id`, and `redirect_uri`.
2. **Token Exchange**: Upon user approval, the app receives an authorization code. Exchange it at `/restapi/oauth/token` with `grant_type=authorization_code`.
3. **Token Refresh**: Use the `refresh_token` grant type to obtain new access tokens when they expire.

## Best Practices
- Always store `client_secret` and JWT tokens securely (e.g., environment variables, secret managers).
- Handle token expiration gracefully by utilizing refresh tokens.
- Use the official RingCentral SDKs when possible, as they handle token lifecycle and refreshing automatically.
