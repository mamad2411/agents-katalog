---
name: konzept-const-sync
description: Read-only T1-Gate gegen Konstanten-Drift zwischen Konzept-Prosa und Code-Spec. Difft numerische Konstanten in einem Konzept-Dokument (Tier-Skalen, benannte Schwellen, Inline-Arithmetik) gegen die Single Source of Truth (`rules.mjs` `DEFAULT_SPEC`) und optional `conformance.mjs`. Schließt die Fehlerklasse „Konstante in Prosa ≠ Code", die grüne Tests UND Adversarial-Audits systematisch übersehen. Use bei „Konstanten gegen Spec prüfen", „const drift", „sourceTier/Schwellen-Drift", VOR Konzept-Merges mit Zahlenwerten.
---

# konzept-const-sync (CDP5 T1-Gate)

## Warum

Aus den Konzept-Fehlerfunden 2026-05 (NSAI-Edge K1/K2): eine in `rules.mjs` definierte `sourceTier`-Skala wurde im Konzept-Text (UC-MS) mit **anderer** Nummerierung wiederholt (`behoerde=4` statt `5`, Phantom-Tier `audit=6`), und ein AUTH_FLOOR-Beispiel rechnete falsch (`full × fachquelle = 3000`, aber als „erreicht 4500" deklariert). Beide hätten eine PHP-Re-Implementierung **nach dem Text** in die Paritäts-Drift geführt.

Diese Klasse ist tückisch: **grüne Tests lesen nur `rules.mjs`** (sehen den Text nie), **Adversarial-Audits prüfen nur Verhalten** (sehen die Prosa nie). Nur ein Diff Text↔Spec fängt sie — deterministisch, in 0 LLM-Token.

## Aufruf

```bash
node "${CLAUDE_PLUGIN_ROOT}/skills/konzept-const-sync/konzept-const-sync.mjs" \
  --konzept=<KONZEPT.md> --spec=<rules.mjs> [--conformance=<conformance.mjs>] [--json]
```

Exit: `0` konsistent · `1` Drift gefunden · `2` Nutzungsfehler.

Die Spec muss `export const DEFAULT_SPEC = {...}` führen (dynamic import). `conformance.mjs` (optional) wird zusätzlich gegen `rules.mjs` gespiegelt (`QUORUM_CONSTANTS`, `DECAY_RECALL_CONSTANTS`).

## Checks (deterministisch, kein LLM)

1. **Annotation** `name(N)` — `name` muss in der Spec genau diesen Wert haben. Erlaubte Namen: `sourceTier`-Tiers, `quorumTrustRank`-Ränge (Quorum-Domäne gewinnt bei Namens-Kollision, z. B. `authoritative(1500)` statt trustFactor-`1000`), benannte Skalare.
2. **Tier-Deklaration** `name = N` / `name: N` — gegen `sourceTier`. Fängt die K1-Klasse (Skalen-Enumeration im Text).
3. **Skalar-Deklaration** `KEY = N` — **nur normative Verdikt-Schwellen** (`AUTH_FLOOR`/`quorumAuthFloor`, `quorumMulti`, `deleteThreshold`, `quarantineThreshold`, `contestedThreshold`, `beliefSharpness`).
4. **Decay-‰** `name … N ‰` (‰-verankert) — gegen `decayPerPeriod`.
5. **Arithmetik** `a × b = c` (rein numerisch UND annotiert `name(A) × name(B) = C`) — verifiziert das Produkt. Fängt die K2-Klasse.
6. **Phantom-Key** — ein unbekannter `name=N`-Token in einer Zeile mit ≥2 bekannten Tier-Namen (z. B. `audit=6`).

## Bewusste Scope-Grenzen (false-positive-Schutz)

- **Tunables** (`recallProtectionDays`, `recallDecayDivisor`, `reinforceDelta`, `demote*`, `trustAdjustMinEvidence`) werden NUR in Annotationsform `KEY(N)` geprüft — eine bare `recallProtectionDays = 0`-Zeile ist im Konzept ein **AC-Szenario** („=0 deaktiviert das Feature"), keine Default-Behauptung.
- **trustFactor** (`authoritative`=1000) wird NICHT in Deklarationsform geprüft (kollidiert mit `quorumTrustRank.authoritative`=1500); nur die Annotationsform der Quorum-Domäne gilt.
- **`recencyHalflifeDays`** (mit `∞`) wird nicht numerisch geprüft.
- **Autoren-Konvention (bewusst, nicht im Gate aufgeweicht):** wer einen FALSCHEN Wert als Beispiel beschreibt (Drift-Demo, „vorher/nachher"), schreibt ihn NICHT in `name=N`-/`name: N`-Deklarationsform — sonst flaggt das Gate ihn korrekt als Drift. Stattdessen Prosa-Form ohne `=`/`:`: „`behoerde` auf 4 statt 5". Das Gate bleibt strikt (fängt echte Drift zuverlässig); die Disziplin liegt beim Text.
- Bedeutungs-/Wortlaut-Korrektheit bleibt Judgment (`konzept-reviewer`). Befunde sind Hinweise, die der Main-Agent verifiziert (CDP5 §10.6).

## Warum dediziert (nicht in `konzept-model-api`)

`konzept-model-api` difft PHP-Enums ↔ OpenAPI-YAML. `konzept-const-sync` difft Konzept-Prosa ↔ JS-`DEFAULT_SPEC` — andere Quell-Domäne, anderer Parser. Getrennt gehalten, beide bleiben fokussiert.

## Beispiel-Output

```
konzept-const-sync — 1718 Zeilen, 25 getrackte Konstanten, 2 Drift-Stellen

  ✗ Z1035 [tier-decl] — `behoerde=4` ≠ sourceTier 5
  ✗ Z1047 [arithmetic] — 1000 × 3 = 4500 (korrekt: 3000)

2 Drift  ·  Exit 1
```
