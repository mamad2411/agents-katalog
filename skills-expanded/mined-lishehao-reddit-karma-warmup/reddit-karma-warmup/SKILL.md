---
name: reddit-karma-warmup
description: Run authorized Reddit research, browsing, native posts, comments, follow-up, and profile/community work through one persistent user-visible Reddit operating task and the user's logged-in Chrome. Use when a user asks to operate, warm up, publish to, research, or monitor a Reddit account or community.
---
# Reddit Community Operations
## Startup state machine
Treat an HTTPS install/upgrade request as the start of one intake flow:

1. Fetch/validate the raw or codeload Skill, run `scripts/resolve_remote_sync.py --apply`, read back the installed tree, and rerun the validator before `BOOTSTRAP_READY`. Compatible differences apply atomically (`HOT_REPLACED`, `HOT_REPLACED_SAME_VERSION_DRIFT`, `NOOP_ALREADY_SYNCED`, or `REMOTE_OLDER_IGNORED`); defer only for incompatible schema, unsettled mutation, or `UNCERTAIN` runtime facts, recording `REMOTE_NEWER_DEFERRED`. Before `BOOTSTRAP_READY`, resolve the current task ID and rename/pin it as `Reddit 运营台`; read back when supported. This presentation step is allowed during bootstrap; do not open Chrome/Reddit, research, or create mission/queue/Heartbeat yet.
2. Detect a complete direct target assignment before showing the intake form. It must contain 1–32 target post URLs, explicit units/actions, and a duration. Compile it with `scripts/compile_startup_intake.py`; `DIRECT_TARGET_ASSIGNMENT_COMPLETE` skips the four canonical questions and starts the first formal round. A partial assignment gets one concise direct-text reminder and no mission; do not invent missing data.
3. Otherwise call Codex `request_user_input` exactly once in this same task turn, without `autoResolutionMs`, using the three visible prompts in [startup intake](references/startup-intake.md): duration, operating direction, and combined action scope/rhythm. Normalize the third answer to four canonical fields. Do not ask for an account name or handle. Wait live; do not defer to Heartbeat or report startup complete while waiting. On unanswered/partial/dismissed/expired, send the prescribed normal text response listing all four canonical questions and remain `WAITING_FOR_STARTUP_INPUT`.
4. Persist the answers or direct assignment and run the compiler. Only `STARTUP_ANSWERS_COMPLETE` or `DIRECT_TARGET_ASSIGNMENT_COMPLETE` continues; do not ask a second round. In that same task turn run `current-task scope -> envelope -> one Chrome/session gate -> INITIAL packet`. The current task was already renamed/pinned during bootstrap; presentation failure is non-blocking. `INITIAL` is formal round one, not a preview or pre-filter, and must do real work immediately. Heartbeat creation/readback is advisory and never blocks INITIAL.
Use the current task as the authority. Resolve the exact current Codex task ID
from the current task context before compiling anything. A
`<source_thread_id>` inside a delegated wrapper is provenance only; it is the
parent/creator task and MUST NOT be used as this task's owner ID. The queue
owner, mission owner, Heartbeat target, and finalization target must all equal
the exact current task ID. The current task context is the only identity
source. If the runtime exposes a parent/source ID instead of the current ID,
keep the source as provenance and use the task's own ID for queue/Heartbeat
fields; do not perform a cross-task search to resolve it.
Inspect only its own mission/queue and
its own Heartbeat when one already exists. Do not scan other tasks, other
Heartbeats, other environments, locks, or historical handoffs. If this task
has no mission yet, create its queue after the four answers; do not block on
an unrelated runtime. `scripts/runtime_fence.py` remains an explicit
diagnostic tool, not a startup-wide scan.
## One task, five internal units
Run one present Reddit operating task. It owns one mission record, one queue, an
advisory Heartbeat when available, one Chrome binding, and one primary Reddit
tab; session-bound work claims a visible user Chrome tab first, while temporary
tabs are recovery-only and do not prove login. Never create unit tasks, a
browser dispatcher, a lock daemon, or a second Chrome owner.
| Unit | Owns | Never owns |
| --- | --- | --- |
| `browsing` | qualified reads and candidate packs | publication, replies, profile changes, votes |
| `comments` | candidate research and proactive comments | posts, replies, profile changes, votes |
| `posts` | rule-qualified native posts using truthful material | comments, replies, profile changes, votes |
| `follow-up` | default account-maintenance hook: own-profile negative-score cleanup; with follow-up authority, also sweep own posts/comments, notifications, known permalinks, and authorized replies | unrelated discovery, new posts, profile bio/membership changes, votes |
| `presence` | explicit truthful profile/community/flair changes | publication, replies, votes |
Default authority is research-only. The scheduler always keeps the `follow-up`
maintenance hook active; it is not a startup question or reply authorization.
It checks own posts and hides/deletes score `-2` or below with reload
verification; `全面推进` additionally sweeps all eligible own conversations.
Voting is removed; legacy `vote_policy` only normalizes to `DISABLED`.
## Surface contract
| Surface | Use | Never treat as |
| --- | --- | --- |
| Built-in Web Search | broad current discovery, terminology, primary sources, duplicate/FAQ risk | current Reddit permission or action proof |
| Official Reddit API via `scripts/community_index.py` | optional GET-only public community metadata, rules, and up to three hot pointers | browsing, account access, writes, or a Chrome fallback |
| Logged-in Chrome | every real Reddit read, live rule/session/composer gate, action, and verification | parallel task control or evasion |
Missing API credentials are normal. Start with Old Reddit for ordinary text work and use one equivalent current-Reddit fallback only when the required live capability is absent. A content timeout is `CHROME_CONTENT_CHANNEL_TIMEOUT`, not a disconnect, missing tab, session risk, or `RULE_BLOCKED`; follow [Chrome and actions](references/chrome-and-actions.md).
Global community exclusion: `r/saas`; never search, open, read, index, comment, post, follow up, or change presence there. Drop it from discovery results and reject any direct target or handoff that normalizes to `r/saas`; this does not block the rest of a mission.

