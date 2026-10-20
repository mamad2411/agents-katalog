# Kostenrechnung

> Kostenartenrechnung, Kostenstellenrechnung, Kostenträgerrechnung — vollständige Kostenrechnungssystematik für betriebliche Entscheidungen.

## When to Activate

- Aufbau oder Überarbeitung eines Kostenrechnungssystems
- Kalkulation von Produktkosten oder Dienstleistungspreisen
- Erstellung eines Betriebsabrechnungsbogens (BAB)
- Entscheidung zwischen Voll- und Teilkostenrechnung
- Innerbetriebliche Leistungsverrechnung
- Zuschlagssätze berechnen oder validieren
- Kostenstellenplanung und Budgetierung

## Core Concepts

### Kostenrechnungssysteme im Überblick

| Dimension | Ausprägung | Einsatz |
|-----------|-----------|---------|
| Zeitbezug | Istkostenrechnung | Nachkalkulation, Abweichungsanalyse |
| Zeitbezug | Normalkostenrechnung | Laufende Kalkulation mit Durchschnittswerten |
| Zeitbezug | Plankostenrechnung | Vorkalkulation, Budgetkontrolle |
| Umfang | Vollkostenrechnung | Langfristige Preisfindung, Bestandsbewertung |
| Umfang | Teilkostenrechnung | Kurzfristige Entscheidungen, Engpassplanung |

### Kostenartenrechnung — Welche Kosten sind angefallen?

**Einzelkosten** — direkt dem Kostenträger zurechenbar:
- Fertigungsmaterial (Materialeinzelkosten)
- Fertigungslöhne (Fertigungseinzelkosten)
- Sondereinzelkosten der Fertigung (z. B. Spezialwerkzeuge)
- Sondereinzelkosten des Vertriebs (z. B. Verpackung, Fracht)

**Gemeinkosten** — nur indirekt über Schlüssel zurechenbar:
- Materialgemeinkosten (Lagerhaltung, Einkauf)
- Fertigungsgemeinkosten (Meistergehälter, Abschreibungen Maschinen)
- Verwaltungsgemeinkosten (Geschäftsführung, Buchhaltung)
- Vertriebsgemeinkosten (Marketing, Außendienst)

### Kostenstellenrechnung — Wo sind die Kosten angefallen?

**Kostenstellentypen:**
- Hauptkostenstellen — leisten direkt am Produkt (Fertigung, Montage)
- Hilfskostenstellen — unterstützen Hauptkostenstellen (Instandhaltung, Energieversorgung)
- Allgemeine Kostenstellen — für Gesamtbetrieb (Verwaltung, Vertrieb)

**Innerbetriebliche Leistungsverrechnung (ILV):**
1. Anbauverfahren: Hilfskostenstellen verrechnen nur auf Hauptkostenstellen, gegenseitige Leistungen werden ignoriert
2. Stufenleiterverfahren: Hilfskostenstellen verrechnen nacheinander, Rückverrechnungen werden ignoriert
3. Gleichungsverfahren (mathematisch): Simultane Verrechnung aller gegenseitigen Leistungen (Gleichungssystem)

### Kostenträgerrechnung — Wofür sind die Kosten angefallen?

**Divisionskalkulation** (homogene Massenproduktion):
- Einstufig: Gesamtkosten / Produktionsmenge
- Zweistufig: Herstellkosten/Prod.menge + Verwaltungs-/Vertriebskosten/Absatzmenge
- Mehrstufig: Je Fertigungsstufe getrennt
- Äquivalenzziffernkalkulation: Gewichtete Divisionskalkulation bei artverwandten Produkten

**Zuschlagskalkulation** (Mehrproduktunternehmen):
```
  Materialeinzelkosten (MEK)
+ Materialgemeinkosten (MGK = MEK x MGK-Zuschlagssatz)
= Materialkosten
+ Fertigungseinzelkosten (FEK)
+ Fertigungsgemeinkosten (FGK = FEK x FGK-Zuschlagssatz)
+ Sondereinzelkosten der Fertigung
= Herstellkosten
+ Verwaltungsgemeinkosten (VwGK = HK x VwGK-Zuschlagssatz)
+ Vertriebsgemeinkosten (VtGK = HK x VtGK-Zuschlagssatz)
+ Sondereinzelkosten des Vertriebs
= Selbstkosten
```

