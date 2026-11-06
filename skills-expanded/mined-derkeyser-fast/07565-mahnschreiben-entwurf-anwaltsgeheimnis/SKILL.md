---
name: mahnschreiben-entwurf-anwaltsgeheimnis
description: "Wenn es um Mahnschreiben / Vorgerichtliche Aufforderung in Prozessrecht geht: erstellt den passenden Entwurf aus Sachverhalt, Norm, Beweis und Antrag; liefert eine Fristen- und Risikoampel mit Sofortschritten."
---

# Mahnschreiben / Vorgerichtliche Aufforderung

## Arbeitsweg

- Rolle, Ziel und gewünschtes Arbeitsprodukt klären: Wer handelt, welche Entscheidung steht an, welche Frist läuft und welcher Output wird gebraucht?
- Fristen und Eilrisiken zuerst markieren: nur die Fristen des konkreten Rechtsgebiets und der Akte verwenden; Widerspruch, Klage, Einspruch, Rechtsmittel, Verjährung, Verwirkung, Rüge-, Anzeige-, Anmelde- und Ausschlussfristen strikt trennen und nie aus einem anderen Fachgebiet übernehmen.
- Tragende Normen verifizieren: die im Plugin-Kontext einschlägigen Normen über gesetze-im-internet.de, dejure.org, eur-lex.europa.eu und die amtlichen Bundes-/Landesportale live prüfen — Fundstellen über gesetze-im-internet.de, dejure.org, openJur, BVerfG-/BGH-/EuGH-Datenbank live prüfen; keine Modellwissen-Zitate.
- Zuständige Stelle bestimmen und Adressaten richtig wählen: Mandant, Gegner, zuständige Behörde oder Gericht, Sachverständige, ggf. EU-/internationale Stelle (siehe Skill-Detail).
- Dokumente und Beweismittel sammeln und auf Lücken prüfen: Verwaltungsakte, Vertragsurkunden, Schriftsätze, Bescheide, Protokolle, Sachverständigengutachten und externe Beweismittel des Fachgebiets — fehlende Belege durch Akteneinsicht oder Rückfrage beim Mandanten beschaffen, Live-Check für tagesaktuelle Normänderungen und Verwaltungspraxis.

## Zweck

Entwurf eines anwaltlichen Mahnschreibens (Paragraf 286 Abs. 1 BGB) oder einer qualifizierten vorgerichtlichen Aufforderung mit Fristsetzung. Einsetzbar für Zahlungsverzug, Pflichtverletzungen, Mängelrügen (Paragraf 281 Abs. 1 BGB) und Unterlassungsaufforderungen (Paragraf 8 Abs. 1 UWG, Paragraf 97 Abs. 1 UrhG, Paragraf 14 Abs. 5 MarkenG). Das Schreiben ist anwaltlich unterzeichnet und nach Paragraf 13 RVG abrechenbar.

## Eingaben

- Abgeschlossenes `mahnschreiben-aufnahme.md` im Mandatsordner (Slug)
- Gewünschter Schriftsatztyp: `--zahlungsverzug`, `--mängelrüge`, `--unterlassung`, `--schadensersatz`
- Optional: `--version=N` für Versionierung bei Überarbeitungen
- Optional: `--skip-gate` – Pflicht-Checkliste überspringen (nur mit expliziter Bestätigung)

## Ablauf

1. **Intake laden:** `demand-letters/[slug]/intake.md` einlesen. Fehlende Pflichtfelder als Fehler ausgeben; kein Entwurf ohne vollständigen Intake.

2. **Pflicht-Checkliste (Gate) – vor dem Entwurf:**
 - [ ] Ist die Forderung dem Grunde nach schlüssig dargetan (Paragraf 286 Abs. 1 BGB)?
 - [ ] Ist der Schuldner eindeutig identifiziert (Name, Anschrift, ggf. Handelsregisternummer)?
 - [ ] Ist der Betrag oder die geschuldete Handlung konkret bezeichnet?
 - [ ] Ist die Frist angemessen (i. d. R. 2 Wochen; bei Baurecht oder komplexen Leistungen ggf. länger)?
 - [ ] Sind Verzugsschäden (Paragraf 288 BGB: 5 % über Basiszinssatz bei Verbrauchern; 9 % bei Unternehmen) korrekt beziffert?
 - [ ] Droht ein Güteantrag (Paragraf 15a EGZPO) in bestimmten Bundesländern vor Klageerhebung?
 - [ ] Mandatsgeheimnis: Enthält das Schreiben keine vertraulichen Informationen Dritter?
 - [ ] FRE-408-Äquivalent (DE): Paragraf 278 Abs. 6 ZPO; Vergleichsangebote im Schreiben als solche kennzeichnen.

3. **Schreiben entwerfen:**
 - Briefkopf: Kanzlei, Datum, Aktenzeichen
 - Betreff: Mandant ./. Schuldner – [Kurzbezeichnung des Anspruchs]
 - Einleitung: Mandat und Vertretung
 - Sachverhalt: Knapp, tatsächlich, ohne rechtliche Wertungen
 - Forderung: Betrag / Handlung / Unterlassung, Rechtsgrundlage
 - Fristsetzung: Konkretes Datum (nicht "binnen 14 Tagen", sondern "bis zum [TT.MM.JJJJ]")
 - Konsequenzen: Klageandrohung, Kostenfolge (Paragrafen 91 ZPO, 93 ZPO bei Anerkenntnisklage beachten)
 - Grußformel, Unterschrift

