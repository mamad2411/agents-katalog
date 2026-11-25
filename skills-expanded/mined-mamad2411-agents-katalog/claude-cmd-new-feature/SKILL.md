---
allowed-tools: all
description: Build new features with proper testing and validation
---

# 🎯 /new-feature ARGUMENTS$

**🚨 CRITICAL PARALLEL EXECUTION REQUIREMENT:**
This command MUST spawn ALL agents IN PARALLEL using single messages with multiple Task tool invocations.
NEVER spawn agents sequentially - this defeats the purpose of comprehensive feature development.

## Arguments Integration

**Task**: ARGUMENTS$

Apply to: store_fr3k: Store feature requirements and context

---

## Phase 1: Feature Planning & Research

**For any tasks created, use scope: 'feature'**

**CRITICAL: Use PARALLEL spawning - ALL agents in ONE message:**
```
"Spawning research agents IN PARALLEL based on complexity:
- sherlock: Existing pattern analysis for similar implementations
- sherlock: Architecture impact and system constraints  
- murphy: Dependencies and integration requirements
- opinion: Evaluate feature approach and complexity

Spawning all research agents simultaneously now..."
[Use single message with multiple Task tool invocations]
```

## Phase 2: Implementation Strategy

**CRITICAL: Spawn ALL development agents IN PARALLEL - single message, multiple tools:**
```
"Spawning agents IN PARALLEL to implement the new feature:
- [SPECIALIZED_AGENT]: Design and implement core feature functionality
- [SPECIALIZED_AGENT]: Create comprehensive tests for new feature  
- [SPECIALIZED_AGENT]: Implement error handling and edge cases
- scribe: Document feature usage and API

Spawning all development agents simultaneously now..."
[MUST use single message with multiple Task tool invocations]
```

**MANDATORY: Replace [SPECIALIZED_AGENT] with language-specific agent:**
- **Go features** → **gopher** agent
- **JavaScript/Node.js features** → **jsmaster** agent
- **Python features** → **thesnake** agent
- **TypeScript features** → **typegod** agent
- **React features** → **reactlord** agent
- **Vue.js features** → **vuelord** agent
- **Next.js features** → **nextking** agent
- **Mixed/Unknown** → **artisan** (ONLY as last resort)

## Phase 3: Integration & Validation

**CRITICAL: Spawn ALL integration agents IN PARALLEL - all at once:**
```
"Spawning agents IN PARALLEL to integrate and validate the feature:
- [SPECIALIZED_AGENT]: Integrate feature with existing codebase
- bugsy: Test integration points and fix any conflicts
- murphy: Update configurations and dependencies
- [SPECIALIZED_AGENT]: Validate feature works end-to-end

Spawning all integration agents simultaneously now..."
[Use single message with multiple Task tool invocations]
```

**MANDATORY: Use same specialized agent as development phase:**
- Maintain consistency by using the SAME language specialist throughout all phases
- NEVER mix artisan with specialized agents in the same feature

**🚨 PARALLEL EXECUTION RULE:**
- NEVER: Spawn agent 1, wait for result, spawn agent 2...
- ALWAYS: Spawn ALL agents in ONE message with multiple tool calls
- Example: One message → 4 Task tool invocations → All run in parallel

## Success Criteria

Before marking complete:
- [ ] Feature works as specified
- [ ] All tests pass including new feature tests
- [ ] Integration with existing code is seamless
- [ ] Error handling is comprehensive
- [ ] Documentation is complete and accurate
- [ ] Performance is acceptable
- [ ] Security considerations are addressed

## Feature Validation

- Test feature with real use cases
- Verify edge cases are handled
- Confirm integration doesn't break existing functionality
- Store feature implementation lessons with store_fr3k

---

**Core principle: Build features that work reliably and integrate seamlessly.**