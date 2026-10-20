---
name: team-scaffold
description: Stand up a new infiquetra agent-team repo end-to-end — context-library-compliant repo + Discord identity + GitHub identity + split-vault wiring + Ansible deploy harness — by composing a deterministic generator with two human-in-loop portal gates
when_to_use: |
  Use this skill when the user:
  - Wants to create a brand-new agent team (a new persona or crew in the Olympus grouping or the Asgard grouping)
  - Says "scaffold a team", "stand up team-X", "add a new team", "new agent team repo"
  - Needs to reproduce the polyrepo per-team layout (deploy harness, vault slice,
    profiles/, engineering journal) without repeating the manual migration dance
  - Wants to promote an existing host-level agent into its own team repo
  - Asks how new teams get their Discord bot / GitHub App / vault tokens wired
---

# team-scaffold

Automates "stand up a new team" end-to-end. The migration that created the first
12 teams (`infiquetra/team-*`) was a manual dance; this skill makes it
repeatable. It composes a **deterministic Python pipeline** (`team-scaffold` CLI,
in `scripts/`) with the **two irreducible human gates** that cannot be
API-automated.

> Native `hermes profile install` packaging is DEFERRED. The deploy artifact is
> the Ansible harness (`deploy/<team>.yml`) that installs reusable role code from
> `infiquetra.hermes_team` and takes inventory/shared secrets as explicit inputs.

## Mental model

| Layer | Owner | Tool |
|---|---|---|
| repo skeleton, harness, vault wiring, inventory, identity stub | **deterministic** | `team-scaffold` CLI (`scripts/`) |
| Discord **bot App create + token reveal** (gate G1) | **human** | Chrome-MCP, per `home-lab/Discord-Bot-Creation-Instructions.md` |
| GitHub **App create + install** (gate G2) | **human** | `home-lab/scripts/github_app_provision.py` |
| SOUL authoring, per-profile runtime config | **operator/creative** | edit `profiles/<n>/SOUL.md`, `deploy/team_profiles.yml` |

Everything deterministic is idempotent and **probes live state** (repo exists?
token vaulted? host in inventory?) — re-runnable and resumable across the gates.

## Setup

```bash
cd scripts && uv venv && uv pip install -e ".[dev]"
uv run team-scaffold --help
```

## The runbook (drive top to bottom)

Full detail in [references/runbook.md](references/runbook.md); spec schema in
[references/input-contract.md](references/input-contract.md). Summary:

0. **Author `team-spec.yaml`** (the one operator input) →
   `team-scaffold validate-spec team-spec.yaml`
1. **Create the repo:** `gh repo create infiquetra/team-<name> --private` (skip
   if it exists).
2. **Stamp the skeleton:** `team-scaffold stamp team-spec.yaml --out <clone>`
   (context-library-compliant repo + deploy harness + authored stubs).
3. **Author SOUL(s):** edit `profiles/<n>/SOUL.md` (placeholder → real persona),
   or pull the live SOUL for a promoted existing agent.
4. **Fill `deploy/team_profiles.yml`** (runtime config) →
   `team-scaffold validate-profiles deploy/team_profiles.yml`.
5. **— GATE G1 (human): Discord bot App + token reveal —** drive Chrome-MCP per
   `home-lab/Discord-Bot-Creation-Instructions.md`. Then encrypt the revealed
   token and splice it into the team vault:
   `ansible-vault encrypt_string --name vault_discord_bot_token_<persona> '<token>'`
   → append to `ansible/inventory/group_vars/all/vault.yml`. (For a promoted
   existing agent, instead: `team-scaffold vault-wire team-spec.yaml --source
   <home-lab all.yml> --out <clone>` to copy the block verbatim.)
6. **— GATE G2 (human): GitHub App create + install —**
   `python3 home-lab/scripts/github_app_provision.py --app <persona> --org infiquetra`.
   Record the App slug + token-var NAME in `identity/README.md` (names only,
   never the secret).
7. **Discord guild topology** (roles/channels) via the existing home-lab scripts
   (`set_bot_intents.py`, `discord_phase3.py`) if the team needs channels.
8. **Commit + push** the team repo.
9. **Register the host** (the ONLY home-lab write):
   `team-scaffold register-host team-spec.yaml` (dry-run) →
   `... --apply`, then commit home-lab's `hosts.yml` as a single revertible commit.
10. **Dry-run the deploy:** install collections, set
    `INFIQUETRA_SHARED_INFRA_VAULT`, then run `ansible-playbook -i
    <inventory-artifact> --limit <host> deploy/<team>.yml --check --diff
    --vault-password-file ~/.vault_pass.txt`.

## Guardrails

- **Secrets never touch the repo.** `identity/` holds token-var NAMES only;
  `vault.yml` holds only `!vault`-encrypted blocks (verbatim copies, same vault
  password). The `.gitignore` excludes `.env` / vault-pass files.
- **home-lab stays infra-only.** The single write-back is the `hosts.yml` host
  entry (step 9). Keep it last and as one commit so abort = `git checkout hosts.yml`.
- **Co-resident hosts** (e.g. mac mini = mimir + freya): the generated play's
  hard-gate (`assert filter | length > 0` derived from `profiles/`) keeps each
  team's deploy from touching its neighbor. Don't bypass it.
- **Orchestrator-crew teams** (`host_group: orchestrator_vms`) include the
  `hermes_orchestrator` role and the orchestrator profile carries NO
  `discord_token_var` (it posts as the conductor bot). The validators enforce this.

## Verify

```bash
cd scripts
uv run pytest -q                 # generator contract + validators + modules
uv run team-scaffold golden      # re-derive the 12 known teams vs frozen fixtures
```
The harness tests prove the generator emits collection install, explicit
inventory/shared-vault inputs, and no legacy roles-path dependency. Run them
after any change to `harness_gen.py` or the specs.
