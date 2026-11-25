---
name: intuition-mission-cook
description: >
  Use when working on Intuition Box missions or bounties — selecting a mission
  from the board, writing a winning application comment, scoping and building the
  deliverable against the Intuition protocol (atoms, triples, signals, the SDK,
  GraphQL, the MultiVault contract), and preparing the submission for community
  review. Triggers on mentions of intuition.box, Intuition missions, 0xintuition
  bounties, or building on the Intuition knowledge graph.
---

# Intuition Mission Cook

A harness for going from "open mission on the board" to "paid, merged, reviewed."
Built for Claude Code. The output of a run is a real, open-source, community-useful
deliverable plus the docs and proof needed to pass review.

## The one thing to get right first

There are TWO layers and they are not the same thing. Keep them straight or the
build drifts.

- **Intuition Box** — the builder DAO/LLC running the missions program. Funds and
  coordinates contributors under a services agreement with the Intuition Foundation.
  This is who you apply to, who reviews, who pays. Reputation here is **iBOX**
  (governance, not equity). Missions share a ~$4,000/month pool with grants and bounties.
- **Intuition Protocol** — the actual tech you build against: a decentralized,
  semantic, token-curated knowledge graph. This is where atoms/triples/signal live.

Most missions are "build a tool / doc / template that helps other builders use the
**protocol**." So you need protocol fluency even though you apply through the **Box**.

## Missions are application-first

This is the part people get wrong. You do **not** just grab a mission and build. The
lifecycle is:

`Ideas → Backlog → Application Open → In Progress → In Review → Pending Payment → Paid`

You can only start building once you've **applied on the GitHub issue and been
selected**. Selection logic:

- no applicants → deadline extended, reward may rise
- one applicant → judged on qualifications + approach
- multiple applicants → best fit wins on experience, approach, timeline

So the application comment is its own deliverable with its own quality bar. Treat
winning the issue as Phase 1, not a formality.

Board: https://github.com/orgs/intuition-box/projects/21
Live list: https://intuition.box/missions
Process docs: https://intuition.box/docs/missions

## Protocol cheat sheet (verify live before building)

Knowledge graph primitives:

- **Atom** (a.k.a. *Identity* in the Portal) — the base unit. A globally unique,
  persistent decentralized identifier for anything: a person, concept, product, URL.
  Points to a URI, so it can represent on-chain or off-chain data. Has a **Vault**;
  TVL on the vault signals importance.
- **Triple** (a.k.a. *Claim*) — a semantic statement: **Subject – Predicate – Object**,
  where each of the three is itself an Atom. Has a **positive (FOR)** and **negative
  (AGAINST)** vault for attestations. Triples can be used as Atoms inside other Triples,
  so statements compose arbitrarily.
- **Signal** — expressing conviction by staking/depositing into an atom or triple vault.
  A non-zero position = "I attest to this, weighted by my balance." Zero = saying nothing.
  This is "who is attesting to what."

Onchain + dev surface:

- **MultiVault / EthMultiVault** — the core contract. Manages atom/triple creation,
  deposits, redemptions, share distribution. Blends ERC-4626 (vault shares) + ERC-1155,
  with a bonding-curve registry. This is the contract most onchain missions touch.
- **TRUST** — native ERC-20 utility token. Used for deposits, staking, governance, gas.
  Deployed on **Base**; it's the native gas token on the **Intuition Network L3**.
- **SDK** — TypeScript. Type-safe methods to create atoms/triples/signals and query
  the graph. Use it instead of hand-rolling contract calls where possible.
- **GraphQL API + indexing layer** — real-time queries over the graph at scale.
- **Apps** — Portal (flagship app, uses Identity/Claim language), Explorer.

Docs to pull at the start of every run (do not build from this cheat sheet alone —
it can go stale):

- https://www.docs.intuition.systems/docs (introduction, quickstart, primitives)
- https://tech.docs.intuition.systems (architecture, contracts, primitives, FAQ)
- **llms.txt** — Intuition publishes a concise LLM-readable doc index. Fetch it first;
  it's the fastest way to ground the build accurately.

## Workflow

Adapt depth to mission size — a docs mission skips the contract phases. Don't run all
seven phases on a two-hour task.

### Phase 0 — Recon and fit
1. Fetch the live board and `intuition.box/missions`. List open missions with status,
   reward, and closing date.
