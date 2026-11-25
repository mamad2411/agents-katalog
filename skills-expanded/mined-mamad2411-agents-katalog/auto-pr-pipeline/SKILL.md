---
name: auto-pr-pipeline
description: |
  Fuehrt einen repo- und policy-bewussten Delivery-Workflow fuer bestehende Code-Aenderungen aus: Zustand erfassen, passende lokale Checks auswaehlen, selektiv committen, pushen, Draft-PR oder Ready-PR erstellen/aktualisieren, CI und Reviews verarbeiten, Auto-Merge oder Merge Queue nutzen und nur bei echten Hochrisiko-Blockern anhalten.

  Aktivieren bei:
  - /auto-pr
  - /ship-it
  - /pr-pipeline
  - "mach einen PR"
  - "push und merge"
  - "bring das auf main"
  - "mach das fertig"
  - "arbeite die review kommentare ein und mach fertig"
  - "aktualisiere den bestehenden PR"
  - "aktiviere auto-merge"
  - "stell den PR in die merge queue"
  - Wenn Code bereits geaendert ist und der Rest des Wegs bis zum Merge professionell abgearbeitet werden soll
  - Wenn bestehende Commits, offener PR oder halb fertiger Zustand intelligent fortgesetzt statt stumpf neu begonnen werden sollen

  Arbeitsstil:
  - state-driven statt starrer Phasen
  - repo-native Checks statt generischer Befehle
  - pragmatische Commit-Strategie statt Dogmatismus
  - Auto-Merge oder Merge Queue wenn moeglich
  - stoppt nur bei schwerwiegenden Problemen und liefert dann Optionen
triggers:
  - /auto-pr
  - /ship-it
  - /pr-pipeline
  - PR erstellen
  - commit und push
  - mach einen PR
  - merge meinen Branch
  - auto-PR
  - ship it
  - alles durchlaufen lassen
  - PR bis zum Merge
  - vollstaendiger PR-Workflow
  - push und merge
  - von commit bis merge
  - teste und merge das
  - mach das fertig
  - bring das auf main
  - schick das raus
  - review kommentare einarbeiten
  - bestehenden PR aktualisieren
  - auto-merge aktivieren
  - merge queue
---

# Auto-PR-Pipeline v3.0

Arbeite nicht wie ein starres Script. Arbeite wie ein senioriger Delivery-Agent, der zuerst den Zustand, dann die Repo-Policy und erst danach die naechste Aktion bestimmt.

## Mission

Bringe vorhandene Code-Aenderungen sicher und professionell bis zu einem guten Endzustand:

- sauber validiert
- passend committet
- korrekt gepusht
- als Draft-PR oder Ready-PR sauber dokumentiert
- gegen CI, Reviews und Branch-Regeln abgearbeitet
- gemerged oder sauber bewaffnet fuer Auto-Merge / Merge Queue

Wenn der sicherste Endzustand nicht "sofort mergen" ist, ist ein sauber vorbereiteter Draft-PR oder ein armed Auto-Merge ein guter Abschluss.

## Kernprinzipien

1. **Repo-Policy zuerst.** Lies Branch-Regeln, Merge-Optionen, Review-Anforderungen, CI, CODEOWNERS, PR-Templates und vorhandene Workflows bevor du ueber Commit, Push oder Merge entscheidest.
2. **State-driven arbeiten.** Entscheide nicht anhand einer festen Phase, sondern anhand des aktuellen Repo-Zustands.
3. **Kleine Batches bevorzugen.** Wenn die Aenderung zu gross oder gemischt ist, splitte oder stoppe frueh statt unklar weiterzumergen.
4. **Repo-native Checks bevorzugen.** Rate keine Standardbefehle blind. Nutze die Checks, die dieses Repo wirklich verwendet.
5. **Veroeffentlichte History respektieren.** Bereits gepushte oder reviewte Commits werden nicht leichtfertig umgeschrieben.
6. **Plattform-Automation nutzen.** Auto-Merge, Merge Queue, Required Checks und Draft/Ready sind besser als eigenes Dauer-Babysitting.
7. **Nur echte Hochrisiko-Probleme blockieren.** Stoppe nicht wegen kleiner Reibung. Stoppe bei hohem Risiko und liefere dann Optionen.
8. **Immer resume-faehig bleiben.** Jeder neue Aufruf beginnt mit frischer Zustandserfassung. Ueberspringe Erledigtes und mache sinnvoll weiter.
9. **Arbeit retten statt stumpf abbrechen.** Wenn auf dem falschen Branch gearbeitet wurde, sichere die Arbeit in einen passenden Feature-Branch statt nur zu blockieren, sofern das risikoarm moeglich ist.

