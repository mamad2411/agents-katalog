---
allowed-tools: all
description: Create contextual validation scripts that prove business logic works for what we just built
---

# 💪 /prove-it-fr3k

**Context-aware validation script generator that proves business logic works based on current session work.**

## Core Concept

This command creates **minimal "proof-of-life" validation scripts** that prove the business logic of what we just implemented actually works. Not comprehensive tests - just proof that the core requirements are met.

## Phase 1: Context Capture

**Since we just built this together, I already know the context. Just confirm what we built:**

```bash
# Quick sanity check - what files did we just touch?
git status --porcelain
```

**Then immediately create the validation script based on our discussion.**

## Phase 2: Validation Script Creation

**Focus on BUSINESS LOGIC validation, not implementation details:**

### Script Naming Pattern:
- `validate-{feature-name}.{ext}` (e.g., `validate-chunking-formatter.js`)
- Place in `/scripts/validation/` directory

### Script Template Structure:
```javascript
#!/usr/bin/env node
// Validates: {CORE_BUSINESS_REQUIREMENT}
// Created: {DATE} for session context

// Setup minimal test data
const testInput = {REALISTIC_INPUT};

// Call the feature we just built
const result = {FEATURE_FUNCTION}(testInput);

// Prove the main business requirement works
console.assert(result.{KEY_PROPERTY} === {EXPECTED_VALUE}, 'Core business logic failed');
console.assert({SECONDARY_ASSERTION}, 'Secondary requirement failed');

console.log('✅ Business logic validated - {FEATURE_NAME} works as expected');
process.exit(0);
```

## Phase 3: Contextual Intelligence

**The script must validate based on what we ACTUALLY discussed:**

### If we built chunking + formatter:
- Validate: Input gets chunked correctly
- Validate: Chunks get formatted as expected
- Validate: Edge cases (empty input, large input) work

### If we built API endpoint:
- Validate: Endpoint responds with correct status
- Validate: Response structure matches requirements
- Validate: Error handling works for invalid inputs

### If we built data processor:
- Validate: Input data gets transformed correctly
- Validate: Output format matches specification
- Validate: Performance is within acceptable range

## Phase 4: Minimal Implementation

**Keep validation scripts under 50 lines and reasonably fast:**

### Requirements:
- **Single file** - no complex test frameworks
- **Actual execution** - must run the real code we built
- **Business-focused** - test requirements, not implementation
- **Throwaway mentality** - disposable after feature stabilizes
- **Clear output** - obvious success/failure messages

### What NOT to include:
- ❌ Complex test frameworks (Jest, Mocha, etc.)
- ❌ Mocking or stubbing (use real implementations)
- ❌ Comprehensive edge case testing
- ❌ Performance benchmarking (unless that was the feature)
- ❌ Integration with CI/CD systems

## Phase 5: Test the Script

**Simply run the validation script and fix any issues:**

```bash
# Make it executable and run it
chmod +x validate-feature-name.js
./validate-feature-name.js
```

**If it fails, fix the script directly - no agents needed.**

## Success Criteria

Before marking complete:
- [ ] Script tests the actual feature we just built
- [ ] Script validates business requirements from our discussion
- [ ] Script fails meaningfully when logic is broken
- [ ] Clear success/failure output
- [ ] Executable permissions set
- [ ] Stored in appropriate location

## When Validation Isn't Possible

**Some features can't be validated without external dependencies:**

- **API keys missing** - Create script that checks for keys, skips validation if not found
- **Database not available** - Mock the data layer or skip DB-dependent tests
- **External services down** - Add fallback checks or skip network-dependent validation
- **Authentication required** - Test with mock auth or document what needs manual testing

**In these cases:**
```javascript
// Check if we can actually validate
if (!process.env.API_KEY) {
    console.log('⚠️  Cannot validate - API_KEY not provided');
    console.log('   Manual test: Set API_KEY and run again');
    process.exit(0); // Not a failure, just incomplete
}
```

## Memory Integration

```
store_fr3k: Created proof-of-life validation for {FEATURE} - tests core business logic in {TIME}ms
```

---

**Core principle: Prove it works, don't test everything. Context is king.**