## Mission loop
1. Resolve and record the exact current task ID (never the delegation
   `source_thread_id`), then compile one immutable envelope and queue. The task
   was renamed and pinned during bootstrap; presentation failure is non-blocking.
   Store the business goal, community scope, coverage budget, soft action
   threshold, action budget, truthful material references, and evidence/output
   targets. `低 / 标准 / 高` changes workload profiles, not the timer. Scope controls what
   units may act; rhythm controls how much each enabled unit attempts.
2. Establish one readable same-Chrome session gate. Do not create a separate
   neutral canary tab just to prove the browser. Start INITIAL as soon as this
   gate passes. In parallel, make a best-effort 15-minute Heartbeat attempt;
   use the existing DTSTART/UNTIL/COUNT fallback once, record any failure, and
   retry later without blocking current-task work.
   The prompt carries only stable identity/boundaries and
   `runtime_protocol_version`; each wake reloads this installed Skill and queue.
3. Run the formal `INITIAL` packet immediately. For any outward-authorized
   mission, `INITIAL` and every later formal round are action-first: attempt one
   authorized public action before finishing the round. Comments are the default
   first lane when enabled; browsing-only missions may finish as research-only.
   Later wakes may record `heartbeat-observe` when available, then decide
   `RUN|WATCH|SKIP|DEFER` for due units. A normal wake runs one Chrome packet;
   a wake delayed more than five minutes may run up to three packets sequentially
   for currently due units, never concurrently. The queue opens the next
   selected packet after a completed one; keep working until the wake is settled.
   Comments/posts may submit up to two distinct actions, while
   follow-up may batch up to five verified own permalinks and drain its own
   hourly cap; follow-up does not consume the new comment/post/presence action
   cap. ±10 minutes is normal. A delayed wake expands work; no catch-up
   means no replay of missed packets or mutations. A fast NOOP is only for
   early/duplicate, recovery, or genuinely exhausted/parked work; scheduler uncertainty
   or a missing observation is not a reason to skip current-task work.
