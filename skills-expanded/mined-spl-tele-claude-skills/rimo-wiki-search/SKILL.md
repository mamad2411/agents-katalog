---
name: rimo-wiki-search
description: "Durchsucht und indexiert alle Seiten des Rimo-Systems-Wikis (wiki.rimo-systems.com) nach beliebigen Stichworten oder Keywords. Nutzbar in Claude.ai, Claude Cowork und Claude Code. Trigger: Wiki durchsuchen, Rimo Wiki, wiki.rimo-systems.com, Rimo Dokumentation, Handbuch Rimo, Hilfe Rimo, Rimo Anleitung."
---

# Rimo Wiki Search – Skill-Anweisungen

## Zweck
Dieser Skill ermöglicht das Durchsuchen und Indexieren aller Seiten des Rimo-Systems-Wikis unter https://wiki.rimo-systems.com nach beliebigen Stichworten, Keywords oder Themen. Er funktioniert in Claude.ai, Claude Cowork und Claude Code.

## Wann aktivieren
Aktiviere diesen Skill immer, wenn:
- Der Benutzer nach Informationen aus dem Rimo Wiki fragt
- Begriffe wie "Rimo Wiki", "wiki.rimo-systems.com", "Rimo Dokumentation", "Rimo Handbuch", "Rimo Anleitung", "Rimo Hilfe" fallen
- Fragen zu Rimo-Produkten gestellt werden (Cableplus, Projectplus, Workflow Designer, Interfaces, App Neu, Mobile App, BSS)
- Nach Anleitungen, Funktionen oder Features von Rimo-Software gefragt wird

## Vorgehensweise bei der Wiki-Suche

### Schritt 1: MediaWiki-Suche nutzen
Nutze die eingebaute MediaWiki-Suchfunktion über diese URL-Vorlage:
https://wiki.rimo-systems.com/index.php?title=Spezial:Suche&search=SUCHBEGRIFF&ns0=1

Ersetze SUCHBEGRIFF durch den vom Benutzer genannten Begriff (URL-encoded).

### Schritt 2: Volltext-Suche
Für eine breitere Suche verwende:
https://wiki.rimo-systems.com/index.php?title=Spezial:Suche&search=SUCHBEGRIFF&fulltext=1&ns0=1

### Schritt 3: Direkte Seiten aufrufen
Bekannte Hauptbereiche des Wikis:
- Hauptseite: https://wiki.rimo-systems.com/index.php?title=Hauptseite
- Alle Seiten: https://wiki.rimo-systems.com/index.php?title=Spezial:Alle_Seiten
- Alle Kategorien: https://wiki.rimo-systems.com/index.php?title=Spezial:Kategorien
- Cableplus: https://wiki.rimo-systems.com/index.php?title=Cableplus
- Projectplus: https://wiki.rimo-systems.com/index.php?title=Projectplus
- Workflow Designer: https://wiki.rimo-systems.com/index.php?title=Workflow_Designer
- Interfaces: https://wiki.rimo-systems.com/index.php?title=Interfaces
- App Neu: https://wiki.rimo-systems.com/index.php?title=App_Neu
- Mobile App: https://wiki.rimo-systems.com/index.php?title=Mobile_App
- BSS: https://wiki.rimo-systems.com/index.php?title=BSS
- Basisbedienung: https://wiki.rimo-systems.com/index.php?title=Basisbedienung
- Release Notes: https://wiki.rimo-systems.com/index.php?title=Release_Notes

### Schritt 4: Ergebnisse aufbereiten
1. Navigiere zur Suchergebnis-Seite
2. Lies den Inhalt der relevanten Treffer
3. Präsentiere dem Benutzer eine strukturierte Übersicht mit:
   - Seitentitel und direktem Link
   - Kurze Zusammenfassung des Inhalts
   - Relevanz für den gesuchten Begriff

## Regeln
- Suche immer zuerst über die MediaWiki-Suche, bevor du direkte URLs abrufst
- Bei unklaren Begriffen frage den Benutzer nach Präzisierung (z.B. welches Modul)
- Gib immer die direkten Wiki-Links zu den gefundenen Seiten an
- Wenn eine Seite nicht direkt gefunden wird, versuche Varianten des Suchbegriffs
- Zeige dem Benutzer, auf welchen Seiten der Begriff vorkommt und in welchem Kontext