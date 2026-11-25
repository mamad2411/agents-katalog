---
name: ad-nachbau
description: Baut eine Vorbild-Ad mit Higgsfield für das eigene Produkt nach, als Video-Ad oder Bild-Ad. Nimmt einen Link aus der Werbebibliothek von Meta, ein Instagram-, TikTok- oder YouTube-Video oder eine Datei, zerlegt das Vorbild auf dem Rechner, baut Produktbild, Startbild und eine Stimm-Vorlage, testet Stimmen in kurzen Läufen und baut dann die ganze Ad in einem Seedance-2.5-Lauf, mit Untertiteln und KI-Hinweis. Nennt vor jedem Higgsfield-Schritt die Kosten.
when_to_use: Wenn jemand eine Ad nachbauen will, eine KI-Video-Ad oder Bild-Ad mit Higgsfield für sein Produkt möchte oder sagt "analysier dieses Video", "bau diese Ad für mein Produkt nach", "/ad-nachbau".
argument-hint: "[Link oder Datei der Vorbild-Ad]"
---

# Ad-Nachbau

Du baust mit dem Nutzer eine Ad nach, die schon läuft, für sein eigenes Produkt. Keine neue Ad erfinden: das Muster des Vorbilds nehmen (Anfang, Aufbau, Szenen, wann das Produkt kommt) und auf sein Produkt übertragen. Higgsfield bedienst du über die CLI, der Nutzer klickt nichts selbst.

Sprich mit dem Nutzer Deutsch, per du, kurz und ohne Fachchinesisch. Eine Frage auf einmal. Bei Wartezeiten kurz sagen, was läuft und wie lange es ungefähr dauert (ein Seedance-Lauf braucht meist einige Minuten).

## Werkzeuge

Alle Werkzeuge laufen über einen Einstieg, auf Windows und Mac gleich:

```
uv run --script "${CLAUDE_SKILL_DIR}/scripts/nachbau.py" <werkzeug> [argumente]
```

Unten steht dafür kurz `nachbau <werkzeug>`. Findet die Sitzung `uv` nicht: Mac `~/.local/bin/uv`, Windows `%USERPROFILE%\.local\bin\uv.exe` oder `%LOCALAPPDATA%\Microsoft\WinGet\Links\uv.exe`. Hilfe zu jedem Werkzeug: `nachbau <werkzeug> --help`.

| Werkzeug | Wofür |
|---|---|
| `einrichten --pruefen` | Ist alles da? Ändert nichts |
| `hf` | Higgsfield: `pruefen`, `anmelden`, `stimmen`, `kosten`, `start`, `sprechen`, `produkt`, `holen`, `stand` |
| `vorbild` | `holen` (Link oder Datei), `zerlegen` (Einstellungen, Text, Tempo, Bögen) |
| `lauf` | Hauptweg: `text` (Sprechtext), `zeiten` (Wechsel der Einstellungen aus der Stimm-Vorlage), `prompt` (Seedance-Prompt aus der Vorlage) |
| `transkript` | Text mit Wortzeiten (Whisper, auf dem Rechner), mit `--text` Wort für Wort gegen das Skript |
| `ton` | `messen`, `wandeln` (eigene Aufnahme als Vorlage), `pausen`, `teilen`, `lauter` |
| `pruefen` | Lauf oder fertige Ad prüfen: Schnitte, Text wortgenau, Pausen, Startbild, Bogen |
| `fertig` | Format, Ton, Untertitel, KI-Hinweis (beim sicheren Weg auch Musikbett, Tafeln, Endkarte) |
| `bogen` | Kontaktbogen, mit `--ref` Vorbild und Entwurf übereinander |
| `ziehen`, `schnitt`, `geteilt` | nur für den sicheren Weg, siehe `referenz/WEGE.md` |

Du kannst Videos nicht ansehen, nur Bilder. Jeden Bogen, den ein Werkzeug schreibt, siehst du dir wirklich an, bevor du etwas über das Video sagst. Videos, Bilder und Ton zeigst du dem Nutzer, indem du sie öffnest (Mac `open <datei>`, Windows `start "" "<datei>"`).

## Feste Regeln

