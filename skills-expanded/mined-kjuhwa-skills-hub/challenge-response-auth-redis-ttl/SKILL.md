---
tags: [backend, challenge, response, auth, redis, ttl]
name: challenge-response-auth-redis-ttl
description: Replay-resistant two-step login — server issues a short-lived random challenge stored in Redis with TTL, client signs/hashes response, bounded attempts per key
trigger: Login flow needs replay-resistant credential exchange without full TLS client-cert or OAuth2 overhead
category: backend
source_project: lucida-account
version: 1.0.0
---

# Challenge-response auth backed by Redis TTL

See `content.md`.
