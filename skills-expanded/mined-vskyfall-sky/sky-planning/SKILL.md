---
name: sky-planning
description: >-
  Geliştirici için iş planlama: belirsiz isteği netleştirme, işi dikey dilimlere bölme,
  bağımlılık ve risk sıralaması (en riskli önce), her adım için "bitti" tanımı, tahmin verme
  (aralıklarla, belirsizlik payıyla), MVP kesme, spike (keşif) ile belirsizliği azaltma,
  plan dosyası şablonu ve planı güncel tutma. "Nasıl başlayayım", "planla", "bu ne kadar sürer",
  "işi böl" dendiğinde kullan.
disable-model-invocation: true
---

# Sky · Planlama

Ürün düzeyinde PRD için `sky-product-manager` yöntemi, mimari için `sky-architect`. Bu skill **uygulama planı** içindir.

## 1. Netleştir (5 soru)

1. Kim kullanacak, hangi durumda? 2. Başarı neye benziyor (gözlemlenebilir sonuç)? 3. Kapsam dışı ne?
4. Kısıtlar (süre, teknoloji, bütçe, mevcut kod)? 5. Bilinmeyenler neler?
Cevabı tahmin edilebilir olanları varsay ve yaz; yalnızca karar gerektirenleri sor.

## 2. Dikey dilimler

Katman katman (önce tüm DB, sonra tüm API, sonra tüm UI) değil; **uçtan uca ince dilimler**: her dilim kullanıcıya görünen,
deploy edilebilir bir değer.
```
Dilim 1: Tek hizmet, tek personel, sabit çalışma saati ile randevu oluşturma (DB+API+UI+test)
Dilim 2: Birden çok personel + "fark etmez"
Dilim 3: İptal/erteleme bağlantısı
Dilim 4: SMS hatırlatma
Dilim 5: Google Calendar senkronu
```
Her dilim sonunda çalışan ürün → erken geri bildirim, iptal edilse bile değer.

## 3. Risk önce

En belirsiz/riskli parça (bilinmeyen API, performans, karmaşık algoritma) **ilk** ele alınır — gerekirse zaman kutulu **spike**
(ör. "2 saat: iyzico sandbox'ta 3D Secure akışını dene, sonuç: çalışıyor/çalışmıyor + notlar"). Spike kodu atılabilir; öğrenilen kalır.

## 4. Her adımda "bitti" tanımı

- [ ] Kod + testler, CI yeşil
- [ ] Tarayıcıda/uç noktada doğrulandı (mobil dahil)
- [ ] Hata/boş/yükleniyor durumları
- [ ] Gerekirse doküman/changelog
- [ ] Deploy edildi (veya flag arkasında)

## 5. Tahmin

- Tek sayı değil **aralık**: "2–4 gün" + güven ("%70"). Bilinmeyen çoksa önce spike, sonra tahmin.
- Görevleri ≤ 1 günlük parçalara böl; böldükçe tahmin iyileşir ve gizli işler ortaya çıkar.
- Unutulanlar listesi: testler, hata durumları, migration, deploy, doküman, kod incelemesi, düzeltmeler — toplamın ~%30'u.
- Geçmiş verin varsa ona bak (benzer iş ne kadar sürmüştü?).

## 6. MVP kesme

"Bu olmadan ilk kullanıcı değeri alabilir mi?" — hayırsa MVP'de, evetse sonraya. Elle yapılabilecekler (rapor, fatura) başta elle.
Güvenlik, veri bütünlüğü ve yedek kesilmez.

## 7. Plan dosyası

`docs/plans/<özellik>.md`:
```markdown
# Online randevu
Hedef: müşteri telefonla aramadan randevu alabilsin. Başarı: ilk ayda randevuların %30'u online.
Kapsam dışı: ödeme, çoklu şube.
## Dilimler
- [x] 1. Tek hizmet randevu (2g) — PR #12
- [ ] 2. Çoklu personel (1–2g)
- [ ] 3. İptal/erteleme (1g)
## Riskler
- Saat dilimi hataları → slot motoru için kapsamlı birim testleri
## Kararlar
- Slot tutma 10 dk (bkz. ADR-003)
## Açık sorular
- Kapora alınacak mı? (işletme sahibine soruldu)
```
Plan yaşayan dokümandır: her dilimden sonra güncelle, yeni öğrendiklerini ekle.
