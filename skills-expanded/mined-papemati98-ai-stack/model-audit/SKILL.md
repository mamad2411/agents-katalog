---
name: model-audit
description: >-
  Utrzymuje aktualna charakterystyke modeli AI dostepnych w lokalnych CLI.
  Uzyj przy jawnym audycie rynku albo potrzebnym odswiezeniu faktow o nieznanym
  lub zmienionym modelu/CLI. Zwykly dobor wykonawcy nie uruchamia pelnego audytu
  rynku tylko z powodu wieku raportu.
---

# Model audit: current facts needed for decisions

Rynek modeli fluktuuje tygodniami: dzis `Qwen 3.8 Max`, jutro `4` z inna charakterystyka;
Kimi przeskoczyl K2.7 -> K3 Max jedna aktualizacja CLI. **Routing delegacji oparty o stara
wiedze = zle decyzje kosztowe i jakosciowe.** Ten skill trzyma jeden plik prawdy o rynku.

Plik prawdy: **`MODEL-MARKET.md` w skonfigurowanym checkoutcie agent-stack**.

## Dobor wykonawcy (doprecyzowanie 2026-10-18)

Przy zwyklej delegacji uzyj aktualnych profili i potrzebnych dowodow.
Odswiez tylko nieznany model, zmieniony parametr albo fakt istotny dla tego
wyboru; nie caly rynek przed kazdym wezlem. Sam wiek raportu/benchmarku nie
uruchamia pelnego researchu ani petli zgody lub replanowania. Zachowaj
sprawdzenie rzeczywistej tozsamosci, zdolnosci, prywatnosci, dostepnosci i quoty
konkretnych kandydatow oraz denylist. Unknown nie oznacza zera ani pelnej puli.
Ponownie uzyj aktualnych dowodow w niezmienionej fali pracy.

## Pelny audyt rynku — tylko gdy jawnie zamowiony

Ponizsza procedura i siedmiodniowa swiezosc dotycza tego audytu rynku,
nie sa preflightem zwyklej delegacji.

### Resolver sciezki runtime
Uruchom przyklady z katalogu zawierajacego aktywny `SKILL.md` albo ustaw jawnie
`SKILL_ROOT` na ten katalog:

```powershell
if (-not $env:SKILL_ROOT) {
  throw 'Set SKILL_ROOT to the runtime-discovered directory containing this SKILL.md.'
}
$SkillRoot = (Resolve-Path -LiteralPath $env:SKILL_ROOT).Path
if (-not (Test-Path -LiteralPath (Join-Path $SkillRoot 'scripts\check_freshness.ps1'))) {
  throw 'SKILL_ROOT does not point to the active model-audit payload.'
}
```

### 1. Sprawdz swiezosc zamowionego audytu rynku
```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File (Join-Path $SkillRoot 'scripts\check_freshness.ps1')
```
- **exit 0 (`AUDIT_FRESH`)** → **KONIEC TEGO AUDYTU.** Nie rob researchu, nie pisz pliku.
  Jesli byles wywolany rownolegle z `agent-cli` — po prostu uzyj istniejacego `MODEL-MARKET.md`.
- **exit 10 (`AUDIT_STALE` / `AUDIT_MISSING`)** → przejdz do kroku 2.

Data czytana jest z pola `last_audit:` w naglowku pliku (nie z mtime — zeby zwykle skopiowanie
pliku nie udawalo swiezosci). Prog: 7 dni (`-MaxAgeDays` do nadpisania).

### 2. Research (tylko gdy STALE/MISSING)
Sprawdz **aktualny stan** dla kazdego dostawcy obecnego w lokalnych CLI:
Anthropic (Claude), OpenAI (Codex), Moonshot (Kimi), xAI (Grok), Google (Gemini/Antigravity), Alibaba (Qwen).

Dla kazdego ustal: **aktualna nazwa/wersja flagowego modelu kodujacego**, czym sie rozni od
poprzednika, mocne strony, slabe strony, klasa kosztu, czy wymaga nowszego CLI/planu.
Zrodla: oficjalne docs/changelogi dostawcow + `--version`/`models` lokalnych CLI. Preferuj
zrodla pierwotne; benchmarki traktuj ostroznie (marketing).

Zawsze zweryfikuj **lokalnie**, co realnie jest dostepne:
```powershell
kimi provider list          # modele Kimi (np. k3.1-pro = K3.1 Pro, klasa D od 2026-10-24)
& "$env:LOCALAPPDATA\agy\bin\agy.exe" models   # modele Antigravity
codex --version ; grok --version ; claude --version
& "$env:LOCALAPPDATA\qwen-code\bin\qwen.cmd" --version
```
Rozbieznosc „co ogloszono" vs „co mam w CLI" jest wazniejsza niz sama premiera — liczy sie to,
co realnie da sie zlecic.

### 3. Nadpisz `MODEL-MARKET.md`
Naglowek MUSI zawierac `last_audit: YYYY-MM-DD` (dzisiejsza data). Struktura:

```markdown
---
last_audit: 2026-07-21
audited_by: claude
---
# Rynek modeli - stan na 2026-07-21

| Dostawca | CLI | Aktualny model kodujacy | Zmiana vs poprzednio | Mocne strony | Slabe / limity | Koszt |
|---|---|---|---|---|---|---|
...

## Zmiany od ostatniego audytu
- ...
## Wplyw na routing delegacji (agent-cli)
- ...
```

### 4. Zsynchronizuj i zglos
- Plik zyje w origin `agent-stack` (nie w kopii narzedzia).
- Jesli zmiany sa istotne dla routingu — zaktualizuj macierz w skillu `agent-cli`.
- Wiedze trwala (np. „CLI X wymaga wersji Y dla modelu Z") wystaw jako propozycje do `llm-wiki`.

## Zasady
- **Nie zgaduj wersji z pamieci modelu** — zawsze research + lokalna weryfikacja CLI.
- **Nie rob audytu, gdy bramka mowi FRESH** — to marnowanie tokenow; taki jest cel bramki.
- Nie zapisuj w pliku sekretow, kluczy ani danych planu/rozliczen.
- Ceny/limity traktuj jako orientacyjne i oznaczaj jako zmienne.
