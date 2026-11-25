---
name: self-learning-reinforcement
description: >-
  Fuehrt eine Aufgabe nach dem Self-Learning-Reinforcement-Verfahren in neun
  Phasen aus: Wissenskontext laden, Auftrag analysieren und optimieren, Fakten
  mit Quellenpflicht und Vertrauensstufen verifizieren, Plan mit Checkpoints,
  Skill-Luecken schliessen, ausfuehren und jede Teilaufgabe verifizieren,
  adversariale Selbstbewertung, Skills und Lessons Learned zurueckschreiben,
  Abschlussbericht. Anwenden bei Aufgaben, deren Ergebnis belegbar korrekt sein
  muss und deren Erkenntnisse wiederverwendbar bleiben sollen - besonders bei
  Anwendungsentwicklung, Architekturentscheidungen und Recherchen. Trigger:
  "nach dem Verfahren arbeiten", "Self-Learning-Reinforcement", "SLR",
  "Faktenregister anlegen", "Lessons Learned schreiben", "mit Selbstbewertung",
  "Skill verbessern", "adversarialer Review", /self-learning-reinforcement.
---

# Self-Learning-Reinforcement (Neun-Phasen-Verfahren)

## Zweck

Aufgaben so bearbeiten, dass drei Dinge gleichzeitig entstehen: ein belegtes
Ergebnis, ein pruefbarer Beweisweg und ein dauerhafter Kompetenz-Zuwachs des
Systems. Jede Aufgabe hinterlaesst verifizierte Fakten, verbesserte Skills und
dokumentierte Erkenntnisse.

Ausfuehrliche Bewertungsmassstaebe: [BEWERTUNG.md](BEWERTUNG.md).
Qualitaetsstandards fuer Anwendungsentwicklung:
[QUALITAETSSTANDARDS.md](QUALITAETSSTANDARDS.md).

## Vorgehen

Keine Phase darf uebersprungen werden. Kopiere zu Beginn diese Checkliste in
die Antwort und hake sie im Verlauf ab:

```
- [ ] Phase 0: Wissenskontext geladen
- [ ] Phase 1: Auftrag analysiert, Aufgabe optimiert, Arbeitsmodus gewaehlt
- [ ] Phase 2: Wissen gesammelt, Fakten verifiziert, Register angelegt
- [ ] Phase 3: Vorgehensplan mit Checkpoints erstellt
- [ ] Phase 4: Skill-Gaps geschlossen, Skills verankert
- [ ] Phase 5: Ausgefuehrt und jede Teilaufgabe verifiziert
- [ ] Phase 6: Selbstbewertung an allen Checkpoints
- [ ] Phase 7: Skills optimiert, Learnings geschrieben, Memory aktualisiert
- [ ] Phase 8: Abschlussbericht geliefert
```

### Phase 0 — Wissenskontext laden

1. `.claude/skills/` auf vorhandene Skills pruefen, deren SKILL.md lesen.
2. `.claude/learnings/` auf Lessons Learned und `.claude/research/` auf
   bestehende Faktenregister pruefen.
3. `CLAUDE.md` auf Regeln, Konventionen und Erfahrungswerte lesen.
4. Kurz zusammenfassen: Welches vorhandene Wissen ist wiederverwendbar,
   welches fehlt?

### Phase 1 — Auftragsanalyse und Aufgaben-Optimierung

1. **Ziel**: messbares Endergebnis und explizite Abnahmekriterien. Bei
   Anwendungsentwicklung gelten zusaetzlich die Domaenen-Standards aus
   [QUALITAETSSTANDARDS.md](QUALITAETSSTANDARDS.md) als Abnahmekriterien fuer
   alle beruehrten Dimensionen.
2. **Teilaufgaben**: nummeriert, einzeln pruefbar, mit Abhaengigkeiten.
3. **Rahmenbedingungen**: Stack, bestehende Codebasis, Projektkonventionen,
   Einschraenkungen (Kompatibilitaet, Performance, Sicherheit).
4. **Risiken und Unklarheiten**: auflisten. Bei Mehrdeutigkeit begruendete
   Annahme treffen und dokumentieren — nachfragen nur, wenn eine falsche
   Annahme irreversiblen Schaden anrichten wuerde.
5. **Aufgaben-Optimierung**: Original-Formulierung kritisch pruefen (praezise?
   vollstaendig? messbar? widerspruchsfrei?). Optimierte Fassung formulieren,
   die die Absicht exakt bewahrt und Luecken schliesst; Original und optimierte
   Fassung gegenueberstellen; ab dann mit der optimierten Fassung arbeiten.
   Aendert die Optimierung Absicht oder Umfang, vorher bestaetigen lassen.
   Verbesserungsmuster notieren (fliesst in Phase 7 ein).
