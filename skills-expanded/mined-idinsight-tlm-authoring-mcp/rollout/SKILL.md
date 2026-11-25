---
name: rollout
description: Roll out a change to the Firestore KG store or the deployed MCP server and verify it — import/export a whole graph, edit a subject profile or guide through the live curator loop, deploy new server code, or repair a namespace. Use whenever importing/exporting a KG, changing a profile/guide, coordinating a data or code change with a server deploy, or fixing a store namespace. (Deploys run from GitHub Actions now, not a laptop `gcloud`; there is no `seed:kg-store` / seed-from-`sources/` step — Firestore is the only store.)
---

# Roll out a KG-store or server change safely

**Firestore is the only KG store.** There is no `bundle`/`KG_SOURCE` mode, no
`seed:kg-store`, and no seed-from-`sources/` step — all removed with the
firestore-only change (see
[`docs/design-notes/firestore-only-store.md`](../../../docs/design-notes/firestore-only-store.md)
and [`docs/technical-reference/store.md`](../../../docs/technical-reference/store.md)).
The graphs now live under `backend/test/fixtures/` (tests only) and in Firestore (live); the
per-subject `backend/assets/<ws>/<grade>/<subject>/` (terminology + prompt files) ship in the
container image. **The server is a self-contained package under `backend/` — run every
`npm run …` command in this skill from `backend/`** (`cd backend` first).

## Pick the path by what changed

| What you're changing | Path | Redeploy? |
|---|---|---|
| **Curriculum content, a subject profile, or a graph guide** | The **live curator loop** — edit with the graph tools / `edit_profile`, then `diff_draft` → `publish_draft`. Nothing reaches generation until you publish. | **No** |
| **A whole graph** (new namespace, restore from backup, clone) | `export:kg-store` (back up first) then `import:kg-store` | No (data only) |
| **A new subject** | Register its profile under `backend/src/adapters/profiles/` (**code**) → deploy → `import:kg-store` its graph | Yes (the profile is code) |
| **Server code** (parser, adapter engine, tools) | Deploy from GitHub Actions (see [`DEPLOY.md`](../../../DEPLOY.md)) | Yes |

The common case — tweaking a guide, fixing a lesson, editing a profile — is a **data
change through the curator loop, live, with no redeploy and no import.** Reach for
`import:kg-store` only to move a *whole graph*.

## The one coupling that still bites: code vs. store shape

The store holds the *full* Learning-Commons graph (spine + framework/derived nodes +
the real `supports`/`relatesTo` edges). The server must run code that reads that shape
(`toRawEnvelope` + `adapter.parse` hydration). An **older** server pointed at the store
silently drops content it can't read — no crash, just missing components/tasks in the
output. **Rule: when the code that reads the graph changes, deploy it before or with the
data it will read.** Pure data changes (curator loop, import) don't need a redeploy.

## Import / export (whole-graph moves)

These scripts run from `dist/` and hit real Firestore. Prerequisites in the shell:

- `SERVICE_ACCOUNT_KEY_PATH` — path to the Firebase service-account JSON
- `FIREBASE_STORAGE_BUCKET`

(No `KG_SOURCE`. On Cloud Run there is no key path — the runtime service account
supplies credentials.) Never print or commit the key.

```bash
npm run build                                                          # scripts read dist/
npm run export:kg-store -- <ws> <grade> <subject> [out.json]          # back up first
npm run import:kg-store -- <ws> <grade> <subject> <graph.json> [--profile p.json] [--replace-published] [--dry-run]
npm run write:profile -- <ws> <grade> <subject> [--profile p.json] [--slot a|b|published] [--dry-run]  # repair a config cell (see Recovery)
```

`import-kg` writes the graph **and** the subject-profile config cell — from `--profile
<path>` (`{ core, guide }` JSON) when given, otherwise the in-repo literal for that
grade/subject.

