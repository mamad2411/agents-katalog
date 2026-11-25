---
name: sky-ethical-ux
description: >-
  Dürüst tasarım: dark pattern'lerden kaçınma, kolay iptal, dürüst çerez bandı; Tüketici Kanunu, KVKK
  ve ETK açısından riskli kalıplar. "İptal akışı", "çerez bandı" dendiğinde kullan.
---

# Sky · Etik UX

Kısa vadede dönüşümü artıran karanlık kalıplar uzun vadede güveni, yorumları ve hukuki güvenliği yer.
Sky'ın kuralı: **kullanıcının bilseydi istemeyeceği hiçbir şey**. Kullanıcı bu tür bir kalıp isterse
riskini açıkla ve dürüst alternatif öner.

## Kaçınılacaklar → yerine

| Karanlık kalıp | Dürüst alternatif |
|---|---|
| Ödemenin son adımında çıkan "hizmet bedeli" | Toplam fiyat ilk andan görünür |
| Sahte geri sayım / "son 2 ürün" (gerçek değilse) | Gerçek stok/kampanya bitişi veya hiçbiri |
| Ön işaretli pazarlama onayı | Boş onay kutusu, açık metin |
| "Hayır, indirim istemiyorum, param bana yeter" (utandırma) | Nötr "Hayır, teşekkürler" |
| Gri, küçük, gizli "Reddet" | Kabul ve Reddet eşit görünür |
| İptal için telefon/e-posta zorunluluğu | Kaydolduğu kadar kolay iptal (tek akış, ≤ 3 adım) |
| Deneme sonunda habersiz ücretlendirme | Bitişten 3 gün önce hatırlatma e-postası |
| Gizli otomatik yenileme | Yenileme tarihi ve tutarı ayarlarda ve e-postada açık |
| Sürekli bildirim izni isteme | Bağlamlı, bir kez, "şimdi değil" saygılı |
| Hesap silmeyi gizlemek | Ayarlar → Hesap → "Hesabı sil" görünür |
| Sepete gizlice eklenen sigorta/ek ürün | Açık seçim, varsayılan seçili değil |
| Karşılaştırmayı zorlaştıran fiyat sunumu | Birim fiyat, net özellik tablosu |

## Abonelik iptal akışı (dürüst ama akıllı)

1. Ayarlar → Plan → **"Aboneliği iptal et"** (görünür).
2. Tek ekran: "İptal edersen 15 Aralık'a kadar erişimin sürer." + isteğe bağlı neden seçimi.
3. **Bir** alternatif teklif (gerçekten faydalıysa): "Duraklat (3 ay)" veya "Daha uygun plana geç" — reddetmesi tek tık.
4. Onay → anında onay e-postası. Geri dönüş kolay ("İptali geri al").
Neden verisi ürünü geliştirir; duraklatma seçeneği iptallerin bir kısmını dürüstçe kurtarır.

## Çerez onayı

"Kabul et" / "Reddet" / "Tercihler" — eşit ağırlık; reddedince zorunlu dışı scriptler yüklenmez; seçim kalıcı ve
footer'dan değiştirilebilir. En iyisi: çerezsiz analitikle banta hiç gerek bırakmamak (bkz. `sky-privacy-engineering`).

## Bildirim ve izinler

Önce değeri açıkla ("Randevun yaklaşınca haber verelim mi?"), sonra tarayıcı izni; reddedeni tekrar tekrar rahatsız etme;
ayarlardan açılabilir olsun.

## Aciliyet ve kıtlık

Yalnızca **gerçekse**: gerçek kampanya bitiş tarihi, gerçek stok, gerçek kontenjan. Gerçek değilse kullanma.
Sosyal kanıt da gerçek olmalı ("Bugün 12 kişi rezervasyon yaptı" — veriden).

## Hukuki not (Türkiye)

Tüketicinin Korunması Hakkında Kanun ve ilgili yönetmelikler (mesafeli sözleşmeler, haksız ticari uygulamalar,
abonelik sözleşmelerinde kolay fesih), KVKK (açık rıza serbest iradeyle), Elektronik Ticaret Kanunu (ticari ileti onayı, İYS)
birçok karanlık kalıbı açıkça risk hâline getirir. Kesin değerlendirme için hukukçu — ama tasarım tarafında dürüst olan genelde güvenli olandır.

## Güven inşa eden detaylar

- "Kartın istenmez", "İstediğin zaman iptal", "Verilerini dışa aktarabilirsin" — net taahhütler.
- Fiyat artışında önceden bildirim ve eski fiyatı bir süre koruma.
- Hataları kabul eden durum sayfası ve postmortem'ler.
- İnsanlar dürüst ürünleri arkadaşlarına önerir — en ucuz büyüme kanalı.