6. **Arbeitsmodus waehlen**:
   - **Vollmodus** (Standard): alle neun Phasen mit vollem Faktenregister — bei
     neuen Features, Architekturaenderungen, externen Abhaengigkeiten, allem
     Irreversiblen.
   - **Kompaktmodus**: fuer kleine, risikoarme Aufgaben (Tippfehler,
     Umbenennung, Doku-Korrektur). Phasen 2-4 duerfen auf wenige Saetze
     verdichtet und das Register durch Inline-Quellenangaben ersetzt werden.
     NIEMALS entfallen: Verifikationsregeln (Phase 2c), Verifikation jeder
     Aenderung (Phase 5), Kurz-Selbstbewertung (Phase 6). Im Zweifel Vollmodus.
7. **Erfolgsmetriken** je Teilaufgabe festlegen: Effektivitaet, Effizienz,
   Zielgenauigkeit, Faktenqualitaet — und aufgabenweit der Kompetenz-Zuwachs
   (KWI).

### Phase 2 — Wissenssammlung und Faktenverifikation

**2a. Sammlung**

1. **Projektwissen**: relevante Stellen der eigenen Codebasis lesen
   (Primaerquelle erster Ordnung).
2. **GitHub-Recherche**: offizieller Quellcode, README, Release Notes,
   Changelogs, Issues zum konkreten Problem. Repository, Datei/Issue-Nummer und
   Commit/Version notieren.
3. **Offizielle Dokumentation** der tatsaechlich eingesetzten Version.
4. **Ergaenzende Quellen** (nachrangig): Blogs, Foren, Tutorials — nur als
   Hinweisgeber, nie als alleiniger Beleg.
5. **Quellen-Fallback-Kaskade** bei nicht erreichbarer Quelle: (a) alternative
   offizielle Domain oder Spiegel, (b) Websuche zur Quellenfindung, (c) eigene
   praktische Verifikation (ausfuehren, testen, Quellcode lesen), (d) sonst als
   "NICHT VERIFIZIERT — Quelle blockiert" ins Register. Blockierte Quellen und
   funktionierende Ausweichwege gehoeren als Umgebungswissen in die Lessons
   Learned.

**2b. Kuratierte Referenzquellen und Verstehens-Pflicht**

Staendig zu evaluieren: offizielle Anthropic-Dokumentation und -Repositories
(github.com/anthropics), Repositories und Lehrmaterialien von Andrej Karpathy
(github.com/karpathy), zusaetzlich vom Auftraggeber benannte Quellen.

Vertrauen in die Herkunft ersetzt nicht die Pruefung der Uebertragbarkeit.
Jede Information durchlaeuft vor der Aufnahme:

1. **Erklaeren**: Zweck, Funktionsweise, Annahmen, Grenzen in eigenen Worten.
   Was nicht erklaert werden kann, wird nicht uebernommen.
2. **Pruefen**: praktisch verifizieren — ausfuehren, testen, minimal nachbauen;
   mindestens den Quellcode vollstaendig lesen statt nur die Beschreibung.
3. **Kontext-Check**: Version, Aktualitaet, Lizenz, Passung zum Projekt.
   Beispiel-Code aus Lehrmaterial ist Lernvorlage, nicht Produktionscode.
4. **Registrieren**: erst nach 1-3, mit Verifikationsweg "verstanden + geprueft"
   und Fundstelle.

**2c. Verifikationsregeln (absolut verbindlich)**

1. **Quellenpflicht**: jeder Fakt braucht benannte Quelle (URL,
   Repository+Commit, Datei+Zeile, Doku-Abschnitt) und Abrufdatum. Ein Fakt
   ohne Quelle existiert nicht.
2. **Vertrauensstufen**:
   - **A** (direkt verwendbar): eigener Quellcode, offizieller Quellcode,
     offizielle Doku der korrekten Version, selbst ausgefuehrte Tests.
   - **B** (nach Zweitbeleg): Release Notes, maintainer-bestaetigte Issues,
     Standards-Dokumente.
   - **C** (nie allein): Blogs, Foren, Q&A, KI-generierte Inhalte, eigenes
     unbelegtes Vorwissen.
