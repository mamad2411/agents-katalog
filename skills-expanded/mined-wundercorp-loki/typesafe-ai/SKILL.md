---
name: typesafe-ai
license: MIT
description: Build with TypeSafe AI and Jev for typed semantic decisions, probabilities, routing, ranking, verification, extraction, and other bounded judgments in software workflows.
---
# TypeSafe AI / Jev

Use TypeSafe when software needs semantic judgment but code should retain control of the workflow. Jev is TypeSafe's flagship System One model: it evaluates application state against typed questions and returns structured answers and probabilities instead of generated prose.

## Read the live docs

The live TypeSafe documentation is the source of truth for current API contracts, models, limits, SDK behavior, and examples.

- Documentation index: https://docs.typesafe.ai/llms.txt
- Introduction: https://docs.typesafe.ai/introduction
- HTTP API: https://docs.typesafe.ai/api
- Upstream TypeSafe skill: https://github.com/typesafe-ai/skills/blob/main/skills/typesafe-ai/SKILL.md
- Raw upstream skill: https://raw.githubusercontent.com/typesafe-ai/skills/main/skills/typesafe-ai/SKILL.md

For version-sensitive work, read the relevant live docs before changing an integration.

## Loki integration

When Loki exposes `typesafe_ask`, prefer it for Jev calls rather than reimplementing HTTP requests. The tool uses `TYPESAFE_API_KEY`, calls the System One endpoint, and defaults to `jev-latest`. Configure the key with `loki setup jev` or Settings -> Keys -> Tools.

Keep the user's normal chat model for writing, open-ended reasoning, retrieval, code execution, and tool orchestration. Use Jev for bounded semantic judgments that application code can consume directly.

### Jev Auto model routing

When `smart_model_routing.enabled` is true, Loki uses Jev once at the start of a new root session to choose among a bounded shortlist from the already-selected gateway. Routing must never cross provider/gateway boundaries, expose provider credentials, or send conversation history to TypeSafe. Prefer the least expensive candidate that is sufficiently capable for the first task, honor vision/tool/context requirements, require the configured confidence threshold, then keep the chosen model sticky for the session so prompt-cache prefixes remain reusable. Explicit user model changes always take precedence.

## Choose the right primitive

- **Choice**: select one option from a defined set; preserve the returned probability distribution and confidence.
- **Noul**: estimate whether a condition holds; the `noul` value is the probability of yes, so do not reinterpret 0.5 as "medium intensity."
- **Score**: evaluate an ordered described dimension; preserve score, per-level probabilities, legend, and confidence.

TypeSafe accepts state as a string, object, or array. Questions can share the same state and are evaluated independently, so batch independent questions together when possible. Give each question enough relevant state, use one narrow judgment per question, and keep exact rules, calculations, permissions, and final actions in ordinary code.

Do not discard probabilities merely because a top answer exists. Let application policy decide thresholds, escalation, retries, or human review based on the user's consequences and domain.

## External installation

Loki bundles this skill, so Loki users do not need another installation step. For another coding agent, use one TypeSafe-supported installation method:

```bash
# Claude Code
claude plugin marketplace add typesafe-ai/skills
claude plugin install typesafe@typesafe-ai
```

or:

```bash
# Other agents
npx skills add typesafe-ai/skills --skill typesafe-ai
```

Choose the target agent when prompted.

## Security

Keep `TYPESAFE_API_KEY` server-side and out of prompts, logs, source files, generated client code, and error bodies. Never ask Jev to fetch secrets or external resources; provide only the state required for the judgment.
