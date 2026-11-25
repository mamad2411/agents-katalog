---
name: swarm-migrate
description: Bring existing projects into the SwarmVault — register, mirror docs, optionally mine the repo into SDLC artifacts and resume the flow mid-phase (brownfield adoption). Use when the user wants existing projects migrated/connected to the vault, or an existing codebase placed into the SDLC flow.
---

# swarm-migrate — existing-project migration

Three tiers per project; each deeper tier is opt-in with its cost stated up front.
Idempotent: re-running repairs, never duplicates.

## 1. Discover

List candidates: `swarmvault.py register --import-claude` covers Claude Code users'
`~/.claude.json` in one shot; otherwise the user names paths. Ask WHICH projects to
migrate (multi-select) and, per project, the isolation flag.

## 2. Immediate tier (cheap, always)

Per chosen project: register + marker → first `sync` (mirrors existing
CLAUDE.md/AGENTS.md/README/docs and any existing memory; builds the MOC) → wire the
platforms they name with `setup`/`wire` (as swarm-init step 3; one command, no manual file
edits). The project is now queryable.

## 3. Digest tier (token-costing, opt-in)

State the rough cost first. Analyze the repo → `10 Projects/<P>/<P> Digest.md`
(architecture, conventions, entry points — not `generated`, so sync preserves it) + seed
memories for footguns found in code comments/READMEs/issue notes.

## 4. SDLC adoption tier (most token-costing, opt-in) — place it IN the flow

Mine first, ask second (swarm-spec's brownfield mode does the work):

1. Sources: README, docs/, existing plan/TODO files, issue exports, test suites, the code.
2. Produce `docs/SRS.md` + feature specs marked `status: mined-draft`, every statement
   with provenance (`file:line`).
3. Detect the de-facto phase — e.g. "14 of 20 mined features implemented, no design doc"
   — and write flow-state accordingly.
4. Gap interview via the question queue: only gaps, conflicts, low-confidence items.
   Never re-ask what the repo answers.
5. Remaining work → tickets. From here `/swarm-flow` resumes the project mid-phase like
   any SwarmVault project.

## Close

Ask once (if unset): vault as default for new projects? Show the security disclaimer
(swarm-init step 4) if this user hasn't seen it. Huge monorepo → scope the deep tiers to
user-chosen subpaths. A project containing its own Obsidian vault → exclude that folder
from doc mirroring (no vault-in-vault).

---
*Influences: Jeffallan's spec-miner & legacy-modernizer; the original Claude Vault
migration — see CREDITS.md.*
