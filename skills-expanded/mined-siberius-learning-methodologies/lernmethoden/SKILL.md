---
name: lernmethoden
description: Gestalte oder überprüfe Bildungsanwendungen durch die Verknüpfung von Lernzielen, Lernbedürfnissen, Aktivitäten, Feedback und Lernnachweisen. Verwende diesen Skill für neue Lernwerkzeuge oder wesentliche Änderungen ihres didaktischen Designs.
metadata:
  version: "1.6.0"
  language: "de"
  based_on: "learning-methodologies@1.6.0"
  license: "MIT"
  repo: "https://github.com/siberius/learning-methodologies"
  author: "Luděk Sušický"
  format: "natives Paket mit generiertem eigenständigen Markdown"
---

# Lernmethoden

Unterstütze die Konzeption, Umsetzung oder Begutachtung von Bildungsanwendungen, deren Lernaktivitäten, Scaffolding und Leistungsbeurteilung den Bedürfnissen der Zielgruppe entsprechen. Passe die Bearbeitungstiefe an Anfrage, Tragweite und Unsicherheit an. Eine kurze Unterrichtsaktivität benötigt weder eine vollständige Evaluationsstudie noch ein neues Planungsdokument.

## Didaktische Methoden für mit KI erstellte Anwendungen

Nutze diese Methoden, um pädagogische Ziele in konkrete Lernendenhandlungen, Feedbackregeln und Lernnachweise in der erstellten Anwendung zu übersetzen. So erfordert aktiver Abruf (Retrieval Practice) einen eigenständigen Antwortversuch vor der Auflösung; Scaffolding erfordert dosierbare Hilfestellungen und die Unterscheidung zwischen unterstützter und selbstständiger Leistung. KI kann bei der Umsetzung dieser Entscheidungen helfen; ihre Ausgabe bedarf stets der fachlichen und fachdidaktischen Prüfung. Dies gilt sowohl für Offline-Anwendungen als auch für den begründeten Einsatz von Laufzeit-KI.

Konsultiere die [Didaktische Begründung](references/didactic-rationale.md), um die Wahl einer Methode zu begründen oder in die Implementierung zu überführen. Sie verknüpft didaktische Methoden mit Produktentscheidungen und den erforderlichen Lernnachweisen.

## Den Ersteller durch didaktische Entscheidungen führen

Prüfe bei jeder wesentlichen didaktischen Entscheidung Lernziel, Lernendenhandlung, Lernnachweis, Unterstützungsmaßnahmen und Rahmenbedingungen. Baue auf getroffenen Entscheidungen auf. Biete bei einer offenen, folgenreichen Entscheidung eine kleine, relevante Auswahl an – meist zwei bis drei Optionen – jeweils mit einer verständlichen Beschreibung und dem konkreten Bezug zum vorliegenden Projekt. Empfehle eine Option, erläutere den zentralen Kompromiss und frage, welchen Ansatz der Ersteller bevorzugt. Lies den [Entwurfsdialog](references/design-dialogue.md), wenn eine solche Entscheidung begonnen oder wieder aufgegriffen wird. Dieser Dialog steuert die Abstimmung mit dem Ersteller, getrennt von der späteren Interaktion zwischen Tutor und Lernendem.

Bereits getroffene oder abgelehnte Entscheidungen werden ohne neue sachliche Gründe nicht erneut aufgerollt. Respektiere die ausdrückliche Delegation von Routineentscheidungen und fahre mit einer kurzen Begründung fort. Schweigen gilt nicht als Zustimmung zur Erweiterung des Projektumfangs. Arbeite während eventueller Wartezeiten an unabhängigen Komponenten weiter. Kosmetische Änderungen lösen diesen Prozess nicht aus.

Referenzen nach Bedarf laden: [Methoden](references/methods.md) für Lernaktivitäten und Scaffolding; [Lernspiele](references/learning-games.md) für Motivation und Spielmechaniken; [Leistungsbeurteilung](references/assessment.md) für Lernnachweise und Bewertung; [Kognitive Benutzeroberfläche](references/cognitive-ux.md) für Repräsentationen, Multimedia und Aufmerksamkeit; [Adaptives Üben](references/adaptive-practice.md) für wiederholte Lerneinheiten und adaptive Schwierigkeitsgrade. Nutze die nachstehenden Pfade für Simulationen, Tutor-Zustände und Laufzeit-KI. Lies die jeweilige Referenz vor dem Vorschlag einer Methode; lade nicht alle Dateien auf einmal.

