---
name: spl-python-automation
description: >
  Python-Automationen für SPL-Tele, die in PyRunner (pyrunner.spl-tele.com) laufen: Skript-Aufbau,
  die injizierten Helper-Module (pyrunner_ai, pyrunner_datastore, pyrunner_notify, pyrunner_db,
  pyrunner_storage), venv-Pakete, Secrets aus Infisical, Zustandsführung im DataStore, Preflight
  und die Reihenfolge beim Testen. Enthält außerdem die wiederkehrenden Anbindungen: XWiki-REST,
  GitHub-API, Coolify. Nutze diesen Skill immer, wenn eine wiederkehrende Aufgabe automatisiert,
  ein PyRunner-Skript geschrieben, geändert oder debuggt wird, oder wenn ein Automationslauf
  fehlschlägt. Trigger: PyRunner, Automation erstellen, Skript anlegen, ModuleNotFoundError im
  Skript, pyrunner_ai, pyrunner_datastore, DataStore, geplantes Skript, Zeitplan, XWiki schreiben,
  Doku ins Wiki, Skript läuft nicht.
license: MIT
metadata:
  version: 1.0.0
  updated: 2026-08-19
---

# Python-Automationen für SPL-Tele

Automationen laufen in **PyRunner** unter `https://pyrunner.spl-tele.com` — nicht in Claude
Desktop (kein Scheduler, läuft nur bei geöffneter App) und nicht als Cronjob auf einem
Einzelrechner. PyRunner liefert Zeitpläne, verschlüsselte Secrets, venv je Skript,
Run-Historie und einen konfigurierten Claude-Provider.

Läuft auf Postgres (seit 2026-08-19), nicht auf der SQLite-Vorgabe: mehrere Automationen
schreiben nebenläufig, und SQLite serialisiert instanzweit.

## Bevor du Code schreibst

Kläre drei Dinge — sie bestimmen den Aufbau:

1. **Was löst den Lauf aus?** Zeitplan ist die Vorgabe. Eingehende Webhooks kann PyRunner
   (`Channel.inbound_enabled`), aber das verlangt Erreichbarkeit von außen. Polling überlebt
   Neustarts und verpasst nichts.
2. **Was ist der Zustand zwischen zwei Läufen?** Fast jede Automation braucht „was habe ich
   schon verarbeitet". Ohne das ist der Lauf nicht idempotent.
3. **Was passiert bei halbem Fehlschlag?** Ein Lauf, der nach der Hälfte stirbt, darf beim
   nächsten Mal nicht doppelt schreiben und nichts überspringen.

## Die injizierten Helper-Module

Nur innerhalb von PyRunner verfügbar. Import immer defensiv, sonst ist das Skript lokal
nicht testbar.

| Modul | Zweck | Aufruf |
|---|---|---|
| `pyrunner_ai` | Claude über den konfigurierten Provider | `from pyrunner_ai import ask_claude` |
| `pyrunner_datastore` | Key-Value-Zustand | `from pyrunner_datastore import DataStore` |
| `pyrunner_notify` | E-Mail/Benachrichtigung | `pyrunner_notify.email(html=…)` |
| `pyrunner_db` | Managed Postgres (Databases-Feature) | `import pyrunner_db` |
| `pyrunner_storage` | Dateiablage | `import pyrunner_storage` |

```python
ask_claude(prompt, tools=[], system_prompt=…, model="claude-sonnet-5", lean=True)
```

`tools=[]` schaltet das Agent-Toolset ab (reine Textgenerierung), `lean=True` spart rund
50k Tokens Agent-Overhead pro Aufruf. Beides gehört zum Standardaufruf, wenn du nur Text
erzeugen lässt.

`DataStore(name)` bietet `get(key)`, `set(key, value)`, `delete`, `contains`, `keys`,
`items`, `clear`. **`get()` nimmt keinen Default-Parameter** — `get(key, {})` wirft
TypeError. Fehlende Werte selbst abfangen. Werte als JSON-String ablegen, dann ist das
Format über Versionen hinweg stabil.

## Die drei häufigsten Fehlschläge

**1. `ModuleNotFoundError` — venv-Pakete.** Nur die Pakete des PyRunner-Images sind da.
`requests` ist **nicht** dabei. Jedes externe Paket muss unter *Environments* an der
Umgebung des Skripts hängen. Deshalb: externe Importe defensiv und im Preflight melden,
statt das Skript in Zeile 30 sterben zu lassen.

```python
try:
    import requests
except ImportError:
    requests = None   # Preflight meldet es mit Handlungsanweisung
```

**2. Beschädigter Code beim Einfügen.** Der Web-Editor kann beim Einfügen Zeichen
verschlucken — typisch ein `import json`, das als `import ` ankommt und einen SyntaxError
in einer Zeile wirft, die im Original korrekt ist. `core/executor.py` schreibt den
gespeicherten Code **unverändert** in die temporäre Datei, ohne Zeilen voranzustellen: Die
Zeilennummer im Traceback ist also exakt die Zeile im Editor. Nach dem Einfügen Zeilenzahl
und letzte Zeile gegenprüfen.

**3. Fehlende Secrets erst zur Laufzeit.** Siehe Preflight.

