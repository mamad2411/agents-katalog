---
name: ais-chat-builder
description: >
  Erstellt fertige, copy-paste-fähige AIS.chat-Vorlagen für den Schul-KI-Chatbot
  AIS.chat. Deckt alle drei Vorlagentypen ab: Lernszenarien, Dialogpartner und
  Assistenten. Verwende diesen Skill immer, wenn jemand AIS.chat-Vorlagen
  erstellen, optimieren oder überarbeiten will, auch bei indirekten
  Formulierungen wie "erstelle ein Rollenspiel für den Unterricht", "ich
  brauche einen KI-Dialogpartner", "Szenario für Moodle mit AIS.chat", oder
  "Unterrichtsassistent mit KI". Der Skill erkennt automatisch, welcher
  Vorlagentyp gemeint ist, und liefert formatierte Ausgaben mit korrekten
  Zeichenlimits und wortgleich eingebauten Knappheitsregeln, damit AIS.chat im
  Einsatz nicht floskelhaft oder weitschweifig antwortet.
---

# AIS.chat-Builder

Erstelle didaktisch durchdachte, sofort einsetzbare Vorlagen für den Schul-KI-Chatbot AIS.chat (Lernszenarien, Dialogpartner, Assistenten). Jede Vorlage enthält **wortgleich eingebaute Knappheitsregeln**, die im Einsatz verhindern, dass AIS.chat floskelhaft, weitschweifig oder mit ungefragten Zusatzideen antwortet.

## Was ist AIS.chat?

