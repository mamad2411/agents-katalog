---
name: insolvenz-fortbestand-paragraf-103-inso-lizenz
description: "Wenn es um Insolvenz-Fortbestand der Lizenz ($ 103 InsO) in Lizenzvertragsersteller geht: ordnet Sachverhalt, Norm, Beweislast, Gegenargumente und nächsten Schritt; liefert ein direkt nutzbares Arbeitsprodukt mit Prüfpunkten, Risiken und nächstem Schritt."
---

# Insolvenz-Fortbestand der Lizenz ($ 103 InsO)

## Problem

Wird der **Lizenzgeber insolvent**, hat der Insolvenzverwalter nach $ 103 InsO das **Wahlrecht**:
- Erfuellung verlangen (Lizenz besteht fort) oder
- Erfuellung verweigern (Lizenz endet; Schadensersatzanspruch des Lizenznehmers ist nachrangige Insolvenzforderung).

Praxis: Verwalter waehlen typischerweise Erfuellungsverweigerung, wenn das IP an einen anderen Investor verkauft werden soll - mit hoeherem Erlos.

## BGH-Linie (h. M.)

| Entscheidung | Tragende Aussage |
|---|---|
| BGH IX ZR 161/05 (2007) | Wahlrecht $ 103 InsO gilt auch für Lizenzvertraege, nicht nur Kaufvertraege - live verifizieren |
| BGH IX ZR 220/09 (2012) | Bei dinglich uebertragener Lizenz kein Wahlrecht (keine gegenseitige Pflicht mehr offen) |

→ Wer dinglich uebertragene Lizenz mit Voraussetzungen für Bestaendigkeit gestaltet, schuetzt den Lizenznehmer.

## Gestaltungsmoeglichkeiten

### A. Sicherungslizenz (bedingt aufschiebend)

Lizenz wird nur aufschiebend bedingt durch eine Bedingung gewaehrt, die jedenfalls eintritt (z. B. Zahlung des Lizenzgebers an einen Sicherheitsempfaenger). Verwalter findet im Insolvenzfall keine gegenseitig offene Pflicht mehr - $ 103 InsO greift nicht.

### B. Vollabgeschlossene Lizenz mit Royalty-Vorauszahlung

Wenn der Lizenznehmer alle Lizenzgebuehren upfront zahlt: keine offenen gegenseitigen Pflichten mehr - $ 103 InsO greift nicht.

### C. Escrow als Realisierungsweg

Insolvenz-Trigger fuehrt zur Source-Code-Herausgabe (siehe `escrow-quellcode-verwahrer-vereinbarung`). Praktisch loest das Wartung, nicht die Lizenz selbst.

### D. Kollektivvereinbarung mit Sicherheitennehmer (Bank)

Bank gibt Lizenz als Sicherheit; im Insolvenzfall verwertet die Bank die Sicherheit (nicht der Verwalter) - $ 103 InsO entfaellt.

## Klausel-Baustein

> **$ 16 Insolvenzfestigkeit.**
>
> (1) Die Parteien sind sich einig, dass die in diesem Vertrag eingeraeumten Nutzungsrechte als dinglich uebertragen gelten, soweit dies nach deutschem Recht zulässig ist.
>
> (2) Sollte ein Insolvenzverfahren über das Vermögen des Lizenzgebers eroeffnet werden, gilt die Hinterlegung beim Escrow-Agent gemäß $ 14 als Sicherungsmittel im Sinne der $$ 50, 51 InsO. Der Lizenznehmer ist berechtigt, die hinterlegten Materialien zu nutzen, soweit zur Wartung und Fortfuehrung des Lizenzbetriebs erforderlich, ohne dass dies einer Erfuellungswahl nach $ 103 InsO bedarf.
>
> (3) Bereits gezahlte Lizenzgebuehren für den vereinbarten Lizenzzeitraum stehen dem Lizenznehmer als bedingt erworbene Nutzungsrechte zu und unterliegen nicht dem Wahlrecht des Insolvenzverwalters.
>
> (4) Sofern Absatz 1 bis 3 rechtlich nicht durchgreifen, vereinbaren die Parteien eine Sicherungsabtretung des Lizenzgegenstands an [Sicherheitennehmer] gemäß separater Sicherungsabrede.

## Hinweise

- $ 103 InsO ist h. M. zwingendes Recht; vertragliche Abdingung dabei begrenzt.
- Die hier vorgeschlagene Klausel ist eine Best-Effort-Konstruktion; im konkreten Fall ist die Wirksamkeit gegen den Verwalter immer streitig.
- Praxis: Escrow + Sicherungslizenz + dingliche Voll-Uebertragung kombinieren.

## Anschluss

- Escrow: `escrow-quellcode-verwahrer-vereinbarung`
- Sicherheiten: `sicherungslizenz-pfandrecht-an-immaterialguetern`
