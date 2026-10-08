---
allowed-tools: all
description: Universal project health audit using real-world pattern comparison
---

# 🔍 /fr3k-compare ARGUMENTS$

**🚨 CRITICAL PARALLEL EXECUTION REQUIREMENT:**
This command MUST spawn ALL audit agents IN PARALLEL using single messages with multiple Task tool invocations.
NEVER spawn agents sequentially - this defeats the purpose of comprehensive real-world pattern analysis.

## Arguments Integration

**Task**: ARGUMENTS$

Apply to: store_fr3k: Store specific areas to audit and comparison context

**For any tasks created during audit analysis, use scope: 'maintenance'**

---

## Parallel Agent Research

**CRITICAL: Use PARALLEL spawning - ALL agents in ONE message:**

```
"Spawning specialized research agents IN PARALLEL for comprehensive project audit:

- murphy: Use GREP MCP to research dependency management and config patterns. Compare our project's setup against similar repos and report adoption rates for different approaches
- bugsy: Use GREP MCP to research error handling patterns. Find how similar projects handle errors, crashes, and resilience - compare to our current implementation
- validation: Use GREP MCP to research testing and CI/CD patterns. Compare our testing setup and automation against similar projects in the ecosystem
- scribe: Use GREP MCP to research documentation patterns. Compare our README, API docs, and guides against successful similar projects
- opinion: Use GREP MCP to research performance and quality patterns. Find optimization strategies and metrics used by similar projects - assess our current state
- gitty: Use GREP MCP to research git workflow patterns. Compare our repo practices, commit styles, and development workflows against similar projects
- fronty: Use GREP MCP to research frontend patterns (if React/Next.js detected). Compare our component architecture and optimizations against similar apps
- [LANGUAGE_SPECIALIST]: Use GREP MCP to research language ecosystem patterns. Compare our language-specific practices against community standards

Each agent analyzes their domain independently and reports findings with adoption percentages.
Spawning all research agents simultaneously now..."
[Use single message with multiple Task tool invocations]
```

**MANDATORY: Replace [LANGUAGE_SPECIALIST] with detected project agent:**
- **Go projects** → **gopher** agent (search Go ecosystem patterns, best practices)
- **JavaScript/Node.js** → **jsmaster** agent (search Node.js patterns, npm ecosystem)
- **Python projects** → **thesnake** agent (search Python patterns, PyPI ecosystem)  
- **TypeScript projects** → **typegod** agent (search TypeScript patterns, type safety practices)
- **React projects** → **reactlord** agent (search React patterns, component architectures)
- **Vue.js projects** → **vuelord** agent (search Vue.js patterns, composition API usage)
- **Next.js projects** → **nextking** agent (search Next.js patterns, optimization strategies)
- **Mixed/Unknown** → **artisan** (ONLY as last resort when language unclear)

## Success Criteria

**YOU ARE NOT DONE UNTIL:**
- ✅ ALL agents have completed specialized GREP MCP research in their domains
- ✅ Each agent has compared our project against similar projects in their area
- ✅ Evidence-based recommendations provided with adoption rate percentages
- ✅ Actionable prioritized improvement list generated
- ✅ All findings stored with store_fr3k for future reference

**🚨 PARALLEL EXECUTION RULE:**
- NEVER: Spawn agent 1, wait for result, spawn agent 2...
- ALWAYS: Spawn ALL agents in ONE message with multiple tool calls
- Example: One message → 9+ Task tool invocations → All run in parallel

## Failure Response Protocol  

**When research gaps are found:**
1. **IMMEDIATELY SPAWN ADDITIONAL AGENTS IN PARALLEL** to fill knowledge gaps
2. **EXPAND SEARCH SCOPE** - try broader ecosystem patterns if specific ones fail
3. **RE-VALIDATE** - cross-check findings across multiple agent perspectives
4. **DOCUMENT UNCERTAINTY** - clearly flag low-confidence recommendations
5. **NO GUESSING** - if patterns can't be found, report research limitations honestly

## Final Output Format

Expected comprehensive report structure:
```
🔍 FR3K COMPARE RESULTS: [Project Type]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📈 Overall Health Score: X.X/10 ([Status])
🎯 Comparison Baseline: [N similar projects analyzed]
📊 Research Confidence: [High/Medium/Low]

⚡ HIGH IMPACT OPPORTUNITIES:
├─ [Domain]: [Specific finding] ([Adoption %] of similar projects)
├─ [Domain]: [Specific finding] ([Adoption %] of similar projects)
└─ [Domain]: [Specific finding] ([Adoption %] of similar projects)

🎯 INNOVATION DETECTED:
[List unique approaches with intentionality assessment]

📋 DOMAIN-SPECIFIC FINDINGS:
[Detailed breakdown by each agent's research domain]

🚀 PRIORITIZED ACTION PLAN:
[Impact/effort scored recommendations]
```

---

**Core principle: Compare against real-world evidence, respect innovation, provide actionable insights backed by ecosystem data.**