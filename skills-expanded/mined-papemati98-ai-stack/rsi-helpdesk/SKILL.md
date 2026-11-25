---
name: rsi-helpdesk
description: "Helpdesk samonaprawy AI stacku (RSI). Uzyj, gdy w trakcie zadania zawodzi element samego stacku - adapter lub model we Fleet, Agent CLI, Office, Knowledge Hub, wspolny skill, launcher, runtime - i obchodzisz to innym modelem lub narzedziem: zglos usterke jednym poleceniem i wracaj do zadania. Uzyj tez, gdy uruchomiono Cie jako sesje naprawcza RSI Helpdesk albo pytaja o otwarte zgloszenia stacku. Nie dotyczy bledow aplikacji projektowych ani wyczerpanych limitow."
---

# RSI Helpdesk

Stack jest uzywany przez wiele sesji naraz. Gdy cos w nim nie dziala, wykonawca
zwykle obchodzi problem i idzie dalej, co jest dobre dla jego zadania. Usterka
zostaje jednak w stacku i kolejne sesje traca na nia czas. Przyklad z
2026-10-13: Fleet odrzucal raporty Muse 1.4.6 w 12 z 13 runow, wykonawcy
przelaczali model, a nikt tego nie zglosil.

Helpdesk rozdziela te dwie rzeczy: wykonawca **zglasza i wraca do pracy**, a
osobna sesja w tle **naprawia**. Bez czekania na Mateusza i bez wydluzania
biezacych zadan.

Skrypty: `scripts/helpdesk.py` (kolejka), `scripts/resolve_cycle.py` (cykl) i
`scripts/triage_cycle.py` (triaz oraz kolejka decyzji dla wlasciciela).
Stan: `~/.agents/helpdesk/`. Ogloszenia: kanal Office `#rsi-helpdesk` (inny niz helpdeski projektow `helpdesk-*`).

### Terminy triazu i owner-queue

- Triaz W -> D uruchamia sie po 24 h, gdy jest co najmniej `min_untriaged`
  nieprzypisanych zgloszen (domyslnie 10), albo po 7 dniach, gdy jest co
  najmniej jedno takie zgloszenie.
- Owner-queue jest sprawdzana przy kazdym cyklu resolvera. Uruchamia sie, gdy
  co najmniej jedno nie-T2 zgloszenie `candidate` lub `needs-owner` ma ponad
  24 h, a ostatni udany owner-queue byl ponad 6 h temu.
- Zgloszenia T2 pozostaja poza decyzjami D i sa wymieniane w
  `last_result.t2_waiting`; owner-queue nie zmienia ich statusu, a triaz nie
  zmienia ani statusu, ani priorytetu zgloszenia T2 - zostawia je otwarte
  i raportuje wlascicielowi.
- Odpowiedz Dyrektora liczy sie tylko z pol `handoff.summary`, `handoff.text`
  i `public-handoff.json` (ten sam czytnik dla triazu i dla owner-queue).
  Pola sprawdzane sa po kolei, a werdykt bierze sie z pierwszego pola, ktorego
  pierwsza niepusta linia zaczyna sie od `ZATWIERDZAM Z POPRAWKAMI`,
  `ZATWIERDZAM` albo `ODRZUCAM`; pole z wstepem jest pomijane, nie blokuje
  kolejnych pol. `NIE ZATWIERDZAM` w pierwszej linii dowolnego pola i brak
  werdyktu to odrzucenie bez zmian. Runner, ktory nie zwrocil statusu
  sukcesu (`completed`/`CANDIDATE`), nie zmienia zadnego zgloszenia.
- Wynik owner-queue jest zapisywany osobno w `owner_queue_last_result`, wiec
  raport triazu nie nadpisuje raportu kolejki wlasciciela.

Reczne komendy:

```bash
python "<skill>/scripts/triage_cycle.py" run          # oba cykle wedlug osobnych terminow
python "<skill>/scripts/triage_cycle.py" owner-queue # uruchom owner-queue teraz
python "<skill>/scripts/triage_cycle.py" status       # terminy, liczebnosci i wynik
```

## Zglaszajacy (kazdy agent)

Zglos, gdy element stacku zawodzi w sposob, ktory nie minie sam i ktory
obchodzisz albo przez ktory tracisz czas:

```bash
python "<skill>/scripts/helpdesk.py" file --component fleet-adapter:muse \
  --symptom "Fleet odrzuca handoff Muse: No structurally valid handoff, exit 0" \
  --evidence run-20261013T003226Z-4c1d475de6 --impact "implement Muse FAILED" \
  --workaround "przelaczylem na Codex" --reporter <twoje-agent-id>
```

