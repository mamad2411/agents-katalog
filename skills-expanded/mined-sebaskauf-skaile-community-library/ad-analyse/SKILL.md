---
name: ad-analyse
description: Holt Ads der Competitor aus der Werbebibliothek von Meta und zerlegt jede einzelne. Je Ad das komplette gesprochene Skript, ein Bild aus jeder Szene mit Beschreibung, seit wann sie läuft, wie viele Varianten es gibt und eine Einschätzung, wie gut sie läuft. Nimmt Links aus der Werbebibliothek, Bibliotheks-IDs, ganze Competitor (Name oder Link auf ihre Ads), Tabellen mit Links oder eine Videodatei.
when_to_use: Wenn jemand eine Ad oder mehrere Ads aus der Werbebibliothek (facebook.com/ads/library) auswerten will, Winning Ads seiner Competitor analysieren will, oder sagt "analysiere diese Ad", "zieh dir das Skript dieser Ad", "schau dir die Ads von <Firma> an", "/ad-analyse". Auch, wenn der Prompt "Dein Ad-Plan" oder die Skills Ad-Nachbau und Ad-Schnitt eine Ad aus der Werbebibliothek brauchen.
argument-hint: "[Links aus der Werbebibliothek, Firmenname oder Datei]"
---

# Ad-Analyse

Du holst Ads aus der öffentlichen Werbebibliothek von Meta und zerlegst jede einzelne: Skript, Bild je Szene, Laufzeit, Varianten, was an ihr auffällt. Den Vergleich über alle Ads und den Ad-Plan machst du nur, wenn der Nutzer das ausdrücklich will. Das ist die Aufgabe des Prompts "Dein Ad-Plan".

Sprich Deutsch, per du, kurz. Keine Gedankenstriche, echte Umlaute.

## Werkzeug

Alles läuft über ein Skript. Starte es im Ordner des Nutzers (dort entsteht der Ordner `ad-analyse/`):

```
uv run --script "${CLAUDE_SKILL_DIR}/scripts/ad_analyse.py" <Eingaben>
```

- Findet die Sitzung `uv` nicht, nimm den vollen Pfad: Mac `~/.local/bin/uv`, Windows `$env:LOCALAPPDATA\Microsoft\WinGet\Links\uv.exe` oder `$env:USERPROFILE\.local\bin\uv.exe`.
- Bricht das Skript ab, weil etwas fehlt (Pakete, Browser, Sprachmodell), arbeite `${CLAUDE_SKILL_DIR}/SETUP.md` ab und starte dann neu.
- Ein Lauf mit mehreren Ads dauert pro Ad ein bis drei Minuten (Abschrift auf dem Prozessor). Bei mehr als drei Ads starte ihn im Hintergrund und warte auf sein Ende.

Eingaben, beliebig gemischt in einem Aufruf:
- Link einer Ad (`https://www.facebook.com/ads/library/?id=<Bibliotheks-ID>`, auch die lange Form aus der Adresszeile) oder die nackte Bibliotheks-ID
- Link auf die Ads einer Firma (Adresse mit `view_all_page_id=`) oder `--firma "Name"`: Das Skript zeigt ihre aktiven Ads, sortiert nach Impressionen, und nimmt die stärksten (Standard 2, `--je-firma N`). Mit `--nur-liste` zeigt es nur die Liste.
- eine Datei mit Links, zum Beispiel die Tabelle mit den Gewinner-Ads aus dem Video "Gewinner-Ads finden"
- eine Videodatei vom Rechner mit `--name "Firma"`, dazu, wenn bekannt, `--start JJJJ-MM-TT`, `--varianten N` und `--link`

## So gehst du vor

