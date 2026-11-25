---
name: model-council
description: Consult independent model lineages through existing CLI subscriptions and Agent Office for valuable uncertainty, ML hypotheses, architecture disputes or brainstorming. Prefer two relevant subscription/local consultants; paid OpenRouter consultants need explicit incremental benefit and a bounded budget. JEV can advise whether consultation is useful. Historical API panels keep their pinned protocol.
---

# Model Council

## Domyslnie: konsultacja w zespole

Dla NOWEJ pracy obowiazuje [references/team-consultation.md](references/team-consultation.md).
Najpierw dostepne subskrypcje przez Agent CLI/Fleet, rozne rodowody, niezalezne
hipotezy, potem celowana dyskusja w Office i test rozstrzygajacy w tym samym TODO.
Zwykla mala praca pomija rade. JEV moze tanio doradzic sklad i sens konsultacji;
sam nie uruchamia modeli. Dodatkowe API ma domyslny budzet zero. Nie plac drugi
raz za model dostepny przez abonament.

Architekt na wezwanie rozstrzyga trudna niepewnosc techniczna, a nie kazdy maly
szczegol. Preferuj dostepny profil Mythos, potem najlepszy kwalifikowany Opus
wedlug jawnych aktualnych danych Fleet/Model Radar. Nie zgaduj klasy z nazwy.
Logika biznesowa, flow procesu, wymagane pola, dostep i strategia pozostaja
decyzjami Mateusza. Znany odtworzony blad przywracajacy zatwierdzone zachowanie
naprawia zespol. JEV w trybie cieniowym nie zmienia tej granicy ani twardych zgod.

Ponizsze komendy opisuja zachowany historyczny transport platnego panelu.
Nie sa domyslna sciezka nowej konsultacji. Wymagaja najpierw konkretnego
uzasadnienia, skladu i jawnego budzetu zgodnie z nowa polityka.

## Historyczny transport OpenRouter

Skill uruchamia niezalezne recenzje przez OpenRouter, zapisuje dowody i zostawia synteze agentowi prowadzacemu. Nie traktuj nazw modeli zapisanych w dokumentacji jako stalej konfiguracji. Zrodlem wykonawczym jest `references/roster-policy.json` rozwiazywane przez `scripts/resolve_roster.py` na podstawie aktualnego katalogu.

## Uwierzytelnianie publicznej wersji

Przenosny skrypt czyta klucz wylacznie ze zmiennej `OPENROUTER_API_KEY`
w srodowisku biezacego procesu, takze dla `-ResolveOnly`. Brak, pusty lub
bialy klucz zatrzymuje przebieg przed wywolaniem uslugi. Nie uzywa prywatnego
magazynu hosta ani rezerwowej konfiguracji. To zmiana zgodnosci: dawne prywatne
uwierzytelnianie nie jest rownowazne i nie zostalo przeniesione. Nie wypisuj
wartosci klucza. Wersje sprawdzono w PowerShell 7; PowerShell 5 nie jest
sprawdzony. Platny panel nadal wymaga osobnego uzasadnienia i jawnego budzetu;
ta zmiana nie uruchamia zapytan ani nie wlacza nowych platnych domyslnych tras.
Domyslne Referer i Title to generyczne placeholdery; wlasna publiczna
atrybucje przekazuj jawnie przez flagi `-Referer` i `-Title`.

## Workflow

1. Przygotuj samodzielny plan: cel, kroki, zalozenia, ograniczenia, ryzyka i kryteria akceptacji.
2. Usun sekrety, klucze, dane wrazliwe, pelne `.env` i niepubliczne dane klientow. Prompt trafia do zewnetrznych dostawcow.
3. `rada.ps1` blokuje przebieg przed pierwszym requestem, gdy Plan albo Context zawiera sekret wysokiej pewnosci (m.in. private key, dlugi Bearer, rozpoznany prefix vendora albo przypisany key/token). Nie blokuje neutralnych opisow auth/secret. Odpowiedzi providera sa deterministycznie redagowane przed zapisem oraz przed anonimowym bundle rundy 2; wartosci nie sa logowane ani hashowane.
4. Sprawdz Model Radar. Gdy jest `STALE`, `INVALID` albo `MISSING`, wykonaj procedure odswiezenia ze skilla `model-radar` bez pytania uzytkownika i dopiero potem uruchom rade. `rada.ps1` ma ten sam fail-closed preflight przed pierwszym platnym wywolaniem.
5. Przy zmianie rosteru albo kosztow najpierw wykonaj bezplatny preflight:

```powershell
& "<active-skill-dir>\scripts\rada.ps1" -ResolveOnly
```

6. Uruchom panel:

```powershell
$plan = @'
<plan do recenzji>
'@
$ctx = @'
Repo: <sciezka>; ograniczenia: <czas/sprzet/prod>; kryteria akceptacji: <co musi byc prawda>.
'@
& "<active-skill-dir>\scripts\rada.ps1" -Plan $plan -Context $ctx
```

