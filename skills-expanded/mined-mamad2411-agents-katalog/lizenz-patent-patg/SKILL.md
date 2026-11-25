---
name: lizenz-patent-patg
description: "Wenn es um Lizenz Patent (PatG) in Lizenzvertragsersteller geht: ordnet Sachverhalt, Norm, Beweislast, Gegenargumente und nächsten Schritt; liefert ein direkt nutzbares Arbeitsprodukt mit Prüfpunkten, Risiken und nächstem Schritt."
---

# Lizenz Patent (PatG)

## Normenanker

- $ 9 PatG - Schutzwirkung Patent (Ausschlussrecht des Patentinhabers)
- $ 15 PatG - Uebertragung und Lizenzeinraeumung; Rangschutz Lizenznehmer
- $ 24 PatG - Zwangslizenz (oeffentliches Interesse; sehr selten)
- $$ 33 ff. PatG - Anmeldung, Erteilungsverfahren DPMA
- EPUe - Europaeisches Patentuebereinkommen; EPA-Patente
- ArbnErfG - Arbeitnehmererfindergesetz; $ 9 Vergütung Erfinder
- VO (EU) Nr. 316/2014 (TT-GVO) - Technologietransfer-Gruppenfreistellung

## Lizenzformen

| Typ | Definition |
|---|---|
| ausschliessliche Lizenz | nur dieser eine Lizenznehmer + Lizenzgeber selbst darf ggf. nicht nutzen (sole license) |
| einfache Lizenz | Lizenzgeber kann weitere Lizenzen vergeben; Lizenznehmer hat eigenes Nutzungsrecht |
| Cross-License | gegenseitige Lizenz Patentaustausch (Forschungspartner, Wettbewerber) |
| Pool-Lizenz | gepoolte Patente, FRAND-Konditionen, Pool-Administrator |
| Zwangslizenz | $ 24 PatG; Verteidigungsrecht im Klagefall |

## Pflichten beider Seiten

| Lizenzgeber | Lizenznehmer |
|---|---|
| Verteidigung des Patents (Einspruch, Nichtigkeitsverfahren) | Vergütung |
| Aufrechterhaltung (Jahresgebuehren) | Benutzungspflicht ggf. (Mindestlizenzen) |
| Best-Knowledge-Garantie (Patent in Kraft, kein Drittrechtsstreit) | Meldepflichten (Stueckzahlen, Umsatz) |
| Erstattungspflicht bei Rueckruf | Verteidigungs-Mitwirkung im Verletzungsstreit |

## ArbnErfG-Konstellation

Wenn das Patent auf Arbeitnehmererfindern beruht:

1. Diensterfindung vs. freie Erfindung ($ 4 ArbnErfG)
2. Inanspruchnahme durch AG ($ 6 ArbnErfG)
3. **Verguetungspflicht $ 9 ArbnErfG** - vor Lizenzvergabe abgeloest? Sonst Lizenznehmer mittelbar betroffen.
4. Verguetungsbemessung nach Richtlinien (ehem. Richtlinien $ 11)

Im Vertrag: Garantie des Lizenzgebers, dass alle ArbnErfG-Verguetungen abgegolten sind.

## Patent Pool / FRAND

Bei Standardpatenten (z. B. Mobilfunk, Codec): FRAND-Pflicht (fair, reasonable, non-discriminatory). EuGH C-170/13 Huawei/ZTE - live verifizieren auf curia.europa.eu. Implementiert wird FRAND ueblicherweise durch Pool-Lizenzen mit kartellrechtskonformer Royalty-Struktur.

## Klausel-Bausteine (DE)

**1. Lizenzgegenstand Patent:**
> "Der Lizenzgeber raeumt dem Lizenznehmer hiermit das einfache, nicht ausschliessliche Recht ein, die in **Anlage A** bezeichneten Patente und Patentanmeldungen ("Lizenzpatente") für das Anwendungsfeld [Feld] im Territorium [Territorium] zu nutzen."

**2. Lizenzgebuehren:**
> "Der Lizenznehmer zahlt eine Running Royalty in Höhe von [X] % des Nettoumsatzes mit Produkten, die unter mindestens einen Anspruch eines Lizenzpatents fallen ("Lizenzprodukte"), zuzueglich gesetzlicher Umsatzsteuer."

**3. Erfindervergutung:**
> "Der Lizenzgeber garantiert, dass alle Arbeitnehmererfindervergutungen nach $$ 9 ff. ArbnErfG hinsichtlich der Lizenzpatente vollstaendig abgegolten sind."

**4. Verteidigung:**
> "Der Lizenzgeber traegt die Aufrechterhaltungsgebuehren und fuehrt etwaige Nichtigkeitsklagen oder Einspruechen selbst. Der Lizenznehmer informiert den Lizenzgeber unverzueglich über Kenntnisnahme von Verletzungen Dritter."

## Anschluss

- Kartellrecht TT-GVO: `kartellrecht-tt-gvo-eu-316-2014`
- Verguetungsklausel: `klausel-verguetung-pauschale-royalty-tiered`
- Cross-License: `klausel-verbesserungen-grant-back`
