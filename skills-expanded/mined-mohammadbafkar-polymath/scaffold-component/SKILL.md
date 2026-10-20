---
name: scaffold-component
description: Generate a component/service/module in the CURRENT repo per its conventions — native generator first (tool-spec handoff), canonical infra bodies from owning skills, no freehand boilerplate.
---

# scaffold-component

> A new component should look like the team wrote it: the project's
> conventions decide the shape, the stack's own generator produces the
> boilerplate, and infra files come from the skills that own those
> formats. The model's job is composition, not invention.

## When to use

- "Add a new service/module/package/handler like the existing ones."
- A repo with `.polymath/` localization needs a new component that must
  match house conventions.

Not for authoring Polymath plugins/skills (`new-plugin`, `new-skill`,
`new-pack`) — this scaffolds in the *user's* project.

## Procedure

1. **Load the conventions (convention-driven, not vibes).** Read the
   project snapshot (`polymath-core:project-context`): `stack`, then the
   `conventions_docs` roles that govern shape — `knowledge-base`,
   `backend-stack`/`frontend-stack`, `shared-libraries`, `deployment`.
   Mirror an existing sibling component's layout when one exists; name
   per the conventions (treat `[VERIFY: …]` content as unconfirmed).
   No `.polymath/`? Say so and mirror the closest sibling instead.
2. **Tool-spec handoff first.** If the stack has a native generator
   (`dotnet new`, `npm create` / `yarn create`, `cargo new`,
   `django-admin startapp`, `mvn archetype:generate`, a repo-local
   generator named in the conventions docs, …), compose the exact
   command + flags — the spec — show it, and run THAT. Hand-write only
   what no tool generates. Never reimplement a generator's output by
   hand.
3. **Canonical infra bodies.** For infra files the generator doesn't
   produce, delegate to the skill that owns the format instead of
   freehanding: Dockerfile → `polymath-devops:dockerize`, CI workflow →
   `polymath-devops:ci-pipeline-github`, K8s manifests →
   `polymath-kubernetes:write-manifest` — each already consumes the
   project's `deployment` conventions.
4. **Wire the test scaffold** per `stack.testing` (framework, layout
   mirroring siblings) with one real starter test — not an empty file.
5. **Register, never overwrite.** Add the component where the
   conventions require (solution file, workspace globs, knowledge-base
   doc's component table). If any target file already exists, stop and
   show the conflict — scaffolding never overwrites.
6. **Close the loop.** If the component adds tools or env vars, update
   `setup` in `.polymath/project.yaml` and regenerate the onboarding
   checklist: `python3 "${POLYMATH_PLUGIN_ROOT}/bin/gen-prerequisites.py"
   --out docs/onboarding/prerequisites.md`. Finish with a summary:
   generator command used, files created, conventions applied,
   follow-ups.

## Quality bar

- An existing teammate couldn't tell this component from a hand-built
  one — naming, layout, and registration all match the conventions.
- Boilerplate came from the native generator; infra bodies from their
  owning skills; nothing freehanded that had a canonical source.
- Nothing overwritten; every created path listed in the summary.
