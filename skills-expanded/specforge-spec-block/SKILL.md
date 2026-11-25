---
name: specforge-spec-block
description: "Write the spec block, the project's root entity (one of the five structural keywords of the core grammar), and know where configuration really lives: specforge.json holds the project name, version, spec_root, the extensions to load, providers and registries. Use when initializing a SpecForge project in any domain, changing which extensions a project loads, or editing the root spec block."
---

# SpecForge Spec Block

> **Structural, not from an extension.** `spec` is one of the five keywords the core grammar knows (`spec`, `ref`,
> `use`, `define`, `defaults`). It is a graph entity only: **it configures nothing**. No extension, provider or setting
> is read from it. Configuration is `specforge.json`.

## Where configuration lives: `specforge.json`

`specforge init` writes it. The keys an agent touches most:

| Key | What it does |
|-----|--------------|
| `name`, `version` | Project identity and `.spec` format version. |
| `spec_root` | Directory of the `.spec` sources (default: the project root). |
| `extensions` | The extensions to load: a builtin or installed `@scope/name`, or a `.wasm` component file. **This list decides which entity kinds exist.** |
| `exclude` | `.spec` files under the spec root that are not sources. |
| `providers` | Ref schemes (registered only: no host reader yet). |
| `registries` | Package registries for `add`, `update`, `search`, `publish`. |
| `strict` | Treat warnings as errors. |

Change the extension list with commands, not by hand:

```bash
specforge init --extensions @specforge/product,@specforge/governance   # a new project
specforge add @specforge/software                                       # load one more
specforge remove @specforge/governance
specforge extensions                                                    # what is enabled, locked and loaded
```

## The `spec` Block

```spec
spec "clinic-operations" {
  version "0.1.0"
}
```

The name after `spec` is the block's ID (2-60 characters, E014). Write one `spec` block per project, by convention in
`specforge.spec` or `main.spec` under the spec root. Fields beyond `version` are free-form descriptive text; none of
them change how the project compiles.

## Writing Rules

1. **One `spec` block per project.**
2. **Never configure in it** -- `extensions [...]`, `providers {...}`, `persona`/`surface` lines or `coverage {...}`
   inside `spec` do nothing (or fail to parse). Use `specforge.json` and the extensions' own kinds.
3. **Personas and channels are entities** -- with `@specforge/product` loaded, write `persona` and `channel` blocks.
4. **No `define` blocks** -- `define` is reserved but registers nothing (W143). A new entity kind comes from an
   extension: `specforge extension init` scaffolds one.

## Validation Rules

| Code | Owner | Rule |
|------|-------|------|
| E001 | core | Sub-blocks such as `persona admin "..."` or `coverage { ... }` inside `spec` do not parse. |
| E002 | core | A second `spec` block, whatever its name. |
| E014 | core | The spec name is shorter than 2 or longer than 60 characters. |
| E069 | core | `specforge.json` is unusable. |
| I002 | core | No extensions configured: structural-only mode (only `spec`, `ref`, `use`, `define`, `defaults`). |
| W143 | core | A `define` block. |

## What NOT to Do

- Do not list extensions in the `spec` block -- `specforge.json` `extensions` (via `specforge add`) is what loads them
- Do not declare personas, surfaces, coverage or test directories in the `spec` block
- Do not write `define` blocks to invent kinds -- write or install an extension
- Do not put `use` directives inside the spec block -- `use` is file-level
