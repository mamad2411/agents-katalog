# CareerOps agent skill

Public-facing skill docs. Full mode prompts live in [`.agents/skills/careerops/`](../.agents/skills/careerops/).

```bash
npx @telivity/careerops init
```

Modes: `scan` · `evaluate` · `rank` · `tailor` · `interview` · `followup` · `outcome` · `advise`

Human-gated chains: `npx @telivity/careerops run-chain --list` — see [CHAINS.md](CHAINS.md). Extension hooks (not a browser extension): [PLUGINS.md](PLUGINS.md).

Doctrine: materials only — never invent experience; never auto-apply / auto-send. Bullet memory provenance + `resume_struct` canonical sync — see [DOCTRINE_MEMORY.md](DOCTRINE_MEMORY.md). Roadmap: [ROADMAP.md](ROADMAP.md).

**Board pack:** prefer `schema_version` **4+** (accomplishments, portfolio, durable outcomes, Sent metadata, interview events, stories). Optional additive `extensions` for plugins + chain runs. Export from the web app (Settings → Your data) — never includes API keys.
