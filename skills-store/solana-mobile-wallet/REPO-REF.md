# Repo Referensi: solana-mobile/solana-mobile-skills

Repo: https://github.com/solana-mobile/solana-mobile-skills
Ref lokal: /Users/chaali0324/.agents/repo-refs/solana-mobile_solana-mobile-skills
API: curl "localhost:27126/repos/readme?name=solana-mobile_solana-mobile-skills"
Dibuat: 2026-09-16

## Cuplikan README
# solana-mobile/solana-mobile-skills

Source: https://github.com/solana-mobile/solana-mobile-skills
Fetched: 2026-09-16

## README
# Solana Mobile dev skills

Agent skills for building Solana apps on Android with Expo and React Native. These follow the
[Agent Skills](https://agentskills.io) convention — a `SKILL.md` per skill directory — so they
work with Claude Code, Codex, OpenCode, Cline, Amp, and the other agents the installer below
supports.

The repository is also packaged as an [Agent Plugin](https://agent-plugins.org): the root
[`plugin.json`](plugin.json) manifest plus the `skills/` directory make it a portable plugin
that compatible clients can discover and load directly.

## Skills

| Skill | What it covers |
| --- | --- |
| [`integration-privy`](skills/integration-privy/SKILL.md) | Privy authentication over Mobile Wallet Adapter, via Sign-In-With-Solana |
| [`seeker-connect`](skills/seeker-connect/SKILL.md) | Seeker Connect: web dapps talking to the Seeker's built-in wallet |
| [`seeker-domains`](skills/seeker-domains/SKILL.md) | `.skr` domain resolution in both directions, with server and client integration |
| [`seeker-genesis-token`](skills/seeker-genesis-token/SKILL.md) | Seeker device ownership via SGT verification and Sign-in-with-Solana |
| [`solana-mobile`](skills/solana-mobile/SKILL.md) | Project scaffolding, templates, emulators, development builds, toolchain checks |
| [`solana-mobile-publishing`](skills/solana-mobile-publishing/SKILL.md) | Signing a release APK and publishing to the Solana dApp Store |
| [`solana-mobile-wallet`](skills/solana-mobile-wallet/SKILL.md) | Mobile Wallet Adapter: connect, disconnect, sign, send |

Each skill is a self-contained directory: a `SKILL.md` with the procedure, and `references/`
with detail the agent loads only when it needs it. That keeps the up-front context cost small
while the long-form material stays available.

Skills covering a third-party service are prefixed `integration-`, so they group together in
a listing and stay distinguishable from the first-party ones.

## Install

Use [`skills`](https://github.com/vercel-labs/skills), the same installer
`npx solana-mobile create` uses to add the Solana dev skill:

```bash
npx -y skills add solana-mobile/solana-mobile-skills
```

That prompts for which skills and which agents. To take everything without prompts:

```bash
npx -y skills add solana-mobile/solana-mobile-skills --all
```

Skills land in `.agents/skills/`, which most agents read direc
