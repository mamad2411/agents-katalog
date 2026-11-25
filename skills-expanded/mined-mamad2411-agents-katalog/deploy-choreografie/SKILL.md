---
name: deploy-choreografie
description: Die verbindliche Reihenfolge, in der Änderungen an PAWN live gehen — Migration, dann Merge, dann Edge Functions — mit den Abbruchbedingungen und der klaren Trennung zwischen dem, was ein Agent selbst tun darf, und dem, was nur Daouda über Lovable auslösen kann. IMMER anwenden, bevor du etwas als fertig meldest, das die Datenbank, eine Edge Function oder das Ausliefern berührt. Trigger: „deployen", „live gehen", „ausliefern", „mergen", „Migration", „supabase/functions", „supabase/migrations", „Lovable", „Release", „auf main", „kann das raus", „was muss ich noch tun", „PR fertig" — und jedes Mal, wenn dein Diff eine Datei unter supabase/ enthält. Ohne diese Reihenfolge geht Code vor seiner Migration live und neue Uploads antworten mit 400.
---

# Deploy-Choreografie

Drei Bühnen, feste Reihenfolge. Wer sie tauscht, bricht die Seite für echte
Kundinnen — PAWN ist live und nimmt echte Stripe-Zahlungen.

## Wer darf was

| Schritt | Agent | Daouda über Lovable |
|---|---|---|
| Code unter `src/` ändern | ✓ | |
| Migration **schreiben** | ✓ | |
| Migration **ausführen** | ✗ | ✓ |
| Edge Function **ändern** | ✓ | |
| Edge Function **ausliefern** | ✗ | ✓ |
| Auf einen Arbeitszweig pushen | ✓ | |
| Nach `main` mergen | ✗ | ✓ |
| Secrets setzen | ✗ | ✓ |

Jede Zeile mit ✗ gehört als eigener Satz in den Abschlussbericht. Ein Agent, der
einen dieser Schritte stillschweigend einplant und dann „fertig" meldet, hat
Gesetz 7 gebrochen.

## Die Reihenfolge

### 1 · Migration zuerst

Die Migration läuft **vor** dem Code, der sie braucht. Immer.

Belegt, nicht vermutet: `61e0204` musste ausdrücklich warnen — *„Migration muss
VOR dem Live-Gang dieses Codes ausgeführt werden, sonst liefern neue Uploads 400
auf dem noch privaten Bucket."*

Eine Migration ist **nicht rücknehmbar**. Es gibt kein Zurück, nur eine zweite
Migration, die zurücknimmt. Deshalb:
- Migration nur nach ausdrücklichem Auftrag schreiben.
- Nie eine bestehende Migration löschen oder ändern — der Hook `wache.sh`
  blockiert das.
- Im Auftrag an Daouda die Datei beim Namen nennen und dazuschreiben, was
  passiert, wenn sie **nicht** läuft.

**Abbruch:** Ist die Migration nicht bestätigt gelaufen, geht der Code nicht raus.
Keine Ausnahme.

### 2 · Dann der Merge nach `main`

Ein Merge nach `main` ist das Ausliefern. Lovable synct von dort, Vercel spiegelt
auf pawn.vision. Es gibt keinen Zwischenschritt und keinen Rückwärtsgang außer
einem neuen Commit.

Vor dem Merge:
```bash
scripts/verify/verify.sh voll
```
Rot heißt: nicht mergen. Die letzte Zeile ist die Aussage, nicht das Gefühl.

**Abbruch:** Ein gefallenes Launch Gate im Prüfstand ist ein Abbruch, kein
Hinweis. Siehe Skill `zera-audit`.

### 3 · Zuletzt die Edge Functions

Edge Functions werden **nur** über den Lovable-Agenten ausgeliefert. Das kostet
Guthaben — Daoudas Budget ist knapp, und Guthaben ist ausdrücklich für genau
diesen Zweck reserviert.

Nach jeder Änderung unter `supabase/functions/` gehört dieser Satz in den
Bericht, wörtlich und nicht versteckt:

> **Daouda: hier ist ein Lovable-Deploy nötig.** Geänderte Funktionen: `…`.
> Ohne diesen Deploy läuft weiterhin die alte Fassung.

Ein eigener Deploy-Versuch ist immer falsch — auch wenn ein Werkzeug dafür
verfügbar aussieht.

**Warum zuletzt:** Der Frontend-Code muss mit der alten *und* der neuen Fassung
der Funktion arbeiten können, solange der Deploy aussteht. Ist das nicht möglich,
gehört es in den Bericht, bevor gemerged wird.

## Die drei Abbruchbedingungen

1. **Migration nicht bestätigt gelaufen** → kein Merge.
2. **`verify.sh voll` rot** → kein Merge.
3. **Der Frontend-Code überlebt die alte Fassung einer geänderten Edge Function
   nicht** → kein Merge, sondern erst der Deploy.

## Der Übergabesatz

Jeder Bericht, der eine dieser Bühnen berührt, endet mit diesem Block — auch wenn
alle Zeilen leer sind:

```
MIGRATION      … Datei · was passiert ohne sie · Status
MERGE          … Zweig · verify.sh voll: n/m
EDGE FUNCTIONS … welche · Lovable-Deploy nötig: ja/nein
BRAUCHT DAOUDA … die Schritte, die ich nicht ausführen kann
```
