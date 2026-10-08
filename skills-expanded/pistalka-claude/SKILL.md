# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

Projekt je slovenský — UI texty, komentáre aj dokumentácia sú po slovensky. Drž sa toho.

## Príkazy

```bash
npm run dev                     # vývojový server (Vite)
npm run build                   # tsc --noEmit && vite build → public/
npm run preview                 # náhľad produkčného buildu
npm test                        # Playwright, projekty desktop + mobil
npm run test:ui                 # Playwright UI mód
npm run icons                   # pregeneruje PNG ikony v static/icons zo scripts/*.svg
./deploy.sh                     # testy → build → commit public/ → push → nasadenie
```

Jeden test:

```bash
npx playwright test tests/whistle.spec.ts --project=desktop
npx playwright test tests/sound.spec.ts --project=desktop -g "trilkuje"
```

Linter ani formátovač nie sú nakonfigurované; typová kontrola beží len ako súčasť `npm run build`.

## Kritické: `public/` je výstup buildu a je commitnutý

Toto je obrátené oproti bežnému Vite projektu a ľahko sa na tom pomýli:

- `build.outDir: 'public'` + `emptyOutDir: true` — `public/` sa pri každom builde **zmaže a prepíše**. Nikdy tam nič needituj ručne.
- `publicDir: 'static'` — zdrojové statické assety (ikony) sú v `static/`, odtiaľ sa kopírujú do buildu.
- `public/` **nie je** v `.gitignore`, lebo server nasadzuje cez `git reset --hard origin/main` a nebuilduje sa tam. `deploy.sh` build commituje.

Zdrojové súbory (`index.html`, `main.ts`, `style.css`, `services/`, `controllers/`) sú v roote.

## Architektúra

`services/settings-store.ts` je **jediný zdroj pravdy**. Controllery čítajú a zapisujú localStorage priamo cez tento modul, žiadny stav v pamäti sa nezdieľa a controllery spolu nekomunikujú cez eventy. `normalizeSettings()` dopĺňa defaulty a oreže hodnoty na `LIMITS`, takže poškodený JSON alebo nedostupný localStorage (privátny režim) appku nezhodí.

`LIMITS` v settings-store a `min`/`max`/`step` na `<input type="range">` v `index.html` sú duplicita — pri zmene rozsahu treba upraviť obe miesta, inak posuvník dovolí hodnotu, ktorú store oreže.

`services/whistle-sound.ts` syntetizuje zvuk cez Web Audio API, žiadne audio súbory. Dôležitý invariant: `scheduleWhistle()` a všetky `build*()` funkcie berú `BaseAudioContext`, nie `AudioContext` — vďaka tomu ten istý kód beží v živom kontexte aj v `OfflineAudioContext`, na ktorom stoja zvukové testy. **Nový typ zvuku musí byť postaviteľný v `OfflineAudioContext`** (žiadne `MediaElement`, žiadny `AudioWorklet` bez modulu), inak sa nedá otestovať.

`AudioContext` sa vytvára lenivo — `main.ts` ho odomkne pri prvom `pointerdown`, prehliadače inak zvuk blokujú.

### Hlasitostná cesta

Každý hlas je normalizovaný na špičku ~1 (deliče v `build*` treba prepočítať, keď sa zmenia zisky zložiek) a v masteri sedí `DynamicsCompressor` nastavený ako **limiter** (prah -1 dB, ratio 20) — teda ako poistka proti klipovaniu, nie ako hlasitostná úprava. Nastavenie `boost` pridáva pred obálku `WaveShaper` s tanh krivkou; drive je zapečený v krivke, lebo WaveShaper si vstup mimo ⟨-1, 1⟩ oreže. Boost je zámerne vo `scheduleWhistle`, nie v masteri, aby sa dal odmerať v `OfflineAudioContext`. Poradie je dôležité: **tvarovač pred obálkou**, inak orezanie zrovná aj nábeh a dozvuk.

Stimulus controllery sú tenké: `whistle_controller` rieši počítadlo a slovenské skloňovanie (1 písknutie / 2–4 písknutia / inak pískaní), `settings_controller` formulár, ktorý ukladá okamžite pri každom `input`/`change` — appka nemá tlačidlo „Uložiť". Výnimka je posuvník **Boost**: ukladá sa až na `change` (pustenie), aby sa potvrdzovacie `confirm()` neotvorilo uprostred ťahania; počas ťahania `previewBoost()` mení len popis.

## Testy

Playwright beží **proti reálnemu produkčnému buildu** — `playwright.config.ts` si `npm run build && vite preview` spustí sám. Inak by sa nedal overiť service worker ani manifest. Testy sú v `tsconfig.json` vylúčené, takže `npm run build` ich netypuje; `tests/helpers.ts` si preto typ `WhistleSettings` duplikuje.

Dva pozorovacie body namiesto skutočného počúvania zvuku:

- `document` event `pistalka:whistle` (konštanta `WHISTLE_EVENT`) — vystrelí sa pri každom písknutí; `recordWhistles()` ho zachytáva cez `addInitScript` pred bootom appky.
- `window.pistalka.renderWhistleOffline()` — ladiace API vystavené v `main.ts`; `tests/sound.spec.ts` cez neho vyrenderuje buffer a analyzuje peak, RMS, prechody nulou a rozptyl obálky. Vďaka tomu test spadne aj vtedy, keď je píšťalka ticho alebo prestane trilkovať.

`seedStorage()` napĺňa localStorage tiež cez `addInitScript`, teda pred `connect()` controllerov.

## Nasadenie

`./deploy.sh` na `pistalka.vsetkosada.sk` (Apache, DocumentRoot `/var/www/pistalka/public`). Buildí sa lokálne, server si build len stiahne. Skript odmietne bežať mimo `main` alebo pri necommitnutých zdrojových zmenách, a pri zlyhaní ponúkne rollback servera na predchádzajúci commit. `--skip-tests` preskočí Playwright, `--setup` jednorazovo pripraví vhost a certifikát.

Apache vhost zámerne necachuje `sw.js`, `index.html`, `manifest.webmanifest` a `registerSW.js` — inak by sa nová verzia u ľudí neprejavila. Assety v `/assets/` majú hash v názve a cachujú sa navždy.

## Offline režim

Service worker generuje `vite-plugin-pwa` (režim generateSW), registruje ho `services/pwa-update.ts`. Ten okrem registrácie rieši aj **periodickú kontrolu novej verzie** — appka pridaná na plochu iPhonu sa nenačítava, iOS ju drží zamrznutú, takže bez toho by sa aktualizácia nikdy nestiahla. Podrobnosti vrátane iOS špecifík a manuálneho checklistu: `_docs/offline-pwa.md`.

## Poznámka k `_docs/plan.md`

Pôvodný plán, čiastočne neaktuálny — navrhoval Vitest + happy-dom, reálne sa testuje Playwrightom proti buildu. Ber ho ako kontext k zámerom, nie ako popis súčasného stavu.