1. **Eingaben sammeln.** Nimm, was der Nutzer gibt. Liegt im Ordner eine `angebot.md`, lies sie mit, frag das Angebot aber nie selbst ab.
2. **Firmen.** Gibt der Nutzer Competitor statt einzelner Ads, starte zuerst mit `--nur-liste`, zeig ihm die Liste kurz und sag, welche zwei du nehmen würdest und warum (lange Laufzeit, viele Varianten, weit oben nach Impressionen). Will er andere, nimm die Bibliotheks-IDs, die er nennt. Meldet das Skript "FIRMA NICHT EINDEUTIG", zeig die Treffer und frag, welche gemeint ist.
3. **Holen und zerlegen.** Ein Aufruf mit allen Ads. Das Skript holt sie nacheinander, mit Pause dazwischen, und schreibt je Ad einen Ordner `ad-analyse/NN-<firma>-<id>/`. Fertige Ads holt es kein zweites Mal (mit `--neu` doch).
4. **Je Ad ansehen.** Für jeden Ordner, dessen `analyse.md` noch die Zeile `<!-- AD-ANALYSE OFFEN` trägt:
   - Sieh dir `szenen/kontaktbogen.jpg` (bei langen Ads `kontaktbogen-1.jpg`, `-2.jpg`, …) an und bei Bedarf einzelne Szenenbilder.
   - **Skript gegen die Untertitel im Bild:** Sieh dir `szenen/untertitel*.jpg` an (Streifen aus dem unteren Bilddrittel, alle halbe Sekunde, mit Zeit). Vergleich Wort für Wort mit `skript.txt`, besonders die Prüfstellen in `analyse.md`. Steht im Bild ein anderes Wort, ein Name anders geschrieben oder eine Zahl, die in der Abschrift fehlt, berichtige `skript.txt` und trag jede Änderung in `analyse.md` ein (vorher → jetzt). `skript.json` bleibt die rohe Abschrift mit Zeiten. Titel und Einblendungen sind keine Untertitel: Sie fassen oft nur zusammen. Widersprechen sich Untertitel und ein anderes Bildelement (zum Beispiel ein Etikett), ändere nichts und schreib den Widerspruch dazu. Sitzen die Untertitel woanders, erzeug neue Streifen mit `--untertitel <Ad-Ordner> --band mitte` (oder `oben`, oder `60-85` in Prozent der Bildhöhe). Hat die Ad keine Untertitel, schreib das so hin.
   - Füll `analyse.md` ganz aus: je Szene, was zu sehen ist und welcher Text im Bild steht, dann Hook (die ersten drei Sekunden), Angle, Machart (mit KI erstellt oder selbst gefilmt, und woran du das erkennst), Aufforderung am Ende, warum die Ad vermutlich funktioniert, was der Nutzer für seine eigene Ad mitnimmt (mit `angebot.md`, wenn sie da ist). Übernimm Muster, nicht Texte.
   - Lösch zum Schluss die erste Zeile `<!-- AD-ANALYSE OFFEN …` und setz in `ad.json` unter `skript` den Wert `gegen_untertitel_geprueft` auf `true`, wenn du abgeglichen hast.
5. **Übersicht.** Starte `--uebersicht`. Das schreibt `ad-analyse/uebersicht.md` neu (Tabelle über alle Ads). Den Abschnitt "Muster der Winning Ads" darin füllst du nur, wenn der Nutzer den Vergleich will.
6. **Melden.** Je Ad eine Zeile: Firma, läuft seit (Datum und Tage), Varianten, Einschätzung, ein Satz, was an der Ad auffällt. Dazu jede Ad, die nicht geladen wurde, mit dem Grund aus der Ausgabe.

## Was die Zahlen bedeuten

- **Läuft seit:** "Seit dem … ausgeliefert" aus der Werbebibliothek. Laufzeit in Tagen bis heute.
- **Varianten**, bis zu drei Zahlen: Metas eigene Zahl ("N Werbeanzeigen verwenden diese Anzeigengestaltung und diesen Text"), wie viele aktive Ads der Firma dasselbe Video nutzen und wie viele dieselbe Überschrift tragen. Dazu die Zahl aller aktiven Ads der Firma und der Platz dieser Ad nach Impressionen. Fehlt eine Zahl, steht "nicht ablesbar". Erfinde keine.
- **Einschätzung** aus Laufzeit und Varianten: unter zwei Wochen Test, ab vier Wochen interessant, ab drei Monaten wahrscheinlich ein Gewinner. Reichweite zeigt die Werbebibliothek bei diesen Ads nicht, das Skript liest sie nicht.

## Wenn Meta nicht mitspielt

Das Skript lädt die Werbebibliothek mit einem normalen Browser ohne Fenster, so wie jeder Besucher sie sieht. Es meldet sich nirgends an und umgeht nichts. Meldet es eine Anmeldeseite, ein Captcha oder dass die Seite keine Ad-Daten zeigt, versuch es höchstens einmal nach ein paar Minuten noch einmal. Dann biete dem Nutzer den Weg von Hand an:
"Öffne die Ad in der Werbebibliothek in deinem Browser, lade das Video herunter oder nimm es mit dem Bildschirm auf und leg die Datei in diesen Ordner. Sag mir dazu, seit wann sie läuft (Seit dem … ausgeliefert) und wie viele Werbeanzeigen diese Gestaltung verwenden."
Dann: `--name "Firma" --start JJJJ-MM-TT --varianten N --link <Link>` mit der Datei. Eine Ad, die Meta nicht mehr zeigt ("NO_AD_FOUND" oder "zeigt keine Ad"), ist abgeschaltet: Sag das und mach mit den anderen weiter.

## Für andere Skills

Ad-Nachbau und Ad-Schnitt rufen dasselbe Skript auf, wenn sie eine Ad aus der Werbebibliothek brauchen, und lesen dann den Ad-Ordner: `video.mp4`, `skript.txt`, `skript.json` (Sätze und Wörter mit Zeiten), `ad.json` (alle Daten, Szenen mit Zeiten und Bildern), `szenen/`, `analyse.md`. Die Videos fremder Ads bleiben auf dem Rechner und werden nirgends hochgeladen.
