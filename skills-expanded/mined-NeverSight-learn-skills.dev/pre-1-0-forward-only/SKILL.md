---
name: pre-1-0-forward-only
description: >
  Apply forward-only editing, documentation, and review rules for Rust crates or
  workspaces whose package or workspace version is below 1.0. Use when editing,
  reviewing, or documenting pre-1.0 Rust APIs, READMEs, AGENTS.md guidance,
  examples, release notes, migration text, or workflow docs: omit durable
  absent-surface negative prose such as "does not currently..." and avoid
  backward/legacy compatibility obligations, old API preservation, aliases,
  wrappers, or shims unless explicit repository policy or the user requires them.
---

# Pre-1.0 Forward Only

Use this skill to keep pre-1.0 Rust workspaces focused on the current API and
current repository shape. It pairs two rules:

1. Durable docs should route to the surfaces that exist instead of cataloging
   absent surfaces.
2. Pre-1.0 Rust crates and workspaces carry no backward/legacy compatibility
   burden unless explicit project policy or the user says otherwise.

## Scope Check

Before applying the rules:

1. Read the relevant `Cargo.toml`.
2. Treat `workspace.package.version = "0.x.y"` as applying to every workspace
   crate that inherits it.
3. Treat a crate-local `version = "0.x.y"` as applying to that crate.
4. If the relevant version is `1.0.0` or later, or project docs promise
   compatibility, follow that compatibility policy instead.
5. If the user explicitly asks to preserve an old API, command, document shape,
   or migration path, do that and state the tradeoff.

## Durable Docs

For READMEs, `AGENTS.md`, crate docs, examples, and other durable repository
guidance:

- Omit absence inventory such as `does not currently contain`,
  `currently does not include`, `not yet`, `currently lacks`, and similar
  phrasing.
- Prefer positive routing to evidenced surfaces: name the command, crate,
  module, test, generated source, or document that owns the work.
- Remove stale references instead of replacing them with prose about missing
  paths.
- Use negative wording only when it changes an action: `Do not edit generated
  output`, `do not commit secrets`, or `not validated because ...` in a handoff.
- Keep temporary uncertainty in the final response or review note, not in the
  durable repository guide.

Example rewrite pattern:

```md
Start with `just --list`; the `justfile` is the repository command index. The
main Rust workspace is defined in `Cargo.toml`.
```

## Forward-Only API Rule

For pre-1.0 crates and workspaces without an explicit compatibility promise:

- Treat the current API, command surface, route shape, generated output, and
  documented workflow as the contract.
- Apply this as task procedure; do not add a standing pre-1.0 policy sentence to
  durable docs or `AGENTS.md` solely because a manifest version is below `1.0`.
- Move implementation, public exports, tests, examples, generated outputs,
  README text, crate docs, and `AGENTS.md` guidance to the current shape in the
  same change when they name the changed surface.
- Remove obsolete docs, tests, examples, and expectation files once they no
  longer describe the current behavior.
- Avoid adding legacy aliases, compatibility wrappers, deprecated exports,
  migration layers, old command paths, or "keep the old API" wording solely for
  backward compatibility.
- If a compatibility bridge is explicitly required, mark it as user-requested or
  policy-backed and keep it scoped.

## Review Workflow

1. Confirm the pre-1.0 scope from manifests before invoking forward-only rules.
2. Search durable docs and guidance for absence-inventory phrasing.
3. Search affected code/docs for compatibility language such as
   `backward compatibility`, `backwards compatibility`, `legacy`, `deprecated`,
   `old API`, `compatibility shim`, and `migration`.
4. Inspect matches manually; these searches are prompts, not mechanical delete
   rules.
5. Patch the owning implementation, tests, docs, examples, generated sources, or
   guidance so the current shape is described consistently.
6. Validate with the narrowest command that proves the changed surface, or state
   static review for docs-only edits.
