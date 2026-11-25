---
name: darkmatter-ts-toolchain
description: 'The darkmatter TypeScript toolchain contract - Bun (never npm/pnpm), tsgo typecheck, vitest, oxlint/biome, changesets, Effect for I/O, Alchemy deploys (wrangler.toml is prohibited), merge-queue mains, and the no-tiny-functions rule. Use when writing, fixing, building, or shipping TypeScript in any darkmatter repo (platform, nixmac-web, omp-chat, genesis): "fix TS errors", "make CI green", "add a package", "deploy this worker", lockfile complaints, or choosing libraries for I/O-heavy code. Do NOT use for generic TS style (coding-standards) or deep Effect patterns (effect-typescript) — this skill is the org-specific toolchain glue around those.'
---

# Darkmatter TypeScript toolchain

Org-wide contract for TS repos (platform, nixmac-web, and friends). The stack
is deliberate; substituting familiar defaults (npm, jest, wrangler) creates a
second convention and breaks CI.

## Package management — Bun only

- Install: `bun install`; CI uses `bun install --frozen-lockfile`. If CI fails
  with "lockfile had changes, but lockfile is frozen", the lockfile is out of
  sync with a `package.json` — fix by running `bun install` locally and
  committing `bun.lock`; never delete the lockfile to "fix" it.
- Run scripts with `bun run <script>`; execute tools with `bun x <tool>`.
- Monorepos use Turbo + workspaces (`@repo/*` packages). Add shared code to a
  workspace package, not a relative `../../` import across apps.

## Verify in this order

```bash
bun run typecheck   # tsgo -p tsconfig.json (NOT tsc)
bun run test        # vitest
bun run lint        # oxlint / biome per repo
```

Run the narrowest target that covers your change first (single test file,
single package), the repo-wide gates before handing off. All three must pass
on main; merge queues enforce required checks — prefer a PR over a direct
push even when your credentials technically bypass protection.

## Effect for meaningful I/O

Code with real I/O (network, DB, queues, retries) uses Effect — services,
Layers, typed errors, `Config` for env. Load the `effect-typescript` skill
for patterns. Plain async/await is fine for trivial glue; don't wrap a single
fetch in ceremony.

## Deploys — Alchemy, never wrangler

- Infrastructure is code in `alchemy.run.ts`; `wrangler.toml` is prohibited.
- Deploy: `STAGE=prod bun run deploy` (per-app; check the app's README/run
  config for required env). Secrets come from `himitsu read <path>` at deploy
  time and SOPS for config — never hardcoded.
- Alchemy's config schema requires `SOPS_AGE_KEY` explicitly in env; it does
  NOT fall back to `~/.config/sops/age/keys.txt`:
  `SOPS_AGE_KEY=$(grep '^AGE-SECRET-KEY-' ~/.config/sops/age/keys.txt | head -1)`.
- Vite apps: `client` build must precede `ssr` build (hydration manifest).

## Releases

Changesets are the release source of truth: user-facing changes ship with a
`.changeset/*.md`; version bumps and changelogs are generated, not hand-edited.

## Style rules that surprise newcomers

- **No tiny functions**: don't extract a function whose whole body is one
  expression/return — inline it unless the name is a durable contract with
  multiple call sites (enforced as `ts-no-tiny-functions`).
- Conventional Commits, subject ≤50 chars; body only when the why isn't
  obvious.
- Fix problems at the source; no leftover shims, aliases, or re-exports after
  a refactor.
