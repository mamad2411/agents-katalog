---
name: onflou-react-conv-code
description: Use when implementing, reviewing, refactoring, or planning React frontend code for Onflou projects and the user asks about code convention, component structure, styling, API integration, state/effect usage, accessibility, security, or frontend quality standards. Loads the Onflou React convention resources from MCP before changing or judging frontend code.
---

# Purpose

Apply Onflou React frontend code conventions consistently before frontend implementation, review, refactor, or planning.

# MCP-First Rule

Read convention resources from `agent_mcp` first. Local files are fallback/runtime mirrors only.

# Required Knowledge

Read only the resources relevant to the task:

- React code convention: `ai-workspace/70-knowledge/company/onflou/internal/REACT_FRONT_STANDARD_v1.0/REACT FRONT STANDARD (v1.0)/Policy/코드 컨벤션.md`
- React component rules: `ai-workspace/70-knowledge/company/onflou/internal/REACT_FRONT_STANDARD_v1.0/REACT FRONT STANDARD (v1.0)/Guide/컴포넌트 규칙.md`
- React style guide: `ai-workspace/70-knowledge/company/onflou/internal/REACT_FRONT_STANDARD_v1.0/REACT FRONT STANDARD (v1.0)/Guide/스타일 가이드.md`
- React API guide: `ai-workspace/70-knowledge/company/onflou/internal/REACT_FRONT_STANDARD_v1.0/REACT FRONT STANDARD (v1.0)/Guide/API 통신 가이드 (ON Front Standard).md`
- React API error policy: `ai-workspace/70-knowledge/company/onflou/internal/REACT_FRONT_STANDARD_v1.0/REACT FRONT STANDARD (v1.0)/Policy/API/에러 처리 정책.md`
- React state guide: `ai-workspace/70-knowledge/company/onflou/internal/REACT_FRONT_STANDARD_v1.0/REACT FRONT STANDARD (v1.0)/Guide/상태 관리 가이드.md`
- React routing guide: `ai-workspace/70-knowledge/company/onflou/internal/REACT_FRONT_STANDARD_v1.0/REACT FRONT STANDARD (v1.0)/Guide/라우팅 가이드.md`
- React accessibility minimum: `ai-workspace/70-knowledge/company/onflou/internal/REACT_FRONT_STANDARD_v1.0/REACT FRONT STANDARD (v1.0)/Policy/접근성 최소 기준.md`
- React security policy: `ai-workspace/70-knowledge/company/onflou/internal/REACT_FRONT_STANDARD_v1.0/REACT FRONT STANDARD (v1.0)/Policy/보안 정책.md`

# Workflow

1. Identify whether the task is implementation, review, refactor, or planning.
2. Read the smallest relevant MCP convention resources before touching frontend code.
3. Check the existing project pattern and prefer local patterns when they do not conflict with Onflou conventions.
4. Keep pages thin: page files compose UI, while business logic goes into hooks/services.
5. Use function components only and named exports only.
6. Keep component files focused: one component per file where practical, split near 300 lines, separate UI from domain logic.
7. Keep event handlers as `handleVerb` and props/events as `onVerb`; boolean names use `is`, `has`, `can`, or `should`.
8. Use `useEffect` only for synchronization, not data derivation. Use memoized derived values when needed.
9. Put API calls in services/hooks, not directly in page components.
10. Follow styling rules: Tailwind/theme tokens first, mobile-first, avoid arbitrary inline styles except dynamic calculated values.
11. Verify accessibility, error/loading/empty states, and security-sensitive inputs before completion.
12. Document any convention conflict or missing source in MCP-backed shared state when it affects the decision.

# Quick Checks

- No default export.
- No page-level business logic.
- No data derivation through `useEffect` plus state.
- Stable list keys; no index key for dynamic lists.
- Theme tokens instead of arbitrary hex values.
- API errors handled through the project pattern.
- No production `console.log`.

# Output

- Frontend implementation/review guidance aligned with Onflou React conventions.
- Exact convention resources consulted.
- Verification notes and remaining risk.
