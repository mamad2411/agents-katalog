---
name: reflexion
description: Nachbesprechung nach einer Aufgabe oder Sitzung mit den vier Fragen des After Action Review (Was war geplant? Was ist passiert? Warum die Abweichung? Was behalten wir bei, was ändern wir?). Zieht daraus prüfbare Lektionen, schlägt Änderungen an den Dateien vor, die der Agent beim nächsten Mal lädt (CLAUDE.md, AGENTS.md, Cursor-Regeln, SKILL.md), setzt sie nach Freigabe um und schreibt jede Lektion mit Dublettenprüfung in LESSONS.md. Nutze den Skill bei „/reflexion“, „Reflexion“, „Nachbesprechung“, „Manöverkritik“, „AAR“, „After Action Review“, „was haben wir gelernt“, „Lessons learned“, „wende den Fix an“, „fix it“, oder direkt nach einer Aufgabe mit Reibung, Überraschung oder Fehler.
---

# reflexion

Du hältst eine Nachbesprechung über die Aufgabe oder Sitzung, die gerade zu Ende ging. Ziel ist nicht ein Rückblick, sondern eine Änderung: eine Lektion, die so konkret ist, dass die nächste Sitzung sie befolgen kann, und wo nötig eine geänderte Datei, die diese Sitzung beim Start lädt.

## Woher die Methode kommt

Das After Action Review entstand in der US Army in den 1970er-Jahren als Nachbesprechung von Übungen und wurde 1993 als Vorschrift festgeschrieben. Der Kern ist einfach: Man vergleicht Plan und Ergebnis, sucht den Grund für die Lücke, und niemand wird beschuldigt. So fällt derselbe Fehler auf, bevor er sich wiederholt.

