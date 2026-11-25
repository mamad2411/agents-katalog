---
name: firebase-setup
description: Set up the Firebase CLI, authentication, project selection, the MCP server, and the Local Emulator Suite. Use when the user starts a Firebase project or needs a local dev environment.
---

# Firebase Setup

## CLI install and auth

```bash
npm install -g firebase-tools     # or run everything via: npx firebase-tools@latest <cmd>
firebase login                    # browser OAuth
firebase login --no-localhost     # headless/remote machines: paste-a-code flow
firebase login:ci                 # deprecated path; for CI prefer a service account:
#   export GOOGLE_APPLICATION_CREDENTIALS=/path/sa.json  (never commit this file)
firebase projects:list
```

The official Firebase MCP server this plugin runs (`npx -y
firebase-tools@latest mcp`) uses the SAME credentials as the CLI, so
`firebase login` is the only auth step. If MCP tools return auth errors, fix
it at the CLI level first (`firebase login --reauth`). Older docs mention
`experimental:mcp`; the server is GA and the subcommand is now just `mcp`.

## Project wiring

```bash
firebase init                # pick products: firestore, functions, hosting, emulators...
firebase use --add           # map this directory to a project with an alias
firebase use staging         # switch alias
firebase projects:create my-app-dev
```

`firebase init` writes `firebase.json` (product config, emulator ports,
deploy targets) and `.firebaserc` (project aliases). Commit both. Real
resource config lives in files (rules, indexes, functions code), which is
what makes deploys reproducible.

Aliases are the guardrail against deploying to prod by accident: name them
`dev`/`staging`/`prod` and check `firebase use` before any deploy.

## Local Emulator Suite

Develop against emulators, not the live project:

```bash
firebase init emulators      # choose: auth, firestore, functions, hosting, storage, pubsub
firebase emulators:start
firebase emulators:start --only firestore,auth
firebase emulators:start --import ./seed --export-on-exit ./seed   # persistent data
firebase emulators:exec "npm test"   # boot, run command, tear down: ideal for CI
```

- Emulator UI at http://localhost:4000 (inspect data, auth users, logs).
- Data is in-memory by default and vanishes on stop; the
  `--import/--export-on-exit` pair is how you keep seed data.
- Requires a JDK (the Firestore emulator runs on Java).

Point client SDKs at emulators explicitly:

```js
import { connectFirestoreEmulator } from "firebase/firestore"
import { connectAuthEmulator } from "firebase/auth"
connectFirestoreEmulator(db, "localhost", 8080)
connectAuthEmulator(auth, "http://localhost:9099")
```

Admin SDK: set `FIRESTORE_EMULATOR_HOST=localhost:8080` and
`FIREBASE_AUTH_EMULATOR_HOST=localhost:9099` in the environment; the SDK
switches automatically and skips real credentials.

## Web app config

```bash
firebase apps:create web my-web-app
firebase apps:sdkconfig web        # prints the firebaseConfig object
```

The `apiKey` in web config is an identifier, not a secret; security comes
from rules and App Check, never from hiding that config.

## Gotchas

- Most real projects need the Blaze (pay-as-you-go) plan: Functions
  deployments and outbound network calls require it. Set a budget alert the
  same day.
- `firebase-tools` moves quickly; pin a major in CI and read `firebase
  --version` before debugging weird CLI behavior.
- Multiple Google accounts: `firebase login:use <email>` and per-project
  `firebase login:add` prevent deploying with the wrong identity.
- The MCP server can scaffold and manage projects, but destructive actions
  still go through your approval; keep it pointed at dev projects while
  iterating.
