# KOTA

KOTA uses repo-local docs, project data files, and directory-level `AGENTS.md` files to
explain structure, standards, current priorities, and how work moves through
the repo.

- Before broad work, read parent `AGENTS.md` files up to the mono root; nearest scoped instructions apply last.
- Before broad KOTA changes, read `docs/STANDARDS.md` and `docs/ARCHITECTURE.md`.
  Standards owns the engineering and verification conventions; scoped guidance
  specializes ownership and roles.
- Before touching data files or task state, read `data/AGENTS.md` and `data/tasks/AGENTS.md`.
- When touching a directory, read its local `AGENTS.md` first if present.
- Keep docs, data files, and local `AGENTS.md` files aligned with reality.
- Native CLI agents receive read-only Git metadata. Workflow runtime owns index
  staging and commits; agents must not write Git metadata directly.

@docs/STANDARDS.md
