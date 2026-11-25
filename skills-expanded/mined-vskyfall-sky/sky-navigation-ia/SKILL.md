---
name: sky-navigation-ia
description: >-
  Bilgi mimarisi ve navigasyon: kart sıralama ile menü yapısı, birincil/ikincil/yardımcı
  navigasyon, sekme vs sayfa vs akordiyon kararı, breadcrumb, mega menü, mobil menü kalıpları,
  derinlik kuralı (3 tık), arama ve komut paleti ile gezinme, aktif durum, URL tasarımı ve
  boş/kayıp sayfa önleme. "Menü nasıl olmalı", "sayfalar dağınık", "kullanıcı aradığını
  bulamıyor", "site haritası" dendiğinde kullan.
disable-model-invocation: true
---

# Sky · Bilgi Mimarisi & Navigasyon

## Önce içerik envanteri

Tüm sayfaları/özellikleri listele → kullanıcı görevlerine göre grupla (kart sıralama: 5 kişiye kartları
gruplatıp adlandırmak bile çok şey öğretir) → grup adlarını **kullanıcının kelimeleriyle** koy ("Faturalar",
"Ödemeler" değil "Muhasebe Modülü" değil).

## Navigasyon katmanları

| Katman | Örnek | Konum |
|---|---|---|
| Birincil | Panel, Randevular, Müşteriler, Raporlar | sidebar / üst menü / mobil alt bar |
| İkincil | (Müşteriler içinde) Liste, Segmentler, İçe aktar | sekmeler / alt menü |
| Yardımcı | Hesap, Ayarlar, Yardım, Çıkış | sağ üst avatar menüsü |
| Bağlamsal | ilgili kayıt bağlantıları, breadcrumb | içerik içinde |

Birincil öğe sayısı 5–7. Fazlası → grupla veya "Daha fazla".

## Sekme mi, sayfa mı, akordiyon mu?

- **Sekme**: aynı nesnenin eşdüzey görünümleri (Müşteri: Genel / Randevular / Ödemeler); 2–6 sekme; URL'de (`?tab=`).
- **Ayrı sayfa**: bağımsız görev, paylaşılabilir/derin içerik.
- **Akordiyon**: sırayla taranan kısa bölümler (SSS, ayar grupları); önemli içeriği akordiyona gömme.
- **Adım (wizard)**: sıralı zorunlu akış.

## Kurallar

- Her önemli hedef ≤ 3 tık (veya ⌘K ile 1).
- Kullanıcı her an **nerede olduğunu** bilir: aktif menü öğesi (`aria-current="page"`), sayfa başlığı, breadcrumb.
- Breadcrumb hiyerarşik derinlik ≥ 3 olduğunda; son öğe tıklanamaz.
- Etiketler tutarlı: menüde "Müşteriler" ise sayfa başlığı da "Müşteriler".
- Geri tuşu beklendiği gibi çalışır (filtre/sekme URL'de, modal URL'de opsiyonel).

## Mega menü (pazarlama siteleri)

Gruplar başlıklı sütunlar, her bağlantının altında 1 satır açıklama, sağda öne çıkan içerik/görsel;
hover niyeti gecikmesi (150ms) ve klavye ile açılabilir; mobilde akordiyonlu tam ekran menüye dönüşür.

## Mobil menü

- Uygulama: alt navigasyon (4–5 ana bölüm) + "Daha fazla".
- Site: hamburger → tam ekran katman, büyük dokunma hedefleri, birincil CTA en altta yapışkan.
- Hamburger simgesinin yanında "Menü" yazısı keşfedilebilirliği artırır.

## Arama ile gezinme

Büyük uygulamada ⌘K komut paleti (bkz. `sky-dashboard`): sayfalar, eylemler ("Yeni randevu"), son kayıtlar.
Güçlü kullanıcılar için menüden daha hızlı; menüyü değil tamamlar.

## URL tasarımı

- Okunur ve hiyerarşik: `/musteriler/123/randevular`; org bazlı: `/o/acme/musteriler`.
- Kalıcı: URL değişirse 301 (bkz. `sky-seo`).
- Durum URL'de (filtre, sekme, sayfa) → paylaşılabilir ve geri tuşu dostu.

## Kayıp sayfa önleme

404 sayfasında arama + popüler bağlantılar; silinen kayıt bağlantısında "Bu kayıt silinmiş" (genel 404 değil);
yetkisiz sayfada "Erişimin yok — yöneticinden iste" (bkz. `sky-ux-writing`).

## Test

- 5 kullanıcıya "X'i bul" görevi (tree testing — Treejack / kağıt): başarı oranı ve ilk tık.
- Analitik: sık kullanılan sayfalar, arama sorguları (insanlar menüde bulamadığını arar), geri dönüşler.
