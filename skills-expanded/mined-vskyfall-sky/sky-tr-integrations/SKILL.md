---
name: sky-tr-integrations
description: >-
  Türkiye entegrasyonları: e-Fatura/e-Arşiv, kargo (Yurtiçi, Aras, MNG, PTT), SMS ve İYS,
  iyzico/PayTR, TC kimlik, VKN, IBAN, il-ilçe, KDV. "Fatura kes", "kargo", "TC kimlik" dendiğinde
  kullan.
---

# Sky · Türkiye Entegrasyonları

Ortak kural: her entegrasyon **adaptör** arkasında (`lib/integrations/<alan>/<sağlayıcı>.ts`, ortak arayüz) →
sağlayıcı değiştirmek kolay, testte sahte adaptör. Çağrılar arka plan işinde, yeniden denemeli (bkz. `sky-jobs`).

## e-Fatura / e-Arşiv

- Mükellef (VKN'li firma) e-Fatura listesindeyse **e-Fatura**, değilse/bireyselse **e-Arşiv**. Entegratör bunu sorgular.
- Entegratörler: Paraşüt (API'si geliştirici dostu, küçük işletmelerde yaygın), BizimHesap, Logo İşbaşı, Uyumsoft, Foriba/Sovos, QNB eSolutions.
- Akış: ödeme başarılı → fatura işi kuyruğa → entegratöre müşteri + kalemler + KDV → fatura no ve PDF/UBL bağlantısı → müşteriye e-posta.
- Gerekenler: ad/unvan, VKN veya TCKN (bireyde TCKN yoksa 11111111111 kuralı entegratöre göre), adres, vergi dairesi (kurumsal), kalem, KDV oranı (%20, %10, %1, %0 istisna).
- İptal/iade faturası akışı; fatura düzenleme 7 gün kuralı (entegratör ve mali müşavirle teyit et).

## Kargo

- Doğrudan firma API'leri (Yurtiçi, Aras, MNG, Sürat, PTT) ayrı ayrı sözleşme ister; **agregatör** (Geliver, Kargonomi, Basit Kargo) tek API ile çoğuna erişim + indirimli fiyat — çoğu proje için daha iyi.
- İşlemler: fiyat teklifi (desi/ağırlık, il-ilçe), gönderi oluştur, etiket/barkod PDF (10×15), takip numarası,
  durum webhook'u (kargoya verildi → dağıtımda → teslim edildi) → müşteriye bildirim.
- Desi = (en × boy × yükseklik cm) / 3000; ağırlıkla büyük olan esas.
- Adres: il/ilçe/mahalle yapısı zorunlu (bkz. `sky-maps-geo`).
- Kapıda ödeme seçeneği ve tahsilat mutabakatı.

## SMS ve İYS

- Netgsm / İleti Merkezi / Verimor / Mutlucell: onaylı **başlık** (gönderici adı) gerekir; OTP ve bilgilendirme için ayrı başlık/paket olabilir.
- **İYS**: ticari ileti (kampanya SMS/e-posta/arama) için alıcının İYS'de onaylı olması zorunlu; onay/ret kayıtlarını İYS'ye bildir, göndermeden önce sorgula. İşlemsel mesajlar (randevu hatırlatma, OTP, sipariş durumu) kapsam dışı.
- Türkçe karakter → SMS 70 karakter/parça; maliyet için OTP'de ASCII (bkz. `sky-notifications`).

## WhatsApp Business

- Meta Cloud API veya BSP (360dialog, Twilio): onaylı **şablonlar** (randevu hatırlatma, sipariş durumu), 24 saatlik müşteri hizmetleri penceresi, butonlu mesajlar ("Onayla / Ertele").
- Türkiye'de açılma oranı SMS'ten belirgin yüksek — randevu hatırlatmada kullanıcılar sever. Kullanıcı onayı şart.

## Ödeme

iyzico (Checkout Form, taksit, alt üye işyeri), PayTR (iFrame, yaygın, uygun komisyon), Param, Craftgate (çoklu sağlayıcı yönlendirme). Ayrıntı: `sky-payments`.

## Kimlik ve vergi numarası doğrulama

```ts
export function isValidTCKN(t: string) {
  if (!/^[1-9]\d{10}$/.test(t)) return false;
  const d = t.split("").map(Number);
  const odd = d[0] + d[2] + d[4] + d[6] + d[8], even = d[1] + d[3] + d[5] + d[7];
  if (((odd * 7 - even) % 10 + 10) % 10 !== d[9]) return false;
  return d.slice(0, 10).reduce((a, b) => a + b, 0) % 10 === d[10];
}
```
- Algoritma kontrolü yalnızca biçimdir; gerçek kişi doğrulaması **NVİ KPS/MERNİS SOAP servisi** (ad, soyad, doğum yılı ile) — yalnızca gerçekten gerekiyorsa (KVKK: TCKN toplamak gerekçe ister).
- VKN (10 hane) için algoritma kontrolü + entegratörün mükellef sorgusu.
- TCKN'yi şifreli sakla, arayüzde maskele (`123******78`).

## IBAN

`TR` + 24 hane; mod-97 kontrolü (`ibantools`); banka kodu (5. – 9. haneler) ile banka adını göster ("Ziraat Bankası") — kullanıcılar bu küçük doğrulamayı sever. Ad-IBAN eşleşmesi doğrulaması bankalarda (FAST) yapılır, uygulamada değil.

## Veri setleri

- İl / ilçe / mahalle / posta kodu: açık JSON setleri (güncelliğini kontrol et), DB'ye seed.
- Resmi tatiller ve arife yarım günleri (bkz. `sky-date-time`).
- Bankalar ve EFT kodları, vergi daireleri listesi.

## Para ve vergi

- Para tam sayı kuruş; gösterim `Intl.NumberFormat("tr-TR", { style: "currency", currency: "TRY" })` → `₺1.234,50`.
- KDV: `kdv = round(net × oran)`; KDV dahil fiyattan net: `net = round(brüt / (1 + oran))` — yuvarlama farklarını satır bazında hesapla, toplamda değil (fatura ile tutarlılık).
- Fiyat gösteriminde tüketiciye KDV dahil.
