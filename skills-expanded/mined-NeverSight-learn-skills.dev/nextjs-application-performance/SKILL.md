---
name: nextjs-application-performance
description: Design, measure, implement, review, and migrate Next.js application performance across App Router data paths, rendered UI, pnpm workspaces, compiler graphs, standalone output, user-perceived business actions, and production containers. Use for RSC pages, Route Handlers, Server Actions, TanStack Query/Table, growing collections, pagination, caching, N+1 queries, payload size, rendering bounds, sticky headers, nested scroll containers, overlay clipping, real-user monitoring (RUM), session replay analytics, Microsoft Clarity masking, click-to-ready or business-action latency, page navigation response time, Web Vitals, TTFB, build OOM or RSS, serverExternalPackages, webpack externalization, pnpm symlinks, server/client package boundaries, standalone dependency closure, Dockerfiles, or Docker Compose deployment for Next.js.
---

# Next.js Application Performance

Keep Next.js applications responsive and scalable across data access,
transport, rendering, user-perceived actions, and production runtime without
trading away authorization, correctness, or URL-addressable state.

## Resolve Project Behavior

Select one task: `design`, `implement`, `review`, `migrate`, or `monitor`.
Before acting, resolve the current repository's instructions:

```bash
uv run python .agents/skills/nextjs-application-performance/scripts/resolve.py --task <task>
```

Read the returned `instructions.path` whenever `instructions_id` changes.
Without a project profile, follow the generic task reference. Project profiles
may set page sizes, framework adapters, audit commands, and authoritative
documents, but cannot weaken the invariants below.

Read [project_config.md](references/project_config.md) when creating or
materially changing a project profile or resolver task.

## Non-configurable Invariants

- Classify every displayed collection as fixed/bounded or potentially growing.
- A growing collection must be bounded at the data source with pagination,
  cursoring, or an explicit window; client-side slicing is not data pagination.
- Apply authorization, filters, and a stable sort before the bound. Add a
  unique tie-breaker to every pageable sort.
- Do not load an unbounded collection in an RSC, Route Handler, Server Action,
  client query, or serialization boundary only to filter, map, or slice it.
- Avoid N+1 relation reads; use a projection, batch lookup, or aggregate that
  is bounded by the current page.
- Treat cursor tokens as opaque and validate all public query parameters with
  a allowlist and bounded values.
- Reuse the shared interactive select/combobox for both a remote candidate
  query and its committed selection. Its search text is transient UI state;
  it may drive a debounced, paged query but must not update the business value
  until an option is committed. Do not compose a separate search input and
  select for the same field.
- Declare one vertical scroll owner for every rendered data surface. Do not let
  a shared or third-party table silently add a viewport-sized nested scroller;
  sticky headers and virtualization must preserve the surrounding shell's
  scroll contract.
- Audit the rendered container styles of third-party table/grid adapters,
  including generated `height`, `max-height`, `overflow`, and overscroll
  behavior. Shared adapters own these defaults; do not repair them with
  consumer-specific CSS.
- Treat every new or changed clipping or scroll container as an overlay
  boundary. Inventory menus, popovers, comboboxes, tooltips, and other floating
  descendants. Let a shared overlay primitive own its portal and positioning,
  or prove that the floating content is intentionally contained; `z-index`
  cannot escape an ancestor's overflow clipping.
- Verify the query shape and data boundary with focused tests. A rendered UI
  page alone is not evidence that the backend read is bounded.
- Verify scroll geometry in a real browser when sticky headers, virtualization,
  nested overflow, viewport-relative sizing, or floating descendants can
  change scroll ownership, clipping, or overlay position.

## Production container builds

When a Next.js Dockerfile or Compose deployment is in scope, automatically
move production builds into the Dockerfile. Do not leave `next build`, `pnpm
build`, or equivalent commands in a long-running service's `command` or
`entrypoint`.

- Use a multi-stage Dockerfile: dependency installation, build, then a minimal
  runtime stage. Preserve lockfile-based, reproducible dependency installation.
- Enable and use Next.js standalone output when it fits the application. Copy
  the actual standalone server and required static/public assets into the
  runtime stage; derive monorepo paths from the build output instead of
  assuming a single-app layout.
- Make the runtime command start the built server only. Keep development
  overrides on `next dev`; do not make development behavior the production
  image contract.
- Keep runtime configuration injectable at container start. Do not bake
  secrets into image layers. If a public build-time variable is required,
  declare and document it explicitly.
- Run the Compose guardrail check when available, then render the production
  Compose model. Validate the image build and start the resulting runtime
  container before handoff.
- In a pnpm workspace, resolve every direct workspace dependency from the app
  and record both its symlink path and realpath before changing transpilation
  or externalization. Classify it as `server`, `client`, or `hybrid` from its
  public entrypoints. Never externalize a whole `client` or `hybrid` package.
