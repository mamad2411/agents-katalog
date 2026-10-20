# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Czym jest ten projekt

Demonstracja podejścia shift-left do jakości danych: jeden wersjonowany kontrakt pydantic v2
waliduje zdarzenia ecommerce w dwóch pipeline'ach (streaming przez Pub/Sub → Cloud Run → BigQuery
oraz batch), a rekordy łamiące kontrakt trafiają do kwarantanny z powodem odrzucenia.

Projekt ma dwa równorzędne cele: nauczyć właściciela repo pydantic v2 w praktyce oraz być
publicznym portfolio czytelnym dla rekrutera i inżyniera. Oba cele wpływają na decyzje — kod
ma być produkcyjnej jakości, a mechanizmy wyjaśnione, nie tylko użyte.

## Komendy

```bash
make setup                  # instaluje Pythona 3.12, tworzy .venv, synchronizuje workspace uv
make check                  # lint + typy + testy, dokładnie ta sama bramka co CI
make lint                   # ruff check
make format                 # ruff format + autofix importów
make typecheck              # mypy strict z pluginem pydantic
make test                   # pytest z pokryciem, bez testów oznaczonych `slow`
make gen                    # generator: N zdarzeń z odsetkiem błędnych ERR (domyślnie 1000 / 0.2)
make image                  # obraz Dockera usługi ingest (dq-pipeline:local)
make local-stream           # streaming end-to-end na emulatorze Pub/Sub, sprawdzony wyrocznią
make local-stream-down      # sprzątanie po nieudanym local-stream (kontenery zostają do debugowania)
make batch-local            # batch end-to-end: 3 loady sprawdzone wyrocznią (bez Dockera)
make bench                  # benchmark walidacji, BENCH_N=100000; nie w CI
make schemas                # schematy BigQuery z modeli -> infra/terraform/schemas/ (commitowane)
make tf-validate            # Terraform fmt/init/validate z obrazu Dockera (wymaga Dockera)
make help                   # pełna lista celów
```

Pojedynczy test lub plik:

```bash
uv run pytest tests/contracts/test_purchase_event.py::test_value_must_match_line_items -x
uv run pytest -k "currency" -vv
uv run pytest -m slow        # testy wydajnościowe, domyślnie pomijane
```

Każda zmiana w zależnościach wymaga `uv sync --all-packages`; CI leci na `--frozen`, więc
`uv.lock` musi być w commicie.

## Architektura

### Zasada nadrzędna: jedno źródło prawdy

`packages/dq-contracts` to jedyne miejsce, w którym opisany jest schemat danych. Publisher,
usługa ingest, loader batchowy i generator schematów BigQuery importują ten sam pakiet.
Wymusza to `uv workspace` — zależności rozwiązują się do kodu z dysku (`{ workspace = true }`),
nie do wersji z PyPI. Schemat nie może powstać w dwóch miejscach, bo natychmiast się rozjedzie.

Pakiet `dq-contracts` nie ma i nie może mieć zależności od GCP — to czysta warstwa domenowa.
Kod chmurowy żyje w `apps/`.

### Przepływ danych

```
generator → walidacja #1 → Pub/Sub topic → push subscription → Cloud Run (ingest)
                ↓ odrzucone                                          ↓ walidacja #2
         BigQuery: quarantine                          BigQuery: events | quarantine
                                                                  ↓ nieprzetwarzalne
                                                          Pub/Sub dead-letter topic
```

Walidacja wykonuje się dwa razy świadomie: przed publikacją (producent nie zaśmieca tematu)
i po odbiorze (konsument nie ufa producentowi). To sedno shift-left, a nie zdublowana praca.

### Sink jako abstrakcja

Zapis danych idzie przez interfejs `Sink` z dwiema implementacjami: lokalną (JSONL + DuckDB
do raportów) i BigQuery. Dzięki temu cały streaming i batch uruchamiają się bez konta GCP,
tym samym kodem ścieżki biznesowej.

