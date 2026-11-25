---
name: fast-track
description: Basit görevler (yazım hatası, renk değişimi, ufak linter hataları) için 7 adımlık devasa pipeline'ı atlayan "hızlı yol" skill'i. ATDD, plan ve test yazımını atlar. Kodu yazar, verify (linter/format) çalıştırır ve commit atar.
---

# Fast-Track Skill

Bu skill, sadece çok küçük, düşük riskli, test yazılmasını veya mimari karar alınmasını gerektirmeyen (örneğin UI'da bir renk değişimi, bir yazım hatası, basit bir import düzeltmesi) görevler için kullanılır.

## Destek Skiller
- `caveman`, `ponytail` — temel davranışlar geçerli.
- `verify` — sadece Gate 4, 5 ve 6 (Linter, Type-Check, Format) çalıştırılır. Test (Gate 8/9) atlanır.

## Adımlar

1. **Doğrudan Yazım:** Kullanıcının istediği ufak değişikliği anla ve (ATDD/Plan/Test sormadan) **kodu doğrudan kendin yaz** (veya `Agent` alt-ajanıyla yaz).
2. **Kapsam Daraltma:** Değişikliğin KESİNLİKLE sadece istenen ufak yerle sınırlı kaldığını doğrula. Başka dosyalara dokunma.
3. **Verify (Hızlı Doğrulama):** Projedeki tip/linter/format kontrollerini (`verify` skill'i üzerinden sadece ilgili gate'leri veya doğrudan komutları) çalıştır. Eğer projenin CI'ı kırılmıyorsa devam et.
4. **Kullanıcı Onayı ve Commit:** 
   Değişen kodların diff'ini kullanıcıya göster: *"Değişikliği yaptım. Doğrulamadan geçti. Commit atayım mı?"* diye sor.
   Kullanıcı "evet" derse `commit` skill'ini çağırarak süreci tamamla.

## Kural
- Verilen görev "fast-track" sınırlarını aşıyorsa (ör. "yeni bir API endpoint ekle", "veritabanı şemasını değiştir"), kullanıcıyı uyararak "Bu iş fast-track ile yapılamaz, tam ATDD pipeline'ına dönüyorum" de ve süreci iptal et.
- Supabase tablolarına veya auth mekanizmasına dokunan HİÇBİR KOD fast-track ile yazılmaz.
