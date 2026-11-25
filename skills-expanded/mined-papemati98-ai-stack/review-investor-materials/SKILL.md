---
name: review-investor-materials
description: Niezaleznie odbiera pitch deck, memorandum inwestycyjne i one-pager pod katem faktow, finansow, narracji, designu, eksportu i poufnosci. Uzyj przed uznaniem materialu do pozyskania finansowania za gotowy do przegladu wlasciciela; nie uzywaj jako zgody na wysylke lub publikacje.
---

# Review investor materials

Odbierz aktualne pliki, nie deklaracje makerow. Kazdy review jest przypiety do
hashy edytowalnego zrodla albo renderu PDF. Zmiana pliku uniewaznia review.

Helper `scripts/investment_material_acceptance.py` jest deterministyczna bramka
dowodow. Wymaga `pypdf`, aby mierzyc liczbe stron bezposrednio z bajtow PDF. Nie
renderuje, nie naprawia, nie uruchamia modeli i nie wysyla materialu.

Przed pierwszym odbiorem przeczytaj
[acceptance-contract.md](references/acceptance-contract.md). Do przegladu tresci
i designu uzyj [review-checklists.md](references/review-checklists.md).

## Warunki wejscia

1. Kampania `fundraising` ma aktualny seal `READY_FOR_DRAFTING`.
2. Kazdy wymagany artefakt ma edytowalne zrodlo oraz render PDF.
3. Content maker i design maker sa jawni. Reviewer odpowiedniego gate'u jest
   inna linia modelu lub czlowiek.
4. Review evidence i wszystkie artefakty sa lokalnymi plikami wewnatrz katalogu
   kampanii i maja aktualne SHA-256.

## Odbior

1. Factual reviewer sprawdza kazdy claim ze zrodlem, rodzaj claimu, aktualnosc i
   zakres ujawnienia.
2. Financial reviewer przelicza number ledger, okresy, jednostki, waluty,
   projekcje i spojność deck/memo/one-pager.
3. Narrative reviewer ocenia teze, audience fit, logike, ryzyka, ask i brak
   genercznych lub nieudowodnionych stwierdzen.
4. Visual reviewer oglada kazda wyrenderowana strone: hierarchie, gestosc,
   kontrast, clipping, czytelnosc, dostepnosc i dowodowy charakter wizualizacji.
5. Export reviewer sprawdza otwieranie, page count, fonty/media, metadane,
   rozmiar oraz zgodnosc PDF z edytowalnym zrodlem. One-pager ma dokladnie 1 PDF
   page.
6. Confidentiality reviewer sprawdza provider boundary, sekrety, dane restricted
   i materialy, ktorych Mateusz nie zatwierdzil do ujawnienia.

Zapisz candidate receipt, potem uruchom:

```powershell
python scripts/investment_material_acceptance.py validate --campaign-dir <dir> --receipt <candidate.json>
python scripts/investment_material_acceptance.py seal --campaign-dir <dir> --receipt <candidate.json> --output final-acceptance.json
python scripts/investment_material_acceptance.py verify --campaign-dir <dir> --acceptance final-acceptance.json
```

## Petla napraw

`FAIL` lub `BLOCKED` wraca do najmniejszego odpowiedzialnego wezla Agent Graph.
Po zmianie artefaktu trzeba odnowic wszystkie review zwiazane z jego poprzednim
hashem. Nie wolno zmieniac kryterium, liczyc sredniej ani akceptowac najlepszego
dotad wariantu. Budzet napraw pozostaje ograniczony do 1-3 rund.

## Wynik

- `ACCEPTED`: wszystkie szesc gate'ow ma aktualny PASS, lineages sa niezalezne,
  wymagane artefakty sa kompletne i nie ma otwartego P0/P1;
- `NOT_ACCEPTED`: brakuje aktualnego dowodu albo naprawa nie domknela gate'u;
- `BLOCKED`: potrzebna jest decyzja Mateusza albo niedostepny dowod.

Nawet `ACCEPTED` oznacza tylko gotowosc do finalnego przegladu Mateusza.
Dystrybucja pozostaje `not_authorized` i wymaga osobnej zgody na pliki, odbiorce
i kanal.
