---
name: gsp-orchestrator
description: "Use when a request needs routing across this Game Superpowers collection for build, audit, repair, or polish work."
---
# Using Game Superpowers

Collection entrypoint. Classify the request, then route explicitly.

## Classification

- **Build** — new project, prototype, feature, vertical slice
- **Audit** — diagnosis, read-only review, risk or UX review
- **Repair** — targeted fixes after diagnosis
- **Polish** — working game, better feel / UX / feedback / quality

Project state:
- `greenfield`
- `prelaunch`
- `shipped`
- `live-risky`

## Output strategy

Choose one before invoking downstream skills:
- **inline** (default) — keep findings and plans in conversation; do not write `docs/`.
- **minimal** — persist only the small set of files needed for cross-session continuity.
- **full** — write all requested docs artifacts.

Default to **inline** unless the user explicitly wants docs or the project clearly needs them. This overrides downstream defaults.

## Routing

### Build
- `gsp-concept-brainstorm` when fantasy or goals are unclear, and by default for one-prompt generation, showcase builds, benchmark runs, or archetype-led requests such as `runner`, `platformer`, `survivor`, `shooter`, `breakout`, `fps`, `dungeon crawler`, or `arena`
- `gsp-scope-profile`
- `gsp-build-strategy`
- `gsp-super-build`

Add as needed:
- `gsp-douyin-h5` for explicit Douyin-style portrait H5 delivery
- `gsp-ux-flow-designer`, `gsp-feedback-design`
- `gsp-loop-bootstrap`, `gsp-mechanics-systems-design`
- `gsp-build-review`, `gsp-subagent-build-loop`
- `gsp-web-2d-specialist`, `gsp-web-3d-specialist`
- `gsp-polished-prototype`, `gsp-production-feature`

### Audit
- `gsp-project-state-assessment`
- `gsp-project-audit`
- `gsp-audit-scorecard`
- `gsp-repair-roadmap`

Add the matching audit skills:
- `gsp-ux-flow-audit`, `gsp-hud-readability-audit`
- `gsp-feedback-audit`, `gsp-audio-feedback-audit`, `gsp-feel-audit`
- `gsp-mechanics-systems-audit`, `gsp-scope-completeness-audit`
- `gsp-production-readiness-audit`, `gsp-architecture-maintainability-audit`
- `gsp-live-risk-audit` when `project-state == shipped` or `project-state == live-risky`

### Repair
- `gsp-repair-roadmap`
- `gsp-scope-guard`
- `gsp-implementation-plan`
- `gsp-production-code` when quality target >= polished-prototype
- `gsp-playability-verifier`
- `gsp-live-patch` when `project-state == shipped` or `project-state == live-risky`

### Polish
- `gsp-hud-feedback-polish`
- `gsp-feedback-design`
- `gsp-screenshot-critic`
- `gsp-playability-verifier`
- `gsp-audio-feedback-audit`
- `gsp-feel-audit`

### Trigger examples
- Requests like `做一个 Douyin H5 Interactive 作品`, `抖音互动作品`, `抖音互动空间`, `抖音互动H5`, `竖屏 H5 互动页`, or `平台只接受 H5，要先定框架、文件结构和适配方式` should strongly bias toward `gsp-douyin-h5`.
- If the same request also includes real-time browser gameplay, add `gsp-web-2d-specialist` after the platform shell and route are locked.
- Requests that explicitly ask for `requirements/spec/design/tasks`, `OpenSpec`, `spec-driven`, or durable repo-native planning artifacts should route through `gsp-spec-driven-planning`.

## Spec-driven overlay
- `gsp-spec-driven-planning` is an optional planning layer, not a replacement for Build, Audit, Repair, or Polish.
- Use it when the user wants durable change artifacts in the target repo.
- Keep the normal track classification, then add the spec-driven layer on top where it helps.

## Rules
- Classify before implementation and prefer specialized skills over ad hoc reasoning.
- Keep the quality target explicit: `first-playable`, `polished-prototype`, `production-feature`, or `live-patch`.
- For live or risky projects, prefer audit-first and surgical changes.
- For browser games, lock spatial model, camera/view model, control grammar, obstacle grammar, and first-30-seconds promise before coding.
- Prefer a builder + reviewer + verifier loop when the host supports subagents and the user wants maximum result quality; parallelize only across disjoint ownership zones.
- Require fresh runtime verification before claiming a benchmark or showcase build is complete.
- For cross-project reference or benchmarking, audit the reference project first, then apply the extracted patterns to the target via Repair or Build.
- Do not force spec-driven files when the user only wants inline planning.

## Output expectation

At the start, state the selected track, current project state, output strategy, and the next 2-5 Game Superpowers skills.
