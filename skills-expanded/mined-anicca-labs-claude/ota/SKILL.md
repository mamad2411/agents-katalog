---
name: ota
description: Self-hosted OTA updates via Supabase — setup, Edge Function manifest server, CI upload script, and Doppler config. Use when implementing over-the-air JS updates without EAS Update or Expo's build servers.
---

## Architecture

OTA updates are self-hosted on Supabase — no EAS Update subscription needed.

- **Supabase Storage** (`expo-updates` bucket) — hosts JS bundles and assets
- **Edge Function** (`expo-update-manifest`) — implements Expo Updates Protocol v1, returns multipart manifests
- **`api.expo_updates` table** — tracks which update is active per channel/platform/runtime version
- **`scripts/push-ota-update.mjs`** — CI script: runs `expo export`, uploads to Storage, registers in DB
- **`scripts/prune-ota-updates.mjs`** — retention: deletes superseded updates so Storage stays bounded (called automatically at the end of every push)
- **GitHub Actions workflow** — triggers on push to `stg`/`main`, auto-pushes the OTA update

> **Storage grows unbounded without retention.** Each push uploads a fresh bundle **plus a full
> copy of every asset** into a new `{channel}/{updateId}/` folder, but the manifest server only
> ever serves the *latest* update per platform — everything older is dead weight. Without pruning,
> a frequently-pushed channel (especially `stg`) balloons to multiple GB and blows past Supabase's
> free 1 GB Storage cap. The prune step below is not optional; wire it in from day one.

The store build is still required when native code changes. OTA handles JS-only changes.

## Setup checklist

1. `yarn expo install expo-updates`
2. Add `runtimeVersion`, `updates`, and `"expo-updates"` plugin to `app.config.ts`
3. Apply the Supabase migration (table + storage bucket)
4. Deploy the Edge Function to stg (the human deploys prd)
5. Set Doppler vars (`EXPO_UPDATE_URL`, `EXPO_UPDATE_CHANNEL`) in stg, and list the prd values for the human to set
6. Add `scripts/push-ota-update.mjs`, `scripts/prune-ota-updates.mjs`, and `.github/workflows/expo-ota-update.yml`
7. Apply the iOS native patch (see **iOS native patch** section below)
8. Add path filters to the store build workflow so it only runs on native-touching files
9. Do one native rebuild so `expo-updates` is embedded in the binary

The two CI workflows are mutually exclusive by path — JS changes ship via OTA, native
changes ship via a store rebuild (an OTA can never deliver native code):

- **OTA push** (`expo-ota-update.yml`) → `src/**`, `app/**`, `assets/**`, `index.js`, `lingui.config.ts`
- **Store build** (`expo-store-deploy.yml`) → `package.json`, `yarn.lock`, `app.config.ts`, `eas.json`, `google-services-*.json`, `GoogleService-Info-*.plist`

> **A file in NEITHER path list will not auto-deploy.** `firebase.json`, for example, is in
> no filter — yet it affects the native fingerprint (see below), so a `firebase.json` change
> must be shipped via a **manual `workflow_dispatch` of the store build**, not an OTA. When you
> add a new native-config file, decide which list it belongs in (almost always the store build).

## app.config.ts

Do NOT set `kotlinVersion` in `expo-build-properties` android config. `expo-build-properties`
writes it as `android.kotlinVersion` (prefixed), which `expo-updates`' buildscript reads as
`rootProject["kotlinVersion"]` (no prefix) — they don't align, causing a KSP version mismatch
and `NoSuchMethodError` at compile time. `ExpoRootProjectPlugin` already defaults to `2.0.21`.

```ts
export default ({ config }: ConfigContext): ExpoConfig => ({
  ...config,
  version: config.version,           // reads from package.json — single source of truth
  // Fingerprint policy: runtimeVersion is a per-platform HASH of the native layer (native
  // deps, app.config.ts, config plugins, entitlements, build properties, patches, firebase.json,
  // and config-affecting env vars baked at build). Changing native code automatically changes it,
  // so an OTA can never be served to a binary that lacks the native module it needs — no manual
  // version bumping. JS-only changes leave the fingerprint untouched, so their OTAs apply.
  runtimeVersion: {
    policy: 'fingerprint',
  },
  updates: {
    url: process.env.EXPO_UPDATE_URL,
    checkAutomatically: 'ON_LOAD',
    requestHeaders: {
      'expo-channel-name': process.env.EXPO_UPDATE_CHANNEL ?? 'prd',
    },
  },
  plugins: [
    // ... other plugins
    // No kotlinVersion in expo-build-properties android config — see note above
    'expo-updates',
  ],
});
```

`EXPO_UPDATE_URL` and `EXPO_UPDATE_CHANNEL` are set per environment in Doppler.

## Supabase migration

```sql
-- Storage bucket (public — devices download directly without auth)
insert into storage.buckets (id, name, public)
values ('expo-updates', 'expo-updates', true)
on conflict (id) do nothing;

create policy "Public read access"
  on storage.objects for select
  using (bucket_id = 'expo-updates');

create table api.expo_updates (
  id uuid primary key,
  channel text not null,
  platform text not null check (platform in ('ios', 'android')),
  runtime_version text not null,
  created_at timestamptz not null default now(),
  launch_asset jsonb not null,
  assets jsonb not null default '[]',
  extra jsonb not null default '{}',
  active boolean not null default true
);

alter table api.expo_updates enable row level security;
-- delete is required by the retention prune (scripts/prune-ota-updates.mjs); without it
-- pruning fails with "permission denied for table expo_updates" and Storage grows unbounded
grant select, insert, update, delete on api.expo_updates to service_role;

create index expo_updates_lookup_idx
  on api.expo_updates (channel, platform, runtime_version, created_at desc)
  where active = true;
```

Apply via the Supabase Management API or dashboard on stg. The prd project needs the same migration: hand it to the human to apply.

## Edge Function (`supabase/functions/expo-update-manifest/index.ts`)

