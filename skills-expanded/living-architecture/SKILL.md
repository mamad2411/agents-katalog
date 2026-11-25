---
name: living-architecture
description: 'Reference for the living-architecture layer (LikeC4 structure model + arc42 principles + model-truth import enforcement + cross-check): its syntax, the checks, the rules a coding agent follows when it changes code under it, and how to maintain it. Building the first model is la:arch-init; carving a boundary is la:arch-cleanup.'
---

**Preflight:** run `la-doctor --plugin <this skill's base directory>` once per session before using any `la-*` or `dr-*` command; if it fails, stop and show the user its output.

# Living architecture

Four layers, one element id everywhere. Behaviour lives in OpenSpec (in repos that use it); everything
cross-cutting lives here:

| Layer | Question | Artifact | Property |
|---|---|---|---|
| Behaviour | what does it do, now? | `openspec/specs/<id>/spec.md` | living, merged by OpenSpec |
| Structure | how is it arranged, now? | LikeC4 model + views | living; ONE model, diagrams are projected views |
| Rationale | why is it this way, and what must all code here obey? | arc42 file per element that earns prose | living, edited in place |
| Enforcement | is the code actually like this? | `arch_check` model-truth (the one import law) + LikeC4 model validation, run before a change is done and in CI | executable, blocking |

**History is NOT a layer here.** Git history, plus the OpenSpec archive (per-change
design + deltas, dated, immutable) in repos that use it, IS the decision trail. Never create
ADR files or append-only decision logs (they are merge hell). "Why it is like
this now" belongs in the element's arc42, present tense; "how we got here" is
history.

## Alignment rules

- **arc42 = LikeC4 = module structure align perfectly.** An element's fully qualified id is its LikeC4 id
  and names its arc42 file, `architecture/<id>.arc42.md`; a precise element's package is its node's `package` plus
  its path below the node.
- **OpenSpec is looser.** A spec either belongs to one element at any depth (listed in that element's
  metadata `specs` — the element is then a behaviour *leaf*) or is **cross-cutting** (listed once in `index.yaml`
  with the fully qualified elements it touches, at any depth). Never duplicate a spec across elements; `arch_check`
  enforces exactly-once.
- **Model depth is a dial, not an obligation.** Model precisely where you are
  actively enforcing boundaries; sweep the rest into a few *virtual bucket
  nodes* (tagged `#virtual`, claiming several packages, no alignment claim,
  governed only at bucket granularity — no nested elements, no child-level arrows).
  Deepen a bucket into precise nodes the first time real
  work touches it. Never model deeper than you're willing to keep true.

## File layout — the tree is virtual

Each tool keeps its native layout; shared node ids join them. The LikeC4 model
maps nodes to code; `index.yaml` holds only repo-wide settings.

```
repo/
  openspec/specs/<spec-id>/spec.md
  architecture/
    model.c4                         # the ONE LikeC4 model: one specification and one model block
    views.c4                         # one views block; each view scoped to one language root
    index.yaml                       # repo-wide settings (below)
    system.arc42.md                  # root narrative + global principles
    <element id>.arc42.md            # e.g. python.sql.arc42.md; only where an element earns prose
  living-architecture.yaml           # repo config: format, and architecture: true once the model exists
```

Every arc42 file sits directly in `architecture/`, never in a subfolder.

These are the only LikeC4 files allowed anywhere under `architecture/` (`.c4` or
`.likec4`). Nothing else may sit at their top level. Any other layout makes
`la-arch-check` exit 2 and `la-arch-diagrams` exit 1, with one message naming
every violation. The repo's format is `format` in `living-architecture.yaml`:
the `la` version that introduced it. Every command refuses any other format,
naming the `la` to upgrade to for a newer one and `la-arch-migrate` for an older
or missing one; `la-arch-migrate` converts the repo (verified, all-or-nothing)
and stamps the current format.

The checker is `la-arch-check` (the one import law + cross-check, run by the
gates); it needs no per-repo code. `la-arch-diagrams` regenerates the embedded
view diagrams.

The model has one top-level **root element per language** `index.yaml` declares,
whose id is the language (`python`, `typescript`); it carries no mapping metadata. A node
is a direct child of a root; it is virtual iff its element kind is declared
`#virtual`. Relations are written inside a root with names relative to it
(`sql -> core` inside `python { }` is `python.sql -> python.core`), so a relation
across roots cannot be written. Element ids are fully qualified in findings and
in `touches:`. Any element — root, node or nested — MAY list the `specs` it owns in one `metadata { }`
block; a node also declares its mapping there:

