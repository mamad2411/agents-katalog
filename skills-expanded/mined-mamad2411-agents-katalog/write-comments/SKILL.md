---
name: write-comments
description: Apply codebase commenting conventions for TypeScript, Python, and any language. USE WHEN writing or reviewing comments, adding section comments, organizing code into logical groups, or asked about comment style. Covers when to comment, how to write good comments, section comment format (emoji + capitalized name), emoji reference table, and anti-patterns to avoid (obvious comments, redundant JSDoc, TODO lint bypasses, dash-line dividers).
license: MIT
---

# Commenting

## When to Comment

Code should be self-explanatory through good naming. Comments add value only when they explain **why** something is done — not **what** it does.

**Comment when:**

- Explaining non-obvious intent or business logic
- Documenting known edge cases or external constraints
- Noting a workaround with a link to the upstream issue

**Don't comment when:**

- The code is clear from reading it
- You're narrating what the code obviously does

## How to Comment

### Good Comments

```typescript
// Delay is intentional: the third-party API enforces a 1s rate limit per key
await delay(1000);

// Uses linear search because this list is always < 10 items and never hot
const found = items.find((item) => item.id === targetId);
```

### Bad Comments

```typescript
// Increment counter
counter++;

// Call the API
const result = await fetchData();

// Return the value
return value;
```

## Anti-Patterns

### Obvious Comments

```typescript
// Bad: restates what the code already says
const user = getUser(id); // Get the user by id
```

### Redundant JSDoc

Avoid JSDoc on private functions or functions whose signature is self-documenting.

```typescript
// Bad: JSDoc that adds nothing
/**
 * Gets the user.
 * @param id - The user id.
 * @returns The user.
 */
function getUser(id: string): User { ... }

// Good: JSDoc only when it adds non-obvious context
/**
 * Returns the user record, or throws `UserNotFoundError` if the id is
 * not present in the active-users projection. Does NOT check the archive.
 */
function getUser(id: string): User { ... }
```

### TODO Comments

Don't leave TODO comments to bypass lint rules or defer real fixes.

```typescript
// Bad: silences a rule without explanation
// eslint-disable-next-line @typescript-eslint/no-explicit-any
function process(data: any) { ... }

// Good: fix the underlying issue instead
function process(data: unknown) { ... }
```

If a TODO is genuinely needed (tracked work), include a ticket reference:

```typescript
// TODO(#1234): remove once the upstream API supports batch deletes
```

### Divider Comments

```typescript
// Bad: dash dividers
// ---------------------------------------------------------------------------
// Configuration
// ---------------------------------------------------------------------------

// Bad: equals dividers
// ===========================
// Configuration
// ===========================

// Bad: plain section label with no emoji
// Configuration

// Bad: #region blocks
//#region 🔧 Configuration
//#endregion
```

Use emoji section comments instead — see [Section Comments](#section-comments) below.

## Section Comments

When a file benefits from logical groupings, mark each section with a single-line emoji comment.

### Format

```text
// <emoji> <Section name>
```

- **Emoji first** — conveys purpose at a glance
- **Capital first letter** — `// 🔧 Configuration`, not `// 🔧 configuration`
- **Single line** — no closing marker, no surrounding dash lines
- **Python** uses `#` instead of `//` — same rules otherwise

### Examples

#### TypeScript / JavaScript

```typescript
// 🔧 Configuration

const MAX_RETRIES = 3;
const API_TIMEOUT = 5_000;

// 🎭 Mocks

vi.mock("./api.js");

// 🧪 Tests

describe("MyService", () => { ... });
```

#### NestJS service layout

```typescript
@Injectable()
export class MyService {
  // 🏗 Dependency injection
  constructor(private readonly logger: LoggerService) {}

  // 🔐 Private fields

  // 🔑 Public fields

  // 🔏 Private methods

  // 🌎 Public methods
}
```

#### Python

```python
# 🔧 Configuration

MAX_RETRIES = 3

# 🧪 Tests

class TestMyService(unittest.TestCase): ...
```

### Emoji Reference

| Emoji | Typical use |
| ----- | ----------- |
| 🏗 | Dependency injection, constructors |
| 🔧 | Configuration, constants |
| 🗄️ | Types, data structures |
| 🏷️ | Type aliases, interfaces |
| ♟️ | Constants module |
| 🔐 | Private fields |
| 🔑 | Public fields |
| 🔏 | Private methods |
| 🌎 | Public methods |
| 🎭 | Mocks |
| 🧪 | Tests |
| 🔗 | Relations, associations, links |
| 🔎 | Queries |
| 🖋️ | Mutations |
| 📋 | Headings, lists |
| 📦 | Code blocks, packages |
| 📝 | Paragraphs, docs |
| 🖼️ | Images |
| ✏️ | Inline formatting |
| ✅ | Completed / passing |
| ➖ | Thematic breaks |
| 💬 | Blockquotes |
| 📊 | Tables |
| 📚 | Grammar groups, large topic areas |

### Rules Summary

1. Format: `// <emoji> <Section name>` (TypeScript/JS) or `# <emoji> <Section name>` (Python)
2. Section name: capitalized first letter, short noun phrase
3. Never wrap a section comment in dash lines or any other delimiter
4. Never use `#region`/`#endregion` — plain emoji comments are sufficient
5. Choose an emoji that conveys the section's purpose; consult the table above
