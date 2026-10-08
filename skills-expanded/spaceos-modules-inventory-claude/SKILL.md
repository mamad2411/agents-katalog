# SpaceOS.Modules.Inventory — CLAUDE.md

## SESSION STARTUP/SHUTDOWN RITUAL

**Minden session elején:**
```bash
# 0. Datahaven státusz regisztráció — jelezd hogy dolgozol
curl -X POST https://datahaven.joinerytech.hu/api/terminal/status \
  -H "Authorization: Bearer $DASHBOARD_AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "terminal": "inventory",
    "status": "working",
    "currentTask": "Session started - checking inbox"
  }'

# 1. Inbox ellenőrzés
ls /opt/spaceos/docs/mailbox/inventory/inbox/
grep -l "status: UNREAD" /opt/spaceos/docs/mailbox/inventory/inbox/*.md 2>/dev/null
```

**Session végén (DONE/BLOCKED outbox után):**
```bash
# Datahaven státusz regisztráció — jelezd hogy befejeztél
curl -X POST https://datahaven.joinerytech.hu/api/terminal/status \
  -H "Authorization: Bearer $DASHBOARD_AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"terminal":"inventory","status":"idle"}'
```

**Datahaven Dashboard:** https://datahaven.joinerytech.hu (token: `dev-token-spaceos-dashboard-2026`)
- Dashboard (`/`) — Inventory státusz (WORKING/IDLE), inbox/outbox metrikák
- Kanban (`/kanban`) — Inventory swimlane a Delivery track-en
- Teljes API: `docs/WORKFLOW.md` — "Datahaven Dashboard" szakasz

---

## JELENLEGI ÁLLAPOT (2026-04-17)

| | |
|---|---|
| **Terminál** | inventory · Port: **5004** · Mailbox: `/opt/spaceos/docs/mailbox/inventory/` |
| **Aktuális commit** | `f27ac00` (INVENTORY-005: OpenConnectionAsync affinity fix) |
| **Tesztek** | **53/53 pass** |
| **VPS** | LIVE ✅ |

### TenantGucKey
```
TenantGucKey = "app.current_tenant_id"
```

### InternalEndpoints.cs — OpenConnectionAsync minta (KÖTELEZŐ)
```csharp
if (db.Database.IsRelational())
    await db.Database.OpenConnectionAsync(ct);
try {
    if (db.Database.IsRelational())
        await db.Database.ExecuteSqlRawAsync(
            "SELECT set_config('app.current_tenant_id', {0}, false)",
            tenantGuid.ToString());
    // ... EF queries and SaveChangesAsync ...
} finally {
    if (db.Database.IsRelational())
        await db.Database.CloseConnectionAsync();
}
```

---

## Stack
- .NET 8, Clean Architecture + DDD + CQRS
- PostgreSQL 16 schema: `spaceos_inventory`
- EF Core 8 + Npgsql 8.0.11

## Approved packages
MediatR 12.4.1 · FluentValidation 12.1.1 · Ardalis.Result 10.1.0 · Ardalis.Specification 8.0.0
EF Core 8.0.11 · Npgsql 8.0.11 · xUnit v3 · Moq 4.20.72 · FluentAssertions 6.12.2

A listán kívüli package hozzáadása explicit egyeztetést igényel.

## Pipeline: INBOX → CODE → BUILD → TEST → OUTBOX

### Kötelező lépések
1. `ls /opt/spaceos/docs/mailbox/inventory/inbox/` → UNREAD inbox olvasása
2. `dotnet build` → **0 error, 0 warning**
3. `dotnet test` → **minden zöld**
4. Outbox: `mailbox/inventory/outbox/YYYY-MM-DD_NNN_<slug>-done.md` · `status: UNREAD`

## Layer dependency rule
```
Domain ← Application ← Infrastructure ← Api
                                       ← Tests
```

## Naming conventions
- PascalCase: classes, methods, properties
- _camelCase: private fields
- camelCase: local variables
- CancellationToken: mindig `ct`

## Universal code rules
```csharp
await repo.GetAsync(id, ct).ConfigureAwait(false);  // ConfigureAwait(false) minden async callban
_db.PanelStocks.AsNoTracking().Where(...)           // AsNoTracking() minden read-only lekérdezésnél
```

## Security
- Minden endpoint: `[Authorize(Policy = "ManufacturerOnly")]`
- TenantId JWT-ből, nem request bodyból
- RLS: PanelStock, Offcut, StockMovement táblák tenant alapján védve