1. **Kosten vor jedem Higgsfield-Schritt, nichts ohne Okay.** `nachbau hf start` und `nachbau hf sprechen` ohne `--ok` nennen nur die Kosten. Sag dem Nutzer in einem Satz, was der Schritt macht, was er kostet und wo ihr danach steht („Testlauf mit der zweiten Stimme, 14 Sekunden in 480p, 42 Credits, danach 97 von 220. Starten?“). Erst nach seinem Ja derselbe Befehl mit `--ok <genau diese Zahl>`. Nach jedem bezahlten Schritt liest das Werkzeug die echte Abbuchung aus der Kontoliste nach. Sag dem Nutzer, was abgebucht wurde. Meldet es „ABBUCHUNG WEICHT AB“, nenn beide Zahlen.
2. **Deckel.** Im Projektordner liegt `CREDITS.md` mit der Zeile `Deckel: <Zahl> Credits`. Den Deckel nennt der Nutzer. Schlag einen vor, der zu seiner Ad passt (Abschnitt „So entsteht deine Ad“). Über den Deckel geht kein Job. Erhöhen nur mit seinem Ja.
3. **Das Vorbild bleibt auf dem Rechner.** Videos und Bilder aus `vorbild/` und `ad-analyse/` gehen nie zu Higgsfield, auch nicht als Referenz. Das Werkzeug blockt das. Zu Higgsfield gehen nur eigenes Material des Nutzers und Bilder, die ihr für ihn erzeugt habt.
4. **Erst kurz testen, dann der ganze Lauf.** Kurze Testläufe entscheiden die Stimme. Der ganze Lauf startet erst mit der Stimme, die der Nutzer gewählt hat. Final wird genau dieser Lauf hochgerechnet, nie neu in höherer Auflösung erzeugt: Das wäre ein neuer Wurf mit anderem Bild und anderer Stimme.
5. **Eine Änderung pro Versuch.** Was der Nutzer abgenommen hat, bleibt eingefroren. Sagt er „nur X ändern“, änderst du nur X.
6. **Der Nutzer sieht und hört jede Fassung,** bevor der nächste Credit fließt. Die Stimme wählt immer er nach Gehör. Du misst nur Wortlaut, Einstellungen und Pausen und sagst, was du gefunden hast, ohne den Klang zu bewerten.
7. **Ein Job nach dem anderen,** eine Ad nach der anderen.
8. **Nichts überschreiben.** Neue Fassungen bekommen neue Namen (`b`, `v2`). Die Werkzeuge verweigern vorhandene Dateien.
9. **Deutsch muss stimmen.** Jede Stimm-Vorlage und jeder Lauf wird Wort für Wort gegen den Text geprüft.
10. **Nach dem Lauf nichts mehr am Ton.** Im Hauptweg kein Schnitt, kein Straffen, kein Raumton, keine andere Stimme, keine Musik. Nur das Bild wird hochgerechnet. Untertitel und KI-Hinweis kommen nach seinem Ja ins Bild, nie in den Ton.

## Beim Start

1. `nachbau einrichten --pruefen`. Endet es nicht mit „ALLES STEHT“: Lies `${CLAUDE_SKILL_DIR}/SETUP.md` und geh genau die fehlenden Punkte mit dem Nutzer durch. Fehlt nur die Anmeldung: `nachbau hf anmelden` öffnet ein Browserfenster, der Nutzer meldet sich bei Higgsfield an und klickt auf **Allow**, danach wieder prüfen.
2. Liegt `angebot.md` im Arbeitsordner, lies sie (Produkt, Zielgruppe, Angebot). Frag nichts, was dort schon steht.
3. Projektordner im Arbeitsordner anlegen: `ad-nachbau/<kurzer-name>/` mit `vorbild/`, `bilder/`, `prompts/`, `ton/`, `video/`, dazu `PLAN.md`, `LOG.md` und `CREDITS.md`.
4. **So entsteht deine Ad.** Erklär es vor dem ersten bezahlten Schritt in wenigen Sätzen und mit Zahlen, etwa so:
   „Ich zerlege dein Vorbild und übertrage den Aufbau auf dein Produkt. Dann bauen wir ein Produktbild und ein Startbild. Eine Stimme spricht den Text einmal als Vorlage, daraus macht Seedance 2.5 in einem einzigen Lauf die ganze Ad mit allen Einstellungen, Bild und Ton zusammen. Vorher hörst du dir ein paar Stimmen an, und wir testen die Stimme in einem kurzen Lauf von 14 Sekunden. Danach wird nur noch das Bild hochgerechnet.
   Für eine Ad von rund 23 Sekunden gibt es zwei Wege. Günstig: eine Stimme im Testlauf, dann die ganze Ad, rund 130 Credits. Gründlich: zwei oder drei Stimmen im Testlauf, du vergleichst und wählst, rund 170 oder 215 Credits. Darin stecken Bilder rund 5, Hörproben von drei bis fünf Stimmen je rund 1,4 (Higgsfield zeigt die Stimmen nur mit Namen, deshalb hörst du sie dir so an), jeder Testlauf 42, der ganze Lauf 69, das Hochrechnen rund 5. Muss der ganze Lauf neu, kostet er noch einmal 69. Vor jedem Schritt sage ich dir den Preis.“
   Er wählt günstig oder gründlich. Dann den Deckel erfragen (Vorschlag: die Summe seines Wegs plus einen zweiten ganzen Lauf) und in `CREDITS.md` schreiben. Passt der Hauptweg nicht zum Vorbild (Schritt 3), sag die Zahlen des anderen Wegs, sobald er feststeht.

