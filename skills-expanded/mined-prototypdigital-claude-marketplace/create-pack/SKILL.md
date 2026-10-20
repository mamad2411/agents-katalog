---
name: create-pack
description: Scaffold a whole new bluetemberg pack — package.json metadata, llm/ layout, catalog registration, and validation.
---

# create-pack

Use this skill when asked to create a new bluetemberg pack (a publishable npm package of rules, agents, or skills) in the bluetemberg-packs monorepo.

## Triggers

- "create a new pack for..."
- "scaffold a bluetemberg-rules / -agents / -skills package"
- "add a new pack that bundles ..."
- Any request to start a brand-new distributable content package (not a single rule/agent/skill in an existing project)

## Required behavior

1. The agent MUST gather the following before writing anything — if any is unclear, ask:
   - **kind**: exactly one of `rules`, `agents`, or `skills`. A pack contains a single kind.
   - **topic**: kebab-case topic (e.g. `testing`, `accessibility`, `database`). The package name is `bluetemberg-{kind}-{topic}`.
   - **description**: one sentence ending in "for Bluetemberg" style, summarizing the pack's contents.
   - **universal vs profiles**: is this pack for every team (`universal: true`, `profiles: []`) or profile-scoped (`universal: false`, `profiles: [...]` from `frontend`, `backend`, `fullstack`, `devops`, `pure-infra`, `agentic`)? A pack is never both universal and profile-scoped.

2. The agent MUST check `packages/` for an existing pack with the same name or overlapping scope before creating anything. If one exists, extend it instead and report which.

3. The agent MUST create the directory at exactly `packages/bluetemberg-{kind}-{topic}/` with this layout:
   - `package.json` (see template)
   - `llm/{kind}/...` — `llm/rules/*.md`, `llm/agents/*.md`, or `llm/skills/{name}/SKILL.md` depending on kind

4. The agent MUST write a `package.json` matching the house conventions exactly: `version` `0.1.0`, `keywords` including `"bluetemberg-pack"` and the kind, `author` `"Prototyp Digital"`, `license` `"MIT"`, the shared `repository`, `files: ["llm/"]`, and a `bluetemberg` block with `universal` and `profiles`.

5. The agent MUST author at least one real content file using the matching meta-skill conventions — `create-rule` for rules, `create-agent` for agents, `create-skill` for skills. An empty pack must not be created.

6. The agent MUST register the pack in `bluetemberg.config.json` by adding `./packages/bluetemberg-{kind}-{topic}` to the `extends` array, keeping the array alphabetically sorted. Validation fails if a package exists but is not listed.

7. The agent MUST run, in order, and not report success until all pass:
   - `npm run generate:catalog` — regenerate `catalog.json` and the wiki catalog table (run this BEFORE validate; the validator fails if the catalog is stale)
   - `npm run validate` — pack-structure, config, release-please, and catalog-freshness cross-check
   - `npm run lint:md` — markdownlint over the new `.md` files

8. The agent MUST NOT mix kinds in one pack (no rules and skills together) and MUST NOT set both `universal: true` and a non-empty `profiles` array.

## package.json template

Use the correct `bluetemberg` block for the pack's scope — choose one, never mix.

**Profile-scoped pack** (`universal: false` — only installed for specific profiles):

```json
{
  "name": "bluetemberg-{kind}-{topic}",
  "version": "0.1.0",
  "description": "{One sentence} for Bluetemberg.",
  "keywords": ["bluetemberg-pack", "{kind}"],
  "author": "Prototyp Digital",
  "license": "MIT",
  "repository": {
    "type": "git",
    "url": "https://github.com/prototypdigital/bluetemberg-packs.git"
  },
  "files": ["llm/"],
  "bluetemberg": {
    "universal": false,
    "profiles": ["backend", "fullstack"]
  }
}
```

**Universal pack** (`universal: true` — installed for every profile, `profiles` must be `[]`):

```json
{
  "name": "bluetemberg-{kind}-{topic}",
  "version": "0.1.0",
  "description": "{One sentence} for Bluetemberg.",
  "keywords": ["bluetemberg-pack", "{kind}"],
  "author": "Prototyp Digital",
  "license": "MIT",
  "repository": {
    "type": "git",
    "url": "https://github.com/prototypdigital/bluetemberg-packs.git"
  },
  "files": ["llm/"],
  "bluetemberg": {
    "universal": true,
    "profiles": []
  }
}
```

## Examples

The two most common pack-creation mistakes are mixing kinds in one pack and setting both `universal: true` and a non-empty `profiles` array — validation rejects both:

```text
BAD:  packages/bluetemberg-mixed-tooling/
        llm/rules/*.md           # rules AND skills in one pack
        llm/skills/{name}/SKILL.md
      package.json → "bluetemberg": { "universal": true, "profiles": ["backend"] }
      -- Two kinds in one pack, and universal:true WITH a non-empty profiles list.
         The pack can't be categorized or scoped; `npm run validate` fails.

GOOD: packages/bluetemberg-rules-tooling/    # exactly one kind
        llm/rules/*.md
      package.json → "bluetemberg": { "universal": false, "profiles": ["backend", "fullstack"] }
      -- One kind, one scope. Registered in bluetemberg.config.json (alphabetical)
         and in release-please-config.json + .release-please-manifest.json.
```

- "Create a testing rules pack for backend and frontend" → `packages/bluetemberg-rules-testing/` with `package.json` (`universal: false`, `profiles: ["frontend", "backend", "fullstack"]`), `llm/rules/*.md` authored per `create-rule`, registered in `bluetemberg.config.json`, catalog regenerated, validate + lint:md green
- "Scaffold a universal observability skills pack" → `packages/bluetemberg-skills-observability/` with `universal: true`, `profiles: []`, `llm/skills/{name}/SKILL.md`

## When NOT to use

- The request is to add a single rule/agent/skill to an existing project or pack — use `create-rule` / `create-agent` / `create-skill`
- A pack with the same name or overlapping scope already exists — extend it
- The work is in a consumer project, not the bluetemberg-packs monorepo (consumer projects author into their own `llm/`, they do not create publishable packages)
