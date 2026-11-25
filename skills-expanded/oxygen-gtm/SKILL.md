---
name: oxygen-gtm
description: Route a GTM outcome to the correct OXYGEN primitive and select the narrower bundled skill for hosted execution.
---

# Route the next GTM job

Read [the runtime contract](../../../docs/runtime-contract.md). Use this fallback when no narrower OXYGEN skill already fits.

```sh
oxygen capabilities search "research and qualify target accounts" --json
oxygen commands get "tables create" --json
```

Search by the actual goal, then hydrate the returned command. Provider operations have a separate catalog: bounded `tools search`, then `tools get` for the selected operation's inputs, readiness, effects and current estimate.

| Job | Native owner / bundled guide |
|---|---|
| Company, ICP, offer, rubric, durable learning | [Knowledge](../oxygen-knowledge/SKILL.md) |
| Choose a repeatable business play | [Recipes](../oxygen-recipes/SKILL.md) |
| Working account lists, AI/tool/waterfall columns | Tables; [kit composition](../../../docs/composition.md) |
| Canonical company/person/deal truth | Records; inspect promotion and field ownership |
| Existing-thread replies and direct email | [Unibox / Messages](../oxygen-unibox/SKILL.md) |
| Content, engagement and scheduled posts | [LinkedIn marketing](../oxygen-linkedin-marketing/SKILL.md); Posts, Signals and Publishing |
| Outreach cadence, enrollment and reply stops | [Sequences](../oxygen-sequencer/SKILL.md) |
| Deterministic triggers, branches and retries | [Workflows](../oxygen-workflow-authoring/SKILL.md) |
| Adaptive goals and tool choice | Agents; discover the native goal/thread/checkpoint surface |
| Run failures, provenance and spend | [Diagnostics](../oxygen-diagnostics/SKILL.md) |

In Tables, use a formula for deterministic transforms, AI for reasoning, a tool column for one provider operation and a native waterfall for ordered fallback. Cross-table links remain Tables relations; they do not automatically create CRM objects. Shared Tags label native objects, and Dashboards summarize their data.

Prefer the kit's existing callables for research/scoring/copy. Inspect one mapped row and its estimate before live work. Long-running production work belongs in durable OXYGEN runs. Return object links, completed scope, cost evidence and held work.
