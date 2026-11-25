---
name: sky-code-review
description: >-
  Kod incelemesi (review) yapma ve alma: neye bakılır (doğruluk, güvenlik, veri kaybı, yetki,
  performans, test, okunurluk, kapsam), öncelik sırası, yorum yazma dili ve önem etiketleri
  (blocker/öneri/nit), küçük PR kültürü, kendi PR'ını gözden geçirme listesi, otomatik
  kontrollere bırakılacaklar, AI ile üretilmiş kodu inceleme ve geri bildirimi karşılama.
  "Kodu incele", "PR review", "bu değişiklik iyi mi" dendiğinde kullan.
disable-model-invocation: true
---

# Sky · Kod İncelemesi

## Öncelik sırası (yukarıdan aşağı, zaman bitince dur)

1. **Doğruluk**: istenen şeyi yapıyor mu? Kenar durumlar (boş, null, eşzamanlılık, saat dilimi, büyük veri, Türkçe karakter)?
2. **Güvenlik ve veri**: yetki kontrolü (IDOR), girdi doğrulama, sır sızıntısı, veri kaybı riski (yıkıcı migration, silme), geri alınabilirlik.
3. **Hata yolları**: hatalar yutuluyor mu, kullanıcı ne görüyor, yeniden deneme/idempotency.
4. **Testler**: davranışı test ediyor mu, hata düzeltmesinde regresyon testi var mı.
5. **Performans**: N+1, döngüde ağ çağrısı, gereksiz render, büyük bundle.
6. **Tasarım ve okunurluk**: isimler, sorumluluklar, gereksiz soyutlama/tekrar, projenin kalıplarına uyum.
7. **Biçim/stil**: linter/formatter'ın işi — insan yorumu harcama.

## Nasıl okunur

- Önce PR açıklaması ve bağlantılı iş (neyi çözüyor?), sonra testler (beklenen davranış), sonra kod.
- Büyük PR (> 400 satır mantık) → bölünmesini iste; dikkatli inceleme küçük PR'da mümkündür.
- Diff'te olmayanı da düşün: "bu fonksiyonu çağıran diğer yerler etkilendi mi?" (grep).
- Gerekirse dalı çek ve çalıştır (UI değişikliğinde mutlaka).

## Yorum dili

Önem etiketi + gözlem + neden + öneri:
```
[blocker] Bu uç noktada orgId kontrolü yok; başka org'un randevusunu id ile iptal edebilirim.
  Öneri: bookingService.cancel içinde membership kontrolü (diğer uç noktalardaki gibi).
[öneri] Bu sorgu her satır için client çekiyor (N+1). `with: { client: true }` ile tek sorgu olur.
[nit] `data2` yerine `upcomingBookings` daha açıklayıcı.
[soru] Hatırlatma iptal edilen randevu için de gidiyor mu? Testte göremedim.
[övgü] Slot hesaplamasını saf fonksiyona çıkarman testleri çok kolaylaştırmış 👍
```
- Kişiyi değil kodu konuş ("bu fonksiyon…", "sen yanlış yapmışsın" değil).
- Soru sor, varsayma. Övgü de yaz — neyin iyi olduğunu bilmek de öğreticidir.
- `nit`ler engellemez; blocker'ları netleştir.

## Kendi PR'ın için (göndermeden önce)

- [ ] Diff'i kendin baştan sona okudun (debug kodu, yorum satırı, TODO, alakasız değişiklik yok)
- [ ] Başlık ve açıklama: ne, neden, nasıl test edildi, risk/geri alma
- [ ] Testler eklendi ve yeşil; UI ise ekran görüntüsü/video (375px dahil)
- [ ] Migration varsa geriye uyumlu, ayrı belirtildi
- [ ] Yeni env/flag/bağımlılık belirtildi
- [ ] `/sky-check` GEÇTİ

## AI ile yazılmış kodu incelerken

Ekstra dikkat: var olmayan API/paket (halüsinasyon), aşırı genel hata yakalama, gereksiz soyutlama katmanları, projenin kalıplarını
görmezden gelen yeni kalıplar, test edilmeden "çalışıyor" iddiası, sessizce değiştirilmiş davranış, gereksiz bağımlılık.
Kodun her satırını açıklayabiliyor musun? Açıklayamıyorsan birleştirme.

## Geri bildirim alırken

Savunmaya geçme; anlamadığın yorumu sor; katılmıyorsan gerekçeyle konuş, karar verilemiyorsa üçüncü kişiye/ADR'ye taşı.
Her yorumu çöz veya cevapla; "düzeltildi: abc123" ile commit bağla.

## Otomasyon

İnsanın değil makinenin işi: format, lint, tip, testler, bağımlılık açıkları, bundle boyutu farkı, kapsam düşüşü, sır taraması (bkz. `sky-github-actions`).
Sky agent'ları: `sky-code-reviewer` (genel), `sky-security-reviewer`, `sky-db-reviewer`, `sky-ui-reviewer`.
