---
name: bitir
description: Üzerinde çalışılan docs/PLAN.md maddesini kapatır - testleri çalıştırır, planı işaretler, commit atar ve tek satır özet verir.
disable-model-invocation: true
argument-hint: "(boş) | <commit mesajı>"
---

# Maddeyi kapat

Bir `docs/PLAN.md` maddesi bittiğinde çalışır. Amaç: her seferinde elle "testleri çalıştır, planı işaretle, commit at" demeyi ortadan kaldırmak.

## Sıra

**1. Doğrula**

`CLAUDE.md` içindeki doğrulama matrisine bak, değişiklik türüne göre **minimum gerekli** testi çalıştır.
Değişiklik birden fazla kategoriye giriyorsa, en geniş olanı uygula.

Test kırılırsa: **dur, commit atma.** Çıktıyı göster ve sor.

**2. Planı güncelle**

`docs/PLAN.md`'de ilgili maddeyi `- [x]` yap. Plan dışına çıkılan bir şey yapıldıysa plana yeni madde olarak ekle — sessizce geçme.

**3. Sır kontrolü**

Commit'lenecek dosyalarda sır var mı bak: `.env`, API anahtarı, parola, token.
Şüphe varsa **commit atma**, sor. (Repo açık kaynak olacak.)

**4. Commit**

- Dosyaları **adıyla** ekle — `git add -A` / `git add .` yasak
- Mesaj Türkçe, tek satır. `$ARGUMENTS` verilmişse onu kullan, verilmemişse maddeden türet
- İlgili plan maddesi varsa gövdeye yaz: `PLAN 2.3`
- Sonuna: `Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>`
- `git push` **yapma** — kullanıcı ayrıca söylemeli

**5. Özet**

Tek blok, fazlası yok:

```
Kapatıldı: <madde no> <başlık>
Doğrulandı: <çalıştırılan test, sonuç>
Commit: <kısa hash> <mesaj>
Sıradaki: <docs/PLAN.md'deki bir sonraki işaretsiz madde>
```

## Kural

Yaptığın işi burada tekrar anlatma — zaten yapılırken anlatıldı. Sadece kapanış bilgisi.
