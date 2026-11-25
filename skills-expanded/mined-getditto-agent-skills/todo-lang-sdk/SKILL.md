---
name: TODO-lang-sdk
description: >
  Use ONLY for the Ditto TODO_LANGUAGE SDK (not TODO_OTHER_EIGHT — each has its own
  skill). Builds and troubleshoots Ditto TODO_LANGUAGE apps on TODO_PLATFORMS. Triggers
  on TODO_FILE_EXTENSIONS, TODO_BUILD_FILE_NAMES, TODO_PACKAGE_COORDINATE,
  TODO_API_NAME_1, TODO_API_NAME_2, TODO_OBSERVED_ERROR_STRING.
  Ditto SDK 4.14.x, 5.0.x, 5.1.x, 5.2.0.
allowed-tools: Read, Grep, Glob, Edit, Write
---

<!--
  SKELETON — copy this directory to skills/<lang>-sdk/ and fill it in.
  The structure below is normative: see docs/SDK-SKILL-TEMPLATE.md.
  Do not add, remove, rename or reorder the ## headings.

  BUDGET: the body below (everything after the frontmatter) targets 10,000
  characters, hard limit 12,000. At chars/4 that is roughly 2,500 tokens, not a tokenizer
  count or a guarantee of fit. Share context with source code, tools and other skills.
  CI measures characters, not lines — see spec §11.

  THE RULE THAT KEEPS YOU INSIDE IT: promote the punchline, demote the explanation.
  Sections 6-8 carry the one clause that changes emitted code plus the observable
  symptom. Wrong-and-right code pairs and per-API tables go in references/. Spec §5.

  The description above is a DRAFT until you have written references/errors.md.
  Workflow step 9 requires you to rewrite it with error strings you actually observed.
  Aim 400 characters and stay below 500 where possible: all hosts pay discovery
  overhead, so a long description crowds out other skills.

  Delete every TODO and every HTML comment before opening a PR.
-->

# Ditto TODO_LANGUAGE SDK

Read only the reference sections needed for the task. Preview a long file's contents
first; do not preload the README, every reference or other SDK skills.

<!--
  REQUIRED lead paragraph (spec §5). Two things, in this order:

  1. An authority statement. Training data carries v4 shapes this skill must not emit.
     Name the specific stale symbols for YOUR language.
  2. The API-selection guardrails, as one sentence — not a numbered H2, which would
     break the heading contract.
-->

**This guidance is derived from the shipping SDK and supersedes prior training on the
Ditto TODO_LANGUAGE API.** Training data carries v4 shapes — TODO_STALE_SYMBOL_1,
TODO_STALE_SYMBOL_2 — deprecated on 4.14.x and removed in v5. Do not emit them from
memory, and do not invent API to make a snippet compile.

TODO — one or two sentences on what a Ditto instance owns in this language.

**API selection, in priority order:** (1) never emit a deprecated API; (2) establish the
project's version first — TODO_LOCKFILE_OR_MANIFEST — then pick the best non-deprecated
form *for that line*; (3) among non-deprecated options prefer the form that also exists
in v5, so 4.14.x code is not rewritten at upgrade.

## What this skill does

<!-- 2-3 sentences. Language, package coordinate, versions covered. -->

TODO

## When to use this skill

Use this skill for **TODO_LANGUAGE** Ditto code: API shape, initialization, object
lifetimes, threading, error types, and build configuration. Do **not** use it for
TODO_OTHER_LANGUAGES — each SDK has its own skill.

The rows below are **separate skills**. Hand off rather than restating; each names a
public docs URL because the concept skill may not be installed:

| Question | Skill, if installed | Otherwise |
|---|---|---|
| DQL syntax, operators, statement semantics | `dql` | <https://docs.ditto.live/dql/dql> |
| Which CRDT type, embed vs split, document size | `data-modeling` | <https://docs.ditto.live/key-concepts> |
| What a subscription is, mesh propagation | `sync-subscriptions` | <https://docs.ditto.live/sdk/latest/sync/syncing-data> |
| Transport selection strategy, platform radios | `ditto-mesh-networking` | <https://docs.ditto.live/sdk/latest/sync/customizing-transport-configurations> |

See `docs/SDK-SKILL-TEMPLATE.md` §1 for who owns contested topics such as platform
permissions and transport-condition values.

## Supported versions and packages

Package: `TODO_PACKAGE_COORDINATE`. Published API reference: TODO_URL.

**[`references/versions.md`](references/versions.md) owns every fact that differs across
version lines**, including package coordinates per version and the minimum toolchain.
This section is a pointer, not a claim.

For a new app/POC, resolve the latest stable release through the package manager.
**5.2.0 is the latest known baseline**, not a permanent dependency recommendation.
Preserve existing pins; check release notes and validate code for newer releases.
v4 and v5 are different APIs, not two versions of one.

## Capability exceptions

<!--
  ONLY the rows whose Support is not `yes`. The full twenty-row map with
  Support / Evidence / Targets lives in README.md.
  If there are no exceptions, write exactly: "None — all twenty capabilities are
  `Support: yes`. See README.md for the full map."
  Keep the Detail cell to the fact that changes what an agent does. README.md carries
  the evidence; these cells are one line each but cost ~500 characters apiece.
