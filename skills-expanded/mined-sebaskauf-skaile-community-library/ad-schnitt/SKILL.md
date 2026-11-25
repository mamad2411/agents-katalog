---
name: ad-schnitt
description: Schneidet selbst gefilmte Ads. Aus einer Aufnahme mit mehreren Hooks, Hauptteil und Call to Action baut Claude je Hook eine fertige Ad im Hochformat, schneidet Versprecher und doppelte Anläufe heraus, schreibt Titel und Wort-Captions passend zum Angebot, setzt animierte Grafiken (Motion Graphics) genau auf das gesprochene Wort, baut eigenes Material ein und übernimmt den Stil einer Referenz-Ad. Läuft auf dem eigenen Rechner, ohne Konto.
when_to_use: Wenn jemand sagt "Stelle diese Ads fertig", "Ich möchte auch von den Motion Graphics her alles so haben, wie du es in meiner Referenz siehst", "Pass diesen Stil auf mein eigenes Angebot an", "schneide meine Ad", "mach aus meiner Aufnahme Ads", "je Hook eine Ad", "/ad-schnitt", oder eine selbst gefilmte Aufnahme mit mehreren Hooks schickt und fertige Ads will.
argument-hint: "[Videodatei der Aufnahme] [Referenz-Ad, optional]"
---

# Ad-Schnitt

Du machst aus einer selbst gefilmten Aufnahme fertige Ads. In der Aufnahme stehen mehrere Hooks, ein Hauptteil und ein Call to Action, dazwischen Versprecher und neue Anläufe. Du erkennst die Teile, nimmst je Satz den letzten sauberen Anlauf und baust je Hook eine eigene Ad: Hook, Hauptteil, Aufruf, mit Titel, Wort-Captions, Schlusskästen und, wo es passt, Grafik-Karten. Der Nutzer muss dafür nur „stelle diese Ads fertig“ sagen.

Sprich mit dem Nutzer Deutsch, per du, kurz. Frag nur, wenn du es wirklich nicht selbst klären kannst, und dann eine Frage auf einmal. Bei Wartezeiten sag kurz, was läuft und wie lange es ungefähr dauert. Alles läuft auf dem eigenen Rechner und kostet nichts: kein Konto, keine Credits.

## Werkzeuge

Alle Schritte laufen über einen Einstieg, auf Windows und Mac gleich:

```
uv run --script "${CLAUDE_SKILL_DIR}/scripts/ad.py" <schritt> [argumente]
```

Unten steht dafür kurz `ad <schritt>`. Findet die Sitzung `uv` nicht: Mac `~/.local/bin/uv`, Windows `%USERPROFILE%\.local\bin\uv.exe` oder `%LOCALAPPDATA%\Microsoft\WinGet\Links\uv.exe`. Unter Windows jeden Befehl einzeln, kein `&&`, Pfade in Anführungszeichen.

| Schritt | Wofür |
|---|---|
| `einrichten --pruefen` | Ist alles da? Ändert nichts. Fehlt etwas: `${CLAUDE_SKILL_DIR}/SETUP.md` abarbeiten |
| `abschreiben <video> --ordner <arbeitsordner> --begriffe "..."` | Ton ziehen, Stück für Stück wortgenau abschreiben, jeder Anlauf eine eigene Zeile |
| `referenz <video oder ordner> --ordner <arbeitsordner>` | Referenz-Ad zum Ansehen aufbereiten: Bogen, Einzelbilder, Skript |
| `bauen --ordner <arbeitsordner> --nur-pruefen` | Schnittplan auflösen und Kanten zeigen, nichts rendern |
| `bauen --ordner <arbeitsordner> --ausgabe <ordner>` | alle Varianten rendern, je Variante ein Kontaktbogen |
| `pruefen --ordner <arbeitsordner>` | jede Naht nachhören, Wortlaut gegenprüfen, Bericht schreiben |

Du kannst Videos nicht ansehen, nur Bilder. Jeden Kontaktbogen liest du wirklich an, bevor du etwas über eine Ad sagst. Videos zeigst du dem Nutzer, indem du sie öffnest (Mac `open "<datei>"`, Windows `start "" "<datei>"`).

## Feste Regeln

