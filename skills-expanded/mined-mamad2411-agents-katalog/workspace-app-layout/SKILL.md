---
name: workspace-app-layout
description: How each app under apps/* lays out its workspace package, pure environment factories, daemon/script bindings, and app singleton. Use when creating workspace-backed apps, adding daemon or script consumers, or deciding where browser-only, Bun-only, or platform-specific imports belong.
metadata:
  author: epicenter
  version: '4.0'
---

# Workspace App Layout

Workspace apps split construction from runtime side effects. Two shipped
shapes; pick by whether the app gates UI on signed-in identity.

**Shape A**: auth-gated SvelteKit web apps (fuji, honeycrisp, zhongwen):

```txt
apps/<app>/src/lib/
|- auth.ts                          createCookieAuth(), exports `auth`
`- session.svelte.ts                singleton: createSession + HMR + getSignedInSession()
apps/<app>/src/routes/(signed-in)/<app>/
|- index.ts                         iso doc factory: open<App>Doc({ encryptionKeys })
|- browser.ts                       browser factory: open<App>({ userId, peer, bearerToken, encryptionKeys })
|- daemon.ts                        long-lived daemon factory (cli-side)
|- script.ts                        one-shot script factory (cli-side)
`- integration.test.ts
```

No `client.ts`. The singleton lives in `session.svelte.ts`, where
`createSession({ auth, build })` owns the workspace lifecycle. The iso and
browser factories sit beside the signed-in routes because the app isn't a
running thing until identity exists.

**Shape B**: module-level singleton apps (opensidian, tab-manager, whispering):

```txt
apps/<app>/src/lib/<app>/
|- index.ts                         iso doc factory
|- browser.ts | extension.ts | tauri.ts   env binding (browser / chrome ext / Tauri)
|- client.ts                        singleton: auth wait + module-level open<App>(...)
|- daemon.ts                        long-lived daemon factory (if applicable)
|- script.ts                        one-shot script factory (if applicable)
`- integration.test.ts
```

`client.ts` is the only singleton with side effects; it blocks on
`session.whenReady` / `waitForAuthState` and exports a constructed handle.
Whispering is the simplest variant (no auth, no encryption, Tauri singleton).
Opensidian and tab-manager are scheduled to migrate to shape A
(`specs/20260507T054727-opensidian-tab-manager-create-session.md`); until
then, do not move their singleton during unrelated changes; review churn
isn't worth it.

For both shapes, `index.ts`, `browser.ts`, `daemon.ts`, and `script.ts` stay
pure construction surfaces. Side effects (auth subscriptions, HMR, persisted
state, network) live only in the singleton (`session.svelte.ts` for shape A,
`client.ts` for shape B).

## Layers

| File | Shape | Job | Imports | Returns |
| --- | --- | --- | --- | --- |
| `index.ts` or `core.ts` | A + B | Isomorphic doc factory | Workspace core, schemas, pure action factories | `ydoc`, tables, kv, encryption, actions, batch, dispose |
| `browser.ts` | A + B | Browser factory | Iso factory plus IndexedDB, BroadcastChannel, sync, browser caches | Doc bundle plus browser resources |
| `extension.ts` / `tauri.ts` | B | Env binding for non-web runtimes | Iso factory plus chrome.storage / Tauri APIs | Doc bundle plus runtime resources |
| `daemon.ts` | A + B | Long-lived daemon factory | Iso factory plus `attachYjsLog`, `attachSync`, materializers | Doc bundle plus writer persistence and sync |
| `script.ts` | A + B | One-shot script factory | Iso factory plus `attachYjsLogReader`, `attachSync` | Doc bundle plus readonly warm hydrate and sync |
| `auth.ts` | A | Auth client construction | `createCookieAuth` (or `createBearerAuth`) | `auth` |
| `session.svelte.ts` | A | App singleton + lifecycle | `createSession` from `@epicenter/svelte`, env factory, auth | `session`, `InferSignedIn`, module-level `getSignedInSession()` |
| `client.ts` | B | App singleton + auth wait | One env factory plus auth/session lifecycle | `auth` plus a running app singleton; module-level `await session.whenReady` |

Daemon and script factories live in the same directory as the iso/browser
factories regardless of shape; they're consumed by the `cli` package for
`epicenter up` (daemon) and one-shot script entry points.

## Iso Factory

The iso factory accepts an optional `clientID` so daemon and script peers can
use stable Yjs identities.

```ts
import { attachEncryption, type EncryptionKeys } from '@epicenter/workspace';
import * as Y from 'yjs';
import { createFujiActions, fujiTables } from '../workspace.js';

export function openFuji({
	encryptionKeys,
	clientID,
}: {
	encryptionKeys: () => EncryptionKeys;
	clientID?: number;
}) {
	const ydoc = new Y.Doc({ guid: 'epicenter.fuji', gc: false });
	if (clientID !== undefined) ydoc.clientID = clientID;
	const encryption = attachEncryption(ydoc, { encryptionKeys });
	const tables = encryption.attachTables(fujiTables);
	const kv = encryption.attachKv({});
	const actions = createFujiActions(tables);
	return {
		ydoc,
		tables,
		kv,
		encryption,
		actions,
		batch: (fn: () => void) => ydoc.transact(fn),
		[Symbol.dispose]() {
			ydoc.destroy();
		},
	};
}
```

Rules:

- Keep the iso factory free of `node:*`, `bun:*`, `chrome.*`, Tauri APIs,
  `y-indexeddb`, `BroadcastChannel`, and runtime singletons.
- Use relative imports for schemas when daemon or script files will import the
  factory outside Vite alias resolution.
- Put pure actions in the iso factory when they depend only on tables.
- Keep env-bound actions in the env factory when they need filesystem, SQLite,
  shell, browser persistence, or other runtime state. Opensidian actions stay
  extracted in `actions.ts`.

## Browser Factory

Browser factories hydrate local IndexedDB first and then attach sync with the
current public remote-action API.

```ts
export function openFuji({
	userId,
	peer,
	bearerToken,
	encryptionKeys,
}: {
	userId: string;
	peer: PeerIdentity;
	bearerToken?: () => string | null;
	encryptionKeys: () => EncryptionKeys;
}) {
	const doc = openFujiDoc({ encryptionKeys });
	const idb = doc.encryption.attachIndexedDb(doc.ydoc, { userId });
	attachOwnedBroadcastChannel(doc.ydoc, { userId });
	const awareness = attachAwareness(doc.ydoc, {
		schema: { peer: PeerIdentity },
		initial: { peer },
	});
	const sync = attachSync(doc, {
		url: toWsUrl(`${APP_URLS.API}/workspaces/${doc.ydoc.guid}`),
		waitFor: idb,
		bearerToken,
		awareness,
	});
	return { ...doc, idb, awareness, sync };
}
```

Do not restore `sync.peer()` or `describePeer()`. Remote calls use
`createRemoteActions`; manifest fetches use `describeRemoteActions`.

## Daemon Factory

Daemon factories own the writer side of local persistence.

```ts
export function openFuji({
	bearerToken,
	encryptionKeys,
	device,
	projectDir = findEpicenterDir(),
	clientID = hashClientId(projectDir),
	apiUrl = EPICENTER_API_URL,
}: {
	bearerToken?: () => string | null;
	encryptionKeys: () => EncryptionKeys;
	device: DeviceDescriptor;
	projectDir?: ProjectDir;
	clientID?: number;
	apiUrl?: string;
}) {
	const doc = openFujiDoc({ clientID, encryptionKeys });
	const persistence = attachYjsLog(doc.ydoc, {
		filePath: yjsPath(projectDir, doc.ydoc.guid),
	});
	const sync = attachSync(doc, {
		url: toWsUrl(`${apiUrl}/workspaces/${doc.ydoc.guid}`),
		bearerToken,
	});
	return { ...doc, persistence, sync };
}
```

Defaults:

- `projectDir = findEpicenterDir()`
- `clientID = hashClientId(projectDir)`
- `apiUrl = EPICENTER_API_URL`

The public lifecycle command is `epicenter up`. Do not document daemon
factories as `epicenter serve` consumers.

## Script Factory

Script factories read the daemon's local Yjs log and write through sync.

```ts
export function openFuji({
	bearerToken,
	encryptionKeys,
	projectDir = findEpicenterDir(),
	clientID = hashClientId(Bun.main),
	apiUrl = EPICENTER_API_URL,
}: {
	bearerToken?: () => string | null;
	encryptionKeys: () => EncryptionKeys;
	projectDir?: ProjectDir;
	clientID?: number;
	apiUrl?: string;
}) {
	const doc = openFujiDoc({ clientID, encryptionKeys });
	const persistence = attachYjsLogReader(doc.ydoc, {
		filePath: yjsPath(projectDir, doc.ydoc.guid),
	});
	const sync = attachSync(doc, {
		url: toWsUrl(`${apiUrl}/workspaces/${doc.ydoc.guid}`),
		bearerToken,
	});
	return { ...doc, persistence, sync };
}
```

Defaults:

- `projectDir = findEpicenterDir()`
- `clientID = hashClientId(Bun.main)`
- `apiUrl = EPICENTER_API_URL`

## Package Exports

Apps that expose daemon and script factories should export them explicitly.
Point each subpath at the file's actual owner. Signed-in-owned apps may export
from `src/routes/(signed-in)/...`; client-singleton apps usually export from
`src/lib/...`.

```json
{
	"exports": {
		"./workspace": "./src/routes/(signed-in)/fuji/workspace.ts",
		"./openFuji": "./src/routes/(signed-in)/fuji/index.ts",
		"./browser": "./src/routes/(signed-in)/fuji/browser.ts",
		"./daemon": "./src/routes/(signed-in)/fuji/daemon.ts",
		"./script": "./src/routes/(signed-in)/fuji/script.ts"
	}
}
```

Client-singleton apps use the same subpaths, but point at `src/lib/...`.

Do not export a running `client.ts` singleton from package exports.

## Tests

Every daemon/script pair should have a handoff test:

```txt
daemon opens projectDir
daemon writes rows
daemon disposes and closes writer persistence
script opens the same projectDir
script observes rows from attachYjsLogReader replay
```

## Anti-Patterns

- Putting auth, `createPersistedState`, `auth.onStateChange`, or HMR disposal in
  `browser.ts`, `daemon.ts`, or `script.ts`.
- Importing `daemon.ts` from browser code.
- Restoring `serve` as the public lifecycle command.
- Restoring `sync.peer()` or `describePeer()` as the primary remote action API.
- Inlining Opensidian actions back into `browser.ts`.
- Relocating `client.ts` (shape B) or `session.svelte.ts` (shape A) during a daemon-only change without a review reason.
- Adding a `client.ts` to a shape A app: the singleton already lives in `session.svelte.ts`. There is no second home.
- Putting auth subscriptions or workspace construction in a Svelte component: it belongs in the singleton (`session.svelte.ts` or `client.ts`).
