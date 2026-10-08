---
name: architecture-model-bootstrap
description: Use to refine a generated Better Harness architecture model into a confirmed one for the Impact pane. Trigger when a project has no
  .better-harness/architecture/model.json, when the Impact pane shows an "Auto-generated" model, or when a reader asks to name, merge, split,
  re-kind, or describe the derived Container/Component structure and propose external systems before saving it as declared.
---

# Architecture Model Bootstrap

Turn the deterministic candidate the Impact pane generates into a model a reader
can confirm. The server already derives a bounded, grounded skeleton from the
worktree (one SoftwareSystem, a Container per workspace, Components for source
directories). This skill does the **semantic** half a static analyzer cannot:
naming, grouping, kinding, describing, and proposing the external systems the
code only hints at — without inventing structure the evidence does not support.

Default to the repository's reply language. Keep edits grounded and reversible:
the output is a *proposal* a human saves, never a fact you assert.

## When to use

- A project declares no model and the Impact pane falls back to a generated one.
- A reader wants the generated skeleton refined before saving it as declared.
- An existing declared model needs elements renamed, merged, split, re-kinded, or
  described against current code.

Do not use it to invent business capabilities, runtime traffic, or external
systems that no evidence supports. L1 system context and external systems stay
**proposed and human-confirmed**, per the parent spec's non-goal.

## Inputs (the evidence pack)

Gather these before proposing anything:

1. **The generated candidate.** Open the Impact pane on any commit, or read the
   model the server would generate — one SoftwareSystem, Containers per
   workspace manifest, Components per source directory, every element tagged
   `generated`, plus bindings mapping path globs to element ids.
2. **Workspace manifests.** `package.json` (root and nested), plus any
   `Cargo.toml`, `go.mod`, `pyproject.toml`, or similar boundary markers.
3. **Directory evidence.** The tracked path list and the top-level source layout,
   so a proposed boundary points at real paths.
4. **Prose evidence.** `README.md`, `AGENTS.md`, `docs/`, ADRs — for names,
   ownership, and declared external dependencies only, never for structure the
   code contradicts.

## Workflow

1. **Read the candidate and the manifests.** Establish the real boundaries the
   generator found before changing any of them.
2. **Name and describe.** Replace generic ids/names (`packages-api`, `src`) with
   the project's own vocabulary. Give each kept element a one-line description
   grounded in what its files do.
3. **Re-kind where evidence warrants.** A deployable/independently owned unit is
   a `Container`; an internal building block inside one is a `Component`. Do not
   promote a directory to a Container without a boundary marker (a manifest, an
   entrypoint, a deploy target).
4. **Merge and split.** Fold sibling directories that are one component; split a
   directory that clearly hosts two. Every resulting element keeps at least one
   real path glob.
5. **Propose relationships** you can ground in imports, HTTP clients, or declared
   dependencies. Mark each with its kind (`Contains`, `Imports`, `ResolvedCall`,
   `DeclaredHttp`, `DeclaredRelationship`). Leave an unresolved edge out rather
   than guessing a target.
6. **Propose external systems and people** only as clearly-labelled candidates,
   with the evidence (a client, an env var, a README claim) named in the
   description. These are the L1 scale the parent spec keeps human-confirmed.
7. **Validate the shape** against [Model Schema](references/model-schema.md), then
   hand the model and bindings back for the reader to save through the Impact
   pane's **Save as declared model** action. Never write the file yourself unless
   the reader asks.

## Grounding rules (hard constraints)

- Every element you keep must have at least one binding whose path glob matches a
  real tracked path. No element without evidence.
- Never invent a binding to a path that does not exist in the worktree.
- Keep the arch-core shape exactly: `elements` (snake_case `parent_id`) +
  `relationships` (`source_id`/`target_id`). This is what the Impact host
  consumes and what discovery validates.
- A directory is not a component and a repository is not a container. Boundaries
  need a marker, not just a folder.
- Proposed external systems, people, and L1 context are candidates a human
  confirms, labelled as such in their descriptions.

## Output

Return two artifacts, ready for **Save as declared model**:

- `model.json` — the refined `{ elements, relationships }` in arch-core's shape.
- `bindings.json` — `[{ "path_glob": "...", "element_id": "..." }]`, every glob
  resolvable in the worktree.

State briefly what you renamed, merged, split, re-kinded, and proposed, and which
elements remain low-confidence candidates a reader should check first.
