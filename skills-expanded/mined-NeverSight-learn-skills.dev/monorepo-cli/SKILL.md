---
name: monorepo-cli
description: Manage the CLI tools monorepo using helper scripts. Use when checking CI status, release commits, or managing multiple CLI projects.
---

# Monorepo CLI

Cross-project management for the CLI tools monorepo.

## Overview

This skill provides helper scripts for managing multiple CLI projects in the monorepo:
- App-Store-Connect-CLI
- Google-Drive-CLI
- Google-Play-Developer-CLI
- Grokipedia-CLI
- App-StoreKit-CLI
- App-Store-Server-CLI
- Apple-Map-Server-CLI
- MyMarketNews-CLI
- cimis-cli

## Available Scripts

### check-ci-status.sh

Check GitHub Actions CI status for all projects.

```bash
# Human-readable output
./skills/monorepo-cli/scripts/check-ci-status.sh

# JSON output for automation
./skills/monorepo-cli/scripts/check-ci-status.sh --json
```

**Output:**
- Shows emoji indicators for each project
- Success: ✅
- Failure: ❌
- No runs: ⚠️
- Unknown: ❓

## Prerequisites

- GitHub CLI (`gh`) installed and authenticated
- Access to all monorepo repositories

## Agent Best Practices

1. **Check CI first** before releases
2. **Use JSON output** for automation
3. **Review all projects** - one failure can block releases
