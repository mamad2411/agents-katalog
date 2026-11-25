---
name: nsai-online
description: Trigger für den vollständigen Online-Sync und Key-Wechsel der NSAI-Anbindung — primär die nsai-edge-Bridge dieses Plugins (Default-Hub nsai.bittransit.io/mcp), sekundär die Symfony-App-Seite (app:nsai:online). Use bei „Online-Verbindung prüfen/einrichten", „voll synchronisieren", „Key ändern/ungültig", „Sync hängt", „NSAI offline/online".
---

# nsai-online — Online-Sync auslösen & Key pflegen

Zwei Ebenen, klar trennen:

1. **nsai-edge-Bridge (dieses Plugin, Claude-Code-seitig)** — der lokale Wissensgraph
   synct mit dem zentralen Hub im **Direktzugriff**. **Default ohne Konfiguration:** `https://nsai.bittransit.io/mcp`
   mit dem geteilten **„Extern"-Key** (Low-Trust: serverseitig Quarantäne/Arbitrierung +
   Rate-Limit). **Write-Through:** jeder Schreib-Tool-Aufruf reiht die Aussage sofort in eine
   **durable lokale Outbox** ein und stellt sie direkt zu. Ist der Hub offline, bleibt sie
   gepuffert (kein Verlust) und wird beim nächsten Write/Intervall (10 min)/MCP-Start
   **deterministisch + idempotent** (per `triple_hash`) nachgeliefert. Lokal bleibt immer die Wahrheit.
2. **Symfony-App-Seite** (rocket-launch-nsai-Installation) — deren eigener Backlog-Sync
   zum konfigurierten Online-Store (`app:nsai:online`).

## Key-Regel (fest verdrahtet, kein Eingriff nötig)

**Leerer oder ungültiger Key ⇒ immer Fallback auf das Default-Paar (Hub + Extern-Key).**
- Leer: `bridgeConfig()` setzt automatisch den Default ein.
- Ungültig (401/403): `bridgeSync()` probiert den eigenen Key read-only (`probeKey`),
  fällt bei Ablehnung aufs Default-Paar zurück und meldet das auf stderr — der Sync
  läuft IMMER weiter. Nicht-Erreichbarkeit ist KEIN Key-Fallback (kein Falschalarm).

## Vollständigen Sync auslösen (der Trigger dieses Skills)

```bash
# Im Plugin-Verzeichnis (nsai-edge/) — Push eigener Fakten + Pull Online-Diff:
node bin/nsai-edge.mjs bridge
```

Ausgabe interpretieren: `push.pushed` (hochgeladene eigene Fakten), `pull.added`
(neu übernommene Hub-Fakten), `fallback: true` = eigener Key wurde abgelehnt und
der Default griff (→ Key prüfen/neu setzen, siehe unten).

## Eigenen Key einrichten / wechseln

Eigener Informant statt geteiltem Extern-Key (empfohlen für zuordenbare Beiträge):
1. Key in der App erzeugen: `https://nsai.bittransit.io/account/source` (einmalig sichtbar).
2. Für den MCP-Server setzen — je nach Setup:
   - **Shell/Session:** `export NSAI_APP_KEY="<bearer>"` (gilt für neu gestartete MCP-Server)
   - **Dauerhaft (Claude Code):** in `~/.claude/settings.json` unter `env`:
     `"NSAI_APP_KEY": "<bearer>"`
3. Verifizieren: `node bin/nsai-edge.mjs bridge` → `fallback` darf NICHT true sein.

Weitere Schalter: `NSAI_APP_ENDPOINT="https://host/mcp"` (eigener Server),
`NSAI_APP_ENDPOINT=off` (komplett offline, Bridge aus).

## Symfony-App-Seite (sekundär)

Auf einer rocket-launch-nsai-Installation pflegt das Konsolen-Kommando die dortige
Online-Verbindung (im App-Verzeichnis, read-only zuerst):

```bash
php bin/console app:nsai:online            # Status: Opt-In, Endpunkt, Backlog-Größe
php bin/console app:nsai:online --test     # Erreichbarkeit + Key-Gültigkeit
php bin/console app:nsai:online --endpoint="https://host/mcp" --key="<bearer>"   # ändern (Operator-Freigabe)
php bin/console app:nsai:online --flush    # Backlog jetzt schieben (Cron: app:nsai:sync)
```

- `--test: 401` → Key dort neu setzen; nicht erreichbar → Endpunkt/Netz, System fällt
  automatisch offline zurück (Backlog wächst, kein Datenverlust).
- Async-Versand braucht den Worker (`messenger:consume async`), Backlog-Flush den Cron —
  im Docker-Setup eigene Compose-Services (`nsai_worker`, `nsai_cron`).

## Leitplanken
- Schreibende Änderungen (Key/Endpunkt setzen) nur nach Operator-Freigabe.
- Keys niemals im Klartext loggen/committen; Status-Ausgaben maskieren.
- Bei „Sync hängt": erst Verbindung testen, dann voller Sync, dann Worker-Status — in dieser Reihenfolge.