### Schematy BigQuery generowane z modeli

Schematy tabel powstają z modeli pydantic (`make schemas`), commitują się do
`infra/terraform/schemas/`, a Terraform czyta je przez `file()`. CI pilnuje driftu — jeśli
wygenerowany schemat różni się od zacommitowanego, build pada. Nigdy nie przepisuj schematu
tabeli ręcznie.

## Etapy projektu

Etapy numerujemy od 1. Realizacja idzie w tej kolejności, każdy etap kończy się działającą
komendą — jeśli czegoś nie da się uruchomić jedną komendą, etap nie jest zamknięty.
Wszystkie etapy są zamknięte. README jest teraz dokumentacją produktu; historia etapów
to tabela na jego końcu, a uzasadnienia decyzji żyją w `docs/adr/0001-0006`.

1. **Etap 1 — szkielet** (gotowy): uv workspace, ruff, mypy strict, pytest, Makefile, CI.
2. **Etap 2 — modele pydantic + testy** (gotowy): `dq_contracts`, każda reguła walidacji ma
   test pozytywny i negatywny. 81 testów, 100% pokrycia.
3. **Etap 3 — generator** (gotowy): `dq_datagen`, katalog błędów z oczekiwanym powodem
   kwarantanny (wyrocznia testowa), dokładny plan błędów, `make gen`. 134 testy, 100% pokrycia.
4. **Etap 4 — streaming lokalnie** (gotowy): `apps/pipeline` (`dq_pipeline`), usługa ingest
   w Dockerze, emulator Pub/Sub, redrive, raport DuckDB, `make local-stream` (też w CI).
5. **Etap 5 — batch lokalnie** (gotowy): powtórka vs duplikat (`TransactionLedger`), loader
   `dq-batch` z idempotentnością pliku i wiersza, `make batch-local` (w CI), `make bench`.
6. **Etap 6 — Terraform** (gotowy): `dq_contracts.bigquery` + `make schemas`, `BigQuerySink`
   (`DQ_SINK=bigquery`), `infra/terraform/` z projektem GCP, job CI `terraform`.
7. **Etap 7 — README** (gotowy): README przebudowane pod czytelnika gotowego projektu,
   ADR 0002–0006, szacunek kosztów z cennika Google z 2026-10-02.

### Co zostaje otwarte (świadomie, opisane w README → „Ograniczenia")

- `terraform apply` / demo na GCP - decyzja właściciela repo, nie dług.
- Loader batchowy w chmurze: load job + `MERGE` zamiast `rename` (ADR 0005).
- Storage Write API zamiast `insertAll` - kandydat do zmiany (ADR 0004), dotyczy tylko `bq.py`.
- Przejście TestClient na `httpx2` - czeka na decyzję właściciela.
- Przy zmianie liczb w README (testy, benchmark, koszty) aktualizuj też ADR 0006 i tabelę
  kosztów - liczby są powtórzone świadomie, żeby README dało się czytać bez ADR-ów.

### Topologia wdrożenia (docelowa, nieuruchomiona)

`dq-contracts` to biblioteka wbudowana w obraz, nie osobna usługa. Usługa ingest idzie na
Cloud Run (`europe-central2`), obraz do Artifact Registry, loader batchowy jako Cloud Run Job
na tym samym obrazie, dane do BigQuery (`events`, `quarantine`), stan Terraforma docelowo do
bucketa GCS z wersjonowaniem. Pierwszy `apply` jest dwuetapowy: rejestr i zasoby, potem push
obrazu, na końcu usługa Cloud Run — bo jej definicja wskazuje na konkretny tag obrazu.
Szczegóły i diagramy: README, sekcja „Jak wyglądałoby wdrożenie".

### Tryb strict: co trzeba wiedzieć, zanim napiszesz kolejny kod

