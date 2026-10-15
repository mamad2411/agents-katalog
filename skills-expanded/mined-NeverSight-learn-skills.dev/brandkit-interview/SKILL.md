---
name: brandkit-interview
description: Führt ein hartnäckiges Interview, aus dem eine belastbare Markenbeschreibung entsteht (brand interview, brand identity, design system, visual identity). Fragt Positionierung, Persönlichkeit, Farben, Typografie, Tonfall und Verbotslisten ab und schreibt daraus eine ausführliche Rohfassung. Nutze diesen Skill, sobald jemand eine Marke, ein Brand Kit, ein Designsystem oder eine visuelle Identität erarbeiten will, oder sagt, seine Webseiten und Grafiken sähen beliebig aus.
license: MIT
---

# Markeninterview

Dieser Skill ist Schritt 2 von 4, zwischen `brandkit-setup` und `brandkit-build`.

Ergebnis ist **eine Datei**: eine ausführliche Rohfassung der Marke, aus der
Schritt 3 das kurze, verbindliche Kit verdichtet.

## Warum überhaupt ein Interview

Ohne Marke fällt jede Designentscheidung neu und zufällig aus. Das Ergebnis
sieht dann aus wie das, was Sprachmodelle statistisch am häufigsten gesehen
haben: blau-violette Verläufe, abgerundete Karten, Inter als Schrift. Nicht
falsch, aber austauschbar.

Ein Interview zwingt zu Festlegungen, die man selbst nie trifft, solange
niemand fragt. Die Person weiß fast alles, was hier gebraucht wird. Sie hat es
nur nie ausgesprochen.

## Vorgehen

Rufe zuerst den Skill `grill-with-docs` auf. Er startet ein Interview, das in
Runden arbeitet: alle Fragen, die gerade beantwortbar sind, kommen gemeinsam,
nummeriert, jeweils mit einer Empfehlung. Dann wird die Antwort abgewartet,
bevor die nächste Runde folgt.

Ist `grill-with-docs` nicht installiert, führe das Interview nach demselben
Muster selbst und weise einmal darauf hin, dass `brandkit-setup` ihn
nachinstalliert.

Die Achsen unten sind der Fragenvorrat, keine Checkliste zum Abarbeiten. Was
schon beantwortet ist, wird nicht nochmal gefragt.

## Die Achsen

Die Reihenfolge ist Absicht. Farben ohne Positionierung zu wählen führt zu
Geschmacksdiskussionen, die nichts entscheiden.

**1. Kern.** Was ist das in einem Satz? Für wen, und wogegen grenzt es sich ab?
Was soll jemand über die Marke sagen, wenn er sie weiterempfiehlt?

**2. Persönlichkeit.** Drei bis sechs Eigenschaften. Nützlicher als die
Zustimmung ist die Ablehnung: Was soll die Marke ausdrücklich **nicht** sein?
„Nie corporate" trifft schärfer als „modern".

**3. Struktur.** Eine Dachmarke über allem, oder mehrere Untermarken? Wo steht
der Klarname der Person, wo der Markenname? Diese Frage wird gern übersprungen
und rächt sich beim ersten Logo.

**4. Vorbilder und Gegenbilder.** Welche zwei, drei Marken treffen den Ton?
Und welche liegen nah dran, sind aber falsch? Das Gegenbeispiel schärft mehr
als das Vorbild.

**5. Farbe.** Ein Grundton (dunkel, hell, warm, kühl) und höchstens ein bis zwei
Akzente. Frage nach einem Akzent, der Bedeutung trägt, nicht nach einer
Lieblingsfarbe. Kläre außerdem: Gibt es einen hellen Modus, oder ist alles
dunkel, auch Druck und Dokumente? Diese Entscheidung schlägt später überall
durch und ist teuer, wenn sie fehlt.

**6. Typografie.** Zwei bis drei Rollen genügen: Display für Überschriften, Body
für Fließtext, optional Mono für Zahlen, Preise, Versionen, technische Labels.
Die Mono-Rolle wird unterschätzt und ist oft das, was eine technische Marke
erkennbar macht.

**7. Raster und Anmutung.** Wie viel Leerraum? Symmetrisch oder redaktionell
asymmetrisch? Runde Ecken oder Kanten? Schatten, Verläufe, Glaseffekte: ja oder
nein? Ein klares Nein hier ist mehr wert als drei vage Ja.

**8. Bausteine.** Welche Elemente kommen immer wieder vor? Preistabelle,
Vergleichstabelle, FAQ, Kundenstimme, Formular, Diagramm. Und gibt es ein
Signature-Element, an dem man die Marke sofort erkennt?

**9. Sprache.** Sprache und Ansprache (du oder Sie). Ein gutes und ein schlechtes
Beispielsatzpaar für dieselbe Aussage. Und eine **Verbotsliste**: Wörter, die
nie vorkommen. Das ist der wirksamste Teil des ganzen Kits, weil er sich
maschinell prüfen lässt.

**10. Formate.** Was wird tatsächlich gebaut? Webseite, Thumbnails, Slides,
Dokumente, Social Posts? Notiere die Pixelmaße, die dabei anfallen.

**11. Bilder.** Fotografie, KI-erzeugte Bilder, Illustration, oder gar keine
Bilder? Wenn KI-Bilder vorkommen: Welche Motive passen, welche sind verboten?
Diese Antwort braucht Schritt 4 direkt.

## Wo du bohren musst

Bei drei Antworten lohnt sich Nachfragen, weil sie fast immer zu weich kommen:

- „Modern und professionell" beschreibt nichts. Frage nach dem Extrem: brutal
  minimal, maximalistisch, redaktionell, Luxus, verspielt, industriell.
- „Eigentlich mag ich alle Farben" heißt, die Person hat noch nicht verstanden,
  dass Einschränkung der ganze Sinn ist. Frage nach dem Anteil: Wie viel Prozent
  einer Fläche darf der Akzent belegen?
- Eine leere Verbotsliste heißt, es wurde nicht nachgedacht. Jede Marke hat
  Dinge, die sie nicht sein will.

## Die Rohfassung schreiben

Schreibe das Ergebnis in eine Datei, üblicherweise `MARKE-ROH.md` im künftigen
Brand-Ordner. Sie darf lang und ausführlich sein, mehrere hundert Zeilen sind
normal. Sie ist das Archiv, nicht das Arbeitsdokument.

Halte fest, **warum** eine Entscheidung so fiel, nicht nur wie sie ausfiel.
Schritt 3 kürzt die Begründungen weg, aber wer in einem Jahr etwas ändern will,
braucht sie.

Trage konkrete Werte ein, wo sie feststehen: Hex-Farben, Schriftnamen,
Pixelgrößen. Wo etwas offen blieb, schreibe das ausdrücklich hin, statt einen
plausiblen Wert zu erfinden. Eine erfundene Farbe steht sonst zwei Jahre später
noch im Kit, ohne dass sie je jemand entschieden hat.

Am Ende: Sag, dass die Rohfassung steht, nenne den Pfad, und weise auf
`brandkit-build` hin, der daraus das benutzbare Kit macht.
