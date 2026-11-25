---
name: steuer-spar-erklaerung
description: Prüft einen konkreten Steuerfall in einer vom lokalen Release unterstützten SteuerSparErklärung unter Windows, gleicht ihn mit Belegen ab, richtet bei Bedarf die lokale Automation über npm ein oder bearbeitet nach Freigabe eine verifizierte Arbeitskopie. Verwenden bei „meine Steuererklärung prüfen“, SteuerSparErklärung/SSE bedienen, Belege abgleichen sowie API- oder MCP-Einrichtung; nicht für allgemeine Steuerfragen ohne lokalen SSE-Fall und niemals für ELSTER-Versand.
---

# SteuerSparErklärung sicher prüfen

Führe technisch unerfahrene Nutzer standardmäßig auf Deutsch. Arbeite
read-only, bis eine konkrete Änderung an einer verifizierten Arbeitskopie
separat freigegeben wurde.

## Nutzerziel zuerst erkennen

Ordne den Auftrag ohne technische Rückfrage einem sicheren Modus zu:

- „prüfen“, „Schnellcheck“ oder „Fehler finden“: ausschließlich read-only;
- „mit Belegen abgleichen“: read-only in Fall und freigegebenen Quellen;
- „korrigieren“ oder „ändern“: zuerst Vorschläge, dann nur eine verifizierte
  Arbeitskopie und jede einzelne Freigabe;
- „UStVA“, „Umsatzsteuer-Voranmeldung“, Monat oder Quartal vorbereiten:
  UStVA-Modus; Zieljahr, gesetzliche Frequenz und vorhandene Übermittlung
  zuerst prüfen, nur bei ausdrücklichem Auftrag in einer Arbeitskopie ändern;
- „einrichten“ oder „Verbindung reparieren“: Einrichtungsmodus, noch keine
  Steuerdaten lesen.

Bestätige den erkannten Modus in einem kurzen deutschen Satz. Erkläre API, MCP,
Hashes oder Dateiformate nur, wenn der Nutzer danach fragt oder eine konkrete
Entscheidung davon abhängt.

## Harte Grenzen

Diese Regeln gelten auch auf ausdrücklichen Wunsch:

- Sende, übermittle, bestätige oder schließe niemals über ELSTER ab. Bereite
  keinen Versandklick und keinen Umgehungsweg vor.
- Lösche oder überschreibe Originalfälle und übermittelte Falldateien nie auf
  Dateiebene, benenne sie nie um. Verschiebe Fälle im normalen Prüf- und
  Bearbeitungsablauf nicht. Die einzige enge Ausnahme ist ein ausdrücklich
  beauftragter Archivlauf für nachweislich nicht übermittelte Fälle über
  `sse_archive_cases`: vollständiges Inventar, Hashbindung und ausschließlich
  ein neues Ziel im konfigurierten Backupbereich sind Pflicht. Lies das
  Inventar mit `sse_list_cases` und `includeBackups: true`. Das Programm legt
  beim Speichern eine eigene `<Fallname>_Backup`-Datei daneben, und der
  Bestandsabgleich zählt sie mit; ein unvollständiger Restbestand wird mit
  `inventory-mismatch` gestoppt, ohne etwas zu verschieben.
  Bei `rolledBack: false`, `retainedTargets` oder `recoveryFiles` stoppe den
  Ablauf und lege dem Menschen genau diese strukturierten Pfade zur Klärung
  vor; starte keine zweite Archivierung und verschiebe Recovery-Dateien nicht
  automatisch.
- Ändere Steuerdaten nur nach Sicherung über `sse_make_working_copy` nach
  `backups:`: standardmäßig in einer bytegleich verifizierten Arbeitskopie, im
  Original nur auf ausdrücklichen Nutzerwunsch (references/first-run.md).
- Arbeite nie mit einem wiederhergestellten Fall weiter. Hat SteuerSparErklärung
  nach einem unsauberen Ende eine Wiederherstellungsdatei geladen, stoppt
  `launch` mit `kind="recovered-state"`. Der geöffnete Inhalt entspricht dann
  nicht mehr der Datei, deren Hash du verifiziert hast, und jeder Report daraus
  wäre fachlich falsch. Schließe den Fall ohne Speichern, lass den Nutzer die
  Wiederherstellung im Programm verwerfen und öffne danach erneut.
- Öffne auch für eine UI-gebundene reine Prüfung niemals den Originalfall.
  SSE markiert schon beim Navigieren die zuletzt besuchte Seite als
  ungespeicherte In-Memory-Änderung. Erzeuge daher vor der ersten UI-Navigation
  mit `sse_make_working_copy` eine hashverifizierte Prüffallkopie und öffne
  nur diese. Für die reine Prüfung wird ein Original nur dateibasiert gelesen.
