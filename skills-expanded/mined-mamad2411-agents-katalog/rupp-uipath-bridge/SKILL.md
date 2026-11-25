---
name: rupp-uipath-bridge
description: Liest und schreibt UiPath Orchestrator über die OData API. Nutze diesen Skill immer wenn UiPath-Inhalte abgefragt, gemonitort, deployed, gestartet oder verwaltet werden sollen — Folders, Releases (Processes), Jobs, Queues, Schedules (Triggers), Assets, Buckets, Robots, Machines, Audit-Logs. Trigger-Phrasen Deutsch und Englisch, Beispiele UiPath abfragen, UiPath Inventur, Orchestrator durchsuchen, Bot starten, Job auslösen, Queue Item einfügen, Asset abrufen, RedPath Status, UiPath Audit, UiPath Folder, UiPath Robot, UiPath Schedule, UiPath Snapshot, Tenant-Inventur, cloud.uipath.com, X-UIPATH-OrganizationUnitId. Nutze diesen Skill auch proaktiv wenn der Benutzer einen cloud.uipath.com-Link teilt, eine Folder-ID (fid=) oder Tenant-ID (tid=) erwähnt, oder wenn aus einem anderen System (BCA, RIMO, n8n) Daten in UiPath synchronisiert werden sollen.
---

# Rupp UiPath Bridge

Pragmatischer UiPath-Orchestrator-Client für die SPL Tele Cloud-Instanz. Lesen und Schreiben aller wichtigen Orchestrator-Ressourcen über die OData-REST-API. Erfüllt die Rupp-Qualitäts-Charta (Evidenz-Prinzip, BVL, Reputations-Mandat) und den SPL-Tele-Skript-Standard (Header-Konvention, siehe Header in jedem Script).

## Was dieser Skill kann

**Lesen:**
- Tenant-weite Inventur (Folders, Machines, Robots, Sessions, Libraries)
- Folder-Inhalt (Releases, Queues, Schedules, Assets, Buckets, Tasks, TestSets)
- Job-Historie mit Filter (State, Source, Type, Zeitfenster)
- Audit-Logs (sofern aktiviert)
- User-Identität und Permissions
- Vollständige Tenant-Snapshots als JSON oder Excel

**Schreiben (mit Vorsicht!):**
- Folder anlegen, umbenennen, löschen
- Asset erstellen / aktualisieren
- Queue Item einfügen
- Process Schedule (Trigger) anlegen
- Job ad-hoc starten / stoppen

**Bewusst NICHT abgedeckt:**
- Release-Deployment (gehört in den CI/CD-Pipeline-Kontext, nicht in den Bridge-Skill)
- Robot-Provisioning (UI-getrieben, EntraID-föderiert bei SPL)
- Tenant-Settings (administrative Schicht, nur via UI/Identity Server)
- Studio-Code-Generation (separater Workflow)

## Voraussetzungen

1. **Code-Execution-Sandbox** (Bash + Python) — Skill ist scriptbasiert. Funktioniert in Claude.ai mit Sandbox, Claude Code, Cowork.
2. **UiPath Personal Access Token (PAT)** mit ausreichendem Scope. Erstellung: UiPath Cloud → User-Icon → Preferences → Personal Access Token → Generate.
3. **Python-Packages:** `requests`, `openpyxl`. Werden bei Bedarf via `pip install --break-system-packages requests openpyxl` installiert.
4. **Tenant-Kontext bekannt:** Organization, Tenant, Base-URL.

## Authentifizierung

Token wird ausschliesslich aus Environment-Variablen gelesen — **niemals im Code hardcoden**.

```bash
export UIPATH_PAT='rt_<...>'
export UIPATH_ORG='spltele'
export UIPATH_TENANT='DefaultTenant'
export UIPATH_BASE="https://cloud.uipath.com/${UIPATH_ORG}/${UIPATH_TENANT}/orchestrator_"
```

Im Output erscheinen Tokens nur als `${UIPATH_PAT}`-Platzhalter. Scripts loggen maximal die ersten/letzten 4 Zeichen zu Debug-Zwecken.

## Folder-Kontext-Regel (kritisch)

Viele Orchestrator-Endpoints (Releases, QueueDefinitions, ProcessSchedules, Assets, Buckets, Tasks, TestSets) benötigen einen **Folder-Header**:

```
X-UIPATH-OrganizationUnitId: <FolderId>
```

Fehlt der Header → HTTP 400. Lösung: Skill setzt Header automatisch aus Argument `--folder-id` oder iteriert über alle Folder bei Tenant-Snapshots.

Ausnahmen (kein Folder-Header nötig):
- Folders, Machines, Jobs, Libraries, AuditLogs, Users → Tenant-Scope.

## Workflow für jeden UiPath-Auftrag

1. **Token-Status klären** — Falls `UIPATH_PAT` nicht in Env, bei Dimitri abholen (gemäss API-Token-Policy aus User-Preferences 5.2).
2. **Tenant-Kontext setzen** — Org, Tenant, Base-URL als Env-Vars (Default: spltele/DefaultTenant).
3. **Identität verifizieren** — `python scripts/uipath_bridge.py whoami` → BVL 1 wenn User-ID + Email zurückkommt.
4. **Operation ausführen** — read/write je nach Auftrag.
5. **Verifikation bei Writes** — Anschliessend GET, um Persistenz zu bestätigen.
6. **Output für Dimitri** — Kompaktes Markdown-Summary mit IDs, Statusänderungen, Errors. Keine Token-Echoes.

## Script-Übersicht

