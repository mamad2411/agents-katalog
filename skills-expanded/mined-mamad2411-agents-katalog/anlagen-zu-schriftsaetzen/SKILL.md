---
name: anlagen-zu-schriftsaetzen
description: "Wenn es um Anlagen zu Schriftsaetzen bauen in Anlagen zu Schriftsätzen geht: erstellt den passenden Entwurf aus Sachverhalt, Norm, Beweis und Antrag; liefert einen verwertbaren Entwurf mit Anträgen, Begründung und Anlagenlogik."
---

# Anlagen zu Schriftsaetzen bauen

Dieser Skill erstellt aus einem Aktenordner ein einreichungsfaehiges Anlagenpaket. Er wird genutzt, wenn ein Schriftsatz bereits steht oder parallel entsteht und die Anlagen in sauberer Reihenfolge, mit nachvollziehbaren Dateinamen und ohne Belegluecken an Gericht, Behoerde oder Gegenseite gehen sollen.

## Arbeitsgang

1. Lies den Schriftsatz oder Entwurf und notiere jede Anlagenreferenz in der Reihenfolge ihres Auftretens.
2. Gleiche die Referenzen mit den vorhandenen Dateien im Aktenordner ab.
3. Vergib eindeutige Kennungen wie `Anlage K 1`, `Anlage B 2` oder eine gerichtsspezifische Sonderlogik, wenn sie im Schriftsatz schon vorgegeben ist.
4. Markiere fehlende Anlagen, doppelte Anlagen, falsch benannte Scans und Dateien, deren Inhalt nicht zur Bezeichnung passt.
5. Erzeuge nur dann ein Anlagenkonvolut, wenn die Reihenfolge plausibel ist; sonst liefere zuerst eine Lueckenliste.

## Werkzeug

Wenn lokale Dateien vorliegen, nutze `werkzeuge/build_anlagenkonvolut.py` als technische Hilfe. Das Werkzeug ersetzt nicht die juristische Kontrolle: Die inhaltliche Reihenfolge muss aus dem Schriftsatz folgen, nicht aus Dateinamen allein.

## Ergebnis

Liefere eine kurze Belegmatrix mit Spalten fuer Anlagenziffer, Dateiname, Dokumenttyp, Datum, Beweisthema, Fundstelle im Schriftsatz, Status und naechsten Schritt. Das Endprodukt wird in vollstaendigen Saetzen erlaeutert; reine Dateilisten reichen nicht.
