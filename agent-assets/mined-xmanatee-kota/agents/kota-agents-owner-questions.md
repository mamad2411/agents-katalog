# Owner-Questions Module

Surfaces the `kota owner-question` CLI and HTTP routes for the owner
question queue — the mechanism agents use to escalate high-stakes decisions
they cannot responsibly resolve alone.

The queue state and review gate live in `src/core/daemon/` as shared runtime
primitives. This module is the operator surface: listing pending questions,
answering, dismissing, and exposing the same actions over HTTP so clients
beyond the local CLI can handle escalations.

Workflow-authored dismissals use their owning workflow's synchronous successful
finalization hook and the queue's pending-only dismissal API. They retain the
question revision they observed, preserve newer or terminal owner responses,
and stage notification events through the run's transactional publication API.

The module contributes two HTTP surfaces against the selected scope's
`OwnerQuestionQueue`: the public `/api/owner-questions*` routes
through `KotaModule.routes` for the user-facing `kota serve` server, and the
daemon-control `/owner-questions*` routes through `KotaModule.controlRoutes`
(`read` scope on `GET /owner-questions`, `control` scope on the two POSTs)
for token-authenticated operator clients. Both surfaces collapse to one local
helper family in `routes.ts` so the wire contract — list/answer/dismiss
envelopes, the missing-answer 400, and the missing-or-resolved 404 — has a
single implementation.
Route registrations resolve the daemon scope provider through their
`ModuleContext`; the runtime loader's provider registry is the authority for
multi-scope queue selection. The process singleton remains only the local,
unscoped fallback.

Every answer surface — `kota owner-question answer/dismiss` (CLI/HTTP),
inline-keyboard buttons in Telegram, and free-form Telegram chat replies
that target the delivered owner-question message — calls the same
`OwnerQuestionQueue.answer(id, text, source)` API. The only difference is
the typed `resolutionSource` label recorded on the resolved question:
`http` for CLI/HTTP, `telegram-inline` for inline-keyboard selections,
and `telegram-reply` for free-form chat replies. New surfaces should pick
a distinct source label rather than reusing or aliasing an existing one
so answer-source attribution stays usable.
