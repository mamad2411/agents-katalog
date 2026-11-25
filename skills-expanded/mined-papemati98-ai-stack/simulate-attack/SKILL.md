---
name: simulate-attack
description: Bounded, read-only adversarial audit for the existing security-audit-cycle gate. Uzywaj wylacznie na TEST, STAGING lub izolowanym kandydacie z danymi syntetycznymi, gdy audyt jest przeterminowany lub przed duzym wydaniem na produkcje. Petla wykonuje read-only rekonesans, ograniczone iteracyjne proby wejscia i zredagowany raport pod ~/.agents/security-audits. Brak jawnego limitu iteracji albo tokenow z execution pool, proba aktywnego ataku na produkcje bez zgody wlasciciela lub kazda proba destrukcji, maila, platnosci, CRM, Billingo, kalendarza czy publicznej integracji jest twardo odrzucana.
---

# simulate-attack

Kontrolowany, niedestrukcyjny, read-only red team dla aktywnego projektu.
Nie jest ogolnym skanerem, nie jest klientem Codex Security CLI i nie ma
dostepu do chmury. Wspoldzieli jedyny 14-dniowy ledger bramki
`security-audit-cycle` i nigdy nie tworzy drugiego licznika.

## Kiedy uruchomic

Uzywaj tylko wtedy, gdy spelni sie co najmniej jeden wyzwalacz:

- `security-audit-cycle status` zwrocil `AUDIT_REQUIRED` (audyt
  starszy niz 14 dni przy nastepnej istotnej pracy).
- Planowany release kandydata na produkcje przeszedl plan review, ale jeszcze
  nie trafil na PROD - wyzwalacz `pre_production_release_candidate`.

W obu przypadkach bramka wskazuje `escalation_required: true` oraz
`trigger_source: security-audit-cycle`; skill nie sprawdza daty sam.

## Twarde granice (fail-closed)

Kazde wywolanie musi spelniac wszystkie ponizsze warunki, inaczej konczy
sie `BLOCKED` z kodem wyjscia `4` i brakiem raportu:

1. Cel musi nalezec do klasy `TEST`, `STAGING` lub `isolated_candidate`.
   Slowo kluczowe `prod` w etykiecie celu lub fladze `live_customer_data`
   oznacza klase `PROD` i jest twardo odrzucane. `TEST` musi fizycznie lezec
   pod `~/.agents/security-audits/synthetic-targets`; `STAGING` i
   `isolated_candidate` wymagaja dokladnie jednego wpisu w lokalnym
   `target-registry.json`, ktory potwierdza dane syntetyczne i zgode na
   aktywne, niedestrukcyjne proby.
2. Wymagana jest jawna, pozytywna wartosc `max_iterations` oraz
   `max_fresh_tokens` z execution pool. Wartosc `0`, `None`, ujemna lub
   pusty budzet oznacza `BUDGET_EXHAUSTED` przed startem.
3. Ta wersja nie obsluguje produkcji ani realnych danych klienta: sa
   `PROD_LOCKED`; podanie `owner_approval` nie odblokowuje ich i jest odrzucane.
   Syntetyczny TEST oraz odizolowany, potwierdzony w rejestrze STAGING nie
   wymagaja tej flagi. Nadal musza przejsc atestacje celu, trigger i budzet.
4. W kazdej iteracji odrzucane sa: kasowanie plikow, podtrzymywany DoS,
   realna mutacja bazy lub plikow, wysylka maila, zapis do CRM, Billingo,
   platnosci, kalendarza, publicznej integracji i kazde inne polecenie
   spelniajace `deny_actions`.
5. Raport musi zostac zapisany pod `~/.agents/security-audits/<project-id>/audits/<id>/` i
   zostac zredagowany z kazdej znalezionej wartosci sekretu. Kiedykolwiek
   rozwiazana sciezka raportu wykracza poza `~/.agents/security-audits`,
   wywolanie konczy sie `PATH_VIOLATION` bez zapisu.
6. Model nigdy nie dostaje prawdziwego katalogu projektu. Kazda iteracja
   widzi wylacznie limitowany snapshot dozwolonych plikow tekstowych po
   redakcji; snapshot jest usuwany przed publikacja raportu.