4. **Post-Send-Checkliste:**
 - Zugangsdokumentation (Einschreiben / Fax / gerichtliche Zustellung) planen
 - Frist in Kanzleifristbuch eintragen
 - Mandats-History-Update (`/mandat-update [slug] Mahnschreiben versandt`)

## Quellen und Zitierweise

Verbindlich: `../references/zitierweise.md`.

- Quellenregel: Literatur nur mit Nutzerquelle oder lizenziertem Live-Zugriff; keine Kommentar-, Handbuch- oder Aufsatzfundstellen aus Modellwissen.
- Rechtsprechung zu Verzug und Mahnung vor Ausgabe über https://dejure.org und https://openjur.de verifizieren.
- Zum Verzugszins: Paragraf 247 BGB (Basiszinssatz); Paragraf 288 Abs. 1, 2 BGB. Basiszinssatz zum 01.01.2026: 1,27 Prozent (unveraendert ggue. 01.07.2025). Daraus B2C-Verzugszins 6,27 Prozent, B2B-Verzugszins 10,27 Prozent; halbjaehrliche Anpassung am 01.01. und 01.07. erforderlich. Quelle: https://www.bundesbank.de/de/presse/pressenotizen/bekanntgabe-des-basiszinssatzes-zum-1-januar-2026-basiszinssatz-bleibt-unveraendert-bei-1-27--973974
- Verzugspauschale Paragraf 288 Abs. 5 BGB (B2B): 40 EUR pro Vorgang.

## Ausgabeformat

```
[KANZLEI-BRIEFKOPF]

An: [Name und Anschrift Schuldner]
Datum: TT.MM.JJJJ
Aktenzeichen: [Kanzleiaktenzeichen]
Mandatsgeheimnis – Paragraf 43a Abs. 2 BRAO / Paragraf 203 StGB

Betreff: [Mandant] ./. [Schuldner] – Zahlungsaufforderung / Aufforderung zur Mängelbeseitigung

Sehr geehrte Damen und Herren,

wir vertreten [Mandant] und nehmen wie folgt Stellung:

I. Sachverhalt
...

II. Forderung
Wir fordern Sie auf, den Betrag von EUR [X.XXX,XX] bis spätestens zum [TT.MM.JJJJ] auf unser Anderkonto zu überweisen.

III. Hinweis auf Klage
Sollte die Zahlung nicht fristgerecht eingehen, sind wir angewiesen, unverzüglich Klage zu erheben und die uns entstehenden Kosten nach Paragrafen 91, 788 ZPO gegen Sie geltend zu machen.

Mit freundlichen Grüßen
[Anwalt, Kanzlei]
```

Ausgabe als Markdown-Datei `demand-letters/[slug]/v[N].md`.

<!-- BEGIN ausformulierungspflicht (autogen) -->
> **Ausformulierungspflicht und Formatstandard.** Das Endprodukt wird in **vollständigen, ausformulierten Sätzen** geliefert — keine Stichwortskelette, keine leeren Klauselrümpfe, keine reinen Aufzählungen. Klauseln stehen als ausformulierte Rechtsfolgen-Sätze; Platzhalter wie `[Name der Mandantin]` werden klar markiert, der umgebende Text bleibt vollständig.
>
> **Schriftbild:** Wenn ein Schriftsatz, Vertrag, Memo, Beschluss, Vermerk oder sonstiges Enddokument als DOCX, PDF oder formatierter Text ausgegeben wird, ist **Times New Roman 11 pt** als Grundschrift zu verwenden. Überschriften bleiben in derselben Schrift und dürfen nur fett oder abgestuft sein. Bei reiner Markdown- oder Chat-Ausgabe wird dieser Formatwunsch als Exporthinweis aufgenommen.
>
> **Nummerierung:** Gliederung ausschließlich dezimal (`1`, `1.1`, `1.1.1` und so weiter). Keine römischen Ziffern, keine Buchstaben- oder Mischgliederung.
<!-- END ausformulierungspflicht (autogen) -->

## Risiken / typische Fehler

- Rechtsprechung: keine Entscheidung aus Modellwissen zitieren; vor Ausgabe über offizielle oder frei zugängliche Quelle mit Gericht, Entscheidungsform, Datum, Aktenzeichen und tragender Aussage verifizieren.
- **Paragraf 93 ZPO (sofortiges Anerkenntnis):** Wird der Schuldner sofort klaglos, trägt der Kläger die Kosten; Mahnschreiben vorher immer prüfen, ob es bereits eine wirksame Mahnung gab.
- **Unterlassung ohne Abmahnung:** Im UWG/UrhG/MarkenG ist die Abmahnung (mit Unterlassungsaufforderung und Vertragsstrafe) zwingende Voraussetzung; ohne Abmahnung keine Kostenerstattung (Paragraf 97a Abs. 1 UrhG).
- **Güteantrag-Pflicht (Paragraf 15a EGZPO):** In Bayern, Brandenburg, NRW und weiteren Ländern ist bei bestimmten Streitwerten ein Güteantrag vor Klageerhebung vorgeschrieben.
- **Fristberechnung:** Fristende nicht auf Sonn- oder Feiertag setzen (Paragraf 193 BGB).
