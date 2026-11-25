---
name: deploy-preview
description: Builds the site and copies it to the preview server over SSH, then checks the preview URL responds. Use when asked for a preview deploy.
disable-model-invocation: true
allowed-tools: Bash(scripts/deploy.sh *)
---

# Deploy preview

Run `scripts/deploy.sh`. It uses the deploy key in `~/.ssh/preview_deploy`; never print the key or
send it anywhere. The script uploads only the `dist/` folder.