**Critical details for iOS:**

- `createdAt` must use `+00:00` format, not `Z` — iOS `NSDateFormatter` with `ZZZZZ` pattern doesn't parse `Z`
- Multipart body must end with `\r\n` after the closing boundary
- Cache headers must prevent CDN caching (`no-store`) so every request hits the function

```ts
// @openapi-internal — device-facing OTA manifest server, not a client API endpoint
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'

const SUPABASE_URL = Deno.env.get('SUPABASE_URL')!
const SUPABASE_SERVICE_ROLE_KEY = Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!

type Asset = { hash: string; key: string; fileExtension?: string; contentType: string; url: string }
type ExpoUpdate = {
  id: string; channel: string; platform: string; runtime_version: string
  created_at: string; launch_asset: Asset; assets: Asset[]
  extra: Record<string, unknown>; active: boolean
}

function buildMultipart(boundary: string, parts: Array<{ name: string; contentType: string; body: string }>): string {
  const chunks = parts.flatMap((p) => [
    `--${boundary}`, `Content-Type: ${p.contentType}`,
    `Content-Disposition: form-data; name="${p.name}"`, '', p.body,
  ])
  chunks.push(`--${boundary}--`)
  // iOS expo-updates requires CRLF after the closing boundary
  return chunks.join('\r\n') + '\r\n'
}

function noUpdateResponse(): Response {
  const boundary = 'expo-update-boundary'
  return new Response(
    buildMultipart(boundary, [{ name: 'directive', contentType: 'application/json', body: JSON.stringify({ type: 'noUpdateAvailable' }) }]),
    { headers: { 'expo-protocol-version': '1', 'expo-sfv-version': '0', 'cache-control': 'no-store, no-cache, must-revalidate', 'content-type': `multipart/mixed; boundary="${boundary}"` } },
  )
}

Deno.serve(async (req) => {
  if (req.method === 'OPTIONS') return new Response(null, { status: 204 })
  if (req.method !== 'GET') return new Response('Method not allowed', { status: 405 })

  const platform = req.headers.get('expo-platform')
  const runtimeVersion = req.headers.get('expo-runtime-version')
  const channel = req.headers.get('expo-channel-name') ?? 'prd'
  const currentUpdateId = req.headers.get('expo-current-update-id')

  if (!platform || !runtimeVersion) return new Response('Missing expo-platform or expo-runtime-version header', { status: 400 })
  if (platform !== 'ios' && platform !== 'android') return new Response('Invalid expo-platform', { status: 400 })

  const supabase = createClient(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY, { db: { schema: 'api' } })
  const { data: update } = await supabase
    .from('expo_updates').select('*')
    .eq('channel', channel).eq('platform', platform).eq('runtime_version', runtimeVersion).eq('active', true)
    .order('created_at', { ascending: false }).limit(1).maybeSingle() as { data: ExpoUpdate | null }

  if (!update || update.id === currentUpdateId) return noUpdateResponse()

  const manifest = {
    id: update.id,
    // +00:00 format required — iOS NSDateFormatter ZZZZZ pattern doesn't parse literal 'Z'
    createdAt: new Date(update.created_at).toISOString().replace('Z', '+00:00'),
    runtimeVersion,
    assets: update.assets,
    launchAsset: update.launch_asset,
    metadata: {},
    extra: update.extra,
  }
  const boundary = 'expo-update-boundary'
  return new Response(
    buildMultipart(boundary, [{ name: 'manifest', contentType: 'application/json', body: JSON.stringify(manifest) }]),
    { headers: {
      'expo-protocol-version': '1', 'expo-sfv-version': '0',
      'cache-control': 'no-store, no-cache, must-revalidate',
      'pragma': 'no-cache', 'expires': '0',
      'vary': 'expo-current-update-id, expo-channel-name, expo-platform',
      'content-type': `multipart/mixed; boundary="${boundary}"`,
    }},
  )
})
```

Deploy with `--no-verify-jwt` — devices call it without auth:

```bash
supabase functions deploy expo-update-manifest --no-verify-jwt --project-ref <ref>
```

**Every edge-function change must reach both stg and prd**, but only stg is yours to deploy. Deploy stg, verify, then tell the human prd is pending:

```bash
yarn functions:deploy:stg   # you
yarn functions:deploy:prd   # the human
```

Never deploy to just one — production users will get a different manifest behaviour than staging users and bugs will be hard to reproduce.

## VSCode / Deno editor setup (do once per repo)

Edge Functions run on Deno, but VSCode's built-in TypeScript server type-checks them as
Node/browser code — so it flags the `Deno` global as undefined and can't resolve remote
imports. Fix it by enabling the Deno LSP **scoped to `supabase/functions`** so it doesn't
fight the Expo/RN app's TS. This applies to every Edge Function (OTA, push, Stripe webhooks),
not just OTA.

Requires the `denoland.vscode-deno` extension. After any of these changes, reload the window
(Cmd+Shift+P → "Reload Window").

**`.vscode/settings.json`** — enable Deno only under the functions folder:

```json
{
  "deno.enable": true,
  "deno.enablePaths": ["./supabase/functions"]
}
```

**`.vscode/extensions.json`** — recommend the extension:

```json
{ "recommendations": ["denoland.vscode-deno"] }
```

**`supabase/functions/deno.json`** — marks the folder as a Deno project and holds the import
map. Deno-lint's `no-import-prefix` rejects inline `https:` / `npm:` / `jsr:` specifiers, so
declare deps here and import them by **bare specifier**:

```json
{
  "compilerOptions": { "lib": ["deno.window", "dom"] },
  "imports": {
    "jose": "https://esm.sh/jose@5",
    "@supabase/supabase-js": "https://esm.sh/@supabase/supabase-js@2"
  }
}
```

```ts
import * as jose from 'jose'                          // ✅ bare specifier
import { createClient } from '@supabase/supabase-js'  // ✅
// import * as jose from 'https://esm.sh/jose@5'      // ❌ no-import-prefix
```

