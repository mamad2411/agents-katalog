# Skill Root Router
> Level 0: Always in context (~200 tokens)
> Routes to category routers on match

## Category Triggers

| Category | Trigger Keywords | Router File |
|---|---|---|
| Web Dev | frontend, backend, css, html, react, vue, angular, svelte | web-dev-router.md |
| DevOps | docker, k8s, kubernetes, terraform, ansible, ci-cd, helm, jenkins | devops-router.md |
| AI/ML | ai, ml, llm, gpt, neural, transformer, embedding, rag, langchain | ai-ml-router.md |
| Security | security, cve, vuln, pentest, crypto, auth, owasp, sanitize | security-router.md |
| Blockchain | blockchain, web3, solidity, eth, solana, defi, nft, smart-contract | blockchain-router.md |
| Database | sql, postgres, mysql, mongo, redis, database, migration, orm | database-router.md |
| Mobile | ios, android, flutter, react-native, mobile, swift, kotlin | mobile-router.md |
| Cloud | aws, gcp, azure, cloud, lambda, s3, ec2, serverless | cloud-router.md |
| Game Dev | game, unity, unreal, godot, bevy, pygame, canvas, webgl | game-dev-router.md |
| Creative | design, ui, ux, figma, animation, video, image, music | creative-router.md |
| Productivity | todo, task, calendar, email, automation, workflow | productivity-router.md |
| Reference | docs, guide, tutorial, reference, api, sdk, book | reference-router.md |
| MCP | mcp, server, tool, integration, smithery, proxy | mcp-router.md |
| Token Opt | token, cost, budget, compress, cache, save, optimize | token-opt-router.md |
| Resource | cpu, ram, memory, thermal, battery, resource, performance | resource-router.md |
| Skill Potency | quality, score, refinery, sweep, amplify, evaluate, heal | potency-router.md |

## Routing Rules
1. Match user intent to category by keyword
2. Load that category's router file (max 3 routers at once)
3. Router matches specific skill → load skill name+description
4. Invoke skill → load full skill body on-demand
5. Purge router after 5 turns of no match in that category
