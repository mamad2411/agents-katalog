# Investitionsrechnung

> Statische und dynamische Verfahren der Investitionsrechnung — von Kostenvergleich bis vollständigem Finanzplan.

## When to Activate

- Bewertung von Investitionsalternativen (Maschinen, Projekte, Akquisitionen)
- Kapitalwertberechnung (NPV) oder interner Zinsfuß (IRR)
- Amortisationsrechnung für Projekte
- Erstellung eines vollständigen Finanzplans (VoFi)
- Investitionsentscheidungen unter Unsicherheit
- Vergleich von Ersatz- oder Erweiterungsinvestitionen
- Wirtschaftlichkeitsanalyse für Business Cases

## Core Concepts

### Statische Verfahren (einperiodisch, Durchschnittswerte)

**1. Kostenvergleichsrechnung**
```
Durchschnittskosten = fixe Kosten + variable Kosten
fixe Kosten = kalk. Abschreibung + kalk. Zinsen + sonstige Fixkosten
kalk. Abschreibung = (Anschaffungskosten - Restwert) / Nutzungsdauer
kalk. Zinsen = (Anschaffungskosten + Restwert) / 2 x Zinssatz
```
Entscheidung: Alternative mit niedrigsten Durchschnittskosten. Kritische Menge berechnen, ab der Alternative B günstiger wird.

**2. Gewinnvergleichsrechnung**
```
Durchschnittsgewinn = Durchschnittserlöse - Durchschnittskosten
```
Entscheidung: Alternative mit höchstem Durchschnittsgewinn. Sinnvoll, wenn Alternativen unterschiedliche Erlöse generieren.

**3. Rentabilitätsrechnung**
```
Rentabilität = Durchschnittsgewinn / durchschnittlich gebundenes Kapital x 100
durchschnittlich gebundenes Kapital = (AK + Restwert) / 2
```
Entscheidung: Alternative mit höchster Rentabilität, sofern > Mindestverzinsung.

**4. Statische Amortisationsrechnung**
```
Amortisationszeit = Anschaffungskosten / (Durchschnittsgewinn + kalk. Abschreibung)
                  = Anschaffungskosten / durchschnittlicher Rückfluss
```
Entscheidung: Alternative mit kürzester Amortisationszeit. Risikomaß, kein Rentabilitätsmaß.

### Dynamische Verfahren (mehrperiodisch, Zeitwert des Geldes)

**1. Kapitalwertmethode (NPV — Net Present Value)**
```
NPV = -I_0 + Summe(CF_t / (1+i)^t) + RW_n / (1+i)^n
```
- I_0 = Anfangsauszahlung
- CF_t = Cashflow in Periode t (Einzahlungen - Auszahlungen)
- i = Kalkulationszinssatz (WACC oder Opportunitätskosten)
- RW_n = Restwert am Ende der Nutzungsdauer

Entscheidungsregel: NPV > 0 = Investition vorteilhaft. Bei Alternativen: höchster NPV gewinnt.

**2. Interner Zinsfuß (IRR — Internal Rate of Return)**

Der Zinssatz, bei dem NPV = 0. Berechnung durch Interpolation:
```
IRR = i_1 + NPV_1 / (NPV_1 - NPV_2) x (i_2 - i_1)
```
Entscheidungsregel: IRR > Kalkulationszinssatz = vorteilhaft.

**Probleme des IRR:**
- Mehrfache Nullstellen bei nicht-normalen Zahlungsreihen
- Implizite Wiederanlageprämisse zum IRR (unrealistisch bei hohem IRR)
- Skalenblindheit (kleines Projekt kann höheren IRR haben als großes mit höherem NPV)

**3. Annuitätenmethode**
```
Annuität = NPV x Annuitätenfaktor = NPV x (i(1+i)^n) / ((1+i)^n - 1)
```
Wandelt den Kapitalwert in gleiche jährliche Beträge um. Nützlich bei unterschiedlichen Nutzungsdauern (Kettenrechnung).

**4. Dynamische Amortisationsrechnung**
Zeitpunkt, an dem die kumulierten diskontierten Cashflows die Anfangsauszahlung erreichen.

### Vollständiger Finanzplan (VoFi)

Explizite Planung aller Ein- und Auszahlungen, Finanzierungsmaßnahmen und Geldanlagen je Periode. Vorteile gegenüber NPV:
- Unterschiedliche Soll-/Habenzinsen möglich
- Verschiedene Finanzierungsformen abbildbar (Annuitätendarlehen, Tilgungsdarlehen)
- Steuern periodengerecht berücksichtigen
- Endvermögen als Zielgröße

### Investitionsentscheidungen unter Unsicherheit

