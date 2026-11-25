---
name: sky-ux-writing
description: >-
  Türkçe arayüz metni: sen/siz tutarlılığı, buton, hata, boş durum ve onay metinleri, Türkçe ek ve
  kesme işareti kuralları. "Ne yazsın bu buton", "hata mesajını düzelt" dendiğinde kullan.
---

# Sky · UX Metni

## Ses ve ton

**Ses** sabittir (markanın kişiliği): açık, saygılı, yardımcı, gereksiz süs yok.
**Ton** bağlama göre değişir:

| Bağlam | Ton | Örnek |
|---|---|---|
| Başarı | kısa, ılık | "Kaydedildi." |
| Hata (kullanıcı kaynaklı) | nötr, çözüm odaklı, suçlamasız | "E-posta adresini kontrol et: @ işareti eksik." |
| Hata (sistem) | dürüst, özürlü, yol gösterici | "Bir şeyler ters gitti. Değişikliklerin kaybolmadı; tekrar dene." |
| Yıkıcı işlem | ciddi, net | "Bu proje ve 14 dosyası kalıcı olarak silinecek." |
| Boş durum | davetkâr | "Henüz randevun yok. İlkini oluştur." |
| Onboarding | cesaretlendirici, kısa | "Harika, hesabın hazır. Şimdi ilk müşterini ekle." |

Espri yalnızca düşük riskli yerlerde (404, boş durum); hata, ödeme, veri silme yerlerinde **asla**.

## Sen / siz

Proje başında **tek karar**, her yere uygulanır (`CLAUDE.md`e yaz):
- **Sen:** tüketici ürünleri, genç kitle, samimi marka. Fiil: "Kaydet", "Devam et", "Hesabını doğrula".
- **Siz:** kurumsal, finans, sağlık, kamu, B2B. Fiil: "Kaydedin", "Devam edin", "Hesabınızı doğrulayın".
Karışım (bir ekranda "Hesabını", diğerinde "Hesabınızı") en sık görülen hatadır; grep ile ara.
Butonlar her iki durumda da **emir kipi** olabilir ("Kaydet" siz dilinde de kabul edilir; tutarlı ol).

## Butonlar

- **Fiil + nesne**, sonucu söyler: "Randevu oluştur", "Ödemeyi tamamla", "Değişiklikleri kaydet".
  ✗ "Gönder", "Tamam", "Evet", "Devam" (bağlamsız).