4. Action units may find their own target in the same packet. In `discover` or `seeded_expandable`, rotate through five distinct communities (four if a route fails) before repeating one; this is a routing target, not a filler quota. Browsing candidate
   packs and atomic `handoff` remain useful but are optional; a candidate pack is
   not a reason to end an action-authorized round. On an expanded late wake,
   mark useful currently due units `RUN` up to the reported packet slots, then
   process them in priority order. Link work through recorded evidence;
   verified own permalinks arm follow-up. An
   `ACTION_ELIGIBLE` unit outranks more browsing. The follow-up maintenance
   hook runs hourly when due and its cleanup is separate from public-action quotas.
   For comments, continue across
   new targets (up to 60 target reads) until the first compliant target is found;
   under an active action budget, continue to a second distinct target after
   the first verified action until the packet or hourly cap is reached. Only
   cutoff, no authority, a content-channel failure, a visible blocker on every tested target, no truthful contribution after the expanded search, or an uncertain submission justifies a no-action round. Record failed self-selected candidates locally;
   use `candidate-reject` for a handoff-supplied target; do not turn either
   into mission-wide `RULE_BLOCKED` or `MATERIAL_REQUIRED`. An archived/locked
   target is `TARGET_ARCHIVED`/`TARGET_LOCKED`, not an account ban;
   discard it and continue. A runtime read failure is `LIVE_GATE_UNVERIFIED`; the
   next wake must create/claim one fresh agent-owned tab and run one real content
   probe before continuing or yielding the same unit. URL-only checks/finalize
   do not count; retry later and never permanently park a due unit. A yielded
   unit may leave the late wake's remaining serial slot(s) for independent due
   units; it never authorizes resending the uncertain action.
5. Comments use a minimal action path: target/nearby context, one visible rule or submit signal, and composer. Fold truth and relevance into the comment; do not require account history, quality scoring, or broad research. Use zero Web Search queries unless a factual/technical/unfamiliar claim needs one.
   Same-target duplicate checking is enough. Posts keep the 4-8 query research pass and fuller rule, truth, duplicate, format, Flair, session, and submit gates.
6. Before every public action persist deterministic `MUTATION_INTENT` and
   `action_key`. Submit once and verify separately; if it stays `submitting...` with no echo,
   allow one same-target refresh/read, never a second submit. Freeze uncertain exact keys
   permanently; never reopen or retry them. Before drafting, read the bounded per-account recent-public-content library with `scripts/recent_public_content.py` and rewrite exact or template-similar
   text; comments and follow-up replies stay short, while posts may use a concise title plus a 40–120-word body (hard maximum 180 words/eight lines) when context is needed. After independent verification append the new item. At completion/deadline enter `FINALIZE_ONLY`,
   release only owned tabs, delete the exact Heartbeat with proof, retire the queue, and keep the visible operating task available. Runtime receipt tokens are opaque; envelope re-hashing is diagnostic-only (`REDDIT_STRICT_INTEGRITY=1`).
## Load only what the current decision needs
| Situation | Reference |
| --- | --- |
| intake | [startup intake](references/startup-intake.md) |
| mission, timer, recovery, retirement | [single-owner runtime](references/single-owner-runtime.md) |
| Web Search, API index, community/candidate evidence | [research and community index](references/research-and-community-index.md) |
| Chrome and action boundaries | [Chrome and actions](references/chrome-and-actions.md) |
| selected unit | [unit guides](references/unit-guides.md) |
| goal, KPI, coverage, threshold, scope | [mission goals and profiles](references/mission-goals-and-profiles.md) |
| numeric/script defaults | [operation defaults](references/operation-defaults.json) |
Do not load historical lane, dispatcher, worker, callback, or migration files. Compact receipt:
```text
本轮完成：<完成/暂停/阻塞的单元、有效阅读、已验证动作>。
下轮时间：<当地时间与 UTC；终止则“无（Heartbeat 已删除）”>。
下轮计划：<下一个单元或恢复动作，以及真实风险>。
```