```
specification {
  element node
  element bucket {
    #virtual
  }
  tag legacy
  tag virtual
}
model {
  python = system 'My package' {             // the python root (any element kind)
    sql = node 'SQL' {                       // precise node python.sql
      metadata {
        package 'mypkg.sql'                  // required
        claims ['mypkg.sqlutil']             // optional: further units it owns
        specs ['sql-dialects']               // specs owned by THIS node alone
      }
      // arc42 doc, if any: architecture/python.sql.arc42.md
      render = node 'Render' { metadata { specs ['sql-render'] } }  // maps to mypkg.sql.render; nested elements may own specs
      dialects = node 'Dialects'             // maps to mypkg.sql.dialects
    }
    surfaces = bucket 'Surfaces' {           // virtual bucket
      metadata {
        packages ['mypkg.api', 'mypkg.mcp', 'mypkg.cli']
      }
    }
    surfaces -> sql
  }
}
```

TypeScript units are extensionless paths relative to the section's
`source_root` (`package 'src/daemon'`, nested `pty` maps to `src/daemon/pty`); a
unit is a directory with a visible source file or exactly one module file, and a
unit naming both is ambiguous. Test files, declaration files
(`la-config get lang.typescript.declaration_globs`) and installed dependencies are
invisible; type-only imports never count.

Keys and types come from the shared node schema; values are `key 'value'` or
`key ['a', 'b']` — single quotes, no escapes, arrays may span lines, no trailing
comma. Nested elements, at any depth, carry no mapping keys: `<node>.a.b` maps to `<package>.a.b`, and the
import law applies wherever the model nests. Malformed metadata is a setup error (exit 2) naming the element; a
model still using the retired `arc42` key converts with `la-arch-migrate`.

`index.yaml`:

```yaml
python:                               # one section per language; at least one
  root_package: mypkg                 # required, or root_packages: the unit of the python root
  source_root: src                    # optional: directory containing the roots
typescript:
  root_package: src
  source_root: web                    # optional
  tsconfig: web/tsconfig.app.json     # optional: default each root's nearest tsconfig

legacy_arrows: {baseline: 8}          # exact count of #legacy arrows in the model (ratchet)

cross_cutting_specs:
  queries: {touches: [python.core, python.engine, python.sql]}

x-anything: {}                        # repo-owned keys start with x-; the tools ignore them
```

`root_packages: [app, packages/ui]` replaces `root_package` when a language's code sits in several sibling
directories under one `source_root`; the roots are disjoint and unit ids stay relative to `source_root`.

`views.c4` scopes each view to a root, `view <id> of <root> { ... }`, with include names and predicate
anchors relative to the root at any depth (`include api.handlers`, `api.handlers -> *`); the root itself is never
drawn.

## arc42 element file — required shape

arc42-lite, per element, always present tense, updated in place:

1. **Purpose & context** — 3–10 lines.
2. **Building blocks** — pointer to the node's LikeC4 view. Never a duplicate
   drawing, never a prose restatement of the model.
3. **Principles** — numbered rules that ALL code in this element and its descendants, old and new,
   MUST obey. Each tagged `[enforced: <check|test id>]` or
   `[review]`. Prefer enforced; every `[review]` principle is a standing
   candidate for a new fitness function. Keep them normative and minimal: when
   work strains a principle, first make the code comply; edit one only when it
   genuinely forbids something needed, in the smallest general wording — never
   descriptive text or implementation detail (function names, mechanisms).
4. **Rationale** — why the current shape is right. Where it derives from a
   specific change, link the archived openspec change id — do not restate
   history.

## Enforcement wiring — the one import law

There is no separate import-linter config: the entire import law lives in the
LikeC4 model and is checked by `la-arch-check` (**model-truth**). The
model's relations must exactly match the AST-measured runtime import edges, at
every granularity the model declares:
- a module attributes to its finest mapped element, else its node;
- every edge is licensed by its most-specific covering arrow — a declared
  arrow is the only thing that permits an import, and silence is a ban;
- a measured edge with no covering arrow, a declared arrow with no measured
  edge, and an undeclared edge between two nested elements are all findings.

Type-only imports are excluded. Grandfathered crossings are dashed
`#legacy` arrows in the model itself (one arrow per real edge, no wildcards);
"layer direction" is just *no upward arrow declared*, and a child boundary is
just *no arrow declared between those nested elements* — so one law subsumes what used
to be separate `layers` / `forbidden` / boundary contracts.

Python edges come from `ast`, TypeScript edges from the TypeScript compiler
under the repo's tsconfig. Either twin checks a mixed repo: each language's facts
come from its own twin (PyPI or npm, found on PATH or run through `uvx`/`npx`), and
model-truth runs once over all of them.

