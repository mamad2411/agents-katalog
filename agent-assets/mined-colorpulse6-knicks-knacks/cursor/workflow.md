---
description: Follow this workflow when requested to create branches, make changes, open PRs, or set up CI/CD
globs: 
alwaysApply: false
---
# Workflow Rules
## Rule Type: Agent Requested

- Use **feature branches** (`feature/` or `bugfix/`) for new features and fixes.
- Commits must follow conventional commit messages:

feat(scope): add new feature
fix(scope): fix a bug
chore(scope): maintenance task
refactor(scope): code improvement without changing behavior

- Pull requests require code reviews and successful CI checks before merging.
- Auto deployment to Vercel (web) and Railway (API) upon merging to `main`.
- Mobile app builds:
- Expo OTA updates auto-deployed upon PR merge to `main`.
- EAS Build triggered manually or via GitHub Actions for store submissions.
- Testing coverage must aim for **>80%** on all new feature contributions.
- Keep README.md for each app/package clearly documented:
- Installation/setup
- Development instructions
- Deployment steps

---

## ✅ Testing & Linting

- Always run lint and tests before committing:
- `pnpm lint`
- `pnpm test`
- Run E2E tests for web apps using **Playwright**
- Confirm code adheres to `/packages/eslint-config`

---

## 🤖 CI/CD & Deployment

- Web apps:
- Deploy to **Vercel** on merge to `main`
- Backends:
- Deploy to **Railway** on merge to `main`
- Mobile:
- Trigger OTA updates via **Expo** on merge to `main`
- Manual or GitHub Action-based **EAS Build** for store releases

---

## 📝 Documentation

- Every app must include:
- `README.md` with setup, tech stack, and deployment steps
- `.env.example` file for environment variables
- Screenshots or GIFs if applicable

