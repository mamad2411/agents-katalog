---
name: wordpress-engineering
description: "Projektuje, rozwija, diagnozuje i audytuje WordPress: pluginy, motywy, bloki, REST API, uprawnienia i operacje WP-CLI. Użyj przy zadaniach WordPress, z obowiązkowym rozpoznaniem typu projektu, środowiska oraz granic produkcji przed zmianami."
---

# WordPress engineering

Najpierw ustal, czy pracujesz nad core, pluginem, motywem klasycznym, block theme, blokiem czy integracją. Nie zakładaj struktury projektu na podstawie samej obecności PHP.

## Procedura

1. Rozpoznaj typ projektu, wersje PHP/WordPress, narzędzia, aktywny katalog i środowisko: local, DEV, staging lub produkcja.
2. Sprawdź aktualną dokumentację WordPress dla używanych API. Preferuj publiczne API i konwencje istniejącego repozytorium.
3. Zdefiniuj kontrakt funkcji, uprawnienia, sanitizację, escaping, nonce/CSRF, REST permission callbacks oraz migracje danych.
4. Wprowadź najmniejszą zmianę i uruchom istniejące testy PHP/JS, lint oraz sprawdzenie renderowania lub endpointu.
5. Dla bloków sprawdź zapis, edycję, serializację, atrybuty i migrację wersji. Dla REST sprawdź schemat, capability gate i brak IDOR.
6. Operacje WP-CLI, import/eksport bazy, search-replace, aktualizacja pluginów, publikacja i zmiana produkcji wymagają jawnego wskazania środowiska i osobnej zgody.

## Zasady

- Nigdy nie zgaduj URL, ścieżki, prefixu tabel ani aktywnego konta hostingowego.
- Nie zapisuj artefaktów audytu do drzewa pluginu lub motywu, chyba że repo ma taki kontrakt.
- Nie kopiuj kodu ani tekstu z zewnętrznych repozytoriów WordPress bez kontroli licencji.
- Błędy security i kompatybilności raportuj jako konkretne kryteria `PASS`, `FAIL` lub `BLOCKED`.

Kontrakt projektu znajduje się w `references/project-contract.md`, a granice
aktywacji w `references/trigger-cases.json`.
