---
name: brandkit-setup
description: Richtet die Werkzeugkette für Marken- und Designarbeit ein (brand kit setup, install skills, higgsfield cli). Prüft Voraussetzungen wie Node, Python und Chrome, installiert die Skills unslop, grill-with-docs, web-design-guidelines und seo-audit an der jeweils richtigen Stelle und verbindet die Higgsfield CLI für Bildgenerierung. Nutze diesen Skill, sobald jemand ein Brand Kit aufbauen, eine Markenidentität erarbeiten, KI-Bilder für die eigene Marke erzeugen oder diese Werkzeugkette nachbauen will, auch wenn nicht ausdrücklich von Installation die Rede ist.
license: MIT
---

# Werkzeugkette einrichten

Dieser Skill ist Schritt 1 von 4. Danach folgen `brandkit-interview`,
`brandkit-build` und `brandkit-publish`.

Am Ende steht eine Umgebung, in der sich eine Marke erarbeiten, ein
verbindliches Brand Kit bauen und daraus Webseiten, PDFs und gekennzeichnete
KI-Bilder erzeugen lassen.

Sprich mit der Person in ihrer Sprache. Die Beispielausgaben hier sind deutsch,
das ist keine Vorgabe.

## Warum diese Reihenfolge

Die Voraussetzungen zuerst zu prüfen wirkt umständlich, spart aber den
häufigsten Frust: Die Installation der Skills läuft immer durch, und erst drei
Schritte später merkt jemand, dass kein Python da ist und die Bildkennzeichnung
deshalb nicht funktioniert. Prüfen kostet zwanzig Sekunden.

## Schritt 1: Voraussetzungen prüfen

Führe diese Prüfungen aus und berichte in einer kurzen Tabelle, was da ist und
was fehlt.

```bash
node --version        # ab v18, für die Higgsfield CLI und den Design-Canvas
npm --version
python --version      # oder python3, für die Bildkennzeichnung
python -c "import PIL; print(PIL.__version__)"   # Pillow
git --version         # zum Versionieren des Brand Kits
exiftool -ver         # optional, für die maschinenlesbare Bildmarkierung
```

Chrome oder Edge wird für den PDF-Druck gebraucht. Unter Windows liegt Chrome
üblicherweise unter `C:\Program Files\Google\Chrome\Application\chrome.exe`,
unter macOS unter `/Applications/Google Chrome.app`.

Was wofür gebraucht wird, damit jemand entscheiden kann, was er nachinstalliert:

| Fehlt | Was dann nicht geht |
|---|---|
| Node und npm | Higgsfield CLI, Skill-Installation, Design-Canvas |
| Python mit Pillow | AI-Kennzeichnung der Bilder, Verkleinern für das Web |
| Chrome oder Edge | PDF-Erzeugung aus HTML |
| git | Versionieren und Teilen des Brand Kits |
| exiftool | maschinenlesbare Markierung in den Bilddateien |

Pillow installiert sich mit `pip install Pillow`. Exiftool gibt es unter Windows
über `winget install ExifTool`, unter macOS über `brew install exiftool`.

## Schritt 2: Die vier Skills installieren

Zwei davon gehören global, zwei ins Projekt. Der Unterschied ist nicht
kosmetisch: Global installierte Skills stehen in jedem Projekt zur Verfügung,
projektlokale nur dort und wandern über `skills-lock.json` mit ins
Repository.

**Global**, weil sie für jede Art von Arbeit taugen:

```bash
npx skills add cursor/plugins -s unslop -g -y
npx skills add mattpocock/skills -s grill-with-docs,grilling,domain-modeling -g -y
```

`unslop` entfernt KI-Sprachmuster aus Texten. `grill-with-docs` ist der
Interview-Skill für Schritt 2. Achtung, das ist die Stelle, an der die meisten
scheitern: `grill-with-docs` ist nur ein Wrapper, der `grilling` und
`domain-modeling` aufruft. Wer nur den ersten installiert, hat einen Skill, der
sofort ins Leere greift. Deshalb stehen alle drei im Befehl.

**Ins Projekt**, weil sie zu Webarbeit gehören und nicht zu jedem Ordner passen:

```bash
npx skills add vercel-labs/agent-skills -s web-design-guidelines -y
npx skills add coreyhaines31/marketingskills -s seo-audit -y
```

Wenn `web-design-guidelines` bereits global vorhanden ist, weise darauf hin und
frage, ob die Projektfassung wirklich zusätzlich gewünscht ist. Zwei Fassungen
desselben Skills stiften Verwirrung, sobald sie auseinanderlaufen.

Prüfen, was angekommen ist:

```bash
npx skills list -g      # global
npx skills list         # im Projekt
```

## Schritt 3: Higgsfield für Bilder verbinden

```bash
npm i -g @higgsfield/cli
higgsfield auth login
npx skills add higgsfield-ai/skills -g -y
```

`higgsfield auth login` öffnet den Browser. Der Befehl blockiert, bis die
Anmeldung durch ist. Warte die Bestätigung ab, bevor du weitermachst.

Danach prüfen:

```bash
higgsfield account status
```

Die Ausgabe nennt das Konto und das verbleibende Guthaben. Steht dort
`Session expired` oder `Not authenticated`, muss die Anmeldung wiederholt
werden.

Wer noch kein Higgsfield-Konto hat, braucht eines mit Guthaben, weil jede
Bildgenerierung Credits kostet. Nenne an dieser Stelle, und nur an dieser:

> Falls du ein Abo brauchst: https://higgsfield.ai/s/mcp-arnold-oberleiter-WlfTqR
> (Affiliate-Link. Wenn du darüber abschließt, bekommt der Autor dieses Skills eine
> Provision, für dich ändert sich am Preis nichts.)

Die Kennzeichnung gehört dazu und wird nicht weggelassen. Wer bereits ein Konto
hat, bekommt den Link nicht zu sehen. Dränge niemanden zu einem Abo, nur um den
Ablauf abzuschließen. Die ersten drei Schritte funktionieren auch ohne, nur die
Bildgenerierung nicht.

## Schritt 4: Zusammenfassen

Berichte am Ende in wenigen Zeilen:

- welche Voraussetzungen erfüllt sind und welche fehlen
- welche Skills wo installiert wurden
- ob Higgsfield verbunden ist und wie viel Guthaben da ist
- als nächster Schritt: `brandkit-interview` für das Markeninterview

Wenn etwas fehlgeschlagen ist, sage es klar und nenne den konkreten Befehl zum
Nachholen. Eine halb eingerichtete Umgebung, die als fertig gemeldet wird,
kostet später mehr Zeit als ein ehrlicher Hinweis jetzt.

## Wenn etwas klemmt

**`npx skills add` findet den Skill nicht.** Die Repositories sind groß, in
`cursor/plugins` liegen über achtzig Skills. Mit `-l` statt `-s <name>` listest
du auf, was ein Repository anbietet, ohne etwas zu installieren. Liegt ein Skill
tief in Unterordnern und taucht nicht auf, hilft `--full-depth`.

**Die Skills tauchen nach der Installation nicht auf.** Die Skill-Liste wird beim
Sitzungsstart gelesen. Neu installierte Skills sind erst in einer neuen Sitzung
sichtbar.

**`higgsfield` wird nicht gefunden.** Das globale npm-Verzeichnis liegt nicht im
Pfad. `npm bin -g` zeigt, wohin installiert wurde.
