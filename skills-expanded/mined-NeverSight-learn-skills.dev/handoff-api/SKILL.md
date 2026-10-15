---
name: handoff-api
description: Upload, organize, and share content in a Handoff deployment by calling its BFFless pipeline API directly, authenticating with a BFFless API key (X-API-Key)
---

# Handoff API

Handoff is a give-away file-sharing app that runs on BFFless: it has no app
server — its `/api/*` endpoints are a BFFless proxy rule set attached to the
deployment's alias. This skill drives them directly as an agent, against any
Handoff deployment.

## Base URL

Resolve the deployment's base URL, in order:

1. `HANDOFF_BASE_URL` env var, if set.
2. Ask the user, or take it from context (e.g. "my handoff is at
   handoff.example.com").

Examples below use `$HANDOFF_BASE_URL` (e.g. `https://handoff.example.com`).
If the base URL came from the user rather than an already-set env var, export
it (`export HANDOFF_BASE_URL=https://handoff.example.com`) so the examples
below run verbatim.

## Auth (send a BFFless API key as X-API-Key)

Every `/api/*` call needs an API key for the BFFless project serving the
deployment, sent as the `X-API-Key` header. Source it in order:

1. **`BFFLESS_API_KEY` env var** (CI, sandboxes, any runtime):

       curl -H "X-API-Key: $BFFLESS_API_KEY" "$HANDOFF_BASE_URL/api/nodes"

2. **The `bffless` CLI credential store** (requires `bffless` >= 0.3.1; filled
   by a one-time human `bffless login` per machine + instance):

       npx bffless auth token   # run standalone first — see below before embedding it in curl

   Inside a cloned Handoff repo, `auth token` resolves the instance from
   `.bffless/config.json` automatically; elsewhere pass
   `--api-url https://admin.example.com` (the BFFless admin URL, not the
   Handoff URL). A fresh fork's committed `.bffless/config.json` still points
   at the upstream demo instance — check that its `apiUrl` is *your* instance
   before trusting the auto-resolve, and pass `--api-url` explicitly if not.

`$(npx bffless auth token)` substitutes to an **empty string** on failure (the
error goes to stderr, not stdout), so a failed lookup silently becomes
`X-API-Key: ` rather than a visible error. Run `npx bffless auth token` on its
own first; only once it exits 0 and prints a key, embed it:
`curl -H "X-API-Key: $(npx bffless auth token)" "$HANDOFF_BASE_URL/api/nodes"`.
If it exits non-zero, or neither this nor `BFFLESS_API_KEY` yields a key, stop
and tell the user to run `npx bffless login` (or export `BFFLESS_API_KEY`). Do
not hunt for keys in agent-runtime config files.

The key authenticates as its owner, so content you create is owned by that
user (the same as uploading in the browser). The PUT-to-bucket step (below) is
the one exception — it is presigned and takes no key.

Two *different* things can be wrong with a key, and they need different checks.
Run both before concluding anything about what content exists.

**1. Is the key recognised?** An unrecognised key is not rejected — it falls
through to *anonymous*, and the read endpoints answer anonymously rather than
erroring. The usual cause is a key for a **different instance**: `bffless login`
stores one credential per admin URL, and `auth token` will hand you whichever one
it resolves. Compare the full bodies, not a `head -c` prefix:

    curl -s "$HANDOFF_BASE_URL/api/nodes" | python3 -m json.tool > /tmp/anon.json
    curl -s -H "X-API-Key: $KEY" "$HANDOFF_BASE_URL/api/nodes" | python3 -m json.tool > /tmp/keyed.json
    diff /tmp/anon.json /tmp/keyed.json    # byte-identical ⇒ NOT recognised

**If they match, the key is not recognised — stop and fix it, do not work around
it.** Check that the admin URL you logged into belongs to the same instance as
`$HANDOFF_BASE_URL` (`handoff.example.com` → `admin.example.com`), then
`npx bffless login --api-url https://admin.example.com`.

**2. Is it the *right user*?** A recognised key authenticates as exactly one
user, and the diff above passes for **any** valid user on the instance — so it
gives a false all-clear. This is the failure that wastes the most time: the human
runs `bffless login`, but a stale `BFFLESS_API_KEY` is already exported and
**outranks it** (source order above: env var beats the CLI store). Every call
then succeeds while showing a *different account's* tree, and the user's own
folders look like they do not exist.

Suspect it whenever a path the user just linked you resolves `401`, or the root
listing lacks folders they say are there. Compare the two sources directly:

    echo "env: ${BFFLESS_API_KEY:0:12}…"
    echo "cli: $(npx bffless auth token --api-url https://admin.example.com | head -c 12)…"

If they differ, the env var is shadowing the login. Use the CLI key explicitly
(`CLI_KEY=$(npx bffless auth token --api-url …)`, then send `$CLI_KEY`) and tell
the user their `BFFLESS_API_KEY` is stale — the login was never the problem.
There is **no `/api/me`** endpoint to ask "who am I" with (requesting it returns
the SPA, not a 404 — see Gotchas); the available identity signal is the `ownerId`
on a node the user says is theirs.

A recognised key authenticates as its owner: nodes it creates carry that user's
`ownerId`, and it can list, delete, and patch them.

Every write is rejected with `401` when the key is unrecognised. Older
deployments accepted those writes and recorded `"ownerId": null` — orphans that
no API key can delete, because no key can reach `edit` on them. If you find some,
tell the user; they need an admin in the browser.

## Discovery

In a Handoff repo clone, the endpoint source of truth is the authored rules
under `.bffless/proxy-rules/` — `handoff/` (the `/api/*` app backend) and
`handoff-rss-feed/` (the public `/feed/*` feeds). Each route is a
`rules/**/rule.yaml` whose path mirrors the URL. Outside a clone (or for live
state), `get_proxy_rule_set` via a BFFless MCP connection to the instance
works too, but is optional.

## Resolve a path to a node

Every write is keyed by `parentId`, but users hand you *paths* — a URL like
`https://handoff.example.com/tree/claude`, or just "put it in claude".
`GET /api/resolve/<path>` turns one into the other:

    curl -s -H "X-API-Key: $BFFLESS_API_KEY" "$HANDOFF_BASE_URL/api/resolve/claude"
    → {"node":{"id":"a46c2c42-…","type":"folder","path":"claude",
               "parentId":"root","mode":"restricted","ownerId":"…"}}

The path is everything after `/tree/` or `/blob/` in the browser URL, encoded per
segment (`Design%20Docs/Q3`). Folders resolve by walking names down the tree,
files and Sites by their storage key. It runs the same ACL gate as the serve
endpoint, so the answer reflects what you may actually see:

| Status | Meaning |
| --- | --- |
| `200` | Resolved and readable — use `node.id` as `parentId`. |
| `401` | No credential, key unrecognised, **or the path exists and this user cannot see it**. |
| `404` | No such path. |

`403` is *not* what an inaccessible path returns here — a restricted folder you
lack a grant on answers `401`, the same as sending no key at all. So **`401` does
not mean your key is broken.** The load-bearing distinction is `401` vs `404`:

- `404` — the path genuinely does not exist.
- `401` on a path the user can see in their browser — the path exists and you are
  authenticated as the **wrong user**. Go back to Auth check 2; do not report the
  folder as missing.

`GET /api/nodes?parentId=<id>` follows the same rule: `401` when the folder is
real but invisible to you.

Use it before any write into a named folder. **Do not** tree-walk
`GET /api/nodes?parentId=…` hunting for an id, and **do not** read the app's node
table through the BFFless admin API — `resolve` is the supported route and it
sees restricted folders that a listing will never show you.

`GET /api/nodes?path=…` is *not* a resolver: the parameter is silently ignored
and you get the whole root listing back, which looks like an answer and is not
one.

## Read a file back (download)

List the folder, then pull each node's bytes. **Take the path from the node JSON
and URL-encode it programmatically — never retype it** (see Gotchas: filenames
carry invisible characters). Two routes, both fine:

**Direct** — GET the node's own `url` with the key. Fewest calls:

    curl -s -H "X-API-Key: $KEY" -o out.png \
      "$HANDOFF_BASE_URL/api/uploads/content/tmp/Screenshot%20…png"

**Presigned** — `POST /api/sign` `{path: <node.storageKey>}` →
`{signed:{url,…}}`. The returned `url` is **host-relative**, exactly like
`uploadUrl` (`/api/storage/presigned/local?key=…&exp=…&sig=…`), so prefix
`$HANDOFF_BASE_URL`. It carries its own signature — the GET takes no key. Use it
when the bytes must be fetched by something that has no API key.

Note `path` here is the **`storageKey`** (`bffless/handoff/uploads/content/…`),
not `node.path` and not `node.url` — three similar-looking fields on the same
node. A `storageKey` that does not match a stored object byte-for-byte answers
`403`, not `404`, so a mistyped key reads as a permissions failure.

Verified folder download (both files in `tmp/`), driving straight off the listing:

    curl -s -H "X-API-Key: $KEY" "$HANDOFF_BASE_URL/api/nodes?parentId=$FOLDER_ID" \
     | python3 -c "
    import sys, json, os, subprocess, urllib.parse
    base, key = os.environ['HANDOFF_BASE_URL'], os.environ['KEY']
    for n in json.load(sys.stdin)['nodes']:
        if n['type'] != 'file': continue
        url = base + urllib.parse.quote(n['url'])          # verbatim from the node
        subprocess.run(['curl','-s','-o',n['name'],'-H',f'X-API-Key: {key}',url])
    "

## Upload a file (prepare → PUT → register)

1. `POST /api/uploads/prepare` `{filename, contentType, path, parentId}` → `{uploadUrl, storageKey, originalName, …}`
2. `PUT <uploadUrl>` with `Content-Type: <type>` and the raw file bytes (direct to bucket, no key)
3. `POST /api/nodes` `{storageKey, originalName, parentId:"root"|<folderId>, displayName, createdMs}` → `{node}`

- **`path` is required** — Handoff uses a *verbatim* key strategy (structural
  storage), so prepare needs the file's **verbatim content sub-path**: the
  owning folder's path + the filename. At root that is just the filename
  (`report.md`); in a folder it is `<folder path>/<filename>`
  (`Design Docs/Q3/report.md`). In a repo clone this is what
  `contentSubPath(folderPath, filename)` computes in
  `apps/handoff/src/lib/contentPath.ts`. Omitting `path` fails with
  `400 MISSING_KEY` ("expected a path string for verbatim keyStrategy").
- **`parentId`** (`"root"` or a folder id) should match `path`'s folder.
  Sending it to *prepare* lets an in-folder name collision be rejected
  **before** any bytes are minted/PUT, so an existing file is never
  overwritten.
- Pass the `storageKey` prepare returns to register **unchanged** (it is the
  full bucket key).
- `createdMs` is client-supplied epoch ms, e.g. `date +%s%3N`.
- **`uploadUrl` comes back host-relative** (`/api/storage/presigned/local?…`).
  `curl -X PUT` on it fails with exit 3 / `%{http_code} 000`. Prefix
  `$HANDOFF_BASE_URL` unless it already starts with `http`.
- **Register takes no mime field.** The rule reads exactly `parentId`,
  `originalName`, `displayName`, `path`, `storageKey`, `createdMs` from the
  body — the node's `mime` is derived from the stored object, and on local
  presigned storage it lands as `application/octet-stream` even when you PUT
  `Content-Type: text/markdown`. Nothing in the request fixes this, so don't
  burn calls trying; a `.md` extension in the name is what the viewer has to go
  on.
- Send `path` to register too (same value as prepare) — it is the register
  handler's storage key, not just a prepare-time argument.
- A name collision on register is `409`, with the same "An item with that name
  already exists" text the folder endpoint returns.

Verified root upload (`report.md`): prepare
`{filename:"report.md", contentType:"text/markdown", path:"report.md", parentId:"root"}`
→ PUT bytes to `uploadUrl` → register with the returned `storageKey`.

## Upload renderable HTML (a Site, not a File)

**Registering HTML through `POST /api/nodes` gives a node that never renders.**
The viewer picks its preview from the node *type*, not the mime: `previewFor()`
(`apps/handoff/src/lib/preview.ts`) returns `'site'` only for `type: 'site'`,
and a `text/html` File falls through every branch to `'download'` — the
"Preview unavailable" card. HTML has to be registered as a **Site**:

1. Choose the Site's `name`. It is both the display name and a **path
   segment**, so keep it URL-clean (`ce-v0.2.18-release-review`, not
   `report`). Its content prefix is `contentSubPath(<owning folder path>,
   <name>)` — at root just `<name>`, in a folder `<folder path>/<name>`.
2. For every asset: `POST /api/uploads/prepare`
   `{filename, contentType, path: "<prefix>/<relPath>"}` → `PUT` the bytes.
   Send **no `parentId`** — a Site's assets are bucket objects, not nodes, so
   there is nothing to collide with.
3. `POST /api/sites` `{parentId, name, entry, path: "<prefix>", createdMs}` →
   `{node}` with `type: "site"` and `url` =
   `/api/uploads/content/<path>/<entry>`.

- `entry` is the index document, default `index.html`. The UI's
  `planSiteUpload()` (`apps/handoff/src/lib/site.ts`) picks it the same way:
  root `index.html` if present, else the single `*.html`, else it asks.
- **A lone HTML file can be a Site** — no folder drop needed. Upload it as
  `<prefix>/index.html` and register the Site. This is the API equivalent of
  the UI's "Import as Site" prompt.
- Keep the pretty name out of the path: set a human title with
  `PATCH /api/node/meta` (below) and let `name` stay URL-safe.
- **There is no rename**: `name` and `path` are fixed at creation. To rename,
  re-upload under the new prefix, register a new Site, then delete the old
  node.
- Assets referenced relatively (`assets/app.css`, `../img/x.png`) resolve
  because the whole bundle is stored verbatim under the prefix on the same
  `/api/uploads/content/*` origin (ADR-0001).
- **The entry document must declare `<meta charset="utf-8">`.** Content is
  served as bare `content-type: text/html` — the charset param is dropped even
  if the object was stored with one — so a document without the meta tag falls
  back to windows-1252 and any non-ASCII byte turns to mojibake (`·` → `Â·`).
  Inside the viewer it looks *fine*, because an iframe with no declared charset
  inherits the parent page's UTF-8; the corruption only appears when the
  content URL is opened directly. Check the file (a fragment saved without a
  `<head>` usually lacks it) and prepend
  `<!DOCTYPE html>\n<meta charset="utf-8">` before uploading.

Verified in-folder Site (`reports/ce-v0.2.18-release-review`, single file):
prepare `{filename:"index.html", contentType:"text/html",
path:"reports/ce-v0.2.18-release-review/index.html"}` → PUT → `POST /api/sites`
`{parentId:<reports id>, name:"ce-v0.2.18-release-review", entry:"index.html",
path:"reports/ce-v0.2.18-release-review"}` → renders at
`/blob/reports/ce-v0.2.18-release-review`.

## Other operations

- List a folder: `GET /api/nodes?parentId=<id>` → `{nodes:[…]}` (omit param for root)
- Create folder: `POST /api/folders` `{parentId, name, createdMs}` → `{node}`
- Read a file back: GET `node.url` with the key, or `POST /api/sign`
  `{path:<storageKey>}` → `{signed:{url,…}}` (host-relative) — see "Read a file
  back" above
- Share a folder: `POST /api/share-links` `{folderId, expiresMs?}` → share link
- Delete: `DELETE /api/node?id=<uuid>` → `{id}` (refuses a non-empty folder with 409)
- Set a File/Site's display title + description (feed-surfaced metadata):
  `PATCH /api/node/meta` `{id, title?, description?}` → `{id, title, description}`
  (needs edit on the parent folder; at least one field required, empty string
  clears it)
- Set a folder's sharing mode or feed exclusion: `PATCH /api/node`
  `{id, mode?: "inheriting"|"restricted", feedExcluded?: boolean}` → `{id, mode}`
  (owner/admin only; at least one field required; 400 invalid, 403 forbidden).
  `inheriting` folders take their ancestors' grants; `restricted` cuts off
  inheritance so access is re-derived from the folder's own grants.

## Permissions (grants)

Per-folder access control — the mechanism behind "content is private-by-default".
In all three calls `folderId` is a folder UUID or the literal `root` (the
caller's "My Files" root).

- List: `GET /api/grants?folderId=<id|root>` → `{grants:[{principalId, principalEmail?, principalType?, principalName?, level}]}`
- Add/update: `POST /api/grants` `{folderId, principalId, principalEmail?, principalType?, principalName?, level: "view"|"edit"}`
  → `{grants:[…]}` — upserts by `principalId`; folder owner or admin only (403 otherwise)
- Revoke: `POST /api/grants/revoke` `{folderId, principalId}` → `{grants:[…]}`
  (owner/admin only)

**User grants**: a traditional per-user grant with `principalId` and
`principalEmail`. The email identifies the user.

**Group grants**: set `principalType: "group"` and `principalName` (the group's
display name, a snapshot at grant time). A group grant matches any *member* of
that CE User Group. The `principalName` is informational; membership is
authoritative and evaluated live per request — removing a user from the group
revokes their access on the next request. Requires the CE release that ships
member-accessible group endpoints; on older CE, group endpoints 404 and group
features degrade gracefully.

The reserved principal `anyone` is what "Public" means: granting it makes the
folder world-viewable. It is always capped at `level: "view"` (the server
silently downgrades `edit`), carries no email, and never has a `principalType`
or `principalName` — publicness can never escalate to edit.

**Group management**:
- Discover groups: `GET /api/groups?search=<query>&limit=<n>` → `{groups:[{id, name, memberCount}]}` (member-accessible picker; blank search lists all up to limit). Used to build a group-selector UI.
- Own memberships: `GET /api/me/groups` → `{groups:[{id, name}]}` (the groups this user belongs to). Both endpoints require the CE release shipping member-accessible group endpoints; 404 on older CE versions.

Observed on at least one deployment: both group endpoints answer
`401 {"message":"unauthorised"}` to a valid `X-API-Key` that every other endpoint
accepts — note the `message` envelope, where the rest of the API uses `error`.
Treat group features as unavailable to API-key callers unless you have confirmed
otherwise on that deployment, and do not read the 401 as a bad key.

## Gotchas

- An empty root listing is normal: content is private-by-default; you only see
  what you own or were granted. But a listing that is merely *smaller* than what
  the user describes is usually the wrong-user problem, not privacy — Auth
  check 2.
- **An unknown `/api/*` route returns `200 text/html`, not `404`.** The request
  falls through to the Handoff SPA and you get `index.html` with a success
  status. A typo'd or non-existent endpoint therefore looks like it worked until
  you read the body — `curl … | head` shows `<!doctype html>`. Check that a `200`
  is actually JSON before trusting it, and do not infer an endpoint exists
  because it did not 404. (`/api/me` is one that does not exist.)
- **Filenames carry characters that are not the ones you would type.** macOS
  screenshots use U+202F (narrow no-break space) before `AM`/`PM`; it is
  indistinguishable from a space in terminal output, in a browser URL, and in
  this file. Hand-retyping such a name into `/api/sign` or a content URL fails
  with `403` — which reads as a permissions problem and is not one. Always take
  `storageKey` / `url` / `path` verbatim from the node JSON and URL-encode in
  code, never by hand.
- **Creating requires access to the destination.** `POST /api/folders`,
  `/api/nodes`, `/api/sites`, and `/api/uploads/prepare` answer `401` with no
  credential and `403` without `edit` on the target folder. The check runs
  *before* the name-collision check, so a `403` tells you nothing about whether
  the name is free. At root, any authenticated user may create.
- **A `409` at root can name something you cannot see.** Root is a shared
  namespace and in-folder uniqueness is owner-blind, so a name taken by another
  user's private folder collides for you too. Pick a different name — do not
  switch to the root node's UUID to get around it (next bullet).
- **`parentId: "root"` and the root node's UUID are different destinations.**
  The literal `"root"` is the real root; passing the root node's id creates the
  node one level down, under `My Files/`, with no error either way. If a
  `"root"` create fails on a name collision, switching to the UUID *looks* like
  it worked — it silently put your folder somewhere else. Never use it as a
  workaround.
- The PUT step is unauthenticated and goes straight to the bucket — do not add
  the key.
- Delete is write-gated and single-node; delete children before parents.
- **To correct a file you already registered, re-PUT its storage key.** Call
  `prepare` again with the same `path` and **no `parentId`** (which skips the
  node collision check), then PUT the new bytes: the node still points at that
  key, so the served content updates in place. This is the only way to fix a
  file when the key cannot `DELETE` or `PATCH`. Caveat: `node.size` is set at
  register time and is **not** refreshed, so it goes stale after an overwrite.
- A `text/html` upload registered via `POST /api/nodes` shows "Preview
  unavailable" — that is the type, not a broken file. Use `POST /api/sites`
  (above).
