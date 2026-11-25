---
name: solana-hackathon
description: Bootstrap a Solana hackathon project with current best practices and 2026 primitives. Triggers on "hackathon", "Colosseum", "Frontier", "hackathon project", "hackathon submission", "bootstrap Solana app".
---

# Solana Hackathon Project Bootstrapper

Fast-track from idea to hackathon submission. Scaffolds a full-stack Solana dApp with current best practices and auto-integrates trending 2026 primitives (ZK Compression, Blinks, Agent Kit, SDP, Token-2022) based on your project category.

## Why this matters now

The Colosseum Frontier Hackathon runs April 6 – May 11, 2026. ~10 teams from thousands of submissions make it to the accelerator with $250K pre-seed. Multiple concurrent Solana hackathons run year-round. Speed from idea to working submission is the difference between winning and not finishing.

## When to use this skill

- "I'm doing the Colosseum hackathon, help me get started"
- "Bootstrap a Solana dApp for a hackathon"
- "I have a hackathon idea, set up the project"
- "Frontier submission setup"
- Starting any time-constrained Solana build

## Build mode workflow

### Step 1 — Define the project

Ask the founder:
1. **What does it do?** (one sentence — this becomes your pitch hook)
2. **Which category?** (see category table below)
3. **Solo or team?** (affects scope recommendations)
4. **Deadline?** (days remaining determines what to cut)
5. **What's your Solana experience?** (first project vs. experienced — affects scaffolding depth)
6. **Which hackathon?** (Colosseum Frontier, Superteam, Solana Foundation, other)

### Step 2 — Pick the right primitives

Based on category, recommend which 2026 primitives to integrate:

| Category | Recommended primitives | Why |
|----------|----------------------|-----|
| **DeFi** | Token-2022, SDP Trading API, Blinks for distribution | Token extensions add compliance features; Blinks make swaps shareable |
| **Consumer / Social** | Blinks, ZK Compression, Agent Kit | Blinks for viral distribution on X; compression for mass user onboarding |
| **AI + Crypto** | Solana Agent Kit, Helius MCP, ZK Compression | Agent Kit for on-chain AI actions; compression for agent micropayments at scale |
| **Infrastructure / DevTool** | Solana Developer MCP, Helius MCP | MCP integration for AI-native developer tools |
| **Payments / Fintech** | SDP (Issuance + Payments), Token-2022 | Enterprise-grade payment orchestration with compliance |
| **Gaming** | ZK Compression, Token-2022 (transfer hooks) | Compressed game assets at scale; transfer hooks for royalties |
| **Physical World / DePIN** | SDP, ZK Compression, Blinks | Real-world payments + cheap on-chain state for IoT/sensors |

### Step 3 — Scaffold the project

Generate a full-stack project structure:

```
hackathon-project/
├── programs/
│   └── your-program/
│       ├── src/
│       │   └── lib.rs          # Anchor program
│       └── Cargo.toml
├── app/
│   ├── src/
│   │   ├── app/
│   │   │   ├── page.tsx        # Main page
│   │   │   └── layout.tsx      # Root layout with providers
│   │   ├── components/
│   │   │   └── WalletButton.tsx
│   │   └── lib/
│   │       ├── program.ts      # Program client (IDL-generated)
│   │       └── constants.ts    # Program ID, RPC config
│   ├── next.config.ts
│   └── package.json
├── tests/
│   └── program.test.ts         # Anchor test suite
├── Anchor.toml                 # Anchor config (devnet)
├── README.md                   # Submission README (see template below)
└── package.json
```

**Stack choices:**
- **On-chain:** Anchor (unless the founder is experienced with native Rust)
- **Frontend:** Next.js + App Router + Tailwind
- **Wallet:** `@solana/wallet-adapter` with Phantom, Solflare, Backpack
- **RPC:** Helius (free devnet tier, supports ZK Compression + DAS API)
- **Testing:** Anchor test framework + Bankrun for fast local tests

### Step 4 — Configure devnet deployment

```bash
# Install Anchor
cargo install --git https://github.com/coral-xyz/anchor anchor-cli

# Build + deploy to devnet
anchor build
anchor deploy --provider.cluster devnet

# Get devnet SOL
solana airdrop 2 --url devnet
```

### Step 5 — Build the submission package

**Colosseum Frontier submission requires:**
1. **3-minute pitch video** — use the `winning-pitch-deck` skill from this collection
2. **3-minute demo video** — screen recording of the product working on devnet
3. **README** with: problem, solution, how it works, tech stack, team
4. **Working deployment** — judges will try the product

**Submission README template:**

```markdown
# [Project Name]

> One-line description

## Problem
[What pain point does this solve? Include a stat if you have one.]

## Solution
[What does your product do? One paragraph.]

## How it works
[3-step user journey or architecture diagram]

## Tech stack
- On-chain: [Anchor / Native Rust] on Solana
- Frontend: [Next.js / React Native]
- Key integrations: [ZK Compression / Blinks / Agent Kit / SDP]

## Demo
[Link to deployed app on devnet]

## Team
[Names + one outstanding achievement]
```

### Step 6 — Time management (critical)

Scope based on days remaining:

| Days left | Scope |
|-----------|-------|
| **7+** | Full product — program + frontend + tests + pitch video + demo video |
| **3–6** | Core MVP — program + minimal frontend + demo video. Skip pitch polish. |
| **1–2** | Emergency mode — one working feature end-to-end. Record demo immediately. |

**What to cut first** (in order):
1. Extra features beyond core flow
2. Polished UI (functional > pretty for hackathons)
3. Comprehensive tests (keep one happy-path test)
4. Multi-wallet support (just Phantom is fine)

**What to never cut:**
1. Working demo on devnet
2. Demo video showing the product actually works
3. Clear README explaining the product

## Hard rules

1. **Deploy to devnet early and often.** Don't wait until the last day. Deploy on day 1, iterate in public.
2. **One feature done > three features half-done.** Judges evaluate completeness, not ambition.
3. **Record the demo video before the deadline, not at the deadline.** Recording always takes longer than expected.
4. **Use Anchor unless you have a specific reason not to.** Native Rust is faster at runtime but slower to build. Hackathons optimize for build speed.
5. **Free tiers are your friend.** Helius free tier, Vercel free tier, Supabase free tier. Don't spend the hackathon setting up infrastructure.

## Pairs with other skills in this collection

- **`winning-pitch-deck`** — Build the 3-minute pitch video using the DePitch framework
- **`solana-agent`** — If your project involves AI agents on Solana
- **`solana-blinks`** — If your project needs shareable transactions on X
- **`solana-compress`** — If your project creates many token accounts
- **`solana-sdp`** — If your project involves payments or tokenization
- **`ui-ux-pro-max`** — Design guidance for making the frontend look professional

## Reference links

- [Colosseum Frontier Hackathon](https://www.colosseum.org/frontier)
- [Solana Hackathon Hub](https://solana.com/hackathon)
- [Superteam Hackathons](https://superteam.fun/hackathon)
- [Anchor documentation](https://www.anchor-lang.com/)
- [Solana Cookbook](https://solanacookbook.com/)
- [Cyfrin Updraft Solana Course](https://updraft.cyfrin.io/) (free, 31 lessons)
- [Helius free tier](https://www.helius.dev/)
