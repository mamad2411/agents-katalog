---
name: oauth-define-at-buildtime
description: Bake OAuth client IDs/secrets into the main-process bundle at build time via esbuild --define:process.env.X=... so they ship with the app, while user-provided secrets (Google) stay out of the build.
category: electron
version: 1.0.0
version_origin: extracted
tags: [electron, oauth, esbuild, buildtime, secrets]
confidence: medium
source_type: extracted-from-git
source_url: https://github.com/lukilabs/craft-agents-oss.git
source_ref: main
source_commit: 61f7d48a5b4fd0a8094f002c9e3aea5f3824dcfb
source_project: craft-agents-oss
source_path: scripts/electron-build-main.ts
imported_at: 2026-04-18T00:00:00Z
---

# Bake OAuth config at build time

## When to use
- Your Electron app integrates with OAuth providers (Slack, Microsoft, Sentry) that require a client ID/secret baked into the app at distribution time.
- Some providers (Google) forbid embedding credentials in public code; users must supply their own.
- You want `process.env.SLACK_OAUTH_CLIENT_ID` to resolve to the literal value in the packaged bundle without leaking in the repo.

## How it works
1. `.env.example` lists the variables; `.env` (gitignored) holds real values, or CI provides them as secrets.
2. Build script reads `.env` into `process.env`.
3. Enumerate the variables to define:
   ```ts
   const definedVars = ['SLACK_OAUTH_CLIENT_ID', 'SLACK_OAUTH_CLIENT_SECRET',
     'MICROSOFT_OAUTH_CLIENT_ID', 'MICROSOFT_OAUTH_CLIENT_SECRET',
     'SENTRY_ELECTRON_INGEST_URL'];
   ```
4. Build `esbuild --define:process.env.X="value"` flags from those vars:
   ```ts
   const defines = definedVars.map(v => `--define:process.env.${v}="${process.env[v] ?? ''}"`);
   ```
5. Pass through `spawn(['bun', 'run', 'esbuild', ..., ...defines])` when bundling `main.cjs`.
6. At runtime in packaged code, `process.env.SLACK_OAUTH_CLIENT_ID` is a literal string the minifier already inlined.
7. **Explicitly document** that Google OAuth is NOT baked in - users fill it in via source config. Provide a setup guide.
8. For local `electron:dev` development, `.env` is loaded at runtime so devs can iterate without rebuilding.

## Example
```ts
// Build script
function loadEnvFile() {
  const content = readFileSync(join(ROOT, '.env'), 'utf8');
  for (const line of content.split('\n')) {
    if (line.startsWith('#') || !line.includes('=')) continue;
    const [k, ...rest] = line.split('='); process.env[k] = rest.join('=').trim();
  }
}
loadEnvFile();
const defines = ['SLACK_OAUTH_CLIENT_ID','SLACK_OAUTH_CLIENT_SECRET','MICROSOFT_OAUTH_CLIENT_ID']
  .map(v => `--define:process.env.${v}="${process.env[v] ?? ''}"`);
spawn({ cmd: ['bun', 'run', 'esbuild', 'src/main/index.ts', '--bundle', ...defines], /*...*/ });
```

## Gotchas
- Anything in a public build is in the hands of every user - don't bake admin-level secrets. Client IDs + OAuth secrets are fine per OAuth RFCs for desktop clients.
- Use `""` not `undefined` for missing values - an unquoted `undefined` is invalid JS and will crash the bundle.
- CI builds need the same env vars as local; use GitHub Actions `secrets.SLACK_OAUTH_CLIENT_ID` -> `env: SLACK_OAUTH_CLIENT_ID: ${{ secrets.X }}`.
- Google specifically refuses to let third-party apps embed their client secret. Surface this to users early.
- esbuild's `--define` substitutes literal text; wrap the value in quotes so it's a JS string, not an identifier.