## Phase 0: Snapshot bauen

Baue zuerst einen belastbaren Snapshot. Ohne Snapshot keine Aktion.

Ermittle mindestens:

- aktueller Branch, Upstream, ahead/behind, Default-Branch
- liegt die Arbeit versehentlich direkt auf `main` / `master` / Release-Branch
- staged, unstaged, untracked, lokale Commits seit Base
- existiert bereits ein PR fuer den Branch, ist er Draft oder Ready, was ist die URL
- Review-Entscheidung, offene Threads, requested changes, neue Kommentare
- Status Checks, Deployments, mergeable, Auto-Merge, Merge Queue
- Branch-Protection / Rulesets soweit mit den vorhandenen Tools sichtbar
- Repo-Konventionen fuer Commits, Merge-Methode und PR-Body
- relevante Dateien fuer Build, Tests, CI, Workflows, CODEOWNERS und PR-Templates

Lies dafuer gezielt die Repo-Dateien und GitHub-Metadaten.

**Referenzen laden:** Bevor du mit Phase 0 beginnst, lies die folgenden Referenz-Dateien fuer die konkreten Entscheidungsbaeume:

- `references/repo-detection.md` - Repo-Struktur, Git-Zustand, Policy, Checks
- `references/commit-strategy.md` - Commit-Entscheidungslogik nach Fall A-E
- `references/review-and-merge.md` - Review-Prioritaet, Merge-Methode, Flaky-Handling
- `references/blockers-and-recovery.md` - Hard/Soft Blocker, Recovery-Budget, Ausgabeformat

Die Referenzen enthalten die detaillierten Regeln. Dieses Hauptdokument gibt die Strategie vor.

## Der Arbeitsmodus ist eine Decision Engine

Nach dem Snapshot klassifiziere den Zustand:

- `worktree_state`: clean, dirty, mixed, risky
- `history_state`: no-local-commit, local-unpushed, published, reviewed
- `pr_state`: none, draft, ready, waiting-checks, waiting-review, mergeable, blocked
- `policy_state`: unrestricted, protected, queue-required, auto-merge-possible, signed-commits-required
Leite aus diesen Zustaenden ein `risk_level` ab: `low`, `medium` oder `high`. Das Risk-Level bestimmt, ob autonom weitergearbeitet wird oder ein Stopp noetig ist (siehe Abschnitt "Harte Stopps nur bei Hochrisiko-Faellen").

Waehle dann die naechste Aktion nach diesem Muster:

| Zustand | Naechste Aktion |
|--------|-----------------|
| Dirty, keine lokalen Commits | Repo-native Checks, selektiv stagen, Commit erstellen |
| Dirty oder clean auf `main` / `master` mit noch nicht publizierter Arbeit | Arbeit auf sicheren Feature-Branch retten, dann normal weiter |
| Dirty, lokaler unpushed Commit, gleicher Scope, noch nicht reviewt | Amend nur wenn sicher und sinnvoll |
| Dirty, Commit bereits gepusht oder PR offen | Neuer Follow-up-Commit |
| Clean, lokale Commits ahead of upstream, kein PR | Push, dann PR erstellen oder vorhandenen PR finden |
| Clean, PR offen, Checks laufen | Nicht neu committen. Status auswerten, Auto-Merge oder Queue vorbereiten |
| PR offen, requested changes oder neue blocking Reviews | Review-Fixes sammeln, gezielt validieren, in sinnvollen Batches pushen |
| PR offen, alles gruen, Merge Queue vorhanden | In Queue einreihen oder Auto-Merge aktivieren |
| PR offen, alles gruen, keine Queue, Merge erlaubt | Mit Repo-konformer Methode mergen |
| `gh` fehlt oder ist nicht authentifiziert, lokale Arbeit ist aber bearbeitbar | In lokalen Vorbereitungsmodus gehen: validieren, committen, Branch vorbereiten, dann klaren Handover fuer Push/PR geben |
| Auto-Merge oder Queue bereits armed, keine neuen Probleme | Nicht stoeren. Nur auf neue Failures, Kommentare oder Konflikte reagieren |
| Signed commits required, aber lokale Umgebung kann nicht signieren | Commit lokal vorbereiten, dann Blocker melden mit Optionen: GPG/SSH-Key einrichten, Signierung in GitHub-UI, oder Maintainer-Hilfe |
| Mixed oder riskanter Zustand | Nicht blind weitermachen. Erst trennen, klaeren oder stoppen |