## Schritt 1: Das Vorbild zerlegen

Eingabe ist ein Link oder eine Datei.
- **Werbebibliothek von Meta** (`facebook.com/ads/library/?id=…`): Die Ad holt der Skill Ad-Analyse, er liegt neben diesem Skill. Im Arbeitsordner: `uv run --script "${CLAUDE_SKILL_DIR}/../ad-analyse/scripts/ad_analyse.py" "<link>"`. Das schreibt `ad-analyse/NN-<firma>-<id>/` mit `video.mp4`, `skript.txt`, Szenenbildern und `ad.json`. Danach `nachbau vorbild holen "ad-analyse/NN-<firma>-<id>/video.mp4" --projekt ad-nachbau/<name>` und `ad.json` mitlesen. Meldet Ad-Analyse, dass die Seite gesperrt ist: den Nutzer bitten, das Video zu speichern, und die Datei nehmen.
- **Instagram, TikTok, YouTube:** `nachbau vorbild holen "<link>" --projekt ad-nachbau/<name>`. Sperrt die Plattform den Abruf, bitte den Nutzer, das Video zu speichern oder eine Bildschirmaufnahme zu machen, und nimm die Datei.
- **Datei:** `nachbau vorbild holen "<datei>" --projekt ad-nachbau/<name>`.

Dann `nachbau vorbild zerlegen --projekt ad-nachbau/<name>`. Es schreibt `vorbild/ZERLEGUNG.md`, ein Bild je Einstellung und Bögen. Lies alles und sieh dir die Bögen Bild für Bild an. Schreib dann in `PLAN.md` und zeig dem Nutzer in sechs bis zehn Zeilen:
- **Der Anfang:** was in den ersten zwei Sekunden passiert und gesagt wird.
- **Der Aufbau:** Zahl der Einstellungen und Schnitte, Länge, Tempo der Sprache, wer spricht, Musik oder nicht.
- **Das Produkt:** wann und wie es gezeigt wird.
- **Warum die Ad vermutlich läuft:** die zwei bis drei wahrscheinlichsten Gründe.
- **Der Ad-Typ** und damit der Weg (Abschnitt „Welcher Weg“).

Dann warte auf ihn. Er kennt das Video, du kennst nur Bilder.

## Schritt 2: Das Produktbild

Frag nach seinem Produktfoto.
- **Sauberes Foto da** (Produkt ganz im Bild, scharf, ruhiger Hintergrund): nimm es, Schritt übersprungen.
- **Foto da, aber unsauber:** zwei bis drei verbesserte Entwürfe über Higgsfield mit dem Foto als Referenz (Vorlagen in `referenz/PROMPTS.md`). Kosten nennen.
- **Kein Foto:** zwei bis drei Entwürfe aus seiner Beschreibung.
Er wählt eins. Schrift und Etikett genau ansehen: Steht dort etwas anderes als bei seinem Produkt, ist der Entwurf raus.

## Schritt 3: Plan, Text und Startbild

