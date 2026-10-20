---
name: auth-patterns-pos
description: >
  Extends agent's knowledge of authentication and authorization patterns
  in Java POS applications. Use when implementing cashier login,
  session management, or role-based access control for POS terminals.
compatibility: Java 21+
metadata:
  domain: security
  level: intermediate
  stack: [java-21, slf4j-2]
  version: "1.0.0"
---

# Authentication Patterns for POS

POS terminals have multiple user types (cashier, manager, admin) with
different permissions. A cashier must not void transactions; a manager
must not change system settings. This skill covers BCrypt password
hashing, session tokens, and RBAC enforcement.

## Concepts

- **BCrypt** — adaptive hash function with configurable work factor;
  replaces MD5/SHA-256 for password storage.
- **Session tokens** — random 128-bit token generated at login; stored
  server-side with expiry; passed in-memory (never persisted to disk).
- **RBAC** — Role-Based Access Control: roles (`CASHIER`, `MANAGER`,
  `ADMIN`) mapped to granular permissions.
- **Pin pad fallback** — short numeric codes for quick cashier
  re-auth during shift.

## Rules

1. Hash passwords with `BCryptPasswordEncoder` (work factor ≥12);
   never store plain-text or reversible-encrypted passwords.
2. Invalidate session tokens after 30 minutes of inactivity or on
   explicit logout.
3. Enforce RBAC at the service layer, not just the UI layer — a
   crafted HTTP call must not bypass permission checks.
4. Rate-limit login attempts: max 5 failures per account per 15
   minutes.
5. Log every auth event (login, logout, failed attempt, role change)
   with user ID and terminal ID — never log passwords.

## Anti-patterns

See [anti-patterns.md](./anti-patterns.md).

## Related

- config-encryption — encrypting auth configuration
- secrets-management — protecting API keys and tokens
