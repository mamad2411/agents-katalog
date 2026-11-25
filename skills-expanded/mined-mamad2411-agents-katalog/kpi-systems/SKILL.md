# KPI-System-Design

> Kennzahlensysteme, DuPont, ZVEI, wertorientierte Steuerung — systematisches KPI-Design für Unternehmenssteuerung.

## When to Activate

- Aufbau oder Redesign eines Kennzahlensystems
- ROI-Baum (DuPont-System) erstellen oder analysieren
- Wertorientierte Kennzahlen (EVA, ROCE, ROIC) berechnen
- KPI-Dashboard konzipieren
- Benchmarking-Analysen durchführen
- Reporting-Strukturen definieren
- Ampel-Systeme für Management-Reporting gestalten

## Core Concepts

### DuPont-Kennzahlensystem (ROI-Baum)

Das älteste und bekannteste Kennzahlensystem. Spitzenkennzahl: Return on Investment (ROI).

```
                            ROI
                    ┌────────┴────────┐
              Umsatzrendite    x    Kapitalumschlag
              (Gewinn/Umsatz)      (Umsatz/Gesamtkapital)
           ┌───────┴───────┐    ┌──────┴──────┐
        Gewinn          Umsatz  Umsatz    Gesamtkapital
     ┌────┴────┐                        ┌──────┴──────┐
  Umsatz  -  Kosten                  Anlagever-    Umlaufver-
           ┌──┴──┐                    mögen         mögen
        var.   fixe                              ┌────┴────┐
        Kosten Kosten                         Vorräte  Ford.+Kasse
```

**ROI = Umsatzrendite x Kapitalumschlag = (Gewinn/Umsatz) x (Umsatz/Kapital)**

Stärken: Mathematische Zerlegbarkeit, intuitive Treiber-Analyse.
Schwächen: Vergangenheitsorientiert, keine absolute Wertschaffung, kurzfristiger Fokus.

### ZVEI-Kennzahlensystem

Entwickelt vom Zentralverband Elektrotechnik- und Elektronikindustrie. Zwei Analysebereiche:

**Wachstumsanalyse**: Umsatzwachstum, Personalwachstum, Investitionsquote, Ergebniswachstum

**Strukturanalyse** (Spitzenkennzahl: Eigenkapitalrentabilität):
```
EK-Rentabilität = Gesamtkapitalrentabilität x Leverage-Faktor
                = (Umsatzrentabilität x Kapitalumschlag) x (GK/EK)
```

Enthält ca. 200 Kennzahlen mit Haupt- und Hilfskennzahlen. In der Praxis wird häufig eine reduzierte Version verwendet.

### Wertorientierte Kennzahlen

**EVA (Economic Value Added):**
```
EVA = NOPAT - (WACC x Capital Employed)
    = (ROIC - WACC) x Capital Employed
```
- NOPAT = Net Operating Profit After Tax
- Capital Employed = Eigenkapital + verzinsliches Fremdkapital (oder: Gesamtaktiva - unverzinsliche Verbindlichkeiten)
- Positiver EVA = Wertschaffung über Kapitalkosten hinaus

**ROCE (Return on Capital Employed):**
```
ROCE = EBIT / Capital Employed
```
Vergleich mit WACC: ROCE > WACC = wertschaffend.

**ROIC (Return on Invested Capital):**
```
ROIC = NOPAT / Invested Capital
Invested Capital = Working Capital + Net Fixed Assets + sonstige operative Aktiva
```

**CVA (Cash Value Added):**
```
CVA = Brutto-Cashflow - ökonomische Abschreibung - Kapitalkosten
```

### KPI-Hierarchie

```
Ebene 1: Spitzenkennzahl (z. B. EVA, ROI, ROCE)
    │
Ebene 2: Bereichskennzahlen (z. B. Umsatzrendite, Kapitalumschlag)
    │
Ebene 3: Funktionale KPIs (z. B. Materialquote, Personalquote, DSO)
    │
Ebene 4: Operative KPIs (z. B. Ausschussrate, OEE, Liefertreue)
    │
Ebene 5: Prozess-KPIs (z. B. Durchlaufzeit, Fehlerquote, Rüstzeit)
```

Jede Ebene verdichtet die Information nach oben. Drill-Down ermöglicht Ursachenanalyse.

### Reporting-Frequenz

| Kennzahlenkategorie | Frequenz | Zielgruppe |
|---------------------|----------|------------|
| Strategische KPIs (EVA, ROCE, Marktanteil) | Quartalsweise | Vorstand, Aufsichtsrat |
| Finanzielle KPIs (Umsatz, EBIT, Cashflow) | Monatlich | Geschäftsleitung |
| Operative KPIs (Auslastung, Qualität) | Wöchentlich | Bereichsleitung |
| Prozess-KPIs (Durchlaufzeit, OEE) | Täglich/Echtzeit | Teamleitung |

## Methodology

### KPI-System aufbauen

