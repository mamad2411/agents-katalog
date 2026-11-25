---
name: systematic-debugging
description: Reprodukuj, zawezaj i naprawiaj bledy programistyczne na podstawie dowodow, z testem regresyjnym i jawnym wynikiem NOT_REPRODUCED, gdy reprodukcja sie nie uda.
---

# Systematic Debugging

Uzyj, gdy istnieje konkretny symptom, regresja, blad testu lub rozbieznosc kontraktu.

1. Zapisz symptom, oczekiwany kontrakt i zakres zmian; nie zakladaj root cause.
2. Odtworz problem w dozwolonym srodowisku. Przy odtwarzaniu w non-prod uzyj danych syntetycznych lub zredagowanych i zablokuj realne maile, platnosci oraz inne skutki uboczne. Historyczne logi dowodza wystapienia bledu, ale nie sa aktywna reprodukcja. Jesli odtworzenie jest niemozliwe, oznacz `NOT_REPRODUCED`, zapisz evidence gap i nie przedstawiaj hipotezy jako naprawy.
3. Zbierz dowody na granicach: wejscie, wyjscie, stan, wersja, konfiguracja, storage, API i logi bez ujawniania sekretow.
4. Utworz 2-4 konkurencyjne hipotezy i dla kazdej test rozstrzygajacy. Wybierz najmniejszy eksperyment o najwyzszej wartosci informacyjnej.
5. Znajdz przyczyne zrodlowa, wprowadz najmniejsza odwracalna poprawke, dodaj regresje i uruchom testy wedlug blast radius.
6. Zamknij hipotezy odrzucone dowodem. Raport zakoncz statusem `FIXED`, `NOT_REPRODUCED` albo `BLOCKED`.

Przy incydencie produkcyjnym dodaj przed hipotezami krotka os czasu: symptom i poczatek degradacji, ostatnie deploye i zmiany konfiguracji, metryki oraz logi. Porownaj je z dowodami na granicach. Zbieznosc w czasie wskazuje hipoteze, nie przyczyne; test ma odroznic konkurencyjne wyjasnienia, a wynik nierozstrzygajacy pozostawia przyczyne otwarta. Diagnoza produkcji jest odczytowa: bez jawnej zgody nie sonduj aktywnie produkcji, nie wykonuj rollbacku ani innych dzialan ze skutkiem. Maly izolowany blad lokalny pozostaje przy zwyklej sciezce 1-6 bez osi incydentu.

Przeczytaj [contract.md](references/contract.md) dla formatu dowodow i [trigger-cases.json](references/trigger-cases.json) przed wyborem trybu. Nie usuwaj danych, nie zmieniaj produkcji i nie uruchamiaj zewnetrznych dzialan bez osobnej zgody.

Przy bardzo duzych wynikach (tysiace linii testu, dlugie logi, rozlegle diffy) uzyj opcjonalnego agregatora [scripts/summarize_evidence.py](scripts/summarize_evidence.py) wg [references/large-results.md](references/large-results.md). To nie jest nowy preflight -- stosuj go tylko, gdy reczny odczyt jest niepraktyczny, i nie zastępuje zwyklej sciezki 1-6.

Gdy symptom dotyczy konkretnego artefaktu (binaria, pakiet, snapshot runtime, komunikacja IPC) i zwykla sciezka 1-6 nie wyjasnia przyczyny, zajrzyj warunkowo do [references/artifact-inspection.md](references/artifact-inspection.md). To krotka referencja read-only do mapowania formatu, sledzenia bundli/IPC oraz znakowania twierdzen jako OBSERVED/INFERRED/UNKNOWN z file/hash/line; nie jest nowym obowiazkowym krokiem zwyklej sesji.
