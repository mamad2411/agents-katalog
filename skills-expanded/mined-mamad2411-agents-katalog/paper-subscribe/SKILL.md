---
name: paper-subscribe
description: Subscribe to the centrally generated paper-daily feed, prepare a local digest, and deliver it on a schedule.
---

# Paper Subscribe

Use this skill when a user wants to subscribe to the centrally generated paper feed instead of producing papers themselves.

## Workflow

1. Create a local config from `templates/config.example.json`
2. Install a cron job with `install-cron.sh`
3. On schedule:
   - `prepare-digest.js` reads the public `feed-papers.json`
   - filters items by topic/language/max items
   - emits a digest JSON
   - `deliver.js` sends it to stdout

## Commands

Prepare a digest:

```bash
node skill/paper-subscribe/scripts/prepare-digest.js --config ~/.paper-subscribe/config.json
```

Deliver a digest:

```bash
node skill/paper-subscribe/scripts/deliver.js --config ~/.paper-subscribe/config.json --input /tmp/digest.json
```

Install cron:

```bash
bash skill/paper-subscribe/scripts/install-cron.sh --config ~/.paper-subscribe/config.json
```
