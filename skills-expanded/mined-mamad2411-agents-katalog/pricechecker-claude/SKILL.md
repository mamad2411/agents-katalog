# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Język

Użytkownik jest Polakiem. Komunikacja, komentarze w kodzie, komunikaty commitów, README i UI dashboardu — po polsku. Komunikaty logów w `tracker.py` celowo bez polskich znaków (ASCII), bo trafiają do logów Actions.

## Czym jest ten projekt

Tracker najniższych cen produktów rowerowych w Europie kontynentalnej. Działa jako GitHub Actions (cron `23 10 * * *` UTC = 12:23 CEST; nieokrągła minuta celowo — crony `:00` bywają pomijane przez GitHub). Drugi workflow `watchdog.yml` (14:23 UTC) odpala Light FIRE, jeśli danego dnia nie było udanego runa (crony bywają gubione, a joby ubijane przez brak runnerów — „not acquired by Runner"). Bot commituje wyniki do repo. Nie ma serwera — dashboard to statyczny HTML z osadzonymi danymi, gadający z GitHub API tokenem z localStorage przeglądarki.

## Komendy

System Python jest externally-managed (PEP 668) — używaj venv:

```bash
python3 -m venv /tmp/pt-venv && /tmp/pt-venv/bin/pip install -r requirements.txt
```

Nie ma test suite. Weryfikacja zmian:

```bash
# 1. kompilacja
/tmp/pt-venv/bin/python -m py_compile tracker.py dashboard.py

# 2. składnia JS z szablonu dashboardu (największy blok <script>)
/tmp/pt-venv/bin/python -c "
import re, pathlib
tpl = pathlib.Path('dashboard.py').read_text()
js = max(re.findall(r'<script>\n(.*?)</script>', tpl, re.S), key=len)
pathlib.Path('/tmp/dash.js').write_text(js)" && node --check /tmp/dash.js

# 3. lokalna regeneracja dashboardu (output/dashboard.html + docs/index.html)
/tmp/pt-venv/bin/python -c "
import csv, yaml
from datetime import date
from dashboard import build_dashboard
cfg = yaml.safe_load(open('products.yaml'))
rows = list(csv.DictReader(open('data/history.csv')))
print(build_dashboard(rows, cfg['products'], cfg.get('settings') or {}, date.today().isoformat()))"
```

Pełny run lokalny: `python tracker.py` (bez kluczy w env pomija discovery i sprawdza tylko znane URL-e — bezpieczne). Klucze: `SERPAPI_KEY`, opcjonalnie `TAVILY_API_KEY`, `BRAVE_API_KEY`. `SKIP_DISCOVERY=1` wymusza tryb Light FIRE (zero zapytań do wyszukiwarek).

`gh` CLI nie jest zainstalowane. Do GitHub API używaj tokenu z git credential helper:

```bash
creds=$(printf "protocol=https\nhost=github.com\n" | git credential fill)
TOKEN=$(echo "$creds" | sed -n 's/^password=//p')
```

## Git

Bot Actions commituje `data/ output/ docs/` po każdym runie — przed pushem zawsze `git pull --rebase`. Wzorzec pracy: zmiana → testy jak wyżej → commit + push → użytkownik testuje przez FIRE/Light FIRE z dashboardu. Ręczny FIRE tego samego dnia **zastępuje** dzisiejsze wiersze w obu CSV (dedup po dacie w `append_history`).

## Architektura

Dwa pliki Pythona, reszta to dane:

**`tracker.py`** — cały pipeline w `main()`:
1. **Discovery** (`run_discovery`) — SerpAPI google + google_shopping per kraj z `settings.serpapi_countries`; Serper.dev z szerszej listy `settings.discovery_countries` (osobna pula zapytań); opcjonalnie Tavily/Brave. Dopisuje URL-e do `data/sources.json`. Zasięg = cała Europa kontynentalna (`EU_TLDS`, `ALLOWED_CURRENCIES` z CZK/HUF/RON itd.) — użytkownik sam weryfikuje wysyłkę do PL. Tryb `weekly`: przy `GITHUB_EVENT_NAME=schedule` tylko w poniedziałki; ręczny dispatch zawsze pełne discovery, chyba że `SKIP_DISCOVERY=1`. Shopping odpytywany tylko pierwszą frazą i bez cudzysłowów.
2. **Monitoring** (`fetch_offers`) — pobiera każdy URL, ekstrakcja ceny z JSON-LD schema.org → fallback meta OpenGraph → `__NEXT_DATA__`. Blokada botów (403/429/503 albo HTTP 200 z interstitialem rozpoznanym przez `_is_challenge`) → fallback headless Chromium (Playwright, leniwy start). Gdy strona bez ceny: auto-crawl 1 poziom (szuka linku do karty produktu po tokenach nazwy). Kolejność filtrów per URL: EAN (miękki, `ean_strict` twardy) → `require_tokens` (URL + `<title>` + ident oferty; `"a|b"` = alternatywa) → wariant (ident oferty, przy cenie zbiorczej także URL/tytuł z granicami słowa; `variant_strict` twardy) → dostępność → waluta/region → widełki `min_pln`/`max_pln`. Po pętli `drop_outliers`: przy ≥3 ofertach odpada cena < 25% mediany.
3. **Blind spoty** (`fill_blind_spots`) — domeny, które odrzuciły pobranie (i requests, i przeglądarkę; np. bike24 = Akamai, r2-bike = Cloudflare), dostają cenę z Google: najpierw feed Google Shopping — dostawcy w kolejności Serper.dev (`SERPER_API_KEY`; 2500 darmowych zapytań) → SerpAPI (chroniony `settings.serpapi_reserve`, domyślnie 10), wspólny budżet `settings.shopping_budget` zapytań/run, kraj feedu wg TLD sklepu (`bikero.cz` → `gl=cz`, dowolny kraj Europy; TLD neutralne → pierwszy z `serpapi_countries`), max `shopping_gl_cap` krajów/produkt (domyślnie 3). Celem feedu jest **każdy znany sklep produktu bez ceny w danym runie** (nie tylko blokujący). Plan pobrań per kraj: fraza 1 str. 1 → przy pełnej stronie i brakach str. 2 → przy dalszych brakach fraza 2 (max 3 pobrania); frazy Shopping = dwie pierwsze z `queries` (tekstowe, celowo nie EAN — EAN zwęża feed) — potem indeks Googlebota przez Programmable Search (`GOOGLE_API_KEY`+`GOOGLE_CX`, `settings.cse_budget`/run, domyślnie 15). **Warstwa CSE działa wyłącznie na starych projektach Google Cloud** — Custom Search JSON API jest zamknięte dla nowych klientów (błąd „This project does not have the access…"; starzy klienci do 2027-01-01), więc w praktyce ceny blind spotów łata Shopping przez Serpera. Przy budżecie mniejszym niż liczba produktów z blind spotami start listy rotuje po dniu. Bing Search API nie istnieje (wyłączone 2025-08-11), Brave nie zwraca cen (tylko discovery, od 02.2026 bez darmowego planu). Filtry jakości na tytule oferty (`_title_ok`: tokeny produktu + `require_tokens` + wariant). Takie oferty mają `via=shopping|google` w `all_offers.csv` i znacznik „Google" w audycie dashboardu. Nierozwiązane blind spoty (sklep blokuje + Google bez ceny) lądują w `data/blind_spots.json` (nadpisywany co run) — Diagnostyka pokazuje je w panelu „Blind spoty" jako listę domen do ręcznego dopisania do wyszukiwarki PSE.
4. **FX** — NBP tabela A, fallback frankfurter.app; wszystko przeliczane na PLN.
5. **Zapis** — `data/history.csv` (najniższa cena/produkt/dzień), `data/all_offers.csv` (pełny audyt), Excel `output/prices.xlsx`, log `data/last_run.log` (osadzany w dashboardzie).

**`dashboard.py`** — jeden wielki raw-string `TEMPLATE` (HTML+CSS+JS SPA, Chart.js + js-yaml z CDN). `build_dashboard()` wstrzykuje JSON payload (historia + audyt z ostatnich 120 dni + log + quota SerpAPI) i zapisuje **dwie kopie**: `output/dashboard.html` i `docs/index.html` (GitHub Pages z `/docs`). SPA ma zakładki: Główna (karuzela) / Produkty (tabela → klik = szczegóły) / Diagnostyka (log z filtrami) / Konfiguracja. Konfiguracja edytuje `products.yaml` **przez GitHub API** (PUT contents; komentarze YAML giną przy zapisie). FIRE/Light FIRE = workflow dispatch z inputem `discovery: full|skip`.

**Kluczowy inwariant:** `id` produktu z `products.yaml` jest kluczem wszędzie — `product_id` w obu CSV, klucz w `sources.json`, arkusz Excela, zakładka dashboardu. Zmiana `id` urywa ciągłość historii; duplikat `id` scala bazy URL-i i miesza oferty (tracker pomija duplikat z błędem, dashboard blokuje zapis).

**Baza źródeł (`data/sources.json`) jest tylko dopisywana** — to główne aktywo projektu. Sklep niedostępny danego dnia zostaje w bazie. URL-e normalizowane (`normalize_url` usuwa `srsltid`, `utm_*` itd.). Agregatory cen (ceneo, idealo, geizhals…) i marketplace'y (eBay, Amazon) blokowane globalnie w `BLOCKED_DOMAINS` z dopasowaniem subdomen.

## Limity API (SerpAPI, Serper)

SerpAPI Free: 250 zapytań/mies. Pełny FIRE przy ~10 produktach ≈ 90 zapytań (frazy × kraje × silniki + Shopping). Timeout SerpAPI i tak zużywa zapytanie (stąd `SERPAPI_TIMEOUT=60`). Do testów zmian w monitoringu/dashboardzie używaj Light FIRE — nie zużywa limitu. Stan limitu: `data/serpapi_quota.json` (endpoint `/account`); fallback Shopping dla blind spotów czyta ten plik i pomija silnik SerpAPI, gdy `left − serpapi_reserve ≤ 0`.

Serper: brak endpointu stanu konta — tracker sam zlicza udane zapytania (`_serper_used`) i kumuluje w `data/serper_quota.json` (`save_serper_quota`); pula w `settings.serper_credits` (domyślnie 2500). Po dokupieniu kredytów: zaktualizuj `serper_credits` i usuń `data/serper_quota.json` (albo wyedytuj `used`). Oba stany widać na głównej stronie dashboardu (`quotaWidget`).
