---
name: gstack
description: Route broad GStack requests to Codex-native planning, review, QA, browser, debugging, shipping, diagram, spec, and GBrain setup skills in this port.
---

# GStack

Use this skill when the user asks for GStack generally, asks which GStack skill fits, or gives a broad planning/review/QA/shipping/debugging request.

This port was reconciled against `garrytan/gstack` at commit
`94993f74012782fd94416dd44b8314f6363a13a4`.

## Routing

- Product or project framing: `office-hours`
- Implementation plan review: `plan-eng-review`
- Founder or strategy review: `plan-ceo-review`
- Design plan review: `plan-design-review`
- Project-aware design execution and quality gates: `design-quality`
- Developer-experience plan review: `plan-devex-review`
- Code review before landing: `review`
- QA or verification: `qa` or `qa-only`
- Browser-driven exploration: `browse`
- Reproduce a bug and check its cause directly. The local `investigate` skill remains available on explicit request.
- Compare model or prompt changes: `eval-plan`
- Animate an approved frame: `design-motion`
- Shipping and release: `ship`, `document-release`, `setup-deploy`, or `land-and-deploy`
- Security review: `cso`
- Health check: `health`
- Diagramming: `diagram`
- Issue or implementation brief: `spec`
- GBrain setup or sync: `setup-gbrain`, `sync-gbrain`, or `gbrain-advisor`
- Skillpack upgrade: `gstack-upgrade`
- Impeccable capability drift: `gstack-upgrade` with the `impeccable` map

## Codex Adaptation

Codex already has explicit tool and skill discovery, so this router is a short dispatch layer rather than a shell preamble. It does not run telemetry, first-run activation scripts, or Claude-specific skill path checks.

## Guardrails

- Route to the narrowest skill that fits.
- If a request is already clearly inside another skill, use that skill directly.
- Do not claim upstream runtime support unless the corresponding Codex tools or local commands are available.
