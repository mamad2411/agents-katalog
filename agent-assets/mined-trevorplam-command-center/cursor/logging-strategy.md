---
description: Run Logging Strategy and Audit Trail Verification
globs: ["src/utils/logger.ts", "src/lib/logger.ts", "**/*.ts", "**/*.tsx"]
---
# Observability: Logging Strategy

<audit_rules>
- You MUST enforce structured logging in JSON format (e.g., using Pino or Winston) across the application.
- You MUST ensure consistent fields are present in logs: `timestamp`, `level`, `message`, `userId`, and `requestId`.
- You MUST verify that sensitive data (passwords, tokens, credit card numbers) is NEVER logged.
- You MUST verify that PII (like email addresses) is hashed or truncated if logged.
- You MUST verify that critical audit events (login, logout, permission changes, data deletion) are explicitly logged.
</audit_rules>

<example_good>
```typescript
logger.info({
  event: 'USER_LOGIN',
  userId: user.id,
  requestId: req.headers.get('x-request-id'),
  message: 'User logged in successfully'
});
```
</example_good>

<example_bad>
```typescript
console.log(`User ${user.email} logged in with password ${password}`); // Leaks sensitive data
console.log("Something went wrong"); // Lacks structured format and context
```
</example_bad>

