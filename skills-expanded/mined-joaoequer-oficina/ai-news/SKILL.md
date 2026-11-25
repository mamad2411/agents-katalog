---
name: ai-news
description: Daily AI news briefing in PT-BR from AlphaSignal and Hermes AI (new items only, deduplicated), with optional 30-60s Shorts/Reels scripts built from the strongest stories. Use for "notícias de IA", "o que saiu de novo em IA", "news de hoje", "resumo de IA", "ideias de shorts/roteiros a partir das notícias", "pauta para o canal".
---

# AI news

Collect the new AI stories, explain them in plain PT-BR, and (on request) turn the best ones into short-video scripts. The fetcher does the scraping; the model only reads, ranks and writes.

## Sources

| Source | How | Notes |
|---|---|---|
| Hermes AI (`hermes-ai.net/news`) | HTML list, server-rendered | aggregator: brings one-line summary + the original publisher (Exa, vLLM, Artificial Analysis...) |
| AlphaSignal (`alphasignal.ai/news-sitemap.xml`) | Google News sitemap | upstream newsroom, last ~48h, title + date only |

Both `robots.txt` allow crawling (Hermes asks crawl-delay 1, the script respects it). Neither has RSS. Stories are publisher claims: benchmarks and prices are "segundo X", never stated as fact.

## Output location

`~/.oficina/news/` (override with `OFICINA_NEWS_DIR`). Never inside a repo: this skill ships in a public repo and the briefings are personal.

- `seen.json` – URLs already delivered (the next run brings only new ones)
- `YYYY-MM-DD.md` – the briefing
- `YYYY-MM-DD-shorts.md` – scripts, when asked

## Step 1: fetch

```bash
python <skill-dir>/scripts/fetch_news.py --days 2 --pages 2 > <scratch>/news.json
```

Flags: `--days N` window, `--pages N` Hermes pages (20 items each), `--all` ignore `seen.json` (re-run the same day). Read only `count`, `errors` and the items; do not dump the JSON into the reply. `count: 0` means nothing new: say so and stop.

## Step 2: read before writing

For each story kept (max 10), open the article page only when the summary is empty or the story is a ranking candidate. Prefer the original publisher link when the page has one. Do not invent numbers absent from the page.

Rank by what matters to a dev who uses AI daily: new model or price change > tool/API a dev can use today > research with practical effect > funding/corporate.

## Step 3: briefing (`YYYY-MM-DD.md`)

```markdown
# IA hoje – DD/MM/AAAA

## Destaques
### <título em PT-BR, sem clickbait>
**O que é:** 1-2 frases.
**Por que importa:** 1 frase concreta (custo, o que destrava, quem afeta).
**Fonte:** [Publicador](url) · data

## Rápidas
- <uma linha por notícia restante> – [fonte](url)
```

3-5 destaques, the rest in Rápidas. Plain PT-BR, technical terms kept in English when that is how devs say them (benchmark, open-weights, token). After writing, reply with the path and the destaque titles only.

## Step 4: shorts (only when asked)

Pick the 3 stories with the clearest "so what" for a general tech audience. If the `yt-script` / `yt-shorts` skills are installed, follow their hook and retention rules; otherwise use this format per story:

```markdown
## Short N – <título>
**Gancho (0-3s):** frase que para o scroll, com o fato mais surpreendente.
**Contexto (3-15s):** o que aconteceu, em linguagem de gente.
**Virada (15-40s):** o número ou consequência que muda algo para quem assiste.
**Fecho (40-55s):** opinião curta ou pergunta para comentário.
**Na tela:** 3-4 textos de apoio / b-roll sugerido.
**Fonte (descrição):** url
```

Rules: 110-150 words of narration per short (≈45-55s), one idea per short, no "neste vídeo", no invented quotes, say "segundo <fonte>" for claims. Do not reuse the source's wording or images: write original narration and credit the link in the description.

## Adding a source

Add a generator to `scripts/fetch_news.py` yielding `{url, title, date, source, summary}` and register it in the loop in `main()`. Check the site's `robots.txt` first and prefer a sitemap or feed over HTML.
