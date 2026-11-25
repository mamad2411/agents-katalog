---
name: plan-delivery
description: Plan every new task as a short TODO with requirements, dependencies, maker/reviewer pairs and product checks. A strong current parent plans once; no planning contract or review-of-plan ceremony.
---

# Plan delivery: TODO 1.0

1. Mocny planista czyta prompt, istotny kontekst i wypisuje wszystkie wymagane
   wyniki oraz zakazy. Biezacy rodzic Astra/Fable moze byc tym planista; nie
   wywoluj drugiego modelu dla jego podpisu. Tani rodzic zleca jeden krotki plan
   mocnemu dostepnemu modelowi przez Agent CLI, bez calej historii rozmowy.
2. Kazdy task ma: text, covers, scope, done_when, maker, reviewer, depends_on.
   Dla rzeczywistego wykonania zapisz JEDEN todo.json wedlug
   agent-graph/references/todo-example.json. Dla samej odpowiedzi wystarczy
   inline TODO; nie uruchamiaj CLI do mechanicznego odczytu statusu.
3. Najpierw dowiez najwazniejszy wykonalny niezrealizowany wynik wlasciciela.
   Kosmetyka/poboczny zakres wymaga potrzebnej zaleznosci albo konkretnej blokady
   wyniku glownego. Odbiorca dostaje pierwotne wymaganie obok aktualnego TODO.
   Zaleznosc dodaj tylko dla potrzebnego artefaktu lub kolejnosci biznesowej.
   Rozlaczny frontend/backend startuja razem po ustaleniu interfejsu.
   Osobny task integracji i UAT wynika z ryzyka zmiany, nie potrzeby kolejnego receipt.
4. Dobierz taniego kompetentnego wykonawce i niezaleznego odbiorce z innego labu.
   Ocena dopasowania + dostepna quota decyduja; nie kazdy task wymaga najdrozszego
   krytyka. Specjalizacja moze uzasadniac drozsze wykonanie, np. trudny design.
   Krok z jedna poprawna odpowiedzia (suma, deduplikacja, walidacja, dopuszczenie,
   odczyt stanu) planuj jako kod albo `checks`, bez wywolania modelu; model tylko
   do oceny i tworzenia. Brak potrzebnego narzedzia nazwij blokada tego kroku.
5. Zweryfikuj sam, czy TODO pokrywa prompt. Bez fidelity/sufficiency, swiadka
   planisty, zapieczetowanych kontraktow, amendment budget i osobnych zatwierdzen.
   Pytaj tylko o prawdziwa niejasnosc biznesowa albo wymagana zgode.

## Wykonanie i fast-path S/M/L

- Dobor sciezki wykonania wg zadania i rzeczywistych zaleznosci, z zachowaniem wymaganego odbioru:
  - **S**: inline TODO dla prostych odpowiedzi i malych zmian.
  - **M**: pojedyncza para `todo_pair.py` wykonawca/odbiorca bez narzutu orkiestracji grafu.
  - **L**: `todo_graph.py` dla zadan z galeziami zaleznosci i rownoleglym wykonaniem.
- Pasywny pomiar narzutu: `delivery-audit/scripts/delivery_audit_metrics.py` oblicza
  `lead_time_s`, `model_exec_s`, `review_s`, `check_s`, `ceremony_s` oraz
  `ceremony_ratio = round(ceremony_s / max(lead_time_s, 1.0), 4)` z istniejacych
  `state.json` i `telemetry.jsonl` bez tworzenia nowych plikow receipt.
  Flaga `high_ceremony_alert=True` (>0.25) jest heurystyczna wskazowka, nie bramka
  ani dowod straty. Nieopisany czas, nakladanie czasow i brak danych moga
  znieksztalcic wynik; zero takze nie dowodzi zdrowego procesu. Zmiane uzasadnia
  konkretna przyczyna i skutek dla zadania, nie sam prog ani syntetyczny benchmark.
  Bez dodatkowego pomiaru lub kroku w zwyklej sesji.

Tani rodzic nie buduje grafu, zeby dopiero zamowic plan. Wywoluje bezposrednio
`agent-graph/scripts/todo_fleet.py --request <planning-request.json> --output <result.json>`.
Wzor: `agent-graph/references/planning-request.json`; podmien workspace, opis,
wejscia i aktualnego mocnego kandydata. To jedno read-only wywolanie planisty,
bez starego route/assessment/planning gate. Rodzic przeklada jego wynik na TODO.

Agent Graph uruchamia TODO, Fleet dobiera i uruchamia istniejace natywne CLI.
Model rodzica nie polluje kazdego wezla. Jeden odbiorca sprawdza produkt,
zwraca konkretne usterki wykonawcy albo ACCEPT. Naprawa nie tworzy nowego planu.
Tokeny to telemetria; jawny limit wlasciciela pozostaje wiazacy.
Materialna zmiana intencji wymaga aktualizacji TODO, nie cichego usuniecia wymagania.

Stare plan_contract.py i jego references zostaja tylko do odczytu/recovery
historycznych kontraktow. Nie wywoluj ich dla nowej pracy. Nowa polityka nie
modyfikuje ani nie zatwierdza automatycznie starych runow.

Automatyczny audyt korzysta z tego samego TODO: planista wpisuje typowane
`completion` jak w przykladzie Graphu oraz wskazuje istniejacy context-receipt
rodzica. Nie dodawaj recznego wywolania audytu, nowego planisty ani odczytu
transkrypcji. Brak klasyfikacji/bindingu pozostaje SKIPPED_UNCLASSIFIED.
