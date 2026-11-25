---
name: firebase-deploy-checklist
description: "Runs a pre-deploy checklist before shipping the Workshop Pulse frontend, Firestore rules, indexes, and Cloud Functions to Firebase. Triggers on: deploy firebase, ship to production, pre-deploy, release checklist, firebase preflight, deploy hosting, deploy rules, deploy functions."
---

# Firebase Deploy Checklist

Execute six steps in order. Stop on first failure and report.

1. **Lint + typecheck**
   - `cd frontend && npm run lint && npm run typecheck`
2. **Build**
   - `cd frontend && npm run build`
3. **Rules unit tests** (if present)
   - `cd backend && firebase emulators:exec --only firestore "npm test --prefix tests"`
4. **Env audit**
   - Confirm `.env` for frontend has `VITE_FIREBASE_*` and `VITE_AGENT_ENDPOINT`.
   - Confirm functions runtime env has `GOOGLE_CLOUD_PROJECT`, no inline keys.
5. **Indexes diff**
   - `firebase firestore:indexes` and compare to `backend/firestore.indexes.json`.
6. **Dry-run deploy**
   - `firebase deploy --only hosting,firestore:rules,firestore:indexes,functions --dry-run`

## Output

Return a checklist with ✅/❌ per step and the exact command output for any failure.
Do not run the actual `firebase deploy` unless the user explicitly confirms after
all six steps pass.

## Rules

- Never bypass step 3 by mocking rules; always run against the emulator.
- Never deploy functions with secret env values; require Secret Manager refs.