1. **Die Stimme wird nie bearbeitet.** Kein Entrauschen, kein EQ, keine Kompression, kein Musikbett. Die Werkzeuge schneiden nur und stellen in einem einzigen Faktor linear lauter. Du fügst nichts davon hinzu.
2. **Je Satz der letzte vollständige Anlauf.** Sagt der Nutzer einen Satz mehrmals, nimmst du den letzten, der ohne Versprecher bis zum Ende durchläuft. Bricht der letzte ab oder fehlt ihm ein Stück, nimmst du den letzten vollständigen, auch wenn er früher in der Aufnahme liegt. Bricht ein Anlauf mitten im Satz ab und setzt neu an, beginnt dein Teil beim neuen Ansatz.
3. **Wortgenau.** Der Text jedes Teils im Schnittplan steht genau so im Transkript. Du formulierst nichts um. Untertitel berichtigst du nur bei Schreibweisen (Eigennamen, Zahlen) über `begriffe` oder `caption`.
4. **Reihenfolge wie geplant.** Die Sätze stehen in der Reihenfolge des Skripts aus `ad-plan.md`, ohne Skript in der Reihenfolge der Aufnahme. Spricht der Nutzer einen Satz später noch einmal neu ein (oft nach dem Aufruf), ersetzt die neue Fassung die alte an ihrer Stelle. Sonst stellst du nichts um.
5. **Jede Ad endet mit Hook, Hauptteil und Aufruf.** Ohne Aufruf keine fertige Ad.
6. **Dateiname mit Hook.** Jede Ad heißt so, dass man den Hook erkennt (das macht `stichwort`).
7. **Erst prüfen, dann melden.** Keine Ad gilt als fertig, bevor `ad pruefen` gelaufen ist und du ihren Kontaktbogen gesehen hast. Jede Prüfung läuft einmal. Nach einer Änderung baust und prüfst du nur die geänderte Variante, keine zweite Runde ohne Änderung.
8. **Nichts erfinden.** Titel, Schlusskästen und Karten sagen nur, was der Nutzer in der Aufnahme sagt oder was in `angebot.md` steht. Keine erfundenen Zahlen, Preise, Termine oder Kundennamen.

## Ablauf

### 1. Vorbereiten
- `ad einrichten --pruefen`. Endet es nicht mit „ALLES STEHT“, arbeite `${CLAUDE_SKILL_DIR}/SETUP.md` ab und prüf noch einmal.
- Lies, was im Ordner des Nutzers liegt: `angebot.md` (aus „Dein Ad-Plan“) für Angebot, Zielgruppe, Termine und Schreibweisen, `ad-plan.md` für die geplanten Hooks und Skripte. Beides nutzt du, wenn es da ist. Fehlt es, arbeitest du nur mit der Aufnahme.
- `ad-plan.md` ist frei in Markdown geschrieben, lies es tolerant: Unter „Meine Ads“ steht je Ad ein Abschnitt „Ad 1: …“ mit Zeilen wie Produktion (selbst gefilmt oder mit KI erstellt), Hook 1 bis Hook 3, Skript, Aufruf, dazu unter „Winning Ads“ und „Muster“ die Vorbilder. Passt die Aufnahme zu einer selbst gefilmten Ad aus dem Plan, ordnest du Hooks und Sätze danach zu und nimmst ihren Titel als Grundlage für den Kurznamen.
- Arbeitsordner je Aufnahme: `ad-schnitt/<kurzname>` im Ordner des Nutzers. Fertige Ads: `fertige-ads/<kurzname>`. Der Kurzname kommt aus dem Angebot oder der Datei (zwei bis drei Wörter, klein, mit Bindestrich).

### 2. Abschreiben
`ad abschreiben "<video>" --ordner "ad-schnitt/<kurzname>" --begriffe "<Eigennamen aus angebot.md, mit Komma>"`
Das dauert etwa das Zwei- bis Fünffache der Aufnahmelänge. Starte es im Hintergrund, wenn die Aufnahme länger als zwei Minuten ist, und warte auf das Ende. Liegt die Abschrift derselben Aufnahme schon im Arbeitsordner, rechnet der Schritt nichts neu (mit `--neu` doch). Meldet er „ACHTUNG … digital still“, ist dort der Ton ausgefallen: Sag es dem Nutzer sofort, das lässt sich nicht retten.
Danach liest du `transkript.txt` ganz: eine Zeile je Sprech-Stück mit Zeit. Steht ein Satz mehrmals untereinander, sind das Anläufe.

### 3. Teile erkennen und den Schnittplan schreiben
Lies dafür `${CLAUDE_SKILL_DIR}/PLAN-FORMAT.md` und schreib `schnittplan.json` in den Arbeitsordner.

Was rausfliegt und was bleibt:
- **Raus:** frühere und abgebrochene Anläufe, neu angesetzte Satzanfänge, Wiederholungen mit Absetzen, alles, was nicht an den Zuschauer geht („warte“, „nochmal“, „Moment“, Fluchen, Lachen, Selbstgespräche, Sätze an jemanden hinter der Kamera).
- **Bleibt:** kleine Doppler ohne Pause („das das“, ein Schnitt würde das Wort zerhacken), Füllwörter in einem sonst guten Satz, bewusste Wiederholungen zur Betonung.
- Fehlt ein Satz in jedem Anlauf oder bricht jeder Anlauf ab, lässt du ihn weg und sagst es in der Übergabe. Setz keinen Satz aus Stücken zusammen, die der Nutzer so nie gesagt hat.
- Eine Zeile mit `[ACHTUNG …]` hat oft einen verschluckten Anlauf in sich, `[undeutlich: …]` ein unsicheres Wort. Nimm dort lieber einen anderen Anlauf, wenn es einen sauberen gibt.

