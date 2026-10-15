---
name: privacy-workflow
description: Nutze diesen Skill IMMER wenn es um Kundenkommunikation, Kundendaten, Mail-Entwürfe, Bewertungsantworten, Schadensprotokolle oder Buchungstexte für Nero Lefkada Rental&Retail geht. Definiert den Anonymisierungs-Workflow zwischen Kristinas Laptop (echte Daten bleiben da) und Claude (nur Platzhalter). Enthält Platzhalter-Tabelle, Beispiel-Entwürfe mit Platzhaltern, Stopp-Regeln bei echten Daten und Verweis auf `.claude/rules/privacy-stopp.md` und `.claude/rules/daten-regel.md`.
---

# Privacy-Workflow — Anonymisierung zwischen Laptop und Claude

**Grundprinzip:** Echte Kundendaten bleiben auf Kristinas Laptop (bzw. der Synology). Claude sieht nur Platzhalter. Kristina setzt die echten Werte erst beim Absenden lokal wieder ein.

Das ist DSGVO-konform (Art. 5 Datenminimierung, Art. 32 Sicherheit), schützt vor Datenleaks über Cloud-LLMs und erlaubt Kristina den gleichen Entwurf mehrfach zu verwenden.

Siehe auch:
- [.claude/rules/daten-regel.md](../../rules/daten-regel.md) — Ampelsystem (GRÜN/GELB/ROT), was darf zu Claude
- [.claude/rules/privacy-stopp.md](../../rules/privacy-stopp.md) — Was Claude tut wenn echte Daten auftauchen

---

## Der 6-Schritte-Workflow

```
┌────────────────────────────────┐
│ 1. Echte Kundenmail / Daten    │ ← Kristina hat auf Laptop/Synology
└───────────────┬────────────────┘
                │
                ▼
┌────────────────────────────────┐
│ 2. Platzhalter einsetzen       │ ← Kristina ersetzt lokal
│    (Ersatz-Tabelle unten)      │
└───────────────┬────────────────┘
                │
                ▼
┌────────────────────────────────┐
│ 3. Anonymisierte Version       │ ──→ in Claude-Chat
│    in Claude-Chat pasten       │
└───────────────┬────────────────┘
                │
                ▼
┌────────────────────────────────┐
│ 4. Claude entwirft Antwort     │ ← IMMER mit Platzhaltern
│    mit Platzhaltern            │    (nie Namen erraten!)
└───────────────┬────────────────┘
                │
                ▼
┌────────────────────────────────┐
│ 5. Kristina setzt echte Daten  │ ← auf Laptop/in Mail-Client
│    lokal wieder ein            │
└───────────────┬────────────────┘
                │
                ▼
┌────────────────────────────────┐
│ 6. Versand aus Mail-Programm   │ ← Kristina, nie Claude
└────────────────────────────────┘
```

---

## Standard-Platzhalter

**Immer exakt diese Schreibweise benutzen** (Großbuchstaben, eckige Klammern, Bindestrich bei Mehrworten). Das erlaubt Claude die Platzhalter sicher wiederzuerkennen und im Entwurf zu erhalten.

| Echt | Platzhalter |
|------|-------------|
| Vorname | `[VORNAME]` |
| Nachname | `[NACHNAME]` |
| Vollständiger Name | `[KUNDE]` |
| E-Mail | `[EMAIL]` |
| Telefon / Mobil | `[TEL]` |
| IBAN / Konto | `[IBAN]` |
| Kreditkarte | `[KARTE]` |
| Passnummer | `[PASS-NR]` |
| Ausweisnummer | `[AUSWEIS-NR]` |
| Heimatland | `[LAND]` |
| Stadt | `[STADT]` |
| Adresse | `[ADRESSE]` |
| Geburtsdatum | `[GEB-DATUM]` |
| Buchungs-ID | `[BUCHUNG-ID]` |
| Rechnungs-Nr. | `[RECHNUNG-NR]` |
| Betrag (individuell) | `[BETRAG]` |
| Datum (wenn identifizierbar) | `[DATUM]` |
| Uhrzeit | `[UHRZEIT]` |
| Jetski-Modell (wenn kundenspezifisch) | `[JETSKI]` |
| Gruppengröße | `[ANZAHL-PERSONEN]` |

