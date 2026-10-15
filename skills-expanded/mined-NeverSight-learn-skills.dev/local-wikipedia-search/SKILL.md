---
name: local-wikipedia-search
description: Search and read Jared's publicly hosted text-only English Wikipedia Kiwix/ZIM mirror at wiki.ayrscott.com. Use when the user asks to look something up in our wiki install, needs encyclopedia/background facts, asks for Wikipedia/local wiki evidence, or when external web search is unnecessary.
---

# Local Wikipedia Search

Use this skill to search Jared's hosted English Wikipedia mirror, not the public internet or live Wikipedia.

## Mirror facts

- Public URL: `https://wiki.ayrscott.com/`
- Default script base URL: `https://wiki.ayrscott.com`
- Optional same-host/local base URL: `http://127.0.0.1:3081/`
- Service on the host: `kiwix-wikipedia.service`
- ZIM on the host: `/srv/kiwix/zim/wikipedia_en_all_nopic_2026-03.zim`
- Snapshot: English Wikipedia text-only/no-image ZIM, March 2026
- Content URL prefix: `/content/wikipedia_en_all_nopic_2026-03/`

The helper scripts default to the public URL so this skill works from other machines after installation. On the server itself, set `WIKI_BASE_URL=http://127.0.0.1:3081` or pass `--base-url http://127.0.0.1:3081` if you want to bypass public HTTPS.

Do not confuse this with project markdown wikis. This skill is for the Kiwix-hosted English Wikipedia mirror.

## Preferred workflow

1. Search the hosted mirror.
2. Read one or more likely article pages.
3. Answer from the mirrored articles and cite the article title plus `https://wiki.ayrscott.com/...` URL.
4. If the mirror has no good result, say that the mirror did not have a good hit instead of silently switching to live web search.

## Helper scripts

Run these from this skill directory, or resolve the relative paths against this skill directory.

Search full text through the public mirror:

```bash
python3 ./scripts/wiki-search.py "apollo program" --limit 10
```

Read an article as plain text through the public mirror:

```bash
python3 ./scripts/wiki-article.py "Apollo program" --max-chars 12000
```

Read by URL from a search result:

```bash
python3 ./scripts/wiki-article.py "https://wiki.ayrscott.com/content/wikipedia_en_all_nopic_2026-03/Apollo_program"
```

Use the local listener when running on `lunarian.cc`:

```bash
WIKI_BASE_URL=http://127.0.0.1:3081 python3 ./scripts/wiki-search.py "apollo program" --limit 10
python3 ./scripts/wiki-article.py "Apollo program" --base-url http://127.0.0.1:3081
```

Use the local ZIM index directly when running on the host with `kiwix-search` installed:

```bash
python3 ./scripts/wiki-search.py "apollo program" --zim /srv/kiwix/zim/wikipedia_en_all_nopic_2026-03.zim --limit 10
python3 ./scripts/wiki-search.py --suggest "Apollo" --zim /srv/kiwix/zim/wikipedia_en_all_nopic_2026-03.zim
```

Note: `--suggest` only gives true title suggestions with `--zim`; without `--zim`, the script uses the public Kiwix HTTP search page.

## Manual fallback

Search via public HTTP:

```bash
python3 - <<'PY'
from urllib.parse import urlencode
print('https://wiki.ayrscott.com/search?' + urlencode({'pattern': 'search terms'}))
PY
```

Fetch an article by converting the title to the Wikipedia path form: replace spaces with underscores and URL-encode special characters.

```bash
python3 - <<'PY'
from urllib.parse import quote
base = 'https://wiki.ayrscott.com/content/wikipedia_en_all_nopic_2026-03/'
title = 'Full moon'
print(base + quote(title.replace(' ', '_'), safe='()_,-.'))
PY
```

If you are on the host and the helper scripts or public URL fail, check the service:

```bash
systemctl is-active kiwix-wikipedia.service
curl -fsSI http://127.0.0.1:3081/
curl -fsSI https://wiki.ayrscott.com/
```

If the service is down and sudo is available:

```bash
sudo systemctl restart kiwix-wikipedia.service
```