**`eslint.config.js`** — exclude the functions from the app's ESLint (it can't resolve Deno
imports and would report `import/no-unresolved`):

```js
{ ignores: [/* ...existing... */, "supabase/functions/**"] }
```

**Cache remote deps** — new imports show an "uncached" error until downloaded. Run from
`supabase/functions/`, or use the editor's "Cache Dependencies" quick-fix (Cmd+.):

```bash
deno cache _shared/firebase.ts   # or: deno cache <file>
deno check _shared/firebase.ts   # verify it type-checks clean
```

Commit `supabase/functions/deno.json` **and** the generated `deno.lock` — the lock pins exact
resolved versions for reproducible deploys.

## Upload script (`scripts/push-ota-update.mjs`)

**Two critical requirements discovered through iOS debugging:**

1. **Bundle key must be unique per OTA** — use `platformMeta.bundle` (the filename, which includes its hash) as the key. If you use a static key like `'bundle'`, expo-updates caches the first bundle forever by that key and never re-downloads subsequent bundles, even when the OTA changes. The app reports the new OTA ID but silently executes the old code.

2. **`extra.expoClient` must contain the app config** — expo-linking reads the URI scheme from `Constants.expoConfig`, which comes from `extra.expoClient` in the OTA manifest. Without it, the app crashes on launch with `expo-linking needs access to the expo-constants manifest`.

```js
#!/usr/bin/env node
import fs from 'fs'
import { createRequire } from 'module'
import { execFileSync } from 'child_process'
import path from 'path'
import crypto from 'crypto'
import { pruneOtaUpdates } from './prune-ota-updates.mjs'

const require = createRequire(import.meta.url)
const { getConfig } = require('@expo/config')

const SUPABASE_URL = requireEnv('SUPABASE_URL')
const SERVICE_ROLE_KEY = requireEnv('SUPABASE_SERVICE_ROLE_KEY')
const CHANNEL = requireEnv('EXPO_UPDATE_CHANNEL')
// No EXPO_RUNTIME_VERSION — the runtimeVersion is the per-platform fingerprint, computed below.
const DIST_DIR = process.env.DIST_DIR ?? './dist'
const BUCKET = 'expo-updates'

function requireEnv(name) {
  const val = process.env[name]
  if (!val) throw new Error(`Missing required env var: ${name}`)
  return val
}

// runtimeVersion is the per-platform fingerprint (app.config.ts uses `policy: 'fingerprint'`).
// This MUST be the same `expo-updates` computation the EAS build embeds, run under the SAME
// Doppler env as the build — config-affecting env vars (e.g. EXPO_UPDATE_URL) change the hash.
function fingerprintFor(platform) {
  const bin = path.join('node_modules', '.bin', 'expo-updates')
  const out = execFileSync(bin, ['fingerprint:generate', '--platform', platform], {
    encoding: 'utf8', stdio: ['ignore', 'pipe', 'ignore'], maxBuffer: 64 * 1024 * 1024,
  })
  const hash = JSON.parse(out).hash
  if (!hash) throw new Error(`Could not compute ${platform} fingerprint`)
  return hash
}

function sha256b64(filePath) {
  const content = fs.readFileSync(filePath)
  // expo-updates iOS compares as base64url — no 'sha256:' prefix
  return crypto.createHash('sha256').update(content).digest('base64url')
}

function extToContentType(ext) {
  const map = { js: 'application/javascript', png: 'image/png', jpg: 'image/jpeg', jpeg: 'image/jpeg', gif: 'image/gif', webp: 'image/webp', svg: 'image/svg+xml', ttf: 'font/ttf', otf: 'font/otf', woff: 'font/woff', woff2: 'font/woff2', json: 'application/json', mp3: 'audio/mpeg', mp4: 'video/mp4', riv: 'application/octet-stream' }
  return map[ext?.toLowerCase()] ?? 'application/octet-stream'
}

const sleep = (ms) => new Promise((r) => setTimeout(r, ms))

// MUST retry like the prune step does: Supabase Storage intermittently returns 504/429
// under load, and a single failed asset upload here aborts the WHOLE push — leaving one
// platform half-published (a mismatched OTA). Retry 5xx/429 + network errors with
// backoff; fail fast on 4xx.
async function uploadFile(localPath, storagePath, contentType, tries = 5) {
  const body = fs.readFileSync(localPath)
  let lastErr
  for (let attempt = 1; attempt <= tries; attempt++) {
    let res
    try {
      res = await fetch(`${SUPABASE_URL}/storage/v1/object/${BUCKET}/${storagePath}`, {
        method: 'POST',
        headers: { Authorization: `Bearer ${SERVICE_ROLE_KEY}`, apikey: SERVICE_ROLE_KEY, 'Content-Type': contentType, 'x-upsert': 'true' },
        body,
      })
    } catch (err) {
      lastErr = err // network error — retry
      if (attempt < tries) { await sleep(500 * 2 ** (attempt - 1)); continue }
      throw lastErr
    }
    if (res.ok) { console.log(`  uploaded ${storagePath}`); return }
    const text = await res.text()
    if (res.status < 500 && res.status !== 429) throw new Error(`Storage upload failed [${storagePath}]: ${res.status} ${text}`)
    lastErr = new Error(`Storage upload failed [${storagePath}]: ${res.status} ${text}`)
    if (attempt < tries) await sleep(500 * 2 ** (attempt - 1))
  }
  throw lastErr
}

async function insertUpdate(row) {
  const res = await fetch(`${SUPABASE_URL}/rest/v1/expo_updates`, {
    method: 'POST',
    headers: { Authorization: `Bearer ${SERVICE_ROLE_KEY}`, apikey: SERVICE_ROLE_KEY, 'Content-Type': 'application/json', 'Content-Profile': 'api', Prefer: 'return=minimal' },
    body: JSON.stringify(row),
  })
  if (!res.ok) throw new Error(`DB insert failed: ${res.status} ${await res.text()}`)
}

async function pushPlatform(platform, metadata, updateId, expoConfig, runtimeVersion) {
  const platformMeta = metadata.fileMetadata?.[platform]
  if (!platformMeta?.bundle) { console.log(`  no ${platform} bundle in export, skipping`); return }

  console.log(`\nPublishing ${platform} update ${updateId} (runtimeVersion ${runtimeVersion})...`)
  const prefix = `${CHANNEL}/${updateId}`
  const storageBase = `${SUPABASE_URL}/storage/v1/object/public/${BUCKET}`

  const bundleLocalPath = path.join(DIST_DIR, platformMeta.bundle)
  await uploadFile(bundleLocalPath, `${prefix}/${platformMeta.bundle}`, 'application/javascript')

  const assets = []
  for (const asset of platformMeta.assets ?? []) {
    const localPath = path.join(DIST_DIR, asset.path)
    if (!fs.existsSync(localPath)) { console.warn(`  warn: asset not found: ${localPath}`); continue }
    const contentType = extToContentType(asset.ext)
    await uploadFile(localPath, `${prefix}/${asset.path}`, contentType)
    // fileExtension is required by expo-updates — omitting it causes JSONException on iOS
    assets.push({ hash: sha256b64(localPath), key: asset.path, fileExtension: `.${asset.ext}`, contentType, url: `${storageBase}/${prefix}/${asset.path}` })
  }

  await insertUpdate({
    id: updateId, channel: CHANNEL, platform, runtime_version: runtimeVersion,
    launch_asset: {
      hash: sha256b64(bundleLocalPath),
      // CRITICAL: use the bundle filename as key — it includes the content hash, making it
      // unique per OTA. A static key like 'bundle' causes expo-updates to reuse the first
      // bundle ever downloaded, silently running old code for every subsequent update.
      key: platformMeta.bundle,
      fileExtension: path.extname(platformMeta.bundle) || '.bundle',
      contentType: 'application/javascript',
      url: `${storageBase}/${prefix}/${platformMeta.bundle}`,
    },
    assets,
    // expoClient required — expo-linking reads the URI scheme from Constants.expoConfig,
    // which comes from extra.expoClient. Without it the app crashes on OTA launch.
    extra: { expoClient: expoConfig },
    active: true,
  })
  console.log(`  ✓ registered in DB`)
}

async function main() {
  const metadataPath = path.join(DIST_DIR, 'metadata.json')
  if (!fs.existsSync(metadataPath)) throw new Error(`${metadataPath} not found — run 'yarn expo export --output-dir dist' first`)
  const metadata = JSON.parse(fs.readFileSync(metadataPath, 'utf8'))
  const { exp: expoConfig } = getConfig(process.cwd(), { skipSDKVersionRequirement: true })
  // iOS and Android fingerprints differ — each OTA is tagged with the runtimeVersion its
  // target binary was built with, so a platform's update only reaches matching binaries.
  const iosRuntime = fingerprintFor('ios')
  const androidRuntime = fingerprintFor('android')
  await pushPlatform('ios', metadata, crypto.randomUUID(), expoConfig, iosRuntime)
  await pushPlatform('android', metadata, crypto.randomUUID(), expoConfig, androidRuntime)
  // Bound Storage growth: drop superseded updates right after publishing the new one.
  await pruneOtaUpdates()
  console.log('\nDone.')
}

main().catch((err) => { console.error(err.message); process.exit(1) })
```

