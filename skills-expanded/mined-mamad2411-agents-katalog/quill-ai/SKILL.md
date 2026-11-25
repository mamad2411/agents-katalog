# AGENTS

## ⚠️ HALLUCINATION RISK — Next.js 16

This project uses **Next.js 16**. Most AI training data covers Next.js 13/14/15. Do NOT generate code based on older version assumptions for:

- `middleware.ts` patterns and matchers
- Proxy / rewrites in `next.config.ts`
- `next/headers`, `next/cookies`, async APIs
- API route conventions (`route.ts` App Router only — no `pages/api/`)
- Turbopack-specific behavior
- Metadata / viewport export signatures

Always read the existing files in this repo to understand the actual patterns in use before writing new code.

---

## Regression Guardrails (AI Agent) - Tiered System

Before finishing any coding task, run appropriate quality gates based on task type:

### Tier 1: Critical Production Tasks
**Requirements:** `guardrails:check`, `typecheck`, `lint`, `build`
**Use when:** Production code, security patches, core features, high-impact changes
**Examples:** Authentication flow, payment processing, data migrations

### Tier 2: Quick Development Tasks  
**Requirements:** `guardrails:check`, `typecheck`
**Use when:** Low-risk changes, bug fixes, feature additions, non-critical updates
**Examples:** UI improvements, minor bug fixes, new endpoints

### Tier 3: Experimental Tasks
**Requirements:** `guardrails:check` only
**Use when:** High-risk explorations, new experiments, rapid prototyping
**Examples:** New AI features, architecture experiments, performance optimizations

### Contextual Risk Assessment
```javascript
// AI-assessed task classification
function assessRisk(task) {
  const indicators = {
    production_impact: task.includes('critical', 'production', 'core', 'security'),
    complexity: task.includes('refactor', 'architecture', 'major'),
    urgency: task.includes('hotfix', 'urgent'),
    new_feature: task.includes('new', 'add', 'experimental')
  };
  
  if (indicators.production_impact || indicators.complexity) return 'critical';
  if (indicators.urgency) return 'quick';
  return 'experimental'; // Default to experimental for exploratory work
}
```

Additional non-negotiable rules:

1. Do not modify `node_modules/`.
2. Treat `postcss.config.mjs`, `next.config.ts`, `package.json`, and `src/app/globals.css` as high-risk files; change only when directly required by the task.
3. Keep AI edits narrowly scoped to requested files/feature; avoid opportunistic refactors in unrelated areas.
4. Temporary debug hooks/scripts must be removed before completion.

---

## Builder Behavior (Artifact Discipline)

For app-builder requests in this repository:

1. Always return typed artifact envelopes first (`<quill-artifact>...</quill-artifact>`) before any optional explanation text.
2. Respect builder targets explicitly (`auto`, `page`, `react-app`, `nextjs-bundle`) and do not drift between output formats.
3. Prefer complete runnable outputs over partial snippets for `react-app` and `nextjs-bundle` targets.
4. For `nextjs-bundle`, generate export-first App Router structures (no `pages/api`) and include realistic project files.
5. Preserve active iteration locks (layout/colors/section order/copy) unless user explicitly requests changes.

---

## Chat Backend Guardrails (Anti-Hallucination) - Flexible Module Boundaries

### Primary Module Structure (Recommended)
The chat backend is decomposed into focused modules. Keep this structure when possible:

1. `src/lib/chat/request-utils.ts`
   - Request parsing/validation (`parseChatRequestBody`)
   - Message extraction/normalization (`extractModelMessages`, `extractTextMessages`)
   - Last-user helpers (`summarizeLastUserInput`, `getLastUserParts`)
2. `src/lib/chat/model-selection.ts`
   - Mode typing (`ChatMode`)
   - Daily mode limits (`getDailyLimitForMode`)
   - Provider/model resolution (`resolveModelForMode`)
3. `src/lib/chat/access-gates.ts`
   - Entitlement and quota enforcement (`evaluateChatAccess`)
   - Guest-mode restrictions, paid-tier checks, web search gates
4. `src/lib/chat/policy-runtime.ts`
   - Killer policy/runtime derivation (`evaluatePolicyRuntime`)
   - Permission decisions, sandbox status, `canRunCode`, policy warnings
5. `src/lib/chat/two-pass-builder.ts`
   - Two-pass builder orchestration and persistence path

### When to Bend Module Boundaries (Exceptions)
Direct route edits in `src/app/api/chat/route.ts` are acceptable for:

