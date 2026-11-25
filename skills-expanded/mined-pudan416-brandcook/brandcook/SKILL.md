---
name: brandcook
description: "Cook raw brandbooks into agent-ready skills. Use when a user wants to convert brand guidelines, a Figma library, PDF, presentation, website, asset archive, interview, or loose identity system into a reusable brand-specific Agent Skill, update or audit one, or prepare a brand skill for presentations, documents, websites, social, posters, covers, product surfaces, or image generation. Produces a verified Brand Core and, for visual consumers, an executable Creative Application Kit with assets, art direction, generation recipes, content preservation, visual evals, and honest production status. Do not use merely to apply an already-installed brand skill to one artifact, create a logo or moodboard, or build a UI component library."
license: Apache-2.0
---

# BrandCook

Cook raw brandbooks into brand-specific skills that another AI agent can apply, audit, and update without reconstructing the brand on every run. Keep the master skill brand-agnostic.

Use Python 3.10+ for the bundled scaffolding and validation scripts. Source inspection and visual rendering tools are optional and environment-dependent.

## Output contract

Produce two explicitly separated layers:

1. **Brand Core** — verified constants, rules, source authority, decisions, assets, anti-patterns, review checks, provenance, and stable consumer interfaces.
2. **Creative Application Kit** — an executable production layer for scoped visual consumers: art direction, native brand metaphors, composition patterns, generation recipes, surface adapters, content lock, internal concept selection, render review, and production-readiness checks.

Operational creative directions must never be presented as approved brand truth. Every nontrivial creative direction carries `origin`, `evidence`, `approval`, `confidence`, and `canonical` metadata.

Do not silently embed a presentation, website, image, or document renderer. The kit instructs downstream artifact workflows and exposes resolvable inputs; the downstream workflow still owns the output format.

## Select the mode

- `rules-only` — Brand Core only, for audits, integrations, reference packages, or consumers that need verified rules without visual production guidance.
- `production-ready` — Brand Core plus Creative Application Kit, for applying a brand to presentations, documents, websites, social, posters, covers, product surfaces, imagery, motion, or similar visual work.

Default to `production-ready` when the user asks for a skill “for applying the brand,” design, presentations, image generation, or another visual consumer. Choose `rules-only` when the user asks only for extraction, audit, lookup, or machine-readable integration. Record the selected mode and scoped surfaces in `version.json` and `sources.json`.

## Choose the operation

1. `create` — build a new brand skill from available guidance;
2. `update` — synchronize an existing brand skill with newer or corrected sources;
3. `extend` — add a domain, surface, market, language, asset family, or review capability;
4. `migrate` — normalize an older brand skill to the current architecture without changing approved Brand Core behavior;
5. `audit` — inspect a brand skill or produced artifact for unsupported claims, stale assets, broken contracts, genericity, semantic drift, or incomplete production evidence.

For `update`, `extend`, and `migrate`, preserve the folder name, frontmatter `name`, stable semantic aliases, original provenance, and unaffected Brand Core behavior.

## Decision model

Describe every nontrivial rule, token, asset, exception, metaphor, recipe, and surface pattern independently:

- `origin`: `source` | `inherited` | `operational` | `new`;
- `evidence`: `direct` | `repeated` | `derived` | `none`;
- `approval`: `proposed` | `review` | `approved` | `deprecated`;
- `confidence`: `high` | `medium` | `low`;
- `canonical`: `true` only for authoritative brand truth, otherwise `false`.

Approval never erases origin. Derived or operational guidance remains visibly distinct after approval. Follow [evidence-model.md](references/evidence-model.md).

## Workflow

### 1. Establish the brief and content lock

Capture brand, stable slug, mode, intended consumers, scoped surfaces, source owners, authority and approval route, languages, accessibility target, licensing, confidentiality, distribution target, and current skill path when updating.

For an existing artifact or supplied content, classify immutable meaning and transformable presentation before visual work. Follow [content-preservation.md](references/content-preservation.md). Do not change titles, factual claims, labels, sequence, relationships, or process logic without permission.

### 2. Inspect sources with the best available tools

Prefer native editable structure over rendered appearance:

- follow [source-figma.md](references/source-figma.md) when Figma is available;
- follow [source-adapters.md](references/source-adapters.md) for PDFs, documents, presentations, websites, repositories, asset archives, raster references, interviews, motion, print, packaging, and spatial sources;
- request an export and record the evidence limitation when a source cannot be inspected directly.

Figma is a strong source, not a mandatory dependency.

### 3. Build authority and coverage

Inventory sources and declare authority separately for logo masters, tokens, written rules, imagery, product behavior, applications, verbal identity, and approvals. Record conflicts and the decision that resolves each one.

Distinguish explicit brand truth, repeated evidence, operational needs, creative proposals, and unknown or out-of-scope areas. Do not turn an isolated polished example into a general rule.

### 4. Extract Brand Core

