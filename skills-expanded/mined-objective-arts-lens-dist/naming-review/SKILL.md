---
name: naming-review
description: Review names for clarity principles. Find jargon, ambiguity, inconsistency.
---

# /naming-review [path]

Review names in code or configuration for clarity, consistency, and intent.

> **No arguments?** Describe this skill and stop. Do not execute.

*"Say what you mean, simply and directly."*

## Also Detect: AI-Generated Naming Antipatterns

In addition to clarity-style naming issues, flag these AI naming smells:

| Antipattern | Example | Problem |
|-------------|---------|---------|
| Enterprise suffixes | `UserManager`, `DataHandler`, `ServiceHelper` | Vague, adds no information |
| Unnecessary prefixes | `IUserService`, `AbstractBase` | Hungarian notation for types |
| Generic -er names | `Processor`, `Handler`, `Manager` | Says nothing about what it does |
| Impl suffixes | `UserServiceImpl` | Only one implementation exists |
| Over-qualified names | `UserEntityDataModelObject` | Afraid to commit to a name |

**A name should say what it IS, not what category it belongs to.**

---

## Process

### Step 1: Collect Names

Gather all names in scope:
- Function/method names
- Variable names
- Class/type names
- File/directory names
- Config keys
- CLI commands/flags
- API endpoints

### Step 2: Apply Naming Principles

Review each name against these criteria:

## Naming Principles

### 1. Say What It Does (Clarity)

Names should describe behavior, not implementation.

| Bad | Good | Why |
|-----|------|-----|
| `processData()` | `validateUserInput()` | Says what it actually does |
| `doStuff()` | `sendEmailNotification()` | Specific action |
| `handle()` | `retryFailedPayment()` | Reveals intent |

### 2. Verbs for Actions, Nouns for Things (Clean Code)

| Type | Pattern | Examples |
|------|---------|----------|
| Functions that DO | verb-noun | `createUser`, `deleteFile`, `validateInput` |
| Functions that ASK | is/has/can | `isValid`, `hasPermission`, `canRetry` |
| Classes/Types | noun | `User`, `PaymentProcessor`, `FileReader` |
| Booleans | is/has/should | `isActive`, `hasErrors`, `shouldRetry` |

### 3. Consistent Patterns (Google Style)

Pick a pattern and stick to it across the codebase:

| Pattern | Stick With | Don't Mix |
|---------|------------|-----------|
| get/set | `getUser`, `setUser` | `fetchUser`, `updateUser` |
| create/delete | `createOrder`, `deleteOrder` | `newOrder`, `removeOrder` |
| start/stop | `startJob`, `stopJob` | `beginJob`, `endJob` |
| read/write | `readFile`, `writeFile` | `loadFile`, `saveFile` |

### 4. No Jargon or Insider Terms

Names should be clear to someone new to the codebase.

| Jargon | Clear | Why |
|--------|-------|-----|
| `canonReport` | `skillUsageReport` | "Canon" is internal terminology |
| `ralphLoop` | Keep if documented | Proper noun, acceptable if explained |
| `PSF` | `pageSortFilter` | Abbreviations obscure meaning |
| `ctx` | `context` | Don't abbreviate unnecessarily |

### 5. No Abbreviations (Unless Universal)

| Acceptable | Unacceptable |
|------------|--------------|
| `id`, `url`, `html`, `api` | `usr`, `msg`, `btn`, `cfg` |
| `max`, `min`, `avg` | `cnt`, `idx`, `tmp` |
| `async`, `sync` | `db` (use `database`) |

### 6. Length Matches Scope (Code Complete)

| Scope | Length | Example |
|-------|--------|---------|
| Loop counter | 1 char | `i`, `j`, `k` |
| Local variable | short | `user`, `count` |
| Function parameter | medium | `userId`, `filterOptions` |
| Class field | descriptive | `activeUserCount`, `lastLoginDate` |
| Global/exported | very clear | `MAX_RETRY_ATTEMPTS`, `defaultTimeoutMs` |

### 7. Suffix Patterns for Behavior

Use consistent suffixes to signal behavior:

| Suffix | Meaning | Examples |
|--------|---------|----------|
| `-scan` | Read-only, reports | `gemini-scan`, `qodana-scan` |
| `-fix` | Modifies, repairs | `gemini-review`, `deduplication` |
| `-check` | Validates, returns bool | `type-check`, `lint-check` |
| `-report` | Generates output | `skill-usage-report` |
| `-config` | Configuration object | `appConfig`, `dbConfig` |
| `-handler` | Event/request handler | `errorHandler`, `clickHandler` |
| `-factory` | Creates instances | `userFactory`, `connectionFactory` |

### 8. Prefix Patterns for Type

| Prefix | Meaning | Examples |
|--------|---------|----------|
| `is-`, `has-`, `can-` | Boolean | `isActive`, `hasError` |
| `get-`, `fetch-` | Retrieves data | `getUser`, `fetchOrders` |
| `set-`, `update-` | Modifies data | `setName`, `updateStatus` |
| `create-`, `build-` | Constructs new | `createUser`, `buildQuery` |
| `delete-`, `remove-` | Destroys | `deleteFile`, `removeItem` |
| `on-` | Event handler | `onClick`, `onSubmit` |

## Output Format

```markdown
## Naming Review: [target]

### Summary

| Metric | Value |
|--------|-------|
| Names reviewed | N |
| Issues found | N |
| Patterns broken | N |

### Issues Found

#### Unclear Names 🔴

| Current | Problem | Suggested |
|---------|---------|-----------|
| `processData()` | Vague verb | `validateUserInput()` |
| `handle()` | Says nothing | `routeHttpRequest()` |

#### Jargon/Abbreviations 🟠

| Current | Problem | Suggested |
|---------|---------|-----------|
| `getPSF()` | Abbreviation | `getPageSortFilter()` |
| `canonPath` | Insider jargon | `skillLibraryPath` |

#### Inconsistent Patterns 🟡

| Pattern A | Pattern B | Recommendation |
|-----------|-----------|----------------|
| `getUser` | `fetchOrder` | Standardize on `get-` |
| `createFile` | `newDirectory` | Standardize on `create-` |

#### Wrong Part of Speech 🟡

| Current | Problem | Suggested |
|---------|---------|-----------|
| `validation()` | Noun for action | `validate()` |
| `active` (function) | Adjective for action | `isActive()` or `activate()` |

### Patterns Detected

- [x] Consistent get/set usage
- [ ] Mixed create/new usage
- [x] Boolean prefixes (is/has)
- [ ] Unclear abbreviations

### Recommendations

1. **Standardize on `create-`** — Replace `new-` prefix with `create-`
2. **Expand abbreviations** — `cfg` → `config`, `msg` → `message`
3. **Add verb to vague names** — `data()` → `fetchData()` or `processData()`

---
NAMES_REVIEWED: N
ISSUES_FOUND: N
NAMING_REVIEW_COMPLETE: yes
```

## Rules

- **BE SPECIFIC** — Point to exact names, not vague categories
- **SUGGEST ALTERNATIVES** — Don't just criticize, propose better names
- **CHECK CONSISTENCY** — Same concept should use same words everywhere
- **RESPECT CONTEXT** — Domain terms (medical, financial) may look like jargon but are correct

## When to Use

- Before PR review
- After major refactoring
- Onboarding new codebase
- API design review
- CLI/config design

## Anti-Patterns (Don't Do)

- Renaming without understanding context
- Enforcing personal preference over team conventions
- Flagging domain-specific terms as jargon
- Suggesting longer names just to be "clearer"
- Ignoring existing codebase conventions
