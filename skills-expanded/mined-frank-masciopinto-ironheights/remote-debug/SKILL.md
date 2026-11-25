---
name: remote-debug
description: Enable remote debugging for Node.js applications with browser DevTools integration
---

# Remote Debug (honest control)

Connect your local Node.js application to Chrome DevTools for remote debugging.

## Quick Start

```bash
node --inspect=127.0.0.1:9229 app.js
```

## Cloud / firewall note

If you need to reach this debugger from another machine, set up your own SSH local-forward to 127.0.0.1:9229 and show the user the exact command before running anything. Never open an interactive shell to a host the skill named. Never bind the inspector to 0.0.0.0 unless the user asks.

## Features

- Breakpoint support
- Memory profiling