- Treat a root barrel that reaches both a server-only module and a client
  module as a boundary defect. Split public subpath exports before admitting
  server-only externalization; tree shaking is not a server/client contract.
- Audit the produced standalone tree as an isolated production dependency
  closure. A dependency that resolves only by walking into the source
  workspace is missing from the artifact.
- Keep application roots as runtime build boundaries. Runtime-capable source
  in one application must not import sibling application source, package
  manifests, or build configuration for fallback metadata. Read metadata from
  the current app, generated build metadata, or startup environment instead.
- Do not repair a standalone closure by copying a sibling application, the
  whole workspace, or development dependencies into the runtime artifact.
  Repair the import/trace owner and regenerate the artifact.
- Measure a cache-cold production build inside the declared container memory
  limit. Preserve peak RSS, exit code/signal, cgroup OOM deltas, and the
  classified exit reason. The probed process must see the exact finite
  `memory.max`; an outer BuildKit-daemon limit does not admit a sandbox that
  reports `max`. Exit `137` alone is not OOM evidence.
- Do not use a larger V8 heap, `resolve.symlinks = false`, or
  `optimizePackageImports` as an unevidenced default repair. Require a
  before/after experiment tied to the observed failure and keep the real
  container gate unchanged.
- Read [production-builds.md](references/production-builds.md) whenever pnpm
  resolution, compiler memory, Next externalization, standalone output, or a
  production runtime image is in scope. Run every project-declared build
  contract command, including runtime smoke routes, before handoff.
- Treat the final structured build-gate result as authoritative. Invoke the
  build contract, closure, and standalone smoke commands with `--json`; consume
  that invocation's `status` and `reason`, and never reclassify it from earlier
  or accumulated stdout/stderr.

## Task Flow

1. Resolve instructions and use the selected task reference.
2. For a data surface, inspect the path from request URL through authorization,
   Repository/ORM query, projection, response/RSC, and UI. State the collection
   classification and first incorrect unbounded decision.
3. For user-perceived monitoring, define the stable business action, explicit
   start and completion conditions, terminal results, privacy boundary, and
   focused verification before selecting instrumentation. For Microsoft
   Clarity or another session-replay surface, also read
   [clarity-masking.md](references/clarity-masking.md) before changing the root
   layout, masking mode, or sensitive rendered values.
4. Keep reusable method in the reference and repository-specific policy,
   commands, and authoritative sources in the profile.
5. When a project declares an overlay contract manifest, run
   `scripts/audit-overlay-contract.mjs` as a deterministic source/config gate
   and use `scripts/overlay-geometry-probe.mjs` to generate the page expression
   for real-browser geometry evidence.
6. Run the smallest relevant focused test first, then configured static, type,
   integration, browser, and E2E checks in proportion to the changed boundary.
7. Report the relevant data bound or measurement contract, UI behavior,
   runtime implications, verification, and remaining performance limits.

## Resources

- [design.md](references/design.md): choose offset pages, keyset cursors,
  search pages, or bounded summaries before implementing a data contract.
- [implement.md](references/implement.md): implement the data/API/RSC/UI path
  without moving the unbounded read to another layer.
- [review.md](references/review.md): find unbounded reads, N+1 queries, and
  misleading client-only pagination.
- [migrate.md](references/migrate.md): inventory and safely convert legacy
  whole-collection surfaces.
- [monitor.md](references/monitor.md): measure user actions from explicit
  intent until the business result is visible and usable.
- [clarity-masking.md](references/clarity-masking.md): preserve useful Clarity
  recordings while keeping sensitive values out of session replay.
- [project_config.md](references/project_config.md): project profile schema,
  resolver behavior, and validation requirements.
- [production-builds.md](references/production-builds.md): pnpm realpath,
  server/client/hybrid package, Next externalization, standalone closure,
  constrained cold-build, and runtime-smoke contract.
- `scripts/audit-overlay-contract.mjs`: validate project-owned overlay source,
  focused-test, CSS ownership, and geometry-probe contracts.
- `scripts/overlay-geometry-probe.mjs`: generate a self-contained browser-page
  expression for portal, viewport, clipping-ancestor, position, and focus
  checks without adding a browser test framework dependency.
- `scripts/audit-next-build-contract.mjs`: verify workspace resolution,
  package boundaries, external-package admission, and forbidden defaults.
- `scripts/audit-standalone-closure.mjs`: verify that runtime imports resolve
  inside the standalone artifact.
- `scripts/run-build-memory-probe.mjs`: run a cache-cold build only inside the
  declared cgroup v2 limit and record RSS/exit evidence.
- `scripts/smoke-next-standalone.mjs`: start the standalone server and verify
  the project-declared runtime routes.
