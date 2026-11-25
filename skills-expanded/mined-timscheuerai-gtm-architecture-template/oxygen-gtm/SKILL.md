---
name: oxygen-gtm
description: Route a GTM outcome to the correct OXYGEN primitive and the narrower bundled skill that teaches it: Knowledge, Records, Tables, Signals, Messages, Posts, Sequences, Publishing, Workflows, Agents and Observability.
---

# Route the next GTM job

Read [the runtime contract](../../../docs/runtime-contract.md). Use this fallback when no narrower OXYGEN skill already fits. For onboarding use [oxygen-onboarding](../oxygen-onboarding/SKILL.md); for a diagnosis or plan use [oxygen-gtm-consultant](../oxygen-gtm-consultant/SKILL.md).

```sh
oxygen capabilities search "research and qualify target accounts" --json
oxygen commands get "tables create" --json
```

Search by the actual goal, then hydrate the returned command. Provider operations have a separate catalog: `tools search`, then `tools get` for inputs, readiness and the current estimate.

| Job | Native owner / bundled guide |
|---|---|
| Company, ICP, offer, rubric, durable learning | [Knowledge](../oxygen-knowledge/SKILL.md) |
| Borrow a proven play | [Recipes](../oxygen-recipes/SKILL.md) |
| New companies and people, TAM, personas | [Sourcing](../oxygen-sourcing/SKILL.md) |
| Row work: AI, Classify, formula, tool and lookup columns | [Tables](../oxygen-tables/SKILL.md); [kit composition](../../../docs/composition.md) |
| Contact and company data, waterfalls, verification | [Enrichment](../oxygen-enrichment/SKILL.md) |
| Hiring, funding, tech, engagement and network events | [Signals](../oxygen-signals/SKILL.md) |
| Canonical company, person and deal truth | [Records](../oxygen-crm/SKILL.md) |
| Existing-thread replies and direct email | [Unibox / Messages](../oxygen-unibox/SKILL.md) |
| Post drafts and scheduled delivery | [LinkedIn content](../oxygen-linkedin-content/SKILL.md), [Publishing](../oxygen-publishing/SKILL.md) |
| Outreach cadence, enrollment and reply stops | [Sequences](../oxygen-sequencer/SKILL.md) |
| Deterministic triggers, branches, retries, approvals | [Workflows](../oxygen-workflow-authoring/SKILL.md) |
| Your own REST API as tools | [Custom HTTP](../oxygen-custom-http/SKILL.md) |
| Adaptive goals and tool choice | Agents; discover the native goal and thread surface |
| Run failures, provenance and spend | [Diagnostics](../oxygen-diagnostics/SKILL.md) |

Operating loop: confirm the workspace and its Knowledge context, accept the native owner, hydrate one command, preview the smallest scope, show scope, credits and side effects, get approval and a hard ceiling, run on the hosted primitive, then return links, cost and retryable failures. Prefer the kit's existing callables for research, scoring and copy.
