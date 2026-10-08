# LifeCast X Fetcher

## Purpose
Read the authenticated user's X activity through XActions and hand sanitized records to the local LifeCast ingestion pipeline.

## Scope
- fetch self-authored posts, likes, and mentions only
- enforce a minimum 30-minute fetch interval
- treat XActions as the primary provider and Official API as fallback
- pass summaries and source identifiers to local storage only

## Must
- run XActions through Docker isolation
- keep session cookies and OAuth tokens outside the repository
- preserve read-only behavior at all times
- stop before any operation that would write to X

## Must Not
- post, like, repost, follow, or delete on X
- fetch other users' private data
- send raw scraped data to external services
- bypass the self-rate limit