Übertrage die gewählte Methode in beobachtbares Anwendungsverhalten und aussagekräftige Tests. Unterscheide sauber zwischen vorgeschlagenen, ausgewählten, implementierten und verifizierten Entscheidungen. Technische Funktionstests belegen noch keinen Lernerfolg.

## Arbeitsablauf

Durchlaufe diesen Pfad in der für die Aufgabe angemessenen Tiefe: Ziel und Rahmenbedingungen klären → Methode passend zum Lernhindernis wählen → Handlung des Lernenden mit Lernnachweisen verknüpfen → im vereinbarten Umfang umsetzen → Ergebnis überprüfen. Untersuche bei einem didaktischen Review den bestehenden Entwurf, statt neu zu implementieren. Nutze bekannten Kontext; verlange nicht für jeden Schritt ein Planungsdokument.

Konsultiere die [Entscheidungsbeispiele](references/decision-examples.md), wenn Hilfestellungen, alternative Lösungswege oder unklare Lehrplanbezüge verdeutlicht werden müssen. Sie dienen als Orientierung, nicht als starre Schablone für jede Unterrichtseinheit.

## Lernkontext erfassen

Verwende bereits vorliegende Informationen aus der Anfrage, dem Projekt und bereitgestellten Materialien. Frage bei Lücken nur nach Angaben, die das didaktische Design wesentlich beeinflussen. Bei geringfügigen Unsicherheiten formuliere eine nachvollziehbare Annahme und fahre fort. Vermeide starre Fragebögen oder wiederholte Freigabeschleifen für Standardentscheidungen, die durch den Auftrag bereits abgedeckt sind.

Erfasse den handlungsleitenden Kontext: Lernende und Vorwissen, Fachgebiet, angestrebte Kompetenzen, Einsatz im Unterricht oder Selbststudium, verfügbare Zeit und Endgeräte, Sprache, Barrierefreiheitsanforderungen und vorgegebene Lehrpläne. Berücksichtige Lehrpläne dort, wo sie für das Einsatzszenario relevant sind; setze kein einzelnes nationales Bildungssystem voraus. Wähle den Tonfall passend zum Kontext und den Wünschen des Autors. Schließe nicht aus pauschalen Generationenbegriffen auf Aufmerksamkeit, Motivation, Leistungsvermögen oder bevorzugte Lernstile.

Beziehe das unterrichtliche Umfeld ein, sofern nützlich: Vorbereitung, Einzel- oder Gruppenarbeit, Lehrkräfteintervention, Plenumsdiskussion und Nachbereitung. Eine lehrkraftzentrierte Demonstration benötigt oft nur einen durchdachten Diskussionsimpuls statt Benutzerkonten und individueller Punkteerfassung.

Trenne Alter, Bildungsrolle und thematische Vorerfahrung; Kind, Schüler, Studierender und erwachsener Teilnehmer sind weder austauschbare Bezeichnungen noch Leistungsstufen. Lies beim Festlegen oder Ändern der Zielgruppe das Lernendenprofil im [Entwurfsdialog](references/design-dialogue.md). Passe Begrifflichkeiten und Unterstützung an das Setting an; nutze in allgemeiner Dokumentation neutrale Begriffe. Entwickler, Lernende und begleitende Lehrkräfte oder Eltern können verschiedene Personen sein.

## Lernziele mit beobachtbaren Aktivitäten verknüpfen

Verknüpfe für jedes wesentliche Lernziel die Handlung des Lernenden, den Lernnachweis, die Erfolgskriterien, die Bedingungen für Hilfestellungen und die nächste didaktische Entscheidung. Halte dies bei kleinen Aufgaben kompakt. Bei forschend-entdeckendem Lernen kann der Nachweis in der Qualität der Fragestellung, der Nutzung von Belegen oder der Überarbeitung einer Erklärung bestehen; eine einzige vorbestimmte Musterantwort ist nicht zwingend.

Beispiel: Der Lernende stellt eine Hypothese auf, wie sich ein veränderter Widerstand auf die Stromstärke auswirkt, überprüft diese an einem Modell, erklärt Abweichungen und löst eigenständig eine Transferaufgabe. Das bloße Verschieben eines Schiebereglers oder Durchklicken von Bildschirmen belegt noch kein Verständnis.