**The enforcement bundle** = `la-arch-check` + LikeC4 model validation
(`npx likec4 validate`; if the installed CLI version lacks it, use the lightest
command that parses the model, e.g. `npx likec4 build`) + `la-typecheck` against
its committed baseline. It is blocking: run it before declaring any change done,
and in CI. `arch_check` is cheap and deterministic, so wire it there once the setup
has settled (not at init), pinned to a release, in the form of the repo's
ecosystem: `uvx --no-build --from living-architecture==<version> la-arch-check`
(after `astral-sh/setup-uv`, pinned by commit SHA) or
`npx -y -p living-architecture@<version> la-arch-check` (after
`actions/setup-node`, pinned by commit SHA).

**Ratchet rules (hard):**
- `#legacy` arrows may only ever be REMOVED, never added. Wanting to add one
  means the architecture is changing — change the model and arc42 deliberately
  instead, with the user's explicit OK.
- `legacy_arrows.baseline` in `index.yaml` is the exact `#legacy` count;
  `arch_check` fails if the model's count differs, and the baseline is lowered
  as arrows are retired. Progress is monotonic and machine-checked.

**`la-arch-check` verifies, from the model and `index.yaml`:**
- `architecture/` holds exactly `model.c4` and `views.c4`, each with only its blocks (else exit 2);
- every element's metadata matches the shared schema (else exit 2);
- every precise node's `package` and `claims` (and every bucket's `packages`)
  exist on disk; every nested element's unit exists under its node's package
  and does not collide with another declared unit; a bucket contains no
  elements; every arc42 file sits directly in `architecture/` and is `system.arc42.md`,
  `<element id>.arc42.md` of a model element, or listed in `cross_cutting_arc42`;
- every top-level unit of each language's roots is claimed by exactly
  one node — no orphan packages;
- every spec group (a directory under `openspec/specs/` or under a non-archived
  change's `specs/`) is mapped exactly once: in exactly one element's `specs`
  or in `cross_cutting_specs:`; every element named in a `touches:` list exists;
- model-truth holds at every declared granularity, the `#legacy` count equals
  `legacy_arrows.baseline`, and each mapped doc's embedded view diagram is
  byte-fresh;
- every principle item in an arc42 file carries a status tag —
  `[enforced: arch_check:<check-id>]`, `[enforced: test:<path>]`, `[review]`,
  or `[target: <issue key>]` (a future-state clause; keys must match the
  repo's `issue_key_pattern`); an item may add one `[lang: <language>]` naming
  a declared language it alone binds.

## Maintenance

- No model yet (`architecture/index.yaml` absent) → run the **la:arch-init**
  skill; it builds the first model from a measured scaffold.
- Otherwise keep the model, `index.yaml`, and arc42 in sync IN THE SAME PR as
  any structural change; deepen buckets / add views for new subsystems; tighten
  boundaries via the **la:arch-cleanup** skill.

## Working under the architecture

These rules bind a coding agent at every step of any change in a repo whose
`living-architecture.yaml` sets `architecture: true`: planning, writing tests, implementing,
and fixing review findings. `architecture/*.arc42.md`, `architecture/model.c4`
and `architecture/views.c4` are normative harnesses, exactly like tests.

- **Read them first.** Before the work, read `architecture/index.yaml`, the
  arc42 file of each element the change touches and of each of its ancestors
  (`architecture/<element id>.arc42.md`, where present), `system.arc42.md`
  (cross-cutting principles), and the LikeC4 view of every touched element.
- **Obey them.** Every plan, test, implementation and fix obeys the element
  principles and the model's import law, or explicitly includes the model +
  arc42 update as part of the change. A plan states which principles apply.
- **Flag, never deviate.** If anything in an arc42 file seems wrong,
  contradictory, or makes the task impossible or substantially harder, flag it
  to the user explicitly and wait for their call. Never silently deviate from,
  reinterpret, or ignore a principle, and never produce work that quietly
  conflicts with one.
- **Keep them normative and minimal.** When work strains a principle, first make
  the code comply; propose an edit only when the principle genuinely forbids
  something needed, in the smallest general wording. Never use descriptive text
  or implementation detail (function names, mechanisms).
- **Never edit without per-change approval.** Never create, modify, or delete a
  harness without the user's explicit approval of that specific edit: present
  the exact edit and wait for the OK. An approved plan that mentions the edit
  does not count.
- **Finish green.** Before declaring the change done, run the enforcement bundle
  and fix until it passes.
- **New capability** (OpenSpec repos): decide with the user where its spec
  attaches (one element's metadata `specs`, at any depth, or
  `cross_cutting_specs` in `index.yaml` with a `touches:` list) and record it in
  the same change.
- **Pure structural refactors** (moving code across boundaries) are their own
  changes via **la:arch-cleanup**, never smuggled into feature changes.
