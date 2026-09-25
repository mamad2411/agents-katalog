# Repo Referensi: agentix-cloud/skills

Repo: https://github.com/agentix-cloud/skills
Ref lokal: /Users/chaali0324/.agents/repo-refs/agentix-cloud_skills
API: curl "localhost:27126/repos/readme?name=agentix-cloud_skills"
Dibuat: 2026-09-16

## Cuplikan README
# agentix-cloud/skills

Source: https://github.com/agentix-cloud/skills
Fetched: 2026-09-16

## README
# Agentix Skills

Agent skills for [Agentix](https://agentix.cloud) — an AI agent collaboration platform where a CEO agent manages ephemeral Claude Code workers.

## Skills

### `skills/agentix-ceo`

Orchestrate a team of AI workers from Claude Code. The CEO skill creates roles, assigns tasks, spawns workers on Modal, monitors progress, reviews code, and merges PRs — all autonomously.

- **Auth**: API key (auto-provisioned on first use)
- **Setup**: Install the skill, tell Claude your goal — registration is handled automatically
- **Entry point**: [`skills/agentix-ceo/SKILL.md`](skills/agentix-ceo/SKILL.md)

## Installation

```bash
npx skills add agentix-cloud/skills --yes
```

Then tell Claude: **"Use Agentix to build [your goal]"**

### Self-hosted

If you're running your own Agentix instance, set the API URL first:

```bash
export AGENTIX_API_URL=http://localhost:3456
npx skills add agentix-cloud/skills --yes
```

See the [self-hosted repo](https://github.com/agentix-cloud/agentix) for setup instructions.

## What it does

| Capability | How |
|-----------|-----|
| Create specialized roles | backend-engineer, code-reviewer, frontend-engineer, etc. |
| Define and prioritize tasks | Backlog → ready → in_progress → review → done |
| Spawn parallel workers | Up to 25 ephemeral Claude Code instances on Modal |
| Git automation | Workers branch, commit, push; reviewers open PRs and merge |
| Playbook system | Define operating policies the team follows autonomously |
| Continuous operation | CEO runs in a loop — monitoring, reacting, planning |

## Links

- [Managed service](https://agentix.cloud) — zero setup, multi-tenant, built-in billing
- [Self-hosted](https://github.com/agentix-cloud/agentix) — run your own instance
- [Documentation](https://agentix.cloud/docs/getting-started)

## License

MIT


