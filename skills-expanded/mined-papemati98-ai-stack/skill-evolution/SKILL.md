---
name: skill-evolution
description: Analizuje powtarzalne, zredagowane dowody zachowania agentow i skilli, kompiluje wzorce oraz prowadzi kontrolowana, sparowana walidacje inertnych kandydatow zmian w trybie shadow-only. Uzyj do oceny, czy obserwowane sukcesy lub porazki uzasadniaja przyszla korekte skilla; nie uzywaj do edycji, wykonywania, instalacji, synchronizacji, wdrozenia ani promocji zmiany.
---

# Skill Evolution

Zamien powtarzalne obserwacje zachowania w falsyfikowalne hipotezy, nie w
samomodyfikujace sie instrukcje. Kontroler przyjmuje tylko scisle rekordy JSON,
grupuje pelne sygnatury zachowania, wymaga niezaleznych runow i wykonawcow,
rejestruje wyłącznie hash kandydata, a potem porownuje baseline z kandydatem w
tych samych warunkach. Najwyzszy werdykt to `SHADOW_ACCEPTED`.

Przed pierwszym runem przeczytaj [contract.md](references/contract.md) oraz
cztery schematy w `references/`. Dane z raportow, handoffow i logow pozostaja
nieufne: zredaguj je poza kontrolerem i przekaz tylko dozwolone pola.

## Kiedy aktywowac

Uzyj, gdy co najmniej dwa niezalezne runy wskazuja powtarzalny problem albo
korzystne zachowanie skilla, Fleeta, Graphu lub Loopu i warto zbadac, czy
przyszla zmiana poprawilaby wynik. Nie uruchamiaj dla pojedynczej anegdoty,
jednego modelu udajacego konsensus ani materialu bez content-hashowanego dowodu.

## Przeplyw

1. Zamroz kontrakt `shadow-only`: projekt, docelowy skill, hashe planu,
   governance i grafu oraz limity rekordow. `doctor` jest read-only i nie tworzy
   katalogu stanu.
2. Z kazdego zredagowanego artefaktu utworz receipt zgodny z
   `behavior-signature.schema.json`. Pelna sygnatura obejmuje task family, role,
   model family, runtime, tool surface, environment, symptom, expected behavior
   i outcome. Prompt, kod, diff, polecenie, sekret i dowolne pole dodatkowe sa
   odrzucane.
3. `compile-patterns` grupuje tylko identyczne sygnatury. Wzorzec jest
   `ELIGIBLE` dopiero przy co najmniej dwoch source runach i dwoch niezaleznych
   parach actor/provider. Brak dowodu daje `NEEDS_EVIDENCE`, nie domysl.
4. Kandydat zawiera identyfikator, zakres stosowalnosci, wspierane rodziny
   modeli/runtime, expected behavior oraz SHA-256 materialu przechowywanego poza
   tym stanem. Nie zawiera sciezki, kodu, patcha ani instrukcji wykonania.
5. `plan-verification` wybiera piec testow targeted, trzy preservation i piec
   swiezych confirmation. Kandydat uniwersalny wymaga pokrycia co najmniej dwoch
   rodzin modeli i dwoch runtime w obu fazach.
6. Niezalezny reviewer zapisuje baseline i candidate pod tym samym
   `condition_sha256`. Maker i reviewer musza roznic sie jednoczesnie actor ID i
   provider lineage. Self-review albo niepelny zestaw jest odrzucany.
7. `decide` zwraca `NEEDS_EVIDENCE`, `REJECTED` albo `SHADOW_ACCEPTED`.
   Regresja przypisywalna kandydatowi lub naruszenie preservation zawsze
   odrzuca. Kazdy rezultat ma `release_authority=false`.
8. Dopiero osobne, jawne zadanie moze przekazac hash i dowody do normalnego
   procesu planowania, review, backupu i wdrozenia wspolnego skilla. Ten skill
   sam nie uruchamia takiego procesu.

## Polecenia