Die Bausteine im Plan:
- **Hooks:** die Einstiege am Anfang, bevor der Hauptteil beginnt. Jeder Hook ein eigener Baustein mit `art: hook` und einem `stichwort` aus zwei bis vier Wörtern. Sind die Hooks in `ad-plan.md` geplant, ordnest du sie danach zu.
- **Hauptteil:** ein Baustein `art: hauptteil`, Satz für Satz je ein Teil mit `ab` (Beginn des gewählten Anlaufs) und dem Text. Gibt es mehrere Fassungen des Hauptteils, je Fassung ein eigener Baustein und eine Liste `varianten`.
- **Aufruf:** ein Baustein `art: aufruf`, genauso.
- **Titel:** zwei Zeilen, je höchstens 34 Zeichen, sie stehen während des Hooks. Erste Zeile der Nutzen, zweite das Angebot. Der Titel wiederholt den Hook nicht wörtlich, er verdichtet sein Versprechen: die starken Wörter des Nutzers, Zahlen als Ziffern, nur was die Ad einlöst. Kurze Zeilen werden groß und gut lesbar. Passt zum Hook, also bei Bedarf je Variante eigene Titel.
- **Schlusskästen:** zwei Zeilen ab dem Aufruf, mit dem, was der Aufruf sagt (Termin, wo der Link ist, kostenlos), so wie er es sagt.
- **begriffe:** Schreibweisen für die Untertitel, zum Beispiel Zahlwörter als Ziffern, Produktnamen, „Claude“ statt verhörter Formen.
Dann `ad bauen --ordner ... --nur-pruefen`. Lies die Hinweise: Ein Teil, der nur zu weniger als 100 % gefunden wurde, und jede Naht „mitten im Redefluss“ prüfst du im Transkript nach.

### 4. Karten (Motion Graphics auf dem Wort)
Karten machen aus der Ad mehr als einen Schnitt. Sie sind animiert: Ein Chromium ohne Fenster nimmt sie Bild für Bild auf. Wörter bauen sich auf, Punkte gleiten auf ihrem Wort herein und bekommen einen gezeichneten Haken, Figuren färben sich, ein Ablauf hakt seine Stationen ab und endet mit einem Klick. Startet der Browser auf einem Rechner nicht, baut `ad bauen` dieselben Karten als ruhige Tafeln und sagt es in der Ausgabe („Animationen: aus“). Dann sagst du es dem Nutzer.
Setz die Karten, wenn der Nutzer nichts anderes sagt, nach diesen Regeln (Format in `PLAN-FORMAT.md`):
- In den ersten Sekunden nur der Sprecher: keine Karte im Hook.
- Eine Karte zeigt wörtlich, was gerade gesagt wird, und erscheint genau auf dem Wort. Nennt er eine Zahl: `zahl`. Zählt er auf: `liste`, jeder Punkt auf seinem Wort. Beschreibt er einen Ablauf, der etwas erledigt (von … bis …, und am Ende gibst du frei): `ablauf`, jede Station auf ihrem Wort, der Knopf auf dem Wort, mit dem er abschließt. Eine Kernaussage oder Frage: `text`.
- `oben`, wenn er weiterredet und man ihn sehen soll. `voll` für Aufzählungen und Abläufe. Persönliche Sätze und der Beginn des Aufrufs gehören ihm allein.
- Kurz: Punkte höchstens sechs Wörter, Aussagen höchstens zwölf. Höchstens eine Karte je Aussage, bei 30 bis 60 Sekunden vier bis sechs Karten.
- Gibt der Nutzer eigenes Material (Bildschirmaufnahme, Screenshot, Produktfoto), setzt du es als Karte `video` oder `bild` an die Stelle, an der er davon spricht.

