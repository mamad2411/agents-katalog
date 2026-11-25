---
name: security-audit
description: Uzyj do niezaleznego audytu bezpieczenstwa biezacych zmian lub wskazanego zakresu - ZWLASZCZA przed wdrozeniem lub deployem na produkcje. Sprawdza sekrety, auth/uprawnienia/IDOR, ekspozycje (porty/CORS/tunele/debug), walidacje wejscia, wyciek danych klienta. Raport z severity, bez naprawiania bez zgody.
---

Zrob niezalezny audyt bezpieczenstwa biezacych zmian (lub wskazanego zakresu). Patrz nieufnie; domyslnie zakladaj problem, jesli nie masz pewnosci.

Sprawdz:
- Sekrety w kodzie/repo/logach (klucze, tokeny, hasla).
- Auth i uprawnienia: czy kazdy endpoint i akcja sprawdza dostep; brak IDOR.
- Ekspozycja: porty, CORS, tunele, otwarte buckety, debug na produkcji.
- Walidacja wejscia: SQL/command/path injection, XSS, deserializacja.
- Wyciek danych klienta w odpowiedziach/logach/komunikatach bledow.

Jesli zakres zawiera agentow, skille, MCP, pamiec/RAG, endpointy modeli albo
autonomiczne wywolania narzedzi, dolacz `ai-infrastructure-audit`. Jego macierz
granic zaufania uzupelnia ten przeglad aplikacyjny; nie zastepuje kontroli auth,
IDOR, danych i ekspozycji.

Output: lista ustalen z severity (krytyczne/wysokie/srednie) + plik:linia + rekomendacja.
Nie naprawiaj bez mojej zgody - najpierw raport.

Opcjonalnie uzyj skilla `codex-security-cli` jako drugiego, automatycznego
recenzenta repozytorium. Najpierw wykonaj jego lokalny `preflight`. Skan
modelowy uruchom tylko po jawnej zgodzie na zakres, klasyfikacje danych, wyslanie
kodu do OpenAI i limit kosztu. Nie uruchamiaj bezposrednio `npx
codex-security`. Finding automatyczny zawsze zweryfikuj recznie; brak findingow
nie oznacza, ze system jest bezpieczny.
