---
name: deploy-web
description: Deploy the NeuralAgent relay and website (agent.neuralhub.dev) to the relay host by hand and verify it is live. Use only when the user asks to deploy, "go live", "website/changelog live machen", or after a release when they asked for the deploy.
---

# Deploy relay + website

Background: `docs/RELEASING.md` → "Deploying the relay and website". Rules: `AGENTS.md`.
**Only when the user asked for a deploy in this session.** The relay serves the website,
`/admin/`, the `/app/` web remote, `/changelog`, update manifests and the phone tunnel, so a broken
deploy cuts every remote user off. Never print `/etc/neuralagent/relay.env` or other secrets.

## 1. Before
- Working tree: the deploy ships what `git ls-files` lists **from your working copy**, including
  uncommitted edits. Run `git status --short`; if other agents have half-done changes, ask the user
  first (or deploy from a clean worktree).
- Checks, all green:
  ```
  pnpm typecheck && pnpm test && pnpm lint:tokens && pnpm check:docs
  cargo test -p na-relay 2>&1 | grep -E "test result|FAILED|error" | tail -10
  pnpm --filter @neuralagent/web build 2>&1 | tail -5
  ```
- Note what is live now: `curl -s https://agent.neuralhub.dev/version.json` (`version`, `built`;
  a 404 means a web build from before D44).

## 2. Deploy (repo root)
```
git ls-files -z | rsync -a --from0 --files-from=- ./ root@192.168.30.96:/opt/neuralagent/src/
ssh root@192.168.30.96 'docker tag ghcr.io/lepro10/neuralagent-relay:latest neuralagent-relay:prev 2>/dev/null; cd /opt/neuralagent/src && docker build -f deploy/relay/Dockerfile -t ghcr.io/lepro10/neuralagent-relay:latest . 2>&1 | tail -5 && cd /opt/neuralagent && docker compose up -d'
```
The Dockerfile builds `apps/web` itself (the local build above is only a check) and bundles it.
The `prev` tag is the rollback point.

## 3. Verify (all must pass)
```
curl -fsS https://agent.neuralhub.dev/api/health
curl -fsS https://agent.neuralhub.dev/version.json          # `built` is from the last minutes, `version` as expected
curl -fsS https://agent.neuralhub.dev/changelog.json | head -c 300
curl -fsS -o /dev/null -w "%{http_code} /changelog\n" https://agent.neuralhub.dev/changelog
curl -fsS -o /dev/null -w "%{http_code} /app/\n" https://agent.neuralhub.dev/app/
curl -fsS https://agent.neuralhub.dev/api/releases/latest | head -c 300
ssh root@192.168.30.96 'docker ps --filter name=neuralagent-relay --format "{{.Status}}"; docker logs --since 5m neuralagent-relay 2>&1 | grep -E "ERROR|panic" | tail -5'
```
Optional look: `node scripts/dev/shot.mjs` drives a local UI only; for the live site take a
screenshot of `https://agent.neuralhub.dev/changelog` with playwright-core (phone + desktop).
Open web remotes and Android apps offer "Update → Reload" within a few minutes.

## 4. If something is wrong
Roll back at once, then investigate locally:
```
ssh root@192.168.30.96 'docker tag neuralagent-relay:prev ghcr.io/lepro10/neuralagent-relay:latest && cd /opt/neuralagent && docker compose up -d'
```

## 5. After
Update `docs/HANDOFF.md` (what is live, build id) and tick the STATUS checklist item if any.
Tell the user in short, simple German what is live and what they can check.