- `component` to element stacku: `fleet-adapter:<agent>`, `fleet`, `agent-cli`,
  `office`, `hub`, `skill:<nazwa>`, `launcher:<nazwa>`, `runtime:<nazwa>`.
  Usterka jednego modelu: dodaj `--model <id>`.
- Ta sama usterka laczy sie w jedno zgloszenie z licznikiem; zglos ponownie bez
  obaw, dopisze dowod. Nowe zgloszenie samo uruchamia cykl naprawczy w tle.
- To trwa minute. Nie diagnozuj i nie naprawiaj usterki stacku w swoim zadaniu,
  chyba ze ta naprawa jest Twoim zadaniem albo bez niej nie da sie go wykonac.
- Nie zglaszaj: wyczerpanego limitu z resetem, chwilowej awarii dostawcy,
  bledu wlasnego kodu, bledow aplikacji projektowych (te ida do zespolu
  projektu). Nie wpisuj sekretow, danych klientow ani tresci promptow.

Skaner bez modeli (`helpdesk.py scan-fleet`, uruchamiany w kazdym cyklu) sam
zglasza powtarzalne porazki Fleet: ten sam agent, model i przyczyna co najmniej
3 razy w 24 h w co najmniej 2 workspace'ach. Limity i awarie dostawcy pomija.
Logi stderr czyta tylko z katalogow samego stacku, nigdy z projektow klientow.

## Sesja naprawcza (Resolver)

Uruchamia ja `resolve_cycle.py` wylacznie jako zadanie Harmonogramu
`AgentStack RSI Helpdesk` (co 2 h i na zadanie po nowym zgloszeniu), przez
HiddenLaunch na prywatnym pulpicie, wiec nic nie otwiera okien. Jedna sesja
naraz, rotacja wykonawcow (Codex Sol; Claude Fable tylko w trybie rozliczen
`normalny`), limit czasu rowny claimowi. Dostajesz jedno zgloszenie juz
zajete na Ciebie.

Tor K/W (`fleet-k`, dodany 2026-10-22): w rotacji, ale tylko dla zgloszen
wspolnych skilli (`components` w konfiguracji). `scripts/fleet_resolver.py`
deterministycznie prowadzi jedna pare `todo_pair` (maker Kierownik, recenzent
innego rodowodu; Fleet pilnuje kwalifikacji i denylisty) w odlaczonym
worktree, po zielonej bazie testow skilla. Wynik: `candidate --release`
(decyduje Dyrektor albo Mateusz, tor niczego nie wdraza ani nie zamyka) albo
`open` z notatka. Przy `max_parallel` > 1 cykl uruchamia rownolegle tylko
rozlaczne komponenty i najwyzej jeden resolver wdrazajacy (`deploys`).

1. Przeczytaj [references/resolver.md](references/resolver.md) i wykonaj go.
2. Cel: usterka naprawiona i sprawdzona w aktualnym stacku albo uczciwie
   zamknieta z powodem. Liczba plikow, raportow i testow nie jest celem.
3. Status zgloszenia zmieniaj tylko przez `helpdesk.py update`, i tylko dopoki
   trzymasz claim. Kazda zmiana ma krotka notatke z dowodem. `--force` jest
   wylacznie dla Mateusza przy recznej korekcie.

## Pamiec napraw (dodane 2026-10-17)

`scripts/repair_history.py` prowadzi pochodny indeks per domena pod
`~/.agents/helpdesk/history-index/<domena>.json`, zrodlem prawdy pozostaje
`tickets/`. Tagi `domain` / `canonical_component` wyliczaja sie z prefiksu
`component` (`fleet-adapter` i `fleet` → `fleet`, `skill` → `skills`,
`launcher` → `launchers`, itd.); legacy zgloszenia dostaja je na zadanie
bez przepisywania pliku. Zwykly lookup czyta indeks jednej domeny; pierwszy
brakujacy indeks powstaje lokalnie ze starszych zgloszen, bez wysylania ich
modelowi. Uszkodzony indeks daje ostrzezenie i czesciowy odczyt awaryjny,
nigdy ciche "pusta historia".

- `python helpdesk.py related <ticket>` — rzutowanie dla resolvera (≤5 wpisow,
  ≤4096 B UTF-8 z metadanymi; `trust=untrusted` + caveat; bez surowych
  sciezek/logow; bez skanowania innych zgloszen dzieki bezposredniemu 12hex/prefiksowemu ID).