`PurchaseEvent` ma `strict=True`, a to znaczy co innego dla JSON-a i co innego dla obiektów
Pythona. Ścieżka produkcyjna (Pub/Sub, pliki NDJSON) idzie przez `model_validate_json` i tam
`Decimal`, `datetime`, `UUID` oraz `StrEnum` przyjmują tekstową reprezentację. Ścieżka
obiektowa (`model_validate`) wymaga instancji dokładnie tych typów — łańcuch `"PLN"` dla pola
`Currency` zostanie odrzucony z kodem `is_instance_of`.

Wniosek dla kolejnych etapów: generator buduje zdarzenia z natywnych typów, pipeline czyta
JSON. Testy kontraktu idą przez JSON, bo to odwzorowuje produkcję.

### Generator: co trzeba wiedzieć przed etapami 4-5

- `GeneratedRecord.fault` to odpowiedź wzorcowa: `None` = kontrakt musi przyjąć,
  inaczej `FAULT_CATALOG[fault].expected_reason`. Raport z pipeline'u porównuj z nią.
- Kolejność w pipelinie: najpierw walidacja schematu, dopiero potem
  `TransactionRegistry.register` — tylko dla rekordów, które przeszły. Odwrotnie rejestr
  zapamiętałby ID rekordu odrzuconego, a późniejszy poprawny rekord z tym ID zostałby
  fałszywie uznany za duplikat (wzorzec: `tests/datagen/helpers.py`).
- `future_timestamp` jest względny wobec `--reference-time`; plik walidowany później
  niż ~1 h po wygenerowaniu traci część tych błędów. W testach podawaj czas jawnie.
- `GeneratorConfig` jest celowo lax (wejście z CLI), kontrakt strict — nie ujednolicaj.

## Reguły walidacji do pokrycia

Każda z poniższych musi mieć test pozytywny i negatywny oraz odpowiadający jej wariant
w generatorze:

- wartość transakcji niezgodna z sumą pozycji (cross-field, `model_validator`)
- znacznik czasu z przyszłości
- ujemna lub zerowa cena albo ilość
- waluta spoza dozwolonego zbioru
- duplikat identyfikatora transakcji
- brak pola wymaganego lub pole nadmiarowe (`extra="forbid"`)
- string tam, gdzie ma być liczba — różnica między trybem strict a lax

## Ustalenia, których nie widać w kodzie

- **Infrastruktura powstaje „na sucho".** Terraform ma być kompletny i zwalidowany, ale
  właściciel repo świadomie nie uruchamia `apply` ani nie zakłada projektu GCP. Walidacja bez
  konta: `terraform fmt -check`, `init -backend=false`, `validate` — przez obraz
  `hashicorp/terraform` w Dockerze, bo Terraform nie jest zainstalowany w systemie.
- **Projekt GCP też tworzy Terraform**, nie klikanie w konsoli. Nad każdym blokiem komentarz
  po polsku wyjaśniający, co i w jakiej kolejności trzeba zrobić, żeby to odpalić.
- W README punkt „Demo na GCP" zostaje jawnie oznaczony jako niewykonany. Nie deklaruj, że
  pipeline przeszedł na prawdziwym GCP.
- Środowisko lokalne: brak Javy, więc emulator Pub/Sub idzie przez Dockera
  (`google-cloud-cli:emulators`), nie przez `gcloud components`.
- Emulator BigQuery (`goccy/bigquery-emulator`) został rozważony i odrzucony na rzecz
  lokalnego sinka JSONL + DuckDB; uzasadnienie: `docs/adr/0001-*.md`.
- **Powtórka ≠ duplikat:** ten sam `transaction_id` z identycznym odciskiem treści
  (BLAKE2b z `model_dump_json()`) to powtórka - bez zapisu i bez kwarantanny; z inną treścią
  to duplikat. Pamięć żyje w `dq_pipeline.validation.TransactionLedger`, nie w kontrakcie -
  `TransactionRegistry` z `dq-contracts` zostaje dla zgodności, pipeline go nie używa.