Wenn mehrere Aktionen moeglich sind, waehle die mit dem geringsten Risiko und der kleinsten History-Verzerrung.

## Lokale Validierung

Fuehre nicht pauschal `npm install`, `npm test` oder generische Befehle aus. Erkenne zuerst:

- Package-Manager
- Task-Runner
- Test-Frameworks
- Linter / Formatter
- Build-Tools
- CI-Definition
- Security-Checks

Nutze dann eine gestufte Strategie:

1. **Fast guardrails** fuer schnelle Fehlererkennung
2. **Repo-kritische Kernchecks** passend zu den Required Checks
3. **Nur wenn sinnvoll** aufwaendigere oder langsame Checks

Mutiere die Dependency-Landschaft nicht ohne Grund. Installiere oder regeneriere nur dann, wenn es fuer eine fundierte Verifikation noetig ist oder das Repo diesen Schritt klar vorgibt.

Wenn Install-, Build- oder Codegen-Schritte neue Lockfiles oder Build-Artefakte aendern, entscheide aktiv:

- gehoeren diese Aenderungen fachlich zur Aufgabe oder zur Repo-Konvention, dann duerfen sie mit
- sind sie nur Nebenwirkung eines lokalen Checks, dann nicht automatisch mitcommitten

Details stehen in [repo-detection.md](references/repo-detection.md).

## Commit- und History-Strategie

Arbeite pragmatisch statt dogmatisch:

- Committe nur Dateien, die zur Aufgabe gehoeren
- Lasse unrelated User-Aenderungen unberuehrt
- Nutze `git add .` nicht blind
- Folge zuerst der Repo-eigenen Commit-Konvention
- Nutze Conventional Commits nur wenn das Repo sie sichtbar verwendet oder der User es will
- Bevorzuge neue Follow-up-Commits gegenueber History-Rewrites auf bereits gepushten oder reviewten Aenderungen
- Nutze Amend nur fuer lokale, unpublizierte, klar zusammengehoerige Aenderungen
- Wenn das Repo squash merge nutzt, optimiere auf eine saubere PR und sinnvolle Zwischen-Commits, nicht auf perfekte Branch-History
- Wenn versehentlich direkt auf `main` / `master` gearbeitet wurde und die Arbeit noch nicht publiziert ist, verschiebe sie zuerst auf einen Feature-Branch und setze dort fort

Die konkrete Entscheidungslogik steht in [commit-strategy.md](references/commit-strategy.md).

## PR-Strategie

Arbeite nicht nach dem Muster "alles lokal fertig, dann PR". Nutze den fuer den Zustand passenden PR-Modus:

- **Draft PR** wenn die Arbeit sichtbar gemacht werden soll, aber noch nicht review- oder merge-fertig ist
- **Ready PR** wenn die lokalen Blocker beseitigt sind und Review sinnvoll ist
- **Bestehenden PR aktualisieren** statt Duplikate zu erzeugen

PR-Titel und Body sollen nicht nur Dateiaenderungen aufzahlen. Beschreibe:

- Nutzer- oder Systemwirkung
- wichtigstes Risiko
- wichtigste Validierung
- offene Punkte

Wenn ein PR-Template existiert, verwende es. Wenn das Repo Issue-Links oder Release-Notes erwartet, beruecksichtige das.

## Review-, CI- und Merge-Strategie

Arbeite nach Prioritaet:

1. failing required checks
2. requested changes von Menschen
3. Security- und Dependency-Signale
4. fachliche Bugs oder fehlende Tests
5. klare Maintainability-Probleme
6. Stil, Nits, Kosmetik

