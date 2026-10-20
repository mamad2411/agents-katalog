# Cline Rules: SurrealDB MCP Server Project

## Core Problem-Solving Strategy

**HARD RULE:** When stuck or repeating failed attempts on the same problem:
1.  **STOP:** Do not immediately retry the same failed approach.
2.  **THINK & ANALYZE:** Review the steps taken, the errors encountered, and the available information (Memory Bank, code, error messages). Identify the core assumptions and why they might be wrong.
3.  **RESEARCH:** Actively seek external information. Prioritize web searches (using tools like Brave Search) for specific error messages, library documentation, GitHub issues, Stack Overflow discussions, or examples related to the problem domain.
4.  **RE-PLAN:** Formulate a *new* approach based on the analysis and research before attempting further action.

## Key Learnings & Patterns

1.  **SurrealDB SDK Package:** Use the `surrealdb` npm package, not the deprecated `surrealdb.js`.
2.  **Connection & Authentication (Root):** The most reliable method found for connecting as root to a specific namespace/database with the `surrealdb` (v1.x+) SDK is to provide all details within the `connect` method's options:
    ```javascript
    await db.connect(DB_ENDPOINT, {
      namespace: 'YOUR_NAMESPACE', // e.g., 'n8n'
      database: 'YOUR_DATABASE',   // e.g., 'AIWorld'
      auth: {
        username: 'YOUR_ROOT_USER', // e.g., 'root'
        password: 'YOUR_ROOT_PASS', // e.g., 'root'
      },
    });
    ```
    *   This avoids potential context issues encountered with separate `db.use()` and `db.signin()` calls after connecting.
    *   The `auth` object requires `username` and `password` keys, based on SDK error messages, even if some documentation examples use `user`/`pass`.
3.  **Namespace/Database Existence:** Ensure the target namespace and database exist *before* attempting to connect using the method above. While the script *could* define them using root privileges, it's cleaner if they are pre-existing for standard operations. (User confirmed `n8n`/`AIWorld` exist).
4.  **`db.select()` / `db.update()` / `db.delete()` Specific Record ID:** To select, update, or delete a *specific* record using the corresponding SDK methods (`db.select()`, `db.update()`, `db.delete()`), you **must** pass an instance of the SDK's `RecordId` class (e.g., `new RecordId('table', 'idPart')`) as the first argument. Passing the full `table:id` string, although documented in some examples and valid in SurrealQL, resulted in unexpected behavior (`[]` return or failure) when used directly with these SDK methods in v1.3.1. `db.query()` works reliably with the string format for selection. (Lesson: Verify SDK method behavior against documentation and type definitions, especially when targeting specific records. SDK methods might have stricter type requirements than implied by general SurrealQL syntax or documentation examples).
5.  **SDK Source Code:** The non-minified source for the `surrealdb` Node.js SDK can be found at: https://github.com/surrealdb/surrealdb.js/ (Useful for deeper investigation when documentation or basic research is insufficient).
6.  **Handling Not Found Results:** When using `db.select()` or `db.delete()` for a specific `RecordId`, the result might be `undefined` or an empty array if the record doesn't exist. The MCP tool handler must check for this and return a valid string representation (e.g., `"[]"` or `"Record not found"`) to avoid client-side validation errors (like Zod errors expecting a string).
