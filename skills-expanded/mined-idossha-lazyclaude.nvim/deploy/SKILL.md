---
name: deploy
description: Deploy the application to staging or production
user_invocable: true
---

# Deployment

Deploy workflow:
1. Run `npm test` to verify all tests pass
2. Run `npm run build` to create production build
3. For staging: `npm run deploy:staging`
4. For production: `npm run deploy:prod` (requires manual confirmation)
5. Verify health check at the deployed URL
6. Report deployment status
