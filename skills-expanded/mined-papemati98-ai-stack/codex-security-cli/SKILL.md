---
name: codex-security-cli
status: deprecated
replaced_by: simulate-attack
deprecation_date: 2026-09-02
description: DEPRECATED. Ten skill zostal zastapiony przez `simulate-attack`. Wspolne skille powinny byc migrowane do nowego skilla; skan chmurowy oficjalnym Codex Security CLI nie jest czescia tej warstwy. Nie instaluj juz tego skilla. Niezbedny runtime pozostaje zarchiwizowany w `references/runtime-manifest.json` i w `scripts/` tylko na potrzeby audytu historycznego.
---

# codex-security-cli (TOMBSTONE)

Ten skill jest wycofany. Jego miejsce zajmuje wspolny skill
`simulate-attack`, ktory:

- wykonuje ten sam read-only rekonesans,
- iteruje ograniczona liczbe prob wejscia z budzetem `max_iterations`
  oraz `max_fresh_tokens` z execution pool,
- zapisuje zredagowany raport pod `~/.agents/security-audits`,
- jawnie zabrania kasowania, mutacji, DoS, maila, platnosci, CRM,
  Billingo, kalendarza i publicznych integracji,
- zezwala tylko na cele klasy `TEST`, `STAGING` lub `isolated_candidate`,
- nigdy nie odpala aktywnego ataku na `PROD` (owner_approval wymagany
  per system; w tej wersji odrzucany).

## Dlaczego tombstone, a nie ciche usuniecie

`global/codex/skills-ownership.json` deklaruje ten skill jako
`bootstrap_owned`. Usuniecie bez sladu pogubiloby aktywne kopie i
referencje w trzech miejscach: `security-audit` (historyczny
prompt), `security-audit-cycle` (preflight `codex-security-cli`),
oraz w skryptach rollbacku `scripts/rollback_active_copies.ps1`. Tombstone
zachowuje te referencje jako deprecated, ale prowadzi czytelnika do
`simulate-attack` jako jedynego zrodla prawdy.

## Migracja

1. Otworz `global/codex/skills/simulate-attack/SKILL.md`.
2. Uzyj `preflight` przed `run`, aby sprawdzic budzet i klase celu.
3. Raporty sa zapisywane w tym samym kontenerze
   `~/.agents/security-audits/<project-id>/audits/<run-id>/` co audyt
   cykliczny; nie powstaje drugi licznik 14-dniowy.
4. Manifest wlasnosci w `global/codex/skills-ownership.json` zostal
   zaktualizowany tak, aby `codex-security-cli` mial `status: deprecated`
   oraz wskazanie `replaced_by: simulate-attack`.

## Aktywne kopie i rollback

`scripts/rollback_active_copies.ps1` pozostaje zarchiwizowany. Sluzy
wylacznie do wycofania aktywnych kopii w `~/.codex/skills`,
`~/.claude/skills`, `~/.agents/skills`, `~/.gemini/config/skills` i
`~/.grok/skills` w kierunku `security-audit` + brak
`codex-security-cli`. Nie uruchamiaj go, jesli juz wykonano migracje
do `simulate-attack`.

## Manifest runtime

`references/runtime-manifest.json` zostaje bez zmian. Sluzy do
archiwizacji wersji `0.1.1` pakietu `@openai/codex-security` na
potrzeby audytu historycznego lub `verify_runtime` w testach, ktore
sprawdzaja integralnosc. Nie uzywaj tego manifestu do nowych instalacji.

## Pliki archiwalne (deprecated, read-only)

- `scripts/codex_security_safe.py` - wrapper runtime (archiwalny).
- `scripts/install_runtime.ps1` - instalator Node.js + pakiet
  (archiwalny).
- `scripts/rollback_active_copies.ps1` - rollback aktywnych kopii
  (archiwalny).
- `references/security-policy.md` - polityka runtime (archiwalna).
- `references/runtime-manifest.json` - manifest runtime (archiwalny).
- `references/package-audit.md` - audyt pakietu (archiwalny).
- `tests/test_codex_security_safe.py` - testy runtime (archiwalne;
  przechodza tylko jesli pakiet jest nadal zainstalowany na maszynie).

Te pliki sa utrzymywane, aby migracja, rollback i audyt historyczny
mialy ciag referencji. Nie sa uruchamiane przez `bootstrap.ps1` ani
przez `simulate-attack`. Nowe zadania nie powinny z nich
korzystac.
