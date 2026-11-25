---
name: agent-architect
description: Full-Stack Agent Architect for system instructions, tech stacks, and infrastructure blueprints.
category: autonomous-ai-agents
---

# Full-Stack Agent Architect

## Description
Designs system instructions, tech stack architectures, and asset blueprints (CRMs, databases) for AI agents and automated workflows.

## Features
- PAL-based prompt expansion
- Tech stack infrastructure design (Mermaid.js)
- Asset blueprinting (CRM schemas, database fields)
- Project documentation generation
- ROSTR framework compliance & n8n execution handoff (`references/rostr-n8n-handoff.md`)

## Instructions
1. Use the PAL (Parse, Ambiguity Scan, Latent Intent, Expand, Compile) framework for all requests.
2. Output artifacts in XML blocks: `<architecture_diagram>`, `<tech_stack_recommendation>`, `<asset_blueprint>`, `<agent_artifact>`, `<design_rationale>`.
3. Ground platform choices in 2026 best practices.

## ROSTR Full-Stack SaaS Build Pattern (Proven)

When building a ROSTR-based SaaS platform, follow this exact sequence:

### 1. Backend First — FastAPI + rostr-core + SQLite
```python
# backend/main.py
from fastapi import FastAPI
from rostr.pal import PALCompiler
from rostr.npao import NPAO
from rostr.ragdal import RAGDAL
# Wire all 4 components as REST endpoints
# Use SQLite for persistent state (agents, decisions, learnings, knowledge)
app = FastAPI()
# ... see references/backend-verification-pattern.md for full template
```

### 2. API Client Pattern — typed fetch wrapper
```typescript
// src/lib/api.ts
const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8420';
export const rostr = {
  compile: (input: string) => api<CompileResult>('POST', '/pal/compile', { input }),
  listAgents: () => api<Agent[]>('GET', '/hub/agents'),
  // ... every endpoint wrapped with typed return
};
```

### 3. Frontend — Next.js with 'use client' pages
Every page imports `{ rostr } from '@/lib/api'` and uses `useState` + `useEffect` to fetch live data. Zero mock arrays. Every page has loading, empty, and error states.

### 4. Taste-Skill Design (apply LAST)
Build functional frontend first. Once all API calls work and the build passes, THEN apply taste-skill design (Double-Bezel, Framer Motion, Geist font). Design-first with mock data will be rejected.

### 5. Verification
Run the 19-test API verification script (see `references/backend-verification-pattern.md`) before deploying. Frontend build must pass `npm run build` with zero type errors.

### Sequence Summary
```
rostr-core (Python package)
    ↓ pip install -e .
FastAPI backend (wraps rostr-core, SQLite)
    ↓ verify 19/19 endpoints
Next.js frontend (API client pattern, working but bare)
    ↓ npm run build → zero errors
Taste-skill redesign (Double-Bezel, Framer Motion, Geist)
    ↓ npm run build → still zero errors
Deploy: backend → Railway/Render, frontend → Vercel
```

## Pitfalls

### Self-Improving Agent Learning Retrieval
When building self-improving agents that learn from past executions:
- **Don't rely on simple keyword matching** for learning retrieval. If learning A was logged with context "multi-agent delegation gemini API" and you search for "Create new skills", keyword overlap may be zero even though the rate-limit insight applies.
- **Use semantic similarity or broader pattern matching** instead. Options:
  - TF-IDF cosine similarity on context strings
  - Embedding-based retrieval (sentence-transformers)
  - Tag-based matching (tag learnings with categories like "rate-limits", "disk-space", "parallel-execution")
  - Hierarchical filtering (domain → task-type → specific patterns)
- **Test retrieval explicitly** by logging a learning and immediately querying for it with a semantically-related but lexically-different prompt.
- **Implementation pattern** (proven in ROSTR):
  ```python
  # LearningSystem with semantic retrieval
  learning.log_learning(
      context="Creating multiple skills in parallel using Gemini",
      insight="Gemini API parallel delegation hits rate limits (HTTP 429)",
      outcome="failure",
      source="agent_forge"
  )
  
  # Later, retrieve with broader query
  learnings = learning.retrieve_learnings("skill creation Gemini")
  # This should match via: domain overlap ("skill", "Gemini") + outcome weighting
  ```

### Sibling Sub-Agent File Conflicts (Parallel Delegation)
When dispatching multiple `delegate_task` calls in parallel that target the same project directory:

