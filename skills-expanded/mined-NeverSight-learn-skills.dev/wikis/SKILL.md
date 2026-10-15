---
name: wikis
description: "Query 250K+ Fandom, Miraheze, wiki.gg wikis. Search pages, infobox, images, Markdown. Live fallback for unsynced wikis via Cloudflare Worker."
---

# Wikis Skill

HTTP API skill for game/IP and community wikis (Fandom, Miraheze, wiki.gg, and live fallbacks). Prefer this when you need structured wiki data (search, page markdown, infobox, images) without HTML scraping.

**Base URL:** `https://fff-wiki.neta.art`

Coverage: **253,142+ wikis** (full Fandom + Miraheze + wiki.gg), with live fallback.

## Install this skill

```bash
npx skills add https://github.com/markbang/wikis-skill \
  --skill "wikis" \
  --agent codex \
  --yes \
  --copy
```

Config Space tip: install into your `name=config` Space and **Save** so it publishes to `/configs/user/.agents/skills/wikis`.

## Endpoints

```bash
# List wikis
GET /wikis?page=0&size=20

# Search
GET /wikis/{wiki}/search?q={query}&page=0&size=20

# Pages
GET /wikis/{wiki}/pages/{title}?format=summary    # summary (fastest)
GET /wikis/{wiki}/pages/{title}?format=md         # Markdown
GET /wikis/{wiki}/pages/{title}?format=text       # plain text
GET /wikis/{wiki}/pages?category={cat}&page=0&size=20

# Structured
GET /wikis/{wiki}/infobox/{title}
GET /wikis/{wiki}/images/{title}?page=0&size=20

# Image proxy (anti-bot bypass, ~24h cache)
GET https://fandom-crawl.atou.workers.dev/proxy/image?url={image_url}

# Meta
GET /wikis/{wiki}/categories?page=0&size=20
GET /wikis/{wiki}/stats
```

`{wiki}` is the wiki id/slug (e.g. `genshin-impact`, `dontstarve`, `minecraft`).  
`{title}` should be URL-encoded (spaces → `%20`).

## Examples

```bash
# Search
curl -sS "https://fff-wiki.neta.art/wikis/genshin-impact/search?q=Hu%20Tao"

# Markdown page
curl -sS "https://fff-wiki.neta.art/wikis/dontstarve/pages/Wilson?format=md"

# Infobox
curl -sS "https://fff-wiki.neta.art/wikis/elden-ring/infobox/Malenia,%20Blade%20of%20Miquella"
curl -sS "https://fff-wiki.neta.art/wikis/pokemon/infobox/Pikachu"
curl -sS "https://fff-wiki.neta.art/wikis/naruto/infobox/Naruto%20Uzumaki"

# Category listing (default page=0&size=20)
curl -sS "https://fff-wiki.neta.art/wikis/minecraft/pages?category=Blocks&page=0&size=20"
curl -sS "https://fff-wiki.neta.art/wikis/dontstarve/categories"

# Image proxy
curl -sS "https://fandom-crawl.atou.workers.dev/proxy/image?url=https://terraria.wiki.gg/images/thumb/9/96/Brain_of_Cthulhu.png/800px-Brain_of_Cthulhu.png"
```

## Agent guidance

1. Prefer `format=summary` first; upgrade to `md` / `infobox` when needed.
2. URL-encode titles and queries.
3. For knowledge Spaces: write API JSON/md into `raw/wikis/...`, then distill into `wiki/` pages (do not treat curl output as the only memory).
4. Image hotlinking may fail — use the image proxy when fetching media.
5. This skill is **HTTP API** based. Optional local MediaWiki CLI: [fandom-cli](https://github.com/kjx-talesofai/claude-skill-fandom-cli).

## Related

- Repo: https://github.com/markbang/wikis-skill
- Awesome Cohub: https://github.com/markbang/awesome-cohub
- Alternative CLI skill: https://github.com/kjx-talesofai/claude-skill-fandom-cli
