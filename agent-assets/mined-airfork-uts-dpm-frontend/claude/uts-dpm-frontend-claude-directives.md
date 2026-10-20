# Auth Directives

Validation and authorization directives for authentication.

## Files

| File                                  | What                                                 | When to read               |
| ------------------------------------- | ---------------------------------------------------- | -------------------------- |
| `passwords-equal.directive.ts`        | Validator ensuring password and confirm match        | Password form validation   |
| `passwords-not-equal.directive.ts`    | Validator ensuring new password differs from current | Password change validation |
| `remove-if-unauthorized.directive.ts` | Structural directive hiding elements by role         | Role-based UI visibility   |
