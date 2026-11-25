# Worker instructions

These rules apply under `apps/worker/` in addition to the repository instructions.

- Keep Celery entrypoints thin; call shared application use cases.
- Jobs must be idempotent. Retrying identical input and configuration must not duplicate domain results.
- Define retry, timeout, partial-failure, and unavailable-dependency behavior explicitly.
- Preserve processing-run identity, provider/model version, source references, confidence, and coordinate transformations.
- Do not log source documents, extracted content, credentials, tokens, or signed URLs.
- New worker capabilities must work through Docker Compose.

During implementation, run the affected worker and backend tests first with quiet pytest output. Run integration or Compose checks only when the changed boundary requires real Redis, storage, database, or provider behavior.
