---
name: Project Tooling
description: 'Use when changing dependencies, package scripts, environment variables, repository configuration, or deployment settings.'
applyTo: "package.json, yarn.lock, .env*, .gitignore, vite.config.ts, public/_redirects, README.md"
---

# Project Tooling

- Use Yarn 4.12.0. Do not run `npm install` or add `package-lock.json`; manage dependencies with `yarn add`, `yarn add -D`, or `yarn remove`.
- Never commit secrets. Keep local values in ignored `.env`; add each new variable name to `.env.example` with a short English comment and no real secret value. Ensure `.env` and `.env.local` remain ignored.
- Treat every `VITE_*` variable as public and embedded in the client build. Only use it for values safe to expose publicly; never place credentials, private API keys, or server-side secrets in frontend environment variables.
- Review dependencies for known vulnerabilities with the available Yarn audit workflow after dependency changes and before releases.
- Use only scripts defined in `package.json`. Do not run `yarn lint` or `yarn build` for small changes unless requested; ask before running them after a large change.
- Preserve the SPA fallback in `public/_redirects` when changing client-side routing. The production build outputs to `dist`.
