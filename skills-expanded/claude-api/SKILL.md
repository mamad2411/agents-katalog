---
allowed-tools: all
description: Build complete API with testing, docs, and deployment
---

# 🔌 /api ARGUMENTS$

**🚨 CRITICAL PARALLEL EXECUTION REQUIREMENT:**
This command MUST spawn ALL agents IN PARALLEL using single messages with multiple Task tool invocations.
NEVER spawn agents sequentially - this defeats the purpose of comprehensive API development.

## Arguments Integration

**Task**: ARGUMENTS$

Apply to: store_fr3k: Store API requirements and context

---

## Phase 1: API Discovery & Planning

**CRITICAL: Use PARALLEL spawning - ALL agents in ONE message:**
```
"Spawning agents IN PARALLEL for comprehensive API development:
- sherlock: Analyze existing API patterns and frameworks
- murphy: Validate database schemas and dependencies
- sherlock: Research authentication and security best practices
- [SPECIALIZED_AGENT]: Design API structure and endpoints

Spawning all analysis agents simultaneously now..."
[Use single message with multiple Task tool invocations]
```

**MANDATORY: Replace [SPECIALIZED_AGENT] with language-specific agent:**
- **Go APIs** → **gopher** agent (for gin, echo, gorilla/mux APIs)
- **JavaScript/Node.js APIs** → **jsmaster** agent (for Express, Koa, Fastify APIs)
- **Python APIs** → **thesnake** agent (for FastAPI, Django, Flask APIs)
- **TypeScript APIs** → **typegod** agent (for type-safe backend APIs)
- **Next.js APIs** → **nextking** agent (for Next.js API routes)
- **Mixed/Unknown** → **artisan** (ONLY as last resort)

## Phase 2: Implementation

**CRITICAL: Spawn ALL implementation agents IN PARALLEL - single message, multiple tools:**
```
"Spawning agents IN PARALLEL for API implementation:
- [SPECIALIZED_AGENT]: Build core API endpoints and routing
- [SPECIALIZED_AGENT]: Implement authentication and middleware
- [SPECIALIZED_AGENT]: Create database models and validation
- murphy: Configure deployment and environment settings
- scribe: Generate API documentation and examples

Spawning all implementation agents simultaneously now..."
[MUST use single message with multiple Task tool invocations]
```

**MANDATORY: Use SAME specialized agent as design phase throughout implementation**

## Phase 3: Testing & Validation

**CRITICAL: Spawn ALL testing agents IN PARALLEL - all at once:**
```
"Spawning agents IN PARALLEL for comprehensive testing:
- [SPECIALIZED_AGENT]: Create unit tests for all endpoints
- bugsy: Test error handling and edge cases
- murphy: Validate security and performance
- [SPECIALIZED_AGENT]: Integration testing and end-to-end flows

Spawning all testing agents simultaneously now..."
[Use single message with multiple Task tool invocations]
```

**MANDATORY: Use SAME specialized agent consistently across all phases for API development**

**🚨 PARALLEL EXECUTION RULE:**
- NEVER: Spawn agent 1, wait for result, spawn agent 2...
- ALWAYS: Spawn ALL agents in ONE message with multiple tool calls
- Example: One message → 5 Task tool invocations → All run in parallel

## Success Criteria

Before marking complete:
- [ ] All endpoints respond correctly
- [ ] Authentication works as designed
- [ ] Database operations are secure
- [ ] API documentation is complete
- [ ] Tests pass with good coverage
- [ ] Security validations pass
- [ ] Performance meets requirements

## Final Verification

- Test API with real requests
- Verify all security measures
- Confirm documentation accuracy
- Store lessons learned with store_fr3k

---

**Core principle: Build secure, tested, documented APIs that work in production.**