- Umgehe API-Sperren nie mit Roh-Tastatur, freien Koordinaten oder
  ungebundenen generischen Klicks.
- Installiere nichts still. Ändere weder Autostart noch Agenten-Konfiguration,
  Connector-Zugriff oder Belegablage ohne die jeweils nötige Zustimmung.
- Erfinde keine Releasequelle, Pfade, Befehle, API-Felder, MCP-Konfigurationen
  oder Szenarioschemata. Lies sie aus dem installierten Release.
- Behaupte Erfolg nur nach Readback. Ein Exitcode oder sichtbarer Klick reicht
  nicht als Nachweis.

Unterstütze ausschließlich Windows x64 mit Windows PowerShell 5.1 und ein im
installierten Release als `supported` ausgewiesenes Produktprofil. Derzeit ist
das Profil `2025` mit Engine-Major `31` freigegeben. Automatisiere keine andere
Version ersatzweise. Akzeptiere nur `status=supported` zusammen mit
`operationAccess=full`. Meldet `product_info.buildDrift.drifted=true`, stoppe
vor jeder Mutation, bis der installierte Build gezielt verifiziert wurde; API
und direkter Worker erzwingen diese Mutationssperre zusätzlich.
Bei `health.running=false` und leerem `buildDrift.current` bedeutet
`drifted=true` nur: aktuell ist kein laufender Build messbar. Behaupte daraus
keine installierte Versionsabweichung. Nach einem erlaubten Launch muss
`product_info` den laufenden Build erneut bestimmen; erst dessen nichtleerer
`current`-Wert ist ein echter Gleich-/Driftnachweis.

## Zuerst: ist ein Transport da?

Beginne jeden Auftrag mit genau einem Aufruf von `sse_health`. Sein Ergebnis
entscheidet den weiteren Weg, und zwar ohne Rückfrage:

1. **`ok=true`** — MCP und API laufen. Arbeite normal weiter.
2. **MCP-Tool existiert, meldet aber die API als nicht erreichbar** — die
   API läuft nicht. Starte sie im Ordner in einem eigenen offenen Terminal
   (`node_modules\.bin\steuer-spar-erklaerung-api.cmd --config <absolut>\config.json`)
   und wiederhole `sse_health` höchstens zweimal im Abstand von zwei Sekunden.
3. **Es gibt gar kein `sse_*`-Tool** — der MCP-Server ist beim Client nicht
   angemeldet. Wechsle in den Einrichtungsmodus, arbeite `docs/INSTALLATION.md`
   ab und komm danach hierher zurück. Lies in diesem Zustand keine Steuerdaten.

Nach einer frischen MCP-Anmeldung lädt der laufende Client den Server nicht
nach. Melde dann „Technisches Setup bereit; Client-Verifikation nach Neustart
offen." und verlange genau einen Neustart, statt einen Tool-Erfolg zu behaupten.

## Architektur richtig verwenden

Die lokale HTTP-API auf Loopback ist der universelle Kern. Nur sie kennt
`SSE.exe`, lokale Pfade, Arbeitsbereich, Falldateien und UI Automation.

MCP ist ein dünner Wrapper darüber; sein Prozess kennt nur die API-URL.
Fehlt MCP oder unterstützt der Agent kein MCP, verwende dieselben
Operationen direkt über die API-CLI. Wechsel während einer möglicherweise
begonnenen Schreiboperation nie still den Transport; bei unklarem Zustand stoppen.

Hat der Nutzer ausdrücklich „über npx“, „ohne Installation“ oder „ohne MCP“
verlangt, ist die direkte API-CLI der gewählte Transport. Versuche in diesem
Lauf nicht zuerst MCP und verlange keinen MCP-Neustart; dasselbe gilt nach
`Standard-Einrichtung und Prüflauf ausführen` im selben Auftrag. Wurde dagegen MCP
ausdrücklich gewählt oder bereits für den Auftrag verwendet, ersetze einen
fehlgeschlagenen oder abgebrochenen MCP-Aufruf nicht still durch die API-CLI;
lies zuerst den frischen Zustand und stoppe bei möglicher Mutation.

Die API kennt keine Anmeldung; es gibt kein Token zu lesen oder zu schützen.
Sie weist stattdessen jede Anfrage mit `Origin`, `Sec-Fetch-Site` oder einem
fremden `Host` mit 403 ab, damit keine Webseite im Browser des Nutzers die
Steuersoftware steuern kann. Verwende trotzdem die ausgelieferte CLI statt
eigener HTTP-Befehle: sie kennt Argumentschemata, Grenzen und Ergebnisverträge.

