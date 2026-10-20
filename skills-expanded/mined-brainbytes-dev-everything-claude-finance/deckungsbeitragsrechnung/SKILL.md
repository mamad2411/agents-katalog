# Deckungsbeitragsrechnung

> Einstufige und mehrstufige Deckungsbeitragsrechnung, Break-Even-Analyse, Produktionsprogrammplanung und kurzfristige Entscheidungsunterstützung.

## When to Activate

- Kurzfristige Preis- oder Produktionsentscheidungen
- Break-Even-Analyse für Produkte, Projekte oder Geschäftsbereiche
- Optimierung des Produktionsprogramms bei Engpässen
- Make-or-Buy-Entscheidungen
- Bestimmung von Preisuntergrenzen
- Sortimentsbereinigung oder -erweiterung
- Mehrstufige Ergebnisrechnung nach Produktgruppen

## Core Concepts

### Einstufige Deckungsbeitragsrechnung (Direct Costing)

```
  Erlöse (Preis x Menge)
- variable Kosten
= Deckungsbeitrag (DB)
- fixe Kosten (en bloc)
= Betriebsergebnis
```

**Stückdeckungsbeitrag:** db = p - k_v (Preis minus variable Stückkosten)

Entscheidungsregel: Jedes Produkt mit positivem Deckungsbeitrag trägt zur Fixkostendeckung bei und sollte kurzfristig im Programm bleiben — auch wenn es die vollen Selbstkosten nicht deckt.

### Mehrstufige Deckungsbeitragsrechnung (Fixkostendeckungsrechnung)

```
  Erlöse
- variable Kosten
= Deckungsbeitrag I (produktspezifisch)
- erzeugnisfixe Kosten (z. B. produktspezifische Werbung, Werkzeuge)
= Deckungsbeitrag II (Beitrag der Produktgruppe)
- erzeugnisgruppenfixe Kosten (z. B. Abteilungsleiter)
= Deckungsbeitrag III (Bereichsbeitrag)
- bereichsfixe Kosten (z. B. Werksleitung)
= Deckungsbeitrag IV (Unternehmensbeitrag)
- unternehmensfixe Kosten (z. B. Geschäftsführung)
= Betriebsergebnis
```

Vorteil: Zeigt, auf welcher Ebene ein Produkt/Bereich nicht mehr zur Deckung beiträgt.

### Break-Even-Analyse

**Break-Even-Menge:**
```
x_BE = K_fix / db = K_fix / (p - k_v)
```

**Break-Even-Umsatz:**
```
U_BE = K_fix / (1 - k_v/p) = K_fix / DB-Intensität
```

**Sicherheitskoeffizient (Grad der Sicherheit):**
```
SK = (x_ist - x_BE) / x_ist x 100
```
Gibt an, um wie viel Prozent der Absatz sinken darf, bevor die Gewinnschwelle unterschritten wird. Faustregel: SK > 20 % gilt als komfortabel.

**Operating Leverage (Gewinnsensitivität):**
```
OL = DB / Gewinn = (Erlöse - variable Kosten) / (Erlöse - variable Kosten - fixe Kosten)
```
Hoher Operating Leverage = hohe Fixkosten = hohe Gewinnschwankungen bei Absatzänderungen.

### Preisuntergrenzen

| Fristigkeit | Preisuntergrenze | Begründung |
|-------------|-----------------|------------|
| Kurzfristig (Zusatzauftrag) | variable Kosten (k_v) | Jeder Preis > k_v liefert positiven DB |
| Mittelfristig | variable + erzeugnisfixe Kosten | Produktspezifische Fixkosten müssen gedeckt werden |
| Langfristig | Selbstkosten (Vollkosten) | Alle Kosten müssen gedeckt sein |

### Make-or-Buy-Entscheidung

**Bei freier Kapazität:**
```
Eigenfertigung vorteilhaft wenn: k_v(eigen) < Einkaufspreis
```
Fixkosten sind irrelevant, da sie ohnehin anfallen (sunk costs bei freier Kapazität).

**Bei Kapazitätsengpass:**
```
Fremdbezug vorteilhaft wenn: (Einkaufspreis - k_v(eigen)) / Engpasseinheiten < db_alternativ / Engpasseinheiten
```
Opportunitätskosten des Engpasses berücksichtigen.

### Engpassplanung (ein Engpass)

1. Relativen Deckungsbeitrag je Engpasseinheit berechnen: db / Engpassinanspruchnahme
2. Produkte nach relativem DB absteigend sortieren
3. Engpasskapazität in dieser Reihenfolge zuteilen
4. Ergebnis: Optimales Produktionsprogramm

