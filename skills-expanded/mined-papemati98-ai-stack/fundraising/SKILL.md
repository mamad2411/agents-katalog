---
name: fundraising
description: Buduje albo naprawia pitch decki, memoranda inwestycyjne i one-pagery do pozyskania finansowania na podstawie zweryfikowanych dowodow, spojnych liczb i jawnych decyzji wlasciciela. Uzyj przy tworzeniu materialow inwestorskich; nie uzywaj do wysylki, kontaktu z inwestorami ani porad prawnych, podatkowych lub inwestycyjnych.
---

# Fundraising

Prowadz material inwestycyjny jak kontrolowany proces decyzyjny, nie jednorazowe
generowanie slajdow. Fakty i liczby pochodza wylacznie z zatwierdzonych ledgerow.
Brak wiedzy o firmie blokuje drafting zamiast uruchamiac domysly modelu.

Helper `scripts/fundraising_workflow.py` jest deterministyczna bramka. Nie
wywoluje modeli ani sieci, nie tworzy claimow i nie kontaktuje inwestorow.

## Tryby

- `create`: nowy deck, memorandum, one-pager albo ich spojny zestaw;
- `review-repair`: odbior istniejacych edytowalnych zrodel i PDF, a potem
  ograniczona petla napraw na tym samym kontrakcie dowodow.

Przed pierwszym runem przeczytaj [workflow.md](references/workflow.md). Przy
zrodlach i liczbach przeczytaj [evidence-ledgers.md](references/evidence-ledgers.md).
Dla wybranego formatu przeczytaj [artifact-contracts.md](references/artifact-contracts.md).
Przed delegacja przeczytaj [orchestration.md](references/orchestration.md).

## Bramka wejsciowa

1. Uzyj `llm-wiki` i pobierz `project-brief --require-context`. Gdy continuity
   jest `MISSING`, nie wnioskuj nic z poprzednich rozmow ani model memory.
2. W istniejacym TODO ujmij wymagane artefakty, klasyfikacje/dostep do danych,
   aktualne ledger'y i kryteria niezaleznego odbioru. Nie tworz osobnego kontraktu
   planowania/governance/odbioru ani grafu przed draftingiem. Jeden Agent Graph
   sluzy faktycznej delegacji rozlacznych galezi, gdy jest potrzebna.
3. Zainicjalizuj katalog kampanii albo zweryfikuj istniejacy:

```powershell
python scripts/fundraising_workflow.py init --campaign-dir <dir> --campaign-id <id> --company-name <nazwa> --project-slug <slug> --artifacts deck,memorandum,one-pager
python scripts/fundraising_workflow.py validate --campaign-dir <dir>
python scripts/fundraising_workflow.py gate --campaign-dir <dir>
```

4. Uzupelnij z Mateuszem: odbiorce, etap, geografie, kwote, instrument, warunki,
   zakres ujawnienia, finalny ask i dozwolonych dostawcow. Zewnetrzna dystrybucja
   pozostaje `not_authorized`.
5. Zbuduj source, claim i number ledger. Kazdy claim w artefakcie musi byc
   `verified`; kazda liczba ma jednostke, okres, zrodlo lub formule Decimal.

`gate` musi zwrocic `READY`. `BLOCKED` oznacza konkretne brakujace decyzje lub
continuity. `INVALID` oznacza niespojny dowod, claim albo liczbe do naprawy.

## Realizacja

1. Agent Graph rozdziela evidence freeze, finanse, narracje, design, render i
   odbior. Agent Fleet dobiera wykonawcow; maker nie recenzuje siebie.
2. Rada Modeli rozstrzyga materialne spory o strategie, audience, instrument i
   teze inwestycyjna, ale nie zatwierdza decyzji za Mateusza.
3. Tresc i design moga isc rownolegle dopiero po zamrozeniu claim/number ledger.
   Design Loop pracuje na aktualnym storyboardzie i renderach, nie wymysla
   dowodow wizualnych.
4. Zachowaj edytowalne zrodla. PDF jest domyslnym artefaktem do odbioru i wysylki;
   one-pager ma dokladnie jedna strone PDF.
5. Po kazdej materialnej zmianie ponownie uruchom `validate` i `gate`, a stare
   receipt'y dla zmienionych hashy traktuj jako niewazne.
6. Finalny odbior wykonuje niezalezny skill `review-investor-materials`.

## Twarde granice

- Nie fabrykuj TAM, trakcji, klientow, zespolu, partnerstw, wycen ani obrazow
  przedstawianych jako dowod.
- Nie stosuj arbitralnego score'u "fundability" ani sredniej zamiast gate'ow.
- Nie zakladaj VC, SAFE, USA, Izraela ani innej geografii/instrumentu bez decyzji.
- Nie instaluj zaleznosci, nie uruchamiaj kodu z obcego skilla i nie zmieniaj
  providera/modelu w ramach naprawy materialu.
- Nie wysylaj, nie publikuj i nie kontaktuj inwestora bez osobnej, dokladnej zgody
  Mateusza na finalne pliki, odbiorce i kanal.

## Raport

Podaj: campaign id, tryb i artefakty; continuity i klasyfikacje danych; status
claim/number ledger; nierozstrzygniete owner gates; wykonawcow i reviewerow;
wyniki content/design/export acceptance; aktualne hashe; oraz jednoznaczne
`READY_FOR_OWNER_REVIEW`, `BLOCKED` albo `NOT_ACCEPTED`.