2. Fetch `llms.txt` + the relevant protocol docs for anything the missions touch.
3. Score each open mission on: reward vs effort, fit with what you've already shipped
   (ZK content, agents, onchain builds, SDK work), how reusable the result is, and
   whether you can credibly close it before the deadline.
4. Pick ONE. Smaller and finishable beats ambitious and abandoned — same lesson as the
   hackathon builds. A clean merged mission also banks iBOX/governance for the next one.

### Phase 1 — Win the issue
Write the application comment to post on the GitHub issue. This is an evaluation, so
keep it **professional and concrete** — this is not the place for the lowercase content
voice. Include:
- one line on why this mission matters to the broader builder community (their stated bar)
- relevant proof: links to shipped work that maps to this task
- a short, specific **approach outline** (the actual steps, not vibes)
- a realistic **timeline** with a buffer
- one thoughtful question or scoping clarification if the issue is ambiguous — signals you read it

Stop here and wait for selection. Don't pre-build a large deliverable before you're
assigned unless a tiny proof-of-approach strengthens the application.

### Phase 2 — Scope (only after selected)
Generate the planning docs in the repo:
- `CLAUDE.md` — mission summary, the exact success criteria from the issue, protocol
  surfaces in scope, links to the live docs, and the "definition of done" copied verbatim
  from the issue so review can't move the goalposts.
- `PHASE_0_CHECKLIST.md` — environment, SDK install, network/RPC config (Base + Intuition
  L3), test wallet, any contract addresses, repo + license (open source by default).
- `BUILD_GUIDE.md` — architecture and the build order.

### Phase 3 — Build
Produce a full **prompt-by-prompt Claude Code execution plan**, labeled by phase and
step, ready to paste straight into Claude Code. Use the standard session / phase / stuck
/ commit prompt rhythm. Rules that carry over from the hackathon playbook:
- **use the protocol for real.** Hit the actual SDK / GraphQL / MultiVault — create real
  atoms/triples, real signal, on a testnet or the live network as the mission requires.
  Mocked output reads as low-effort in community review.
- **close the loop.** If it's a tool, it should run end to end without you babysitting it.
- **commit the code yourself** so authorship is clean and there are no AI-attribution
  issues on a public, reviewed repo.

### Phase 4 — Make it reviewable
Review here is community code review + QA + docs verification, not a demo-day vibe check.
So the docs ARE the deliverable as much as the code:
- `README.md` — what it is, why the community benefits, install, usage, a worked example.
  Clear professional prose, not the content voice.
- inline comments where a reviewer would otherwise have to guess.
- a `PROOF` section or short Loom: tx hashes / explorer links / screenshots showing it
  actually touched the graph.
- confirm the open-source license is in place.

### Phase 5 — Submit + amplify
- Post the completion on the GitHub issue with links to the PR, the proof, and the README.
- Then, separately, write the **Spotlight / X post** in the content voice (see below) —
  this is where lowercase, grounded, lived-in tone belongs, not in the repo.

## Voice split — important

Do not blur these:
- **GitHub application + README + code comments** → normal professional writing. Sentence
  case, precise, evaluatable. The reviewers are judging competence.
- **Spotlight posts, X threads, announcements** → the content template: lowercase, no
  bolds/emojis/filler, short sentences, grounded and lived-in, audience assumed to know
  web3. Run the anti-AI-slop pass before posting. Never use "flip the…" or stacked
  negation.

## Recurring lessons baked in
- small and merged > ambitious and stalled
- the application is a deliverable, not a step
- real onchain action wins review; mocks lose it
- open source by default — it's a stated principle, not optional
- commit your own code on public repos
- every completed mission compounds into iBOX / governance weight, so finishing matters
  beyond the single reward

## Quick reference
- Board: https://github.com/orgs/intuition-box/projects/21
- Missions: https://intuition.box/missions · Process: https://intuition.box/docs/missions
- Grants (bigger scope): https://atlas.discourse.group/c/ecosystem-development/grant-applications/36
- Protocol docs: https://www.docs.intuition.systems/docs · https://tech.docs.intuition.systems
- Discord (ask in #builders-chat): https://discord.gg/0xintuition
- Portal: https://portal.intuition.systems · Explorer: https://explorer.intuition.systems
