---
name: konfabulations-audit
description: Checks every external claim for evidence before the final answer and classifies it as supported, inferable, unverified, or do-not-claim. Companion to ultrathink-craftsmanship. Use when stating releases, APIs, prices, benchmarks, studies, product behavior, legal/medical/financial facts, claims about foreign codebases/files/org knowledge, or any numbers, names, dates, versions, quotes — and before any autonomous agent flow adopts a claim that could propagate.
---

# Konfabulations-Audit

Version: 1.0 · Companion zu `ultrathink-craftsmanship` (Phase 5)

## Zweck

Verhindere, dass unbelegte Behauptungen ("Konfabulationen") in eine Antwort, ein
Artefakt oder — besonders kritisch — in einen autonomen Agenten-Ablauf gelangen, wo sie
sich vervielfältigen und zur stillen Prämisse werden. Es ist ein **Verifikations-Gate
für Claims**, kein Stil- oder Reasoning-Gate: pro Behauptung gilt behaupten (mit Beleg),
abschwächen oder streichen.

## Grundsatz (nicht verhandelbar)

> Eine fehlende Information wird **niemals** "logisch" selbst geschlossen.
> Sie wird als Lücke markiert und — je nach Kontext — durch Quelle belegt,
> transparent als ungeprüft gekennzeichnet oder gar nicht behauptet.
> Das Schließen einer Wissenslücke durch plausibles Raten ist die Konfabulation,
> die dieser Skill abfängt.

## Wann verwenden

Aktiviere, sobald die Antwort eine **externe Behauptung** enthalten würde — aktuelle
Releases/Versionen/APIs/Preise/Limits/Benchmarks/Studien; nicht direkt beobachtetes
Produkt-/Systemverhalten; rechtliche/medizinische/finanzielle/regulatorische Fakten;
Aussagen über fremde Codebasen/Dateien/Dokumente ohne gelesene Quelle; jede konkrete
Zahl, jeder Name, jedes Datum, jede Version, jedes Zitat. Nicht nötig bei rein internem
Reasoning, eigener (als solche markierter) Meinung, oder vollständig aus dem
bereitgestellten Kontext Ableitbarem (dann Status `ableitbar` mit Verweis).

## Klassifikation (die vier Marken)

| Marke | Bedeutung | Handlung |
|---|---|---|
| `belegt` | durch geprüfte Quelle / gelesene Datei / Tool-Ergebnis gedeckt | behaupten **mit** Quellenangabe |
| `ableitbar` | folgt zwingend aus bereitgestelltem Kontext/Daten | behaupten **mit** Verweis auf die Basis |
| `ungeprüft` | plausibel, aber ohne Beleg | abschwächen ("möglicherweise", "bitte prüfen") **oder** verifizieren |
| `nicht behaupten` | nicht verifizierbar / sicherheits-/faktenkritisch ohne Quelle | **streichen**; stattdessen Lücke benennen |

Entscheidungsregel: **Im Zweifel runterstufen.** `ungeprüft` ist nie eine Grundlage für
eine definitive Aussage oder für eine Annahme im autonomen Ablauf. Trainingswissen über
veränderliche Fakten (Preise, Releases, Amtsinhaber, Versionen) ist **nie** automatisch
`belegt` — wenn ein Verifikationswerkzeug verfügbar ist (Web-Suche, Doku-Tool, Datei
lesen), nutze es, bevor du `belegt` vergibst.

## Workflow

1. **Claims extrahieren** — jede atomare externe Behauptung listen; Sammelaussagen
   zerlegen ("X ist schneller und billiger" → zwei Claims).
2. **Belegquelle bestimmen** — gelesene Datei/Tool/Suchergebnis → `belegt`; zwingend aus
   Kontext folgend → `ableitbar`; nur Trainingswissen/Plausibilität → `ungeprüft` oder
   `nicht behaupten`.
3. **Verifizieren oder herabstufen** — `belegt`/`ableitbar` mit Quelle behalten;
   `ungeprüft` jetzt verifizieren oder sichtbar abschwächen; `nicht behaupten` entfernen.
3b. **Wiederholungen mitziehen** — nach jedem Herabstufen die Kernbegriffe des Claims
   über das **ganze** Artefakt greppen und **jede** Wiederholung auf dieselbe Marke
   ziehen. Eine Abschwächung nur an der Fundstelle ist keine Abschwächung: sie wirkt
   nicht dort, wo der Leser entscheidet. Besonders zu prüfen sind
   **Empfehlung/Fazit/Zusammenfassung**, **stärkstes Gegenargument** und
   **Änderungsprotokoll** — dort überleben absolute Fassungen, weil sie beim
   Redigieren wie Rückblick statt wie Behauptung aussehen.

   **Der Änderungsprotokoll-Eintrag ist selbst ein Claim der Marke `ungeprüft`.**
   „X ersetzt durch Y", „Finding erledigt", „Absolutaussage entfernt" liest sich wie
   Evidenz, ist aber nur eine Behauptung über den eigenen Diff. Beleg ist der Grep,
   nicht der Eintrag. Erst wenn der Grep null unqualifizierte Treffer zeigt, wird der
   Eintrag `belegt`.

   *Realfall (15.08.2026):* Ein Plan schwächte „es gibt keinen externen Client"
   korrekt zu fünf abgestuften Sätzen mit `ASSUMPTION` ab — **und behielt die
   absolute Fassung in Empfehlung und Gegenargument**, wo die Entscheidung fällt.
   Dasselbe mit Evidenzklassen: der Detailabschnitt sagte
   `AGENT_REPORTED_RUNTIME_EVIDENCE`, die Zusammenfassung leitete mit „jeder Punkt
   gemessen" ein. Beide Findings standen im Protokoll als erledigt und hatten eine
   beauftragte Reviewrunde überlebt.
4. **Lücken benennen statt füllen** — für jede entfernte/unhaltbare Behauptung die offene
   Frage präzise benennen. Im Spec-/Anforderungskontext zwingend: Lücke an den
   **Menschen** zurückgeben (gezieltes Nachfragen, z.B. via `brainstorming`), nicht selbst
   entscheiden.
5. **Audit ausgeben** vor der finalen Antwort (Format unten). Bei Kopplung an
   `ultrathink-craftsmanship`: dies erfüllt dessen Phase 5.

## Ausgabeformat

```text
## Konfabulations-Audit
| # | Claim | Quelle | Marke | Handlung |
|---|-------|--------|-------|----------|
| 1 | ...   | ...    | belegt/ableitbar/ungeprüft/nicht behaupten | behalten/abschwächen/streichen |

Offene Lücken (nicht selbst zu schließen):
- [Frage 1 → an User / via brainstorming]
```

Im Kurzmodus genügt eine Claim-Liste mit Marken, wenn keine kritischen Claims vorliegen.

## Eskalation in autonomen Abläufen

Wenn dieses Audit innerhalb eines Agenten-Workflows (z.B. /agileteam) läuft:

- **Kein** `ungeprüft`- oder `nicht behaupten`-Claim darf als Prämisse in eine spätere
  Phase übernommen werden.
- Tritt ein solcher Claim an einem Anforderungs-/Spec-Punkt auf → **BLOCKER**: Ablauf
  anhalten, Lücke per Nachfrage am Menschen schließen.
- Genau **ein** Remediation-Pass; das Audit selbst wird nicht endlos wiederholt.
