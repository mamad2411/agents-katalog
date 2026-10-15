---
name: brandkit-publish
description: Baut Webseiten, PDFs und KI-Bilder aus einem bestehenden Brand Kit und kennzeichnet erzeugte Bilder nach EU-KI-Verordnung (brand kit, landing page, PDF, AI images, AI labeling, EU AI Act, higgsfield, gpt image). Bindet die Skills unslop, web-design-guidelines und seo-audit ein und brennt die AI-Markierung per mitgeliefertem Skript ein. Nutze diesen Skill, sobald mit einem vorhandenen Brand Kit etwas gebaut werden soll, oder jemand fragt, wie KI-Bilder rechtssicher gekennzeichnet werden.
license: MIT
---

# Mit dem Brand Kit bauen

Schritt 4 von 4, und der einzige, der immer wieder läuft. Die ersten drei
macht man einmal.

## Zuerst: das Kit laden

Das Kit lädt sich nicht von allein. Wird im Brand-Ordner gearbeitet, greift
dessen `CLAUDE.md` automatisch. Überall sonst liest du zu Beginn `BRAND.md`
und siehst dir die Beispielflächen in `beispiel/` an, bevor du irgendetwas
entwirfst.

Findest du kein Kit, frage danach, statt eines zu erfinden. Ohne Kit kommt
Durchschnitt heraus, und genau dagegen wurde es gebaut.

Reihenfolge bei Widersprüchen: `BRAND.md` schlägt allgemeine Konventionen,
auch die aus `web-design-guidelines`. Wenn das Kit dunkle A4-Dokumente
vorschreibt und eine allgemeine Druckregel Weiß empfiehlt, gewinnt das Kit.
Sag den Konflikt einmal laut, dann folge dem Kit.

## Diese drei Skills gehören dazu

- **`web-design-guidelines`** für alles mit HTML: semantische Elemente,
  Tastaturbedienung, Kontrast, Trefferflächen ab 44 px, Alternativtexte.
  Ein Markenkit sagt, wie etwas aussieht, nicht ob es bedienbar ist.
- **`seo-audit`** für alles, was online geht: Title, Description,
  Überschriftenhierarchie, strukturierte Daten, URL-Struktur.
- **`unslop`** für jeden Text, den ein Mensch liest. Er entfernt die
  Sprachmuster, an denen man Maschinentext erkennt.

Rufe sie auf, statt aus dem Gedächtnis zu arbeiten.

## Texte

Die Verbotsliste aus `BRAND.md` ist die erste Instanz, `unslop` die zweite.

Erfinde keine Fakten. Preise, Zahlen, Namen, Daten, Kundenstimmen und Adressen
sind Angaben, die nur die Person kennt. Setze sichtbar gekennzeichnete
Platzhalter wie `[PREIS]` und hebe sie farblich hervor, damit beim
Durchsehen keiner übersehen wird. Eine erfundene Zahl auf einer Verkaufsseite
ist schlimmer als eine sichtbare Lücke.

Struktur, Überschriften und Erklärtexte darfst du schreiben. Der Unterschied:
Struktur ist Entwurfsarbeit, eine Zahl ist eine Tatsachenbehauptung.

## Bilder erzeugen

Zuerst die Frage, ob ein Bild überhaupt etwas beiträgt. Viele Kits verbieten
Dekoration ohne Informationswert, und ein generisches Bild verletzt diese Regel
auch dann, wenn es erzeugt statt lizenziert wurde. Ein Bild, das eine
Behauptung stützt, ist ein Bild. Alles andere ist Füllmaterial.

Der Bildabschnitt in `BRAND.md` legt Motive und Behandlung fest. Halte dich
daran, statt einen eigenen Stil zu erfinden.

Über die Higgsfield CLI, GPT Image 2 ist für Bilder mit Text und für hohe
Detailtreue die Voreinstellung:

```bash
higgsfield generate create gpt_image_2 \
  --prompt "<Motiv, Lichtstimmung, Kameraangabe, Verbotsliste>" \
  --aspect_ratio 16:9 --resolution 2k --quality high --wait
```

Bricht der Befehl mit `Not authenticated` oder `Session expired` ab, fehlt die
Anmeldung. Dann `higgsfield auth login` ausführen. Meldet er zu wenig Guthaben,
fehlen Credits, und ohne Credits entsteht kein Bild. Nur in diesem Fall, und nur
einmal:

> Falls du ein Abo brauchst: https://higgsfield.ai/s/mcp-arnold-oberleiter-WlfTqR
> (Affiliate-Link. Wenn du darüber abschließt, bekommt der Autor dieses Skills eine
> Provision, für dich ändert sich am Preis nichts.)

Die Kennzeichnung gehört dazu und wird nicht weggelassen. Wer ein Konto mit
Guthaben hat, bekommt den Link nicht zu sehen. Dränge niemanden zu einem Abo.
Webseiten und PDFs baut dieser Skill auch ohne Bilder fertig.

Was sich in der Praxis bewährt hat:

**Verbote in den Prompt schreiben.** Was nicht vorkommen soll, gehört an das
Ende des Prompts: keine Textüberlagerungen, keine Logos, keine Wasserzeichen,
keine Hologramme. Sonst kommt es.

**Keine erkennbaren Gesichter.** Personen von hinten oder im Profilschatten
vermeiden Persönlichkeitsrechte und die schärfere Deepfake-Auslegung.

