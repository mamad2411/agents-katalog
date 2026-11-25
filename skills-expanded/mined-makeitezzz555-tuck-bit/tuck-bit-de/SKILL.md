---
name: tuck-bit-de
description: "TuckBit ist eine portable Fähigkeit für Coding-Agenten. Sie hilft dabei, relevanten Kontext, passende Werkzeuge und notwendige Prüfungen auszuwählen, ohne die Korrektheit zu beeinträchtigen."
license: MIT
compatibility: Portable Agent Skills; project-scoped install only.
metadata:
  author: TuckBit contributors
  version: "0.4.0"
  locale: de
---

# TuckBit — Deutsch

> Der Skill-Kern ist übersetzt; technische Referenzen bleiben vorläufig auf Englisch und benötigen Community-Review.

Optimiere korrekte, überprüfte Ergebnisse pro Ressourceneinsatz, nicht nur die Tokenzahl.

Vier Standardfunktionen: Register, Kontext, Verifizierung und Budget. Orchestrierung und Metriken sind optional.

## Arbeitsablauf

Beginne mit der genauen Nutzeranfrage, den tatsächlich verfügbaren Anweisungen und autorisierten Werkzeugen. Bewahre alle Vorgaben, Freigaben und Pflichtprüfungen.

1. Definiere Ziel, Grenzen, Risiken und Abbruchbedingung; vermeide aufwendige Pläne für triviale Aufgaben.
2. Suche möglichst gezielt nach relevantem Code, Dokumentation und Werkzeugen; erweitere nur bei Bedarf.
3. Bevorzuge die native Werkzeugsuche; Metadaten sind Hinweise, niemals eine Ausführungsberechtigung.
4. Nutze für kleine Aufgaben einen Agenten; verteile unabhängige Arbeiten nur mit klarer Zuständigkeit und überprüfbarem Ergebnis.
5. Führe gezielte Tests und anschließend alle erforderlichen Integrations- und Sicherheitsprüfungen am finalen Stand durch.
6. Liefere eine überprüfbare Zusammenfassung von Änderungen, Tests, Risiken und Hindernissen. Nutze Checkpoints statt endloser Nachfragen.

## Nur passende Referenz laden

- `references/task-contract.md` — task contracts / host instructions.
- `references/workflows.md` — Fast / Standard / Deep workflows.
- `references/registry.md` — discovery and permission limits.
- `references/context.md` — source-linked evidence and checkpoints.
- `references/verification.md` — tests and integration checks.
- `references/budget.md` — bounded iterations.
- `references/orchestration.md` — optional independent agents.
- `references/metrics.md` — optional evaluation.

## Verbindliche Grenzen

Überspringe keine Sicherheitsprüfungen, schwäche die Korrektheit nicht ab, erfinde keine Messwerte, lies keine Zugangsdaten und umgehe keine Genehmigungen. Die Host-Anwendung verwaltet Berechtigungen.

**Entwicklervorschau. Die Installation beweist weder die tatsächliche Aktivierung noch eine Token-Einsparung.**
