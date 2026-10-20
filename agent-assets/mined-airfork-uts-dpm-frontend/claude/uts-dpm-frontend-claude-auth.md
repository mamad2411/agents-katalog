# Authentication Module

Handles login, password management, route guards, and HTTP interceptors.

## Files

| File                  | What                                                | When to read                                  |
| --------------------- | --------------------------------------------------- | --------------------------------------------- |
| `auth.guard.ts`       | Route guard for protected routes, role-based access | Adding protected routes, fixing access issues |
| `auth.interceptor.ts` | HTTP interceptor for JWT tokens, 401/403 handling   | Auth header issues, token refresh             |
| `auth.routes.ts`      | Auth module routing configuration                   | Adding auth routes                            |
| `roles.types.ts`      | User role type definitions                          | Understanding role hierarchy                  |

## Directories

| Directory          | What                                                         | When to read                           |
| ------------------ | ------------------------------------------------------------ | -------------------------------------- |
| `auth/`            | Auth wrapper component                                       | Auth layout structure                  |
| `login/`           | Login form component                                         | Login flow, credentials handling       |
| `change-password/` | Password change form                                         | Password update functionality          |
| `directives/`      | Auth-related directives (password validation, authorization) | Form validation, conditional rendering |
