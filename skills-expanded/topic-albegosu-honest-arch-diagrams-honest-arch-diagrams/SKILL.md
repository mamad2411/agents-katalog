---
name: honest-arch-diagrams
description: >-
  Draw honest service-topology and request-path diagrams. Use when mapping how a request
  reaches a service, or turning manifests/traces into an architecture sketch. Separates the
  verified path from inferred companions; never invents components. Not for C4, theming,
  namespace maps, or file inventories.
license: MIT
metadata:
  author: Alberto Gonzalez
  version: "0.11.1"
---

# Honest architecture diagrams

A request-path diagram is only useful if the reader can trust it. This skill produces
diagrams where every element is auditable: is it observed or inferred, and on what
evidence? Prefer an incomplete honest diagram over a complete confident guess.

## When to use

- "Diagram how a request reaches this service / pod."
- "Map this service and its dependencies."
- "Turn these manifests / this repo / this trace into an architecture sketch."

## When NOT to use

- C4 System/Container/Component docs → use a C4 skill.
- "Make it look beautiful," theming, export pipelines → use Archify.
- File-level or symbol-level inventories → use ArchPresent.
- A whole namespace / multi-app map → pick **one** app and draw its request path; other
  co-located workloads are `around` companions, not a second spine.

## The one rule

**Never draw what you did not observe.** A hop you did not verify is absent, not guessed.
A dependency you inferred is a *companion*, drawn differently from the path, and it carries
its evidence. See `references/honesty-rules.md` — this is the core of the skill.

## Hard constraints (do not skip)

1. **One app per model.** `app` names a single service under study. One verified spine. Do
   not put two Services / two Pods on the same path just because they share a namespace.
   Other apps in the release are `around` companions (or a separate model).
2. **Prefer adapters + lint + layout.mjs.** Default deliverable is:
   `<app>.model.json` → `node scripts/lint.mjs` → `node scripts/layout.mjs … --svg`.
   Do **not** default to Mermaid. Mermaid is a last-resort fallback only when the user
   explicitly asks for it or Node cannot run. D2 is optional themeable output, not a
   substitute for skipping the model/lint.
3. **Evidence on every element.** Hops and companions carry a non-empty `evidence` string.
   Put linked evidence in edge labels when rendering.

## Workflow

1. **Gather evidence.** From the description, repo, manifests, or telemetry, collect only
   facts: which hops are on the path, which dependencies have concrete evidence
   (env host, Secret *name*, ConfigMap host, declared server). Never read Secret values.
   When a real source exists, skip hand-building and derive the model from it (paths are
   relative to this skill directory). Pass `--app <name>` when the dump contains more than
   one service (required for honest single-spine diagrams):
   - Kubernetes: `kubectl get ingress,svc,endpoints,deploy -n <ns> -o json > d.json` then
     `node adapters/k8s/from-k8s.mjs d.json --app <name> --out <app>.model.json`.
   - GitOps / Helm-rendered manifests (YAML or JSON, file or dir): 
     `node adapters/gitops/from-gitops.mjs <path> --app <name> [--values values.yaml] --out <app>.model.json`.
   - Terraform: `terraform show -json > t.json` then `node adapters/terraform/from-terraform.mjs t.json --app <name> --out <app>.model.json`.
   - OpenAPI (JSON or YAML): `node adapters/openapi/from-openapi.mjs <spec>.json|.yaml --out <app>.model.json`.
   - Traces (OTel JSON or simplified spans): `node adapters/trace/from-trace.mjs <trace.json> --app <name> --out <app>.model.json`.
   - Docker Compose: `node adapters/compose/from-compose.mjs <compose.yaml> --app <name> --out <app>.model.json`.
   Or use the unified CLI: `node scripts/cli.mjs from-compose <compose.yaml> --app <name>`.
   Each source carries different evidence strength (runtime trace/k8s > infrastructure >
   declared); keep that in mind when reading the result.
2. **Build the model.** Fill `{ hops[], edges[], companions[] }` per
   `references/data-model.md` for **one** `app`. Stamp each element with `evidence` and,
   for companions, `relation` (`linked` = evidence-backed edge; `around` = co-located by
   release/owner).
3. **Apply the honesty rules.** Drop any element that fails them. Cap companions (default 8);
   put the surplus in `overflow: { count, note }` instead of padding the canvas. Save the
   model as `<app>.model.json` and validate it before rendering:
   `node scripts/lint.mjs <app>.model.json`. Fix every reported violation. **Do not render
   until lint passes.**
4. **Lay out.** Assign lanes (Edge / Gateway / Identity / App / Workload / Data) and route
   edges per `references/visual-grammar.md` and `references/layout.md`.
5. **Render (default).** Run the bundled reference layout and present the SVG:
   `node scripts/layout.mjs <app>.model.json --svg <app>.svg`
   That enforces Data under Workload and orthogonal elbows. Only if the user asks for D2,
   generate it with `node scripts/to-d2.mjs <app>.model.json --out <app>.d2` (see
   `references/rendering-d2.md`). Mermaid only as an explicit last resort (see Hard
   constraints). Accent only the verified path.
6. **Self-check.** Run the checklist below before presenting.

## Self-check (must all pass)

- [ ] Exactly one app / one spine; no second service on the path.
- [ ] Delivered `.model.json` + lint PASS + `layout.mjs` SVG (unless the user forbade Node).
- [ ] Did **not** default to Mermaid.
- [ ] Every hop on the path has evidence; nothing was added "to look complete."
- [ ] `linked` companions have a concrete evidence string; `around` companions say
      "also in this release," not "called by."
- [ ] No companion sits on the request path or in the arterial/accented edges.
- [ ] No TLS/auth/datastore hop was invented from a name guess.
- [ ] Companion count is within the cap; extras are in `overflow` (`+N more`), not faked.
- [ ] If rendered with motion, it respects `prefers-reduced-motion`.

## References

- `references/honesty-rules.md` — the invariant. Read first.
- `references/data-model.md` — the `{hops, edges, companions}` shape + fields.
- `references/visual-grammar.md` — lanes, stacking, accent, satellites.
- `references/layout.md` — ranking, orthogonal elbows, the hop-arc.
- `references/rendering-d2.md` — D2 output patterns (+ Mermaid last-resort notes).
- `scripts/layout.mjs` — **default** renderer; lane packer + elbow router; emits SVG.
- `scripts/to-d2.mjs` — optional model → D2 generator (accented path, dashed companions).
- `adapters/k8s/from-k8s.mjs` — derive a model from a Kubernetes JSON dump (evidence, no secret values). Pass `--app` on multi-service dumps.
- `adapters/gitops/from-gitops.mjs` — derive from declared YAML/JSON manifests (GitOps / Helm-rendered).
- `adapters/terraform/from-terraform.mjs` — derive from `terraform show -json` (around by default, linked on reference).
- `adapters/openapi/from-openapi.mjs` — derive from an OpenAPI 3.x JSON or YAML document (declared `x-depends-on` only).
- `adapters/trace/from-trace.mjs` — derive from OpenTelemetry / span JSON (observed path).
- `adapters/compose/from-compose.mjs` — derive from docker-compose.yml (declared services).
- `scripts/diff.mjs` — compare two models (added/removed/changed).
- `scripts/cli.mjs` — unified `honest-arch` entry (`lint`, `layout`, `to-d2`, `diff`, `from-*`).

## Example

See the repo's `examples/checkout-service.model.json` (illustrative D2 beside it;
prefer `scripts/layout.mjs` for the grammar-exact SVG).