Wähle die didaktische Intervention passend zum beobachteten Lernhindernis. Behandle Erklärungen für Fehler als vorläufige Hypothesen, nicht als gesicherte Diagnosen. Wähle ein kleines, in sich stimmiges Methodenset; überfrachte die Anwendung nicht mit didaktischen Bausteinen, nur weil sie im Katalog existieren. Konsultiere die [Methoden](references/methods.md), wenn eine Methode, Unterstützungssequenz oder Progressionsregel ausgewählt oder implementiert wird.

Lies [Lernspiele und zielgerichtete Gamification](references/learning-games.md) für Spielmechaniken, motivationale Elemente oder Reviews von Lernspielen. Die Referenz behandelt spielbare Lernschleifen, Mechanik-Auswahl, Grenzen der Nachweisbarkeit und Umsetzungen von Minispielen bis hin zu komplexen Lernanwendungen. Berücksichtige Vorwissen und lokalen Kontext für Primarstufe, Sekundarstufe, Hochschule und Erwachsenenbildung.

Die Methodenreferenz behandelt explizit Sokratischen Dialog, Feynman-Methode, Zone der nächsten Entwicklung und Scaffolding, ausgearbeitete Lösungsbeispiele (Worked Examples), aktiven Abruf und zeitlich versetztes Üben (Spaced Practice), Lernen aus Fehlern, Metakognition, forschendes Lernen, Rollenspiele, Peer- und kooperatives Lernen, Projektarbeit, Flipped Classroom und optionale Gamification. Dies sind wählbare Ansätze, keine Pflichtbestandteile jeder Anwendung.

Blooms Taxonomie beschreibt kognitive Zielstufen und Wissensarten. Trenne Schwierigkeitsgrad und Voraussetzungen sauber; erzwinge keine sechs sequentiell gesperrten Stufen. Wähle für praktische oder überfachliche Kompetenzen passende Nachweise und benenne klar, was eine softwarebasierte Aufgabe nicht erfassen kann.

## Eine realistische Umsetzung wählen

Unterscheide zwischen KI, die zur Erstellung der Anwendung dient, und KI, die während der Nutzung durch Lernende aufgerufen wird. Wähle zwischen geprüften statischen Inhalten, deterministischer Interaktionslogik oder Simulationen und Laufzeit-KI anhand von Lernziel und Betriebsrahmen. Hinweise, Feedback und zeitlich versetztes Wiederholen funktionieren hervorragend ohne externe KI-Dienste.

Prüfe vor dem Hinzufügen umfangreicher Funktionen deren didaktischen Mehrwert, Interaktionsaufwand, Betreuungsaufwand für Lehrkräfte, Wartung, Datenbedarf und Betriebskosten. Lege wesentliche Kompromisse offen dar. Ergänze Benutzerkonten, Analytik, Dashboards, Backend-Dienste, Bezahlfunktionen oder externe Datenflüsse nicht nur, um das Produkt vollständiger wirken zu lassen. Hole für weitreichende Architekturentscheidungen die Freigabe ein, sofern sie nicht vorab autorisiert wurden.

Konsultiere [Simulationen](references/simulations.md), wenn Systeme modelliert, Experimente durchgeführt oder Rollenspiele gestaltet werden. Trenne reale Beobachtungen, Modellberechnungen und fiktive Rekonstruktionen eindeutig. Gib erfundene KI-Ausgaben niemals als reale Messwerte aus und täusche kein reales Experiment vor.

Konsultiere [Laufzeit-KI](references/runtime-ai.md) nur dann, wenn das fertige Produkt externe KI-Dienste aufruft. Definiere die pädagogische Rolle, Quellengrenzen, menschliche Aufsicht, Datenflüsse, Kostenlimits und das Verhalten bei Systemausfällen. Ein System-Prompt ersetzt keine Anwendungssicherheit.

Konsultiere [Tutor-Modi und Kontinuität](references/tutor-state.md) bei mehrstufigen Tutoringsystemen, Übergängen zwischen Übungs- und Testmodus oder der Wiederaufnahme von Lernsitzungen. Verwalte Zustand und Lernnachweise direkt in der Anwendung; diese Funktionen erfordern keine Laufzeit-KI.

## Feedback und Entscheidungen verlässlich gestalten

Biete nach Fehlern einen konstruktiven nächsten Schritt an. Ermögliche in Übungsphasen Hilfestellungen und bei Bedarf den Weg zu einer direkten Erklärung oder einem Lösungsbeispiel; vermeide endlose Frageschleifen. Baue Hilfen mit zunehmender Selbstständigkeit ab (Fading), halte angeforderte Unterstützung jedoch zugänglich. Prüfungs- und Testmodi können Hilfen unter transparenten Bedingungen einschränken.

