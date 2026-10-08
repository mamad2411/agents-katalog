# Projektkontext: Seminararbeit T-18 Predictive Policing

## Worum es geht
Integrationsseminar WWI 23SEB, DHBW Mannheim (Team Pagnia).
Thema T-18: Predictive Policing (z.B. Palantir). Textteil ~3000 Wörter (+/-10%).
Übergeordnetes Seminarthema: IT-Sicherheit / Sicherheit polizeilicher Systeme.

## Toolchain
- Satzsystem: Typst (NICHT LaTeX).
- Literatur: Hayagriva-Format in literatur/quellen.yml.
- Bauen: ./build.sh  -> hauptdokument.pdf
- Live-Vorschau: ./watch.sh
- Wörter zählen: ./wortzahl.sh
- Zitieren im Text: @schluessel (z.B. @winner1980, @bverfg2023).

## Der rote Faden (NICHT verwässern)
Kernthese: Die Architektur prädiktiver Polizeisoftware ist nicht neutral, sondern
verschiebt den Eingriffszeitpunkt staatlicher Gewalt ins Vorfeld und trifft damit
selbst eine rechtsphilosophische Vorentscheidung. Ob das legitim ist, beantworten
Rechtsordnungen unterschiedlich; die deutsche Antwort ist begründbar, aber kontingent.

Scharnierbegriff: der EINGRIFFSZEITPUNKT (technisch + dogmatisch + philosophisch
dieselbe Naht).

Zwei Achsen:
1. Zeitpunkt-Achse (nach Tat <-> im Vorfeld)
2. Daten-Achse, vorgelagert (aggregiert <-> getrennt) -- DE schützt hier,
   rechtlich-organisatorisch, mit Verfassungstiefe (Volkszählungsurteil).

Methodisches Fundament: Co-Production (Jasanoff, Dach) + Winner (Hebel).
Wiederverwendbar für den geplanten Master "AI in Society" an der TUM.

## Kapitelstruktur (dialektisch)
1. Einleitung (`01_einleitung.typ`)
2. Technologische Grundlagen (`02_grundlagen.typ`)
3. Fallstudie hessenDATA (`03_fallstudie_hessendata.typ`) -- technisches Scharnier
4. Kritische Analyse (`04_kritische_analyse.typ`) -- These / Antithese / Synthese
5. Fazit (`05_fazit.typ`)

Drei Vertiefungsstellen, in den Stubs als Kommentare verankert:
- Antithese (4.2): Eingriffszeitpunkt-Argument mit Winner -- Integrations-
  architektur verschiebt polizeiliches Handeln von der Tat ins Vorfeld,
  Technik ist nicht neutral.
- Synthese (4.3): Rekonstruktion statt Forderung -- BVerfG hat technische
  Defizite selbst benannt (fehlende Protokollierungspflichten,
  unzureichend begrenzte Zugriffsrechte).
- Begrifflicher Akzent (Kap. 3 + Fazit): deutscher Datenschutz verankerte
  den Schutz architektonisch über Datensilo-Trennung; Palantir stuft das
  auf bloße Regulierung zurück.

Fachbegriffe mit Verortung:
- hypothetische Datenneuerhebung -> Kap. 2 + Kap. 3 (BVerfG-Diktion)
- Überwachungsgesamtrechnung -> Kap. 4.2 (Antithese, Aggregatmaßstab)
- Dynamic Ontology -> Kap. 2 + Kap. 3 (Palantir-Datenmodell)
- VeRA (Verfahrensübergreifendes Recherche- und Analysesystem)
  -> Kap. 3 + Fazit (bundesweite Fortsetzung)

## Selbstkontroll-Schwellen
- Kapitel 3 (Fallstudie) darf NICHT ins Deskriptive kippen -> dreistufige Architektur-Logik.
- Co-Production UND Winner NICHT je als eigenen Theorie-Exkurs erklären.
- KEINE empirischen Behauptungen über China/Indien -> Typologie/Gedankenexperiment.
- Ressortübergreifende Aggregation ist Disposition/Möglichkeit, nicht Ist-Zustand.
- Palantir = Such-/Verknüpfungsmaschine, KEIN selbstlernender Prophet.
- Achsen-Diagramm ist ein HEURISTISCHES Schema, kein Messergebnis -> im Text so kennzeichnen.

## Offene Aufgaben
- Abbildungen 1 (Wirkkette) und 2 (Silo vs. Plattform) erstellen.

Quellenstand: `literatur/notizen/beschaffungsliste.md`.
Recherchebericht: `literatur/notizen/recherche-2026-06.md`.

Du darfst nur seiten angeben wenn du die aus der quelle bestätigt hast, niemals aus deinen trainingsdaten!