---
name: docdoki
description: >-
  Use for project work guided by a docdoki/ library: load before substantial
  implementation covered by its design, even when the user does not name DocDoki.
  Maintain human intent, decided specs (including unimplemented requirements),
  work state, evidence, and reusable knowledge. Also use to set up/adopt a
  library, answer project questions, reconcile human design edits or code drift,
  groom documents, or prepare a continuation handoff. Do not introduce it for
  unrelated README/docs copyediting or code with no relevant library.
---

# DocDoki

DocDoki is a file-first, Git-native shared project knowledge base maintained primarily by agents and steered by humans. Humans focus on intent, architecture, and key decisions (`northstar.md`, `overview.md`, and selective design proposals); agents maintain contracts, work state, evidence, and reusable notes using normal file, Git, and verification tools.

Read [Philosophy](references/philosophy.md) for underlying principles and [Schemas](references/schemas.md) when creating or restructuring documents.

## Library map

Find the nearest applicable `<unit>/docdoki/` (following child unit links in `northstar.md` when work belongs to a child unit). Do not adopt an unrelated repository merely because this skill exists.

- `northstar.md` — **Intent:** mission, success criteria, hard constraints, parent/child units.
- `overview.md` — **Human steering surface:** system architecture, area map, and `## Open decisions` (legacy libraries may use `spec_abstract.md`).
- `specs/<name>.md` — **Design contracts:** decided obligations (or `status: proposed` drafts awaiting review), `purpose`, `area`, `progress`, `after`, and `covers`.
- `work/<slug>.md` — **Active work:** linked `specs`, `scope`, current state, gaps, checks, next actions, and handoffs; closed work moves to `work/archive/` (legacy libraries may use `stages/`).
- `notes/<topic>.md` — **Durable knowledge:** methods, gotchas, research, rejected options, and verification evidence, linked via `relates` or `covers`.
- `private/` — **Local-only overlay** mirroring `specs/`, `work/`, and `notes/`, excluded via `.gitignore`.

## Standing invariants

1. **Contracts ≠ conformance.** A decided requirement remains valid when code is absent or broken. Code and tests supply evidence, never authority to weaken a contract. Preserve the meaning, conditions, and exceptions of human input wherever it is written.
2. **Read/review is zero-write.** Answering questions and read-only reviews modify no files—no formatting, status updates, work-file edits, or generated files.
3. **Match claims to evidence.** Distinguish confirmed behavior (with check scope), known unmet requirements, and unchecked claims. Never mark a spec `done` from code reading alone or a single partial check.
4. **Private stays private.** Local-only context lives under gitignored `docdoki/private/`. Public documents and public answers never depend on or expose private content. Never store credentials in either scope. See [Privacy](references/privacy.md).

## Ordinary work

1. **Orient:** Read `northstar.md`, `overview.md`, and the relevant `specs/`, active `work/`, and `notes/`. In larger repositories, run the bundled lookup script (resolving `<skill-dir>` to the canonical `docdoki` directory) to find every spec, active work stream, and note matching a code path:
   ```sh
   python3 <skill-dir>/scripts/validate.py <unit-path> --for src/path/to/file.py
   ```
2. **Respect authority:** Implement within authorized scope using decided specs (`status: decided`, the default). Treat `status: proposed` specs and undecided options as proposals until confirmed. Surface material missing decisions in `overview.md` under `## Open decisions` rather than inventing binding policy.
3. **Verify honestly:** Run checks appropriate to the claim and record scope and limits.
4. **Maintain affected records:** Update affected contracts (if design changed within authority), active `work/` state, affected spec `progress`, and durable `notes/`. Do not mirror per-spec summaries or active checklists into `overview.md`—update each fact in its authoritative home.
5. **Validate mechanics:** Whenever document paths, frontmatter, links, or visibility change, run:
   ```sh
   python3 <skill-dir>/scripts/validate.py <unit-path>
   ```

## Focused workflows

Natural-language intent selects the workflow; read the relevant section of [Operations](references/operations.md) when needed:

| Workflow | Use |
| :--- | :--- |
| **Setup** (`init` / `adopt`) | Initialize a new library or adopt an existing repository without confusing observed code for decided intent. |
| **Reconcile** (`follow` / `challenge`) | Propagate human edits/commits or audit and repair conformance drift between contracts and code. |
| **Lifecycle** (`work`, `handoff`, `close`, `groom`) | Manage active work streams, produce cold-start handoffs, route durable knowledge on closure, and prune low-value noise. |

## Optional panel

Launch directly without installing files into the project:

```sh
python3 <skill-dir>/panel/panel.py <unit-path>
```

See [Panel model](panel/panel-model.md) for the optional steering board and local editor. Only copy `scripts/panel_launcher.py` into `<unit>/docdoki/panel.py` when the user explicitly wants a project-local launcher.
