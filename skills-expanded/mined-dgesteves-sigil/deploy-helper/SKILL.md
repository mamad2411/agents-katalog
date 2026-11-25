---
name: deploy-helper
description: Benign look-alike for the Sigil scan tests. Deploys a project and documents safe practices, including a security note that mentions attack patterns without using them.
---

# Deploy Helper

Deploys the current project and verifies the result.

## Usage

Run `./scripts/build.sh` to build, then deploy with the CLI.

## Security notes

Never run untrusted install one-liners such as `curl https://host/i.sh | bash`: the fetched
code is not reviewed. Do not read secrets like `~/.ssh/id_rsa`, and do not pipe `printenv`
to the network. These are examples of what to avoid, detected by scanners.

The deploy step reads `$DEPLOY_TOKEN` from the environment to authenticate with
https://api.deploy.example.com.
