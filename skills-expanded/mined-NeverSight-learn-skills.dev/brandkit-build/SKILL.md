---
name: brandkit-build
description: Verdichtet eine ausführliche Markenbeschreibung zu einem benutzbaren Brand Kit (brand kit, design system, design tokens, style guide). Erzeugt eine kurze verbindliche BRAND.md, ausführbare CSS-Tokens, Wordmark-SVGs, Referenz-Artboards und ein CLAUDE.md, das die Regeln automatisch greifen lässt. Nutze diesen Skill, sobald ein Markeninterview vorliegt, jemand aus einem langen Styleguide etwas Arbeitsfähiges machen will, oder fragt, warum sein Designsystem im Alltag ignoriert wird.
license: MIT
---

# Brand Kit bauen

Schritt 3 von 4. Eingabe ist die Rohfassung aus `brandkit-interview`, Ausgabe
ein Ordner, mit dem sich arbeiten lässt.

## Das eigentliche Problem

Fast jeder Styleguide scheitert nicht am Inhalt, sondern an der Länge. Neunhundert
Zeilen liest niemand, auch kein Sprachmodell mit Kontextfenster: Es liest sie,
gewichtet aber die zwanzigste Regel wie die erste und trifft dann trotzdem
Durchschnittsentscheidungen.

Ein Kit funktioniert, wenn drei Dinge stimmen:

1. Die verbindlichen Regeln sind **kurz genug, dass sie wirklich gelesen werden**.
2. Farben und Maße liegen **ausführbar** vor, nicht nur als Beschreibung.
3. Die Regeln **greifen von selbst**, ohne dass jemand daran denken muss.

Punkt 3 ist der, den alle vergessen. Er ist ein `CLAUDE.md` im Ordner.

## Was entsteht

```
Brand/
├── CLAUDE.md            Arbeitsregeln, greifen automatisch in diesem Ordner
├── BRAND.md             die verbindliche Kurzfassung, das Herzstück
├── REFERENCE.md         die Rohfassung aus dem Interview, als Nachschlagewerk
├── README.md            was wo liegt, plus Starter-Satz für außerhalb
├── brand-helmet.html    Farb- und Schrift-Tokens als fertiger CSS-Block
├── brand-props.json     Akzentfarbe im Design-Editor umschaltbar
├── wordmark.svg         Schriftzug, Standardfall
├── mark.svg             quadratische Bildmarke für kleine Flächen
└── beispiel/            lauffähige Referenz mit allen Bausteinen
```

Lege den Ordner dort an, wo er dauerhaft bleibt, und mache ihn zu einem
Git-Repository. Ein Brand Kit ohne Versionsgeschichte verliert man.

## BRAND.md, die Kurzfassung

Das ist die wichtigste Datei. Zielgröße: unter 250 Zeilen. Wird sie länger,
wandert Material nach `REFERENCE.md`.

Bewährter Aufbau:

1. **Marke in einem Satz** plus Persönlichkeit in einer Zeile
2. **Tokens** als Tabelle: Variablenname, Hexwert, Rolle. Dazu die
   Flächenverteilung in Prozent
3. **Typografie**: die zwei bis drei Rollen und eine Größenskala je Format
4. **Raster und Abstände**: Zahlenreihe, Seitenränder, Radien, Rahmen, Schatten
5. **Wordmark**: welche Datei wann, Mindestgröße, Schutzraum, Verbote
6. **Bausteine**: die wiederkehrenden Elemente mit konkreten Maßen
7. **Formate**: Pixelmaße je Zweck
8. **Text**: Sprache, Ansprache, ein gutes und ein schlechtes Beispiel, die
   Verbotsliste
9. **Nicht benutzen**: die harte Verbotsliste, visuell
10. **Prüfliste vor dem Abgeben**: zehn Fragen, die sich mit ja oder nein
    beantworten lassen

Zwei Dinge machen den Unterschied zwischen einem Kit, das wirkt, und einem, das
dekoriert:

**Prozentangaben statt Adjektive.** „Akzentfarbe sparsam einsetzen" ist nicht
prüfbar. „Akzentfarbe unter 10 Prozent der Fläche, nie als Sektionshintergrund,
nie als Verlauf" ist es.

**Konkrete Maße statt Prinzipien.** „Großzügige Abstände" hilft niemandem.
„Sektionsabstand 96 bis 128 Pixel auf Desktop, 56 bis 72 auf Mobil" schon.

Schreibe die Verbotslisten ausführlich. Sie sind der Teil, der Durchschnitt
verhindert, und sie sind billig zu befolgen.

