---
name: forderungsschreiben-erste-stufe
description: "Wenn es um Forderungsschreiben Erste Stufe in Fluggastrechte geht: prüft Frist, Form, Zuständigkeit, Rechtsweg und Sofortmaßnahmen; liefert eine Fristen- und Risikoampel mit Sofortschritten."
---
```

Der Skill `fluggastrechte-anlagen-bauen` liest die im Schriftsatz erwähnten Anlagen in Reihenfolge der Erwähnung, konvertiert jede Rohdatei zu PDF, stempelt oben rechts in Arial 12 FETT (= Helvetica-Bold 12pt) den Bezeichner "Anlage K 1", "Anlage K 2" usw. und benennt die Ausgabedatei nach demselben Schema (`Anlage_K_1.pdf`). Optional wird ein Sammel-PDF mit Schriftsatz vorne und durchlaufenden Lesezeichen erzeugt.
