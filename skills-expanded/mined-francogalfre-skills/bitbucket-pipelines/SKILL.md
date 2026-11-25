---
name: bitbucket-pipelines
description: Writes and debugs Bitbucket Pipelines CI/CD configuration. Use when the user says "set up Bitbucket Pipelines", "write a bitbucket-pipelines.yml", "my pipeline is failing", "add a deployment step", "configure CI for Bitbucket", "add tests to my pipeline", "set up staging and production deployments in Bitbucket", or shares a bitbucket-pipelines.yml and asks for help.
---

# Bitbucket Pipelines

Writes correct, efficient `bitbucket-pipelines.yml` files. Covers install,
test, build, and deploy steps — with caching, branch-based conditions,
environment variables, and deployment environments.

---

## Required Details

| Detail | Example |
|---|---|
| **Language / runtime** | Node.js 20, Python 3.11, etc. |
| **Package manager** | npm / pnpm / yarn |
| **Test command** | `npm run test`, `pnpm vitest` |
| **Build command** | `npm run build` |
| **Deploy target** | AWS, Vercel, SSH, custom script |
| **Branch strategy** | `main` → production, `develop` → staging |
| **Secrets needed** | `AWS_ACCESS_KEY_ID`, `VERCEL_TOKEN`, etc. |

---

## Instructions

### Step 1 — Start with the correct base structure

```yaml
image: node:20

definitions:
  caches:
    node: node_modules        # cache node_modules between runs

pipelines:
  default:                    # runs on every branch push
    - step:
        name: Test
        caches:
          - node
        script:
          - npm ci
          - npm run test

  branches:
    main:                     # runs only on main
      - step:
          name: Test & Build
          caches:
            - node
          script:
            - npm ci
            - npm run test
            - npm run build
      - step:
          name: Deploy Production
          deployment: production
          script:
            - npm run deploy
```

### Step 2 — Add caching correctly

```yaml
definitions:
  caches:
    node: node_modules        # cache by folder path
    pnpm: ~/.pnpm-store       # for pnpm

# Per step:
caches:
  - node
```

Always use `npm ci` not `npm install` in pipelines — it's faster and deterministic.

### Step 3 — Configure deployment environments

```yaml
pipelines:
  branches:
    develop:
      - step:
          name: Deploy Staging
          deployment: staging        # maps to Bitbucket environment
          script:
            - npm run deploy:staging

    main:
      - step:
          name: Deploy Production
          deployment: production
          trigger: manual            # require manual approval for prod
          script:
            - npm run deploy:production
```

### Step 4 — Use environment variables correctly

```yaml
# Reference repo/workspace/deployment variables — never hardcode secrets
script:
  - echo "Deploying to $ENVIRONMENT"
  - AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID ./deploy.sh
```

Set secrets in: Repository Settings → Repository Variables (or Deployment Variables for per-environment secrets).

### Step 5 — Parallel steps for speed

```yaml
- parallel:
    - step:
        name: Unit Tests
        script:
          - npm ci
          - npm run test:unit
    - step:
        name: Type Check
        script:
          - npm ci
          - npm run typecheck
    - step:
        name: Lint
        script:
          - npm ci
          - npm run lint
```

### Common deploy patterns

**Deploy to AWS via SST**
```yaml
- step:
    name: Deploy to AWS
    deployment: production
    script:
      - npm ci
      - npx sst deploy --stage production
    caches:
      - node
```

**Deploy to Vercel**
```yaml
- step:
    name: Deploy to Vercel
    script:
      - npm i -g vercel
      - vercel --token $VERCEL_TOKEN --prod
```

**Deploy via SSH**
```yaml
- step:
    name: Deploy via SSH
    script:
      - pipe: atlassian/ssh-run:0.4.1
        variables:
          SSH_USER: $SSH_USER
          SERVER: $SERVER_IP
          COMMAND: 'cd /app && git pull && npm ci && pm2 restart app'
```

---

## Non-Negotiable Acceptance Criteria

- [ ] Uses `npm ci` not `npm install`
- [ ] Secrets are referenced as `$VARIABLE_NAME` — never hardcoded
- [ ] Production deployments use `trigger: manual` or branch protection
- [ ] Caches are defined in `definitions.caches` and referenced per step
- [ ] Each step has a descriptive `name`
- [ ] `deployment:` tag is set on deploy steps for environment tracking in Bitbucket

---

## Output Format

~~~
## bitbucket-pipelines.yml

```yaml
[complete pipeline file]
```

## Setup Required
- [environment variables to add in Bitbucket settings]
- [any external setup: SSH keys, deployment environments, etc.]

## Notes
- [branch strategy explanation]
- [any manual trigger or approval steps]
~~~