# Deploy Skill

This skill handles deployments for the project.

## When to use this skill

- Deploying feature branches to preview environments
- Deploying production builds from the main branch
- Verifying deployment status and URLs
- Troubleshooting deployment or cache issues

## Critical Rules

### Always deploy from the correct directory

> **Note:** This sandbox workspace has no deployed frontend. Deploy skills apply after March 11 in hackathon submission repos.

```bash
cd <frontend-dir>
npm run build
<deploy-command> --branch <branch-name>
```

### Feature branches use preview deploys

```bash
# For feature branches (creates preview deployment)
<deploy-command> --branch feature/my-branch

# ALWAYS report the preview URL to the user for testing
# Do NOT rely on alias URLs if they may have stale cache
```

### Production deploys only from main

```bash
# Only after merge to main AND explicit approval
git checkout main
cd <frontend-dir> && npm run build
<deploy-command> --branch main
```

### Verification steps

After any deployment:
1. Run deployment list command to confirm successful deploy
2. Test a critical endpoint on the preview URL
3. Verify expected content is returned (not an HTML fallback)

## Common issues

### Cache issues

Deployment alias URLs may serve stale cached content from previous deployments. Always test on the **random/unique preview URL** first.

### Missing bindings

If API routes return errors, verify bindings in the project configuration match the correct resource IDs.

## Related files

- Project deployment configuration (e.g., `wrangler.json`, `vercel.json`, `netlify.toml`)
- Worker / API entry point
- `docs/decision-log.md`
