---
name: sinking-ship
description: "Pre-production checklist: verify security, database, deployment, and code readiness before shipping."
disable-model-invocation: true
---

Run the **SINKING SHIP checklist** against the current codebase/project. This is a pre-production audit. Verify each item yourself by reading code, config, and infra; don't take anyone's word for it.

For each item: mark `[x] PASS`, `[ ] FAIL`, or `[?] UNKNOWN` and cite the file:line or config proving it.

## SECURITY

- [ ] No API keys or secrets in frontend code
  - Grep the frontend bundle output and source for patterns: `sk-`, `api_key=`, `password=`, `secret=`, `token=`, AWS keys, private keys
- [ ] Every route checks authentication (audit ALL endpoints, not just the obvious ones)
  - List every route/handler and confirm auth middleware applies. Flag any public-by-default routers.
- [ ] HTTPS enforced everywhere, HTTP redirected
  - Check load balancer / reverse proxy config; confirm HSTS header; confirm 301 from http → https
- [ ] CORS locked to your domain, not wildcard
  - Find CORS config; flag any `*` or overly permissive origins
- [ ] Input validated and sanitized server-side
  - Schema validation (Pydantic, Zod, etc.) on every endpoint accepting input
- [ ] Rate limiting on auth and sensitive endpoints
  - Check for rate limiter middleware on login, signup, password reset, API tokens
- [ ] Passwords hashed with bcrypt or argon2
  - Confirm hashing algorithm; flag MD5, SHA1, SHA256-without-salt, or plaintext
- [ ] Auth tokens have expiry
  - JWT exp claim set; session TTL configured
- [ ] Sessions invalidated on logout (server-side)
  - Logout actually clears server state, not just the client cookie

## DATABASE

- [ ] Backups configured and tested (test RESTORE, not just backup)
  - Confirm backup schedule AND last successful restore test
- [ ] Parameterized queries everywhere, no string concatenation
  - Grep for string-built SQL, f-string SQL, `+` concatenation in query construction
- [ ] Separate dev and production databases
  - Confirm distinct connection strings per environment; no shared prod DB
- [ ] Connection pooling configured
  - Pool size set; no per-request connection creation on hot paths
- [ ] Migrations in version control, not manual changes
  - Migration tool in use (Alembic, Prisma, Flyway, etc.); no record of manual DDL
- [ ] App uses a non-root DB user
  - Check DB grants; confirm principle of least privilege

## DEPLOYMENT

- [ ] All environment variables set on the production server
  - Compare `.env.example` to production env; flag anything missing
- [ ] SSL certificate installed and valid
  - Confirm cert chain, expiry >30 days out, auto-renewal working
- [ ] Firewall configured (only 80/443 public)
  - Check security groups / firewall rules; flag exposed DB, SSH-from-anywhere, admin panels
- [ ] Process manager running (PM2, systemd, Docker restart policy)
  - Confirm auto-restart on crash and on reboot
- [ ] Rollback plan exists
  - Documented procedure; confirmed rollback works (ideally tested)
- [ ] Staging test passed before production deploy
  - CI/CD has a staging gate; last staging run green

## CODE

- [ ] No console.logs in production build
  - Check build config for log stripping; grep compiled output
- [ ] Error handling on all async operations
  - Grep for unhandled promises, missing `try/except` around `await`, unhandled rejections
- [ ] Loading and error states in UI
  - Every data-fetching component has a loading state and an error state
- [ ] Pagination on all list endpoints
  - Flag any endpoint returning an unbounded collection
- [ ] npm audit run, critical issues resolved
  - Run `npm audit` / `pip audit` / equivalent and report output

## Output format

For each section, produce a table:

```
Item | Status | Evidence
```

End with:
- **Total:** X passed, Y failed, Z unknown
- **Ship verdict:** ready / not ready / ready with caveats
- **Blocking issues:** the FAIL items that must be fixed before ship

## Rule

If any critical SECURITY or DATABASE item fails, the verdict is **not ready** regardless of other scores.

---

Target: $ARGUMENTS

If no target specified, audit the codebase rooted at the current working directory.