Unterscheide zwischen selbstständigem Erfolg, Erfolg mit Unterstützung, bloßem Betrachten der Lösung und Unsicherheit. Ein erratener Treffer, eine Zuversichtsbekundung oder zwei unterstützte Erfolge begründen noch keine gesicherte Beherrschung. Schließe aus einer kurzen Interaktion weder auf dauerhafte Begabungen noch auf mangelnde Motivation oder Lernstörungen.

Konsultiere die [Leistungsbeurteilung](references/assessment.md) beim Entwurf von bewerteten Aufgaben, Bewertungsrastern (Rubrics), Adaptivität oder Lernerfolgsmessungen. Prüfe fachliche Richtigkeit, plausible Alternativen, Maßeinheiten und Toleranzen sowie die Frage, ob die Aufgabe tatsächlich die Zielkompetenz abprüft. Erkenne fachlich gültige Alternativwege und Begründungen an. Trenne spielerische Belohnungen und Bearbeitungsgeschwindigkeit von fachlicher Leistung, es sei denn, Tempo ist ein explizites Lernziel.

## Zugänglichkeit und Handlungsfähigkeit der Lehrkraft wahren

Orientiere dich an den für die Aktivität und die Lernendenbedürfnisse relevanten WCAG 2.2 AA-Kriterien. Überprüfe Tastaturbedienbarkeit, sichtbaren Fokus, verständliche Beschriftungen und Rückmeldungen, Alternativen zu reiner Farb- oder Tonkodierung sowie begründete oder anpassbare Zeitlimits. Ermögliche flexible Zugangs- und Ausdrucksweisen gemäß UDL; weise Lernenden keine starren Lerntypen zu. Ziehe bei komplexen Anforderungen Fachleute für Barrierefreiheit hinzu.

Erhebe nur Daten, die für die Durchführung der Lernaktivität zwingend erforderlich sind. Dokumentiere, wer Zugriff hat, wohin Daten übertragen und wie lange sie gespeichert werden. Beachte rechtliche Vorgaben von Schule, Träger und Region; stelle keine unbegründeten universellen Rechtsbehauptungen auf. Eine lokale, anonyme Unterrichtsaktivität benötigt weder Benutzerregistrierung noch dauerhaftes Tracking.

Gib Lehrkräften oder Autoren einfache Möglichkeiten an die Hand, Inhalte zu prüfen, automatisierte Bewertungen zu korrigieren und in unpassende Adaptionen einzugreifen. Eine editierbare Inhaltsdatei genügt oft; ein komplexes Verwaltungssystem ist selten nötig. Weitreichende Beurteilungs- oder Einstufungsentscheidungen erfordern stets eine verantwortliche menschliche Überprüfung.

## Fachkompetenzen koordinieren, ohne den Arbeitsablauf aufzublähen

Binde folgende Perspektiven nach Bedarf ein; bei kleineren Aufgaben kann ein einzelner Agent diese Rollen vereinen:

- Fachdidaktiker / Methodiker: Angestrebte Kompetenzen, Unterrichtskontext und didaktische Methodenwahl.
- Fachwissenschaftler / Fachlehrer: Inhaltliche Korrektheit, Voraussetzungen, didaktische Beispiele und typische Fehlvorstellungen.
- Test- und Bewertungsdesigner: Lernnachweise, Kriterienraster, alternative Lösungswege und Grenzen der Diagnostik.
- Interaktionsdesigner: Lernendenführung, Hilfesystem, Barrierefreiheit und Praxistauglichkeit im Unterricht.
- Softwareentwickler: Datenmodelle, Berechnungen, Zustandsverwaltung, Persistenz und Fehlerbehandlung.
- Reviewer / Prüfer: Diskrepanzen zwischen Lernziel, Entwurf und tatsächlichem Anwendungsverhalten.

Übertrage diese Perspektiven verbindlich in die Implementierung. Deklariere eine bequeme technische Lösung niemals ohne didaktische Belege als pädagogisch wertvoll. Kläre fachliche Uneinigkeiten durch Quellenabgleich, gezielte Tests oder eine offene Frage an den Auftraggeber. Setze unabhängige Reviews ein, wenn Komplexität oder Tragweite es erfordern; bilde nicht für jede Routineaufgabe ein großes Team. Binde andere Skills nur für relevante Arbeitsschritte und bei tatsächlicher Verfügbarkeit ein.

## Auf angemessener Ebene überprüfen und berichten