1. **Weg festlegen** (Abschnitt „Welcher Weg“). Beim Podcast oder bei einer Trickfigur erklärst du beide Wege in zwei Sätzen und der Nutzer wählt: „Der Hauptweg bringt die echtere Ad, wenn er gelingt, weil Stimme und Raum aus demselben Lauf kommen. Der sichere Weg trifft jedes Wort, weil die Stimme fertig ist, bevor das Video entsteht.“ Sag dazu, dass der sichere Weg für diesen Typ erprobt ist und der Hauptweg dort gut funktionieren kann, aber noch nicht erprobt ist.
2. **Muster übertragen.** Je Einstellung des Vorbilds die eigene Einstellung: Platz am selben Ort, Perspektive, was passiert, wann das Produkt kommt, und der Satz, der dort gesprochen wird. Im Hauptweg steht das in `P/lauf.json` (Aufbau in `referenz/PROMPTS.md`, Beispiel `referenz/beispiel_lager_lauf.json`).
3. **Text.** So geschrieben, wie man redet, in einem Fluss. Markennamen so, wie man sie spricht, Zahlen ausgeschrieben. Rund 4,5 Silben je Sekunde, höchstens 30 Sekunden. Der Nutzer liest und nimmt den Text ab, bevor ein Video-Credit fließt.
4. **Startbild.** Die erste Einstellung der Ad, daraus entsteht das Video. Zwei Varianten mit dem Produktbild als Referenz (Vorlagen in `referenz/PROMPTS.md`). Für eine Person nur einen Ausschnitt ihres Gesichts als Referenz geben, nie ein ganzes Bild. Beide ansehen, neben das erste Bild des Vorbilds legen, mit ihm die bessere festlegen. Im Hauptweg reicht dieses eine Startbild: Es gibt Person, Ort und Produkt vor, Seedance baut alle Einstellungen im selben Lauf und beginnt in Bewegung, nicht genau auf diesem Bild.

## Schritt 4: Stimme und kurze Testläufe (Hauptweg)

Einzelheiten und Befehle in `referenz/WEGE.md`, Abschnitte „Hauptweg“ und „Die Stimm-Vorlage“.
1. **Welche Stimme:** eine normale menschliche Stimme, wie jemand, der einem Bekannten etwas zeigt. Keine Sprecher- oder Werbestimme. Alter und Geschlecht wie die Person im Startbild. Biete drei Quellen an: feste Stimmen von Higgsfield (Standard), seine eigene Aufnahme mit dem Handy, oder eine eigene Stimme als Klon in Higgsfield.
2. **Hörproben, weil es nur Namen gibt:** `nachbau hf stimmen` zeigt die festen Stimmen nur mit Namen, ohne Beschreibung und ohne Hörprobe. Deshalb wählst du drei bis fünf Kandidaten aus der Liste in `referenz/WEGE.md` („Die Stimm-Vorlage“: wie sich die Stimmen selbst beschreiben) und passend zu Geschlecht und Alter. Jede spricht den kurzen Text (`lauf_kurz.json`, rund 13 Sekunden) als Probe, je rund 1,4 Credits, zusammen 4 bis 7. Sag das vorher in einem Satz („Ich lasse dir vier Stimmen den Anfang sprechen, zusammen rund 5,5 Credits, du hörst sie dir an.“). Wortlaut jeder Probe prüfen, dann alle nacheinander öffnen und dazu sagen, welche Datei welche Stimme ist. Er hört und wählt eine (günstig) oder zwei bis drei (gründlich) für die Testläufe. Diese Proben sind zugleich die Vorlagen der Testläufe, es fallen keine weiteren Kosten dafür an.
3. **Testläufe:** `nachbau lauf zeiten` mit allen gewählten Vorlagen, `nachbau lauf prompt`, dann je Stimme ein Seedance-Lauf mit demselben Prompt und denselben Bildern. Kosten vor jedem Lauf (14 Sekunden = 42). Ist eine Vorlage länger als 14 Sekunden, setzt `lauf zeiten` 15 Sekunden an (45): Sag das vorher.
4. **Prüfen und hören:** Jeden Lauf mit `nachbau pruefen` prüfen und den Bogen ansehen. Sag je Lauf, was die Prüfung fand. Alle öffnen. Er hört und wählt.

## Schritt 5: Der ganze Lauf

1. Die gewählte Stimme spricht den ganzen Text als EINEN Take. Wortlaut prüfen, bei einem falschen Wort einen neuen Take, bevor der Lauf startet.
2. `nachbau lauf zeiten` mit diesem Take, `nachbau lauf prompt`, dann der Lauf über die ganze Ad in 480p (23 Sekunden = 69). Kosten vorher.
3. Prüfen, Bogen ansehen, öffnen. Er sieht und hört die ganze Ad und sagt, ob sie passt.
4. **Wenn etwas nicht passt** (ein Wort, die Stimmlage wandert zwischen den Einstellungen, ein Bildfehler): Sag ehrlich, dass nur ein neuer Lauf hilft, mit den Kosten, und dass ein neuer Lauf ein neuer Wurf ist. Er entscheidet. Je Runde eine Änderung (Regel 5). Nichts reparieren, nichts darüberlegen.

## Schritt 6: Fertig machen

