---
name: dokumente
description: Arbeitsweisen für Dokument- und Bildaufträge — PDF-Extraktion mit read_pdf, Umgang mit Scans, Tabellen, Bildbeschreibungen und Datenschutz. Nutze dies bei jedem Dokument-/Bilderauftrag.
---
# Dokumente & Bilder — Arbeitsanweisungen

Der Katalog der Arbeitsschritte für Dokumenten- und Bildaufträge.

## PDFs

1. **Immer zuerst `read_pdf`** — nicht `read` (das liefert bei PDFs
   Binärdaten). `read_pdf` liefert den Text pro Seite (`Seite N:`).
2. **Scans erkennt es automatisch** (keine Textebene → LlamaParse-Cloud-OCR,
   dauert 1–2 Minuten). Mit `ocr: true` erzwingst du LlamaParse auch bei
   Text-PDFs, wenn das Layout wichtig ist (Tabellen, mehrspaltig).
3. Bei langen PDFs: erst Umfang schätzen, dann gezielt die relevanten
   Seiten lesen; `pages`-Parameter nutzen ("1-5,12").
4. Beim Zitieren: **(S. 12)** — immer mit Seitenzahl. Wörtliche Zitate in
   Anführungszeichen, sonst sinngemäß zusammenfassen.

## Kollektionen (Fotos & PDFs als Bundle)

Eine **Kollektion** = alle Dateien EINER Nachricht (Fotos und/oder PDFs).
Sie ist ein zusammenhängendes Werk, das man befragen und damit reden kann —
kein Stapel Einzelbilder.

1. Reihenfolge klären (Übermittlungsreihenfolge; bei Unklarheit nachfragen).
2. Alles anlesen: Fotos direkt ansehen, PDFs mit `read_pdf` — pro Item
   einordnen (Text, Bild, Tabelle).
3. Erst DANN als Ganzes auswerten ("die Kollektion gelesen…"):
   - Gesamt-Zusammenfassung (2–5 Sätze)
   - Struktur der Kollektion (welches Item enthält was)
   - Roter Faden: Zusammenhänge über Item- und Mediengrenzen hinweg
4. Zitieren: **(Foto 2)**, **(PDF S. 3)** — Item + Seitenzahl. Übernimmt der
   Nutzer einen Namen ("Kollektion Urlaub"), verwende ihn konsequent.
5. Auf Fragen zur Kollektion antworten, ohne alles zu wiederholen — nur den
   relevanten Teil mit Zitat.
6. Lücken melden: "zwischen Foto 4 und PDF Seite 2 fehlt offenbar eine Seite."
7. Bei Wunsch: Gesamt-Auswertung als Markdown-Datei im Workspace speichern
   (z. B. `kollektion-urlaub.md`) und den Pfad nennen. Für Folgefragen bleibt
   die Kollektion im Kontext der Session.

## Tabellen

- Als Markdown-Tabelle wiedergeben, Spalten vom Original behalten.
- Leere Zellen als `—`, unleserliche als `?` markieren.
- Summen/Zeilensummen prüfen und auf Abweichungen hinweisen (Rechnungen!).

## Bilder

- **Dokumentfotos** (Rechnung, Ausweis, Brief): alle Felder strukturiert
  ausgeben (Absender, Datum, Beträge, …). Unsichere Erkennung kennzeichnen.
- **Fotos/Screenshots allgemein**: erst das Wesentliche in 1–2 Sätzen,
  dann Details (Personen/Objekte/Texte/Zahlen/ Kontext).
- **Text im Bild**: immer vollständig transkribieren, in einem Block zitiert.
- Bei Unleserlichem: nach einer besseren Aufnahme bitten, nicht raten.

## Ergebnisse ablegen

Wenn der Nutzer eine Auswertung als Datei will: als Markdown im Workspace
speichern (z. B. `auswertung-rechnung.md`) und den Pfad nennen.

## Datenschutz-Hinweis

Dokumente können persönliche Daten enthalten. Gib Inhalte nur im Chat
wieder bzw. speichere sie nur im Workspace des Nutzers — niemals anderswo.