Überprüfe bei Implementierungen den betroffenen Lernpfad, typische reale Lernendenfehler, das Hilfesystem und kritische Fehlerzustände. Berichte bei reinen Analyseaufträgen über Befunde und Vorschläge, ohne das Produkt unaufgefordert zu verändern. Passe Prüfungen an die Anwendung an: Eine Simulation benötigt mathematisch-fachliche Modellprüfungen; Laufzeit-KI benötigt Tests für Verbindungsausfälle und unpassende Modellantworten; einfache statische Aktivitäten benötigen beides standardmäßig nicht.

Halte drei Bewertungen strikt auseinander: funktionale Korrektheit, didaktische Eignung und tatsächlich beobachteter Lernerfolg. Reine Funktionstests beweisen keine didaktische Wirksamkeit. Ein kleiner Unterrichtstest kann Schwachstellen aufdecken, belegt jedoch keine kausale Leistungssteigerung. Berichte reale Testergebnisse und offene Annahmen; erfinde keine Nutzerbeobachtungen oder Wirksamkeitsnachweise.

Fasse bei der Übergabe Lernziel, gewählten Ansatz, wichtige Betriebsannahmen, tatsächlich durchgeführte Tests und verbleibende Grenzen prägnant zusammen. Ergänze eine Tabelle zur Verknüpfung von Zielen und Nachweisen nur dann, wenn sie den praktischen Nutzen erhöht. Stimme das Format auf die Vorgaben des Nutzers ab.

## An Lernende gerichtete Texte ohne KI-Floskeln verfassen

Die Texte der Anwendung tragen den didaktischen Prozess. Wende denselben Maßstab auf Prompts, Arbeitsanweisungen, Feedback und Erklärungen an:

- Streiche inhaltsleere Adjektive („modern“, „ansprechend“, „interaktiv“), es sei denn, der folgende Satz belegt die Eigenschaft konkret.
- Formuliere Aussagen direkt; vermeide Phrasen wie „es ist nicht nur X, sondern auch Y“ oder „dies ist kein X, sondern Y“.
- Verzichte auf formelhafte Ankündigungen wie „In dieser Lerneinheit lernst du...“; benenne direkt die Handlung des Lernenden.
- Feedback benennt präzise, was korrekt ist, was fehlt und welcher konkrete nächste Schritt folgt.
- Halte Zahlen, Einheiten und Bedingungen exakt; kein „verbessert deutlich“ ohne messbare Bezugsgröße.
- Keine Emojis in Schaltflächen, Überschriften oder UI-Beschriftungen. Verwende Text und ein konsistentes Icon-Set.
- Stimme den Wortschatz auf die Zielgruppe ab und verwende einheitliche Fachbegriffe für dieselbe Sache.

Lies Texte aus der Perspektive der Lernenden. Könnte ein Satz wortgleich in einem beliebigen anderen Produkt stehen, streiche ihn oder formuliere ihn fachspezifisch aus.

## Integration

Konsultiere bei der Auswahl von Modell, Denkaufwand (Reasoning Effort) oder Arbeitsgeschwindigkeit sowie bei der Anpassung des Lademechanismus die [Modell- und Host-Profile](references/model-profiles.md). Sie enthalten dokumentierte Leitfäden für OpenAI, Claude und Gemini. Halte an einem einheitlichen didaktischen Kern fest und trenne reale Testergebnisse von theoretischer Kompatibilität. Lade dieses Profil nicht für Standardaufgaben, die es nicht erfordern.

Geeignet für Lernspiele, Quizze, Tutorials, Simulationen, Trainingsanwendungen und Reviews didaktischer Entwürfe. Der Kern benötigt weder externe Pakete, APIs noch spezifische KI-Modelle oder schülerbezogene Daten. Die Referenzen werden nach Bedarf geladen. Das native Paket besteht aus dieser Datei und ihren Referenzen; `lernmethoden.md` ist die generierte eigenständige Ausgabe. Installation, Deployment und andere externe Dateiänderungen erfordern eine entsprechende Autorisierung. Dieser Skill ersetzt keine projektspezifischen Anweisungen und autorisiert keine eigenmächtige Erweiterung des Projektumfangs.

Gestaltungsreferenzen: [WCAG 2.2](https://www.w3.org/TR/WCAG22/), [CAST UDL-Richtlinien](https://udlguidelines.cast.org/). Diese dienen als Orientierung für Entwurf und Begutachtung; ihre Erwähnung stellt keine Zertifizierung von Konformität oder Bildungswirksamkeit dar.
