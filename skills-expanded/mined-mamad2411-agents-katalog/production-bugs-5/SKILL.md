---
name: production-bugs-5
description: Five bugs that pass in the tutorial and fail in production - race conditions, authorization bugs, N+1 queries, memory leaks and missing idempotency - each with the problem, what to do and the question to ask, plus a review checklist. Use when reviewing backend or API code, preparing a feature for real traffic, or debugging an incident that "worked in testing". Source @jek.notes 7-slide carousel "10 Developer Problems You Won't See Until Production" (Batch 103). The title promises 10; the carousel shows 5 problems plus an intro and a closing slide (7 slides in all).
---

# 5 bugs you will not see until production

Slide order in the source: 01 race conditions, 02 authorization bugs, 03 N+1 queries, 04 memory leaks, 05 idempotency; framing slides before and after. The cover says "10 developer problems"; only five are in the set (the other five are not in the upload).

| # | Bug | The problem | What to do | The question to ask |
|---|---|---|---|---|
| 1 | Race conditions | Two requests arrive almost at the same time, both read `stock = 1`, both think they can buy it, now `stock = -1`. The code was correct when requests ran one at a time. | Protect the critical operation with the right mechanism: transactions, atomic operations, locks, unique constraints | What if these two operations happen at the same time? |
| 2 | Authorization bugs | Logged in does not mean allowed. Authentication answers "who are you?"; authorization answers "what are you allowed to do?". Example: User A calls `GET /api/orders/482`, order 482 belongs to User B, the API returns `200 OK`. | Check ownership, roles, permissions, resource-level access, server-side enforcement | Can this user perform this action on this resource? |
| 3 | N+1 queries | You fetch a list of users, then run another query inside the loop for each user's posts. 100 users make 101 queries. Fine with 10 records locally; with 10,000 in production the database is the bottleneck. | Fetch related data intentionally: joins, eager loading, batching | Count your database calls, not just your lines of code |
| 4 | Memory leaks | A component, event listener, timer, subscription or resource keeps living after it should have been cleaned up. Memory climbs (100 MB, 180, 290, 470) until the process is out of memory. | Look for uncleared timers, event listeners, subscriptions, retained references, long-lived caches. Create, use, clean up. Test what happens after a feature runs 100 times, not only whether it works | What is STILL ALIVE after this component disappears? |
| 5 | Idempotency | Networks fail, users retry, clients time out, requests get duplicated. A payment request times out, the client retries, and the customer is charged twice (the slide's example: 10,000 + 10,000 = 20,000). | Make retrying the same operation safe: idempotency keys, unique request identifiers, database constraints, carefully designed retry logic | Design for the request you will receive TWICE |

Closing slide, "Code that works is only the beginning": production adds concurrency, permissions, scale, failures and everything the tutorial did not. Build it, break it, understand why. It asks which of race conditions, authorization bugs, N+1 queries, memory leaks and idempotency you have actually debugged.

## Review checklist
For each endpoint or job under review, answer: (1) Can two concurrent calls corrupt a counter, balance or stock? (2) Does every read and write check that the caller owns the resource, server-side? (3) How many queries for 1 row, 100 rows, 10,000 rows? (4) What is created per request or per mount that is never released? (5) What happens when the same request arrives twice? Run `/prod-bug-check <file or feature>`.

Related, already installed: `security-review`, `code-review`, `error-handling-patterns`, `python-resilience`, `postgres-patterns`.