| Methode | Anwendung |
|---------|-----------|
| Sensitivitätsanalyse | Kritische Werte einzelner Parameter bestimmen |
| Szenarioanalyse | Best Case / Base Case / Worst Case |
| Risikoanalyse (Monte Carlo) | Wahrscheinlichkeitsverteilungen für unsichere Parameter |
| Entscheidungsbaumverfahren | Sequenzielle Entscheidungen mit Wahrscheinlichkeiten |
| Korrekturverfahren | Risikozuschlag auf Kalkulationszins oder Sicherheitsabschlag auf Cashflows |

## Methodology

### NPV-Berechnung Schritt für Schritt

1. **Investitionsauszahlung (I_0)** bestimmen: Kaufpreis + Nebenkosten + Installation + Schulung
2. **Nutzungsdauer** festlegen: Technisch vs. wirtschaftlich, steuerliche AfA als Orientierung
3. **Cashflows je Periode** prognostizieren: Umsatzsteigerung, Kosteneinsparung, zusätzliche Kosten
4. **Kalkulationszinssatz** bestimmen: WACC bei Gesamtunternehmensbetrachtung, risikoäquivalenter Zinssatz bei Einzelprojekt
5. **Restwert** am Ende der Nutzungsdauer schätzen
6. **NPV berechnen** und Entscheidung ableiten
7. **Sensitivitätsanalyse** durchführen: Welche Parameter sind kritisch?

### Vergleich bei unterschiedlichen Nutzungsdauern

- **Annuitätenmethode**: NPV in Annuität umrechnen, Annuitäten vergleichen
- **Kettenrechnung**: Investitionen gedanklich wiederholen bis zum KGV der Nutzungsdauern
- **Endwertmethode**: Auf gemeinsamen Endzeitpunkt aufzinsen

### VoFi-Aufbau

1. Zahlungsreihe der Investition eintragen
2. Finanzierung planen (Eigenkapital, Darlehen mit Konditionen)
3. Steuern berechnen (AfA beachten)
4. Überschüsse anlegen / Fehlbeträge finanzieren
5. Endvermögen berechnen
6. Rendite aus Endvermögen ableiten: r = (Endvermögen/Anfangskapital)^(1/n) - 1

## Templates

### NPV-Berechnungsschema

```
Projekt: _______________     Kalk.zins: ____%
Nutzungsdauer: ____ Jahre    I_0: € ________

Jahr    Einzahlung   Auszahlung   CF netto   Abzinsungs-   Barwert
                                              faktor
  0                                -I_0       1,0000       -I_0
  1      _______      _______     _______     _______      _______
  2      _______      _______     _______     _______      _______
  3      _______      _______     _______     _______      _______
  ...
  n      _______      _______     _______     _______      _______
  RW                              _______     _______      _______
                                                    NPV =  _______
```

### Statischer Vergleich

```
                        Alternative A    Alternative B
Anschaffungskosten         € _______       € _______
Nutzungsdauer               __ Jahre        __ Jahre
Restwert                   € _______       € _______
kalk. Abschreibung         € _______       € _______
kalk. Zinsen               € _______       € _______
Sonstige fixe Kosten       € _______       € _______
Variable Kosten/Stück      € _______       € _______
Menge                       ________        ________
Variable Kosten gesamt     € _______       € _______
Gesamtkosten               € _______       € _______
Stückkosten                € _______       € _______
Kritische Menge:            ________
```

### Sensitivitätsanalyse-Template

```
Parameter          Base Case    Kritischer Wert    Abweichung
Absatzmenge         _______        _______           ____%
Verkaufspreis       _______        _______           ____%
Variable Kosten     _______        _______           ____%
Investitionssumme   _______        _______           ____%
Nutzungsdauer       _______        _______           ____%
Kalkulationszins    _______        _______           ____%
```

## Quality Gate

- [ ] Richtige Methode gewählt (statisch bei Überschlagsrechnung, dynamisch bei signifikanten Investitionen)
- [ ] Cashflows sind inkrementell (nur investitionsbedingte Änderungen)
- [ ] Sunk Costs sind ausgeschlossen
- [ ] Opportunitätskosten sind berücksichtigt
- [ ] Kalkulationszinssatz ist begründet (WACC, Alternativrendite, risikoadjustiert)
- [ ] Steuern sind konsistent behandelt (vor/nach Steuern)
- [ ] Sensitivitätsanalyse identifiziert kritische Parameter
- [ ] Bei IRR: Wiederanlageprämisse und Skaleneffekt geprüft
- [ ] Bei unterschiedlichen Nutzungsdauern: Vergleichbarmachung erfolgt
