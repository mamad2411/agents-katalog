---
name: dokku-deploy
description: PaaS deployment with Dokku
version: 1.0.0
tags: [paas, deployment, docker, self-hosted]
---

# Dokku – Self-Hosted PaaS

Dokku is the smallest PaaS — a Docker-powered Heroku alternative
for deploying apps via `git push` on your own server.

- **GitHub**: github.com/dokku/dokku (30 000+ ⭐)
- **License**: MIT
- **Security**: Mature project (10+ years). No malware.

## Usage Examples

### Create an app

```bash
dokku apps:create my-app
```

### Deploy via git push

```bash
git remote add dokku dokku@server:my-app
git push dokku main
```

### Set environment variables

```bash
dokku config:set my-app DATABASE_URL=postgres://...
```

### Add SSL via Let's Encrypt

```bash
dokku letsencrypt:enable my-app
```

## AI Agent Tips

- `git push` deployment — just like Heroku.
- Plugin ecosystem: databases, caching, SSL, cron, and more.
- Runs on a single $5/month VPS.
- Dockerfile, Buildpack, and Cloud Native Buildpack support.
