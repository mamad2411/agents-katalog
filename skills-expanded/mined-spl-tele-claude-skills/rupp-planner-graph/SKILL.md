---
name: rupp-planner-graph
description: Schreibt und liest Microsoft Planner über die Graph API. Nutze diesen Skill immer wenn Microsoft-Planner-Aufgaben erstellt, geändert, gelöscht, abgefragt, zugewiesen oder synchronisiert werden sollen, oder wenn Buckets/Pläne über die Graph API verwaltet werden — auch wenn der Benutzer nur "Planner" oder "MS Planner" oder eine Plan-/Task-/Bucket-ID erwähnt. Trigger-Phrasen Deutsch und Englisch, Beispiele Planner-Aufgabe erstellen, Task in Planner anlegen, Microsoft Planner Task, Planner-Bucket, Plan abfragen, Aufgabe zuweisen, Planner aktualisieren, Planner Task löschen, MS Planner schreiben, Graph Planner, Planner sync, Planner update, planner.cloud.microsoft, Tasks.ReadWrite, Plan-ID, Bucket-ID, Task-ID. Nutze diesen Skill auch proaktiv wenn der Benutzer einen planner.cloud.microsoft- oder tasks.office.com-Link teilt, oder wenn aus einem anderen System (n8n, Outlook) etwas nach Planner überführt werden soll.
---

# Rupp Planner Graph

Pragmatischer Microsoft-Graph-Client für **Microsoft Planner** — Lesen und Schreiben von Plans, Tasks, Buckets und Task-Details über REST. Erfüllt den SPL-Tele-Skript-Standard (Header-Konvention, siehe Header in jedem Script).

## Was dieser Skill kann

**Lesen:**
- Plan-Metadaten abrufen (Plan-ID → Title, Owner-Group, Container)
- Tasks eines Plans listen (mit Bucket, Assignments, Progress, ETag)
- Buckets eines Plans listen
- Task-Details lesen (Description, Checklist, External References)

**Schreiben:**
- Tasks erstellen (mit Bucket-Zuordnung, Assignments, Due Date, Priority, Title)
- Tasks aktualisieren (Progress, Title, Due Date, Bucket-Wechsel, Assignments)
- Task-Details aktualisieren (Description, Checklist)
- Tasks löschen
- Buckets erstellen

**Was bewusst NICHT abgedeckt ist:**
- Premium-Plans (Planner P1 / Project for the Web) — von Graph nicht unterstützt (Stand 2026)
- Plan-Erstellung (erfordert Group-Container-Setup, separater Workflow)
- Recurring Tasks (Graph-API-Limitation)

## Voraussetzungen

1. **Code-Execution-Sandbox verfügbar** (Bash + Python) — der Skill ist scriptbasiert, nicht tool-basiert. Funktioniert in Claude.ai mit Sandbox, Claude Code, Cowork.
2. **Entra-ID-App-Registration mit Graph-Permissions** — siehe `references/app-registration.md`. Bei SPL-Tele-Tenant: Admin Consent durch CDO/IT-Security erforderlich.
3. **Python-Packages:** `msal`, `requests`. Werden bei Bedarf via `pip install --break-system-packages msal requests` installiert.

## Auth-Strategien — wann welche

| Strategie | Wann | Wie |
|-----------|------|-----|
| **Bearer-Token direkt** | Schnelles Testen, einmaliger Auftrag, kurze Sessions | Token aus Graph Explorer kopieren, als `GRAPH_TOKEN` Env-Var setzen. Lebt ~1h. |
| **Device Code Flow** | Interaktive Sessions, persönliches Konto, kein Service-Account | `python scripts/auth.py --device-code` startet Flow, User loggt sich auf microsoft.com/devicelogin ein. Token-Cache `.token_cache.json`. |
| **Client Credentials** | Headless Automation, n8n-Integration, Service-Workflows | Tenant-ID + Client-ID + Client-Secret als Env-Vars. Erfordert Application Permissions (`Tasks.ReadWrite.All`) mit Admin Consent. |

**Wichtig:** Tokens niemals in Output-Dateien echoen. Scripts loggen nur die ersten/letzten 6 Zeichen zu Debug-Zwecken.

## Workflow für jeden Planner-Auftrag