**Nicht anonymisieren:**
- Generische Preise (z.B. „€140 pro Stunde" — öffentlich)
- Öffnungszeiten, Standort, Jetski-Flotte
- Davids WhatsApp und Kristinas Business-E-Mail
- Marketing-Aussagen, Slogans

---

## Beispiel-Entwurf mit Platzhaltern (Buchungsbestätigung EN)

**Input an Claude (anonymisiert):**
> „Kunde will am [DATUM] um [UHRZEIT] eine [BUCHUNG-DAUER] auf dem [JETSKI]. Er fragt ob Water Fun mit dabei ist."

**Claude-Output (bleibt mit Platzhaltern):**
> Hey [VORNAME]!
>
> Great choice — you're confirmed for [DATUM] at [UHRZEIT], [BUCHUNG-DAUER] on [JETSKI]. Meeting point: Lygia Port, Lefkada.
>
> Water Fun (€30/person for the 3-tube ride) is an add-on — we can either lock it in now or decide on the spot. Just let me know.
>
> Any questions before then? WhatsApp David: +30 695 561 2777.
>
> See you on the water!
> – Nero Lefkada

**Kristina ersetzt lokal:**
- `[VORNAME]` → Marco
- `[DATUM]` → Wednesday, May 15th
- `[UHRZEIT]` → 10:00
- `[BUCHUNG-DAUER]` → 1-hour rental
- `[JETSKI]` → Nero Dio

---

## Was Claude NIEMALS tut im Privacy-Workflow

1. **Echte Namen / Daten erraten oder ergänzen.** Auch nicht „um den Text runder zu machen".
2. **Platzhalter entfernen** damit der Text „schöner" klingt. Platzhalter bleiben stehen bis Kristina sie ersetzt.
3. **Mehr personenbezogene Details anfragen als nötig.** Wenn eine Mittwochs-Buchung bestätigt werden soll: Name-Platzhalter + Datum reichen. Keine Geburtsdaten, keine Adresse, keine Passnummer.
4. **Im Verlauf eines Chats Platzhalter durch echte Werte ersetzen** wenn Kristina später im gleichen Chat den echten Namen nennt. Stattdessen: Stopp-Regel (siehe `privacy-stopp.md`), Nachfrage.
5. **In Memory oder Dateien schreiben** wenn dabei echte personenbezogene Daten persistiert würden. Memory darf Muster/Regeln/Workflow enthalten — **nie** konkrete Kundendaten.

---

## Wann dieser Skill greift (Trigger)

- Kristina sagt: „Schreib eine Antwort an Kunde X" / „Entwirf eine Bestätigung" / „Antworte auf diese Bewertung" / „Schreib eine Erinnerung"
- Kristina paste eine Kundenmail (auch wenn sie glaubt sie sei schon anonymisiert — nochmal prüfen)
- Es geht um Schadensprotokolle, Kautionsrückgaben, Umbuchungen, Stornos
- Google-Bewertungs-Antworten (`review-responder`-Agent nutzt diesen Skill ebenfalls)

---

## Zusammenspiel mit anderen Skills/Rules

| Skill / Rule | Was es beiträgt |
|---|---|
| `daten-regel.md` | Ampel GRÜN/GELB/ROT — entscheidet ob überhaupt was zu Claude darf |
| `privacy-stopp.md` | Was Claude tut wenn echte Daten reinrutschen |
| `feedback_payment_red_line.md` (Memory) | Keine IBANs/Kartendaten, nie |
| `feedback_secrets_handling.md` (Memory) | Keine Tokens, API-Keys, Passwörter |
| `compliance-high-standard` (Skill) | Ziel ist HOCH-Compliance, nicht MITTEL |
| `google-business-profile` (Skill) | Liefert Review-Templates DE/EN/IT/EL — der `review-responder`-Agent nutzt beide zusammen |
| `brand-assets` (Skill) | Liefert Tonfall und Signatur für Entwürfe |

---

## Für Kristina (Kurz-Merkzettel)

1. **Bevor Du etwas pastest:** 3-Sekunden-Regel (siehe `daten-regel.md`)
2. **Nutze immer die gleichen Platzhalter** (Tabelle oben)
3. **Fülle Platzhalter erst beim Absenden** in Deinem Mail-Programm
4. **Claude wird Dich erinnern** wenn echte Daten rutschen — nicht als Kritik, als Schutz
