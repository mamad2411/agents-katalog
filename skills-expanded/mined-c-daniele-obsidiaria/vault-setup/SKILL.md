---
name: vault-setup
description: Customization wizard for this AI-augmented Obsidian vault template. Use when the user runs /setup, asks to "customize the vault", "make this mine", set their name/role/language/domain, or onboard to the template for the first time. Interviews the user, writes setup/profile.yml, applies it with setup/apply-profile.mjs, tailors the domain-specific sections, and re-syncs the agent config.
---

# Vault Setup Wizard

This vault ships pre-filled with an **example profile**: *Daniel Lacemore*, a *management consultant*, working in *English* on *data platform and generative-AI delivery*. Your job is to turn that example into the real user's vault with as little friction as possible.

You customize the vault in **two layers**:

1. **Scalar values** — name, role, language, domain one-liner, vocabulary, vault path. These are replaced deterministically by `setup/apply-profile.mjs` from `setup/profile.yml`.
2. **Contextual sections** — the parts that need judgement, not find-and-replace. Today that means **Archie's "Domains of expertise"** section, which must reflect what the user actually delivers.

## The profile variables

`setup/profile.yml` holds these keys (see `setup/profile.defaults.yml` for the shipped defaults):

| Key | Meaning | Default |
|---|---|---|
| `principal_name` | Full name; also used in `owner:` fields | `Daniel Lacemore` |
| `principal_short_name` | How the agents address the user (usually the first name) | `Daniel` |
| `principal_role` | Role / title | `management consultant` |
| `principal_org_type` | Kind of organization, **no real company name** | `a professional services firm` |
| `primary_language` | Working language for notes, replies, deliverables | `English` |
| `domain_summary` | One line: what the user delivers | `data platform and generative-AI delivery` |
| `project_code_label` | How the user labels a project identifier code | `WBS` |
| `vault_abs_path` | Absolute path to the vault on disk (markitdown example) | `/path/to/your/vault` |

## Procedure

1. **Read the current profile** `setup/profile.yml` so you can pre-fill the questions with the present values (defaults on a fresh clone).
2. **Interview the user** with the `question` tool. Group the questions; for each, offer the current value as the recommended option so the user can accept quickly. At minimum ask: name + short name, role, organization type, working language, one-line domain, project-code label, and the absolute vault path. If the user wants to keep the defaults for a field, leave it unchanged.
   - Do **not** collect a real company name into `principal_org_type`; keep it generic (e.g. "a consulting firm", "a SaaS company", "an internal IT department").
   - Reassure the user that values must not contain double quotes (they end up in `opencode.json`).
3. **Write the answers** into `setup/profile.yml` (keep the file's comments; only change the values). One scalar per key.
4. **Apply deterministically**: run

   ```bash
   node setup/apply-profile.mjs
   ```

   It replaces the previous values across `AGENTS.md`, `00_System/System Guide.md`, the agent prompts, the commands, the templates and `opencode.json`, then snapshots the new state to `setup/.profile.prev.yml`. Use `--dry-run` first if you want to preview.
5. **Tailor the contextual sections** that find-and-replace cannot handle well:
   - Open `.opencode/.prompts/archie.md` and rewrite the section marked `## Domains of expertise` (it carries a `<!-- CUSTOMIZE -->` comment) so it reflects the user's real delivery domains. If the user is **not** in Data & AI, replace the data/GenAI stack with their actual areas (e.g. for a product manager: discovery, roadmapping, PRDs, experimentation, GTM; for a lawyer: contract types, jurisdictions, clause libraries). Keep the same shape: a few labelled groups, concrete and specific.
   - If the user's work has no client-facing "deliverables", note that they can simply ignore that folder, or ask Melio to prune it later — do not delete anything during setup.
6. **Re-sync the per-tool agent config** so Claude Code and Kilo match the new prompts:

   ```bash
   node 00_System/AI/sync-agents.mjs
   ```
7. **Report and remind**: summarize what changed, and tell the user to **restart the AI tool** (opencode/Claude/Kilo) so the updated agents and commands load. Point them at `README.md` for the daily workflow (`/obs.morning`, `/obs.inbox`, `/obs.eod`, `/obs.weekly`).

## Re-running

The wizard is idempotent and re-runnable. On each run the script diffs the previous snapshot (`setup/.profile.prev.yml`) against the new `profile.yml`, so changing one field later only rewrites that field. To start over from the shipped example: `node setup/apply-profile.mjs --defaults`.

## What you must NOT do

- Don't invent real client names, projects or numbers — this is configuration, not content.
- Don't add folders, properties or note types. Keep the system light (see `AGENTS.md`).
- Don't touch the user's actual notes (the numbered content folders); setup only edits the config layer plus Archie's domain block.
