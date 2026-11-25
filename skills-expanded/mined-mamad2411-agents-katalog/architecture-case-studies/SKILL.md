---
name: architecture-case-studies
description: >
  Learn from real systems and classic design problems. Use when studying how
  companies scaled (Netflix, Uber, Twitter, Airbnb, Discord, Reddit, Figma,
  Meta, TikTok, Pinterest), designing classic systems (URL shortener, chat,
  feed, notifications, search, maps, Google Docs, stock exchange, S3, Gmail,
  proximity service), or looking for proven patterns. Triggers: "how does X
  scale", "design WhatsApp/Discord/Google Docs", "case study", "real-world
  architecture".
---

# Architecture Case Studies

Real systems are the best teachers. Study the why, not just the what.

## When to use
- Looking for a proven approach to a hard problem.
- Preparing system design examples for interviews.
- Learning how companies evolved their architecture.
- Designing a known class of system (chat, feed, storage...).

## How to read a case study
For each, extract: **constraints → initial design → bottleneck → evolution →
tradeoff accepted**. Do not copy topologies; copy reasoning. The same company
changed its architecture several times as scale and requirements changed.

## Real-world evolution themes
| Company | Lesson |
|---|---|
| Netflix | Microservices maturity, DB polyglot, push at scale, CI/CD |
| Uber | API layer evolution, real-time geospatial scale |
| Twitter | Architecture over a decade; feed recommendation |
| Airbnb | Monolith → microservices evolution |
| Discord | Message storage rewrite as data grew (trillions) |
| Reddit | Serving millions with pragmatic architecture |
| Figma | Postgres sharding/scaling 100x |
| Meta | Automated bug fixing at scale |
| TikTok | Huge frontend monorepo management |
| Pinterest | Small change, huge win (clone times) |
| Shopify | Resilient payment systems |

## Classic design problems
- URL shortener, rate limiter, unique ID generator, chat/collaboration,
  news feed, notifications/push, search, Google Docs, Google Maps,
  stock exchange, S3 upload, Gmail, proximity service.
- Pattern per problem: requirements → API → data model → scale → bottlenecks.

## Common architectural moves seen repeatedly
- Cache aggressively on read paths.
- Async + queue for spiky/slow work.
- Shard when single-node limits hit; consistent hashing for balance.
- Denormalize/materialize read models.
- Push vs pull for notifications; fan-out on write vs read for feeds.
- Move to object storage for large blobs.

## Checklist
- [ ] Constraints of the original system understood.
- [ ] Bottleneck → solution mapping extracted.
- [ ] Tradeoffs of each evolution named.
- [ ] Patterns adaptable (not blindly copied) to current problem.

## Common pitfalls
- Copying FAANG topology for a 100-user app.
- Ignoring that the case study solved a different constraint set.
- Reading only the final architecture, missing the journey.
- Over-engineering toward imagined scale.

## References — real world
- `...\netflixs-overall-architecture.md`, `...\netflixs-tech-stack.md`, `...\netflix-tech-stack-databases.md`, `...\netflix-tech-stack-cicd-pipeline.md`, `...\evolution-of-the-netflix-api-architecture.md`, `...\how-does-netflix-scale-push-messaging-for-millions-of-devices.md`, `...\how-netflix-really-uses-java.md`, `...\4-ways-netflix-uses-caching-to-hold-user-attention.md`
- `...\uber-tech-stack.md`, `...\evolution-of-uber's-api-layer.md`, `...\uber-tech-stack-cicd.md`
- `...\twitter-10-tech-stack.md`, `...\twitter-architecture-2022-vs-2012.md`, `...\how-does-twitter-recommend-tweets.md`
- `...\airbnb-artchitectural-evolution.md`, `...\evolution-of-airbnb's-microservice.md`
- `...\how-discord-stores-trillions-of-messages.md`, `...\reddit's-core-architecture.md`
- `...\100x-postgres-scaling-at-figma.md`, `...\fixing-bugs-automatically-at-meta-scale.md`, `...\how-tiktok-manages-a-200k-file-frontend-monorepo.md`, `...\the-one-line-change-that-reduced-clone-times-by-a-whopping-99-says-pinterest.md`
- `...\how-does-youtube-handle-massive-video-content-upload.md`, `...\what-is-the-journey-of-a-slack-message.md`, `...\how-does-a-typical-push-notification-system-work.md`
- `...\mcdonald's-event-driven-architecture.md`, `...\api-of-apis-app-integrations.md`, `...\is-telegram-secure.md`

## References — classic designs
- `...\how-will-you-design-the-stack-overflow-website.md`, `...\how-do-we-design-a-chat-application-like-whatsapp-facebook-messenger-or-discord.md`, `...\build-a-simple-chat-application.md`
- `...\design-gmail.md`, `...\how-to-design-google-docs.md`, `...\design-google-maps.md`, `...\design-stock-exchange.md`
- `...\proximity-service.md`, `...\quadtree.md`, `...\unique-id-generator.md`
- `...\how-do-search-engines-work.md`, `...\how-do-we-design-a-system-for-internationalization.md`, `...\possible-experiment-platform-architecture.md`
- `...\live-streaming-explained.md`, `...\how-is-email-delivered.md`, `...\what-happens-when-you-upload-a-file-to-amazon-s3.md`
- `...\how-do-airtags-work.md`, `...\how-are-notifications-pushed-to-our-phones-or-pcs.md`
Base: `D:\Agent-Assets\system-design-101\data\guides\`

## Related skills
`system-design-method`, `system-design-interviews`, `scalability-and-performance`,
`database-design`.