Alle Scripts in `scripts/` laden Auth automatisch aus Env-Vars und akzeptieren Argumente via CLI.

| Script | Zweck |
|---|---|
| `uipath_bridge.py` | Hauptskript mit Subcommands (siehe unten) |
| `UiPath-Bridge.ps1` | PowerShell-Pendant für Windows-Sessions |
| `requirements.txt` | Python-Dependencies |

### Subcommands von `uipath_bridge.py`

```
python uipath_bridge.py whoami
    → Aktueller User, Token-Status, Tenant-Info

python uipath_bridge.py snapshot --out ./snapshot_YYYYMMDD/
    → Vollständige JSON-Inventur aller Ressourcen (forensische Baseline)

python uipath_bridge.py snapshot --out ./snapshot_YYYYMMDD/ --xlsx
    → Snapshot + Excel-Audit-Report

python uipath_bridge.py folders [--type Standard|Solution] [--filter "RedPath*"]
    → Folder-Liste mit Hierarchie

python uipath_bridge.py folder-content --folder-id <ID>
    → Inhalt eines Folders (Releases, Queues, Schedules, Assets, Buckets)

python uipath_bridge.py jobs [--state Successful|Faulted|Running] [--top N] [--since YYYY-MM-DD]
    → Job-Historie mit Filtern

python uipath_bridge.py job --id <JOB_ID>
    → Job-Detail inklusive Logs, Input-/Output-Argumente

python uipath_bridge.py releases --folder-id <ID>
    → Releases (deployed Processes) in einem Folder

python uipath_bridge.py queues --folder-id <ID>
    → Queue-Definitionen in einem Folder

python uipath_bridge.py queue-items --queue-name <NAME> --folder-id <ID> [--status New|InProgress|Successful|Failed]
    → Queue-Items abfragen

python uipath_bridge.py add-queue-item --queue-name <NAME> --folder-id <ID> --json '{"key":"value"}'
    → Queue-Item einfügen

python uipath_bridge.py assets --folder-id <ID>
    → Assets-Liste (Werte nur für Text-Assets sichtbar)

python uipath_bridge.py start-job --release-key <KEY> --folder-id <ID> [--input '{"k":"v"}']
    → Job ad-hoc starten

python uipath_bridge.py audit [--since YYYY-MM-DD] [--top N]
    → Audit-Log-Events (sofern aktiviert)
```

## Beispiel-Workflows

### 1. Pre-RedPath-Baseline (forensischer Snapshot)

```bash
export UIPATH_PAT='rt_<...>'
export UIPATH_ORG='spltele'
export UIPATH_TENANT='DefaultTenant'
python uipath_bridge.py snapshot --out ./baseline_20260521/ --xlsx
```

→ `baseline_20260521/snapshot.json` (alle Ressourcen) + `baseline_20260521/audit.xlsx`.

### 2. Tägliches RedPath-Monitoring (nach Go-Live)

```bash
python uipath_bridge.py jobs --since 2026-06-01 --state Faulted --top 50
python uipath_bridge.py queue-items --queue-name RedPath_Tickets --folder-id <RedPath_ID> --status Failed
```

### 3. Asset-Inventur für GuardRail-Compliance

```bash
for fid in $(python uipath_bridge.py folders --json | jq -r '.[].Id'); do
  python uipath_bridge.py assets --folder-id $fid
done > all_assets.txt
```

### 4. Queue-Item-Push aus n8n / RIMO

```bash
python uipath_bridge.py add-queue-item \
  --queue-name RIMO_TicketDispatch \
  --folder-id 110425 \
  --json '{"TicketId": "INC-12345", "Priority": "P2", "AssignedTo": "noc-24x7"}'
```

## Häufige Fallstricke

- **400 ohne Folder-Header** → `--folder-id` setzen oder via `--all-folders` iterieren.
- **404 auf bekannte Endpoints** → API-Pfad zu alt? UiPath ändert OData-Routen zwischen Major-Releases. Bei Bedarf in `references/endpoints.md` Cheatsheet aktualisieren.
- **403 trotz validem Token** → PAT-Scope zu eng. UI öffnen, neuen PAT mit weiterem Scope erstellen.
- **429 Rate-Limit** → UiPath Cloud limitiert ~50 Req/s. Bei Massen-Iterationen `--rate-limit 30` setzen.
- **Audit-Log leer** → Cloud-Audit per default nicht aktiviert, muss von Tenant-Admin enabled werden.
- **Personal Workspace nicht im Folder-Listing** → Personal Workspaces sind separate Scope-Klasse. Über `--scope personal` abfragen.

## Qualitäts-Check vor Skill-Output (Rupp-BVL)

1. Auth funktioniert (whoami liefert User-ID + Email)? **1/0**
2. Folder-Header bei allen relevanten Endpoints korrekt? **1/0**
3. Bei Write-Operationen: nachfolgender GET bestätigt Persistenz? **1/0**
4. Keine Tokens in Outputs/Logs/Files (Grep-Test)? **1/0**
5. SPL-Tele-Skript-Standard-Header in allen Scripts vorhanden? **1/0**

Nur bei 5×1 → Output an Dimitri freigegeben.

## Verweise

- `references/endpoints.md` — OData-Endpoint-Cheatsheet mit Folder-Header-Anforderungen
- `references/scopes.md` — PAT-Scope-Übersicht (welche Operation braucht welchen Scope)
- `examples/redpath-monitoring.md` — Tägliche Job/Queue-Beobachtung für RedPath nach Go-Live
- `examples/guardrail-asset-audit.md` — Asset-Inventur für Sensitivity-Label-Compliance
