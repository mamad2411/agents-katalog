---
name: create-bkn
description: >-
  Guides creation of BKN (Business Knowledge Network) definition files following v2.0.0 spec.
  Covers network, object_type, relation_type, action_type, concept_group.
  Use when creating knowledge networks, BKN files, object types, relation types, action types,
  concept groups, or when user asks to model business knowledge in BKN format.
  When kweaver-core is also loaded, use it to run kweaver CLI (auth, bkn push) after files exist.
---

# Create BKN

Generate well-formed BKN knowledge network definitions following v2.0.0 specification.

## Works with kweaver-core

If **both** skills are loaded:

| Role | Skill |
|------|--------|
| Author modular `.bkn` trees (layout, sections, templates) | **create-bkn** (this skill) |
| Install CLI, auth, **`kweaver bkn push` / `pull`**, other `kweaver bkn` ops | **kweaver-core** |

Typical flow: generate or edit the directory with create-bkn → then use kweaver-core’s workflow for `kweaver auth login` and `kweaver bkn push <dir>`. If you only operate the CLI and need new BKN files from scratch, switch to **create-bkn** for generation first.

## What is BKN

BKN (Business Knowledge Network) is an open format that uses Markdown + YAML frontmatter to describe business knowledge networks. At its core, BKN is a **semantic modeling tool** — it captures the entities, relationships, and operations of a business domain in a structured, explicit way so that humans, AI Agents, and systems share a common understanding. Design principles:

- **Semantic modeling** — Model any business domain through three layers: object types (what exists), relation types (how things connect), and action types (what can be done), forming a queryable, reasonnable knowledge graph schema
- **Markdown-native** — Every definition is a `.bkn` file (plain Markdown). Humans can read and edit directly; AI Agents can parse and generate natively — no specialized editor required
- **Schema as Code** — Knowledge network schemas live as files in a directory, enabling git version control, code review, and CI/CD — treated the same as source code
- **Modular one-file-per-definition** — Each object type, relation type, and action type is an independent `.bkn` file in its corresponding subdirectory, enabling independent maintenance and on-demand loading
- **Declarative** — BKN describes "what is" (schema), not "how to do it" (logic). Action types declare parameter bindings and tool configurations, but execution is handled by the runtime
- **Package and deliver** — A BKN directory can be tar-packed and uploaded directly to the KWeaver platform, which parses it into a complete knowledge network automatically

## Directory Structure

Every BKN network uses this modular layout — **each definition is a separate file in the correct subdirectory**:

```
{network_dir}/
├── SKILL.md                     # Agent-facing usage guide
├── network.bkn                  # Root file (type: network)
├── CHECKSUM                     # Optional, SDK-generated
├── object_types/                # One .bkn per object type
│   ├── pod.bkn
│   └── node.bkn
├── relation_types/              # One .bkn per relation type
│   ├── pod_belongs_node.bkn
│   └── service_routes_pod.bkn
├── action_types/                # One .bkn per action type
│   ├── restart_pod.bkn
│   └── cordon_node.bkn
├── concept_groups/              # One .bkn per concept group
│   └── k8s.bkn
└── data/                        # Optional, .csv instance data
    └── scenario.csv
```

## Workflow