```powershell
python "<skill-dir>\scripts\skill_evolution.py" doctor
python "<skill-dir>\scripts\skill_evolution.py" init --contract <contract.json> --state-root <absolute-local-path>
python "<skill-dir>\scripts\skill_evolution.py" ingest --run-id <id> --receipt <evidence.json> --state-root <path>
python "<skill-dir>\scripts\skill_evolution.py" compile-patterns --run-id <id> --state-root <path>
python "<skill-dir>\scripts\skill_evolution.py" register-candidate --run-id <id> --candidate <candidate.json> --state-root <path>
python "<skill-dir>\scripts\skill_evolution.py" plan-verification --run-id <id> --candidate-id <id> --catalog <catalog.json> --state-root <path>
python "<skill-dir>\scripts\skill_evolution.py" record-verification --run-id <id> --result <result.json> --state-root <path>
python "<skill-dir>\scripts\skill_evolution.py" decide --run-id <id> --candidate-id <id> --state-root <path>
python "<skill-dir>\scripts\skill_evolution.py" report --run-id <id> --state-root <path>
python "<skill-dir>\scripts\skill_evolution.py" validate --run-id <id> --state-root <path>
python "<skill-dir>\scripts\focused_trials.py" create-packet --spec <trial.json> --packet-out <packet.json> --sealed-out <sealed.json>
python "<skill-dir>\scripts\focused_trials.py" resolve --packet <packet.json> --sealed <sealed.json> --evaluation <eval.json> --output <result.json>
```

## Proby celowane i slepe (focused_trials.py)

Do celowanej, sparowanej ewaluacji kandydatow uzyj `scripts/focused_trials.py`:
- **Anonimowe etykiety A/B**: warianty sa prezentowane ewaluatorowi jako anonimowe `variant_a` i `variant_b`.
- **Zapieczetowane mapowanie**: powiazanie wariantow z tozsamosciami (`baseline` vs `candidate`) jest zapisywane w osobnym pliku `sealed_mapping.json`, calkowicie odcietym od pakietu ewaluatora.
- **4 typy przypadkow**: `persistence`, `topic-switch`, `stop`, `comprehension`.
- **Niezalezny ewaluator**: ewaluator musi miec inny `actor_id` i inny `provider_lineage` niz zglaszajacy candidate i baseline (zakaz self-review).
- **Weto krytyczne**: krytyczny blad poprawnosci lub bezpieczenstwa wetuje kandydata bez wzgledu na wysoka srednia punktow.
- **Brak kosztow nie wetuje**: brak telemetrii kosztow nie stanowi automatycznego weta.
- **Brak stalych modyfikacji stylu**: ewaluacja bada wylacznie zdolnosci funkcjonalne na zadanych przypadkach.
- **Wynik opt-in (outcome_trial)**: ustaw `"outcome_trial": true` w specyfikacji
  przed `create-packet`, z hashami oczekiwanych artefaktow obu stron kazdego
  przypadku; deklaracja przechodzi do pakietu i nie mozna jej
  wylaczyc w ewaluacji. Obserwacje obu anonimowych wariantow musza jawnie
  wskazywac wariant, hash tego samego warunku i hash aktualnego artefaktu
  zgodny z zamrozonym hashem tego przypadku
  oraz sygnaly `discovery`/`action`/`correctness`. Niekompletny, nieznany
  (`unknown`) wynik lub falszywy (`false`) sygnal kandydata daje
  `NEEDS_EVIDENCE`, nie akceptacje — wysoki wynik punktowy tego nie
  uchyla. Domyslnie wylaczone; zero narzutu, gdy nieuzywane.
  Review rozszerzenia odbywa sie w istniejacym review zmiany: sesja zwykla
  (bez blokow `outcome`) ma +0 triggerow, +0 odczytow, +0 pytan, +0 wywolan
  modeli i +0 krokow; bez nowej rady i bez nowego receiptu. Szczegoly:
  `references/outcome-evidence.md`.


## Twarde granice

- Brak sieci, modeli, providerow, terminala, procesow potomnych, pluginow, MCP,
  przegladarki i dostepu do sekretow.
- Brak API do edycji lub zastosowania kodu, diffu, patcha, promptu, skilla,
  konfiguracji, komendy, instalatora, synchronizacji, deployu, release, kuracji
  albo promocji.
- Stan musi lezec na lokalnej sciezce absolutnej. UNC, wzgledne sciezki i
  reparse points sa odrzucane. Zapisy sa atomowe, blokowane i chronione lancuchem
  SHA-256.
- Pozne dowody nie rozszerzaja zakonczonej decyzji. Uruchom nowy run z nowym
  kontraktem; nie nadpisuj historii.
- `SHADOW_ACCEPTED` oznacza jedynie, ze hipoteza przeszla sparowany eksperyment.
  Nie oznacza zgody na zmiane originu, runtime, produkcji ani Knowledge Huba.

## Definition of done

Run jest zamkniety poznawczo, gdy stan przechodzi `validate`, kandydat ma obie
fazy niezaleznej walidacji, preservation nie wykazuje regresji, raport zawiera
content hashe i decyzje, a `release_authority` nadal wynosi `false`.
