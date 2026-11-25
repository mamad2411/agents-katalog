---
name: natspec
description: >
  Generates NatSpec-style documentation comments for complex implementations
  in any language or framework. Use when the user wants to add, complete, or
  audit documentation comments. Works with TypeScript, JavaScript, Solidity,
  Python, Rust, Go, and any other language. Triggers on phrases like "natspec",
  "adicionar natspec", "documentar função", "documentar classe", "gerar docs",
  "comentários natspec", "missing docs", "document this", "add comments",
  "adicionar comentários", "documentar implementação", "generate natspec",
  "@notice", "@param", "@return", "@dev".
user-invocable: true
argument-hint: [file or directory]
allowed-tools: Read, Glob, Agent
---

# /natspec

Generates NatSpec-style documentation comments for complex implementations
in any language. Detects the file's language, adapts the comment syntax, and
documents all public/exported declarations.

## Reference

Read `references/natspec-patterns.md` for tag rules, format by language,
and examples before starting.

---

## Flow

### Step 1 — Identify the target

If the argument is a file → process only that file.

If the argument is a directory:
→ Glob for all source files recursively.
→ Ignore: `node_modules/`, `dist/`, `build/`, `.git/`, config files.

If no argument → ask the user: specific file or entire directory?

### Step 2 — Detect language and mode

**Language** (by file extension):

| Extension | Language | Comment syntax |
|---|---|---|
| `.ts`, `.tsx` | TypeScript | `/** ... */` (JSDoc) |
| `.js`, `.jsx` | JavaScript | `/** ... */` (JSDoc) |
| `.sol` | Solidity | `/// ...` (NatSpec native) |
| `.py` | Python | `"""..."""` (docstring) |
| `.rs` | Rust | `/// ...` (doc comments) |
| `.go` | Go | `// ...` (GoDoc) |
| Other | Generic | `/** ... */` |

**Mode** (by current coverage):

| Situation | Mode |
|---|---|
| No documentation at all | `full` — document everything |
| Partial documentation | `patch` — complete what's missing |
| Fully documented | `audit` — validate only |

### Step 3 — Execute in parallel

For each file in `full` or `patch` mode, spawn a `natspec-writer`:

```
Agent(
  subagent_type: "natspec-writer",
  prompt: "File: [path]. Language: [language]. Mode: [full|patch].
           Read the file, generate NatSpec for all public/exported functions,
           classes, interfaces, types, events, and errors.
           Reference: .claude/skills/natspec/references/natspec-patterns.md"
)
```

Independent files run in parallel. One agent per file.

### Step 4 — Validate in parallel

After all writers complete, spawn a `natspec-validator` per file:

```
Agent(
  subagent_type: "natspec-validator",
  prompt: "Validate NatSpec completeness in: [path]. Language: [language].
           Reference: .claude/skills/natspec/references/natspec-patterns.md"
)
```

### Step 5 — Consolidated output

```
NATSPEC COMPLETE

Files processed: N
  ✅ src/module/file.ts — 12 declarations documented, 0 issues
  ✅ contracts/Vault.sol — 8 declarations documented, 0 issues
  ⚠️ src/lib/api.ts — 5 declarations documented, 2 warnings
     └─ Line 47: @returns missing description
     └─ Line 89: @param has no description

Total: N functions | N classes | N types documented
```

---

## Special cases

**Private/internal functions:**
→ `@dev` only — `@notice` is optional (not ABI/API public).

**Inheritance / Override:**
→ Override with no added logic: use `@inheritdoc`.
→ Override with added logic: document normally + mention the override.

**Complex types (interfaces, enums, structs):**
→ Document the type with `@notice`.
→ Document each field/member with inline `@dev`.

**Async functions:**
→ `@returns` must describe what the Promise resolves to, not the Promise itself.

## Success Criteria
- [ ] All exported/public declarations have `@notice` and `@param`/`@returns`
- [ ] Private functions have `@dev` when logic is non-obvious
- [ ] Comment syntax correct for each file's language
- [ ] Validator reports PASSED for all files