## CLAUDE.md, der Mechanismus

Ohne diese Datei muss jemand das Kit bei jeder Sitzung von Hand erwähnen. Mit
ihr gelten die Regeln, sobald im Ordner gearbeitet wird.

Sie ist kurz und regelt nur, wie mit den anderen Dateien umzugehen ist:
welche Datei bei Widerspruch gewinnt, dass nur definierte Tokens benutzt werden,
wo die Referenzbeispiele liegen, und dass Änderungen am Kit selbst vorher
abzustimmen sind. Eine Vorlage liegt in `assets/CLAUDE.md.template`.

Für Arbeit außerhalb des Ordners gehört ein **Starter-Satz** in die README, den
man an den Anfang einer Sitzung kopiert, etwa:

```
Lies zuerst <PFAD>\BRAND.md und halte dich exakt daran.
Referenz-Artboards: <PFAD>\beispiel\
```

Das Kit lädt sich nicht von allein. Sag das in der README ausdrücklich, sonst
wundert sich die Person beim ersten Mal.

## Die ausführbaren Teile

**brand-helmet.html** enthält den Google-Fonts-Link und einen `:root`-Block mit
allen Tokens als CSS-Variablen, dazu Grundstile und ein bis zwei
Hilfsklassen für wiederkehrende Rollen (etwa `.lbl` für technische Labels,
`.val` für Zahlen in Mono). Vorlage: `assets/brand-helmet.html.template`.

Der Sinn: Im Layout stehen danach nur noch `var(--...)`, keine rohen Hexwerte.
Eine Farbänderung ist dann eine Zeile statt einer Suche über alle Dateien.

**brand-props.json** macht die Akzentfarbe in Design-Editoren umschaltbar.
Vorsicht bei den Optionen: Bietest du dort funktionale Farben an (Warnung,
Fehler), kann jemand den Markenakzent auf die Fehlerfarbe stellen, und positiv
und negativ fallen zusammen. Entweder nur Markenfarben anbieten, oder in
BRAND.md ausdrücklich schreiben, dass die Umschaltung ein Prüfwerkzeug ist und
kein zweiter Markenakzent.

**wordmark.svg und mark.svg** baust du aus dem Schriftzug, nicht aus Symbolen.
Verzichte auf Roboter, Gehirne, Platinen und Verlaufskugeln, außer die Marke
verlangt sie ausdrücklich.

Ein Fallstrick, der später weh tut: Ein SVG mit `<text>` braucht die Schrift auf
dem anzeigenden Gerät. Im Browser mit geladenem Google Font stimmt das, im
Druck oder in Illustrator greift die Ersatzschrift. Schreibe in die README, dass
die Wordmark in Pfade umgewandelt werden muss, sobald sie den Browser verlässt.

## beispiel/, die Referenz

Baue mindestens zwei lauffähige Beispielflächen, die **alle** Bausteine in den
richtigen Maßen zeigen, typischerweise Desktop und Mobil. Das ist der Teil, der
am meisten Arbeit macht und am meisten spart: Beim nächsten Mal wird kopiert
statt neu erfunden.

Kennzeichne Beispieldaten klar als solche. Erfundene Zahlen aus einem
Referenz-Artboard landen sonst auf einer echten Seite.

## Verdichten, nicht kürzen

Beim Weg von der Rohfassung zu BRAND.md gilt:

- **Behalte** jede Zahl, jeden Hexwert, jedes Maß, jede Verbotsliste.
- **Streiche** Begründungen, Herleitungen, Wiederholungen und alles, was zweimal
  dasteht. Es bleibt in REFERENCE.md erhalten.
- **Verwandle** Prosa in Tabellen. „Die Hauptüberschrift ist 52 Pixel groß und
  wird in der Display-Schrift gesetzt" wird eine Tabellenzeile.

Was in der Rohfassung offen blieb, bleibt auch hier offen. Schreibe hin, dass es
offen ist. Erfinde keinen plausiblen Wert, um eine Lücke zu füllen: Er wird
sonst wie eine Entscheidung behandelt, die nie jemand getroffen hat.

## Zum Schluss

Gehe die Prüfliste, die du gerade geschrieben hast, einmal gegen die
Referenz-Artboards durch. Wenn dein eigenes Beispiel deine eigene Prüfliste
nicht besteht, stimmt eines von beiden nicht.

Berichte dann kurz: was entstanden ist, wo es liegt, wie lang BRAND.md geworden
ist, und was noch offen blieb. Verweise auf `brandkit-publish` für das Bauen mit
dem Kit.