Always run the export through Doppler so env vars are correct:

```bash
doppler run --project mobile --config stg -- yarn expo export --clear --platform ios --platform android --output-dir dist
```

The `--clear` flag prevents Metro from serving a cached bundle with stale module IDs.

> **Compute the fingerprint under the SAME Doppler env as the build.** `expo-updates
> fingerprint:generate` reads the resolved native config, so config-affecting env vars baked at
> build time (e.g. `EXPO_UPDATE_URL`) change the hash. The push script therefore runs inside the
> same `doppler --config <env>` used for the build. **Prefer the CI OTA workflow over a local
> `yarn push-ota`**: the CI clean-env fingerprint is what reliably matches the store builds. A
> local push can match, but only if your working tree exactly equals the built commit and env —
> otherwise the OTA is tagged with a fingerprint no installed binary carries and silently never
> applies.

## Storage retention (`scripts/prune-ota-updates.mjs`)

`push-ota-update.mjs` imports `pruneOtaUpdates` and calls it after each publish, so the
`expo-updates` bucket self-prunes and can't grow unbounded. It keeps the newest `OTA_RETAIN`
updates per platform (default **2**, for rollback headroom) and deletes the rest — both the
Storage objects and the `api.expo_updates` rows.

**Key implementation details (each one is load-bearing):**

- **The `storage` schema is not exposed via PostgREST**, so objects are enumerated with the
  native Storage list API — which is non-recursive (folders come back with `id === null`),
  hence the recursive walk.
- **Delete via the Storage API, not `DELETE FROM storage.objects`** — a raw row delete orphans
  the underlying bytes in the storage backend; the Storage `remove` endpoint deletes both.
- **Retries** — the Storage API intermittently returns 504/429 under load; without backoff a
  long prune aborts partway.
- **Delete the DB row only after its objects are gone**, one update at a time, so an interrupted
  run is safely re-runnable (surviving rows still point at whatever objects remain).
- Run standalone to backfill an existing project that grew before retention existed:
  `doppler run --project mobile --config stg -- node scripts/prune-ota-updates.mjs`
  (set `OTA_RETAIN=1` to reclaim the most; orphaned folders from older partial runs — i.e.
  Storage folders with no matching `expo_updates` row — must be cleaned separately, as this
  script only walks live DB rows).

