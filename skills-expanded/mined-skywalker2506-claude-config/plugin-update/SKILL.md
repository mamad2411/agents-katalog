---
name: plugin-update
description: "Kurulu plugin'leri güncelle. Triggers: plugin update, plugin güncelle, pluginleri güncelle, update plugins"
---

# /plugin-update

Kurulu plugin'leri GitHub'dan günceller.

## Kullanım
- `/plugin-update` — tüm plugin'leri güncelle

## Akış
1. `config/plugin-update.sh` çalıştır
2. Sonucu raporla

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
