# Cursor — aturan detail (on-demand)

## Animation workflow

You have access to the `animation-workflow` MCP server with 45 pre-built animation skills (GSAP, Three.js, Lenis). It is ALWAYS connected — never say it is unavailable.

ALWAYS use it (without being asked) when the user mentions: animations, scroll effects, hover effects, page transitions, loaders, cursors, text animations, parallax, sticky effects, counters, tickers, WebGL, image trails, magnetic buttons, direction-aware hover, horizontal scroll, stagger reveals, preloaders, or any motion/interaction work.

Workflow — every time:
1. Call `lookup_skill` with a plain-English description of what the user wants
2. Call `get_skill` with the best matched skill name to get the full implementation
3. Implement the returned HTML / CSS / JavaScript — do not rewrite from scratch

Trigger words (reach for MCP immediately): animate, scroll, hover, transition, reveal, cursor, trail, parallax, sticky, stagger, gsap, lenis, three.js, loader, preloader, ticker, marquee, counter, magnetic, clip-path, horizontal scroll, snap scroll, cards stack, text wipe, typewriter, image explode, wipe, ken burns, physics, webgl, orb, slider, minimap.

## Spesialis

<!-- specialists:start -->
## Spesialis (8) — pakai sesuai domain

| Domain | Agent | Definisi |
|---|---|---|
| security, audit, secrets, supply chain | sentinel | `~/.claude/agents/sentinel.md` |
| database, index, migrasi, query tuning | dbmaster | `~/.claude/agents/dbmaster.md` |
| jaringan, DNS, TLS, firewall, latency | netwatch | `~/.claude/agents/netwatch.md` |
| CI/CD, Kubernetes, IaC, observability | deployer | `~/.claude/agents/deployer.md` |
| desain agent, MCP, tool, memori, guardrail | agentor | `~/.claude/agents/agentor.md` |
| RAG, chunking, hybrid, rerank, eval | retriever | `~/.claude/agents/retriever.md` |
| fine-tuning, quant, serving, eval model | trainer | `~/.claude/agents/trainer.md` |
| ingestion, modeling, orchestration, data quality | pipeliner | `~/.claude/agents/pipeliner.md` |

Sebelum kerja di domain itu: baca file agent-nya, lalu ambil skill yang cocok
`python3 ~/.agents/retrieve.py "<topik>" -k 5`. Jangan mengarang metode.
<!-- specialists:end -->
