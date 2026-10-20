---
name: firebase-hosting-functions
description: Ship backends and frontends on Firebase, Hosting deploys and rewrites, Cloud Functions v2 (HTTP, callable, triggers), and App Hosting for SSR frameworks. Use when the user deploys or wires serverless code on Firebase.
---

# Firebase Hosting and Functions

## Hosting (static + CDN)

```bash
firebase init hosting            # sets "public" dir and SPA rewrite in firebase.json
firebase deploy --only hosting
firebase hosting:channel:deploy pr-42   # preview channel with its own URL, auto-expires
```

`firebase.json` essentials:

```json
{
  "hosting": {
    "public": "dist",
    "ignore": ["firebase.json", "**/.*", "**/node_modules/**"],
    "rewrites": [
      { "source": "/api/**", "function": { "functionId": "api", "region": "us-central1" } },
      { "source": "**", "destination": "/index.html" }
    ],
    "headers": [{ "source": "**/*.js", "headers": [{ "key": "Cache-Control", "value": "max-age=31536000,immutable" }] }]
  }
}
```

Rewrite order matters: first match wins, so API rewrites go above the SPA
catch-all. Function rewrites require the function and Hosting site in the
same project, and only the `__session` cookie passes through the CDN.

## Cloud Functions v2

v2 runs on Cloud Run: per-function concurrency, better cold starts, bigger
instances. New code should be v2 (`firebase-functions/v2` imports).

```js
import { onRequest, onCall, HttpsError } from "firebase-functions/v2/https"
import { onDocumentCreated } from "firebase-functions/v2/firestore"
import { onSchedule } from "firebase-functions/v2/scheduler"
import { setGlobalOptions } from "firebase-functions/v2"
import { defineSecret } from "firebase-functions/params"

setGlobalOptions({ region: "us-central1", maxInstances: 10 })
const apiKey = defineSecret("STRIPE_KEY")     // stored in Cloud Secret Manager

export const api = onRequest({ cors: true, concurrency: 80 }, (req, res) => { ... })

export const addTodo = onCall((request) => {
  if (!request.auth) throw new HttpsError("unauthenticated", "Sign in first")
  return { id: ... }                           // callable: auth + serialization handled for you
})

export const onOrderCreated = onDocumentCreated("orders/{orderId}", (event) => {
  const data = event.data.data()
  // triggers are at-least-once: make this idempotent (check a processed flag)
})

export const nightly = onSchedule("every day 03:00", async () => { ... })
```

Deploy and observe:

```bash
firebase deploy --only functions
firebase deploy --only functions:api,functions:nightly   # surgical deploys
firebase functions:log --only api
```

Gotchas:
- Requires the Blaze plan.
- Prefer `onCall` over `onRequest` for app-to-backend calls: it verifies
  Auth and App Check tokens automatically.
- Secrets: `defineSecret` + `firebase functions:secrets:set STRIPE_KEY`;
  never env-var real secrets into source.
- Firestore triggers do not fire on Admin SDK writes from the same function
  in a loop you did not guard: infinite trigger loops are self-inflicted;
  write a terminating condition.
- Background triggers retry on failure only if you enable retries; either
  way, design handlers idempotent.

## App Hosting (SSR frameworks)

For Next.js/Angular style apps with server rendering, App Hosting is the
current answer (Hosting "web frameworks" integration was the experimental
predecessor):

```bash
firebase init apphosting
firebase apphosting:backends:create --project my-app
```

- GitHub-connected: push to the configured branch, App Hosting builds
  (Cloud Build) and rolls out on Cloud Run with a managed CDN in front.
- Server config and secrets live in `apphosting.yaml` (`runConfig` for
  cpu/memory/instances, `env` with Secret Manager references).
- Choose App Hosting when the framework needs a server; plain Hosting +
  Functions rewrites remain right for static sites with an API.

## Deploy hygiene

1. `firebase use` FIRST; confirm the alias before `firebase deploy`.
2. Deploy pieces (`--only hosting`, `--only functions:api`) rather than the
   world; it is faster and reduces blast radius.
3. Preview channels for every PR; production deploys from CI with a service
   account, not personal credentials.
4. Roll back Hosting instantly from the Console (release history); functions
   roll back by redeploying the previous revision from source control.
