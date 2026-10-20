---
name: ac-to-test-scaffold
description: Read-only Test-Scaffolding aus dem Konzept. Erzeugt FAILING Test-Skelette aus den Akzeptanzkriterien-Tabellen eines Konzepts (eine Test-Methode je AC, Kriterium als Kommentar) — Tests AUS der Spec, nicht aus dem Code (TDD-First). Use vor der Implementierung („TDD-First", „Tests aus dem Konzept", „Test-Skelette generieren").
---

# ac-to-test-scaffold (CDP5 T1-Gate, §11.7/§27.4)

Die **TDD-First-Brücke**: liest die `## UC-…` + Akzeptanzkriterien-Tabellen und druckt **failing** Test-Skelette (je AC eine Methode, `markTestIncomplete`/`throw`, Kriterium als Kommentar). So entstehen Tests **aus dem Konzept** statt rückwärts aus dem Code (§11.5-Anti-Pattern vermieden). **Read-only:** druckt auf stdout, der Dev/Orchestrator legt die Dateien an.

## Aufruf

```bash
node "${CLAUDE_PLUGIN_ROOT}/skills/ac-to-test-scaffold/ac-to-test-scaffold.mjs" --konzept=<konzept.md> [--lang=php|js]
```

Exit: `0` Skelette erzeugt · `1` keine AC gefunden (erst `konzept-lint`) · `2` Nutzungsfehler.

## Konvention

AC-Zeilen `| AC-N | Kriterium | Test-Typ | Klasse::methode | Status |` (vgl. CDP5 §11.7). Test-Klasse/-Methode aus der `Class::method`-Spalte; fehlt sie, wird aus UC-/AC-ID abgeleitet. `--lang=php` (PHPUnit, Default) oder `js` (node:test). Danach: `tdd`-Loop (rot → grün je AC); `konzept-mapper` prüft später, ob die Klassen real existieren.
