---
allowed-tools: all
description: Behavior-preserving refactoring with safety validation
---

# 🔧 /refactor ARGUMENTS$

**THIS IS BEHAVIOR-PRESERVING REFACTORING - NO LOGIC CHANGES!**

## Arguments Integration

**Task**: ARGUMENTS$

Apply to: store_fr3k: Store refactoring scope and behavior preservation requirements

**For any tasks created during refactoring, use scope: 'maintenance'**

---

## Phase 1: Analysis & Safety Planning

**IMMEDIATELY spawn agents for refactoring analysis:**
```
"I'll spawn agents to analyze refactoring opportunities safely:
- sherlock: Analyze current code structure and identify refactoring candidates
- [SPECIALIZED_AGENT]: Plan behavior-preserving changes by risk level
- bugsy: Identify potential breaking points and test coverage gaps
- [SPECIALIZED_AGENT]: Design safety validation strategy
Let me analyze refactoring scope in parallel..."
```

**MANDATORY: Use language-specific agent for refactoring:**
- **Go refactoring** → **gopher** agent (Go-specific patterns and idioms)
- **JavaScript/Node.js refactoring** → **jsmaster** agent (modern JS patterns)
- **Python refactoring** → **thesnake** agent (Pythonic patterns and idioms)
- **TypeScript refactoring** → **typegod** agent (type-safe refactoring)
- **React refactoring** → **reactlord** agent (React patterns and hooks)
- **Vue.js refactoring** → **vuelord** agent (Vue composition patterns)
- **Next.js refactoring** → **nextking** agent (Next.js specific optimizations)
- **Mixed/Unknown** → **artisan** (ONLY as last resort)

## Phase 2: Safe Refactoring Implementation

**IMMEDIATELY spawn agents for parallel refactoring:**
```
"I'll spawn specialized agents to handle different risk levels in parallel:
- [SPECIALIZED_AGENT]: Level 1 changes (formatting, whitespace, comments)
- [SPECIALIZED_AGENT]: Level 2 changes (variable renaming, method extraction)
- [SPECIALIZED_AGENT]: Level 3 changes (structural improvements with tests)
- bugsy: Continuous validation and behavior verification
Let me refactor safely in parallel..."
```

**MANDATORY: Use SAME specialized agent throughout all refactoring phases**

## Phase 3: Validation & Testing

**IMMEDIATELY spawn agents for comprehensive validation:**
```
"I'll spawn agents to validate all refactoring changes:
- [SPECIALIZED_AGENT]: Run complete test suite and verify behavior
- bugsy: Test edge cases and error scenarios
- [SPECIALIZED_AGENT]: Performance validation and regression testing
- murphy: Verify build and deployment processes still work
Let me validate everything in parallel..."
```

**MANDATORY: Use SAME specialized agent for validation as used for implementation**

## Success Criteria

Before marking complete:
- [ ] ALL existing functionality works identically
- [ ] ALL tests pass without modification
- [ ] Build succeeds with no errors
- [ ] Code is cleaner but behavior is unchanged
- [ ] Performance is same or better
- [ ] User approves all changes made

## Safety Rules

- **Test after every change** - no batching
- **Preserve exact behavior** - no logic improvements
- **Get user approval** for structural changes
- **Rollback if anything breaks** - safety first

---

**Core principle: Clean code through safe, behavior-preserving transformations.**