3. **Zwei-Quellen-Regel**: jeder entscheidungsrelevante Fakt unterhalb Stufe A
   braucht zwei unabhaengige Belege oder eine eigene praktische Verifikation.
   Eigene Verifikation schlaegt jede Sekundaerquelle — auch die
   Herstellerdokumentation, wenn diese sich widerspricht.
4. **Aktualitaetspruefung**: Version und Datum jedes Fakts pruefen. Ein Fakt zu
   einer anderen Version gilt als unverifiziert, bis die Uebertragbarkeit
   belegt ist.
5. **Keine Fake-Fakten**: niemals Quellen, Versionsnummern, APIs oder Messwerte
   erfinden. Nicht Belegbares als "NICHT VERIFIZIERT — Wissensluecke"
   kennzeichnen und als offenes Risiko behandeln.
6. **Kennzeichnungspflicht**: unverifizierte Annahmen nur weiterverwenden, wenn
   sie (a) als Annahme markiert, (b) im Risiko benannt sind und (c) keine
   irreversible Entscheidung auf ihnen beruht. Fuer kritische Entscheidungen
   sind nur ✅-Fakten zulaessig. **Kritisch** = irreversibel (Loeschen,
   Ueberschreiben, Veroeffentlichen), sicherheits- oder
   datenschutzrelevant, architekturpraegend oder mit Aussenwirkung. Ist ein
   kritischer Fakt trotz Fallback-Kaskade nicht verifizierbar, wird die
   Entscheidung nicht geraten, sondern dem Auftraggeber vorgelegt.

**2d. Faktenregister anlegen**

`.claude/research/YYYY-MM-DD-<aufgabe-kurzname>.md` mit einer Zeile pro Fakt:

```markdown
| # | Fakt/Information | Quelle(n) | Stufe | Abrufdatum | Status | Verifiziert durch |
|---|------------------|-----------|-------|------------|--------|-------------------|
|   |                  |           | A/B/C |            | ✅ verifiziert / ⚠️ Annahme / ❌ verworfen | Zweitquelle / eigener Test / Quellcode |
```

Verworfene Informationen bleiben mit Status ❌ und Grund im Register stehen —
auch das ist Lernmaterial. In Folgephasen darf nur auf ✅ aufgebaut werden;
⚠️ nur unter den Bedingungen aus Regel 6.

### Phase 3 — Vorgehensplan

1. Reihenfolge der Teilaufgaben mit Begruendung.
2. Je Teilaufgabe: Vorgehen, Werkzeuge, verwendete Fakten (Register-Nummern),
   erwartetes Ergebnis, Verifikationsschritt (Test, Ausfuehrung, Review).
3. Checkpoints festlegen — mindestens nach jeder Teilaufgabe und vor Abschluss.
4. **Kalibrierungs-Vorhersage**: VOR der Ausfuehrung die erwarteten Noten je
   Kriterium und die zwei groessten Risiken notieren. Abgleich in Phase 7.

### Phase 4 — Skill-Gap-Analyse und Skill-Entwicklung

1. **Gap-Analyse**: Anforderungen gegen die Skills aus Phase 0. Was ist
   einsetzbar, was muss erweitert werden, was fehlt?
2. **Skill-Entwicklung**: fuer jede fehlende Faehigkeit
   `.claude/skills/<skill-name>/SKILL.md` anlegen mit den Abschnitten: Zweck,
   Vorgehen, Faktenbasis (Verweis auf Register-Eintraege), Pruefkriterien,
   Bekannte Fallstricke, Versionshistorie.
3. **Memory-Verankerung**: jeden neuen oder geaenderten Skill in `CLAUDE.md`
   unter "## Erlernte Skills" eintragen (Name, Zweck, Pfad, Version).
4. Skills duerfen nur auf ✅-Fakten aufbauen; generisch genug fuer
   Wiederverwendung, konkret genug zum Ausfuehren ohne Rueckfragen.

**Verbindliche Formatregeln** (Quelle: offizielle Agent-Skills-Doku):

- `name`: max. 64 Zeichen, nur Kleinbuchstaben, Zahlen, Bindestriche; keine
  XML-Tags; nicht die reservierten Woerter "anthropic"/"claude"; identisch zum
  Ordnernamen. Gerundium oder praezise Nominalphrase, keine vagen Namen
  (helper, utils).
- `description`: nicht leer, max. 1.024 Zeichen, keine XML-Tags, **dritte
  Person**, enthaelt WAS der Skill tut UND WANN er anzuwenden ist, inklusive
  konkreter Trigger-Begriffe.
