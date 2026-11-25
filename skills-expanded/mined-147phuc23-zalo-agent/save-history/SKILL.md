# Save History
Description: Save user, assistant, or tool interaction history in the in-memory DB-shaped store.

Use this skill whenever important user messages, assistant replies, or tool results should be auditable.

Input contract:
- `tenantId`: tenant id.
- `threadId`: Zalo thread id.
- `entries`: role/content/metadata records.

Output contract:
- Count of newly stored and total records for the thread.