**Bei mehreren Engpässen:** Lineare Programmierung (Simplex-Methode) erforderlich.

## Methodology

### Schritt-für-Schritt: DB-Rechnung aufbauen

1. **Kosten klassifizieren**: Jede Kostenart in variabel oder fix einteilen. Mischkosten aufspalten (z. B. Stromkosten: Grundgebühr fix, Verbrauch variabel)
2. **Variable Stückkosten ermitteln**: k_v = variable Gesamtkosten / Menge
3. **Stück-DB berechnen**: db = p - k_v
4. **DB-Intensität prüfen**: DB-Intensität = db / p (je höher, desto besser)
5. **Fixkosten schichten**: Zuordnung zu Produkt, Produktgruppe, Bereich, Unternehmen
6. **Mehrstufige DB-Rechnung aufstellen**
7. **Entscheidung ableiten**: Wo ist der DB negativ? Ab welcher Stufe?

### Break-Even-Analyse durchführen

1. Variable und fixe Kosten sauber trennen
2. Break-Even-Menge und -Umsatz berechnen
3. Sicherheitskoeffizienten bestimmen
4. Sensitivitätsanalyse: Was passiert bei +/- 10 % Preis, Menge, variable Kosten?
5. Grafisch darstellen: Erlös- und Kostenkurve mit Break-Even-Punkt

### Produktionsprogrammoptimierung

1. Absatzhöchstmengen je Produkt erfassen
2. Engpasskapazität identifizieren und quantifizieren
3. Relative Deckungsbeiträge berechnen
4. Rangfolge bilden und Kapazität zuteilen
5. Gesamtdeckungsbeitrag des optimalen Programms berechnen
6. Ergebnis mit aktuellem Programm vergleichen

## Templates

### Einstufige DB-Rechnung

```
                    Produkt A    Produkt B    Produkt C    Gesamt
Absatzmenge             ____         ____         ____
Stückpreis           €  ____      €  ____      €  ____
Erlöse               €  ____      €  ____      €  ____    € ____
- var. Kosten        €  ____      €  ____      €  ____    € ____
= DB gesamt          €  ____      €  ____      €  ____    € ____
  Stück-DB           €  ____      €  ____      €  ____
  DB-Intensität       ____%        ____%        ____%
- Fixkosten                                                € ____
= Betriebsergebnis                                         € ____
```

### Mehrstufige DB-Rechnung

```
                    Prod A   Prod B │ Prod C   Prod D │  Gesamt
Erlöse              _____    _____ │  _____    _____ │  _____
- var. Kosten       _____    _____ │  _____    _____ │  _____
= DB I              _____    _____ │  _____    _____ │  _____
- erzeugn.fix       _____    _____ │  _____    _____ │  _____
= DB II             _____    _____ │  _____    _____ │  _____
                   ──── Gruppe 1 ──│── Gruppe 2 ────│
Summe DB II              _____    │       _____     │  _____
- gruppenfixe K          _____    │       _____     │  _____
= DB III                 _____    │       _____     │  _____
- unternehmensfixe K                                │  _____
= Betriebsergebnis                                  │  _____
```

### Engpassplanung-Template

```
                  Prod A   Prod B   Prod C   Prod D
Stückpreis (p)     ____     ____     ____     ____
var. Stückkosten   ____     ____     ____     ____
Stück-DB (db)      ____     ____     ____     ____
Engpass/Stück      ____     ____     ____     ____
Rel. DB (db/Eng.)  ____     ____     ____     ____
Rang               ____     ____     ____     ____
Opt. Menge         ____     ____     ____     ____
Gesamt-DB          ____     ____     ____     ____
```

## Quality Gate

- [ ] Kosten sind sauber in variable und fixe Bestandteile getrennt
- [ ] Mischkosten sind aufgespalten (nicht pauschal zugeordnet)
- [ ] Break-Even-Menge liegt innerhalb der realistischen Absatzspanne
- [ ] Sicherheitskoeffizient ist berechnet und bewertet
- [ ] Bei Engpassplanung: Engpass korrekt identifiziert, relativer DB berechnet
- [ ] Preisuntergrenzen nach Fristigkeit differenziert
- [ ] Make-or-Buy berücksichtigt Opportunitätskosten bei Engpass
- [ ] Ergebnis ist mit Sensitivitätsanalyse abgesichert
- [ ] Langfristige Vollkostendeckung ist geprüft (DB-Rechnung ersetzt keine Vollkostenperspektive)
