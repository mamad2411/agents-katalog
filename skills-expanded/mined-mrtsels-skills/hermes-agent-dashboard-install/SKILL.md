---
name: hermes-agent-dashboard-install
description: Install and troubleshoot Hermes Agent web dashboard
triggers:
  - hermes dashboard install
  - hermes-agent web dashboard
  - hermes dashboard build failed
tags:
  - hermes-agent
  - web-dashboard
  - troubleshooting
---

# Hermes Agent Web Dashboard — Install Guide

## Prerequisites

```bash
# Hermes venv may not have pip — bootstrap it first
~/.hermes/hermes-agent/venv/bin/python -m ensurepip

# Install web + pty extras
~/.hermes/hermes-agent/venv/bin/python -m pip install 'hermes-agent[web,pty]'
```

## Build & Launch

```bash
hermes dashboard
# or with options:
hermes dashboard --port 9119 --host 127.0.0.1 --no-open
```

If the build fails with a "Cannot find native binding" error from `@tailwindcss/oxide`:

```bash
cd ~/.hermes/hermes-agent/web
rm -rf node_modules package-lock.json
npm install --registry https://registry.npmmirror.com
npm run build
hermes dashboard --no-open
```

## Common Issues

### Missing TypeScript declarations for `lucide-react`

**Error:** `Could not find a declaration file for module 'lucide-react'`

**Fix:** Create a declaration stub:

```bash
mkdir -p ~/.hermes/hermes-agent/web/src/types
echo 'declare module "lucide-react";' > ~/.hermes/hermes-agent/web/src/types/lucide-react.d.ts
```

Then retry `npm run build`.

### npm install times out or hangs

Use a Chinese npm mirror for faster, more reliable downloads:

```bash
npm install --registry https://registry.npmmirror.com
```

### Hermes venv has no pip

```bash
~/.hermes/hermes-agent/venv/bin/python -m ensurepip
~/.hermes/hermes-agent/venv/bin/python -m pip install 'hermes-agent[web,pty]'
```

## Notes

- Dashboard runs at `http://127.0.0.1:9119` by default
- All data stays on localhost — nothing exits the machine
- If frontend hasn't been built and `npm` is available, it builds automatically on first `hermes dashboard` launch
- Profile-aware config: `~/.hermes/config.yaml`, logs: `~/.hermes/logs/`