1. **Auth klären** — welche Strategie? Falls Tokens nicht in Env vorhanden, bei Dimitri abholen (er gibt sie im Chat, gemäss API-Token-Policy).
2. **Plan-ID identifizieren** — aus dem Planner-URL extrahieren (`planner.cloud.microsoft/webui/plan/<PLAN_ID>/view/board`), Tenant-ID aus dem `tid=`-Parameter.
3. **Kontext laden** — `scripts/get_plan.py <PLAN_ID>` für Plan-Metadaten + Buckets, damit Bucket-IDs für Task-Creation bekannt sind.
4. **Operation ausführen** — Tasks listen/erstellen/aktualisieren/löschen.
5. **Verifikation** — Bei jedem Schreibvorgang anschliessend GET, um Persistenz zu bestätigen (BVL: 1 = sichtbar, 0 = nochmal).
6. **Output für Dimitri** — Kompaktes Markdown-Summary mit Task-IDs, Statusänderungen, Errors. Keine Token-Echoes.

## Kritische ETag-Regel

Jedes `PATCH` und `DELETE` auf Planner-Ressourcen MUSS einen `If-Match`-Header mit dem aktuellen ETag der Ressource enthalten. ETag kommt aus dem vorausgehenden GET (Header `@odata.etag`).

```
PATCH /planner/tasks/{id}
Headers:
  Authorization: Bearer <token>
  Content-Type: application/json
  Prefer: return=representation
  If-Match: W/"JzEtVGFzayAgQEBAQEBAQEBAQEBAQEBAWCc="
```

Fehlender oder veralteter ETag → `412 Precondition Failed`. Der Client in `scripts/planner_client.py` handhabt das automatisch (fetch → modify → patch), aber: **nie ETag manuell raten oder weglassen**.

## Häufige Fallstricke

- **OrderHint:** Beim Setzen Format ` !` oder Pattern aus Doku verwenden, nicht den Wert aus GET 1:1 zurückgeben — Graph generiert intern um. Bei unsicheren Fällen: weglassen, Default greift.
- **Assignments:** Jeder Assignment-Eintrag braucht `"@odata.type": "#microsoft.graph.plannerAssignment"` als Pflichtfeld.
- **PercentComplete:** Nur Werte 0, 50 (in progress) oder 100 (complete) sind UI-wirksam. Andere Werte werden zwar gespeichert, aber Planner-UI rundet.
- **Due Date / Start Date:** ISO 8601 mit Zeitzone, z. B. `2026-06-01T00:00:00Z`. Start-Date nach Due-Date → 400 Bad Request.
- **Premium-Plan-Detect:** Wenn GET 403 mit `code: NotSupported` liefert, ist es ein Premium-Plan → Graph nicht nutzbar, dem User klar mitteilen.

## Scripts — Übersicht

Alle Scripts in `scripts/` laden Auth automatisch aus Env-Vars oder Token-Cache und akzeptieren Argumente via CLI.

- `auth.py` — Device Code Flow Setup, Token-Cache verwalten, Token-Validierung
- `planner_client.py` — Core-Client (importierbar, nicht direkt aufrufen)
- `get_plan.py <PLAN_ID>` — Plan + Buckets als JSON
- `list_tasks.py <PLAN_ID>` — Alle Tasks des Plans (mit ETag-Spalte)
- `create_task.py --plan <PLAN_ID> --bucket <BUCKET_ID> --title "..." [--due ISO] [--assign USER_ID]`
- `update_task.py --task <TASK_ID> [--title ...] [--progress N] [--due ISO] [--bucket BUCKET_ID]`
- `delete_task.py --task <TASK_ID>`
- `update_task_details.py --task <TASK_ID> --description "..."` (für lange Beschreibungen)
- `list_buckets.py <PLAN_ID>`

## Wann mehrere Operationen → Batching

Bei >5 Tasks in einem Auftrag: Batching-Strategie über `$batch`-Endpoint (in `planner_client.py` als `batch_request()` verfügbar). Reduziert Latenz und Rate-Limit-Druck.

## Verweise

- `references/app-registration.md` — Entra-ID-App-Setup, Permissions, Admin-Consent-URL-Template
- `references/api-endpoints.md` — Graph-Endpoint-Cheatsheet mit Permissions je Operation
- `examples/workflow-examples.md` — Konkrete Anwendungsfälle (Outlook→Planner, Ticketsystem→Planner, Bulk-Import)

## Qualitäts-Check vor Skill-Abschluss (Rupp-BVL)

1. Auth funktioniert (Token validiert, Whoami liefert User-ID)? **1/0**
2. Get-Operations liefern erwartete Strukturen? **1/0**
3. ETag-Handling bei Write-Operations korrekt? **1/0**
4. Keine Tokens in Outputs/Logs/Files (Grep-Test)? **1/0**
5. SPL-Tele-Skript-Standard-Header in allen Scripts vorhanden? **1/0**

Nur bei 5×1 → Output an Dimitri freigegeben.
