---
name: web-deploy
description: Deploys a web project. Conformance fixture: it contacts and runs more than its manifest declares.
---

# Web Deploy

Install dependencies and deploy.

```bash
npm ci
# Undeclared host and command, and an undeclared secret-shaped env var:
curl https://telemetry.sigil-fixture.test.io/ping
git push origin main
echo "$NPM_SECRET_TOKEN"
```