Nennt der MCP-Eintrag einen expliziten `--config`-Pfad, verwende genau diesen
absoluten Pfad unverändert auch für direkte API-CLI-Aufrufe.

Für direkte API-Aufrufe bevorzuge die ausgelieferte
`steuer-spar-erklaerung-call`-CLI. Beginne bei einer bekannten Einzelaktion
mit `describe <operation>` und nur bei einer breiten Planung mit `discovery`; für komplexe
Argumente bevorzugt eine neue begrenzte UTF-8-JSON-Datei per `--args-file`
verwenden. `--args-file -` ist nur für kleine, im selben Prozess erzeugte
ASCII-Objekte geeignet. Mehrzeiligen Text oder Nicht-ASCII-Zeichen niemals
durch eine Windows-PowerShell-Pipeline an stdin reichen: deren implizite
Codepage kann Umlaute unbemerkt durch `?` ersetzen. Dafür JSON UTF-8 ohne BOM
in eine private Datei schreiben, diese zurückparsen und ihren Pfad an
`--args-file` übergeben. Schreibe Steuerwerte nie als Inline-JSON in die
Kommandozeile oder Prozessliste. Ist ein eigener Client sinnvoller, lies `openapi` und verwende ausschließlich
die dort aktuell veröffentlichten Verträge. Leite Anzahl und Namen immer aus
der Laufzeitquelle ab.

### NPX-Kurzweg ohne globale Runtime-Installation

Verwende diesen Weg nur auf Windows x64 mit bereits vorhandenem Node.js 22+
und npm, wenn der Nutzer ihn ausdrücklich gewählt oder den Paketabruf im
gezeigten Standardplan bestätigt hat. Der Hauptskill kann dafür direkt aus der
Repository-URL gelesen sein; eine Installation im Ordner und MCP sind dafuer
nicht erforderlich.

Leite aus dem bestätigten absoluten Steuerfallpfad dessen Ordner ab. Starte die
API in einem eigenen laufenden Terminalprozess und halte ihn bis zum sicheren
Ende des Auftrags offen:

```powershell
npx.cmd -y @yadimon/steuer-spar-erklaerung-api --case-dir "<ABSOLUTER_FALLORDNER>"
```

Der erste Start legt nur private Arbeitsordner unter dem normalen
Benutzerprofil an. `--case-dir` bindet den bestätigten Fallordner ausschließlich
an diesen laufenden Prozess. Es ist die Auflösungs- und Schwärzungsgrenze für
`cases:`-Referenzen, keine Zugriffssperre der direkten API.
Es wird kein dauerhafter Launcher in den flüchtigen `_npx`-Cache geschrieben.
Existiert eine benannte oder ungültige Konfiguration, ersetze sie nicht
automatisch.

Meldet der Start, dass auf dem Loopback-Port bereits eine SSE-API läuft, fahre
nicht fort. Es kann eine anders konfigurierte Instanz sein. Verwende entweder
bewusst die laufende Installation oder lasse den Nutzer sie zuerst beenden.

Rufe aus einem zweiten Prozess über die CLI auf:

```powershell
npx.cmd -y -p @yadimon/steuer-spar-erklaerung-api steuer-spar-erklaerung-call discovery
npx.cmd -y -p @yadimon/steuer-spar-erklaerung-api steuer-spar-erklaerung-call workspace_status
```

Verwende für weitere Operationen denselben `-p`-Aufruf vor
`steuer-spar-erklaerung-call`. Die API bleibt der einzige langlebige Prozess;
die einzelnen CLI-Aufrufe enden jeweils selbst. Verifiziere vor Steuerdatenarbeit
Discovery, Arbeitsbereich, `capabilities`, `health`, Produktprofil und
Engine-Major.

Prüfe die Fallbindung über Dateiidentität statt über eine Ordnerangabe:
`list_cases` muss den erwarteten Dateinamen des bestätigten Steuerfalls
enthalten, und `case_hash` auf `cases:<Dateiname>` muss demselben SHA-256
entsprechen wie `Get-FileHash -Algorithm SHA256` auf dem bestätigten absoluten
Pfad. Stimmen Name oder Hash nicht überein oder fehlt die Bindung, beende die
API und starte sie höchstens einmal mit dem bestätigten richtigen Ordner neu;
ändere `config.json` dafür nicht manuell.

