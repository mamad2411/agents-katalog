---
name: js-sdk
description: >
  Use ONLY for Ditto JavaScript and TypeScript APIs (not Swift or Kotlin):
  .js/.ts/.tsx, @dittolive/ditto, Ditto.open, DittoConfig, store.execute and
  registerObserver. Explains the shared JavaScript API and routes Node.js, web/React,
  React Native and Expo work to their platform skills. Defaults new projects to the
  latest stable SDK unless a version is requested; existing projects keep theirs;
  covers 5.1.0/5.0.3 and 4.14.6 migration boundaries.
allowed-tools: Read, Grep, Glob, Edit, Write, Bash
---

# Ditto JavaScript / TypeScript

This guidance derives from the shipping SDK and supersedes stale v4 training:
`new Ditto(identity)` and collection query builders are not the v5 API. Establish the
installed version, avoid deprecated APIs, and prefer the non-deprecated v5-compatible form.

## What this skill does

Implements the shared Ditto API in JavaScript/TypeScript. Platform skills own build,
runtime and deployment differences; this skill owns the twenty SDK capabilities.

## When to use this skill

Read package.json and the lockfile first. Route to [js-node](../js-node/SKILL.md),
[js-web](../js-web/SKILL.md), [js-react-native](../js-react-native/SKILL.md), or
[js-expo](../js-expo/SKILL.md). For an unspecified new mobile React app, use the Expo
development-build recipe and say that assumption; preserve existing RN/Expo projects.
Native config comes from [native-app-config](../native-app-config/SKILL.md).

Concept ownership: `write-dql` or <https://docs.ditto.live/dql/dql> for grammar;
`data-modeling` or <https://docs.ditto.live/key-concepts/document-model> for CRDT design;
`sync-subscriptions` or <https://docs.ditto.live/sdk/latest/sync/syncing-data> for propagation;
`ditto-mesh-networking` or <https://docs.ditto.live/key-concepts/mesh-networking> for transport strategy.

## Supported versions and packages

Package: `@dittolive/ditto`. [Versions](references/versions.md) owns version-specific
claims. Pick the version before writing package.json:

- **New project, no version requested:** the latest stable release, from
  `npm view @dittolive/ditto dist-tags.latest` (5.2.0 when authored). Don't take a version
  from memory or older docs, and skip `-dev-weekly`, `-preview`, `-rc` and `-experimental` builds.
- **Version requested by the user** (including 4.x): use it.
- **Existing project:** keep the lockfile's version; upgrade or migrate only on request.

## Capability exceptions

Full twenty-row evidence map: [README](README.md).

| ID | Capability | Support | What changes |
|---|---|---|---|
| CAP-14 | Sync status and local commit tracking | partial | Local commitID and sync.isActive do not provide per-query remote acknowledgements. |
| CAP-20 | Preview and platform-specific APIs | partial | Platform APIs vary; no Data Streams export in the checked JS 5.2.0 distribution. |

## Minimum viable app

The [complete JavaScript program](assets/minimal-app.mjs) opens, licenses, starts sync,
subscribes, observes, writes, waits for delivery, and closes in finally.
[Run instructions](examples/minimal-app.md). For React use [runtime](assets/runtime.ts),
[provider/hook](assets/DittoProvider.tsx), and [task operations](assets/tasks.ts), all tested
as shipped. Do not replace them with an untested library recommendation.

## Concurrency and threading model

Await initialization, store writes and authentication. Observer callbacks execute on
the JS runtime; keep them short. An async callback is not automatic back-pressure.
SignalNext observers must always signal after processing. Never nest a write transaction
or call store.execute inside one; use tx.execute. [Details](references/concurrency.md).

## Object lifetimes and retention

One runtime per application/account, created outside render. Providers borrow it;
queries own their observers/subscriptions and cancel both. App shutdown first unmounts
consumers and awaits outstanding writes, then closes the owner. [Lifetimes](references/lifetimes.md).

## Anti-patterns

- Constructor/collection v4 APIs on v5: unavailable API; use Ditto.open and DQL.
- Instance in render: persistence directory locked; use the app runtime.
- Observer mistaken for subscription: local data works but remote data never arrives.
- Login resolves: inspect result.error or authentication failures go unnoticed.
- Missing signalNext: observer stops delivering subsequent updates.
- Browser persistence claim: closing/reloading the page discards the in-memory store.
- Expo Go or OTA-only native SDK upgrade: native module missing/version mismatch; rebuild.

Wrong/right diagnosis: [anti-patterns](references/anti-patterns.md).

## Version differences

[Version table](references/versions.md) records the v4/v5 split, 5.1 DQL additions,
5.2 config options, and persistence migration boundaries. Do not infer a JS API from
Swift/Kotlin availability or unreleased source.

## References

Load only the topic needed; do not preload the capability map or every reference.
- [setup](references/setup.md): pick the correct runtime binding before copying code.
- [connect](references/connect.md): await the auth handler before starting server sync.
- [concurrency](references/concurrency.md): do not hold transactions across network requests.
- [lifetimes](references/lifetimes.md): provider unmount does not close the application owner.
- [store](references/store.md): bind values; generic types do not validate synchronized documents.
- [sync](references/sync.md): local commit is not remote acknowledgement.
- [observers](references/observers.md): cancel both handles and prevent stale query results.
- [attachments](references/attachments.md): file URIs need native resolution; browser uses bytes.
- [presence](references/presence.md): peer visibility is not document delivery.
- [observability](references/observability.md): custom JS log callbacks are unavailable on RN.
- [errors](references/errors.md): native aborts cannot be caught by a JS catch.
- [anti-patterns](references/anti-patterns.md): diagnose stale APIs and lifecycle errors.
- [versions](references/versions.md): preserve existing versions and persistent paths.
- [preview](references/preview.md): avoid APIs absent from the published JS exports.
- [testing](references/testing.md): distinguish runtime, compile and physical-device evidence.
- [Architecture](best-practices.md): app ownership and data scope decisions.

- [Transports](references/transports.md): use runtime-supported fields and apply the config.
