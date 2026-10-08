---
name: deploy-prod
description: Deploy the current project to PRODUCTION through the platform with every gate — pre-flight, tests, independent review, migration review, backup and rollback statements, and a human approval bound to HEAD. Stops if any gate is not met.
---

Hand this to the `deployment` agent: deploy environment **prod**. High risk.
1. Pre-flight in words: repo, branch `main` vs current, HEAD, tree state, migrations since last prod deploy.
2. `make test`, then ask `review` for an independent check of what changed since the last prod deploy.
3. Check approval: `dev approve prod --verify`. If it exits 4, stop and ask the user to run `! dev approve prod` in this session, then re-verify. You cannot approve; the hook denies it.
4. `dev deploy prod`; read its output.
5. Report health, last log lines, URL, and record that the approval was consumed. On failure offer `dev rollback prod`.
