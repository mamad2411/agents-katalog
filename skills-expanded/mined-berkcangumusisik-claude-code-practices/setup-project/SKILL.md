---
name: setup-project
description: Onboards a new developer - explains the project, runs setup steps, verifies everything works
user-invocable: true
allowed-tools: Bash Read Glob
effort: medium
---

## Project Setup & Onboarding

1. Read the project:
```bash
cat README.md 2>/dev/null | head -60
cat package.json | grep -E '"name"|"description"|"scripts"' -A 10
ls src/ 2>/dev/null
```

2. Run the setup sequence:
```bash
# Install dependencies
npm install 2>&1 || bun install 2>&1

# Check environment
ls .env* 2>/dev/null
```

3. Env vars check - if `.env` is missing, copy from `.env.example` and list what needs filling:
```bash
cp .env.example .env 2>/dev/null && echo "Created .env from example"
```

4. Database setup:
```bash
npx prisma migrate dev 2>/dev/null || echo "No Prisma detected"
```

5. Run the dev server:
```bash
npm run dev 2>&1 | head -20 &
sleep 3
curl -s http://localhost:3000/health 2>/dev/null || echo "Check manually"
```

6. Run tests:
```bash
npm test 2>&1 | tail -10
```

7. Produce a summary report:
```
Project: [name]
Stack: [detected tech]
Setup: ✅ complete / ❌ issues found

Next steps for new developer:
1. Fill in .env: STRIPE_SECRET_KEY, SENDGRID_API_KEY
2. Run: npm run db:seed
3. Read: docs/architecture.md
```
