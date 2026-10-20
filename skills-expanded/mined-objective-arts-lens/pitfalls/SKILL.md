---
name: pitfalls
description: "Known bug patterns and code traps accumulated from production reviews"
allowed-tools: []
---

# Pitfalls: Patterns That Go Wrong

Cross-project patterns accumulated from thousands of code reviews. These are the bugs, security holes, and anti-patterns that recur across codebases regardless of language or framework.

**Use this canon proactively.** Check each pattern against your code before committing.

---

## Logic Traps

### TOCTOU (Time-of-Check-to-Time-of-Use)
- Never pair `existsSync` + `readFileSync` — the file can be deleted between the two calls. Use try-catch around `readFileSync` directly.
- This is the single most common bug pattern across codebases.

### Shell Injection
- NEVER use `execSync` with template literals containing variables: `` execSync(`grep "${pattern}" "${path}"`) ``
- Always use `execFileSync` with an args array: `execFileSync('grep', ['-rn', pattern, path])`
- `shell: false` (default for `execFile`/`spawn`) prevents injection even with untrusted content

### Path Traversal
- Any name from user input (CLI args, config files, regex-parsed content) must be validated before `path.join`: reject `/`, `\`, `..`
- Validate at the boundary where user input enters — not deep in library functions
- Pattern: `if (name.includes('/') || name.includes('\\') || name.includes('..'))` → reject

### Path Prefix Collision
- `path.startsWith(root)` without trailing separator matches too broadly: `/home/user` matches `/home/username`
- Always use `startsWith(root + path.sep)` or `startsWith(root + '/')` for path containment checks

### Symlink Bypass in Path Validation
- `startsWith` checks on resolved paths are bypassed by symlinks pointing outside the allowed directory
- Always resolve with `realpath` AND then verify with `path.relative()` that the result doesn't start with `..`
- Pattern: `const rel = path.relative(allowed, await realpath(target)); if (rel.startsWith('..')) reject;`

### Secrets in CLI Arguments
- Never accept secrets (API keys, passwords, tokens) as positional CLI arguments — they leak to `ps aux` and shell history
- Accept secrets via `--value-file <path>`, stdin pipe, env var, or interactive prompt

### XSS in Embedded JSON
- `JSON.stringify` inside `<script type="application/json">` is vulnerable if data contains `</script>`
- Always escape: `.replace(/<\//g, '<\\/')`

### Sorting Inside Nested Loops
- Never sort an array inside a loop that iterates over it repeatedly — sort once before the loop, then scan linearly
- Fix: pre-sort once into a parallel structure, then use linear scan or binary search inside the loop

### Null-as-Sentinel in Aggregation
- When aggregating records where null means "ongoing/open-ended", a naive reduce can overwrite null with a later non-null value
- Use a boolean flag (`hasOngoing`) to track whether any record had the sentinel, then apply it after the loop

### Unbounded While Loop on Date Ranges
- Any `while (current <= latest)` loop iterating over dates must guard against `earliest > latest` at the top of the function
- Without the guard, malformed or inverted date ranges cause infinite loops and CPU exhaustion
- Pattern: `if (!earliest || !latest || earliest > latest) return [];`

### Bracket-Access Without Fallback on Lookup Objects
- `COLORS[key]` returns `undefined` when key is missing, which silently produces broken DOM attributes (e.g., `fill="undefined"`)
- Wrap lookups in a helper with nullish coalescing: `COLORS[key] ?? FALLBACK_COLOR`

### String-Matching Fragility
- Don't match against human-readable strings to detect state: `result.message.includes('already installed')`
- Check actual filesystem/application state directly instead

### Falsy-vs-Null on Optional Numeric Values
- `if (d.target)` treats 0 as falsy, skipping valid zero values
- Use `d.target !== null && d.target !== undefined` (or `d.target != null`)
- Applies to any optional number where 0 is a meaningful value

### Async Mutation Rollback Scope
- When mutating shared state across multiple async steps, wrap the entire sequence in a single try/catch with rollback
- Partial rollback (only on one failure point) leaves state inconsistent when later steps fail

### Recursive Traversal Depth Limits
- Any recursive function traversing tree/graph data structures must have a max depth parameter
- Without it, circular references or maliciously deep structures cause stack overflow
- Pattern: `if (depth > MAX_DEPTH) return [];`

---

## Security Traps

### D3 .html() with String Concatenation
- Never use D3's `.html()` with template literals to build dynamic content
- Use D3 DOM manipulation instead: `tooltip.append('li').text(item)` — `.text()` escapes automatically
- The string-concat pattern is fragile: one forgotten `escapeHtml()` call creates an XSS vector

### D3 Scale Domain Collapse
- `d3.extent(values)` returns `[x, x]` when all values are identical, producing a degenerate scale where all outputs are NaN
- Guard with: `yMin === yMax ? [yMin - 1, yMax + 1] : [yMin, yMax]`

### DOM Dataset Values as Keys or Selectors
- `element.dataset.sort` used in bracket access or selectors can be manipulated via DOM
- Always validate dataset values against an allowlist before using them as object keys or CSS selectors

### Mass Assignment on Entity Objects
- Never accept entire entity objects from user input and bind them directly to database models
- User can manipulate internal fields like Id, CreatedAt, IsDeleted, Roles
- Use separate DTO/request models with only user-editable fields

### Information Disclosure in Validation Errors
- Use generic messages: "Product not found" instead of "Product 123 not found"
- Only reveal specific details in server logs, never in API responses

### Decimal Overflow in Financial Calculations
- Multiplying decimal Price * int Quantity can exceed decimal max value
- Always check result magnitude before assignment

### Context-Appropriate Encoding (HTML vs Attribute)
- `escapeHtml()` produces HTML entities correct for text content but wrong for HTML attribute values like `id` and `class`
- Use `sanitizeAttr()` for IDs and class names; use `escapeHtml()` only for text content

### CSS-Wide Keyword Injection
- Color sanitizers must block CSS-wide keywords: `inherit`, `initial`, `unset`, `revert`, `revert-layer`
- These change style inheritance rather than setting a color

### Client-Side API Key Exposure
- NEVER use framework-specific client-exposed env var prefixes (VITE_, NEXT_PUBLIC_, REACT_APP_) for secrets
- Inject credentials via server-side proxy headers or backend API routes

### LLM Tool Input Validation
- When an LLM calls tools via tool_use, all input parameters come from the model and must be validated as untrusted input
- Whitelist valid values for enums; cap numeric inputs; validate string IDs for type and length

---

## Design Traps

### Cleanup Symmetry (Resource Pairing)
- Every resource acquisition (event listener, subscription, interval, DOM element) must have a corresponding cleanup in the destroy/teardown path

### Unbounded User-Controlled Lists
- Lists parsed from user-controlled files (config, markdown, env) should have max limits
- Without limits, a malicious config can cause memory exhaustion

### Function Size
- Functions over 30 lines should be decomposed by extracting validation, categorization, and recording steps into named helpers

### Data Format Versioning
- Any persisted data format must include a schema version field
- Without it, v2 code cannot distinguish v1 data from corrupted data

### Non-Happy-Path Test Coverage
- Tests that only cover success paths miss corrupted files, lock contention, interrupted writes, and resource exhaustion
- Require at least one test per failure category that applies

### Database Migrations Over EnsureCreated
- Never use `EnsureCreated()` in production — always generate and apply migrations
- `EnsureCreated` skips migration history, making schema evolution impossible

### Health Check Endpoints
- Every web API needs a `/health` endpoint that returns 200 when the service is ready

### Structured Logging
- Use structured logging with correlation IDs, not default console/debug logging

---

## Code Quality Traps

### Dead Exports
- Verify exports are actually imported somewhere before creating them
- Don't write functions speculatively — wait until there's a caller

### Unused Imports
- Don't import symbols "just in case" — only import what you use
- After refactoring, check if imports became unused

### Redundant Verification Reads
- Don't `readFileSync` after `writeFileSync` to "verify" the write — trust the write

### Unused Parameters Escaping Lint
- ESLint's default `args: 'after-used'` only flags unused params after the last used one
- After refactoring, grep the function body for each parameter name to verify all are still referenced

### Exception Caught Locally (Re-wrapping Pattern)
- Validation checks and synchronous business logic should live OUTSIDE the try block
- Only wrap actual I/O and async operations in try-catch

---

## AI-Generated Antipatterns

### Single-Use Helper Functions
- Do not extract a helper function that is called exactly once — inline the logic at the call site

### Comment Spam
- Do not add JSDoc that restates the function name: `/** Get the user */ function getUser()` — delete it
- Only comment non-obvious behavior: unusual algorithms, why (not what), invariants, edge cases

### Defensive Paranoia
- Do not add null/undefined checks on typed parameters — trust TypeScript's type system
- Do not add `existsSync` checks after a function that already ensures the directory exists

### Speculative Features
- Do not add version fields, config options, or parameters that have only one possible value
- Do not create types/interfaces speculatively — wait until there's a second consumer

### Error Swallowing
- Empty `catch {}` blocks hide real errors. If swallowing is intentional, check the specific error condition

### Over-Extracting Obvious Literals
- Do not extract universally known values into named constants: `MONTHS_IN_YEAR = 12`, `HTTP_OK = 200`
- Only extract a number when its meaning is non-obvious in context or when it appears in multiple places

### Speculative Retry Loops
- Do not add retry loops with hardcoded attempt counts for exceptions that are rare or handled by the framework
- Trust the framework's exception handling — catch and fail fast

### Dependency Injection Violation
- Do not create new instances of repository/service classes inside controller methods
- Always inject dependencies via constructor

---

## Review False Positives

These are patterns that automated reviewers consistently flag but are NOT issues in certain contexts:

- **"Missing rate limiting"** — not applicable to local CLI tools
- **"Allowed base directory" restrictions** — not applicable when the user explicitly chooses their project directory
- **"Environment variable injection"** via `process.env` — not applicable when the user controls their own terminal
- **"Transaction/rollback for multi-step operations"** — disproportionate for dev tools where re-running is trivial
- **`--dangerously-skip-permissions` flag** — intentional for autonomous pipelines, not a vulnerability
- **"Command injection" with `shell: false`** — `execFile`/`spawn` with `shell: false` is safe by design
- **"Rewrite module state as a class"** — module-level `let` is standard for single-instance visualizations
- **"Use date-fns for date arithmetic"** — vanilla `Date` is sufficient for simple offsets
- **"Add input validation to every function"** — validate at boundaries, not internally in closed modules
- **"Split constants file into multiple files"** — for small modules, one file is appropriate
