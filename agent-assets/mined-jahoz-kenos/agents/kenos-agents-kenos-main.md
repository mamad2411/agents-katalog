# AI Execution Contract — kenos

## Context
- Global rules: `~/.agents/AGENTS.md` (réponses FR, code/commits EN, Conventional Commits)
- Project context: `CLAUDE.md`, `README.md` + `pack_codebase` via MCP
- Portfolio governance: `../portfolio-os/` — design registry + milestone log

## Mandatory Behavior
- Start with: objective, scope, DoD, stop condition
- Design Readiness Gate before UI/UX
- Refuse scope creep → Roadmap+
- Deliver small and complete
- Never import design from other projects

## Project-Specific Rules
- **Single-read atomicity is sacred**: the client must never read `echoes`
  directly — map via `echoes_map` view, consumption via `consume_echo` RPC
  only. Any schema change must preserve `FOR UPDATE SKIP LOCKED`.
- **`encrypted_text` never leaks client-side** before atomic consumption.
- **Sealed echoes carry no text locally** — even the author cannot re-read.
- **ROSE color is reserved for destruction** (UI + SQL validation).
- **Audio never blocks the UI**: fire-and-forget bells, pitch coupling is
  best-effort, every plugin call wrapped in try/catch.
- **Sensor-less platforms must stay alive**: accelerometer fallback
  (sinusoidal drift) is a feature, not a workaround.
- **Sky vocabulary is law** (full lexique in CLAUDE.md): a *vestige* is
  a permanent plaintext culture shard (quote/etymology/fact, no account
  identity, never purged); an *artifact* is a curated public-domain poem
  ring (credited poet, readable by all, one 30-day moon, reborn weekly
  from the backlog). Never blur the two — never call a vestige "an
  artefact".
- Demo mode (no Supabase credentials) must keep exact backend semantics.
- **UI voice (V3.52 law)**: French is **canonical** — everywhere, for
  everyone. The WEB build serves English to the first journey only
  (Seuil, two gates, Mirror, revelation, artifact reading —
  `KenosVoice.pick(fr, en)` at each call site) when the traveller's
  platform speaks English; native and everything else stay French.
  **User content is NEVER translated** — the voice dresses the doors,
  never the confidences. Code, comments, commits in **English**.

<!-- portfolio-os:contrats:begin — bloc genere par sync-repomix-configs.sh, ne pas editer -->
## Contrats du portefeuille (charges par toute session agent)

- **Contrat projet** : `.repomix/instructions.md` — stack, UI, interdits, ports, frontiere design. Source de verite : les tables de `projects/portfolio-os/scripts/sync-repomix-configs.sh`.
- **Contexte code en masse** (audit, reprise) : `pack_codebase` via le MCP repomix — jamais de pack commite.
- Langue du code et des commentaires : francais.
<!-- portfolio-os:contrats:end -->
