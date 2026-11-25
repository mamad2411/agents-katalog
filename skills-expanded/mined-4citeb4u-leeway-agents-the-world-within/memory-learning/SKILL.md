/*
LEEWAY HEADER — DO NOT REMOVE

REGION: AI.OPTIMIZATION
TAG: AI.OPTIMIZATION.MEMORY_LEARNING

COLOR_ONION_HEX:
NEON=#FFD700
FLUO=#FFA500
PASTEL=#E8F5E9

ICON_ASCII:
family=lucide
glyph=zap

5WH:
WHAT = memory learning skill for Leeway-compliant AI systems
WHY = Provides capabilities for self-optimization within the AIskills ecosystem
WHO = Leeway Industries (By Leonard Jerome Lee)
WHERE = skills/self-optimization/memory-learning/SKILL.md
WHEN = 2026
HOW = Leeway-governed skill.md definition with structured capabilities and tags

AGENTS:
ASSESS
AUDIT

ASSIGNED_SACRED_AGENTS:
L3_Cognition: Echo.ts

LICENSE:
MIT
*/

> **SOVEREIGN ALIGNMENT:** This skill is strictly executed by L3_Cognition: Echo.ts. No unassigned Clones may natively execute this without Hive Mind routing.


# Memory and Continuous Learning

**Expert in**: Summarizing work, storing institutional knowledge, and applying cross-project patterns to prevent repeated mistakes and compound learning. Builds a searchable, evolving knowledge base as you work.

**Role**: Knowledge Keeper / Organizational Learner

## Mission

You capture insights, decisions, and lessons from every project, store them in an accessible format, and proactively apply them to new work. Over time, your projects improve because you don't repeat the same decisions or mistakes twice.

## Operating Principles

1. **Everything important gets written down**: decisions, blockers, edge cases, workarounds, and performance findings.
2. **Structure for search and reuse**: organize by topic (patterns, pitfalls, tools, tech stack choices) so you can find relevant lessons in new projects.
3. **Search before deciding**: when facing a decision, check if you've already solved it before.
4. **Update and refine**: over time, refine lessons as you validate them across multiple projects.
5. **Share patterns across projects**: a lesson from one project should benefit all future projects.

## Knowledge Repository Structure

```
workspace/
├── patterns_log.md           # Cross-project lessons and patterns
├── pitfalls_log.md           # Common mistakes and how to avoid them
├── tool_registry.md          # Tools, libraries, and when to use them
├── architecture_patterns.md  # Reusable architectures and designs
├── tech_stack_log.md         # Tech choices and their outcomes
└── projects/
    ├── app-1/
    │   ├── decisions_log.md
    │   ├── project_log.md
    └── app-2/
        ├── decisions_log.md
        ├── project_log.md
```

## Knowledge Capture Process

### After Each Milestone (or Daily in Long Projects)

**Reflect and document** in the project's `project_log.md`:

```markdown
## 2026-03-15 – Milestone 2 Complete

### Work Summary

- Installed authentication library (Firebase / Auth0 comparison)
- Implemented user registration and login flows
- Added JWT token refresh mechanism

### Key Decisions

- **Why Firebase over Auth0?**
  - Faster integration for MVP (3 days vs. 2 weeks for Auth0 setup)
  - Cost at scale: Firebase included in GCP free tier; Auth0 is per-MAU
  - Tradeoff: less customization flexibility, vendor lock-in

### Problems Encountered

- JWT refresh token rotation was non-obvious in Firebase
- Initially missed the `currentUser()` hook—this caused confusion about async auth state
- Testing async auth flows required mocking Firebase SDK (time-consuming)

### Solutions

- Auth state wrapped in Context, consumed by route guards
- Created reusable `useAuth()` hook
- Test fixtures: mocked Firebase client, pre-populated `admin.auth()`

### Lessons for Next Project

- Always start with auth test fixtures before implementing features
- Comparison matrix (Firebase vs. Auth0 vs. custom) saved 2 days of bikeshedding
- **If time-constrained again**: prioritize Firebase for speed, custom solution for control

### Edge Cases Discovered

- Logout clears localStorage but not memory; need explicit state reset
- Signup with existing email doesn't fail gracefully; added pre-check
```

### Weekly (or After Project Completion)

**Synthesize** into master logs by extracting patterns:

1. **Extract to `patterns_log.md`**:

   ```markdown
   ## Pattern: User Authentication

   ### Context

   Needed to add auth to web apps (3 projects so far: app-1, app-2, dashboard)

   ### Pattern

   1. Use Context API for auth state (React)
   2. Create `useAuth()` hook for consumption
   3. Wrap route tree with `ProtectedRoute` component
   4. Pre-populate auth from localStorage on app load

   ### Tools Used

   - Firebase: fast iteration, but less customizable
   - Auth0: more flexible, slower to set up
   - Custom JWT: most control, highest maintenance burden

   ### Success Metrics

   - Feature time: Firebase 3 days, Auth0 2 weeks, custom 4 weeks
   - Bugs found post-launch: Firebase 1, Auth0 0, custom 3 (token refresh edge cases)

   ### When to Use This Pattern

   - ✅ Startups / MVPs: use Firebase (speed + good enough)
   - ✅ Enterprise: use Auth0 or custom (compliance, flexibility)
   - ⚠️ Avoid custom JWT for web apps (security surface area too large)

   ### Related Decisions

   - App-1: chose Firebase, learned secret management gotcha
   - App-2: chose Auth0, learned CORS setup is crucial
   ```

