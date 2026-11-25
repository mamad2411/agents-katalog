# Debugging Protokoll
- Bevor du Code änderst, erstelle eine kurze Hypothese: "Was ist die wahrscheinlichste Ursache?"
- Analysiere immer die Seiteneffekte: "Welche anderen Komponenten könnten durch diesen Fix brechen?"
- Wenn ein Fehler unklar ist, schlage zuerst Log-Statements (Print-Debugging) an strategischen Stellen vor, anstatt zu raten.
- Bevorzuge bei komplexen Fehlern Claude Opus 4.5 für die Analyse und Sonnet 4.5 für die Implementierung.
# Kontext-Regeln
- Lies immer die `README.md` oder zentrale Typ-Definitionen, bevor du Logik in Untermodulen änderst.
- Wenn du eine Funktion änderst, prüfe auch deren Aufrufer (Call Hierarchy), um Typ-Konflikte zu vermeiden.
- Nutze das `@Codebase` Tool nur, wenn der Fehler über mehrere Layer (z.B. Frontend -> API -> DB) hinweg geht.
# Code-Qualität beim Fixen
- Schreibe für jeden Bug-Fix einen passenden Unit-Test, falls möglich.
- Behalte den bestehenden Coding-Stil exakt bei (z.B. Early Returns, Namenskonventionen).
- Lösche niemals Kommentare oder bestehende Fehlerbehandlungen (Try-Catch), es sei denn, es ist explizit gefordert.

# TradeTrackr Development & Debugging Rules

## Tech-Stack Context
- Frontend: Flutter (FlutterFlow-kompatibel, aber Fokus auf Custom Code)
- Navigation: GoRouter (Strict Type-Safety)
- Database: Firestore (Remote) + Isar/SQLite (Local)
- Auth: Firebase Auth mit RBAC (Owner, Admin, Mitarbeiter)

## Debugging: Sync & Data-Flow
- Bei Fehlern in der Datenanzeige: Prüfe IMMER zuerst, ob der Fehler im Local Store (Isar), im Sync-Service oder in Firestore liegt.
- Sync-Logik: Achte bei Bugfixes auf Idempotenz. Mehrfache Sync-Versuche dürfen keine Duplikate erzeugen.
- Konfliktlösung: Bevorzuge beim Mergen von Delta-Updates die "Last-Write-Wins" Strategie, sofern nicht anders im Code definiert.

## Multi-Tenancy & Security
- Jeder Firestore-Query MUSS eine `tenantId` Filterung enthalten. 
- Prüfe bei jedem neuen Feature: "Ist sichergestellt, dass Mitarbeiter A keine Daten von Mandant B sieht?"
- Security Rules: Wenn du Backend-Logik änderst, weise mich darauf hin, falls die Firebase Security Rules angepasst werden müssen.

## Flutter Performance (Handwerker-App)
- Offline-First: UI-Komponenten müssen immer einen Lade- und Offline-Status haben.
- Asset-Handling: Bilder für Berichte müssen vor dem Upload komprimiert werden. Debugge Speicherlecks bei der Bildverarbeitung besonders kritisch.

## KI-Module (OCR/Agenten)
- Fehlgeschlagene OCR-Erkennungen müssen im lokalen State markiert werden, damit der Nutzer sie manuell korrigieren kann, bevor sie nach Firestore synchronisiert werden.