# Firebase shared-project safety

This app uses the shared Firebase project `inter-level-progress-manager`.

The only authoritative Firestore and Storage rules repository is:
https://github.com/jeevanvarghese579/school-softwares-firebase-shared-config

Do not create, replace, or deploy Firestore/Storage rules from this app's repository. Do not run an unscoped `firebase deploy`.

Preserve strict application isolation. This app may access only `/apps/{APP_KEY}/users/{uid}/...`.

Access must also be controlled through Firebase Access Manager using this app's fixed Firebase Web App ID.

If rules need to change:

1. Clone or update the canonical shared-rules repository.
2. Modify only its canonical `firestore.rules` or `storage.rules` file.
3. Do not weaken, remove, or overwrite rules belonging to other apps.
4. Add or update emulator tests for this app.
5. Run the complete rules test suite.
6. Perform a Firebase dry run.
7. Show the exact proposed rule changes and obtain the user's explicit approval before deploying them.

Never introduce broad permissions such as `allow read, write: if request.auth != null;`.

Never allow access to another application's namespace, generic `/users/**` paths, or unidentified legacy collections.

For Hosting, deploy only the intended site: `firebase deploy --only hosting:{SITE_NAME}`.

For Functions, deploy only explicitly named functions. Never delete or migrate production data without an exact manifest, backup confirmation, and the user's explicit action-time approval.

## Existing isolated app identifiers

This is an existing isolated app.

Canonical appKey: `gymTracker`

Firebase Web App ID: `1:379503088311:web:f430dcb999873898133332`

Hosting site: `jeevansgymtracker`

Preserve these identifiers and the existing Firestore data paths. Do not create a new namespace or migrate data unless the user explicitly requests it. If the requested feature needs additional permissions, make the smallest possible change in the canonical shared-rules repository and test every existing app rule before deployment.