1. **Strategie als Ausgangspunkt**: Welche strategischen Ziele werden verfolgt? Welche Steuerungslogik? (Gewinnmaximierung, Wertorientierung, Wachstum)
2. **Spitzenkennzahl wählen**: ROI (renditeorientiert), EVA (wertorientiert), EBITDA (cashflow-orientiert)
3. **Dekomposition**: Spitzenkennzahl mathematisch oder logisch in Treiber zerlegen
4. **Bereichszuordnung**: Welcher Bereich beeinflusst welchen Treiber?
5. **Operative KPIs ergänzen**: Nicht-finanzielle Kennzahlen für operative Steuerung (Qualität, Zeit, Flexibilität)
6. **Messbarkeit sicherstellen**: Datenquellen, Berechnungslogik, Verantwortliche definieren
7. **Zielwerte setzen**: Interne Historie, externe Benchmarks, strategische Ambitionen

### Benchmarking durchführen

1. **Internes Benchmarking**: Vergleich zwischen Werken, Sparten, Regionen
2. **Wettbewerbsbenchmarking**: Vergleich mit direkten Wettbewerbern (Geschäftsberichte)
3. **Branchenbenchmarking**: Branchendurchschnitte und Best-in-Class
4. **Funktionales Benchmarking**: Best Practice aus anderen Branchen für einzelne Funktionen

Quellen: Geschäftsberichte, Branchenstudien, Verbandsdaten, Datenbanken (Bloomberg, S&P Capital IQ).

### Dashboard-Design

**Grundprinzipien:**
- Max. 7 (+/- 2) KPIs auf einer Dashboard-Seite
- Ampelfarben: Grün/Gelb/Rot mit klaren Schwellenwerten
- Trendpfeile: Entwicklung gegenüber Vorperiode
- Drill-Down-Möglichkeit in Details
- Abweichungskommentierung bei Gelb/Rot obligatorisch

**Aufbau eines Management-Dashboards:**
```
┌──────────────────────────────────────────────┐
│  SPITZENKENNZAHL (z.B. EVA)     Trend: ↑↓→  │
├──────────┬──────────┬────────────────────────┤
│ Umsatz   │ EBIT     │ Cashflow               │
│ Ist/Plan │ Ist/Plan │ Ist/Plan               │
├──────────┴──────────┴────────────────────────┤
│  Treiber-KPIs (3-4 Stück mit Ampel)         │
├──────────────────────────────────────────────┤
│  Aktionsliste: Top-3 Maßnahmen bei Rot/Gelb │
└──────────────────────────────────────────────┘
```

## Templates

### ROI-Baum Berechnungstemplate

```
Unternehmen/Bereich: _______________    Periode: ___________

Umsatzerlöse:                          € ____________
- Herstellkosten:                      € ____________
- Vertriebskosten:                     € ____________
- Verwaltungskosten:                   € ____________
= Gewinn (EBIT):                       € ____________

Umsatzrendite = EBIT / Umsatz =        ____________ %

Anlagevermögen:                        € ____________
+ Umlaufvermögen:                      € ____________
= Gesamtkapital:                       € ____________

Kapitalumschlag = Umsatz / GK =         ____________ x

ROI = Umsatzrendite x Kapitalumschlag = ____________ %
```

### EVA-Berechnungstemplate

```
EBIT:                                  € ____________
- Steuern auf EBIT (____%):           € ____________
= NOPAT:                               € ____________

Eigenkapital:                          € ____________
+ verzinsliches Fremdkapital:          € ____________
= Capital Employed:                     € ____________

WACC:                                   ____________ %
Kapitalkosten = WACC x CE:             € ____________

EVA = NOPAT - Kapitalkosten:            € ____________
ROIC = NOPAT / CE:                      ____________ %
Wertschaffung (ROIC - WACC):            ____________ %
```

### KPI-Steckbrief

```
KPI-Bezeichnung:    ___________________________
Berechnung:         ___________________________
Datenquelle:        ___________________________
Verantwortlicher:   ___________________________
Messfrequenz:       ___________________________
Zielwert:           ___________________________
Schwellenwerte:     Grün: ≥ ___  Gelb: ≥ ___  Rot: < ___
Benchmark:          Branche: ___  Best-in-Class: ___
Treiber:            ___________________________
Maßnahmen bei Rot:  ___________________________
```

## Quality Gate

- [ ] Spitzenkennzahl ist strategiekonform gewählt
- [ ] Dekomposition ist mathematisch/logisch konsistent
- [ ] KPI-Hierarchie bildet die Organisationsstruktur ab
- [ ] Jeder KPI hat einen definierten Verantwortlichen
- [ ] Datenquellen sind verfügbar und zuverlässig
- [ ] Zielwerte sind durch Benchmarks oder Strategie fundiert
- [ ] Ampel-Schwellenwerte sind definiert und akzeptiert
- [ ] Reporting-Frequenz passt zur Steuerungsebene
- [ ] Dashboard zeigt max. 7 KPIs, Drill-Down ist möglich
- [ ] Review-Prozess bei Abweichungen ist definiert
