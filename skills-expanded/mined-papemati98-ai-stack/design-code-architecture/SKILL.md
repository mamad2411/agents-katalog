---
name: design-code-architecture
description: "Projektuje lub recenzuje architekturę kodu przez model domeny, granice modułów, publiczne kontrakty i małe pionowe kroki wdrożenia. Użyj przed większą funkcją, przebudową odpowiedzialności, podziałem monolitu albo gdy zmiana przecina wiele modułów."
---

# Design code architecture

Nie zaczynaj od katalogów i klas. Najpierw ustal język domeny, odpowiedzialności, przepływ danych i miejsce, w którym wymagana zmiana powinna być izolowana.

Przed edycją zrób zwięzłą mapę wpływu, gdy zmiana istotnie usuwa albo przenosi moduł,
zmienia jego nazwę na granicy modułów lub zmienia publiczny kontrakt. Uwzględnij callerów
przychodzących, zależności wychodzące, przepływ danych, konsumentów i dotknięte sprawdzenia
regresji. Mała lokalna zmiana bez naruszenia tych granic nie wymaga osobnego artefaktu
architektonicznego; szczegóły i przykłady są w `references/architecture-contract.md` oraz
`references/trigger-cases.json`.

## Procedura

1. Zmapuj aktualny system: wejścia, wyjścia, dane trwałe, zależności, publiczne API i właścicieli modułów.
2. Nazwij pojęcia domenowe oraz niezmienniki. Oddziel reguły biznesowe od transportu, frameworka i storage.
3. Wskaż `fixed diff point`: najmniejszą stabilną granicę, za którą przyszłe warianty nie wymagają rozlewania zmian po systemie.
4. Porównaj 2-3 warianty. Dla każdego podaj koszt migracji, ryzyko operacyjne, testowalność, coupling i sposób wycofania.
5. Wybierz najmniejszą wystarczającą architekturę. Abstrakcja musi usuwać realną złożoność albo odpowiadać istniejącemu wzorcowi repozytorium.
6. Rozbij wdrożenie na pionowe, obserwowalne kroki, z testem publicznego zachowania po każdym kroku.
7. Po implementacji sprawdź, czy nowa granica faktycznie zawiera zmianę i nie stworzyła równoległego źródła prawdy.

## Twarde zasady

- Nie rób refaktoru „przy okazji”.
- Nie twórz generycznego frameworka dla jednego przypadku.
- Nie testuj prywatnej implementacji, jeśli można przetestować publiczne zachowanie.
- Migracje danych, API i uprawnień muszą mieć kompatybilność wsteczną albo jawny plan przejścia.
- Dla pracy produkcyjnej połącz ten skill z `new-task`, `test-first-engineering` i właściwym QA.

## Weryfikacja dowodowa architektury (architecture_evidence.py)

Dla istotnych granic modułów i publicznych kontraktów generuj weryfikowalne diagramy Mermaid oparte na dowodach w kodzie (`scripts/architecture_evidence.py`):
1. **Przypięty commit Git**: dowody weryfikowane są przez `git show <commit>:<sciezka>` w ukrytym podprocesie (`CREATE_NO_WINDOW`), nigdy na mutowalnym drzewie roboczym.
2. **Ścisłe cytowania**: deklaruj bezpieczne ścieżki repo-relative, ograniczone 1-indeksowane zakresy linii (maks. 500) i dokładne cytaty.
3. **Deterministyczny Mermaid z ucieczką etykiet**: znaki specjalne (`"`, `<`, `>`, `[`, `]`, `(`, `)`) są encjowane, a relacje znakowane statusem `[review req]`.
4. **Atomowa publikacja**: diagram `.mmd` publikowany jest dopiero po przejściu 100% walidacji; wcześniejszy poprawny plik przetrwa błąd walidacji.

Polecenia CLI:
```bash
# Walidacja manifestu JSON względem repozytorium Git
python -B scripts/architecture_evidence.py validate manifest.json --repo . --diagnostics diag.json

# Walidacja i atomowe wygenerowanie diagramu Mermaid
python -B scripts/architecture_evidence.py render manifest.json --output arch.mmd --repo .
```

### Granica zapewnień (Assurance Boundary)
- Walidacja kodu potwierdza wyłącznie, że wskazany plik, zakres linii i cytat istnieją w niezmiennym obiekcie commita Git.
- Walidacja NIE stanowi dowodu semantycznego: nie poświadcza prawdziwości asercji relacyjnych, logiki biznesowej ani braku pominiętych zależności.
- Wszelkie asercje relacji semantycznych pozostają jawnie `REVIEW_REQUIRED` (wymagają przeglądu architekta).

Szablon decyzji znajduje się w `references/architecture-contract.md`, granice
aktywacji w `references/trigger-cases.json`, a format dowodów Mermaid w
`../creating-mermaid-diagrams/reference/code-evidence.md`.
