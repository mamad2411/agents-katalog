---
name: ilerle
description: docs/PLAN.md'deki sıradaki maddeyi rapor vermeden doğrudan uygulamaya başlar. /durum'un sessiz hâli.
disable-model-invocation: true
---

# İlerle

`/durum` ile aynı işi yapar, **ama durum raporu vermez.** Kullanıcı nerede kalındığını zaten biliyor, sadece devam edilmesini istiyor.

## Akış

1. `docs/PLAN.md`'yi oku, ilk işaretsiz `- [ ]` maddeyi bul
2. Tek satır söyle: `Başlıyorum: <madde no> <başlık>`
3. Uygula — `CLAUDE.md` çalışma döngüsü ve doğrulama matrisine göre
4. Bitince `docs/PLAN.md`'de kutuyu işaretle, kısa çıktı formatıyla bitir

## İstisna

`/durum`'daki onay listesi burada da geçerli: migration, silme, geniş refactor, yetkilendirme değişikliği, bağımlılık, deploy → **önce sor.**

## Kural

Giriş cümlesi, özet, plan anlatımı yok. Tek satır "başlıyorum", sonra iş.
