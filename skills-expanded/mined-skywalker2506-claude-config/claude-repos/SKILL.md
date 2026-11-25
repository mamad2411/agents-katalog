---
name: claude-repos
description: "Claude ile ilgili tüm GitHub repolarını listele — ccplugin-*, claude-*, marketplace. Triggers: claude repos, claude repoları, plugin repoları, hangi repolar var, github repoları."
argument-hint: "[]"
---

# /claude-repos — Claude GitHub Repo Listesi

`mcp__github__search_repositories` ile SkyWalker2506 hesabındaki Claude-related repoları listele.

## Akış

1. Şu pattern'leri ara (owner: SkyWalker2506):
   - `ccplugin-` prefix'li repolar
   - `claude-` prefix'li repolar

2. Her repo için: isim, description, son push tarihi, star sayısı

3. Kategorilere göre grupla:

```
## 🔌 Plugins (ccplugin-*)
| Repo                        | Açıklama                  | Son Push  |
|-----------------------------|---------------------------|-----------|
| ccplugin-notifications      | Ses + macOS bildirimi     | 2 saat önce |
| ccplugin-telegram           | Telegram bot bridge       | ...       |
| ...                         |                           |           |

## 🧠 Core (claude-*)
| Repo                        | Açıklama                  | Son Push  |
|-----------------------------|---------------------------|-----------|
| claude-config               | Ana config + agent OS     | ...       |
| claude-marketplace          | Plugin registry           | ...       |
| claude-agent-catalog        | 134 agent tanımları       | ...       |
```

## Kurallar
- Max 5 tool call
- Sıralama: son push tarihi (yeni → eski)
- Arşivlenmiş repolar en alta

## When NOT to Use
- Tek satirlik basit soru/cevap ise
- Skill'in scope'u disindaysa
- Riskli/destructive is ise (ayri onay gerekir)

## Red Flags
- Belirsiz hedef/kabul kriteri
- Gerekli dosya/izin/secret eksik
- Ayni adim 2+ kez tekrarlandi

## Error Handling
- Gerekli kaynak yoksa → dur, blocker'i raporla
- Komut/akıs hatasi → en yakin guvenli noktadan devam et
- 3 basarisiz deneme → daha uygun skill/agent'a yonlendir

## Verification
- [ ] Beklenen cikti uretildi
- [ ] Yan etki yok (dosya/ayar)
- [ ] Gerekli log/rapor paylasildi
