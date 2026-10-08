# Skill

The public MoneyClaw OpenClaw skill is published in this repository so it can be inspected directly.

## Install

```bash
clawhub install moneyclaw
```

## Primary Environment Variable

```text
MONEYCLAW_API_KEY
```

The published skill also declares this through `metadata.openclaw.primaryEnv` and `metadata.openclaw.requires.env` so OpenClaw can surface the credential requirement correctly.

## Read The Skill Files

- [moneyclaw-skill/SKILL.md](https://github.com/elvismusli/moneyclaw/blob/main/moneyclaw-skill/SKILL.md)
- [moneyclaw-skill/agents/openai.yaml](https://github.com/elvismusli/moneyclaw/blob/main/moneyclaw-skill/agents/openai.yaml)
- [moneyclaw-skill/references/payment-safety.md](https://github.com/elvismusli/moneyclaw/blob/main/moneyclaw-skill/references/payment-safety.md)

## Scope Note

This is the public skill layer only.

Internal operator notes, infra details, and private operational context are intentionally not part of this repo.