In diesem Kurzweg können `settings.md` und ein altes Tracking fehlen. Verwende dann nur die im aktuellen Auftrag ausdrücklich
bestätigten Fall- und Belegpfade sowie den bestätigten Modus; erfinde oder
persistiere keine weiteren Präferenzen. Report und Prüffallkopie bleiben
Pflicht. Beende nach positivem Close-/Hash-Readback auch die Foreground-API mit
Strg+C. Falls der Agent keinen laufenden Prozess halten kann, biete stattdessen
das persistente Setup an.

Soll aus diesem Kurzweg eine dauerhafte Installation im Ordner werden, beende
zuerst die Foreground-API mit Strg+C — sonst belegt sie den Port — und arbeite
danach `docs/INSTALLATION.md` ab. Der NPX-Kurzweg bleibt bewusst der einmalige
Prüflauf ohne Ordnerbindung.

Lege bei direkten Laufzeit- und UI-Aufrufen mit `--journal-file
<neue-private-datei.jsonl>` immer eine neue Journaldatei im privaten
Arbeitsbereich des Agenten an. Die CLI schreibt vor dem API-Aufruf dauerhaft
einen JSONL-Eintrag mit `status="pending"`, `command`, `invocationId` und
`startedAt` und danach `status="complete"`, `exitCode` und vollständigem
`result` oder `status="error"` samt Fehlertext.
Existierende Dateien werden nie überschrieben. `pending`, ein fehlender
Abschlusseintrag oder leerer stdout bedeuten einen unbekannten Zustand: lies
zuerst das Journal und danach frischen API-Zustand, starte dieselbe Aktion aber
nicht erneut. Vermische eigene Diagnoseausgaben nicht mit dem JSON-stdout der
CLI; lies das Journal in einem getrennten Schritt. Verwende für `launch`, `windows`, `collect`, `ui_state`, `close`
und `health` auf langsamen PCs kein künstlich verkürztes Transportlimit. Für
den ersten `launch` in einer VM oder auf einem nachweislich langsamen PC direkt
`--timeout-ms 280000` verwenden; die CLI-Vorgabe von 90 Sekunden kann einen
noch laufenden Kaltstart sonst nur als unbekannten Transportzustand
zurücklassen.
Ein synchronisierter `complete`-Eintrag mit `exitCode=1` ist kein
Transportfehler: lies `result`. Bei `result.ok=false` ist die fachliche
Operation nachweislich fehlgeschlagen oder absichtlich unvollständig. Ein
`collect` mit `kind="collection-incomplete"` und `stopKind="limit-reached"`
darf seine gelesenen Seiten als klar begrenzten Teilstand liefern, aber niemals
als vollständige Prüfung gelten.

Eine Agentensandbox darf die API-Wahrheit nicht durch lokale Prozessproben
ersetzen. Unterdrücktes oder verweigertes `Get-CimInstance`, `Get-Process` oder
`tasklist` beweist keine beendete SSE-PID. Melden `close` nicht gleichzeitig
`ok=true` und `stillRunning=false`, bleibt nur die Aussage: „Meine Automation
ist beendet; SSE kann noch geöffnet sein.“ Behaupte „SSE ist geschlossen“ erst
nach diesem positiven Close-Readback und einer frischen API-Abfrage von
`windows` oder `health`, in der die gebundene PID/HWND nicht mehr läuft.

Rufe nach erfolgreicher Verbindung zuerst `sse_capabilities` beziehungsweise
die API-Operation `capabilities` auf. Diese PC-neutrale Selbstbeschreibung ist
die verbindliche Quelle für verfügbare Selektoren, Klickmuster, erlaubte
Dialogantworten und die sichere Fallback-Leiter; erfinde keine Methode aus
Modellwissen. Prüfe zusätzlich `liveEvidence.operationStatus` vor UI- oder
Steuerdatenaktionen. `untested` bedeutet, dass dieser Weg im Release noch nie
erfolgreich an der echten Anwendung belegt wurde: nicht als bewiesen
darstellen und nur mit ausdrücklicher, passender Fixture-Voraussetzung
erproben. `error-path-only` belegt ausschließlich ein echtes strukturiertes
Fehlerergebnis, aber noch keinen erfolgreichen Fachweg. Der Status ist über
alle Jahresprofile aggregiert und kein Nachweis für das aktuell gebundene
`profile.id`. `liveEvidence.affectsAvailability=false` ist absichtlich rein
informativ; die tatsächliche Serversperre steht weiterhin ausschließlich in
`operationPolicy`.

Vorausgesetzt sind Node.js 22+ mit npm; Python und PowerShell 7 nicht.
Verwendet wird Windows PowerShell 5.1.

## Einstieg

