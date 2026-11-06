---
name: luecken-aufzeiger
description: "Wenn es um Gap-Analyse: Interne Richtlinien vs. Aufsichtsverlautbarungen in Regulatorisches Recht – Plugin für deutsches geht: ordnet Akteninhalt, Belege, Lücken und Nachforderungen; liefert ein direkt nutzbares Arbeitsprodukt mit Prüfpunkten, Risiken und nächstem Schritt."
---

# Gap-Analyse: Interne Richtlinien vs. Aufsichtsverlautbarungen

## Eingaben

- **Aufsichtsverlautbarung:** BaFin-Rundschreiben / Leitlinie (hochgeladen oder per Link)
- **Interne Richtlinie(n):** Zu prüfende Bestandsdokumente (hochgeladen oder aus Richtlinienbibliothek)
- **Segment:** Art des Instituts / Unternehmens (z. B. Kreditinstitut KWG § 1, Zahlungsinstitut ZAG § 1, Wertpapierfirma WpIG § 2)
- Optional: Übergangsfrist aus der Verlautbarung
- Optional: Bestehende Gap-Liste aus vorherigem Lauf

## Ablauf

### 1. Verlautbarung einlesen und strukturieren

Die Aufsichtsverlautbarung lesen und gliedern:

| Modul / Abschnitt | Regelungsinhalt | Adressatenkreis | Übergangsfrist |
|---|---|---|---|
| [z. B. AT 4.3.2] | [Anforderung] | [Alle Institute / Bedeutende Institute] | [TT.MM.JJJJ] |

Für MaRisk-Rundschreiben (BaFin RS 09/2017 i.d.F. Novelle 2023) [Modellwissen – prüfen auf aktuelle Fassung]:
- **AT-Module:** Allgemeiner Teil (AT 1 – AT 9)
- **BT-Module:** Besonderer Teil (BTO Kreditgeschäft, BTRO Handelsgeschäft)
- **BTR-Module:** Besondere Anforderungen Risikosteuerung (BTR 1–4)

### 2. Interne Richtlinien einlesen und zuordnen

Für jede interne Richtlinie ermitteln:
- Welches Modul / welchen Abschnitt der Verlautbarung deckt sie ab?
- Letzte Aktualisierung
- Verantwortlicher

Zuordnungsmatrix erstellen:

| Verlautbarungsabschnitt | Interne Richtlinie | Deckungsgrad | Bemerkung |
|---|---|---|---|
| AT 4.3.2 | IKS-Richtlinie v. 01.03.2023 | teilweise | Datenhaltungsfristen fehlen |
| BT 3.1 | Stresstesting-Policy | vollständig | Aktuell |
| BTR 2.3 | Liquiditätsrichtlinie | keine | Richtlinie fehlt `[prüfen]` |

### 3. Gap-Identifikation

Für jede identifizierte Lücke:

```yaml
gap:
 id: "[GAP-2025-001]"
 verlautbarung: "[BaFin RS 09/2017 Novelle 2023, AT 4.3.2]"
 anforderung: "[Beschreibung der neuen Anforderung]"
 bestandsregel: "[Aktuelle interne Regelung oder 'keine']"
 luecke: "[Was fehlt oder abweicht]"
 schweregrad: "[🔴 Blockierend / 🟠 Hoch / 🟡 Mittel / 🟢 Gering]"
 frist: "[TT.MM.JJJJ oder 'keine Frist']"
 eigentuemer: "[PLATZHALTER]"
 status: "offen"
```

Schweregradkriteria:
- 🔴 **Blockierend:** Fehlende Anforderung ist prüfungsrelevant; BaFin-Prüfung würde Mängelbescheid auslösen
- 🟠 **Hoch:** Anforderung ist klar formuliert, Lücke vorhanden, Frist < 3 Monate
- 🟡 **Mittel:** Anforderung besteht, Lücke marginal oder Frist > 3 Monate
- 🟢 **Gering:** Best-Practice-Empfehlung ohne verbindlichen Charakter

### 4. Gap-Bericht erstellen

**Zusammenfassung:**
- Gesamtzahl Gaps: N
- Davon 🔴 Blockierend: N | 🟠 Hoch: N | 🟡 Mittel: N | 🟢 Gering: N
- Nächste Frist: TT.MM.JJJJ (GAP-2025-xxx)

**Detaillierte Gap-Tabelle:** (alle Gaps mit Status, Frist, Eigentümer)

**Handlungsempfehlungen:** Priorisierte Liste nach Schweregrad und Frist

### 5. Gap-Tracker schreiben

Gap-Liste in `~/.claude/plugins/config/claude-fuer-deutsches-recht/regulatorisches-recht/gap-tracker.yaml` aktualisieren.

## Aktuelle Rechtsprechung & Leitsätze

- Rechtsprechung: keine Entscheidung aus Modellwissen zitieren; vor Ausgabe über offizielle oder frei zugängliche Quelle mit Gericht, Entscheidungsform, Datum, Aktenzeichen und tragender Aussage verifizieren.

## Zentrale Normen (Paragrafenkette)

