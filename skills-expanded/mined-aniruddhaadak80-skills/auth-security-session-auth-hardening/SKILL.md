---
name: auth-security-session-auth-hardening
description: "Cookies, rotation, and revocation done right for server-rendered apps."
---
# Harden session authentication

> Cookies, rotation, and revocation done right for server-rendered apps.

**Track:** ⚙️ Backend Engineering · **Domain:** Auth & Security Basics · **Level:** intermediate · **~35 min**

**Who this is for:** Backend Engineers, API Developers, Platform Engineers, Full-Stack Developers

## When to Use This Skill

Cookies, rotation, and revocation done right for server-rendered apps.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. Store session ID in HttpOnly, Secure, SameSite=Lax cookies
2. Rotate session IDs on login and privilege change
3. Keep server-side session records enabling instant revocation
4. Expire idle sessions; re-authenticate before sensitive actions
5. Rate-limit login and reset endpoints per IP and per account
6. Log auth events to an append-only trail with device metadata

## Common Pitfalls

- JWTs in localStorage inviting XSS token theft
- No server-side revocation after 'logout everywhere' requests

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill auth-security-session-auth-hardening
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill auth-security-session-auth-hardening -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills