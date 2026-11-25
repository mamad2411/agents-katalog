---
name: risk-based-code-review
description: Use when reviewing or verifying software changes before completion, release, merge, deployment, or acceptance, especially when the appropriate test depth is unclear or security, data, migrations, external interfaces, infrastructure, or user-visible behavior may be affected.
---

# Risikobasierte Softwareprüfung

## Zweck

Prüfe Änderungen nach möglicher Auswirkung, nicht nach Zeilenzahl. Der Katalog ist kein Pflichtprogramm: Wähle zuerst eine Stufe, führe deren Pflichtkern aus und ergänze nur die ausgelösten Fachmodule.

## Wann der Skill gilt

Nutze ihn:

- vor einer Abschluss-, Merge-, Release- oder Deployment-Aussage,
- bei Code-Reviews und Abnahmen,
- nach Fehlerkorrekturen und funktionalen Änderungen,
- bei unklarer Testtiefe,
- immer bei Sicherheits-, Daten-, Migrations- oder Betriebsrisiken.

Nicht nötig ist der volle Skill für reine Fragen ohne Änderung. Bei einer reinen Textkorrektur genügt Stufe 1.

## 1. Prüfstufe bestimmen

Entscheidend ist der schlimmste plausible Schaden. Im Zweifel eine Stufe höher wählen.

### Stufe 1 – Minimal

Gilt nur, wenn **alle** Aussagen zutreffen:

- Änderung ist lokal und leicht rückgängig zu machen.
- Kein ausführbares Verhalten, Vertrag, Build-Artefakt oder generierter Inhalt ändert sich.
- Keine Sicherheits-, Daten-, Berechtigungs-, Migrations- oder Produktionswirkung.

Typisch: Rechtschreibung, Kommentare, nicht ausführbare Dokumentation, isolierte Darstellung ohne Logik.

Pflicht:

- [ ] Exakten Diff und Arbeitsbaum prüfen.
- [ ] Geänderten Inhalt bzw. die Darstellung direkt prüfen.
- [ ] Eine unmittelbar auf die geänderte Datei bezogene Schnellprüfung ausführen, sofern das Projekt eine solche bereits bereitstellt; keinen projektweiten Lint nur dafür einführen.
- [ ] Unbeabsichtigte Änderungen und Geheimnisse ausschließen.

Nicht automatisch nötig: vollständige Suite, Browsermatrix, Backup, Migration, Deployment.

### Stufe 2 – Standard

Gilt, wenn Verhalten oder Zusammenspiel geändert wird, aber kein Hochrisiko-Auslöser vorliegt.

Typisch: Geschäftslogik, normale API-/UI-Erweiterung, Persistenz in bestehendem Schema, Abfragen, mehrere Komponenten.

Pflicht:

- [ ] Alles aus Stufe 1.
- [ ] Anforderung und Akzeptanzkriterium festhalten.
- [ ] Positiv-, Negativ- und relevanten Fehlerfall testen.
- [ ] Betroffene Unit-/Integrations-/Schnittstellentests ausführen.
- [ ] Relevante Regression-Suite ausführen.
- [ ] Persistenz, Zustandsübergänge und Berechtigungen prüfen, falls berührt.
- [ ] Saubere, reproduzierbare Testumgebung verwenden.
- [ ] Benutzerablauf real im Browser prüfen, falls UI berührt.

### Stufe 3 – Hochrisiko

Gilt bereits bei **einem** Auslöser:

- Authentifizierung, Autorisierung, Besitz, Mandanten oder Rollen,
- Geheimnisse, externe Eingaben, Uploads oder Code-/Kommandoausführung,
- personenbezogene, finanzielle oder anderweitig kritische Daten,
- Schema-/Datenmigration, Backup, Restore oder destruktive Aktion,
- Netzwerkzugriff, Redirect, DNS, Browser-Automation oder externe Dienste,
- Queue, Nebenläufigkeit, Hintergrundjob oder verteiltes System,
- Produktionskonfiguration, Container, Deployment oder Infrastruktur,
- breite Änderung, unklare Reichweite oder schwerer Rollback.

Pflicht:

- [ ] Alles aus Stufe 2.
- [ ] Ausgangszustand und Vergleichsbasis erfassen.
- [ ] Sicherheits-, Missbrauchs-, Grenz- und Ausfallfälle prüfen.
- [ ] Vollständige relevante Tests, statische Analyse und Audits ausführen.
- [ ] Produktionsnahe Konfiguration und Betriebsabläufe prüfen.
- [ ] Rollback bzw. Wiederherstellung konkret verifizieren.
- [ ] Kritische Invarianten vor und nach der Änderung vergleichen.
- [ ] Unabhängige zweite Prüfung durchführen.
- [ ] Offene, blockierte und akzeptierte Risiken dokumentieren.

### Harte Eskalationsregeln

- Wenige Zeilen senken die Stufe nicht.
- Ein „optionales“ Feld bleibt mindestens Stufe 2; mit Auth-/Besitzwirkung Stufe 3.
- Dokumentation ist Stufe 2 oder 3, wenn sie Konfiguration, Code, Verträge oder Artefakte erzeugt.
- Fehlende Informationen führen nicht zu Stufe 1, sondern zu Klärung oder höherer Stufe.
- Mehrere kleine Änderungen gemeinsam nach ihrer kombinierten Wirkung einstufen.
- Bereits veröffentlichte Migrationen, öffentliche APIs und produktive Konfiguration sind immer Stufe 3.

## 2. Fachmodule auswählen

Nach der Stufe alle Module markieren, deren Gegenstand direkt oder indirekt berührt wird.

| Änderung betrifft | Pflichtmodule |
|---|---|
| Immer | A, B, R |
| Ausführbarer Code, Build oder Laufzeitverhalten | C, D |
| Logik oder Zustand | D, E, F |
| Tests mit DB/Diensten/Zeit/Zufall | G |
| Auth, Rollen, Eingaben, API-Schreibfelder | H |
| HTTP, URLs, Redirects, Browser, Downloads | I |
| Secrets, Logs, personenbezogene Daten | J |
| Destruktive Datenoperation | K |
| Schema oder Migration | L |
| Container, Konfiguration, Deployment | M |
| UI oder Nutzerablauf | N |
| Listen, Suche, Filter, Sortierung | O |
| Ableitungen, Belege, Auditdaten | P |
| Code oder maschinengeprüfte Artefakte | Q |

Für Stufe 1 gelten ausschließlich die vier Punkte ihres Pflichtkerns; A, B und R strukturieren nur den Bericht und lösen keine weiteren Prüfungen aus. Ab Stufe 2 Module nicht wegen Aufwand auslassen. Nur fachlich unberührte Module sind N/A. Ein aktives Modul macht nicht pauschal jede Zeile darin verpflichtend: Zusätze wie „falls betroffen“, „falls vorhanden“ oder klar fachfremde Einzelpunkte bleiben N/A. Die Pflichtkerne der gewählten Stufe gelten dagegen vollständig.

## 3. Prüfablauf

1. **Scope:** Stand, Basis, Anforderungen und betroffene Komponenten bestimmen.
2. **Stufe:** Minimal, Standard oder Hochrisiko mit Begründung wählen.
3. **Module:** Pflichtmodule anhand der Auslösertabelle auswählen.
4. **Baseline:** Bei Stufe 3 sowie risikoreichen Stufe-2-Änderungen Ausgangstests erfassen.
5. **Prüfen:** Code lesen, Hypothesen bilden und reproduzierbare Tests ausführen.
6. **Gegenprüfen:** Externe Reviewer-Aussagen nicht übernehmen, sondern reproduzieren oder verwerfen.
7. **Finalisieren:** Auf finalem Stand erneut prüfen; Status und Diff kontrollieren.
8. **Berichten:** Bestätigt, fehlgeschlagen, blockiert, N/A und offene Risiken trennen.

## 4. Prüfkatalog

### A – Prüfgegenstand und Beweisführung

- [ ] Commit, Branch, Arbeitsbaum, Artefakt oder Version eindeutig nennen.
- [ ] Anforderungen und Akzeptanzkriterien festhalten.
- [ ] Geänderte und unversionierte Dateien berücksichtigen.
- [ ] Erwartetes und beobachtetes Verhalten trennen.
- [ ] Aussagen durch Test, Ausgabe, Codepfad, Trace, Screenshot oder Diff belegen.
- [ ] Tool-Erfolg nicht automatisch als Beweis der Zustandsänderung behandeln.
- [ ] Einzeltest nicht als Gesamtabnahme darstellen.
- [ ] Annahmen, Blockaden und offene Prüfungen kennzeichnen.
- [ ] Falsch-positive Befunde nach Gegenprüfung verwerfen.

### B – Ausgangszustand und Umfang

- [ ] Status, Vergleichsbasis und vollständigen Diff prüfen.
- [ ] Unbeabsichtigte Dateien, Änderungen und Geheimnisse ausschließen.
- [ ] Vorhandenen Build-, Test-, Analyse- und Auditstatus erfassen.
- [ ] Scope-Abweichungen benennen; Zusatzverbesserungen nicht still bündeln.
- [ ] Bei Hochrisikoänderungen konkreten Rollback-Weg nennen.

### C – Build, Start und Grundfunktion

- [ ] Abhängigkeiten aus sauberem Checkout reproduzierbar installieren.
- [ ] Unterstützte Ziele bauen und Anwendung produktionsnah starten.
- [ ] Start-, Migrations- und Hintergrundprozesse auf Fehler prüfen.
- [ ] Health Checks müssen reale Abhängigkeiten abbilden.
- [ ] Neustart und Abschalten mit laufenden Jobs prüfen, falls betroffen.
- [ ] Installiertes Artefakt dem geprüften Quellstand zuordnen.

### D – Automatisierte Tests

- [ ] Regression möglichst zunächst fehlschlagend belegen.
- [ ] Passende Unit-, Integrations-, Schnittstellen- und E2E-Ebene wählen.
- [ ] Gezielte Tests und relevante Gesamtsuite ausführen.
- [ ] Tests, Assertions, Fehler, Warnungen, Skips und Deprecations auswerten.
- [ ] Positiv-, Negativ-, Grenz-, Leer- und Fehlerfälle abdecken.
- [ ] Fachliche Wirkung statt nur Statuscode oder Textfragment prüfen.
- [ ] Gemeinsamen Lauf, Reihenfolge und Wiederholung berücksichtigen.
- [ ] Vorher-/Nachher-Ergebnisse vergleichen, wenn eine Baseline nötig ist.

### E – Zustandslogik und Datenintegrität

- [ ] Kombinationen mehrerer Zustände und gemischte Teilerfolge prüfen.
- [ ] Cache- und Ableitungsdaten vollständig invalidieren.
- [ ] Neuaufbau aus definierten Quellen deterministisch prüfen.
- [ ] Manuelle und automatische Daten unterscheiden.
- [ ] Referenzen auf Existenz und passenden Typ prüfen.
- [ ] Besitz und Gültigkeit aus vertrauenswürdigem, persistiertem Zustand ableiten.
- [ ] Gleichzeitige Beziehungsänderung darf keine Rechte freischalten.
- [ ] Verwaiste Datensätze und temporäre Artefakte behandeln.
- [ ] Integritätsprüfung vor Commit oder in derselben Transaktion ausführen.
- [ ] Idempotenz sicherstellen.

### F – Transaktionen, Fehler und Nebenwirkungen

- [ ] Zusammengehörige Änderungen atomar ausführen.
- [ ] Teilfehler müssen Daten- und Nebenwirkungen zurückrollen.
- [ ] DB, Datei, Queue und Fremdsystem gemeinsam betrachten.
- [ ] Nach Fehler mit frischer Verbindung den persistierten Zustand prüfen.
- [ ] Retries dürfen nichts duplizieren; Abbruch und Dead Letter prüfen.
- [ ] Nebenläufigkeit, Sperren, Lost Updates und Doppelverarbeitung testen.
- [ ] Fehler nicht als Erfolg loggen oder durch Fallback verdecken.

### G – Reproduzierbare Testumgebung

- [ ] Testdatenbank und Dienste automatisch bereitstellen oder dokumentieren.
- [ ] Effektive Laufzeitkonfiguration statt angenommener Env-Werte prüfen.
- [ ] Schema/Migrationen auch bei bestehender Testdatenbank validieren.
- [ ] Test-, Entwicklungs- und Produktionssystem sicher trennen.
- [ ] Destruktive Tests gegen falsche Ziele absichern.
- [ ] Keine Abhängigkeit von lokalen unversionierten Dateien oder Vorarbeiten.
- [ ] Fixtures deterministisch, isoliert und mehrfach ausführbar halten.
- [ ] Zeit, Zeitzone, Locale, Zufall und externe Netze kontrollieren.
- [ ] Fehlende Infrastruktur darf keinen stillen Scheinerfolg erzeugen.

### H – Authentifizierung, Autorisierung und Eingaben

- [ ] Schreiboperationen verlangen vorgesehene Authentifizierung.
- [ ] Autorisierung pro Objekt, Mandant, Rolle und Beziehung prüfen.
- [ ] Besitz nicht aus manipulierbaren Request-Feldern ableiten.
- [ ] Explizite Allowlist schreibbarer API-Felder verwenden.
- [ ] Interne Status-, Pipeline-, Audit- und Metafelder schützen.
- [ ] Verschachtelte Objekte und Relationen berücksichtigen.
- [ ] Länge, Format, Bereich, Enum und Dateityp serverseitig validieren.
- [ ] Kontextgerecht gegen HTML-, Script-, URL-, SQL- und Kommando-Injection schützen.
- [ ] Groß-/Kleinschreibung, Unicode, Kodierung und Parser-Differenzen testen.
- [ ] Rate- und Ressourcenlimits berücksichtigen.

### I – Netzwerkzugriffe und Weiterleitungen

- [ ] Protokolle explizit und normalisiert erlauben.
- [ ] Credentials, Steuerzeichen und mehrdeutige URLs ablehnen.
- [ ] Loopback, private, link-lokale, reservierte und spezielle IPs für IPv4/IPv6 sperren.
- [ ] Alle DNS-Antworten prüfen und Rebinding bis zur Verbindung verhindern.
- [ ] Browser, HTTP-Client, Downloader und Subressourcen gleich absichern.
- [ ] Jede Weiterleitung erneut validieren.
- [ ] Bei Herkunftswechsel Header, Cookies und Auth-Optionen bereinigen.
- [ ] Alternative Headerdarstellungen und bodylose Redirect-Methoden testen.
- [ ] Redirectzahl, Zeit, Antwort- und Downloadgröße begrenzen.
- [ ] Nicht auflösbare oder nicht eindeutig öffentliche Ziele geschlossen ablehnen.

### J – Geheimnisse, Datenschutz und Logging

- [ ] Keine produktiven Credentials oder Schlüssel versionieren.
- [ ] Entwicklungszugänge dürfen nicht produktiv nutzbar sein.
- [ ] Secrets nicht in argv, URL, Fehler, Log oder Prozessliste offenlegen.
- [ ] Logs auf Tokens, Cookies, personenbezogene und vertrauliche Daten prüfen.
- [ ] Externe Fehler begrenzen, intern aber korrelierbar halten.
- [ ] Temporäre Dateien restriktiv erstellen und löschen.
- [ ] Aufbewahrung, Löschung und Maskierung prüfen.
- [ ] Abhängigkeiten und Images auditieren.

### K – Backup, Restore und destruktive Abläufe

- [ ] Vor Zerstörung lesbares und frisches Backup verlangen.
- [ ] Backup inhaltlich an den aktuellen Datenstand binden.
- [ ] Fingerprint umfasst Quellen, Beziehungen und relevante Felder.
- [ ] Restore isoliert tatsächlich ausführen und fachlich prüfen.
- [ ] Verifikation ohne unnötige Produktionsprivilegien ermöglichen.
- [ ] Temporäre Ressourcen auch bei Fehlern entfernen.
- [ ] Abbruch vor Commit und Fehler während Neuaufbau testen.
- [ ] Rollback und Recovery-Ziele praktisch validieren.

### L – Schema und Migrationen

- [ ] Veröffentlichte Migrationen niemals umbenennen oder umschreiben.
- [ ] Korrekturen als neue Migration liefern.
- [ ] Frische Installation und Upgrade von unterstützten Ständen testen.
- [ ] Beide Wege müssen zum gleichen Schema führen.
- [ ] Historie, Schema und Anwendungscode konsistent halten.
- [ ] Gestaffeltes Deployment und Abwärtskompatibilität prüfen.
- [ ] Sperren, Indizes, Rückfüllung und Datenmenge berücksichtigen.
- [ ] Rollback-Weg und irreversible Transformationen dokumentieren.

### M – Konfiguration, Container und Deployment

- [ ] Effektive zusammengeführte Produktionskonfiguration prüfen.
- [ ] Keine Entwicklungsports, Debug-Modi, Testzugänge oder unsicheren Defaults erben.
- [ ] Nur nötige Interfaces und Ports veröffentlichen.
- [ ] Containerrechte, Root, Capabilities, Sandbox und Netzwerk minimieren.
- [ ] Secrets über vorgesehenes Secret-Management zuführen.
- [ ] Reload/Restart nach Konfigurationsänderung nachweisen.
- [ ] Installiertes Artefakt per Version, Hash oder Verhalten verifizieren.
- [ ] Rollout, Health, Migration und Rollback gemeinsam testen.

### N – UI und Browser

- [ ] Kritische Abläufe real in unterstützten Browsern/Viewports ausführen.
- [ ] Erfolg, leer, laden, Fehler und Berechtigung prüfen.
- [ ] Formulare unverändert, gültig, ungültig und manipuliert testen.
- [ ] Fehlgeschlagenes Speichern darf keine Teiländerung hinterlassen.
- [ ] Links und Filter anklicken und resultierende Daten prüfen.
- [ ] Platzhalterzeilen nicht als Daten zählen.
- [ ] Pagination darf Testobjekte nicht zufällig verstecken.
- [ ] Eindeutige Testdaten unabhängig vom globalen Volumen verwenden.
- [ ] Gleichstand mit identischen Primärwerten und Tie-Breaker testen.
- [ ] Overflow/Sticky, Fokus, Tastatur und Kontrast prüfen.
- [ ] Browser-Skript, Fixtures und Ergebnisformat versionieren.
- [ ] Screenshot, Konsole, Netzwerk und persistierten Zustand gemeinsam auswerten.

### O – Filter, Suche, Sortierung und Pagination

- [ ] Explizite Positiv- und Negativfälle prüfen.
- [ ] Zusammengesetzte AND-/OR-Bedingungen testen.
- [ ] Null und fehlende Werte bewusst behandeln.
- [ ] Sichtbare Anzahl unabhängig berechnen.
- [ ] Erwartete Inhalte zusätzlich zur Anzahl prüfen.
- [ ] Eindeutigen Tie-Breaker für stabile Sortierung verwenden.
- [ ] Seitenwechsel auf Lücken und Duplikate prüfen.
- [ ] Leere, volle und große Ergebnismengen testen.
- [ ] Unbekannte Filter dürfen keinen irreführenden ungefilterten Erfolg erzeugen.

### P – Herkunft und Auditierbarkeit

- [ ] Ableitungen auf konkrete Quellen und Belege zurückführen.
- [ ] Belege müssen fachlich zum Ergebnis gehören.
- [ ] Algorithmus/Modell, Version, Zeit und Konfidenz speichern, falls nötig.
- [ ] Manuelle Überschreibungen kennzeichnen und auditieren.
- [ ] Neuaufbau darf Herkunftsketten nicht verlieren oder umbiegen.
- [ ] Auditdaten nicht öffentlich schreibbar machen.
- [ ] Lösch- und Aufbewahrungsregeln prüfen.

### Q – Statische und unabhängige Prüfung

- [ ] Compiler bzw. Typsystem sinnvoll streng ausführen.
- [ ] Lint, Format und Diff-/Whitespace-Prüfung ausführen.
- [ ] Tote Imports, doppelte Definitionen und unerreichbaren Code suchen.
- [ ] Verschluckte Exceptions und zu breite Catch-Blöcke prüfen.
- [ ] API, Schema und Dokumentation konsistent halten.
- [ ] Kritische Logik unabhängig kalt prüfen lassen.
- [ ] Reviewer-Berichte als Hypothese, nicht als Beweis behandeln.
- [ ] Baselines dürfen neue Fehler nicht bloß ausblenden.

### R – Abschluss und Freigabe

- [ ] Alle vereinbarten Prüfungen auf dem finalen Stand wiederholen.
- [ ] Finalen Status und Diff prüfen.
- [ ] Bestanden, fehlgeschlagen, blockiert, N/A und offene Risiken trennen.
- [ ] Keine Aussage „keine Regressionen“ ohne Baseline-Vergleich.
- [ ] Kein Deployment mit offenen Sicherheits-, Daten- oder Betriebsblockern.
- [ ] Nach Deployment Artefakt, Konfiguration, Migration, Health und Kernablauf prüfen.
- [ ] Rollback-Bereitschaft bis zum Ende der Nachprüfung erhalten.

## 5. Befund- und Abschlussformat

Für konkrete Fehler:

```text
Schweregrad: kritisch | hoch | mittel | niedrig
Ort: Komponente, Datei oder Schnittstelle
Voraussetzung: Zustand und Eingaben
Reproduktion: wiederholbare Schritte
Erwartet: gefordertes Verhalten
Beobachtet: gemessenes Verhalten
Auswirkung: Sicherheit, Daten, Betrieb oder Nutzer
Nachweis: Test, Ausgabe, Screenshot, Trace oder Diff
Status: offen | behoben | nicht reproduzierbar | akzeptiertes Risiko
```

Für die Abnahme:

```text
Prüfstand: <Commit/Artefakt/Version>
Stufe: <1|2|3> – <Begründung>
Aktive Module: <A, B, ...>
Bestanden: <Prüfungen mit Nachweis>
Fehlgeschlagen: <Befunde>
Blockiert/nicht ausgeführt: <Prüfungen und Grund>
N/A: <bewusst ausgeschlossene Module>
Offene Risiken: <Risiko und Entscheidung>
Freigabe: ja | nein | eingeschränkt
```

## Häufige Fehler

| Fehlentscheidung | Korrektur |
|---|---|
| „Nur fünf Zeilen, also Minimalprüfung“ | Auswirkung statt Diffgröße bewerten. |
| „Test grün, also fertig“ | Prüfen, ob der Test die fachliche Zustandsänderung beweist. |
| „API-Feld ist optional, also Low Risk“ | Persistenz und Auth machen es mindestens Standard, ggf. Hochrisiko. |
| „Reviewer hat es gefunden, also stimmt es“ | Reproduzieren oder als unbestätigt markieren. |
| „Alles im Katalog muss immer laufen“ | Nur Stufenpflichten plus ausgelöste Module. |
| „Keine Infrastruktur, daher Skip = grün“ | Als blockiert melden; kein Scheinerfolg. |

## Mindeststandard für Erfolgsaussagen

„Fertig“, „bestanden“ oder „keine Regressionen“ nur sagen, wenn der genaue Stand identifiziert, die risikogerechten Prüfungen frisch ausgeführt und offene bzw. blockierte Punkte sichtbar benannt wurden.