Prüfe zuerst nur Metadaten: Betriebssystem, Architektur, vorhandenes Release,
API-Health, Produktprofil und Arbeitsbereich. Lies danach `settings.md` aus
diesem Arbeitsbereich. Lies noch keine Belege, Connector-Inhalte oder
Steuerdaten.
Ist die Einrichtung unvollständig oder sind Fall und Belegquellen noch nicht
sicher bestätigt, lies
[references/first-run.md](references/first-run.md) und führe den dortigen
einfachen First-Run-Wizard aus. Er stellt vor der technischen Einrichtung nur
die zwei entscheidenden fachlichen Fragen: richtiger Steuerfall und
vollständige Belegordner. Erst danach kann der Nutzer alle gezeigten sicheren
technischen Defaults gemeinsam mit `OK Standard` bestätigen.
Enthält der aktuelle Auftrag bereits absolute Pfade, deren
Vollständigkeitsbestätigung und ausdrücklich `OK Standard` samt den dort
definierten engen read-only Schritten, frage weder Pfade noch Standardplan
erneut ab. `Standard-Prüflauf ausführen` oder `Standard-Einrichtung und Prüflauf ausführen` ist bei genau
einem absoluten Steuerfallpfad und genannten absoluten Belegpfaden eine
gleichwertige Bestätigung dieses engen Vertrags und bestätigt zugleich, dass
diese Belegangabe vollständig ist; „keine Belege“ zählt als vollständige
Angabe. Ein zusätzlicher Satz zur Vollständigkeit ist dann nicht nötig. Fehlt
jede Belegangabe, stelle die zweite fachliche Frage trotzdem.

Fehlt eine funktionierende Einrichtung und wurde nicht ausdrücklich der
NPX-Kurzweg gewählt, arbeite die kanonische Anleitung
`https://github.com/yadimon/steuer-spar-erklaerung-mcp/blob/main/docs/INSTALLATION.md`
ab, statt die Einrichtung frei zu improvisieren. Es gibt kein Setup-Programm:
Ordner anlegen, zwei npm-Pakete und den Skill installieren, API starten,
MCP-Server beim Client anmelden.
Verlange danach einen grünen CLI-Aufruf `health` und bei ausdrücklich
gewähltem MCP zusätzlich Serverliste plus echten Aufruf von `sse_health` mit
strukturiertem `ok=true`; „connected“ oder ein Handshake allein genügt nicht.
Dieser Nachweis muss im MCP-Modus ein tatsächlicher MCP-Tool-Aufruf sein.
`health` über Shell oder direkte API-CLI ist dort kein Ersatz. Ist `sse_health`
im neu gestarteten MCP-Client nicht als Tool verfügbar, stoppe vor jeder
Facharbeit in diesem MCP-Auftrag und melde die fehlende Client-Verifikation.
Im ausdrücklich gewählten NPX-/API-Modus gilt stattdessen der oben definierte
CLI-Readback; fehlendes MCP ist dort kein Fehler.
Wurden Skills oder MCP im aktuellen Lauf neu installiert oder geändert, melde
statt eines vorgetäuschten Tool-Erfolgs „Technisches Setup bereit;
Client-Verifikation nach Neustart offen.“ Fordere genau einen Client-Neustart
an. Der danach gestartete Prüfauftrag führt Serverliste und den echten
MCP-Aufruf `sse_health` vor jedem direkten API-Aufruf aus und setzt bei Erfolg
ohne neue Bestätigungsfrage fort.
Kehre danach automatisch
zum ursprünglichen Prüfauftrag zurück; ein Auftrag wie „Prüfe meine
Steuererklärung“ ist nicht schon durch die Einrichtung erfüllt. Bereits
bestätigte Pfade und Entscheidungen nicht erneut erfragen.
Scheitert der Start, ändere `config.json`, Runtime-Dateien oder Prozesse
niemals manuell als Umgehung. Melde den konkreten sicheren Stopp.

Lies anschließend das in `settings.md` benannte Tracking. Ohne solche Angabe
gibt es kein implizit freigegebenes Tracking; verwende nur eine im aktuellen
Auftrag ausdrücklich genannte Datei. Mit direktem, freigegebenem Dateizugriff darf Markdown nach
Hashprüfung und Backup aktualisiert werden. Über API/MCP sind Textdateien
absichtlich create-only: lies den letzten Stand und schreibe einen neuen
datierten Snapshot unter `workspace:tracking/`, statt eine Datei zu
überschreiben. Bei einer vorhandenen `.xlsx`-Datei verwende
eine verfügbare Tabellenkalkulations-Fähigkeit und erhalte ihre Struktur; die
lokale API selbst liest oder schreibt XLSX nicht. Ist das nicht zuverlässig
möglich, frage, ob zusätzlich Markdown-Snapshots angelegt werden dürfen.
Ersetze Excel niemals still.