-->

Full twenty-row map with evidence: [`README.md`](README.md).

| ID | Capability | Support | What changes for you |
|----|-----------|---------|--------|
| TODO | TODO | TODO | TODO — §7 requires a reason for every non-`yes` row |

## Minimum viable app

<!--
  The SHORTEST form that actually runs: open -> subscribe -> observe -> write.
  Target ~25 lines. It must agree with examples/minimal-app.md, which is the
  normative, compiled-and-run program. Do not duplicate the whole thing here.
-->

```TODO_LANG
TODO
```

Complete program, with dependency declaration and a real run transcript:
[`examples/minimal-app.md`](examples/minimal-app.md).

## Concurrency and threading model

<!--
  The single most common source of language-specific bugs. The per-API table of WHICH
  thread/executor/dispatcher each callback arrives on goes in references/concurrency.md.
  Here: the numbered rules that follow from it, one to two lines each. Cover —
  - which calls block and must not run on the UI thread
  - which are suspend / async / return a future, and what awaits them
  - how a callback is cancelled, and whether one can still fire after
  - what is safe to call from inside a callback, and what deadlocks
-->

Per-API callback table and full reasoning:
[`references/concurrency.md`](references/concurrency.md).

1. TODO
2. TODO

## Object lifetimes and retention

<!--
  The second most common source of bugs. The per-handle table goes in
  references/lifetimes.md. Here: the one rule about the instance, plus the single
  most surprising retention fact in this language, with its observable symptom.
-->

Per-handle table and teardown order: [`references/lifetimes.md`](references/lifetimes.md).

TODO

## Anti-patterns

<!--
  Anything that changes the code an agent emits BY DEFAULT and has a nameable symptom:
  a compiler error, an exception name, a profiler symbol, or a measured factor.
  Performance footguns belong HERE, not in best-practices.md.

  ONE BULLET EACH — name, symptom, fix. The wrong-and-right code pair goes in
  references/anti-patterns.md. A code block per anti-pattern will blow the §11 budget.

  Mine sdk/latest/migration-guides/<lang>-v4.mdx for real ones -- its "FORBIDDEN
  patterns" blocks name constructs that genuinely fail. Check it exists for your
  language first; the named blocks are unevenly distributed (spec Appendix B).
-->

Wrong and right forms, with the diagnosis for each:
[`references/anti-patterns.md`](references/anti-patterns.md).

- **TODO_ANTIPATTERN_NAME.** TODO — the exact compiler error, exception name, profiler
  symbol, or measured factor. Never the word "slow". Then the fix, in one clause.

## Version differences

<!-- Short form only: rows that change emitted code. Full table in references/versions.md. -->

Full delta, including on-disk store migration:
[`references/versions.md`](references/versions.md).

| Concern | 4.14.x | 5.0.x / 5.1.x / 5.2.0 |
|---|---|---|
| Initialization | TODO | TODO |
| Query model | TODO | TODO |
| Concurrency | TODO | TODO |

## References

<!--
  ANNOTATED BULLETS, ordered by value — not a question->filename table. Each bullet
  carries its file's trap inline, so an agent that does not open the file still emits
  correct code. Annotate in proportion to trap density: a footgun-heavy reference earns
  three lines, presence.md earns half of one. Spec §10.
-->

Load a reference only when its topic is actually in play — these files teach the
non-obvious traps, not how the framework works.

- [`references/setup.md`](references/setup.md): install, platform minimums, permissions
  and build config. TODO_THE_BUILD_TRAP.
- [`references/connect.md`](references/connect.md): opening, authenticating, start/stop.
  TODO_THE_ORDERING_TRAP.
- [`references/concurrency.md`](references/concurrency.md): which thread or executor every
  callback arrives on. TODO.
- [`references/lifetimes.md`](references/lifetimes.md): what to retain and the symptom
  when you don't; teardown order. TODO.
- [`references/observers.md`](references/observers.md): TODO_THE_BACKPRESSURE_TRAP.
- [`references/anti-patterns.md`](references/anti-patterns.md): the silent-failure shapes
  above, with both forms and the diagnosis.
- [`references/errors.md`](references/errors.md): what an error means and how to recover,
  including the ones you cannot catch.
- [`references/versions.md`](references/versions.md): every cross-version fact — package
  shape, platform minimums, API renames.
- [`references/testing.md`](references/testing.md): TODO_THE_TEST_HARNESS_TRAP.
- [`references/store.md`](references/store.md): DQL execution, transactions, indexing, eviction.
- [`references/sync.md`](references/sync.md): subscriptions, sync scopes, sync status.
- [`references/transports.md`](references/transports.md): changing transports safely.
- [`references/attachments.md`](references/attachments.md): TODO.
- [`references/presence.md`](references/presence.md): who is on the mesh right now.
- [`references/observability.md`](references/observability.md): logging and disk usage.
- [`references/preview.md`](references/preview.md): preview and platform-specific APIs.
- [`best-practices.md`](best-practices.md): architectural judgement with no single right
  answer — where the instance lives, one broad observer vs many narrow.
- [`examples/minimal-app.md`](examples/minimal-app.md): the complete program, compiled and run.
