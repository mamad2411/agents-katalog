---
description: Run Documentation and Configuration Consistency Audit
globs: ["**/*.md", "**/*.config.*", "**/*rc*", "**/.env*", "**/Dockerfile"]
---
# Code Quality: Documentation & Configuration Consistency

<audit_rules>
- You MUST verify that comments above functions/classes are accurate and do NOT reference non-existent parameters.
- You MUST flag any TODO comments older than 3 months or empty boilerplate comments (e.g., "Constructor for User class").
- You MUST verify configuration consistency (e.g., no duplicate config files like `.prettierrc` and `prettier.config.js`).
- You MUST ensure environment variable references in the code match the `.env.example` file.
- You MUST check that the `README.md` accurately reflects the project's current state, including technology claims, directory structures, and setup instructions.
</audit_rules>

<example_good>
```typescript
/**
 * Fetches user data by ID.
 * @param {string} id - The unique identifier of the user.
 * @returns {Promise<User>} The user object.
 */
async function getUser(id: string): Promise<User> {
  // implementation
}
```
</example_good>

<example_bad>
```typescript
/**
 * Fetches user data.
 * @param {string} userId - The unique identifier of the user. // BAD: parameter name mismatch
 * @param {boolean} includePosts - Whether to include user's posts. // BAD: parameter doesn't exist
 */
async function getUser(id: string): Promise<User> {
  // implementation
}
```
</example_bad>

