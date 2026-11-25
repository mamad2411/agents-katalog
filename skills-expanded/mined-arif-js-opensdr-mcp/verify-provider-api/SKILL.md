---
name: verify-provider-api
description: Check a third-party provider's CURRENT official API docs (Apollo, Hunter, Exa, Tavily, Instantly, HubSpot, or a new one) before writing or changing a client, and record findings in docs/providers/<provider>.md. Use whenever an endpoint, auth scheme, rate limit, credit cost, or response shape is about to be coded.
---

# Verify a provider API

The endpoints in `.internal/plan.md` §9 are **expected**, not confirmed. Provider APIs change (Apollo moved auth to headers and introduced a separate People API Search, Hunter is on v2, Instantly deprecated v1). Coding from memory causes silent breakage.

## Steps
1. **Find official docs only.** Use your web search / fetch tools on the provider's own docs domain (e.g. `docs.apollo.io`, `hunter.io/api-documentation`, `docs.exa.ai`, `docs.tavily.com`, `developer.instantly.ai`, `developers.hubspot.com`). Ignore blog posts, SDK wrappers and Stack Overflow, except as hints to confirm against the official docs.
2. For **each endpoint** you will use, record:
   - Method + full URL
   - Auth (header name or param) and key type requirements (e.g. Apollo master key)
   - Request params you will send, with exact names and allowed enum values
   - Response fields you will read, with a trimmed sample
   - Pagination model and max page size
   - Rate limits and the headers that expose them
   - Credit or cost model (does this call consume credits? how many?)
   - Error body shape for 401/403/422/429
   - Idempotency (is it safe to retry?)
3. **Write `docs/providers/<provider>.md`** with this header:
   ```
   # <Provider> API notes
   Verified: YYYY-MM-DD by <agent/session> against <doc URLs>
   ```
   Then one section per endpoint, using the fields above. Add a **Discrepancies with .internal/plan.md** section if anything differs.
4. **If anything differs from .internal/plan.md §9 or a PRD**, update .internal/plan.md and the PRD in the same change, and tell the user.
5. **Fixtures**: when a key is available and the user approves a live call, capture real responses into `test/fixtures/<provider>/<endpoint>.json`. **Scrub** keys, real names, real emails, phone numbers and IDs: replace them with `.example` domains and fake names. If no key is available, build fixtures from the documented samples and mark them `"_source": "docs-sample"`.

## Rules
- Never put an API key into a file, command line history, or fixture.
- Never make a live call that consumes paid credits or creates resources without asking the user first.
- If the docs are ambiguous (e.g. whether an endpoint consumes credits), write "UNCONFIRMED" in the notes and make the code assume the costlier option.
