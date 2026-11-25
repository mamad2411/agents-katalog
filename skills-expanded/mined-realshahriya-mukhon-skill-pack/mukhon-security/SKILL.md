---
name: mukhon-security
description: |
  Sovereign identity, anti-fraud, SafePay escrow, and financial ledger security standard for MUKHON.
  Enforces zero-trust invariants: HMAC-SHA256 NID blind indexing, scrypt password hashing, timing-safe
  comparisons, double-entry financial ledger balance, row-level locks on escrow deals, and OWASP hardening.
license: MIT
metadata:
  version: v1.0.0
  publisher: mukhon-core
---

# MUKHON Sovereign Security & Anti-Fraud Standard

This skill defines the mandatory security invariants and threat mitigation practices across the MUKHON platform.

---

## 1. Sovereign Identity & Zero Raw PII Invariants

1. **HMAC-SHA256 Blind Indexing:**
   - Plaintext National ID numbers (NID) and raw biometric data must **NEVER** be stored in public, unencrypted, or persistent database columns.
   - 1-Citizen-1-Account uniqueness is enforced solely via HMAC-SHA256 blind indexing (`nid_blind_index`) salted with server environment secret keys.
2. **Cryptographic Password Hashing:**
   - Passwords must be hashed using `scrypt` with a cryptographically secure random 16-byte salt (`salt:hash`).
   - All password and signature validations must use `crypto.timingSafeEqual` to eliminate timing side-channel attacks.
3. **Session & Auth Resiliency:**
   - In client context (`AppContext.tsx`), never invalidate user sessions on transient network blips or cold-start 5xx errors; session invalidation occurs exclusively on explicit `401 Unauthorized` responses.

---

## 2. SafePay Escrow & FinTech Ledger Invariants

1. **Double-Entry Bookkeeping:**
   - Every monetary movement must have balanced debit and credit entries.
   - Never update or alter a user's wallet balance directly without an immutable ledger entry.
2. **Row-Level Escrow Locking:**
   - Escrow operations must acquire strict row-level locks (`SELECT ... FOR UPDATE`) to prevent race conditions and double-spending during concurrent OTP verifications or courier webhooks.
3. **3-Attempt Brute Force OTP Limit:**
   - Handshake release OTPs are strictly rate-limited to 3 failed attempts. On the 3rd consecutive failed verification, the transaction immediately transitions to `DISPUTED` and locks pending administrator review.

---

## 3. Database & Network Security Invariants

1. **Environment-Driven Connections:**
   - Zero hardcoded database connection strings, credentials, or secrets in code files. All database access is strictly driven by `process.env.DATABASE_URL`.
2. **PostgreSQL Relational Safety & UUID Guards:**
   - In PostgreSQL queries, validate parameters before executing queries (`UUID_REGEX.test(id)`) to prevent syntax parsing exceptions on text handles.
3. **Row-Level Security (RLS):**
   - Public tables (`posts`, `comments`, `reactions`, `verified pages`) allow universal read access while strictly constraining mutations to verified content authors (`auth_uid() = author_id`).
   - Private tables (`messages`, `conversations`, `wallets`, `ledger_entries`, `p2p_escrows`) are restricted to verified participants or backend service role credentials.