- **Batch:** load = SHA-256 pliku, katalog `data/batch/loads/<sha16>/` publikowany jednym
  `os.replace`, manifest `_load.json` jako ostatni. `LocalJsonlSink` MUSI zapisywać postać
  kanoniczną (`model_dump_json()`), bo z niej liczony jest odcisk przy zasilaniu pamięci.
- **Terraform:** nazwy zasobów Pub/Sub i tabel pilnuje `tests/test_terraform_names.py`;
  pierwszy apply dwuetapowy przez `deploy_service`. Loadera batchowego jako Cloud Run Job
  świadomie NIE ma - chmurowa idempotentność wymaga load joba + `MERGE`, nie `rename`.
- **mypy i google.cloud:** importuj `import google.cloud.pubsub_v1 as pubsub_v1` (nie
  `from google.cloud import ...`), bo otypowany google-cloud-bigquery dzieli tę przestrzeń nazw.
- **Docker Desktop:** nigdy nie uruchamiaj go sam (`open -a Docker` wymaga zgody w
  ustawieniach). Gdy `docker info` pada - zgłoś i czekaj.
- **Semantyka ack/nack w ingest:** kwarantanna (także uszkodzony JSON) = 204/ack; awaria
  sinka = 5xx/nack → retry → dead-letter → redrive na temat, NIE do kwarantanny. Nie
  przywracaj starej wersji z README („zły JSON na dead-letter, dead-letter do kwarantanny").
- **Emulator Pub/Sub nie przenosi serii wiadomości na dead-letter:** po ~3 nieudanych
  rundach push staje (sprawdzone: odmowa połączenia i HTTP 500, świeża instancja;
  pojedyncza wiadomość przechodzi). Scenariusz redrive kładzie wiadomości na DLQ wprost.
  Emulator nie wysyła też `deliveryAttempt` i dubluje pola koperty (`messageId`/`message_id`).
- `google-cloud-pubsub` nie ma `py.typed` — override w mypy tylko dla `google.cloud.pubsub_v1`.
  Styk z klientem Google ma `pragma: no cover` i jest sprawdzany przez job CI `local-stream`.
- Testy pokazują `StarletteDeprecationWarning` (TestClient na `httpx`, Starlette chce
  `httpx2`). Przejście na `httpx2` czeka na decyzję właściciela repo — nie wyciszaj ostrzeżenia.

## Konwencje

- **Kod, nazwy, commity, opis repozytorium i topics po angielsku. Komentarze, docstringi,
  README i cała dokumentacja po polsku.** README jest wyłącznie polskie — to świadoma decyzja
  właściciela repo, nie przeoczenie.
- Commity w konwencji Conventional Commits, tytuł do 72 znaków.
- Nigdy nie commituj na `main`. Każda zmiana idzie przez branch (`feat/`, `fix/`, `chore/`,
  `docs/` + kebab-case) i pull request przez `gh pr create`, z opisem: co się zmienia, dlaczego,
  jak zweryfikować. Przed otwarciem PR uruchom `make check` i wklej wynik do opisu.
- Po scaleniu: `gh pr merge --squash --delete-branch`.
- **Komentarze piszemy gęsto, ale nierównomiernie.** W plikach konfiguracyjnych (TOML, YAML,
  Makefile, Terraform) komentujemy praktycznie każdą decyzję, łącznie z tym, co dana opcja
  robi — to wiedza, której nie da się odczytać z samego kodu, a projekt ma uczyć. W kodzie
  Pythona komentujemy decyzje i mechanizmy pydantic, nie składnię języka; docstring modułu
  wyjaśnia rolę pliku w całości, a nie parafrazuje nazwy klas.
- W Makefile komentarze stoją NAD celem. Linia wcięta tabem trafia do shella i wypisuje się
  na ekran przy każdym uruchomieniu.
- Kod uruchamiaj, zanim powiesz, że działa.
