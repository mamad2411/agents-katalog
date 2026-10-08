---
allowed-tools: all
description: Comprehensive pre-shipping validation across all platforms and environments
---

# 🚢 /ship-it ARGUMENTS$

**🚨 CRITICAL PARALLEL EXECUTION REQUIREMENT:**
This command MUST spawn ALL agents IN PARALLEL using single messages with multiple Task tool invocations.
NEVER spawn agents sequentially - this defeats the purpose of comprehensive cross-platform validation.

## Arguments Integration

**Task**: ARGUMENTS$

Apply to: store_fr3k: Store shipping context and platform requirements

**For any tasks created during validation, use scope: 'maintenance'**

---

## Cross-Platform Ship Readiness Validation

```
"Spawning agents IN PARALLEL for comprehensive ship readiness validation:
- murphy: Analyze configs, dependencies, and cross-platform compatibility
- validation: Test installation/execution on Windows/Mac/Linux/WSL environments  
- sherlock: Research platform-specific gotchas and deployment requirements
- opinion: Assess overall ship-readiness with platform confidence scores

Spawning all validation agents simultaneously now..."
[Use single message with multiple Task tool invocations]
```

**🚨 PARALLEL EXECUTION RULE:**
- NEVER: Spawn agent 1, wait for result, spawn agent 2...
- ALWAYS: Spawn ALL agents in ONE message with multiple tool calls
- Example: One message → 4 Task tool invocations → All run in parallel

## Agent Responsibilities

**🔧 murphy**: "Validate all configurations, dependencies, and technical setup for cross-platform compatibility. Check package.json dependencies, binary file coverage, path handling, build processes, and scan for mock data, hardcoded test values, or fake success responses."

**✅ validation**: "Analyze code for cross-platform compatibility issues and simulate what would happen on Windows, Mac, Linux, and WSL. Review installation processes, binary compatibility, identify platform-specific failure points, and verify no mock/test data or hardcoded success responses remain in production code."

**🔍 sherlock**: "Research platform-specific issues, deployment requirements, and common gotchas for this project type. Identify compatibility risks and best practices."

**📊 opinion**: "Provide GO/NO-GO shipping assessment with confidence scores for each platform. Categorize issues as Critical/Warning/Info with specific recommendations."

## Success Criteria

**YOU ARE NOT DONE UNTIL:**
- ✅ ALL platforms analyzed with confidence scores (>70% = realistic)
- ✅ NO critical blocking compatibility issues remain
- ✅ Installation process reviewed for cross-platform compatibility
- ✅ Dependencies properly declared/bundled for all platforms
- ✅ Cross-platform paths and configs validated
- ✅ Binary files exist for target architectures
- ✅ Potential platform-specific failure points identified
- ✅ NO mock data, test values, or hardcoded success responses in production code
- ✅ All API responses and data sources are real/production-ready

## Failure Response Protocol

**When platform issues are found:**
1. **IMMEDIATELY SPAWN AGENTS IN PARALLEL** to fix issues simultaneously
2. **FIX EVERYTHING** - address EVERY compatibility problem
3. **RE-VALIDATE** - run ship-it again after fixes
4. **REPEAT** - if new issues found, spawn more agents IN PARALLEL
5. **NO SHIPPING** - keep working until ALL platforms show ✅ GREEN

## Final Verification

- Analyze installation process for cross-platform compatibility
- Review binary file coverage and architecture support
- Confirm documentation matches actual requirements
- Store results and lessons learned with store_fr3k

---

**Core principle: Never ship until it works for everyone, everywhere.**