Die Forschung zu Sprachmodellen kennt dasselbe Muster unter dem Namen Reflexion (Shinn et al., 2023, [arXiv:2303.11366](https://arxiv.org/abs/2303.11366)): Ein Agent, der nach einem Fehlversuch in eigenen Worten festhält, was schiefging, und diese Notiz beim nächsten Versuch mitnimmt, schneidet besser ab als einer, der jedes Mal von vorn beginnt. Dieser Skill ist die Handarbeit dazu: Du schreibst die Reflexion, und `LESSONS.md` ist das Gedächtnis.

## Die vier Fragen

Beantworte alle vier, der Reihe nach, kurz und in eigenen Worten. Es geht um das, was du als Agent getan hast, nicht um Vermutungen über den Nutzer.

1. **Was war geplant?** Auftrag, Plan und erwartetes Ergebnis, schlicht benannt.
2. **Was ist tatsächlich passiert?** Das echte Ergebnis, mit halben Lösungen, Fehlern, stillen Fehlschlägen, Umwegen und Korrekturen durch den Nutzer.
3. **Warum weicht das eine vom anderen ab?** Der Mechanismus, kein Gefühl. „Der Test lief mit `unittest tests/test_repo.py` statt mit `discover -s tests`, dadurch fehlte der Importpfad“ ist eine Ursache. „Ich war nicht gründlich genug“ ist keine. Kennst du die Ursache nicht, schreib „unbekannt“ und mach aus Frage 4, wie man sie herausfindet.
4. **Was behalten wir bei, und was machen wir anders?** Die Regel, die die Lücke verhindert hätte, oder das Vorgehen, das funktioniert hat und wiederholt werden soll.

Lief alles nach Plan, ist das eine gültige Antwort auf Frage 3. Dann hält Frage 4 fest, warum es geklappt hat. An schlechten Tagen fängt die Nachbesprechung Fehler, an guten sichert sie ein Vorgehen, das noch nicht selbstverständlich ist.

## Eine Lektion, die man prüfen kann

Prüfe jede Lektion mit dieser Frage: Weiß ein anderer Agent in einem halben Jahr nach dem Lesen dieser einen Zeile, was er tun oder lassen soll, ohne selbst abzuwägen?

So nicht:

- „Sorgfältiger arbeiten.“
- „Tests besser im Blick behalten.“
- „Klarer mit dem Nutzer kommunizieren.“

So schon:

- „Supabase-Migrationen mit dem Zeitstempel aus `date +%Y%m%d%H%M%S` benennen, nie mit einem ausgedachten Datum, und bestehende Migrationen nie ändern.“
- „Tests in diesem Repo immer mit `python3 -m unittest discover -s tests` starten. Der direkte Aufruf einer Testdatei scheitert am Importpfad und sieht aus wie ein echter Fehler.“
- „Beispielzahlen für die README erst nach dem Runden auf vier Nachkommastellen übernehmen, sonst weicht die Doku in der letzten Stelle vom Skript ab.“

Eine Lektion ohne Datei, Befehl, Zahl, Werkzeug oder Bedingung ist noch keine. Schärfe sie nach oder lass sie weg. Null Lektionen sind erlaubt, wenn nichts Prüfbares herauskommt. Mehr als drei sind fast immer zu viel.

## Vom Merksatz zum Fix

Nicht jede Lektion braucht eine Dateiänderung. Manches ist nur Wissen: „Die Staging-Datenbank ist montags langsam, das ist normal.“ Das gehört nur ins Logbuch. Stell dir pro Lektion eine Frage: **Macht die nächste Sitzung denselben Fehler, wenn sich an dem, was sie lädt, nichts ändert?** Wenn ja, braucht die Lektion einen Fix-Plan.

Ein Fix-Plan nennt zwei Dinge:

- **Ziel:** die Datei, die beim nächsten Mal wirklich geladen wird. Das ist meist `CLAUDE.md` oder `AGENTS.md` im Projekt, eine Regel unter `.cursor/rules/`, ein Schritt in einer bestimmten `SKILL.md`, eine Checkliste oder eine Konfigurationsdatei.
- **Änderung:** der wörtliche Text, der dazukommt oder ersetzt wird, mit Stelle. „Den Deploy verbessern“ ist keine Änderung. „In `skills/release/SKILL.md` nach Schritt 4 einfügen: Vor dem Tag `git status` prüfen, bei ungesicherten Änderungen abbrechen“ ist eine.

Zeig den Plan als nummerierte Liste, bevor du etwas anfasst:

```
FIX-PLAN
1. Ziel: CLAUDE.md, Abschnitt „Tests“
   Neue Zeile: „Tests immer mit python3 -m unittest discover -s tests starten,
   nie eine Testdatei direkt.“
2. Ziel: .cursor/rules/migrationen.mdc
   Neue Regel: „Migrationsdateien mit date +%Y%m%d%H%M%S benennen. Bestehende
   Migrationen nie ändern, stattdessen eine neue anlegen.“

Freigeben? Antworte mit „ja“ oder nenne die Nummern.
```

**Freigabe:**

- Ohne ausdrückliches Ja änderst du nichts. Schweigen oder ein Themenwechsel heißt „noch nicht“.
- Steht schon im Aufruf „anwenden“, „wende den Fix an“, „fix it“ oder „/reflexion anwenden“, setzt du den Plan direkt um und berichtest danach.
- Gibt der Nutzer nur einzelne Nummern frei, setzt du nur diese um.
- Nach jeder Änderung liest du die Datei noch einmal und bestätigst, dass der Text an der richtigen Stelle steht.

Erzwinge keinen Fix für jede Lektion. Wer jede Erkenntnis in eine Regeldatei schreibt, begräbt die wichtigen Regeln unter den unwichtigen.

## Das Logbuch

Jede Lektion kommt in `LESSONS.md`, ob mit Fix oder ohne. Das Werkzeug `lessons.py` liegt im selben Ordner wie diese Datei. Es braucht Python 3.8 oder neuer und keine Pakete.

**Erst prüfen, dann schreiben.** Bevor du eine Lektion einträgst, suchst du nach ähnlichen:

```bash
python3 <skill-ordner>/lessons.py aehnlich "Text der neuen Lektion"
```

Das Skript vergleicht die Kernwörter mit allen vorhandenen Lektionen. Ab 40 Prozent zeigt es Treffer, ab 70 Prozent gilt die Lektion als Dublette. Dann schreibst du keine neue, sondern ergänzt die vorhandene: Datum lassen, Felder schärfen, Status anpassen. Steckt in der neuen Lektion wirklich etwas anderes, schreib sie mit `--trotzdem` und mach den Unterschied im Text sichtbar.

**Schreiben:**

```bash
python3 <skill-ordner>/lessons.py hinzufuegen \
  --lektion "Tests immer mit python3 -m unittest discover -s tests starten, nie eine Testdatei direkt." \
  --geplant "Repo-Tests laufen grün durch." \
  --passiert "test_repo meldete FAILED, obwohl der Code stimmte." \
  --ursache "Beim direkten Aufruf fehlt tests/ im Importpfad, _load.py wird nicht gefunden." \
  --fix "CLAUDE.md, Abschnitt Tests: neue Zeile" \
  --status angewendet \
  --tags "tests,python"
```

`--status` ist `notiert` (nur Logbuch), `vorgeschlagen` (Fix-Plan steht, noch nicht freigegeben) oder `angewendet`. So sieht man später, ob die Ursache behoben ist oder nur aufgeschrieben. Wird ein vorgeschlagener Fix später freigegeben, änderst du in `LESSONS.md` den Status der Lektion auf `angewendet`.

**Lesen:**

```bash
python3 <skill-ordner>/lessons.py liste
python3 <skill-ordner>/lessons.py liste --tag tests
python3 <skill-ordner>/lessons.py liste --status offen
```

`--status offen` zeigt alle Fixes, die vorgeschlagen, aber nie umgesetzt wurden.

Standard ist `./LESSONS.md` im aktuellen Projekt. Lektionen, die überall gelten, schreibst du mit `--global` nach `~/.claude/LESSONS.md`. Die Lektion selbst steht in der Sprache der Sitzung. Mit `--sprache en` bekommen auch die Feldnamen englische Bezeichnungen.

## Damit die nächste Sitzung es liest

Ein Logbuch, das niemand öffnet, ist ein Tagebuch. Die Schleife schließt sich erst, wenn die nächste Sitzung es vor der Arbeit liest:

- Steht in der `CLAUDE.md` oder `AGENTS.md` des Projekts noch kein Hinweis, schlägst du diese Zeile als Teil des Fix-Plans vor: „Lies LESSONS.md, bevor du mit einer Aufgabe beginnst.“ In Cursor-Projekten geht das auch als Regel mit `alwaysApply: true` unter `.cursor/rules/`.
- Vor einer Aufgabe, die einer früheren ähnelt, lohnt `lessons.py liste --tag <thema>`. Das kostet Sekunden und fängt den Fehler, bevor er passiert.

## Ablauf

1. Die Aufgabe oder Sitzung ist beendet. Wird `/reflexion` mitten in einer Aufgabe aufgerufen, besprichst du den Teil bis jetzt.
2. Beantworte die vier Fragen im Chat.
3. Zieh null bis drei prüfbare Lektionen heraus.
4. Entscheide pro Lektion, ob sie einen Fix braucht. Wenn ja, zeig den Fix-Plan und setz ihn nach Freigabe um, oder sofort, wenn der Aufruf das schon sagt.
5. Prüfe jede Lektion mit `lessons.py aehnlich` und schreib sie mit `lessons.py hinzufuegen`, mit passendem Status.
6. Fehlt der Lese-Hinweis in `CLAUDE.md` oder `AGENTS.md`, nimm ihn in den Fix-Plan auf.
7. Berichte im Chat in dieser Form:

```
REFLEXION · <Aufgabe in wenigen Wörtern>

1. Was war geplant?
2. Was ist tatsächlich passiert?
3. Warum weicht das eine vom anderen ab?
4. Was behalten wir bei, und was machen wir anders?

LEKTIONEN
- <Lektion> (Status)

FIX-PLAN
1. Ziel: ... / Änderung: ... (vorgeschlagen oder angewendet)

Logbuch: <Pfad zu LESSONS.md>
```

## Regeln

- Ehrlich bleiben, auch bei Erfolg. Eine Nachbesprechung, die immer „lief gut“ sagt, taugt nichts. Such die echte Reibung, auch wenn die Aufgabe am Ende gelang.
- Keine Schuld verteilen, auch nicht an den Nutzer. Eine unklare Anweisung ist eine Ursache, aus der sich eine Regel machen lässt („Bei mehrdeutigem Ordnernamen nachfragen, bevor Dateien angelegt werden“).
- Keine erfundenen Ursachen. Was du nicht weißt, heißt „unbekannt“.
- Jede Lektion nennt eine Datei, einen Befehl, eine Zahl, ein Werkzeug oder eine Bedingung.
- Jeder Fix-Plan nennt eine Zieldatei und den wörtlichen Text der Änderung.
- Nichts ändern ohne Freigabe, außer der Aufruf sagt schon „anwenden“ oder „fix it“.
- Vor jedem Eintrag auf Dubletten prüfen.

## Was dieser Skill nicht kann

Er trainiert kein Modell und ändert keine Gewichte. Er schreibt Text in Dateien, die ein Agent liest. Ein Fix wirkt erst, wenn er umgesetzt ist und die nächste Sitzung die Datei lädt, also ab dem nächsten Mal, nicht mitten in der laufenden Aufgabe. Fehlt eines davon (prüfbare Lektion, genauer Fix, geladene Datei), entsteht nur der Anschein eines lernenden Systems.