Follow [token-extraction.md](references/token-extraction.md) and [rule-authoring.md](references/rule-authoring.md). Extract primitives, semantic roles, patterns, surface overrides, masters, selection logic, exceptions, anti-patterns, accessibility, production constraints, and recognition signals.

State which plausible fonts, variants, formats, assets, or behaviors are not part of the brand when omission could cause invention.

### 5. Build the Creative Application Kit when scoped

Read [creative-application-kit.md](references/creative-application-kit.md). Define a visual thesis that can reject weak design, brand-specific recognition signals, a minimum viable recognition combination, native metaphors, composition patterns, expressive devices, genericity traps, and concrete generation recipes.

If imagery is not defined by official sources, create an `operational` or `new` direction grounded in verified recognition signals, product or cultural relevance, and the requested surface. Mark it `canonical: false`; never call it the official style.

Follow [assets-and-resolvers.md](references/assets-and-resolvers.md) for usable assets, rights, masters, deterministic resolvers, checksums, fallbacks, and blocked states.

Treat manifest URLs as inert metadata. The bundled resolver is local-only: use an environment-authorized download tool first, then pass its verified local result with `--source-file`.

### 6. Scaffold the generated brand skill

Read [brand-skill-architecture.md](references/brand-skill-architecture.md), then initialize the package:

```bash
python3 scripts/init_brand_skill.py <slug> --brand "<Brand>" --output <directory> --mode rules-only
```

For visual consumers, declare only the surfaces actually in scope:

```bash
python3 scripts/init_brand_skill.py <slug> --brand "<Brand>" --output <directory> \
  --mode production-ready --surfaces presentation,social
```

Fork maintainers may override package provenance with `--creator-name`, `--creator-handle`, and `--creator-url`.

Keep exact values in `brand-constants.json`, sources in `sources.json`, decisions in `decisions.json`, assets in `assets/manifest.json`, and detailed guidance in routed modules. Preserve provenance as package metadata only; never propagate it into artifacts.

### 7. Define the consumer contract

Document stable token paths, semantic aliases, asset resolution, production status, additive and breaking changes, surface compatibility, and deliberate boundaries. Downstream skills depend on semantic aliases and asset aliases, not file positions or incidental filenames.

### 8. Produce visual artifacts through an internal workflow

When a downstream artifact is requested, follow [production-workflow.md](references/production-workflow.md): lock meaning, resolve the surface and assets, generate two or three internal directions, score them, reject generic corporate options, choose one concept, render, review the screenshot, run semantic diff and asset-integrity checks, and perform at least one correction pass when problems are found.

Show the selected result rather than making the user manage routine iterations. Do not add generator credits, package provenance, comparison labels, technical status, or other meta-copy inside an artifact unless requested.

### 9. Validate behavior and visual quality

Run:

```bash
python3 scripts/validate_brand_skill.py /path/to/generated-brand-skill --strict
```

Run bundled smoke checks and relevant evals. Follow [quality-gates.md](references/quality-gates.md) and [visual-evaluation.md](references/visual-evaluation.md). Include exact-value retrieval, constrained application, hallucination traps, update/conflict handling, content preservation, native metaphor, official asset use, source-poor imagery, genericity rejection, clean-artifact, production-status, screenshot-review, and should-not-trigger cases.

Apply the brand-transplant test: if replacing the logo and palette with another brand leaves nearly the same design, reject the result as too generic. Color and logo alone are not sufficient proof of distinctiveness.

### 10. Report production status

Assign one status outside the artifact:

- `production-ready` — meaning is preserved, required masters and rights are verified, surface requirements pass, and visual, machine, semantic, and asset-integrity checks pass;
- `concept-ready` — the direction is strong but needs a missing asset, font license, legal or market review, or image clearance;
- `blocked` — a critical master, source, right, or decision is unavailable.

Do not downgrade missing critical evidence to a warning merely to finish.

### 11. Update and distribute safely

Follow [update-and-versioning.md](references/update-and-versioning.md). Preserve unaffected modules, deprecate instead of silently deleting, retain aliases where safe, append provenance history, update affected tests, and provide factual migration notes.

For Git distribution and installation, follow [distribution.md](references/distribution.md). Publish only when the user asks. Never publish confidential sources or licensed assets merely because the local skill can access them.

## Completion bar

A Brand Core is incomplete when a critical scoped item lacks authority, traceability, exact values, rights, approval state, anti-hallucination boundaries, provenance, a consumer contract, representative tests, or update ownership.

A visual brand skill is incomplete until an unfamiliar agent can produce a distinctive first-pass artifact that passes the brand-transplant test without changing the user’s semantic content.

## Handoff

Report the generated or updated path and slug, mode and surfaces, source authority and unresolved conflicts, approved versus proposed material, stable contract and migration impact, assets bundled or resolved, production status, tests and evals, known limitations, and the next update trigger.
