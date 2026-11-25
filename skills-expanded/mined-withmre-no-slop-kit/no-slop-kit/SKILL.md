---
name: no-slop-kit
description: Route a task to the relevant No Slop Kit skill without loading unrelated guidance. Use when auditing the kit, choosing its modules, or starting a cross-cutting release review.
---

# No Slop Kit router

Load only the smallest set of modules that covers the task.

| Task | Load |
|---|---|
| Published text, README, email or site copy | `claude-home/skills/deslop/SKILL.md` |
| UI or visual review | `claude-home/skills/ui-design/SKILL.md` |
| Auth, data, API, payment, webhook, upload or secret | `claude-home/skills/security/SKILL.md` |
| Data fetching, queries, external API, errors, logging, cache or backup | `claude-home/skills/reliability/SKILL.md` |
| Docker, Compose, Kubernetes, image, network, port or runtime secret | `claude-home/skills/container-security/SKILL.md` |
| Public release, high traffic event or broad production audit | `claude-home/skills/production-readiness/SKILL.md` |
| New repository setup | `claude-home/skills/project-setup/SKILL.md` |

For a broad audit, the production-readiness skill selects the additional modules and uses its shared P0/P1/P2 report format.