✅ **Simple corrections**: Typo fixes, single-function bug fixes
- Example: Fix typo in `extractLastUserParts()`
- Example: Add null check to `evaluateAccess()`

✅ **Urgent hotfixes**: Prioritize speed while maintaining core functionality
- Example: Critical security patch that needs immediate deployment
- Example: Production-blocking bug that can't wait for module refactor

✅ **Performance optimizations**: Direct changes in high-traffic areas
- Example: Cache optimization in request parsing
- Example: Database query optimization in policy evaluation

✅ **Experimental endpoints**: Keep in route until stabilized
- Example: New AI model testing endpoint
- Example: Experimental feature endpoint

❌ **Avoid direct route edits for**: Major refactors, complex new features, architectural changes

### Required Workflow for Chat Modifications
1. **Assess task type** using the tiered system above
2. **Read existing architecture** in `route.ts` and relevant modules
3. **Choose appropriate approach**: Use modules or direct route based on task type
4. **Apply quality gates**: Use tiered system (critical/quick/experimental)
5. **Maintain orchestration**: Keep parse -> runtime -> access -> build -> stream pattern

---

## Optional Feature Guides

When users request features beyond the base template, check for available recipes in `.kilocode/recipes/`.

### Available Recipes

| Recipe       | File                                | When to Use                                           |
| ------------ | ----------------------------------- | ----------------------------------------------------- |
| Add Database | `.kilocode/recipes/add-database.md` | When user needs data persistence (users, posts, etc.) |

### How to Use Recipes

1. Read the recipe file when the user requests the feature
2. Follow the step-by-step instructions
3. Update the memory bank after implementing the feature

## Memory Bank Maintenance - Simplified

Track only **significant architecture changes** to reduce manual overhead:

### Required Updates
- **Major architecture changes**: New modules, core refactors, framework changes
- **Critical feature additions**: New system capabilities that change development approach
- **Major API changes**: Breaking changes to external interfaces

### Automated Tools Use
- Use AI assistance for documentation updates
- Leverage templates and pre-generated content
- Automate routine documentation where possible

### Review Frequency
- Monthly reviews of all changes
- Quarterly deep dives and consolidation
- Use AI summaries to identify patterns and evolution

## Production vs Development Speed Decision Matrix

| Business Context | Risk Tolerance | Velocity Priority | Recommended Tier |
|------------------|----------------|------------------|------------------|
| E-commerce checkout | Low | High | Critical |
| Blog feature | Medium | High | Quick |
| Internal tool | High | High | Experimental |
| API endpoint | Medium | Medium | Quick |
| Bug fix (UI) | Low | High | Quick |
| Security patch | Low | Medium | Critical |
| New experiment | High | Medium | Experimental |

## Available Custom Droids

### Security Scanner
- **Purpose**: Vulnerability assessment, dependency audit, security best practices
- **Use Cases**: New features, production deployments, compliance checks
- **Integration**: Automated scanning with `npm audit`, security lint rules
- **Usage**: `task security-scanner "scan new authentication endpoint"`

### Performance Optimizer
- **Purpose**: Bundle analysis, loading optimization, runtime performance tuning
- **Use Cases**: Pre-launch optimization, performance degradation fixes
- **Integration**: Bundle analyzer, Lighthouse, React profiling
- **Usage**: `task performance-optimizer "analyze bundle size for new feature"`

### Documentation Generator
- **Purpose**: Automated technical documentation, API docs, README generation
- **Use Cases**: New features, documentation updates, knowledge management
- **Integration**: JSDoc, OpenAPI, markdown documentation automation
- **Usage**: `task doc-generator "generate API docs for new chat endpoint"`

## Available MCP Servers

### Figma Integration
- **Purpose**: Design-to-code workflow, component generation from Figma designs
- **Features**: Fetch design files, extract components, generate code from designs
- **Usage**: Access via Figma MCP tools when working with design files

## CLI Enhancement: Tiered Quality Gates

### New CLI Options
```bash
quill --tier critical "production auth system"    # Full quality checks
quill --tier quick "bug fix"                    # Basic checks only  
quill --tier experimental "new AI feature"      # Minimal checks
```

### REPL Commands
```
.mode fast|thinking|advanced        # Change AI mode
.tier critical|quick|experimental  # Change quality tier
.clear                             # Clear conversation
.help                              # Show help
```

## Application Examples

### Quick Fix Example
```