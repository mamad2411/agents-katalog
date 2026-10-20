# Web Client

React app built with Vite, TanStack Query, Tailwind CSS, and shadcn/ui.

- Consumes only the daemon HTTP+JSON API and SSE event stream.
- No direct `.kota/` file access.
- Build output (`dist/`) is served by the daemon's HTTP server.
- Run `pnpm build` to produce the static assets before starting the daemon.
- During development, `pnpm dev` starts a Vite dev server that proxies API requests to `http://127.0.0.1:3000`.
- Voice goes through `/api/voice/transcribe` and `/api/voice/synthesize` —
  never through a vendor SDK in the browser. Microphone capture uses
  `MediaRecorder`; playback uses `HTMLAudioElement`.

## Directory-Scope Routes And Queries

The daemon hosts one or more directory-scope runtimes. The web client consumes
the canonical `ScopeRegistryProjection` from `/identity` and uses `scopeId` on
every scoped daemon request.

- The active scope lives in `ScopeContext` (`src/lib/scope-context.tsx`) and is
  encoded into the URL hash as `#s/<scopeId>/<sub-route>`. The `s/<scopeId>`
  prefix is owned by the context; everything after it is scope-local navigation.
  The live dashboard uses `surface/<surfaceId>` for daemon-graph navigation.
  Hash-based routing is the convention here — no client-side router library.
- Every directory-scope TanStack Query key starts with the scopeId
  (`["sessions", scopeId]`, `["ui-surfaces", scopeId]`) so
  the cache cannot leak rows across scopes by construction. Keys are
  produced by the factories in `src/api/queries.ts`; mirror that shape when
  adding a new query rather than inventing a parallel key form.
- Scoped routes call `api.<x>(scopeId, …)` from `src/api/client.ts`, which
  appends `?scopeId=<id>` to the daemon path.
- The header `ScopeSelector` (`src/components/sidebar/ScopeSelector.tsx`)
  hides itself when the projection has exactly one directory scope, so the
  KOTA-on-itself experience is unchanged.
- The SSE transport selects the same scopeId as queries. Daemon live delivery
  and replay share scope filtering; omitted selectors retain the global operator
  stream. Only declared daemon-wide event types may omit payload scopeId, with
  that classification generated from the daemon contract for browser filtering.
  Retired connections cannot deliver callbacks, and scope changes start a fresh
  subscription and cursor. The shared
  graph's `refreshEvents` and log-stream event types own surface invalidation
  and live log subscriptions; non-graph queries keep their narrow typed
  handlers. The selector's reactive `scopeId` drives both query keys and
  subscriptions, so switching scopes re-fetches every scoped
  surface and never bleeds rows or stream entries from the prior selection.
- Tests render directory-scoped components inside `<TestScopeProvider>`
  (in `src/lib/scope-context.test-utils.tsx`) instead of stubbing a fake
  identity payload through `fetch`.

## Verification ownership

Retain platform navigation, accessibility, interaction, trust, confirmation,
rendering, and transport boundaries. Shared resource transitions and generated
wire shapes are proved at their owner; do not repeat their matrices per screen
or enumerate fixture catalogs. Client composition journeys keep production
providers, navigation, and transport, with doubles only at network and device
ports. Pure view construction is compiler proof, not rendered evidence.