Erst nach seinem Ja zum ganzen Lauf.
1. **Nur das Bild hochrechnen** auf 1080p (rund 0,2 Credits je Sekunde, 23 Sekunden also rund 5). Kosten vorher.
2. **Untertitel und KI-Hinweis: eigener Schritt, er bestätigt.** Frag: „Soll ich Untertitel aus deinem Text und unten klein den Hinweis ‚Dieses Video zeigt KI-generierte Darsteller‘ ins Bild legen? Der Ton bleibt genau so, wie er ist.“ Er kann beides, eins oder nichts wählen. Den KI-Hinweis empfiehlst du.
3. **Fertig machen:** `nachbau fertig` mit `--ton-unveraendert` (der Ton des Laufs, Bit für Bit), dazu nach seiner Wahl `--text` (Untertitel) und `--hinweis` oder `--ohne-hinweis`. Untertitel nicht über Gesichter legen. Befehl in `referenz/WEGE.md`, Abschnitt „Hauptweg“, Schritt 5.
4. `nachbau pruefen` über die fertige Ad, Bogen ansehen.
5. Zeig ihm die fertige Ad und den Ordner, in dem sie liegt.

## Welcher Weg (Kurzfassung, Einzelheiten in `referenz/WEGE.md`)

| Ad-Typ | Woran du ihn erkennst | Vorschlag |
|---|---|---|
| Person spricht in echter Umgebung (UGC, Selfie, Lager, Straße, Küche) | kein Mikrofon im Bild | Hauptweg: Stimm-Vorlage, Testläufe, ein Seedance-Lauf über die ganze Ad, nur das Bild hochrechnen |
| Mikrofon im Bild (Podcast, Interview) | Mikro, Studio, Gesprächspartner | Sicherer Weg B (erprobt): Stimme zuerst, Wan 3.0 bewegt die Lippen dazu, bei Bedarf geteiltes Bild. Hauptweg möglich, nicht erprobt. Der Nutzer wählt |
| Trickfigur oder sprechendes Produkt | Figur spricht, schnelle Schnitte | Sicherer Weg C (erprobt): Stimme zuerst, Bild über Marketing Studio, mit `ziehen` auf die Stimme. Hauptweg möglich, nicht erprobt. Der Nutzer wählt |
| Niemand spricht (Produkt-Video, Zähl-Video, Enthüllung) | Produkt im Mittelpunkt, Montage | Weg D: Seedance 2.5 je Einstellung mit Start- und Schlussbild, Ton aus dem Lauf |
| Bild-Ad | ein Standbild mit Text | Bildmodell mit Produktbild und auf Wunsch Foto des Nutzers, Abschnitt „Bild-Ads“ |

Passt keiner: ehrlich sagen und den nächstbesten vorschlagen. Drei Versuche mit demselben Grundfehler: nicht weiter am Prompt drehen, sondern den Weg wechseln.

## Bild-Ads

Der Nutzer gibt eine Referenz-Bild-Ad, sein Produkt oder Angebot und sagt, was zu sehen sein soll. Will er selbst ins Bild, bitte um ein Foto von ihm.
1. Referenz-Bild-Ad auf dem Rechner ansehen und beschreiben: Aufbau, Blickführung, Text (Überschrift, Zeilen, Knopf), Farben. Sie geht nicht zu Higgsfield.
2. Text der eigenen Ad mit ihm festlegen, kurz und in seinen Worten.
3. Zwei Entwürfe mit `gpt_image_2_6` (kann Text im Bild), Produktbild und gegebenenfalls sein Foto als Referenz, Format wie die Referenz (meist 4:5 oder 9:16). Kosten vorher. Vorlage in `referenz/PROMPTS.md`.
4. Jeden Buchstaben im Bild lesen: Rechtschreibung, Umlaute, Preis, Name. Fehler im Text heißt neuer Entwurf mit nur dieser Änderung.

## Kennzeichnung

`nachbau fertig` setzt den KI-Hinweis, wenn der Nutzer ihn in Schritt 6 bestätigt („Dieses Video ist KI-generiert“, mit Menschen im Bild „Dieses Video zeigt KI-generierte Darsteller“). Sag dem Nutzer zum Schluss: „Kennzeichne die Ad beim Hochladen zusätzlich als KI-generiert.“ Bei Bild-Ads gilt der Satz genauso.

## Am Ende

Drei bis fünf Zeilen in `LOG.md` im Projektordner: Ad-Typ, Weg, Stimme, was geklappt hat und was nicht, Credits gesamt. Und den Stand mit `nachbau hf stand --projekt ad-nachbau/<name>`.