- SKILL.md-Body unter 500 Zeilen. Waechst der Inhalt darueber: Details in
  Referenzdateien im Skill-Ordner auslagern, die direkt (nur eine Ebene tief)
  aus SKILL.md verlinkt werden. Referenzdateien ueber 100 Zeilen beginnen mit
  einem Inhaltsverzeichnis.
- Pfadangaben immer mit Forward-Slash, auch unter Windows.
- MCP-Tools voll qualifiziert benennen (`ServerName:tool_name`).
- Keine zeitgebundenen Angaben im Hauptteil; Veraltetes in einen klar
  markierten Altbestand-Abschnitt.

Diese Regeln nicht per Sichtpruefung abhaken, sondern pruefen lassen —
`scripts/Test-SkillFormat.ps1` verifiziert sie maschinell und meldet jeden
Verstoss mit Datei und Fundstelle. Ausfuehren nach jeder Skill-Aenderung, bis
der Lauf ohne Befund durchlaeuft (Exit-Code 0):

```powershell
# einzelner Skill
./scripts/Test-SkillFormat.ps1 -Path ../<skill-name>
# alle Skills eines Repos
./scripts/Test-SkillFormat.ps1 -Path ../../skills
```

### Phase 5 — Ausfuehrung

1. Plan aus Phase 3 Teilaufgabe fuer Teilaufgabe abarbeiten.
2. Bei jedem Schritt vermerken, welcher Skill und welche Fakten
   (Register-Nummern) zum Einsatz kamen.
3. Jede Teilaufgabe sofort nach Abschluss verifizieren (Test ausfuehren, Code
   starten, Ergebnis pruefen) — niemals ungeprueft weiterarbeiten.
4. Erweist sich ein Fakt als falsch: Status im Register auf ❌ (mit Grund), alle
   darauf aufbauenden Entscheidungen pruefen und korrigieren, dann erst weiter.
5. Erweist sich ein Skill als lueckenhaft: unterbrechen, Skill sofort
   korrigieren, Version erhoehen, mit der korrigierten Fassung weiterarbeiten.

### Phase 6 — Selbstueberpruefung und Bewertung

Vollstaendige Massstaebe: [BEWERTUNG.md](BEWERTUNG.md). Kurzfassung:

Jede Note ist eine Tatsachenbehauptung und unterliegt denselben
Verifikationsregeln wie jeder andere Fakt — sie stuetzt sich auf zaehlbare
Messgroessen, nicht auf Eindruecke.

**Adversarialer Selbst-Review (Pflicht vor jeder Benotung):** Das eigene
Ergebnis angreifen statt verteidigen — mindestens drei Einwaende eines strengen
externen Pruefers formulieren (je einer zu Korrektheit, Vollstaendigkeit,
verdeckten Annahmen). Jeden Einwand mit Beleg entkraeften oder als
dokumentierte Schwaeche in die Bewertung uebernehmen. Erst danach benoten.

**Notenskala** (Beweislast beim Praedikat): 1 = Abnahmekriterien verfehlt oder
unverifiziert; 2 = teilweise erreicht, wesentliche Nacharbeit; 3 =
professioneller Standard (funktioniert, verifiziert, dokumentiert) — der
Erwartungswert; 4 = zusaetzlich Enterprise-Checkliste erfuellt; 5 = es ist
konkret benannt, WELCHER anerkannte Massstab WORIN messbar uebertroffen wurde,
mit Beleg.

| Kriterium | Messgroessen | Note 1-5 |
|-----------|--------------|----------|
| Effektivitaet | erfuellte/definierte Abnahmekriterien (x/y), jeweils verifiziert | |
| Effizienz | Anlaeufe und Umwege; Rework-Quote nach "fertig" | |
| Zielgenauigkeit | Nachbesserungen nach Auftraggeber-Feedback; unbegruendete Abweichungen | |
| Faktenqualitaet | Anteil Stufe-A-Belege; jeder widerlegte ✅-Fakt ⇒ Note ≤ 2 plus Ursachenanalyse | |
| Kompetenz-Zuwachs (KWI) | neue/verbesserte Skills; Zuwachs wiederverwendbarer Fakten; Wiederverwendungsquote | |

Bei Note ≤ 3 in einem Kriterium: Ursache analysieren (Plan? Recherche? Skill?
Ausfuehrung?), konkrete Korrektur ableiten und umsetzen, bevor es weitergeht.

### Phase 7 — Skill- und Verfahrens-Optimierung

Nach Abschluss — und sofort, wenn Phase 6 eine Schwaeche aufdeckt:

1. **Retrospektive**: jede Bewertung durchgehen. Was lief gut, was nicht, warum?
2. **Kalibrierungs-Abgleich**: Vorhersage aus Phase 3 gegen tatsaechliche Noten.
   Systematische Ueber- oder Unterschaetzung ist ein Kalibrierungsfehler erster
   Ordnung — mit Gegenmassnahme ausweisen. Externe Signale (Korrekturen des
   Auftraggebers, fehlgeschlagene Tests, spaetere Review-Befunde) korrigieren
   vergebene Noten rueckwirkend im Learning-Dokument.
3. **Laengsschnitt-Review**: nach je fuenf Aufgaben (oder auf Anforderung) alle
   Learning-Dateien auswerten: Notentrends, KWI-Verlauf, wiederkehrende
   Schwaechen. Tritt dieselbe Schwaeche zum zweiten Mal auf, genuegt kein
   Skill-Patch — dann wird das Verfahren selbst geaendert (Versionssprung mit
   Begruendung).
4. **Skill-Ueberarbeitung**: neue Fallstricke ergaenzen, Umweg-verursachende
   Schritte praezisieren, falsche Anweisungen entfernen, Faktenbasis
   aktualisieren, Version erhoehen und Aenderung begruenden.
5. **Recherche-Lernen**: Register auswerten — welche Quellen waren zuverlaessig,
   welche falsch oder veraltet? In den Lessons Learned festhalten.
6. **Aufgabenformulierungs-Lernen**: Verbesserungsmuster aus Phase 1.5
   dokumentieren und konkret vorschlagen, wie kuenftige Auftraege dieser Art
   formuliert werden sollten.
7. **Lessons Learned**: `.claude/learnings/YYYY-MM-DD-<aufgabe-kurzname>.md` mit
   Aufgabe (Original + optimiert), eingesetzten Skills, Faktenregister-Bilanz,
   Selbstbewertungen, Skill-Optimierungen und uebertragbaren Erkenntnissen.
8. **Memory-Update**: in `CLAUDE.md` die Abschnitte "## Erlernte Skills" (neue
   Versionen) und "## Lessons Learned" (Verweis plus wichtigste Erkenntnis als
   Merksatz) aktualisieren.

### Phase 8 — Abschlussbericht

1. **Ergebnis** gemessen an den Abnahmekriterien aus Phase 1; was bewusst nicht
   umgesetzt wurde und warum.
2. **Verifikation**: welche Tests und Pruefungen mit welchem Resultat.
3. **Faktenbilanz**: gesammelt / verifiziert / verworfen; Entscheidungen auf
   ⚠️-Basis und die daraus verbleibenden Restrisiken.
4. **Gesamtbewertung**: Durchschnittsnoten aller fuenf Kriterien ueber alle
   Checkpoints, mit Kalibrierungs-Ergebnis.
5. **Skill-Bilanz**: neu erstellt, ueberarbeitet (mit Versionssprung), kuenftig
   wiederverwendbar wofuer.
6. **Empfehlung zur Aufgabenstellung**: optimierte Formulierung und konkreter
   Vorschlag fuer kuenftige Auftraege dieser Art.

## Ablagestruktur im Projektordner

```text
.claude/
├── skills/<skill-name>/SKILL.md   # ein Skill je Ordner, versioniert
├── research/YYYY-MM-DD-<name>.md  # Faktenregister je Aufgabe
└── learnings/YYYY-MM-DD-<name>.md # Lessons Learned je Aufgabe
CLAUDE.md                          # Skills-Index + Lessons Learned
```

## Grundprinzipien

- Skills sind Werkzeuge, keine Dokumentation: ausfuehrbare
  Handlungsanweisungen, nicht Beschreibungen.
- Kein Fakt ohne Quelle, keine Entscheidung ohne verifizierten Fakt. Eine
  dokumentierte Wissensluecke ist besser als eine plausible Erfindung.
- Jede Aufgabe macht das System besser: Es ist ein Fehler, eine Aufgabe
  abzuschliessen, ohne mindestens einen Skill erstellt oder verbessert zu
  haben — es sei denn, alle eingesetzten Skills haben nachweislich ohne
  Korrekturbedarf funktioniert (dann genuegt der KWI-Nachweis ueber
  Registerzuwachs oder dokumentiertes Umgebungswissen).
- Auch die Aufgabenstellung ist Lernmaterial: jede Aufgabe endet mit einem
  Vorschlag, wie sie besser haette formuliert werden koennen.