AIS.chat ist der ländergemeinsame, datenschutzkonforme KI-Chatbot für deutsche Schulen (DigitalPakt/AIS-Projekt). Der Markenname wird ohne Artikel verwendet. Lehrkräfte konfigurieren darin drei Typen von **Vorlagen** (auch „AIS.chat-Vorlagen"), die per QR-Code oder Link an Lernende geteilt oder seit der Sharing-Funktion bundesweit mit anderen Lehrkräften geteilt werden können:

- **Lernszenario**: Offener, themengebundener Chat mit definiertem Verhalten und Lernauftrag
- **Dialogpartner**: Simulierte Person/Figur mit Rollenkonsistenz, Einstiegsfrage und Leitplanken
- **Assistent**: Flexibles Werkzeug für Lehrkräfte (z.B. Materialerstellung, Unterrichtsplanung)

„Vorlagen" ist im FWU-Sprachgebrauch der Sammelbegriff für diese drei Typen. Wenn die Lehrkraft von „einer Vorlage" spricht, ohne den Typ zu nennen, frage einmal nach (Routing-Tabelle unten).

Die Anwendung läuft unter `https://app.ais-chat.schule`, Projektseite ist `https://ais-chat.schule`. Beachte den Bindestrich in den URLs (ais-chat), während der Markenname selbst mit Punkt geschrieben wird (AIS.chat).

Der Begriff für das verbrauchsbasierte Kontingent heißt **Tokenvolumen**.

## Routing: Welcher Vorlagentyp ist gemeint?

Erkenne anhand des Kontexts, welchen Vorlagentyp die Lehrkraft braucht:

| Signal | → Vorlagentyp |
|--------|---------|
| Rollenspiel, historische Figur, Perspektivwechsel, sokratisch, simulierte Person | Dialogpartner |
| Lernende arbeiten selbstständig mit KI, Projektarbeit, offener Lernauftrag, Übung | Lernszenario |
| Unterrichtsvorbereitung, Materialerstellung, Aufgabengenerator, Korrekturhilfe | Assistent |
| Unklar, nur „Vorlage" genannt | Kurz nachfragen: "Sollen die Lernenden direkt mit AIS.chat arbeiten (Lernszenario/Dialogpartner) oder nutzen Sie AIS.chat selbst als Werkzeug (Assistent)?" |

## Modus: Direkt oder Interview?

**Direktmodus** (Standard): Wenn genug Kontext vorhanden ist (Thema, Zielgruppe, didaktisches Ziel), generiere direkt die fertigen Formularinhalte. Das ist der häufigere Fall.

**Interview-Modus**: Wenn die Eingabe vage ist oder die Lehrkraft explizit um Begleitung bittet ("hilf mir Schritt für Schritt"), führe ein kompaktes Interview. Stelle pro Schritt eine Frage, warte auf die Antwort, dann weiter. Kein unnötiges Aufblähen, keine Zwischenkommentare nach jeder Antwort.

Entscheide selbst, welcher Modus passt. Im Zweifel: Direktmodus mit Rückfrage bei den 1-2 kritischsten Lücken.

## Vorgehen

1. **Vorlagentyp erkennen** (Routing-Tabelle oben)
2. **Referenzdatei lesen**: Lies die passende Spezifikation unter `references/`:
   - `references/dialogpartner.md` für Dialogpartner
   - `references/lernszenario.md` für Lernszenarien
   - `references/assistent.md` für Assistenten
3. **Generieren oder interviewen** je nach Modus
4. **Knappheitsregeln wortgleich einbauen** (Pflichtbausteine, siehe unten), nicht verhandelbar
5. **Validieren**: Zeichenlimits prüfen, Rollenkonsistenz sicherstellen, Altersstufeneignung checken
6. **Ausgabe**: Exakt die Feldstruktur aus der Referenzdatei verwenden, Titel pro Feld, darunter der Text, direkt kopierbar

## Pflichtbausteine gegen Schwätzigkeit (Knappheitsregeln)

Das zentrale Differenzierungsmerkmal dieses Skills: In jede generierte Vorlage werden **Knappheitsregeln** wortgleich in das Instruktionsfeld eingebaut. Diese kurzen Bausteine bewirken, dass AIS.chat im Einsatz deutlich knapper antwortet: keine Floskeln, keine ausufernden Erklärungen, keine ungefragten Zusatzideen.

Ohne diese Bausteine antworten AIS.chat-Vorlagen typischerweise zu lang, zu selbsterklärend, mit Begrüßungsfloskeln und „Möchten Sie noch …?"-Angeboten am Ende. Die Knappheitsregeln verhindern das durch eine wortgleich übernommene Anweisung im passenden Block des Instruktionsfelds.

Regeln zur Verwendung:
- **Wortgleich**: Nicht umformulieren, nicht sinngemäß anpassen, nicht kürzen. Der Wortlaut ist erprobt und ergibt zusammen die Wirkung.
- **Pflicht**: Jede vom Skill generierte Vorlage enthält mindestens einen der folgenden Bausteine. Das ist nicht verhandelbar.
- **Platzierung**: Am Ende des passenden Blocks im Instruktionsfeld, durch Absatzumbruch abgetrennt.

### BAUSTEIN_DIALOG

Zielvorlagen:
- Dialogpartner: am Ende des Verhalten-Blocks
- Lernszenario: am Ende des VERHALTEN-Blocks

Wortlaut:

> Antworte knapp und präzise. Vermeide Floskeln, Einleitungen und Zusammenfassungen. Formuliere so kurz wie nötig, damit die Aussage oder Rückfrage trägt. Stelle höchstens eine gezielte Rückfrage pro Antwort. Höre auf, sobald die Aufgabe erfüllt ist. Füge keine Zusatzideen oder weiterführenden Hinweise hinzu, wenn nicht danach gefragt wurde. Schreibe im normalen Fließtext. Setze Überschriften, Zwischenüberschriften, Trennlinien, Fettungen oder Aufzählungen nur ein, wenn die Aufgabe es ausdrücklich verlangt; bei kurzen Antworten von wenigen Sätzen verzichte darauf.

### BAUSTEIN_DIALOG_NEG

Zielvorlage:
- Dialogpartner, nur dann verwenden, wenn ein expliziter Anti-Verhalten-Block formuliert wird. Ist kein eigenes Feld mehr, sondern optionaler Unterblock im Instruktionsfeld. Wenn kein Anti-Verhalten-Block existiert, weglassen.

Wortlaut:

> Keine Begrüßungsfloskeln, keine Meta-Kommentare über die eigene KI-Natur, keine ausschweifenden Erklärungen. Keine Wiederholung der Frage. Keine Aufzählungen, wenn ein Satz reicht. Keine Zusatzideen und keine "Möchten Sie noch …?"-Angebote am Ende einer Antwort. Keine Überschriften, keine Zwischenüberschriften, keine Trennlinien, keine Fettungen, keine Tabellen. Schreibe wie eine Person im Gespräch.

### BAUSTEIN_WERKZEUG

Zielvorlage:
- Assistent, am Ende des Instruktionsfelds (nach FORMAT-Block bzw. dem letzten inhaltlichen Block)

Wortlaut:

> Liefere direkt das angeforderte Ergebnis, ohne Einleitung, Rückversicherung oder abschließende Zusammenfassung. Keine Floskeln, kein Meta-Text über die Aufgabe. Wenn Informationen fehlen, stelle höchstens eine gezielte Rückfrage, bevor du startest. Nutze das vorgegebene Ausgabeformat strikt. Strukturiere nur das Ergebnis selbst, kein dekoratives Beiwerk und keine Trennlinien zwischen kurzen Abschnitten. Stoppe, wenn die Aufgabe erfüllt ist.

### Regel zur Platzierung

- Der Baustein steht am Ende des passenden Blocks im Instruktionsfeld, durch einen Absatzumbruch abgetrennt.
- Inhaltlich davor steht die spezifische Rollen- oder Verhaltensbeschreibung für den konkreten Fall.
- Zeichenzählung: Der Baustein wird in die 10000-Zeichen-Grenze des Instruktionsfelds eingerechnet. Bei den 500er-Feldern (Arbeitsauftrag, Einstiegsfrage, Kurzbeschreibung, Promptvorschlag) wird kein Baustein eingefügt.

## Qualitätsprinzipien (gelten für alle Vorlagentypen)

- **Knapp vor ausführlich**: Lieber kurze, klare Anweisungen als ausufernde Erklärungen. Auch wenn das Instruktionsfeld 10000 Zeichen erlaubt, wird es nur dann lang, wenn Kontextmaterial mitgegeben wird. Sonst ist kurz und strukturiert besser.
- **Dialogisch denken**: AIS.chat soll im Einsatz nachfragen und zum Denken anregen, nicht monologisieren. Das wird durch die Pflichtbausteine erzwungen.
- **Zeichenlimits sind hart**: Überschreitungen werden von AIS.chat abgeschnitten. Kürze elegant statt abrupt. Zähle Zeichen inklusive Leerzeichen, inklusive Pflichtbaustein.
- **Rollenkonsistenz explizit machen**: Bei Dialogpartnern immer explizit formulieren, dass die Figur in der Rolle bleibt, auch wenn die Lehrkraft das nicht erwähnt hat.
- **Keine didaktischen Meta-Kommentare** in den generierten Texten. Die Texte gehen direkt in AIS.chat-Formulare. Sie sprechen Lernende an oder instruieren die KI, nicht die Lehrkraft.
- **Sprachmodell-Feld nur mit Modellname**: Das Feld „Sprachmodell" in der Ausgabe enthält ausschließlich den Modellnamen (z.B. `GPT-5 nano`). Eine Begründung steht **nicht** in diesem Feld, da es 1:1 in das AIS.chat-Formular kopiert wird, dort ist nur Platz für einen Modellnamen.
- **Modellwahl konservativ, Entscheidung bei der Lehrkraft**: Setze im Sprachmodell-Feld als Default ein effizientes Modell der unteren Leistungsklasse ein. Treffe die Wahl im Zweifel zugunsten des effizienteren Modells, die Lehrkraft kann jederzeit hochstufen, das Modellangebot unterscheidet sich nach Bundesland und ändert sich regelmäßig. Empfehle **nicht** automatisch ein stärkeres Modell, nur weil die Vorlage „komplex" wirkt. Im Empfehlungs-Abschnitt der Ausgabe immer auf die Modell-Übersicht verweisen: <https://mgkurz.github.io/ki-modell-auswahl/>
- **Strukturierung des Instruktionsfelds mit Markdown**: Das Instruktionsfeld geht als Text in den Systemprompt des Modells ein. AIS.chat bettet es in einen durchgängig in Markdown formatierten Systemprompt ein (Hauptsektionen mit `##`, das Lehrkraft-Feld als Body unter einer `###`-Überschrift), rendert die Antworten als Markdown (`react-markdown` mit `remark-gfm`) und weist das Modell systemseitig ausdrücklich an, Markdown zu nutzen. Strukturiere das Instruktionsfeld daher selbst in Markdown:
  - **Block-Überschriften als Markdown der vierten Ebene** (`#### Rolle`, `#### Kontext`, `#### Verhalten`, `#### Format`; beim Dialogpartner `#### Simulierte Person`, `#### Zielgruppe`, `#### Kontext`, `#### Verhalten`, kein FORMAT-Block). AIS.chat hängt das Instruktionsfeld unter eine `###`-Überschrift; `####` setzt die Hierarchie eine Ebene tiefer sauber fort, ohne mit den AIS.chat-eigenen Ebenen zu kollidieren. Mixed Case, keine Großbuchstaben.
  - **Alternative für sehr kurze Vorlagen**: fette Labels statt Überschriften (`**Rolle**`, `**Verhalten**`), wenn eine eigene Heading-Ebene überdimensioniert wäre.
  - **Listen** mit Bindestrich (`- `), da AIS.chat GitHub-Flavored Markdown rendert. Nummerierte Listen nur, wenn eine Reihenfolge gemeint ist.
  - Ein Leerzeilen-Abstand zwischen Block-Überschrift und Block-Text.
  - **Wichtige Unterscheidung, nicht verwechseln**: Markdown-Struktur *im Instruktionsfeld* hilft dem Modell beim Parsen der Konfiguration. Das ist etwas anderes als die Struktur *in der Antwort* des Bots. Wie der Bot antwortet (bei Dialog: knapp, im Fließtext, ohne Überschriften), steuern allein die Knappheitsbausteine. Ein mit `####` gegliedertes Instruktionsfeld erzeugt also keinen mit Überschriften gegliederten Chat, sofern der Knappheitsbaustein das unterbindet.
  - Bei komplexen Vorlagen (z.B. funktionaler Dialogpartner im „Sid"-Stil) ist eine abweichende Struktur erlaubt, sollte aber bewusst gewählt werden.
  - **Trade-off, transparent**: Das offizielle „Beispiel anzeigen" im AIS.chat-Formular nutzt Großbuchstaben- bzw. Mixed-Case-Zeilen ohne Markdown. Wer maximale optische Übereinstimmung mit diesem Formular-Beispiel sucht, kann bei Großbuchstaben bleiben; der funktionale Unterschied fürs Modell ist gering. Dieser Skill wählt bewusst Markdown (`####`), weil es konsistent mit dem tatsächlichen, durchgängig in Markdown gehaltenen Systemprompt-Container von AIS.chat ist.

## Ausgabeformat

Gib die Felder in exakt der Reihenfolge und mit exakt den Titeln aus, die in der jeweiligen Referenzdatei definiert sind. Unter jedem Feldtitel steht genau ein zusammenhängender Text, kein zusätzlicher Kommentar, keine Erklärung, keine Formatierung außer dem Text selbst und dem Markup innerhalb des Instruktionsfelds. Die Ausgabe muss 1:1 in die AIS.chat-Formulare kopierbar sein.

Nach den Feldern: ein kurzer Abschnitt „Empfehlungen" mit genau dieser Struktur:

- **Schultyp / Klassenstufe / Fach**: aus der Eingabe übernommen oder Platzhalter
- **Modellwahl prüfen**: Der Vorschlag im Feld „Sprachmodell" ist ein konservativer Startpunkt. Welches Modell zum konkreten Einsatz, Tokenvolumen und Bundesland passt, entscheidet die Lehrkraft. Übersicht und Empfehlungen: <https://mgkurz.github.io/ki-modell-auswahl/> (Projektseite: <https://github.com/mgkurz/ki-modell-auswahl>)
- **Hintergrundwissen**: Hinweis, dass in AIS.chat Dateien hochgeladen werden können (docx, pdf, md, txt). Dateien müssen **textbasiert und gut lesbar** sein, keine reinen Bild-PDFs oder gescannten Grafiken ohne OCR-Textlayer, da AIS.chat diese nicht verarbeiten kann. Bei komplexen Vorlagen Modularisierung mit Präfixen empfehlen (`00_CORE_…`, `01_…`)
- **Weblinks**: Falls konkrete, geeignete Quellen bekannt sind, kurz nennen. Sonst Hinweis, dass die Lehrkraft 1-3 passende Webquellen ergänzen sollte
- **Tokenvolumen und Nutzungszeit** (nur bei Lernszenario und Dialogpartner): Default 10 % / 45 Minuten, an Gruppengröße und Unterrichtseinheit anpassen
- **Freigabe**: Schulintern und/oder via Link, je nach beabsichtigter Reichweite

**Nach dem Empfehlungs-Abschnitt folgt nichts mehr.** Keine Selbst-Kritik an der eigenen Generierung, keine didaktische Meta-Reflexion, keine Hinweise auf mögliche Varianten, keine Begründung von Designentscheidungen, keine Rückblick-Zusammenfassung. Wenn während der Generierung echte Zweifel an einer Designentscheidung bestehen, gehören diese als **Rückfrage vor der Ausgabe**, nicht als Anhang danach. Die Ausgabe endet mit dem letzten Stichpunkt des Empfehlungs-Abschnitts.