Art. 20 Abs. 3 GG (Lueckenfuellungs-Pflicht) — § 5 EGBGB (Analogie) — §§ 133, 157 BGB (Auslegung) — §§ 306 Abs. 2 BGB (Lueckenfuellung AGB-Recht) — Art. 288 AEUV (Richtlinien-Umsetzungs-Luecken)

## Quellen und Zitierweise

Zitierweise: `../../../references/zitierweise.md`

Einschlägige Verlautbarungen und Normen:
- BaFin-Rundschreiben 09/2017 (BA) – Mindestanforderungen an das Risikomanagement (MaRisk) i.d.F. der Novelle 2023 [Modellwissen – prüfen auf aktuelle Fassung; abrufbar unter bafin.de]
- BaFin-Rundschreiben 10/2017 (VA) – VAIT (Versicherungsaufsichtliche Anforderungen an die IT) [Modellwissen – prüfen]
- BaFin-Rundschreiben 10/2018 (BA) – BAIT (Bankaufsichtliche Anforderungen an die IT) i.d.F. 2021 [Modellwissen – prüfen]
- EBA-Leitlinien EBA/GL/2021/04 – IRRBB/CSRBB [Modellwissen – prüfen]
- § 25a KWG (Ordnungsgemäße Geschäftsorganisation)
- § 25b KWG (Auslagerungen)
- Art. 74 CRD V (Governance-Anforderungen)

Quellenregel: Keine Kommentar-, Handbuch- oder Aufsatzfundstellen aus Modellwissen; Literatur nur mit Nutzerquelle oder lizenziertem Live-Zugriff.
- Quellenregel: Keine Kommentar-, Handbuch-, Aufsatz- oder Tabellenfundstellen aus Modellwissen; nur Nutzerquelle, amtliche/freie Quelle oder lizenzierte Live-Verifikation verwenden.
- Lerch, ZAG, 2. Aufl. 2020, § 27 Rn. 1 ff. (Risikomanagement Zahlungsinstitute).

## Beispiel

**Eingabe:** "Bitte die MaRisk-Novelle 2023 gegen unsere Risikomanagement-Richtlinien prüfen. Richtlinien sind im Ordner /compliance/richtlinien/ hinterlegt."

**Ausgabe (Auszug):**

> **⚠️ Prüfernotiz**
> - **Quellen:** MaRisk RS 09/2017 Novelle 2023 [Modellwissen – prüfen gegen bafin.de], Richtlinien [Nutzer-Input]
> - **Gelesen:** MaRisk vollständig; 5 Richtlinien
> - **Zu Ihrer Einschätzung:** 2 Gaps mit 🔴 markiert `[prüfen]`
> - **Vor Verwendung:** MaRisk-Fassung gegen bafin.de aktuellen Stand prüfen

---

**Gap-Bericht: MaRisk-Novelle 2023**
*Erstellt: 01.06.2025 | Institut: Musterbank AG | Segment: KWG-Kreditinstitut*

**Zusammenfassung:** 7 Gaps identifiziert: 🔴 2 | 🟠 3 | 🟡 2 | 🟢 0

| Gap-ID | Modul | Anforderung | Lücke | Schwere | Frist |
|---|---|---|---|---|---|
| GAP-2025-001 | AT 4.3.2 | Datenhaltung 10 J. | Richtlinie sieht 7 J. vor | 🔴 | 31.12.2025 |
| GAP-2025-002 | BTR 3.2 | ESG-Risikointegration | Keine ESG-Policy vorhanden | 🔴 | 31.03.2026 |
| GAP-2025-003 | BTO 1.2.4 | Kreditvergabestandards | Teilweise abgedeckt | 🟠 | 30.06.2026 |

**Handlungsempfehlungen:**
1. **Sofort (GAP-2025-001):** IKS-Richtlinie um Datenhaltungsklausel ergänzen; Norm: AT 4.3.2 MaRisk. Verantwortlich: Compliance.
2. **Bis 31.12.2025 (GAP-2025-002):** ESG-Risikorichtlinie neu erstellen; `/regulatorisches-recht:richtlinien-neufassung` nutzen.

## Risiken / typische Fehler

- **Veraltete MaRisk-Version:** BaFin novelliert MaRisk regelmäßig; stets die aktuell gültige Fassung von bafin.de verwenden. Modellwissen über MaRisk-Inhalte immer gegen die offizielle Fassung prüfen: `[Modellwissen – prüfen]`.
- **Adressatenkreis-Fehler:** Nicht alle MaRisk-Anforderungen gelten für alle Institute gleichermaßen (Proportionalitätsgrundsatz § 25a Abs. 1 S. 3 KWG). Institutsgröße und -komplexität beachten.
- **Fehlende Übergangsfrist:** MaRisk-Novellen enthalten oft gestaffelte Übergangsfristen für einzelne Module. Nicht alle Gaps haben dieselbe Frist.
- **Nur formale Prüfung:** Auch wenn eine interne Richtlinie den Anforderungswortlaut übernimmt, kann sie in der Praxis nicht gelebt werden. Hinweis auf erforderliche Prozessprüfung.
- **Auslagerungsrisiken:** § 25b KWG-Anforderungen an ausgelagerte Tätigkeiten separat prüfen – nicht durch Richtlinienprüfung allein abgedeckt.