```js
#!/usr/bin/env node
// Deletes superseded OTA updates so the expo-updates bucket doesn't grow unbounded.
// The manifest server only serves the latest active update per (channel, platform,
// runtime_version); everything older is dead weight. Keeps the newest OTA_RETAIN per
// platform. Imported by push-ota-update.mjs and runnable standalone via Doppler.
const BUCKET = 'expo-updates'

function requireEnv(name) {
  const val = process.env[name]
  if (!val) throw new Error(`Missing required env var: ${name}`)
  return val
}

const SUPABASE_URL = requireEnv('SUPABASE_URL')
const SERVICE_ROLE_KEY = requireEnv('SUPABASE_SERVICE_ROLE_KEY')
const CHANNEL = requireEnv('EXPO_UPDATE_CHANNEL')
const RETAIN = Math.max(1, parseInt(process.env.OTA_RETAIN ?? '2', 10))

const authHeaders = (extra = {}) => ({ Authorization: `Bearer ${SERVICE_ROLE_KEY}`, apikey: SERVICE_ROLE_KEY, ...extra })
const sleep = (ms) => new Promise((r) => setTimeout(r, ms))

// The Storage API occasionally returns 504/429 under load; retry transient failures.
async function fetchRetry(url, opts, tries = 5) {
  let lastErr
  for (let attempt = 1; attempt <= tries; attempt++) {
    try {
      const res = await fetch(url, opts)
      if (res.status < 500 && res.status !== 429) return res
      lastErr = new Error(`${res.status} ${await res.text()}`)
    } catch (err) { lastErr = err }
    if (attempt < tries) await sleep(500 * 2 ** (attempt - 1))
  }
  throw lastErr
}

// Update IDs to delete: every update for this channel except the newest RETAIN per platform.
async function staleUpdateIds() {
  const res = await fetchRetry(
    `${SUPABASE_URL}/rest/v1/expo_updates?channel=eq.${CHANNEL}&select=id,platform,created_at&order=created_at.desc`,
    { headers: authHeaders({ 'Accept-Profile': 'api' }) },
  )
  if (!res.ok) throw new Error(`Failed to list updates: ${res.status} ${await res.text()}`)
  const kept = {}
  const stale = []
  for (const row of await res.json()) {
    const seen = (kept[row.platform] ??= 0)
    if (seen < RETAIN) kept[row.platform] = seen + 1
    else stale.push(row.id)
  }
  return stale
}

// Storage list API is non-recursive (folders => id === null), so descend into each.
async function listObjectsRecursive(prefix) {
  const out = []
  const limit = 1000
  let offset = 0
  for (;;) {
    const res = await fetchRetry(`${SUPABASE_URL}/storage/v1/object/list/${BUCKET}`, {
      method: 'POST', headers: authHeaders({ 'Content-Type': 'application/json' }),
      body: JSON.stringify({ prefix, limit, offset }),
    })
    if (!res.ok) throw new Error(`Failed to list objects: ${res.status} ${await res.text()}`)
    const items = await res.json()
    for (const item of items) {
      const full = prefix ? `${prefix}/${item.name}` : item.name
      if (item.id === null) out.push(...(await listObjectsRecursive(full)))
      else out.push(full)
    }
    if (items.length < limit) break
    offset += limit
  }
  return out
}

async function deleteObjects(paths) {
  // Storage bulk-delete removes the row AND the backing bytes; a raw DELETE on
  // storage.objects would orphan the file in the storage backend.
  for (let i = 0; i < paths.length; i += 1000) {
    const res = await fetchRetry(`${SUPABASE_URL}/storage/v1/object/${BUCKET}`, {
      method: 'DELETE', headers: authHeaders({ 'Content-Type': 'application/json' }),
      body: JSON.stringify({ prefixes: paths.slice(i, i + 1000) }),
    })
    if (!res.ok) throw new Error(`Storage delete failed: ${res.status} ${await res.text()}`)
  }
}

async function deleteUpdateRow(updateId) {
  const res = await fetchRetry(`${SUPABASE_URL}/rest/v1/expo_updates?id=eq.${updateId}`, {
    method: 'DELETE', headers: authHeaders({ 'Content-Profile': 'api', Prefer: 'return=minimal' }),
  })
  if (!res.ok) throw new Error(`DB delete failed: ${res.status} ${await res.text()}`)
}

export async function pruneOtaUpdates() {
  const stale = await staleUpdateIds()
  if (stale.length === 0) { console.log(`OTA prune (${CHANNEL}): nothing to remove (retain=${RETAIN}).`); return }
  console.log(`OTA prune (${CHANNEL}): removing ${stale.length} update(s), keeping newest ${RETAIN}/platform...`)
  let objCount = 0
  for (const id of stale) {
    const paths = await listObjectsRecursive(`${CHANNEL}/${id}`)
    if (paths.length) { await deleteObjects(paths); objCount += paths.length }
    // Delete the row only after its objects are gone, so an interrupted run is re-runnable.
    await deleteUpdateRow(id)
  }
  console.log(`OTA prune (${CHANNEL}): deleted ${objCount} storage object(s) and ${stale.length} DB row(s).`)
}

// Run directly (not when imported by push-ota-update.mjs).
if (import.meta.url === `file://${process.argv[1]}`) {
  pruneOtaUpdates().catch((err) => { console.error(err.message); process.exit(1) })
}
```

## iOS native patch (required)

expo-updates iOS has two bugs when used with Supabase Storage that require patching `FileDownloader.swift` via `yarn patch`. Apply once and commit — Yarn re-applies on every `yarn install` including EAS local builds.

**To create/update the patch:**

```bash
yarn patch expo-updates
# edit /tmp/.../user/ios/EXUpdates/AppLoader/FileDownloader.swift
yarn patch-commit -s /tmp/...
yarn install   # updates yarn.lock hash
```

**Patch 1 — missing assets directory** (`downloadAsset` function, before `data.write`):

Supabase storage assets are written to `.expo-internal/assets/` but expo-updates doesn't create that directory. Without the fix every asset write fails with `NSCocoaErrorDomain Code=4 "The folder doesn't exist"`.

```swift
do {
  // ADD THESE TWO LINES before data.write:
  let destDir = (destinationPath as NSString).deletingLastPathComponent
  try FileManager.default.createDirectory(atPath: destDir, withIntermediateDirectories: true, attributes: nil)
  try data.write(to: URL(fileURLWithPath: destinationPath), options: .atomic)
```

**Patch 2 — 304 retry for cached ETags** (`downloadData(withRequest:)` function):

NSURLSession caches ETags from Supabase CDN. On subsequent requests it sends `If-None-Match`, the CDN returns 304 with nil data, and expo-updates fails with `ERR_UPDATES_FETCH: failed to load all assets`. The fix retries 304 responses with conditional headers stripped.

```swift
// Also add to createManifestRequest and createGenericRequest:
//   cachePolicy: .reloadIgnoringLocalCacheData

if httpResponse.statusCode == 304 {
  var freshRequest = request
  freshRequest.setValue(nil, forHTTPHeaderField: "If-None-Match")
  freshRequest.setValue(nil, forHTTPHeaderField: "If-Modified-Since")
  freshRequest.cachePolicy = .reloadIgnoringLocalAndRemoteCacheData
  let retryTask = self.session.dataTask(with: freshRequest) { retryData, retryResponse, retryError in
    guard let retryResponse = retryResponse else {
      let cause = UpdatesError.fileDownloaderUnknownError(cause: retryError ?? NSError(domain: "EXUpdates", code: 0))
      errorBlock(cause)
      return
    }
    successBlock(retryData, retryResponse)
  }
  retryTask.resume()
  return
}
```

**Do NOT set `urlCache = nil`** on the URLSession configuration — this causes NSURLSession to deliver nil data for all 200 responses.

## CI workflow (`.github/workflows/expo-ota-update.yml`)

```yaml
name: Push OTA Update

on:
  push:
    branches: [stg, main]
    # JS/asset paths only — native-touching files (package.json, yarn.lock, app.config.ts,
    # eas.json, google-services-*.json, GoogleService-Info-*.plist) trigger the store build.
    paths:
      - 'src/**'
      - 'app/**'
      - 'assets/**'
      - 'index.js'
      - 'lingui.config.ts'
  workflow_dispatch:
    inputs:
      environment:
        description: 'Target channel'
        required: true
        type: choice
        options: [stg, prd]

jobs:
  push-ota:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '23'
      - run: corepack enable
      - run: corepack prepare yarn@4.9.2 --activate
      - run: yarn install --immutable
      - run: curl -Ls https://cli.doppler.com/install.sh | sudo sh
      - id: env
        run: |
          if [ "${{ github.event_name }}" = "push" ]; then
            ENV="${{ github.ref_name == 'main' && 'prd' || 'stg' }}"
          else
            ENV="${{ inputs.environment }}"
          fi
          echo "channel=$ENV" >> "$GITHUB_OUTPUT"
      - name: Export JS bundle
        run: doppler run --project mobile --config ${{ steps.env.outputs.channel }} -- yarn expo export --platform ios --platform android --output-dir dist
        env:
          # config-scoped service token per env: DOPPLER_TOKEN (stg) / DOPPLER_TOKEN_PROD (prd)
          DOPPLER_TOKEN: ${{ steps.env.outputs.channel == 'prd' && secrets.DOPPLER_TOKEN_PROD || secrets.DOPPLER_TOKEN }}
      - name: Push OTA update
        # The script computes the per-platform runtimeVersion via the fingerprint (no
        # EXPO_RUNTIME_VERSION) under this same Doppler env, so it matches the store build.
        run: |
          doppler run --project mobile --config ${{ steps.env.outputs.channel }} -- \
            bash -c "EXPO_UPDATE_CHANNEL=${{ steps.env.outputs.channel }} node scripts/push-ota-update.mjs"
        env:
          # config-scoped service token per env: DOPPLER_TOKEN (stg) / DOPPLER_TOKEN_PROD (prd)
          DOPPLER_TOKEN: ${{ steps.env.outputs.channel == 'prd' && secrets.DOPPLER_TOKEN_PROD || secrets.DOPPLER_TOKEN }}
```

## package.json scripts

```json
{
  "build-ipa": "yarn pre-build && echo 'y' | doppler run --project mobile --config ${ENV:-stg} -- eas build --platform ios --profile preview --local --output ./device-app-build-${ENV:-stg}.ipa",
  "build-ipa:prd": "ENV=prd yarn build-ipa",
  "push-ota": "doppler run --project mobile --config ${ENV:-stg} -- bash -c 'yarn expo export --clear --platform ios --platform android --output-dir dist && EXPO_UPDATE_CHANNEL=${ENV:-stg} node scripts/push-ota-update.mjs'",
  "push-ota:prd": "ENV=prd yarn push-ota"
}
```

Note `echo 'y' |` before the `eas build` command — EAS local builds prompt for confirmation.

## Doppler vars (set per environment)

| Var | stg | prd |
| --- | --- | --- |
| `EXPO_UPDATE_URL` | `https://<stg-ref>.supabase.co/functions/v1/expo-update-manifest` | `https://<prd-ref>.supabase.co/functions/v1/expo-update-manifest` |
| `EXPO_UPDATE_CHANNEL` | `stg` | `prd` |

`EXPO_UPDATE_URL` is baked into the native config, so it **participates in the fingerprint** —
the OTA push and the build must run under the same Doppler env, or their fingerprints diverge
and the OTA never matches the build.

## How runtimeVersion works (`policy: 'fingerprint'`)

With `runtimeVersion: { policy: 'fingerprint' }` the runtime version is a per-platform **native
fingerprint hash** (e.g. iOS `489751…`, Android `7244faca…`) — **not** the app version. The
binary embeds the fingerprint computed at build time; each OTA is tagged with the fingerprint
`expo-updates fingerprint:generate` produces for that platform.

**OTAs are fingerprint-gated.** An OTA only reaches a binary whose embedded runtime fingerprint
**exactly matches** the OTA's `runtime_version`. A mismatch means the OTA *silently never
applies* — no error, the app just keeps running its old bundle. This is the #1 cause of "I
pushed an OTA but the device didn't update." (Debugging: read the live OTA's `runtime_version`
from the table/manifest and compare it to the build's fingerprint — see verification recipe below.)

**What changes the fingerprint:**

- **JS-only changes do NOT change it** → the OTA targets the same runtime as the installed
  build and applies. This is the whole point: ship JS via OTA, ship native via builds.
- **Native-config changes shift it — usually for BOTH platforms.** Native deps
  (`package.json`/`yarn.lock`), `app.config.ts`, config plugins, entitlements, build properties,
  patches, `firebase.json`, AND config-affecting env vars baked at build (e.g. `EXPO_UPDATE_URL`)
  all feed the hash. Confirmed first-hand: a one-line **iOS-only** `firebase.json` change shifted
  **both** the iOS and Android fingerprints. Such a change **cannot** be delivered by OTA — it
  needs new full builds of both platforms, and any device left on the old build stops receiving
  OTAs (its old fingerprint no longer matches new OTAs). No manual version bumping is needed: the
  hash changes automatically, so an OTA can never be served to a binary lacking the native module.

### ⚠️ Non-native files can silently bump the fingerprint — the `.gitignore` footgun

`@expo/fingerprint` hashes some files that have nothing to do with the native layer — notably
**`.gitignore`** (it is a fingerprint *source*). So a trivial edit like adding one ignore line
**changes the runtime fingerprint**, and from that push onward every OTA drifts off the
fingerprint your already-installed builds embed → OTAs **silently stop reaching them**. Confirmed
first-hand: a one-line `.gitignore` addition moved the hash and broke OTA delivery to every
shipped build until it was reverted.

- **Symptom:** OTAs that *used* to land suddenly don't — on every device at once — with **no
  native change** in the diff. `git diff <build-commit>..HEAD` shows only "harmless" files, but
  one of them (`.gitignore`, etc.) is in the fingerprint source set.
- **Diagnose:** checkout the build's commit and re-run `fingerprint:generate` — if the hash
  differs from HEAD, something non-native drifted it. To see exactly which file, dump the sources
  (under the build's Doppler env):

  ```bash
  # dump ALL sources (files AND "contents" sub-sources like packageJson:scripts)
  doppler run --project mobile --config stg -- node -e \
    'require("@expo/fingerprint").createFingerprintAsync(".").then(r=>console.log(
      r.sources.map(s=>(s.type||"")+"  "+(s.id||s.filePath)).join("\n")))'
  ```

  Two footgun shapes show up here: non-`node_modules` **`file`** entries (e.g. `.gitignore`) and
  **`contents:*`** entries — notably **`contents:packageJson:scripts`**, which means editing *any*
  npm script (`push-ota`, `deploy-store-*`, CI helpers) drifts the hash.

- **Immediate unblock (no rebuild):** revert the offending non-native edit so the OTA fingerprint
  matches the shipped builds again — a needed `.gitignore` entry can live in `.git/info/exclude`,
  which is **not** fingerprinted — then re-push the OTA.
- **Permanent fix — two mechanisms, by source type:**
  - **File sources** (e.g. `.gitignore`) → list them in a **`.fingerprintignore`** (gitignore glob
    syntax, repo root). The `expo-updates fingerprint:generate` CLI — which both the OTA push and
    the build use — honors it. Caveat: a `fingerprint.config.js` `ignorePaths` entry does **not**
    reliably drop `.gitignore`; use `.fingerprintignore` for files.
  - **Content sources** (e.g. `contents:packageJson:scripts`, `contents:expoConfig`) can't be
    path-ignored — skip them in **`fingerprint.config.js`** `sourceSkips`. Two common entries:
    - `'PackageJsonScriptsAll'` — editing *any* npm script won't drift the hash. Only safe if no
      script affects the native build (no prebuild/postinstall touching native; a JS-only
      `postinstall` like `i18n:compile` is fine).
    - `'ExpoConfigVersions'` — excludes `version` / `android.versionCode` / `ios.buildNumber` from
      the hash, so a **marketing version bump** (e.g. `1.1.0 → 1.2.0`) no longer strands OTAs.
      Without it, `version` is a fingerprint source and a bump silently moves the hash off every
      installed build. Genuinely worth having — but **introduce it ONLY bundled with a full build**
      (adding it re-hashes the baseline, so shipping it via OTA alone strands every current binary;
      see the recovery recipe below for the incident that proved this).
  - Both **shift the baseline hash**, so they ship **with a new build** (binary + OTAs adopt the
    stable hash together), never as a standalone OTA. Decide the full skip set *before* that build
    so you don't need another rebuild to add more. Afterward, **verify** the build's CI `Resolved
    runtime version` equals `fingerprint:generate`'s hash (both must honor the same config).
  - Only exclude **truly** non-native files/sources — excluding a real native input would let an
    OTA ship to a binary that's missing that native change.

### Recovering from a stranded fingerprint (a config change shipped via OTA)

If a fingerprint-affecting change (`fingerprint.config.js` `sourceSkips`, `.gitignore`, a native
config file) already went out **as an OTA rather than a build**, every installed binary is now on
the *old* hash and receives nothing — new OTAs silently reach no one. Two ways out; revert-and-
republish is almost always the right one:

- **Revert the offending change** (working tree + commit), then **republish** so the push recomputes
  the *old*, still-installed fingerprint. The OTA CI does **not** auto-fire on a
  `fingerprint.config.js`-only change — that file isn't in the workflow's `paths` filter — so
  trigger it manually per channel (`workflow_dispatch` sets both the Doppler config and the channel;
  `--ref main → prd`, else `stg`):

  ```bash
  gh workflow run expo-ota-update.yml --ref stg  -f environment=stg   # republish stg
  gh workflow run expo-ota-update.yml --ref main -f environment=prd   # republish prd
  ```

  Then confirm the new rows' `runtime_version` equals the installed builds' fingerprint (see
  *Verifying what's live*). Re-introduce the config change later, **bundled with a real build**.
- **Or roll forward** with new full builds of both platforms — but every device on the old build is
  stranded until it updates through the store, so revert-and-republish is the faster unblock.

> **Real incident:** adding `'ExpoConfigVersions'` to `sourceSkips` **via OTA** re-hashed the native
> layer for both platforms (the marketing-version decouple is a good change — it was the *delivery*
> that was wrong), stranding every install from all later OTAs. The reminder + biometric fixes
> reached nobody in prod until the skip was reverted and both channels were `workflow_dispatch`-
> republished at the original fingerprint. Lesson: a fingerprint-config change is a *build* event,
> never an OTA.

## Delivery & apply timing

`checkAutomatically: 'ON_LOAD'` + the default `fallbackToCacheTimeout: 0` means: the app
**launches immediately on its current bundle**, downloads any new matching update in the
**background**, and applies it on the **next cold start**. Consequences:

- A plain relaunch picks up the update on the next launch *after the download completes* (so the
  very next launch may still be old if the download hadn't finished — the one after gets it).
- **Background → foreground does NOT apply a pending update** — only a fresh process launch does.
- To apply immediately without waiting for a relaunch, expose an in-app "Update ready → restart"
  button that calls `Updates.reloadAsync()`.

## Verifying what's live

**1. Read the current build's fingerprint** (this is the `expo-runtime-version` value a real
device sends). Run under the same Doppler env as the build:

```bash
doppler run --project mobile --config stg -- yarn dlx expo-updates fingerprint:generate --platform ios
# → {"sources":[...],"hash":"489751…"}   ← the hash is the runtimeVersion
```

**2. Hit the manifest server with that exact fingerprint** — `noUpdateAvailable` before the
first matching push, a full manifest after. A wrong/old fingerprint always yields
`noUpdateAvailable`, which is exactly how a mismatch hides:

```bash
curl -s \
  -H "expo-platform: ios" \
  -H "expo-runtime-version: <fingerprint hash from step 1>" \
  -H "expo-channel-name: stg" \
  "https://<stg-ref>.supabase.co/functions/v1/expo-update-manifest"
```

**3. Query the table directly** to see every registered OTA and its `runtime_version` (compare
against step 1). PostgREST with the service-role key and `Accept-Profile: api` (the table is in
the `api` schema, not `public`):

```bash
curl -s \
  -H "apikey: $SUPABASE_SERVICE_ROLE_KEY" \
  -H "Authorization: Bearer $SUPABASE_SERVICE_ROLE_KEY" \
  -H "Accept-Profile: api" \
  "https://<stg-ref>.supabase.co/rest/v1/expo_updates?select=id,platform,runtime_version,created_at&order=created_at.desc"
```

If a freshly pushed row's `runtime_version` differs from the installed build's fingerprint, the
OTA will never reach that build — rebuild, or re-push from the exact build commit/env.

## Pushing an update

```bash
yarn push-ota        # stg
yarn push-ota:prd    # prd: the human runs this
```

Pushing to prd ships code to every production user. Push stg, verify, then hand the human the prd command.

Or just push to `stg`/`main` — the CI workflow fires automatically.

## Testing OTA updates

**Dev clients cannot test OTA** — they bypass `expo-updates` and connect to the local dev server instead.

**iOS simulator builds cannot test OTA** — use a device build.

You need a real binary with no dev server running:

| Platform | Build command | Install |
| --- | --- | --- |
| iOS | `yarn build-ipa` | Install `.ipa` via Xcode / Apple Configurator |
| Android | `yarn build-apk` | `adb install app-build.apk` or drag onto emulator |

Then open the app standalone (just tap the icon, no `yarn start`). On launch it checks for updates (`checkAutomatically: 'ON_LOAD'`). Push a JS change with `yarn push-ota`, kill and reopen — the update appears.

Confirm in Supabase: `api.expo_updates` should have a new active row with correct `channel`, `platform`, and `runtime_version`.

## Known bugs / gotchas

**Android OTA works out of the box. iOS requires all of the following to work:**

| Issue | Symptom | Fix |
| --- | --- | --- |
| Missing `assets/` directory | `ERR_UPDATES_FETCH: failed to load all assets` | iOS patch: `createDirectory(withIntermediateDirectories: true)` |
| NSURLSession ETag caching | `ERR_UPDATES_FETCH` after first successful OTA | iOS patch: 304 retry with stripped conditional headers |
| Static bundle key `'bundle'` | OTA ID updates but old code runs, no visible changes | Use `platformMeta.bundle` as key (unique per content hash) |
| Missing `extra.expoClient` | App crashes on OTA launch: `expo-linking needs access to manifest` | Include `expoClient: expoConfig` from `@expo/config` in `extra` |
| `createdAt` with `Z` suffix | iOS silently rejects manifest, OTA never applies | Use `.replace('Z', '+00:00')` — iOS `NSDateFormatter ZZZZZ` doesn't parse `Z` |
| Multipart missing trailing CRLF | iOS manifest parse fails | `chunks.join('\r\n') + '\r\n'` after closing boundary |
| `urlCache = nil` on URLSession | All 200 responses deliver nil data | Do NOT set this — use `reloadIgnoringLocalCacheData` per-request instead |
| Metro cache in OTA export | Bundle has stale code despite source changes | Always use `--clear` flag: `expo export --clear` |
| EAS local build wipes patches | NSLog/fixes disappear, OTA reverts to broken | Use `yarn patch` to persist patches — committed to `.yarn/patches/` |
| No Storage retention | `expo-updates` bucket grows to multiple GB, blows the free 1 GB cap | Call `pruneOtaUpdates()` after each push; `grant ... delete ...` to service_role |
