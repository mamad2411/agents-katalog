# Claude Code Production System Directive
# Standard: secure-code

You are operating under the `secure-code` doctrine. Code generated must strictly comply with zero-trust security and extreme performance benchmarks.

## Critical Invariants:
1. **Never Concatenate Queries**: Parameterize all database access (SQL, NoSQL, ORM).
2. **Never Trust IDs From Clients**: Prevent IDOR by asserting ownership in query `WHERE` clauses using the authenticated session's tenant/user ID.
3. **No Timing Attacks**: Use constant-time comparison (`crypto.timingSafeEqual`, `hmac.compare_digest`) for hashes, tokens, and webhooks.
4. **No Float Money**: Use integer cents or arbitrary-precision `Decimal` with Banker's Rounding for all financial math.
5. **No Network in Transactions**: Never perform external HTTP requests inside active database transactions.
6. **No N+1 Queries**: Eagerly load relationships or batch queries with DataLoader/joins.
7. **SSRF Blocking**: Verify target IPs against RFC 1918 private ranges and AWS metadata (`169.254.169.254`) before making backend fetches.
8. **Security Headers**: Ensure web responses include CSP, HSTS, X-Content-Type-Options: nosniff, and frame deny.
