---
name: security-audit-cycle
description: Uzyj na poczatku istotnej pracy nad aktywnym systemem lub repozytorium, aby sprawdzic, czy istnieje ukonczony audyt bezpieczenstwa z ostatnich 14 dni. Brak lub przeterminowanie audytu oznacza zalegle utrzymanie; nie blokuje samo lokalnej poprawki. Realna zmiana IAM/ekspozycji/granic zaufania, krytyczna luka lub duzy kandydat produkcyjny wymaga stosownego audytu/testow przed aktywacja. Bramka eksponuje takze wyzwalacze `next_substantive_work` i `pre_production_release_candidate` dla kontrolowanego, read-only skilla `simulate-attack`; nie tworzy drugiego licznika 14-dniowego. To nie jest audyt skilla ani automatyczna zgoda na skan chmurowy.
---

# Security audit cycle

Ten skill zarzadza cyklem audytu calej aplikacji lub systemu. Jest oddzielny od:

- `audit-skills` - kontrola obcego skilla przed instalacja,
- `security-audit` - recenzja biezacej zmiany lub waskiego zakresu,
- `simulate-attack` - kontrolowana, read-only eskalacja adversarial
  dla przeterminowanego audytu lub kandydata produkcyjnego.

## Obowiazkowy start

1. Rozwiaz rzeczywista sciezke projektu. Nie uzywaj odziedziczonego `cwd`, gdy
   uzytkownik wskazal inny katalog.
2. Przeczytaj projektowe `AGENTS.md` i `APP_PROFILE.md`, jezeli istnieja.
3. Uruchom bramke:

```powershell
python "$env:USERPROFILE\.agents\skills\security-audit-cycle\scripts\security_audit.py" status `
  --project "<pelna-sciezka>"
```

4. Interpretuj wynik:
   - `AUDIT_FRESH` - kontynuuj prace i podaj identyfikator ostatniego audytu.
   - `AUDIT_REQUIRED` - zapisz potrzebe utrzymaniowego audytu. Sam uplyw14dni
     nie blokuje lokalnej poprawki. Zmiana IAM, granic zaufania, ekspozycji sieci,
     znana krytyczna luka lub duzy kandydat produkcyjny wymagaja stosownych
     testow/audytu przed aktywacja. Review security aktualnej zmiany pozostaje.
   - `NOT_ACTIVE` - nie wymuszaj audytu tylko dlatego, ze katalog istnieje.
5. Kod wyjscia `3` oznacza zalegle utrzymanie, nie awarie skryptu ani samodzielna blokade lokalnej poprawki. Rodzic sprawdza stan raz; wykonawcy dostaja istotny wynik.

## Wyzwalacze eskalacji adversarial

Bramka 14-dniowa jest jedynym zrodlem swiezosci. Pole
`adversarial_triggers` w wyniku `status` wskazuje, czy eskalacja do
`simulate-attack` jest wymagana:

- `next_substantive_work: true` - audyt starszy niz14dni: sygnal utrzymania
  wspolny z `AUDIT_REQUIRED`, bez automatycznej eskalacji kazdej lokalnej poprawki.
- `pre_production_release_candidate: true` - przed duzym wydaniem
  produkcyjnym; wymaga izolowanego kandydata lub stagingu, nigdy PROD.

Stan wyzwalaczy mozna odczytac bez zapisu:

```powershell
python "$env:USERPROFILE\.agents\skills\security-audit-cycle\scripts\security_audit.py" adversarial-status `
  --project "<pelna-sciezka>" `
  --trigger next_substantive_work
```

Kod wyjscia `0` oznacza wymagana eskalacje, `4` - brak eskalacji.
Wynik nie zapisuje nic w ledgerze, kontenerze raportu ani w
repozytorium.

## Audyt lokalny

```powershell
python "$env:USERPROFILE\.agents\skills\security-audit-cycle\scripts\security_audit.py" run-local `
  --project "<pelna-sciezka>" `
  --agent "codex" `
  --classification "confidential" `
  --scope "pelny projekt, read-only"
```

Audyt:

- nie modyfikuje projektu,
- nie czyta `.env`, kluczy, baz danych, logow, uploadow ani danych klientow,
- nie wypisuje dopasowanych sekretow,
- nie uruchamia instalatorow, migracji, deployu ani uslug,
- zapisuje wynik w `%USERPROFILE%\.agents\security-audits`,
- nie uruchamia wycofanego `codex-security-cli`; jego tombstone wskazuje
  `simulate-attack`,
- nigdy automatycznie nie wysyla kodu do OpenAI ani innej chmury.

Skan chmurowy wymaga osobnej, jawnej zgody na repozytorium, klasyfikacje danych,
wyslanie kodu i limit kosztu. Brak zgody oznacza lokalny baseline.

## Reczna weryfikacja

Automatyczny baseline jest dowodem wykonania kontroli, ale nie dowodem pelnego
bezpieczenstwa. Zweryfikuj recznie:

- auth, role, IDOR i dostep do danych innych uzytkownikow,
- ekspozycje portow, tuneli, CORS, debug i panele administracyjne,
- walidacje wejscia, SQL/command/path injection, XSS i deserializacje,
- logowanie danych klientow, tokenow i pelnych tresci,
- konfiguracje produkcyjna, backup, recovery i aktualnosc zaleznosci.

Findings podawaj z severity, `plik:linia`, dowodem bez sekretu, rekomendacja i
statusem false positive. Nie naprawiaj ustalen bez zgody, jesli uzytkownik prosil
o audyt.

## Raport i slad

Po uruchomieniu zawsze podaj:

- `audit_id`,
- narzedzie/agent,
- projekt i zakres,
- czy kod opuscil komputer,
- werdykt `PASS`, `REVISE` albo `NO-GO`,
- liczbe findings wedlug severity,
- pelna sciezke do `REPORT.md`,
- date kolejnego audytu.

Archiwum jest poza repozytorium, aby poufne ustalenia nie trafily do commita.
Nie kopiuj raportu do projektu bez jawnej decyzji wlasciciela.

## Audyt przez inne narzedzie

Prompty dla Codex Desktop, Claude Code Desktop i Antigravity sa w
`references/desktop-prompts.md`. Zewnetrzny audytor ma tryb read-only, bez web,
bez sekretow, bez edycji i bez deployu. Wynik mozna dolaczyc:

```powershell
python "$env:USERPROFILE\.agents\skills\security-audit-cycle\scripts\security_audit.py" attach-review `
  --project "<pelna-sciezka>" `
  --audit-id "<audit-id>" `
  --agent "claude" `
  --source "<plik-wyniku-audytora>"
```

Pelny standard, ograniczenia i model katalogow sa w
`references/audit-standard.md`.