- Ehrlichkeit vor Eleganz: Fehlschlaege, Umwege und verworfene Fakten werden
  dokumentiert, nicht kaschiert.
- Verhaeltnismaessigkeit: Die Tiefe folgt Risiko und Umfang (Voll- vs.
  Kompaktmodus) — die Verifikationsregeln selbst sind nie verhandelbar.

## Pruefkriterien

Das Verfahren wurde korrekt angewendet, wenn:

- die Fortschritts-Checkliste in der Antwort steht und abgehakt ist;
- ein Faktenregister unter `.claude/research/` existiert, in dem jeder Fakt
  Quelle, Stufe, Abrufdatum und Status traegt;
- jede Teilaufgabe eine benannte, tatsaechlich ausgefuehrte Verifikation hat;
- die Selbstbewertung zaehlbare Messgroessen nennt und der adversariale Review
  mit mindestens drei Einwaenden dokumentiert ist;
- eine Learning-Datei unter `.claude/learnings/` existiert und `CLAUDE.md`
  aktualisiert wurde;
- mindestens ein Skill erstellt oder verbessert wurde — oder begruendet ist,
  warum nicht.

## Bekannte Fallstricke

- **Checkbox-Compliance**: Phasen formal abhaken ohne Substanz. Erkennbar an
  Bewertungen ohne zaehlbare Messgroessen.
- **Herstellerdoku blind vertrauen**: Offizielle Dokumentation kann sich selbst
  widersprechen. Bei Widerspruch entscheidet die eigene Messung (Regel 2c.3),
  und der Widerspruch gehoert ins Register.
- **Vollmodus fuer Trivialaufgaben**: erzeugt Reibung ohne Erkenntnisgewinn.
  Modus in Phase 1.6 bewusst waehlen und begruenden.
- **Goodhart-Effekt**: einen Trivial-Skill anlegen, nur um den KWI zu erfuellen.
  Zaehlt als Zielgenauigkeits-Mangel.
- **Beweislast-Umkehr**: "Es gab keine Hinweise auf Fehler" ist kein Beleg.
  Belegt ist nur, was geprueft wurde.
- **Superlative ohne Messwert** ("perfekt", "weltklasse") kosten einen
  Notenpunkt im betroffenen Kriterium.
- **Register nur anlegen, nicht pflegen**: Ein waehrend der Ausfuehrung
  widerlegter Fakt muss auf ❌ gesetzt werden, sonst wird das Register selbst
  zur Fehlerquelle.
- **Zwei Fassungen eines Skills**: Wird ein Skill aus einem Repo nach
  `~/.claude/skills/` kopiert, existiert er doppelt. Jede spaetere Aenderung
  zuerst im Repo vornehmen, dann die Kopie erneuern und per Hash-Vergleich
  bestaetigen — sonst arbeitet die Session mit einem veralteten Stand,
  waehrend das Repo bereits korrigiert ist.

## Versionshistorie

- v2.5.1 (2026-07-31): Fallstrick "Zwei Fassungen eines Skills" ergaenzt —
  entdeckt bei der ersten Selbstanwendung, als die installierte Kopie nach einer
  Repo-Korrektur veraltet war.
- v2.5 (2026-07-31): Als Skill im Repo verankert. Inhaltlich identisch zum
  Master-Prompt v2.5 vom 2026-07-16; Anhang A nach
  [BEWERTUNG.md](BEWERTUNG.md), Anhang B nach
  [QUALITAETSSTANDARDS.md](QUALITAETSSTANDARDS.md) ausgelagert, um die
  500-Zeilen-Grenze fuer SKILL.md einzuhalten. Formatregeln in Phase 4 gegen
  die offizielle Agent-Skills-Doku verifiziert und um Forward-Slash-Regel sowie
  MCP-Namenskonvention ergaenzt. Faktenregister:
  `.claude/research/2026-07-31-slr-skill-installation.md`.
- v2.0 bis v2.4 (2026-07-16): Entwicklung als Master-Prompt vor der
  Skill-Verankerung — Faktenverifikation mit Vertrauensstufen und
  Faktenregister (v2.0), Fortschritts-Checkliste, Arbeitsmodi und
  Quellen-Fallback-Kaskade (v2.1), Enterprise-Selbstbewertung mit adversarialem
  Review und KWI (v2.2), Konsistenz-Release (v2.3), vollstaendige Autarkie der
  Bewertungsmassstaebe (v2.4).
- v1.0 (2026-07-16): Erstversion mit Sieben-Phasen-Verfahren.