## Preflight — verpflichtendes Muster

Alles prüfen, was den Lauf scheitern lässt, **bevor** die erste Einheit verarbeitet wird:
Module, Umgebungsvariablen, Erreichbarkeit und Authentifizierung jedes Zielsystems. Ein
Lauf, der nach der Hälfte an einer fehlenden Variable stirbt, hat AI-Tokens verbraucht und
möglicherweise halb geschrieben.

Jede Meldung nennt das Problem **und** die Behebung:

```
FEHLT: Das Paket 'requests' fehlt in der Python-Umgebung.
   -> PyRunner: Environments -> Umgebung des Skripts -> Package hinzufuegen: requests
```

Alle Probleme sammeln und gemeinsam ausgeben — nicht beim ersten abbrechen. Sonst wird
Fehlersuche zur Schleife: fehlt dreierlei, braucht es sonst drei Läufe.

## Secrets

Herkunft ist **Infisical** (siehe Skill `infisical-secrets`), hinterlegt werden sie als
Secrets am Skript und landen als Umgebungsvariablen im Lauf. Niemals im Code, niemals im
Repo, niemals ins Log.

| Zweck | Infisical |
|---|---|
| GitHub (fabric_documentation) | `github/prod → GITHUB-FABRIC-DOCUMENTATION-XWIKI-PAT` |
| XWiki | `dimitri/prod → XWIKI-IT-ADMIN-DRU`, `XWIKI-IT-ADMIN-PASSWORD` |
| Coolify | `infra/prod → COOLIFY_API_TOKEN` |
| PyRunner-API | `apps/prod → PYRUNNER-API-TOKEN-CLAUDE-CODE` |

Für Automationen fine-grained Tokens mit minimalem Umfang. Fine-grained PATs auf
`spl-tele`-Repos brauchen die Freigabe eines Org-Owners — bis dahin liefern sie 404 auf
jedes private Repo, ununterscheidbar von fehlenden Rechten.

## Zustand und Idempotenz

Pro Einheit den Änderungsstempel der Quelle speichern (Blob-SHA, ETag, `updated_at`) und
beim nächsten Lauf vergleichen. Unverändert → überspringen.

```python
{"blob_sha": "...", "status": "ok", "ziel": "...", "synced_at": "2026-08-19T09:38:00Z"}
```

`status` mitschreiben: Fehlgeschlagenes wird erneut versucht, Erfolgreiches nicht. Ein
`FORCE=1`-Schalter für erzwungene Neuverarbeitung gehört dazu.

## Vor dem Schreiben validieren

Wenn ein Modell den Inhalt erzeugt, prüfe das Ergebnis, bevor es ein Zielsystem erreicht:
Struktur vorhanden, Markup balanciert, kein Fremdformat durchgerutscht — und **kein
plötzlicher Umfangsverlust** gegenüber dem Bestand (Schutz gegen versehentliches
Leerschreiben). Schlägt die Prüfung an: Ziel unangetastet lassen, Fehler protokollieren,
beim nächsten Lauf erneut versuchen.

## Wiederkehrende Anbindungen

**XWiki** (`http://xwiki.intern.spl-tele.com`) — REST unter `/rest/wikis/xwiki`.
Unterseiten sind eigene Spaces: `/spaces/A/spaces/B/pages/WebHome`, **nicht**
`/spaces/A.B/`. Schreiben per `PUT` mit `application/xml` und `<syntax>xwiki/2.1</syntax>`.
XWiki versioniert jede Änderung, ein Überschreiben ist also rückholbar. Seiten-Standard:
`{{box}}`+`{{toc/}}`, `= Titel =`, `{{info}}` mit **What:**, `|=`-Tabellen, `{{mermaid}}`.

**GitHub** — Dateiliste über `git/trees/<ref>?recursive=1` (liefert Blob-SHAs für den
Zustandsvergleich gleich mit), Inhalt über `contents/<pfad>` (base64).

**Coolify** (`http://coolify.intern.spl-tele.com/api/v1`) — Deployments und Env-Variablen.
Kein Endpunkt für Befehlsausführung im Container. `docker_compose_domains` erwartet beim
PATCH ein **Array** aus `{name, domain}`.

## Testreihenfolge

1. **Lokal** gegen die echten Systeme, Schreibpfade abgeschaltet
2. **Trockenlauf** (`DRY_RUN=1`) — Ergebnis nur ins Log
3. **Testbereich** im Zielsystem (`_Test/`), nicht der Produktivbaum
4. **Produktiv**, dann erst Zeitplan aktivieren

Beim ersten Lauf in PyRunner zusätzlich prüfen, was lokal nicht testbar war: Der DataStore
existiert nur dort — ein **zweiter** Lauf ohne Quelländerung muss „unverändert" melden.

## Modell-IDs

`claude-sonnet-5`, `claude-opus-5`, `claude-haiku-4-5` — ohne angehängte Datums- oder
Versionsteile. **PyRunner validiert das Feld nicht**: Eine falsche ID zeigt „Last tested"
in Grün und scheitert erst beim ersten echten Lauf. Und ein Provider kann *Configured*
sein und trotzdem *disabled* — „Enable AI for scripts" ist ein separater Schalter.