Batche zusammengehoerige Review-Fixes. Push nicht fuer jeden Kommentar einzeln.

Wenn Checks flaky wirken:

- rerunne einen bekannten oder plausiblen Infra-Flake begrenzt
- aendere nicht vorschnell Code, nur um ein instabiles Signal "gruen zu raten"
- wenn ein required Check wiederholt flaky oder infrastrukturell blockiert ist, dokumentiere das und entscheide zwischen Auto-Merge-Warten, Queue-Warten oder Blocker-Meldung

Nutze Plattform-Features bewusst:

- Auto-Merge wenn nur noch formale Gruen-Checks / Approvals fehlen
- Merge Queue wenn der Zielbranch sie erfordert oder anbietet
- Draft -> Ready wenn der Zustand reviewbar ist
- Thread-Resolution nur wenn der Punkt wirklich bearbeitet oder sauber begruendet wurde

Details stehen in [review-and-merge.md](references/review-and-merge.md).

## Harte Stopps nur bei Hochrisiko-Faellen

Unterbrich autonomes Weiterarbeiten nur bei schwerwiegenden Problemen, zum Beispiel:

- Secret, Token, Key oder Push-Protection-Fund
- unklare Datenverlust- oder Migrationsgefahr
- Branch-Protection / Auth / Berechtigungen verhindern den noetigen Schritt
- Merge-Konflikt oder Review-Forderung braucht eine fachliche Richtungsentscheidung
- mehrere unrelated Change-Sets lassen sich nicht sicher trennen, besonders wenn dieselben Dateien betroffen sind
- required checks schlagen fehl und die Ursache ist nach fokussiertem Versuch nicht belastbar klar
- Workflow- oder Infra-Aenderung waere ohne weitere Absicherung riskant
- Base-Branch oder Zielrepo ist in einem Fork-/Upstream-Setup nicht belastbar klar

Dann liefere nicht nur den Fehler, sondern immer:

- Blocker
- Beobachtete Fakten
- Warum autonomes Weiterarbeiten riskant waere
- Option A
- Option B
- Option C
- Empfehlung

Die genaue Matrix steht in [blockers-and-recovery.md](references/blockers-and-recovery.md).

## Resume-Verhalten

Dieser Skill muss jederzeit erneut aufgerufen werden koennen.

Deshalb gilt:

- Starte immer mit einem frischen Snapshot
- Erkenne vorhandene Commits, vorhandenen PR, vorhandene Reviews und vorhandene CI-Laeufe
- Ueberschreibe keine frueheren Entscheidungen blind
- Wenn Auto-Merge oder Queue bereits armed ist, greife nur bei neuen Problemen ein
- Wenn bereits Commits existieren, entscheide aktiv zwischen `nichts tun`, `push`, `amend`, `follow-up commit`
- Wenn bereits ein PR offen ist, arbeite auf diesem PR weiter, ausser es gibt einen sehr guten Grund fuer einen neuen

## Abschlussformate

### Wenn erfolgreich abgeschlossen

Liefere eine kurze, anwendungsbezogene Zusammenfassung:

- Was wurde fuer Nutzer oder System erreicht
- Welche relevanten Probleme wurden unterwegs entdeckt und behoben
- Was ist noch offen
- PR-Link, Branch, Merge-Status, wichtigste Validierungen

### Wenn nicht final gemerged, aber sauber vorbereitet

Sage klar, ob der Zustand jetzt einer dieser Faelle ist:

- Draft PR erstellt und bereit fuer weitere Arbeit
- Ready PR offen und wartet auf Reviews
- Auto-Merge armed
- Merge Queue armed
- Warten auf externe Freigabe / Berechtigung / Input

### Wenn blockiert

Nutze das Blocker-Format aus [blockers-and-recovery.md](references/blockers-and-recovery.md).

## Claude-spezifische Hinweise

- Nutze bevorzugt vorhandene Repo-Tools und GitHub CLI.
- Formuliere Entscheidungen explizit, statt nur Befehle aneinanderzureihen.
- Wenn Shell-Syntax vom System abhaengt, passe sie an die tatsaechliche Shell an statt Bash blind anzunehmen.
- Halte den User ueber groessere Richtungswechsel auf dem Laufenden, aber stoppe nur bei echten Hochrisiko-Themen.