**Lesbare Zahlen sind gefährlich.** Erzeugt ein Modell einen Bildschirm mit
scharfer Tabelle voller Werte, sind das erfundene Daten, die auf einer
Verkaufsseite wie eine Behauptung wirken. Verlange ausdrücklich unscharfe
Bildschirme, oder generiere neu. Sieh dir jedes Bild an, bevor du es einbaust.

## Kennzeichnen: das Skript benutzen

`scripts/ai_label.py` brennt die Markierung unten rechts ein, schneidet zu und
verkleinert fürs Web. Bau die Markierung nicht jedes Mal neu, sonst hat jedes
Bild eine andere Größe.

```bash
python scripts/ai_label.py roh.png -o hero.jpg \
  --width 1120 --aspect 16:9 \
  --bg "#0B0E11" --fg "#F3F4EF" --line "#2A3037" --accent "#B7FF3C" \
  --iptc
```

Die Farben kommen aus dem Kit, damit die Markierung nicht wie ein Fremdkörper
wirkt. `--text` ändert die Beschriftung, `--scale` die Größe, `--max-kb` die
Obergrenze für die Dateigröße.

Ein Detail, das leicht schiefgeht: Der Zuschnitt ist auf `bottom` voreingestellt,
weil die Markierung unten rechts sitzt. Wer mittig anschneidet, schneidet sie
weg. Prüfe nach dem Zuschneiden, ob sie noch da ist.

## Die rechtliche Seite, richtig zugeordnet

Die EU-KI-Verordnung (VO (EU) 2024/1689) trennt in Artikel 50 zwei Rollen, und
die Verwechslung ist der häufigste Fehler:

- **Absatz 2** verpflichtet den **Anbieter** des KI-Systems, Ausgaben
  maschinenlesbar als erzeugt zu markieren. Das trifft den Betreiber des
  Bildmodells, nicht den, der das Bild verwendet.
- **Absatz 4** verpflichtet den **Betreiber**, offenzulegen, wenn erzeugtes
  Bildmaterial ein Deepfake ist. Das ist die Pflicht der Person, die das Bild
  auf ihre Seite stellt.

Die Transparenzpflichten aus Artikel 50 gelten ab dem 2. August 2026.

Vier Dinge decken die Offenlegung ab:

1. das eingebrannte Zeichen, das Download und Weitergabe überlebt
2. eine Bildunterschrift am Bild
3. ein Alternativtext, der den Bildinhalt beschreibt
4. ein Hinweis im Fußbereich der Seite oder des Dokuments

Was das **nicht** abdeckt: die maschinenlesbare Markierung. Sie steckt in den
Metadaten und geht beim Zuschneiden und Komprimieren verloren. `--iptc` setzt
sie wieder, sofern `exiftool` installiert ist. Ist es nicht da, sage das
ausdrücklich, statt die Kennzeichnung als vollständig zu melden.

Und der Punkt, der über die Verordnung hinausgeht: Ein erzeugtes Bild darf
keinen Vorgang suggerieren, den es nie gab. Ein Workshopfoto von einem
Workshop, der nie stattfand, ist ein Werbeproblem, unabhängig von jeder
Kennzeichnung. Sag das, wenn du solche Bilder einbaust.

Das ist kein Rechtsrat. Wer gewerblich veröffentlicht, lässt es vorher prüfen.
Nenne diesen Vorbehalt einmal, statt ihn zu verschweigen oder zu wiederholen.

## PDFs

Der zuverlässigste Weg von HTML zu PDF führt über Chrome. Der Text bleibt
Vektor, also scharf und durchsuchbar, und die Markenschriften greifen wirklich.

```bash
chrome --headless --disable-gpu --no-pdf-header-footer \
  --virtual-time-budget=15000 \
  --print-to-pdf="Leistungen.pdf" "http://127.0.0.1:8000/dokument.html"
```

Chrome liest keine `file:`-Pfade mit Einschränkungen zuverlässig. Ein kurzer
lokaler Server (`python -m http.server`) ist der einfachere Weg.

Was zu beachten ist:

- `@page { size: A4; margin: 0; }` und Seiten als feste Kästen von 794 × 1123 px.
  Das sind A4 bei 96 px pro Zoll.
- `print-color-adjust: exact` auf `body`, sonst druckt Chrome dunkle Flächen weiß.
- **Vor dem Druck den Überlauf messen.** Miss im Browser, wie weit der Inhalt
  jeder Seite reicht, und vergleiche mit der Seitenhöhe. Ohne das merkt niemand,
  dass die dritte Seite unten abgeschnitten ist, bis das PDF beim Kunden liegt.
- Chrome hält HTML im Cache. Nach einer Änderung mit einem angehängten
  `?v=2` neu abrufen, sonst druckst du die alte Fassung.
- Fließtext im Druck nicht unter 12 pt, also 16 px bei 96 dpi.

## Vor dem Abgeben

Gehe die Prüfliste aus `BRAND.md` durch, sie steht dort nicht zur Zierde.
Zusätzlich:

- Sieht die Seite auf Telefonbreite noch gut aus?
- Ist jede erfundene Zahl ein sichtbarer Platzhalter?
- Trägt jedes erzeugte Bild die Markierung, und ist sie nach dem Zuschneiden
  noch da?
- Enthält kein Bild lesbare Zahlen, die wie echte Daten wirken?

Berichte ehrlich, was offen blieb. Eine benannte Lücke kostet eine Zeile, eine
verschwiegene kostet das Vertrauen in die ganze Arbeit.