## Verbindlicher Ablauf

1. Lies die gespeicherten Nutzerprioritäten und das Tracking, dann
   `capabilities` und den versionsgebundenen Operationskatalog aus der
   API-Selbstbeschreibung. Verifiziere danach API-Health, aktives Profil,
   Engine-Major und Arbeitsbereich.
2. Inventarisiere freigegebene Quellen. Speichere für Dateien Quelle,
   Dateiname, Größe, Änderungszeit soweit verfügbar, SHA-256 und relative
   Zielreferenz. Connectoren erst nach Zustimmung lesen.
   Für PDF-Belege verwende zuerst eine bereits verfügbare PDF-Fähigkeit. Fehlt
   sie, installiere weder Python noch Poppler, sondern rendere gezielt nur die
   für Zieljahr/-zeitraum plausiblen Dateien mit dem ausgelieferten
   `powershell/render-pdf.ps1` in einen neuen privaten Temp-Ordner. Der Helper
   begrenzt Breite und Seitenzahl, überschreibt keine PNG-Datei und liefert
   kompaktes JSON. Starte ihn immer als eigenen Prozess mit
   `powershell.exe -NoProfile -NonInteractive -File`; die WinRT-Runtime mancher
   Windows-Builds kann sonst beim Prozessabbau einen fremden Restcode liefern.
   Erfolg verlangt zugleich Exitcode 0, `ok=true` und den PNG-Readback. OCR
   erfolgt danach bei Bedarf lokal mit `ocr-image.ps1`.
   Rendere nicht vorsorglich Belegordner anderer Jahre vollständig.
   Für eine vollständige SSE-Bestandsaufnahme bevorzuge kurze
   `sse_collect`-Segmente entlang des linearen `Weiter`-Pfads. Lies pro Seite
   Überschrift, Felder und sichtbare Tabellen und kontrolliere Dialog,
   Seitenwechsel, Zyklus sowie Ressourcenlimit. Verwende `sse_table_read` nur
   für eine erkannte lange Tabelle, deren Zeilen virtualisiert sind. Die globale
   Suche dient danach nur zum gezielten Rücksprung auf eine bereits kartierte
   Seite; ein angezeigter Suchtreffer allein beweist keine Navigation. Ist die
   Seite, Tabellenzuordnung oder ein von Qt nicht strukturiert exponiertes
   Bedienelement trotzdem unklar, erfasse zusätzlich mit `sse_screenshot` ein
   Fensterbild im Ergebnisbereich. Nutze es zur visuellen Zustands- und
   Layoutprüfung; Beträge, Auswahlwerte und Vollständigkeit müssen weiterhin
   durch strukturierte Felder, Tabellen und Summen belegt werden.
   Kann die Agentensandbox lokale Ergebnisdateien nicht direkt öffnen, schwäche
   keine ACL. Fordere das Bild mit `includeImage: true` an und lies Textresultate
   über `sse_workspace_read_text` beziehungsweise `workspace_file_read_text`.
   Den globalen Steuerprüfer deterministisch öffnen: zuerst den Navigationsknoten
   `Prüfen und Abgeben`, dann per `goto` ohne Suche mit `direction="Weiter"` die
   Seite `Steuererklärung prüfen`, danach genau einmal `checker_run`. Details
   ausschließlich mit `checker_open` öffnen und lesen; `checker_detail` nicht
   vorher probeweise auf eingeklappte Karten anwenden.
   Auf dynamischen Übersichts- und Listenbereichen zuerst `subpages` verwenden.
   Meldet `table_read` dort `stopKind="no-table"`, ist das kein Grund für freie
   Suche nach Kindüberschriften: wähle einen nicht destruktiven, unmittelbar
   zuvor gelesenen Hyperlink über seine frische `rid` und `click_point`. Vor dem
   nächsten Geschwistereintrag über eine frisch gelesene, nicht destruktive
   Zurück-/Historienaktion oder eine bereits kartierte übergeordnete Übersicht
   zur exakten Liste zurückkehren. Suche nie direkt nach der Listen- oder
   Geschwisterüberschrift; danach deren `subpages` neu lesen. Fehlt ein
   eindeutig gebundener Rückweg, sicher stoppen. Verwerfe das Ergebnis einer
   Navigationsoperation niemals mit `Out-Null`; prüfe `ok` und die erwartete
   Überschrift, bevor der Ablauf fortgesetzt wird.
3. Empfehle Kopien unter `documents`. Bei Ablehnung nur Quelle und Entscheidung
   dokumentieren; Originale nicht verändern.