### 5. Referenz-Ad (wenn der Nutzer eine mitgibt)
- Datei oder Ordner: `ad referenz "<datei oder ordner>" --ordner "ad-schnitt/<kurzname>"`.
- Link aus der Werbebibliothek: Liegt der Skill Ad-Analyse daneben (`${CLAUDE_SKILL_DIR}/../ad-analyse/SKILL.md`), hol die Ad im Ordner des Nutzers damit: `uv run --script "${CLAUDE_SKILL_DIR}/../ad-analyse/scripts/ad_analyse.py" "<link>"`. Das legt `ad-analyse/NN-<firma>-<id>/` an (Video, Skript mit Zeiten, Szenen). Diesen Ordner gibst du an `ad referenz`. Fehlt Ad-Analyse, bitte den Nutzer um die Videodatei.
- Link von Instagram, TikTok oder YouTube: Liegt der Skill Ad-Nachbau daneben (`${CLAUDE_SKILL_DIR}/../ad-nachbau/SKILL.md`), lädt er das Video: `uv run --script "${CLAUDE_SKILL_DIR}/../ad-nachbau/scripts/nachbau.py" vorbild holen "<link>" --projekt "ad-schnitt/<kurzname>/referenz-quelle"`. Das legt dort `vorbild/vorbild.mp4` ab, die Datei gibst du an `ad referenz`. Dafür braucht es keine Anmeldung bei Higgsfield. Sperrt die Plattform den Abruf („LINK GEHT NICHT“) oder fehlt Ad-Nachbau, bitte den Nutzer, das Video zu speichern oder eine Bildschirmaufnahme davon zu machen, und nimm die Datei.
- Sieh dir `bogen.jpg` und Bilder aus `bilder/` an, bei einem Ordner von Ad-Analyse auch dessen `szenen/untertitel*.jpg` (Untertitel-Band alle 0,5 s, dort liest du Titel und Caption-Stil am besten ab), und schreib auf: Wann kommen Titel und wie sehen sie aus, wie sind die Captions (Größe, Lage, Farbe des aktiven Worts, Großbuchstaben), welche Grafiken kommen an welchen Stellen, wie lange ist der Sprecher allein.
- Übertrag das in `stil.json` (Farben, Lagen, Größen), in die Karten und in `schluss_ab` (ab welchem Wort die Schlusskästen stehen): dieselben Stellen im Aufbau, dieselbe Art Grafik, angepasst auf das Angebot des Nutzers. Bewegte Grafiken der Referenz setzt du mit der Karte um, die ihr am nächsten kommt.

### 6. Bauen und prüfen
- `ad bauen --ordner "ad-schnitt/<kurzname>" --ausgabe "fertige-ads/<kurzname>"`, danach `ad pruefen --ordner "ad-schnitt/<kurzname>"`.
- Die Prüfung hört jede Naht, den Anfang und das Ende jeder Ad und die ganze Ad noch einmal nach und misst jeden Clip. Lies `pruefbericht.md`, so behebst du die Befunde:

| Befund | Bedeutung | Im Plan ändern |
|---|---|---|
| „zusätzlich gehört“ oder „doppelt gehört“ (Naht, Anfang, Wortlaut) | Ein Stück eines anderen Anlaufs ist mitgekommen | späteres `ab` oder anderer Anlauf, notfalls `von_genau` |
| „mehr Sprache, als der Text braucht“ | im Clip steckt ein zweiter Anlauf | wie oben |
| „nicht gehört“, „endet mitten im Laut“ | ein Wort oder sein Ausklang ist abgeschnitten | `bis_genau` weg oder später, sonst `"luft": 0.06` |
| „fast stumm“ | die Wortzeit lag daneben | anderer Anlauf, sonst `von_genau`/`bis_genau` aus dem Transkript |
| „Stille mitten im Clip“ | eine lange Pause ist stehen geblieben | den Teil an der Pause in zwei Teile trennen |
| „Untertitel prüfen“ | das zweite Hören hat ein Wort anders verstanden | meist hört das Modell falsch. Sagt die Aufnahme dort wirklich etwas anderes als der Untertitel: `caption` |

  Ein Befund, der nur an einem Eigennamen hängt (Claude, Produkt, Firma), ist fast immer ein Hörfehler des Prüfers: im Transkript nachsehen, nicht ändern. Nach einer Änderung nur diese Variante neu bauen und prüfen (`--nur <nummer>` bei `bauen` und `pruefen`). Was nach einer Korrektur noch auffällt, nennst du in der Übergabe, statt weiter zu würfeln.
- Lies jeden Kontaktbogen in `fertige-ads/<kurzname>/kontakt/` an: Titel lesbar, Captions im Bild, Karten am richtigen Wort, nichts verdeckt das Gesicht im Hook.

### 7. Übergabe
Sag dem Nutzer kurz:
- wo die Ads liegen und wie jede heißt (eine Zeile je Ad: Datei, Hook, Länge),
- was du herausgeschnitten hast (Anzahl der Anläufe und Versprecher),
- was du an Titeln, Captions und Karten gesetzt hast,
- was fehlt oder offen ist: Sätze, die in keinem Anlauf vollständig waren, Stellen, die du bewusst drin gelassen hast, Befunde, die nach der Korrektur geblieben sind.
Frag dann, ob er Änderungen will (anderer Titel, Karte weg, anderer Anlauf). Änderungen sind ein neuer Lauf von Schritt 6 mit geändertem Plan.
