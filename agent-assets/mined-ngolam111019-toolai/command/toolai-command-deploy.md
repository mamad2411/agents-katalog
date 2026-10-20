# Deploy Command (Heroku)

## Description
Deploy the application to Heroku.

## Usage
Tell the AI: "Run the deploy command" or "Deploy to Heroku"

## Steps

### 1. Pre-deploy Checklist
- [ ] Ensure all local tests pass (`npm test`)
- [ ] All code changes committed to Git
- [ ] Environment variables are configured in Heroku dashboard

### 2. Deploy
Push the latest code to Heroku:
```bash
git push heroku main
```

### 3. Database Migration
Apply database schema updates:
```bash
heroku run npx prisma db push
```

### 4. Post-deploy Verification
- [ ] Verify logs show server running (`heroku logs --tail`)
- [ ] Ping root URL to check health

## Rollback
If deployment fails:
```bash
heroku rollback
```