4. Identifiziere den Originalfall dateibasiert read-only. Vor jeder UI-
   Navigation – auch bei einer reinen Prüfung – Hash berechnen, eine eindeutig
   neu benannte Prüffallkopie unter `cases` erzeugen, beide Hashes vergleichen
   und vor dem Öffnen Bytegleichheit bestätigen. Das Original öffnet nur der
   ausdrücklich gewünschte Originalweg (references/first-run.md).
   Starte eine Einkommensteuerdatei `.ESt<jahr>` immer explizit mit
   `mode="normal"` statt der `einur`-Vorgabe für Gewinnermittlungsdateien.
   Die Prüffallkopie bleibt bis zu einem später ausdrücklich beauftragten,
   inventargebundenen Archiv- oder Bereinigungsschritt bestehen; lösche sie
   nicht mit Roh-Dateibefehlen.
5. Lies unmittelbar vor jeder Änderung Fallreferenz, Zustand, Fensterbindung
   (`HWND`) und Hash neu. Führe genau eine eng gebundene Änderung aus und lies
   Wert sowie Zustand sofort zurück. Für eine Tabellenzeile liefert
   `sse_table_read` mit `sumLabel` die aktuelle Kontrollsumme als `summe`;
   genau dieser Wert gehört unverändert als `expectedBefore` in
   `sse_table_add`, `sse_table_update` oder `sse_table_delete`. Rate ihn nie.
6. Stoppe bei Hash-, Ziel-, Dialog- oder Readback-Abweichung ohne Wiederholung.
   Die read-only Prüfung darf weiterlaufen, wenn sie den unsicheren Zustand
   klar ausgrenzt. Meldet die Prüffallkopie nach Navigation
   `ungespeichert=true`, navigiere nicht weiter. Schließe nur mit bestätigtem
   `discardChanges=true` (der Standard-Prüflauf deckt genau dieses Verwerfen),
   lies `stillRunning=false`, Fenster, Health und beide Hashes zurück, speichere
   nie diesen Navigationszustand, lies die restlichen Abschnitte nach
   references/first-run.md weiter. Beim Originalfall: eigene Bestätigung Pflicht.
7. Verwende für wiederholbare Mehrschrittaufgaben ein versioniertes Szenario
   aus dem installierten API-Vertrag: relative Workspace-Referenzen, eindeutige
   Schritt-IDs, dynamische `$steps.<id>.result...`-Referenzen und obligatorisches
   `finally`. Verwende `continueOnError` nur für rein lesende Diagnosen; danach
   darf keine Hauptmutation folgen.
8. Bringe bei einem fachlichen Prüfauftrag dein Steuerwissen aktiv ein: benenne
   Auffälligkeiten und schlage konkrete Verbesserungen vor, wenn du sicher bist.
   Belege strittige oder betragsrelevante Punkte per Websuche an offiziellen
   deutschen Quellen (Gesetz, BMF-Schreiben, amtliche Anleitungen,
   Rechtsprechung, Herstellerhinweise), nicht an Ratgeberseiten oder Foren.
   Ohne Webzugriff bleiben Prüferauswertung und Belegabgleich; die
   steuerfachliche Bewertung erklärst du dann ausdrücklich für unterblieben,
   statt sie still auf Erinnerungswissen zu stützen. Sag Unsicherheit offen und
   empfiehl bei hohem Risiko eine befugte Steuerfachperson.
9. Schreibe immer einen Ergebnis- oder Stoppreport unter `results` und lies ihn
   abschließend zurück.

## Bedarfsreferenzen

Fehlt für ein benötigtes Control eine Spezialoperation, lies erst dann
[references/ui-fallback.md](references/ui-fallback.md). Bei einem ausdrücklichen
UStVA-, Umsatzsteuer-Voranmeldungs-, Gewinn-Erfassungs- oder Folgejahr-Auftrag
lies vor der Facharbeit
[references/ustva.md](references/ustva.md). Für eine normale Einkommensteuer-
Prüfung werden diese Detailreferenzen nicht benötigt.

Lies [references/betriebsvertrag.md](references/betriebsvertrag.md), bevor du
API/MCP einrichtest, einen Fall öffnest oder einen Report erzeugst.

## Sichtbare UI Automation

Kündige vor dem ersten sichtbaren Schritt an:

> SteuerSparErklärung wird nun sichtbar bedient. Bitte lassen Sie den PC
> entsperrt und SSE sichtbar. Klicken oder tippen Sie während der angekündigten
> Schritte nicht und sperren Sie den Rechner nicht. Ich sage ausdrücklich
> Bescheid, wenn die Bedienung beendet ist. Schwarze Konsolenfenster sind kein
> normaler Betriebszustand.