1. **Gather requirements** — identify objects, relations, actions, optional concept groups
2. **Create `network.bkn`** — read [references/network.md](references/network.md)
3. **Create `object_types/*.bkn`** — one file per object, read [references/object_types.md](references/object_types.md)
4. **Create `relation_types/*.bkn`** — one file per relation, read [references/relation_types.md](references/relation_types.md)
5. **Create `action_types/*.bkn`** — one file per action, read [references/action_types.md](references/action_types.md)
6. **Create `concept_groups/*.bkn`** — optional, read [references/concept_groups.md](references/concept_groups.md)
7. **Update `network.bkn`** — list all IDs in Network Overview
8. **Add `SKILL.md`** — agent-facing guide (see below)
9. **Validate (MUST)** — run `kweaver bkn validate <dir>`. Fix all errors until validation passes. See [Validation](#validation).
10. **Import** (optional) — `kweaver bkn push <dir>` packs, validates, then uploads. See below.

## Import via kweaver CLI

**Install** (pick one):

- **TypeScript / Node** (recommended): `npm install -g @kweaver-ai/kweaver-sdk` — requires Node.js 22+
- **Python**: `pip install kweaver-sdk[cli]` — requires Python ≥ 3.10
- One-off without global install: `npx kweaver …` (same subcommands)

Full install matrix: [README.md](../../README.md) (this repo root).

```bash
kweaver auth login https://your-kweaver-instance.com
kweaver bkn push <path-to-bkn-directory> [--branch main] [-bd <business-domain>]
```

`push` packs the directory (macOS tar uses `COPYFILE_DISABLE=1`), may refresh `CHECKSUM`, then imports on the platform. Export: `kweaver bkn pull <kn-id> [<dir>]`. More `kweaver bkn` commands: [kweaver-core/references/bkn.md](../kweaver-core/references/bkn.md).

## Validation

> **MUST** — Every generated BKN directory must be validated before delivery or upload.

```bash
kweaver bkn validate <path-to-bkn-directory>
```

On success prints `Valid: N object types, N relation types, N action types`. On failure prints each error and exits non-zero.

If validation fails, read the error messages, fix the `.bkn` files, and re-run until it passes.

## Per-Type Reference

Read the reference for the type you are creating:

| Directory | Reference | Required Sections |
|-----------|-----------|-------------------|
| `network.bkn` | [references/network.md](references/network.md) | `#` title, `## Network Overview` |
| `object_types/` | [references/object_types.md](references/object_types.md) | Data Properties, Keys |
| `relation_types/` | [references/relation_types.md](references/relation_types.md) | Endpoint, Mapping Rules |
| `action_types/` | [references/action_types.md](references/action_types.md) | Bound Object, Tool Configuration, Parameter Binding |
| `concept_groups/` | [references/concept_groups.md](references/concept_groups.md) | Object Types |

## Naming Conventions

- **ID**: lowercase letters, numbers, underscores (e.g. `pod_belongs_node`, `product2bom`)
- **File name**: `{id}.bkn` (e.g. `pod.bkn`, `pod_belongs_node.bkn`)
- **Heading level**: `#` network title, `##` type definition, `###` section, `####` sub-item (logic property)
- **Frontmatter**: all types require `type`, `id`, `name`; `tags` optional

## Validation Checklist

> **MANDATORY** — You MUST pass every item below before considering a BKN directory complete. Run `kweaver bkn validate <dir>` (see [Validation](#validation)) to catch errors automatically.

### Structure & Frontmatter

- [ ] `network.bkn` exists at directory root with `type: network` frontmatter
- [ ] Every `.bkn` file has valid YAML frontmatter containing at least `type`, `id`, `name`
- [ ] Each `.bkn` file lives in the correct subdirectory matching its `type` (`object_types/`, `relation_types/`, `action_types/`, `risk_types/`, `concept_groups/`)
- [ ] File name matches `{id}.bkn` (e.g. frontmatter `id: pod` → file `object_types/pod.bkn`)

### Referential Integrity

- [ ] `network.bkn` Network Overview lists **all** IDs from every subdirectory — nothing missing, nothing extra
- [ ] All relation type Endpoints reference existing object_type IDs defined in `object_types/`
- [ ] All action type Bound Object IDs reference existing object_type IDs
- [ ] Risk type references (if any) point to existing action_type or object_type IDs
- [ ] Concept group `## Object Types` only list existing object_type IDs

### Content Quality

- [ ] Table column names use canonical English headers (Name, Display Name, Type, Required, Description, etc.)
- [ ] Parameter Binding `Source` is one of: `property`, `input`, `const`
- [ ] YAML code blocks (e.g. Trigger Condition) parse as valid YAML
- [ ] No `type: delete` or `type: patch` files — BKN uses upsert-only model
- [ ] Heading hierarchy is strict: `#` > `##` > `###` > `####` with no level skips

## Output Rules

1. Output raw BKN Markdown with frontmatter — do not wrap in ````markdown` code blocks
2. Reference existing IDs when creating relations/actions
3. ID uses lowercase + underscores; display names and descriptions in Chinese unless otherwise specified
4. Follow heading hierarchy strictly: `#` > `##` > `###` > `####`

## Examples

- **K8s network**: `examples/bkn/k8s-network/` — 3 objects, 2 relations, 2 actions, 1 concept group
- **Supply chain**: `examples/bkn/supplychain-hd/` — 12 objects, 14 relations, full MRP flow

## SKILL.md for BKN Directory

Each BKN directory should include a `SKILL.md` as agent-facing guide. The core principle is **progressive disclosure**:
agent reads SKILL.md first to understand the network topology and locate definitions, then reads individual `.bkn` files on demand.

**SKILL.md = overview + index (always loaded), `.bkn` files = detail (read on demand)**

### Structure

1. **Network metadata**: ID, version, tags (blockquote header)
2. **Network overview**: one paragraph describing the business domain
3. **Index tables with file paths** (the key progressive disclosure mechanism):
   - Core objects table: object | file path | description
   - Core relations table: relation | file path | source -> target | description
   - Actions table: action | file path | bound object | description
4. **Topology diagram**: ASCII or mermaid, showing object relationships at a glance
5. **Usage scenarios**: query and ops scenarios, each pointing to relevant `.bkn` files to read
6. **Index by type and by function**: glob patterns (`object_types/*.bkn`) and functional grouping

### Why File Paths in Tables Matter

The tables serve as a **routing layer**: agent sees "restart_pod | `action_types/restart_pod.bkn` | Pod" and knows exactly which file to read when the user asks about pod restart. Without these paths, the agent would need to scan the entire directory.

### Example

See `examples/bkn/k8s-network/SKILL.md` and `examples/bkn/supplychain-hd/SKILL.md` for real implementations.
