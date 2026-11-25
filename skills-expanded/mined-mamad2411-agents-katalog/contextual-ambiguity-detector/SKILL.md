---
name: "Contextual Ambiguity Detector"
version: "1.0.0"
description: "Detects hidden assumptions, undocumented choices, and alternative-path gaps in code. Surfaces where code chose one way without explaining why, making implicit decisions explicit."
author: "workspace"
activated: false
---

# Contextual Ambiguity Detector

Detects hidden assumptions, undocumented choices, and alternative-path gaps in code. Surfaces where code chose one way without explaining why, making implicit decisions explicit.

## Decision Framework

### When to Apply
Use when:
- Reviewing code with hardcoded magic numbers or string literals
- Finding conditional logic that assumes user behavior (e.g., "users will always have email")
- Spotting API integrations with assumed response formats
- Detecting UI code with assumed screen sizes or input methods
- Code review where "why this way?" has no documented answer

### When NOT to Apply
Don't use when:
- Code is well-documented with ADRs (Architecture Decision Records)
- Configuration is externalized and environment-driven
- Domain rules are formally specified (e.g., regulatory requirements)

## Anti-Patterns Detected

## Trigger Phrases

- "Review code for assumptions"
- "Check for hardcoded values"
- "Detect hidden choices"
- "Find undocumented decisions"
- "Audit code assumptions"

### 1. User Behavior Assumptions
Code that assumes how users will interact without fallbacks.

```javascript
// ASSUMPTION: User always has a name
const displayName = user.firstName + ' ' + user.lastName;

// BETTER: Handle missing data
const displayName = [user.firstName, user.lastName]
  .filter(Boolean)
  .join(' ') || 'Anonymous User';
```

**Triggers:**
- Direct property access without null checks
- String concatenation assuming non-empty values
- Date/time calculations assuming timezone
- Form submissions assuming all fields filled

### 2. Tech Stack Assumptions
Hardcoded dependencies on specific technologies without abstraction.

```javascript
// ASSUMPTION: Always MySQL
const query = `SELECT * FROM users WHERE id = ${id}`;

// BETTER: Abstracted
const query = db.select('users').where({ id });
```

**Triggers:**
- Raw SQL strings
- Browser-specific APIs without feature detection
- OS-specific file paths
- Network assumptions (always online, specific latency)

### 3. UI Pattern Assumptions
Interface code that assumes specific interaction patterns.

```javascript
// ASSUMPTION: Desktop mouse interaction
element.addEventListener('click', handler);

// BETTER: Universal interaction
element.addEventListener('click', handler);
element.addEventListener('touchend', handler);
element.setAttribute('role', 'button');
element.setAttribute('tabindex', '0');
```

**Triggers:**
- Mouse-only event handlers
- Fixed pixel layouts
- Assumed viewport sizes
- Hover-dependent interactions

### 4. Data Shape Assumptions
Code that assumes specific data structures without validation.

```javascript
// ASSUMPTION: Response always has data.users array
const users = response.data.users.map(u => u.name);

// BETTER: Validated access
const users = (response?.data?.users || []).map(u => u?.name || 'Unknown');
```

**Triggers:**
- Deep property access without optional chaining
- Array operations without empty checks
- API response usage without schema validation

### 5. Edge Case Blindspots
Missing handling for boundary conditions.

```javascript
// BLINDSPOT: Zero, negative, very large quantities
const total = price * quantity;

// BETTER: Validated
const total = price * Math.max(0, Math.min(quantity, MAX_ORDER_QTY));
```

**Triggers:**
- Division without zero-check
- Array access without bounds check
- Date math without DST consideration
- File operations without size limits

## Detection Rules

| Rule ID | Category | Severity | Pattern |
|---------|----------|----------|---------|
| AMB-001 | User Assumption | Warning | Property access without null check |
| AMB-002 | User Assumption | Error | Name/email concatenation |
| AMB-003 | Tech Assumption | Warning | Raw SQL string |
| AMB-004 | Tech Assumption | Error | Browser-specific API |
| AMB-005 | UI Assumption | Warning | Click handler without touch |
| AMB-006 | UI Assumption | Error | Fixed pixel dimensions |
| AMB-007 | Data Assumption | Warning | Deep property access |
| AMB-008 | Data Assumption | Error | Array operation without check |
| AMB-009 | Edge Case | Warning | Division operation |
| AMB-010 | Edge Case | Error | Unbounded iteration |

## Output Format

```markdown
## Ambiguity Report

### 🔴 Critical (Must Document)
- [file:line] Assumes all users have email addresses
  - Alternative: Support phone-only or anonymous users
  - Decision: Document in ADR-XXX

### 🟡 Warnings (Should Document)  
- [file:line] Hardcoded to PostgreSQL array syntax
  - Alternative: Use parameterized queries
  - Decision: Document in ADR-XXX

### 📝 Suggestions (Consider)
- [file:line] Assumes desktop viewport
  - Alternative: Responsive breakpoints
  - Decision: Document if intentional
```

## Integration with Other Skills

- **database-schema-designer**: Validate data access assumptions
- **authentication-flow-designer**: Check identity/permission assumptions  
- **accessibility-pattern-library**: Verify interaction assumptions
- **mobile-gesture-handler**: Validate touch/mobile assumptions