7. Kazda iteracja musi zwrocic kompletny `REDTEAM_RESULT` z jawna decyzja
   `findings` albo `no_findings`, lista findings i niepustym dowodem. Brak
   albo blad schematu oznacza `BLOCKED`, nigdy domyslny `PASS`.

## Przeplyw

1. Rozwiaz `<skill-dir>/scripts/simulate_attack.py` przez `pathlib` na
   podstawie katalogu tego `SKILL.md`. Nie uzywaj `$env:USERPROFILE` ani
   `cwd` z innego zadania.
2. Uruchom `preflight` z obowiazkowymi parametrami. Brak `max_iterations`
   albo `max_fresh_tokens`, brak wyzwalacza lub cel spoza allowlisty
   koncza sie kodem `4` bez uruchamiania petli.
3. `run` wykonuje:
   1. `recon` - rekonesans read-only na dozwolonych klasach celu.
   2. `iterate` - do `max_iterations` prob wejscia, kazda na zredagowanym
      wyniku poprzedniej.
   3. `remediate` - generuje zredagowany raport z zaleceniami.
4. Kazde polecenie zwraca JSON z polem `state` (`PRECHECK_OK`,
   `RUNNING`, `PASS`, `REVISE`, `BLOCKED`, `BUDGET_EXHAUSTED`,
   `PROD_LOCKED`, `PATH_VIOLATION`).

## Komendy

```powershell
python "<skill-dir>\scripts\simulate_attack.py" preflight `
  --project "<pelna-sciezka-projektu>" `
  --target-class TEST `
  --target-name "synthetic-vault" `
  --max-iterations 2 `
  --max-fresh-tokens 2000 `
  --trigger next_substantive_work
```

Wynik `preflight`:

- `state=PRECHECK_OK, decision=proceed` - mozna wywolac `run`.
- `state=BLOCKED, decision=deny` - blad krytyczny, brak raportu.
- `state=BUDGET_EXHAUSTED, decision=deny` - brak execution pool.

`run`:

```powershell
python "<skill-dir>\scripts\simulate_attack.py" run `
  --project "<pelna-sciezka-projektu>" `
  --target-class TEST `
  --target-name "synthetic-vault" `
  --max-iterations 2 `
  --max-fresh-tokens 2000 `
  --trigger next_substantive_work
```

`status` zwraca aktualny stan bramki z czytelnym `escalation_required`
bez zapisu raportu.

```powershell
python "<skill-dir>\scripts\simulate_attack.py" status `
  --project "<pelna-sciezka-projektu>"
```

## Raport

Po `run` skill zapisuje:

- `metadata.json` - identyfikator, wyzwalacz, limity, werdykt.
- `recon.json` - wynik read-only rekonesansu.
- `iterations.jsonl` - zredagowane wyniki kazdej iteracji.
- `remediation.md` - rekomendacje dla wlasciciela.
- `REPORT.md` - podsumowanie z `audit_id`, werdyktem, liczba iteracji,
  liczba zredagowanych znalezisk, katalog raportu, kodem wyjscia.

Kazda linia w `iterations.jsonl` ma `redacted: true`. Polecenie `verify`
sprawdza, czy w zadnym pliku raportu nie pozostala wartosc sekretu.
Wynik adversarial zapisuje osobne `adversarial-latest.json` i
`adversarial-ledger.jsonl`; nie nadpisuje bazowego `latest.json`, wiec sam
nie zeruje 14-dniowej bramki baseline.

## Ograniczenia

- Skill nie wykonuje prawdziwego ataku, nie generuje ruchu sieciowego
  poza `localhost` i nie korzysta z internetu.
- Petla ma deterministyczne granice, walidator i sposob rozliczania; modelowy
  wynik oraz identyfikator uruchomienia moga sie roznic.
- `run` nie moze byc uzyty do wykonywania destrukcyjnych technik nawet
  jesli o to poprosi uzytkownik. Nalezy to eskalowac do Mateusza.
- Brak wsparcia dla `PROD` - dokladna specyfikacja jest w
  `references/attack-policy.md`.