### Normalkostenrechnung

Statt Ist-Zuschlagssätzen werden Normalzuschlagssätze aus Durchschnittswerten vergangener Perioden verwendet. Abweichung = Ist-Gemeinkosten - verrechnete Normalgemeinkosten. Über- oder Unterdeckung wird analysiert und im Ergebnis berücksichtigt.

## Methodology

### BAB-Erstellung (Betriebsabrechnungsbogen)

1. **Primärkostenverteilung**: Gemeinkosten aus der Kostenartenrechnung auf Kostenstellen verteilen (Verteilungsschlüssel: qm, Köpfe, kWh)
2. **Sekundärkostenverteilung**: ILV durchführen — Hilfskostenstellen auf Hauptkostenstellen umlegen
3. **Zuschlagssätze berechnen**: Gemeinkosten der Hauptkostenstellen ins Verhältnis zur Zuschlagsbasis setzen
4. **Kontrolle**: Zuschlagssätze mit Vorperioden und Branchenwerten vergleichen

### Zuschlagssätze berechnen

```
MGK-Zuschlagssatz = (Materialgemeinkosten / Materialeinzelkosten) x 100
FGK-Zuschlagssatz = (Fertigungsgemeinkosten / Fertigungseinzelkosten) x 100
VwGK-Zuschlagssatz = (Verwaltungsgemeinkosten / Herstellkosten) x 100
VtGK-Zuschlagssatz = (Vertriebsgemeinkosten / Herstellkosten) x 100
```

### Maschinenstundensatzrechnung

Bei kapitalintensiver Fertigung: FGK nicht über Fertigungslöhne, sondern über Maschinenstunden verrechnen.

```
Maschinenstundensatz = (kalk. Abschreibung + kalk. Zinsen + Raumkosten
                       + Energiekosten + Instandhaltung + Werkzeugkosten)
                       / geplante Maschinenstunden
```

## Templates

### BAB-Template

| Kostenart | Gesamt | Material | Fertigung I | Fertigung II | Verwaltung | Vertrieb |
|-----------|--------|----------|-------------|-------------|------------|----------|
| Gehälter | XXX | XX | XX | XX | XX | XX |
| Abschreibungen | XXX | XX | XX | XX | XX | XX |
| Miete | XXX | XX | XX | XX | XX | XX |
| Summe primär | XXX | XX | XX | XX | XX | XX |
| Umlage Hilfs-KSt | — | XX | XX | XX | XX | XX |
| Summe gesamt | XXX | XX | XX | XX | XX | XX |
| Zuschlagsbasis | — | MEK | FEK I | FEK II | HK | HK |
| Zuschlagssatz | — | X% | X% | X% | X% | X% |

### Kalkulationsschema-Template

```
Produkt: [Bezeichnung]         Stückzahl: [n]
─────────────────────────────────────────────
MEK:                              €  ______
+ MGK (____%):                    €  ______
= Materialkosten:                 €  ______
FEK:                              €  ______
+ FGK (____%):                    €  ______
+ SEK Fertigung:                  €  ______
= Herstellkosten:                 €  ______
+ VwGK (____%):                   €  ______
+ VtGK (____%):                   €  ______
+ SEK Vertrieb:                   €  ______
= Selbstkosten:                   €  ______
+ Gewinnzuschlag (____%):         €  ______
= Barverkaufspreis:               €  ______
+ Skonto (____%):                 €  ______
= Zielverkaufspreis:              €  ______
+ Rabatt (____%):                 €  ______
= Listenverkaufspreis (netto):    €  ______
```

## Quality Gate

- [ ] Kostenartenplan ist vollständig und trennt Einzel- von Gemeinkosten sauber
- [ ] Kostenstellenplan bildet die Organisationsstruktur ab
- [ ] Verteilungsschlüssel sind sachlich begründet und dokumentiert
- [ ] ILV-Methode ist gewählt und konsistent angewendet
- [ ] Zuschlagssätze sind plausibel (Vergleich Vorperiode, Branche)
- [ ] Über-/Unterdeckungen bei Normalkostenrechnung werden analysiert
- [ ] Kalkulationsergebnis wurde mit Marktpreis abgeglichen
- [ ] Vollkosten- vs Teilkostenansatz ist bewusst gewählt und begründet
