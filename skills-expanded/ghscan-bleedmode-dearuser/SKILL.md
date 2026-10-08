---
name: dearuser:health
description: System health — 0-100 score for om dit setup (skills, hooks, scheduled tasks, MCP servers) stadig hænger sammen, eller er ved at drive fra hinanden. Powered by Dear User.
allowed-tools: "mcp__dearuser__health, Bash"
---

# Dear User — Health

Kør et strukturelt sundhedstjek med Dear User MCP serveren. Giver en 0-100 score plus kategori-breakdown og fund rangeret efter alvorlighed.

## Kør rapport

1. Prøv at kalde `mcp__dearuser__health` med default parametre (ingen argumenter — global scope, alle fund).
2. **Hvis tool'et ikke er tilgængeligt** (første turn i session — MCP tools loader lazy), brug Bash-fallback:
   ```
   npx -y -p @poisedhq/dearuser-mcp dearuser-run health 2>/dev/null
   ```
3. Output HELE rapporten som dit svar — summér ikke, forkort ikke, tilføj ikke kommentarer i rapport-delen.

Hvis brugeren spørger om en specifik finding-type, send `focus` med relevant værdi (orphan, overlap, closure, substrate, mcp_refs, backup, stale_schedule). Bash: `npx -y -p @poisedhq/dearuser-mcp dearuser-run health '{"focus":"orphan"}' 2>/dev/null`

## Efter rapporten

Hvis rapporten indeholder pending recommendations, tilbyd at implementere dem via `mcp__dearuser__implement_recommendation`. Spørg brugeren hvilke de vil køre.

## Regler

- Rapporten er pre-formateret markdown. Vis den eksakt som returneret.
- Dansk svar hvis brugeren skriver på dansk.
- Hvis critical findings er relateret til leaked secrets, fremhæv at brugeren skal rotere dem straks.