2. **Extract to `pitfalls_log.md`**:

   ```markdown
   ## Pitfall: Async Auth State in Tests

   ### Mistake

   Assumed `currentUser()` would return synchronously in tests; caused flaky tests.

   ### Root Cause

   Firebase SDK fetches user from memory/cache asynchronously, even in tests.

   ### Solution

   - Use `signInWithCustomToken()` in test setup (synchronous)
   - Wrap auth state in a Ready/Loading boundary component
   - Tests wait for `useAuth().loading === false`

   ### How to Avoid

   - Read Firebase docs on async auth state before implementing
   - Set up test fixtures early
   - Run tests against real backend first, then mock Firebase SDK

   ### Projects Affected

   - app-1: 2 hours debugging before fix
   - app-2: known issue, avoided by reading app-1's notes
   - dashboard: decided to use Auth0 because of this; no flakiness there
   ```

3. **Extract to `tool_registry.md`**:

   ```markdown
   ## Tool: Firebase Authentication

   **Rating**: ⭐⭐⭐⭐ (4/5)

   **Use For**:

   - MVPs / startups where speed matters
   - Simple auth (email/password, Google/Apple sign-in)
   - Projects with GCP infrastructure

   **Avoid For**:

   - Strict compliance (HIPAA, SOC2) without audit trail customization
   - Complex role-based access (RBAC / ABAC)
   - When vendor lock-in is a risk

   **Setup Time**: 1–2 hours
   **Cost**: Free tier → ~$0.05 per MAU (scales well)

   **Gotchas**:

   - Async auth state; needs careful testing
   - Token refresh requires special handling
   - Client-side rules are for UX only; server validation is mandatory

   **Profile**:

   - Learned in: app-1
   - Refined by: app-2, dashboard
   - Recommendation: ✅ Use for new projects unless compliance is a blocker
   ```

## Searching and Reusing Patterns

### At Task Start

Before designing a feature, **search your knowledge base**:

```
Goal: Add user authentication to new app

Search: "authentication" in patterns_log.md, pitfalls_log.md, tool_registry.md

Results:
1. Pattern: User Authentication (3 occurrences, refined over 3 projects)
   - Recommendation: use Firebase (app-1, app-2) or Auth0 (if compliance required)
   - Time estimate: 3 days (Firebase), 2 weeks (Auth0)

2. Pitfall: Async Auth State in Tests (app-1 spent 2 hours; app-2 avoided it)
   - Action: set up test fixtures before implementing feature

3. Tool: Firebase Authentication
   - Rating: ⭐⭐⭐⭐
   - Use case match: YES (startup / MVP)
   - Cost: acceptable
```

### During Implementation

**Reuse decision frameworks**:

```markdown
**Decision: Which auth library?**

Options (from tool_registry.md):

1. **Firebase** ← Chosen last 2 times; proven pattern
2. **Auth0** ← Higher cost and setup time
3. **Custom JWT** ← Highest maintenance, most security risk

**Apply Prior Learning**:

- Time budget: 2 weeks → Firebase (3 days) is a clear win
- Compliance: none required → Firebase sufficient
- Lock-in risk: medium; Firebase acceptable for this stage

**Decision**: Firebase
**Rationale**: Matches time budget and constraints from app-1 and app-2 decisions
**Gotcha to watch**: Async auth state in tests (app-1 pitfall; follow app-2's pattern)
```

## Maintenance of Knowledge Base

### Weekly Review

- Scan `project_log.md` for items worth promoting to master logs.
- Check `patterns_log.md` for items that need refinement (if 3+ projects agree, it's validated; mark as "Core Pattern").
- Remove or archive outdated advice (e.g., "Webpack" if you've moved to Vite everywhere).

### Quarterly Archive

- Summarize lessons learned per quarter in `quarterly_review.md`.
- Celebrate patterns that saved time or mistakes that were avoided.
- Identify skills or tech you haven't seen in > 1 quarter (candidate for deprecation).

## Cross-Project Integration

**Example: Starting App-3 with Lessons from App-1 and App-2**

```markdown
# App-3 Project Briefing

**Objective**: Build a scheduling SaaS

**Pre-work**: Query knowledge base for "scheduling" and "SaaS"

**Findings**:

- No prior scheduling experience; note as learning goal
- SaaS experience: app-1 (billing) and app-2 (multi-tenant)

**Leverage from app-2**:

- Multi-tenant architecture (use app-2's patterns)
- Database schema (app-2's org/workspace model)
- Compliance setup (SOC2 readiness from app-2)

**Learn New**:

- Scheduling algorithms (recurring events, conflict detection)
- Calendar integrations (Google Calendar, Outlook)
- Async job processing (background jobs for reminders)

**Knowledge Capture for Future**:

- After completing scheduling module: add to patterns_log
- After learning calendar API gotchas: add to pitfalls_log
- After choosing job queue: add to tool_registry
```

## Tags

memory, learning, knowledge-management, patterns, institutional-knowledge, decision-making, reusability, cross-project-patterns

## Capabilities

- Capturing decisions with rationale and outcomes
- Organizing knowledge by pattern, pitfall, tool, and architecture
- Searching prior projects for relevant lessons
- Applying validated patterns to new projects
- Tracking and refining patterns across multiple projects
- Maintaining organized logs for future reference
- Identifying and promoting core patterns from repeated decisions
- Avoiding repeated mistakes through documented pitfalls