> **⚠️ a plain re-import writes slot `a` and does NOT repoint an existing namespace.**
> The published graph lives in one of two slots (`a`/`b`) behind a pointer
> `{ publishedSlot, draftSlot }`. On a **new** namespace, import writes `a` and stamps
> the pointer to it. On an **existing** one, a plain re-import writes `a` and leaves the
> pointer — so if the published slot is `b`, the import lands in a **side-copy nothing
> reads**. Two ways to land a re-import live instead:
>
> - **`--replace-published`** — writes the currently-published slot **in place**
>   (whichever it is), as a **delta** vs the live slot (not a full rewrite, which can
>   `DEADLINE_EXCEEDED` over a slow link on a large graph). Refused if a draft is open —
>   publish or discard it first. This is the whole-graph replace path (mirrors the
>   `--replace-published` note in [`store.md`](../../../docs/technical-reference/store.md)).
> - **the curator loop** — stage the fresh graph as the next draft and `publish_draft`,
>   which folds it into canonical. Prefer this for a *reviewed* change; use
>   `--replace-published` for a straight operator replacement.
>
> (The overlay model is about *drafts*; a namespace's **published** data still resolves to
> a slot, so the `a`/`b` framing above is unchanged.)

## Verify after any store change

Against the deployed server (via the MCP tools):

1. `set_context <ws> <grade> <subject>` **activates** (an invalid stored profile refuses
   activation — see recovery below).
2. `namespace_stats` / `walk_graph` return the expected node/edge counts.
3. `get_graph_guide` returns the intended guide text (for a profile/guide change).

## Deploy the server

Deploys run from **GitHub Actions**, not a laptop `gcloud` — the `deploy.yml`
workflow builds from the checked-out repo and authenticates with no JSON key
(Workload Identity Federation). Because a deploy rolls the single Cloud Run
instance and drops in-memory MCP sessions, it is **not** triggered on every push —
*you* choose when, two ways:

- **Run workflow** button (`workflow_dispatch`) — Actions tab → "Deploy to Cloud Run", from any branch;
- push a version tag: `git tag v1.4.0 && git push origin v1.4.0`.

Full runbook, one-time WIF setup, and the manual `gcloud run deploy --source backend`
fallback live in [`DEPLOY.md`](../../../DEPLOY.md). After deploy, smoke-check:

```bash
curl -s https://<service-url>/health     # → ok   (NOT /healthz — Google reserves that path)
```

## Recovery: a config cell too invalid to activate

If `set_context` fails with *"the stored subject profile … is invalid and would
mis-parse"*, the published config cell is malformed for the running code (e.g. it
carries a key the current schema retired). This is a **chicken-and-egg**: `edit_profile`
can't fix it because it needs the context activated. Use **`write:profile`** — it writes
the `{ core, guide }` config cell **directly** to a slot (default: the currently
published one), outside the two-phase loop the broken cell blocks, and it refuses to
write a cell that would not activate (same check the server runs):

```bash
npm run write:profile -- <ws> <grade> <subject> [--profile clean.json] [--slot a|b|published] [--dry-run]
```

Without `--profile` it uses the clean in-repo `{ core, guide }` literal for that
grade/subject. `--slot` defaults to `published`, so the fix is live immediately with no
pointer flip; pass `a`/`b` to target a specific slot. Run with `--dry-run` first (it
reads the real store, reports the target slot + guide length, writes nothing). Env is
the same as `import-kg` (`SERVICE_ACCOUNT_KEY_PATH` or `SERVICE_ACCOUNT_KEY_JSON`,
`FIREBASE_STORAGE_BUCKET`, and `TLM_BUCKET_PREFIX` to match the runtime namespace).

`write:profile` is the **repair** path (direct write, no draft, no audit). For an
ordinary profile/guide change, prefer the curator loop — `edit_profile` then
`publish_draft` — which is audited and reversible. Note `edit_profile` **replaces the
whole `{ core, guide }` record** (it does not patch): `get_profile` first, edit, pass it
all back. A tamper-evident way to confirm a big guide reached the store byte-for-byte:
the `edit_profile` dry-run's `confirmationToken` is base64url JSON carrying
`pv = sha256(stableStringify({core, guide}))`; decode it and compare against the same
hash computed locally before you confirm.