Beginne erst nach Zustimmung. Eine Zustimmung im aktuellen Auftrag zählt ohne
dritte Rückfrage, wenn sie genau den bestätigten Fall, eine hashverifizierte
Prüffallkopie und sichtbare read-only UI-Navigation in der entsperrten Sitzung
nennt. Kündige die sichtbare Navigation trotzdem mit obigem Hinweis an und
beginne dann. Eine allgemeine Bitte „prüfen“ reicht dafür nicht. Stoppe bei
Nutzerinteraktion, unbekanntem Dialog, Fensterwechsel oder Sperrbildschirm.
Die definierte Formulierung `Standard-Prüflauf ausführen` zählt hier als
diese Zustimmung, wenn der Auftrag zugleich genau einen absoluten Fallpfad und
die vollständigen absoluten Belegpfade nennt.

## Wiederholungsgrenzen

| Situation | Grenze |
|---|---|
| API-Health | Ein erster Versuch plus höchstens zwei Wiederholungen nach je 2 Sekunden und erneutem Lesen der Konfiguration |
| UI-/Fensterbindung | Eine Wiederholung erst nach frischem Fall-, Fenster-, Zustands- und Hash-Readback |
| MCP-Registrierung durch Nutzer | Ein erneuter Hinweis, dann direkte API anbieten |
| Gleiche unbeantwortete Frage | Höchstens zweimal stellen, dann sicher stoppen |
| Hash-, Ziel-, unbekannter Dialog oder Readback abweichend | Keine Wiederholung und keine weitere Änderung |
| Abgebrochener MCP-/API-Aufruf | Zustand ist unbekannt; erst frischen Zustand lesen, dann bewusst entscheiden |
| API-/HTTP-Transporttimeout oder `transport-unknown` | Zustand kann nach bereits gestarteter Operation unbekannt sein; nicht als Unerreichbarkeit behandeln, erst frischen Zustand lesen |

## Stoppen und ehrlich berichten

Stoppe insbesondere bei inkompatiblem OS/Profil, fehlender Vertragsquelle,
unklarem API-Zugang, unsicherem Arbeitsbereich, fehlender Zustimmung,
Connector-Anmeldung, ungeprüfter Arbeitskopie, abweichender Bindung, paralleler
Nutzerinteraktion, ausgeschöpftem Retry-Budget oder fachlicher Unsicherheit.

Berichte bei jedem Stopp:

1. blockierende Bedingung,
2. letzten verifizierten Zustand,
3. ob und welche Dateien oder Arbeitskopien bereits verändert sein können,
4. genau eine nächste sichere Nutzeraktion.

## Ergebnis

Schreibe UTF-8-Markdown nach
`results/YYYY-MM-DD_HH-mm-ss_<kurzer-zweck>.md`. Der Report enthält Auftrag,
Modus, Profil, Engine, Fallreferenz, Quelleninventar, geprüfte Punkte,
Abweichungen, Änderungen mit Vorher/Nachher/Readback, Hashes, Transportwechsel,
fachliche Quellen, Unsicherheiten, Stopps und manuelle Schritte. Entferne Token,
Zugangsdaten und unnötige personenbezogene Daten.

Enthält der Bericht fachliche Aussagen oder Vorschläge, schließe ihn genau so ab:

> Dies ist keine Steuerberatung im Sinne des Steuerberatungsgesetzes und ersetzt
> keine Beratung durch eine befugte Person. Diese Auswertung wurde mit KI
> erstellt und kann Fehler enthalten; prüfen Sie alles vor der Abgabe selbst.

Übergib einen mehrzeiligen Bericht ausschließlich über eine neue UTF-8-
Argumentdatei an `workspace_file_write_text`, nie über eine PowerShell-stdin-
Pipeline. Lies die Datei über die API zurück und vergleiche API-, physische und
aus dem UTF-8-Text berechnete SHA-256-Bytes. Prüfe zusätzlich, dass erwartete
Umlaute erhalten und keine Ersatzfragezeichen entstanden sind. Ist ein
create-only Bericht inhaltlich kodierungsbeschädigt, überschreibe ihn nicht:
markiere ihn in einem neuen korrekt kodierten Bericht ausdrücklich als
verworfen.
Verwende entweder eine vollständige Referenz wie `results:bericht.md` oder
`area="results"` mit `ref="bericht.md"`; kombiniere `area="results"` nie mit
`ref="results/bericht.md"`, weil das einen doppelten Unterordner erzeugt.

Beende mit dem zurückgelesenen relativen Reportpfad und dem ausdrücklichen
Hinweis, dass keine ELSTER-Übermittlung durchgeführt wurde.