- `python helpdesk.py update ... --lesson "<krotki wniosek>"` — append-only
  source lessons (wersja/data/by/status; pelna historia zachowywana w zgloszeniu,
  limitowane wylacznie rzutowanie modelowe), powiazany z biezacym claimem; przezywa
  reopen. Wniosek dopisuje sie do istniejacego update, bez osobnej komendy.
- `python helpdesk.py update ... --lesson "<tekst>" --lesson-context '{"target":"harness","outcome":"effective","applicability":"python 3.13+ / agent-fleet-suite >=0.9.73"}'`
  — opcjonalny, scisle ograniczony obiekt RSIFlow-like (`target` ∈
  `harness|model|artifact`, `outcome` ∈ `effective|ineffective|unknown`,
  krotki `applicability` opisujacy wersje/stan runtime). Tylko z `--lesson`; nieznane
  klucze, bledne typy, sekrety i nadmiar bajtow odrzucane bez zapisu. Kontext jest
  dowodem doradczym (nie autorytetem, nie poleceniem), przezywa reopen i jest
  przepuszczany przez rzutowanie related-history. Wniosek `ineffective` zostaje
  obok `effective`: zadnego wnioskowania sukcesu ze statusu zgloszenia ani
  powtorzen, zadnego kasowania wczesniejszych lessons.
- Resolver prompt automatycznie dostaje blok `<related-history>` jako
  niezaufane dane; sekcja instrukcji mowi wprost: stosuj wnioski tylko po
  zywej weryfikacji wersji/stanu biezacego stacku. Rzutowanie zachowuje
  przynajmniej jeden wniosek z `outcome=ineffective|unknown` obok najnowszego,
  nawet jesli trzeba obciac pozostale wnioski pod 5 wpisow / 4096 B; udana
  liczba zaleglych zgloszen nie wymazuje wczesniejszej porazki.

## Granice

Decyzja Mateusza 2026-10-13. Sesja naprawcza sama wdraza poprawki odwracalne
wewnatrz AI stacku (Fleet, Agent CLI, Office, Hub, wspolne skille, adaptery CLI,
launchery) po testach, niezaleznym ACCEPT innego rodowodu i kanarku, z gotowym
rollbackiem. Sama nie robi: sekretow, kasowania, IAM i uprawnien, domen i
tuneli, aplikacji projektowych i klientow, nowych platnych kosztow, zmian
logiki biznesowej. Takie zgloszenie dostaje `needs-owner` z jednym
konkretnym pytaniem.

Tryb wdrozenia ustawia `"deploy_mode"` w `~/.agents/helpdesk/config.json`:
`candidate` (domyslnie) konczy na przejrzanym kandydacie, `auto` pozwala
wdrazac. Sesja dziala jako uzytkownik Mateusza z pominieciem sandboxu CLI;
granice sa proceduralne (prompt, ta procedura, bramki instalatorow), nie
techniczne. Dowodow nie czyta z katalogow projektow i klientow.

Wylacznik: plik `~/.agents/helpdesk/STOP` albo `"enabled": false` w
`~/.agents/helpdesk/config.json`. Cykl wtedy nic nie uruchamia; nieczytelny
config tez blokuje uruchamianie. Sesja w toku sprawdza wylacznik przed
wdrozeniem. Zatrzymanie harmonogramu: `Disable-ScheduledTask -TaskName
"AgentStack RSI Helpdesk"`.

## Podglad

```bash
python "<skill>/scripts/helpdesk.py" list          # aktywne zgloszenia
python "<skill>/scripts/helpdesk.py" stats --days 7   # metryki kolejki za 7 dni
python "<skill>/scripts/helpdesk.py" set-priority <ticket> --priority P1 --by <id> --note "<powod>"  # priorytet zgloszenia
python "<skill>/scripts/resolve_cycle.py" status   # sesje naprawcze i konfiguracja
python "<skill>/scripts/resolve_cycle.py" dry-run  # co cykl by zrobil, niczego nie zapisuje
python "<skill>/scripts/triage_cycle.py" status    # stan triazu i owner-queue
```

Triaz W (wspolny) przygotowuje propozycje, a D (Dyrektor) zatwierdza albo
koryguje je jednym zapytaniem. Zwykle dylematy techniczne w owner-queue
rozstrzyga D. Sprawy T2 czekaja na Mateusza; nie trafiaja do decyzji D.