- Birincil buton eylemi, ikincil "İptal"/"Vazgeç". Yıkıcı: "Sil", "Kaldır" (kırmızı, sağ veya ayrık).
- Uzunluk: ≤ 3 kelime, ≤ ~20 karakter (Türkçe uzar; 375px'te iki buton yan yana sığmalı).
- Yükleniyor: "Kaydediliyor…" (üç nokta tek karakter `…`), buton genişliği sabit.
- Bağlantı metni hedefi söyler: "Fiyatlandırmayı gör" ✓, "buraya tıkla" ✗.
- Sentence case: "Değişiklikleri kaydet" ✓, "Değişiklikleri Kaydet" ✗ (başlık yazımı yalnızca marka/özel ad).

## Hata ve doğrulama mesajları

Formül: **ne oldu + nasıl düzelir** (gerekirse neden). Alanın altında, alan adını tekrar etmeden.
```
✗ Geçersiz giriş.
✗ Telefon alanı hatalı.
✓ Cep telefonu 05 ile başlayıp 11 hane olmalı.
✓ Bu e-posta zaten kayıtlı. Giriş yapmayı dene veya parolanı sıfırla.
✓ Parola en az 8 karakter olmalı.
```
- Teknik terim yok: "422", "null", "token", "sunucu hatası" kullanıcıya söylenmez.
- "Lütfen" her cümlede değil; nadiren, yumuşatma gerektiğinde.
- Ünlem yok. Büyük harfle bağırma yok.
- Sistem hatasında veri kaybı olmadığını söyle (doğruysa) ve tekrar dene seçeneği ver.
- Yetki hatası: "Bu sayfayı görüntüleme yetkin yok. Erişim için yöneticine yaz." (varlığı gizlemek gerekiyorsa 404 metni).
- Çevrimdışı: "İnternet bağlantın yok. Bağlanınca değişikliklerin gönderilecek."

## Boş durumlar

Üç parça: **ne burada olur** + **neden boş / değeri ne** + **ilk eylem**.
```
Başlık:   Henüz fatura yok
Açıklama: Oluşturduğun faturalar burada listelenir ve ödeme durumlarını takip edebilirsin.
Eylem:    [Fatura oluştur]
```
Filtre sonucu boşsa farklı: "Aramanla eşleşen fatura yok. [Filtreleri temizle]".
İlk kullanımda yardım bağlantısı veya örnek veri yükleme seçeneği değerli.

## Onay diyalogları

- Başlık soru veya eylem: "Projeyi silmek istiyor musun?" / "Projeyi sil".
- Gövde: **ne silinecek, geri alınabilir mi, etkisi**. Nesnenin adını yaz: "«Kaset Odası» projesi ve 14 dosyası kalıcı olarak silinecek."
- Butonlar: eylem fiili + vazgeç — "Sil" / "Vazgeç". **Evet/Hayır asla.**
- Yüksek risk: adı yazdır ("Onaylamak için proje adını yaz").
- Geri alınabilir işlemler için diyalog yerine **toast + Geri al** daha iyi.

## Yükleniyor, başarı, bilgi

- Yükleniyor ≥ 1 sn sürecekse metin: "Rapor hazırlanıyor… bu birkaç saniye sürebilir."
- Başarı toast'ı 2–5 kelime, geçmiş zaman: "Randevu oluşturuldu.", "Bağlantı kopyalandı." Opsiyonel eylem: "Görüntüle".
- Toast'ta soru sorma, kritik bilgi verme (kaybolur); kritikse inline.
- İlerleme: adım sayısı "Adım 2/4 · Ödeme bilgileri".

## Form metinleri

- **Etiket:** kısa isim, iki nokta yok: "E-posta", "Cep telefonu", "Doğum tarihi".
- **Yardım metni:** etiketin altında, neden/biçim: "Randevu hatırlatmaları bu numaraya gönderilir."
- **Placeholder:** yalnızca örnek biçim ("05xx xxx xx xx"), etiket değil; kaybolur.
- **Zorunluluk:** çoğunluk zorunluysa "(isteğe bağlı)" yaz; yıldız kullanıyorsan formun başında açıkla.
- **Onay kutuları:** birinci tekil kişi: "Kampanya e-postaları almak istiyorum." Yasal: "[KVKK Aydınlatma Metni]'ni okudum."
- **Seçenek etiketleri** paralel yapıda: "Aylık / Yıllık", "Hemen / Daha sonra".

## Onboarding ve ipuçları

- Her adım bir şey öğretir; 3 adımı geçme. "Atla" her zaman var.
- Değeri söyle, özelliği değil: ✗ "Takvim entegrasyonu" ✓ "Randevuların takvimine otomatik eklenir."
- Tooltip ≤ 1 cümle; ikon butonlarında eylem adı ("Düzenle").

## Bildirim ve e-posta

- Push/bildirim: ≤ 50 karakter, en önemli bilgi başta, kişisel veri yok (kilit ekranı). "Siparişin kargoda: 2 gün içinde sende."
- E-posta konusu: ≤ 50 karakter, ne olduğunu söyler, clickbait yok: "Randevun onaylandı: 5 Kasım 14:30".
- Ön başlık (preview) konuyu tamamlar, tekrarlamaz.
- İşlemsel e-postada tek CTA.

## 404 ve sistem sayfaları

- 404: "Bu sayfa yok ya da taşındı." + arama/ana sayfa bağlantısı; hafif espri olabilir.
- 500: dürüst, "Üzerinde çalışıyoruz" yalnızca doğruysa; durum sayfası bağlantısı.
- Bakım: ne zaman biteceği (saat dilimiyle).

## Türkçe tuzakları

- **Ek + özel ad:** kesme işareti: "Ayşe'nin", "İstanbul'da"; **dinamik değerlere ek getirme** ("{name}'ın" → Ayşe'ın ✗). Cümleyi çevir: "Ayşe için sipariş", "Sipariş sahibi: Ayşe".
- **Çoğul:** sayıdan sonra tekil: "3 dosya" ✓ "3 dosyalar" ✗. Belirsiz sayıda "dosyalar".
- **Büyük İ / küçük ı:** CSS `text-transform` ve JS `toUpperCase` locale'siz bozar (bkz. `sky-i18n`); metni zaten doğru halde yaz.
- **Kısaltmalar:** "vb.", "örn.", "dk", "sn" — "dk." noktalı değil (TDK: dk). Para: "₺1.250" veya "1.250 TL" tek biçim.
- **Tarih:** "5 Kasım 2026, Perşembe", saat "14:30"; "Kasım 5" ✗.
- **Anglisizm:** "Submit et" ✗ "Gönder"; "Login" ✗ "Giriş yap"; "Cancel" ✗ "Vazgeç/İptal"; "Settings" ✗ "Ayarlar"; "Dashboard" → "Panel" (marka terimiyse kalabilir).
- **Bağlaç "de/da"** ayrı; "ki" ekleri: "halbuki, oysaki, çünkü, sanki" bitişik.
- **Noktalama:** cümle sonu nokta; başlıklarda ve buton/etiketlerde nokta yok; madde listelerinde tutarlı.
- **"Lütfen", "başarıyla", "!"** → çoğu zaman gereksiz; sil.

## Uzunluk rehberi

| Öğe | Sınır |
|---|---|
| Buton | ≤ 20 karakter |
| Başlık (sayfa) | ≤ 40 |
| Toast | ≤ 60 |
| Hata mesajı | ≤ 90, tek cümle (iki gerekirse ikincisi çözüm) |
| Boş durum açıklaması | ≤ 140 |
| Tooltip | ≤ 80 |
| Push | ≤ 50 |

## Kontrol listesi

- [ ] Sen/siz tutarlı (grep: "ınız|iniz|unuz|ünüz" vs "ın|in|un|ün")
- [ ] Butonlar fiil + nesne; Evet/Hayır/Tamam yok
- [ ] Hata = ne oldu + nasıl düzelir; teknik terim yok
- [ ] Dinamik değere ek getirilmiyor
- [ ] Sentence case; gereksiz ünlem/"lütfen"/"başarıyla" yok
- [ ] Boş durumlarda eylem var
- [ ] 375px'te metinler taşmıyor (Türkçe uzunluğu test edildi)
