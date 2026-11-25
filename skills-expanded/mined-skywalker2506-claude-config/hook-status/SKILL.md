---
name: hook-status
description: SessionStart hook'larinin calisip calismadigini kontrol et — success/fail/skip ozeti goster.
---

## /hook-status

Bu session'da hangi SessionStart hook'larinin calistigini raporla.

## Uygulama

Baska hicbir sey yapma. Sadece bu session'in basinda gelen `system-reminder` mesajlarindan
`SessionStart:resume hook success:` ile baslayanlari listele.

Her satir icin:
- Mesaj geldiyse: ✅ `HOOK_ADI` — cikti (ilk 80 karakter)
- Mesaj gelmediyse: ❌ `HOOK_ADI` — tetiklenmedi

## Beklenen hook'lar (settings.json sirasinda)

1. `JARVIS_MODEL` — model adi ve emoji
2. `PROJECT_INDEX` — proje index guncelleme (silent if no index.md)
3. `REPORTS_CHECK` — bekleyen rapor sinyali (silent if none)
4. `GRAPH_CACHE_STALE` — cache > 7 gun ise uyari (silent otherwise)
5. `SESSION_SYNC` — claude-config sync
6. `JARVIS_POLICY` — politika mesaji

Not: `AVAILABLE_SECRETS` ve `MCP_ACTIVE` artik auto-inject degil — `/harness-status` on-demand.

## Rapor Formati

```
=== SessionStart Hook Durumu ===
✅ JARVIS_MODEL     — claude-sonnet-4-6 🔶
⚪ PROJECT_INDEX    — silent (no index.md)
⚪ REPORTS_CHECK    — silent (no pending)
⚪ GRAPH_CACHE      — silent (fresh / absent)
✅ SESSION_SYNC     — ok
✅ JARVIS_POLICY    — Sen implementer degilsin...

6 hook tanimli — 2 ✅  4 ⚪  0 ❌
```

Ekstra aciklama YAZMA. Sadece tablo + ozet satir.
