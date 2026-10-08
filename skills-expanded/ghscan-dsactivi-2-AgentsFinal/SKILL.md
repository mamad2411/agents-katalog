---
name: Publisher
description: Post-Veröffentlichung via Postiz
---
## Modell: ollama/gemini-3-flash-preview:cloud
# SKILL: Publisher — Post-Veröffentlichung via Postiz

## Aktivierung

Dieser Skill wird aktiviert durch:
- Übergabe von SKILL:reviewer nach Freigabe (🟢)
- Direkte Anfragen: "Veröffentliche den Post", "Plane den Post für..."
- Geplante Posts die ihren Veröffentlichungszeitpunkt erreichen

## Postiz-Integration

### API-Konfiguration

Postiz läuft lokal oder als Docker-Container:
- **URL:** `http://127.0.0.1:4200` (Standard)
- **API:** REST API mit Bearer Token

### Workflow

1. **Post-Daten vorbereiten:**
   - Caption (aus Writer-Output)
   - Hashtags anhängen
   - Medien-URLs (falls Bilder/Videos)
   - Plattform wählen (Instagram / Facebook)
   - Posting-Zeit setzen

2. **Postiz API aufrufen:**
   ```
   POST /api/posts
   {
     "platform": "instagram",
     "content": "[Caption + Hashtags]",
     "media": ["url1", "url2"],
     "scheduledAt": "2026-03-16T09:00:00Z"
   }
   ```

3. **Bestätigung erhalten:**
   - Post-ID speichern
   - Geplanten Zeitpunkt bestätigen
   - In Memory loggen

### Direkt-Posting vs. Geplantes Posting

**Direkt:** Wenn Posting-Zeit = jetzt (oder < 15 Minuten)
**Geplant:** Wenn Posting-Zeit in der Zukunft → Postiz übernimmt Scheduling

## Output-Format

```markdown
## Publishing-Ergebnis

**Status:** ✅ Veröffentlicht / 📅 Geplant / ❌ Fehler

**Post-ID:** [Postiz-ID]
**Plattform:** [Instagram/Facebook]
**Geplant für:** [Datum + Uhrzeit]
**Inhalt (Vorschau):** [Erste 100 Zeichen...]

**Memory-Log:** Gespeichert unter [post-id]
```

## Fehlerbehandlung

Bei API-Fehler:
1. Log Fehler mit Details in Memory
2. Retry nach 5 Minuten (max. 3 Versuche)
3. Bei dauerhaftem Fehler: Eskalation + manuelle Prüfung

## Media-URL Validierung (Pflicht vor Posting)

Bevor Medien an Postiz übergeben werden, **jede URL prüfen**:

### Checkliste

| Prüfpunkt | Erwartung | Aktion bei Fehler |
|-----------|-----------|-------------------|
| URL erreichbar | HTTP 200 | Bild neu hochladen oder URL korrigieren |
| Content-Type | `image/jpeg`, `image/png`, `image/webp`, `video/mp4` | Format ablehnen, Agent informieren |
| Dateigröße | Bilder < 8 MB, Videos < 100 MB | Komprimierung anfordern |
| URL-Schema | `https://` (kein `http://`) | URL ablehnen |
| Verfallszeit | Keine ablaufenden URLs (z.B. Meta CDN `_nc_` params) | Bild lokal speichern + eigene stabile URL verwenden |

### Implementierung (OpenClaw Tool-Call Beispiel)

```
# 1. URL-Check
GET {media_url} → prüfe Status, Content-Type, Content-Length

# 2. Falls Meta CDN URL (facebook.com, fbcdn.net, cdninstagram.com):
#    → Bild über meta-bridge /images/{path} abrufen (lokal gespeichert)
#    → Oder: direkt aus IMAGE_STORAGE_DIR lesen

# 3. Postiz Upload (falls lokale Datei):
POST http://127.0.0.1:4200/api/uploads
Content-Type: multipart/form-data
→ Erhalte stabile Postiz-interne URL

# 4. Dann erst: POST /api/posts mit validierter URL
```

### Fehlercodes

- `media_url_unreachable` → Bild neu generieren lassen (SKILL:writer)
- `media_url_wrong_type` → Format nicht unterstützt, ablehnen
- `media_url_too_large` → Komprimierung oder Alternativ-Bild anfragen
- `media_url_insecure` → HTTP statt HTTPS, ablehnen

## Qualitätssicherung beim Publishing

- Nochmals prüfen: Ist Reviewer-Freigabe vorhanden?
- Kein Publishing ohne `status: "approved"` in Memory
- Medien-URLs **immer validieren** (siehe oben) bevor Postiz-Aufruf
- Bei Zweifeln: SKILL:reviewer erneut aufrufen

## Memory-Nutzung

```
memory_search("postiz api token") → API-Credentials
memory_search("publishing log") → Letzte Veröffentlichungen
```

Nach erfolgreichem Posting:
```
Speichere: "Post [ID] veröffentlicht [Plattform] [Datum] [Uhrzeit] — [Caption-Preview]"
```
