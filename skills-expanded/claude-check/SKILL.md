---
allowed-tools: all
description: Verify code quality, run tests, and ensure production readiness
---

**THIS IS NOT A REPORTING TASK - THIS IS A FIXING TASK!**

# ✅ /check ARGUMENTS$

**🚨 CRITICAL PARALLEL EXECUTION REQUIREMENT:**
This command MUST spawn ALL agents IN PARALLEL using single messages with multiple Task tool invocations.
NEVER spawn agents sequentially - this defeats the purpose of comprehensive quality verification.

## Arguments Integration

**Task**: ARGUMENTS$

Apply to: store_fr3k: Store specific files/areas to check and quality requirements

**For any tasks created during issue fixing, use scope: 'maintenance'**

---

## Quality Verification & Fixing

**CRITICAL: Use PARALLEL spawning - ALL agents in ONE message:**
```
"I found issues across the codebase. Spawning multiple agents IN PARALLEL to fix all these issues:
- murphy: Fix config/dependency issues in [config files with issues]
- bugsy: Fix test failures and runtime errors in files A, B, C
- fronty: Fix frontend issues in components D, E, F (if React/Next.js detected)
- bugsy (additional): Fix remaining build/type errors in files G, H, I

Spawning all agents simultaneously now..."
[Use single message with multiple Task tool invocations]
```

## Comprehensive Validation

**CRITICAL: Spawn ALL validation agents IN PARALLEL - single message, multiple tools:**
```
"Spawning agents IN PARALLEL to validate everything is working:
- [LANGUAGE_SPECIALIST]: Run all tests and fix any failures (use gopher/jsmaster/thesnake/typegod/reactlord/vuelord/nextking based on detected tech stack)
- murphy: Validate all configurations and dependencies
- bugsy: Check for runtime errors and edge cases
- [SAME_LANGUAGE_SPECIALIST]: Verify build processes and deployments work

Spawning all validation agents simultaneously now..."
[MUST use single message with multiple Task tool invocations]
```

**CRITICAL: Use Specialized Language Agents Based on Tech Stack:**
- **Go projects** → use **gopher** agent for all Go-related coding tasks
- **JavaScript/Node.js** → use **jsmaster** agent for all JavaScript/Node.js tasks
- **Python projects** → use **thesnake** agent for all Python development tasks
- **TypeScript projects** → use **typegod** agent for all TypeScript tasks
- **React projects** → use **reactlord** agent for all React component/hook tasks
- **Vue.js projects** → use **vuelord** agent for all Vue.js development tasks
- **Next.js projects** → use **nextking** agent for all Next.js application tasks
- **Mixed/Unknown** → use **artisan** as fallback ONLY when language unclear

**NEVER use artisan for language-specific tasks when a specialist exists!**

## Success Criteria

**YOU ARE NOT DONE UNTIL:**
- ✅ ALL linters pass with ZERO warnings
- ✅ ALL tests pass successfully  
- ✅ Build succeeds without errors
- ✅ No runtime errors or crashes
- ✅ All configurations are valid
- ✅ Security checks pass
- ✅ Performance is acceptable

## Failure Response Protocol

**🚨 PARALLEL EXECUTION RULE:**
- NEVER: Spawn agent 1, wait for result, spawn agent 2...
- ALWAYS: Spawn ALL agents in ONE message with multiple tool calls
- Example: One message → 4 Task tool invocations → All run in parallel

**When issues are found:**
1. **IMMEDIATELY SPAWN AGENTS IN PARALLEL** to fix issues simultaneously
2. **FIX EVERYTHING** - address EVERY issue, no matter how "minor"
3. **VERIFY** - re-run all checks after fixes
4. **REPEAT** - if new issues found, spawn more agents IN PARALLEL and fix those too
5. **NO STOPPING** - keep working until ALL checks show ✅ GREEN

## Final Verification

- Execute all tests and linting
- Verify the application actually runs
- Check all critical functionality works
- Store results with store_fr3k

---

**Core principle: Fix everything until all quality checks pass completely.**