### Taste-Skill Design Integration (Sequence Matters)
When applying taste-skill design (design-taste-frontend-v1, high-end-visual-design) to an existing functional dashboard:
- **NEVER design-first, API-second.** Building a beautiful mock-data shell then trying to wire real API calls afterward leads to brittle, broken pages. Build the functional API-connected frontend first, verify the build passes, THEN apply taste-skill design.
- **Sub-agent isolation:** When delegating a taste-skill redesign, the sub-agent will see taste directives demanding `DoubleBezel`, `framer-motion`, `@phosphor-icons/react`, and specific className patterns. If these aren't in the component library yet, the sub-agent will import them from nowhere and the build will fail. **Always provide the sub-agent with a `context` field listing exactly which components exist** (e.g., "GlassCard exists at @/components/glass-card and accepts { children, className }. DoubleBezel does NOT exist yet. Do NOT import it.").
- **Post-redesign fix pattern:** After a taste-skill sub-agent finishes, expect type errors. The most common: `Property 'hover' does not exist`, `Module has no exported member 'DoubleBezel'`, `Cannot find module 'framer-motion'`. Fix by (a) removing unsupported props, (b) adding missing exports to components, (c) running `npm install` if package.json was updated.
- **Build gate:** After ANY taste-skill sub-agent completes, run `npm run build` before declaring done. If build fails, fix type errors one by one (read each error, patch the file, rebuild). Never deploy with build failures.
- **Design params reference for sub-agents:** When dispatching a taste-skill redesign, include these exact directives in the task context: DESIGN_VARIANCE=8, MOTION_INTENSITY=6, VISUAL_DENSITY=4, VIBE=Ethereal Glass (#050505, radial mesh, glass cards), LAYOUT=Asymmetrical Bento (fractional grid units, col-span variations), FONT=Geist+JetBrains Mono (Inter BANNED), ACCENT=cyan only (NO purple), CARDS=Double-Bezel nested, MOTION=spring physics (stiffness:100,damping:20), ICONS=@phosphor-icons/react (NOT lucide), BANNED=emojis,centered heroes,3-col grids,h-screen,scroll listeners,backdrop-blur on non-fixed.
- **Race condition:** Two sub-agents can write to the same file simultaneously. The last writer wins, potentially breaking imports (e.g., one agent writes `DoubleBezel` component, the other writes a page that doesn't know `DoubleBezel` exists).
- **Mitigation:** NEVER dispatch parallel sub-agents that both have write access to the same file tree. Serialize them instead, or give each a dedicated subdirectory.
- **Fix pattern when conflicts occur:**
  1. Run `npm run build` (or equivalent) to find type/import errors
  2. Read each broken file to understand what the sibling wrote
  3. Rewrite the page cleanly, importing from components that actually exist
  4. Rebuild and verify zero errors
- **Detection:** Build errors like `Module has no exported member 'DoubleBezel'` or `Property 'hover' does not exist` are almost always sibling-agent conflicts.
- **Prevention for `delegate_task`:** When multiple tasks touch the same source tree, provide each with explicit `context` listing which files NOT to touch. Example: `"You are redesigning ONLY the components folder. Do NOT modify any page.tsx files in src/app/. Those are handled by a parallel agent."`
When dispatching parallel sub-agents (e.g., 3 agents building skills for Life/Business/Health):
- Cloud APIs (Gemini, OpenAI) often rate-limit parallel requests from the same account
- **Mitigation:** Cap `max_parallel_tasks` to 1 when agent manifests indicate past rate-limit failures, OR use local models (Ollama, vLLM) for high-volume generation tasks
- **Signal:** HTTP 429 errors with "Quota exceeded for metric: generativelanguage.googleapis"
- **Self-improving response**: Agent manifests should auto-adjust:
  ```yaml
  model: local  # switched from gemini-1.5-pro due to rate limits
  max_parallel_tasks: 1  # reduced from 3 due to past 429s
  learning_context:
    applied_learnings: 3
    failure_patterns_avoided: 1
  ```

### Dashboard Architecture: Never Ship Mock Data
When building dashboards, monitoring panels, or admin UIs:
- **The user expects real SaaS, not static shells.** A dashboard with hardcoded mock data (even beautiful, taste-skill-designed ones) will be rejected. Always pair a frontend with a working backend API — even if minimal.
- **Backend-first pattern:** Before finalizing any dashboard, stand up a FastAPI (or equivalent) server wrapping the core logic. The dashboard should call `fetch()` to real endpoints, not import mock JSON.
- **Verification:** Run an automated API test script that hits all endpoints and reports PASS/FAIL counts. See `references/backend-verification-pattern.md` for the canonical 19-test template.
- **Database bridging:** When using SQLite as backing store, tools/capabilities/phases fields are often stored as comma-separated strings (not JSON arrays). Always write a `_parse_list()` utility that handles both `"web_search,file_system:read"` and `'["web_search"]'` formats. See references for the implementation.
- **User signal:** If the user asks "how does it work" or "what is the SaaS functionality" or says "no mock data", they are telling you the frontend-only approach failed. Switch immediately to backend-first.

### Gemini ADK Integration
When integrating with Google's Agent Development Kit:
- **Package name**: `google-adk` (not `google-genai` alone)
- **Agent wrapping pattern**: Create `ROSTRGeminiAgent` class that wraps ROSTR YAML configs into ADK `Agent` objects
- **Tool mapping**: Convert ROSTR capabilities to ADK `Tool.from_function()` objects
- **Graceful degradation**: If ADK unavailable, still load agent configs and show availability status
- **See**: `references/gemini-adk-integration.md` for full implementation