7. Przeczytaj `_manifest.json`, `_index.json` i odpowiedzi modeli. Sprawdz, jaki model zostal rozwiazany oraz jaki model faktycznie odpowiedzial.
8. Zrob wlasna synteze: zgodne obawy, punkty sporne, najlepsze poprawki, odrzucone zarzuty oraz `GO`, `GO-Z-POPRAWKAMI` albo `NO-GO`.

## Tryby

- `-Quick`: 4 soczewki - przewodniczacy, wykonanie, poprawnosc i niezalezna perspektywa Meta.
- Domyslnie: 9 soczewek - `Quick` plus Claude Opus, Kimi, HY4 jako inzynier systemowy, alternatywna architektura i kontrarianin Grok.
- `-Full`: 12 soczewek - panel domyslny plus red-team, prostota/YAGNI i intencja biznesowa.
- `-Brainstorm`: dwie platne rundy na tym samym, swiezym rosterze: niezalezna dywergencja, a potem anonimowy bundle i krytyka/integracja przez kazdego zdrowego czlonka. Rodzic pozostaje syntezerem.
- `-NoChair`: usuwa role przewodniczacego.
- `-Models "author/model-a","author/model-b"`: jawny panel niestandardowy. To swiadomy override; kazdy model nadal musi istniec i miec aktywny endpoint.
- `-IncludeFugu`: dodaje opcjonalnego arbitra.
- `-RefreshRoster`: wymusza odswiezenie publicznego katalogu przed rozwiazaniem skladu.
- `-Effort low|medium|high`, `-MaxTokens N`, `-Throttle N`: kontroluja glebokosc, koszt i wspolbieznosc. `MaxTokens` nie moze byc nizsze niz 2048, bo reasoning i finalna odpowiedz dziela ten sam budzet.

Przed `-Brainstorm` przeczytaj
[references/brainstorm-protocol.md](references/brainstorm-protocol.md) oraz
[references/trigger-cases.json](references/trigger-cases.json). Tryb brainstorm
jest jawny; zwykly review pozostaje zachowaniem domyslnym.

## Gwarancje

- Brak automatycznego fallbacku do starszej generacji. Provider moze zmienic endpoint dla tego samego modelu, ale rada nie zamieni Qwen 3.8 na 3.7, HY4 na HY3 ani nowszego Groka na starszego po cichu.
- `stealth/ox-alpha` jest wycofanym aliasem testowym GLM-5.3 Flash. Nie jest rola rady i jest blokowany takze w panelu niestandardowym. Publiczny model moze wrocic tylko pod kanonicznym ID i po oddzielnej decyzji o transporcie; preferowany jest Coding Plan zamiast dodatkowego kosztu OpenRouter.
- Selektory rodzin wybieraja najnowszy zgodny model powyzej zaakceptowanego floor. Dotyczy to takze rodzin Claude Opus i Kimi. Nowy model pasujacy do rodziny moze wejsc automatycznie; nowa rodzina, zmiana nazewnictwa albo decyzja o zmianie roli wymaga jawnej aktualizacji polityki.
- Uwierzytelniony katalog OpenRouter `models/user` jest cache'owany maksymalnie 7 dni poza skillem w `~/.agents/model-council`; uwzglednia ustawienia konta, a wybrane modele maja sprawdzane endpointy przy kazdym panelu.
- Dwa kolejne bledy modelu uruchamiaja 24-godzinny circuit breaker. Aktualizacja stanu ma blokade miedzyprocesowa, a plik nie zawiera promptow ani sekretow.
- Pusta odpowiedz, ktora zuzyla caly jawnie ustawiony budzet `MaxTokens`, jest oznaczana jako `budget_exhausted` i odrzucana z rundy, ale nie zatruwa circuit breakera dostawcy.
- Brak wystarczajacej liczby zdrowych modeli zatrzymuje zadanie przed inferencja.
- Brainstorm fail-closed: za malo odpowiedzi po rundzie 1 blokuje runde 2, a za malo odpowiedzi po rundzie 2 konczy przebieg bez fallbacku. Manifest rozdziela rundy, tokeny, koszty i pliki dowodowe.
- `_manifest.json` zapisuje wersje polityki, Model Radar, katalog, rozwiazany roster, ceny, maksymalny koszt samego outputu, tokeny i koszt raportowany przez API.

## Synteza

W brainstormingu nie licz glosow. Zachowaj zgodne i sprzeczne hipotezy, najmocniejsze elementy, zalozenia oraz testy rozstrzygajace; decyzje GO/NO-GO i decyzje produkcyjne pozostaja po stronie rodzica.

- `ZGODNE OBAWY`: co najmniej dwie niezalezne soczewki albo jeden mocny zarzut `[pewne]` poparty dowodem.
- `PUNKTY SPORNE`: pokaz obie strony i rozstrzygnij wedlug celu oraz ograniczen.
- `NAJLEPSZE POMYSLY`: poprawki o wysokiej wartosci i proporcjonalnym koszcie.
- `CO ODRZUCAM`: spekulacje, wymagania spoza kontekstu, duplikaty i zarzuty obalone dowodem.
- `REKOMENDACJA`: werdykt, `MUST-FIX`, `SHOULD-FIX`, kolejna sekwencja i poziom pewnosci.

Szczegoly rosteru, algorytmu i procedury utrzymania sa w `references/panel-i-synteza.md`.
