---
name: live-dev-storage-init
description: Provisions Firebase project and Firestore database. Automatically configures .firebaserc, firebase.json, and secure firestore.rules using local rules references, and guides on billing or Blaze-plan error escalations.
---

# live-dev-storage-init

This skill handles backend resource provisioning specifically for Firebase and Firestore database setup.

`bash` blocks are POSIX (Git Bash on Windows). Any logic beyond one command/pipe lives in `resources/*.js` (if applicable), never in shell control flow. If your Bash tool is cmd.exe or PowerShell, translate each snippet before running it.

## 1. Firebase & Firestore Provisioning

Configure or verify Firebase resources in this order:

| Resource | Skip if | Constraints |
| --- | --- | --- |
| Firebase project | `.firebaserc` | Project ids are globally unique → generate `<repo-name>-<rand4>`, never ask the user to invent one. |
| Firestore database | it already exists | id is the literal `'(default)'` — quote it, bash eats the parens. Location `us-central1` unless data-residency is stated. |
| `firebase.json` | file exists | `firebase init firestore` must run non-interactively; hand-write the file if it prompts. Without it, both deploy and the emulator fail. |
| `firestore.rules` | never skip | author before deploying: `allow read, write: if false;` + per-collection auth rules from `references/react-firestore-rules.md`. Deploy immediately — never leave test-mode rules live. |

- Blaze-plan features (Cloud Functions, outbound calls from triggers) need a card entered in the Console — the CLI cannot do it. This is the only legitimate console visit. On any billing/plan error: stop → name the single step → link `https://console.firebase.google.com/project/<id>/usage/details` → resume on confirmation.
- Local QA verification using Firestore emulator should follow rules in `references/react-firestore-rules.md`.
