---
name: sky-ecommerce
description: >-
  E-ticaret: ürün/varyant, stok, sepet, sipariş durumu, kupon, Türkiye kargo entegrasyonları, iade ve
  fatura. "Online mağaza", "e-ticaret sitesi", "sepet" dendiğinde kullan.
---

# Sky · E-Ticaret

## Önce: yapmalı mı?

Küçük mağaza için Shopify / ikas / Ticimax / T-Soft gibi hazır platformlar çoğu zaman doğru cevap.
Özel ihtiyaçta: **Medusa** (açık kaynak, Node) veya Shopify Storefront API + Next (headless). Sıfırdan
yazmak yalnızca iş modeli gerçekten farklıysa.

## Veri modeli

```
products   id, slug, title, description, brand, status (draft|active|archived), seo jsonb
options    product_id, name ("Renk", "Beden"), position
variants   id, product_id, sku UNIQUE, option_values jsonb ({"Renk":"Siyah","Beden":"M"}), price_minor, compare_at_minor, barcode, weight_g
inventory  variant_id, location_id, on_hand, reserved
media      product_id, variant_id?, url, alt, position
orders     id, number ("SKY-10042"), user_id?, email, status, currency, subtotal, discount, shipping, tax, total, addresses jsonb, created_at
order_items order_id, variant_id, title_snapshot, price_snapshot, qty
```
Siparişte ürün adı/fiyatı **anlık görüntü** olarak saklanır (ürün sonradan değişse de sipariş değişmez).

## Stok

- `available = on_hand − reserved`. Ödeme başlayınca **rezerve** et (15 dk), ödeme olunca düş, süre dolunca serbest bırak.
- Atomik: `update inventory set reserved = reserved + $q where variant_id = $v and on_hand - reserved >= $q` (etkilenen satır 0 → stok yok).
- "Son 3 ürün" rozeti (gerçekse — sahte kıtlık yok, bkz. `sky-ethical-ux`).
- Stok bitince "Gelince haber ver" (e-posta toplama).

## Sepet

- Misafir sepeti çerez ID'si + DB (localStorage yalnızca değil — cihazlar arası/terk edilmiş sepet için).
- Giriş yapınca birleştir (aynı varyant → miktarları topla).
- Sepette fiyat ve stok **her açılışta yeniden doğrulanır**; değişen satırda uyarı.
- Kayan sepet çekmecesi (drawer), "Kargoya ₺150 kaldı" ilerleme çubuğu — sepet tutarını belirgin artırır.

## Sipariş durum makinesi

```
pending_payment → paid → preparing → shipped → delivered
        ↓            ↓         ↓
     cancelled    refunded  return_requested → returned → refunded
```
Her geçiş audit'li (bkz. `sky-audit-history`), müşteriye bildirim (bkz. `sky-notifications`), geçersiz geçiş reddedilir.

## Kupon / kampanya motoru

- Türler: yüzde, sabit tutar, ücretsiz kargo, X al Y öde, sepet tutarı eşiği, kategori/ürün kısıtlı.
- Kurallar: başlangıç/bitiş, kullanım limiti (toplam ve kişi başı), minimum tutar, birleşebilir mi.
- Hesap **sunucuda**; istemci yalnızca kodu gönderir. Otomatik kampanyalar kodsuz uygulanır, sepette gösterilir.

## Kargo

- Ücret: sabit / ağırlık-desi / ücretsiz eşik; teslimat süresi tahmini ("Yarın kargoda").
- Türkiye entegrasyonları (Yurtiçi, Aras, MNG, Sürat, PTT; agregatörler: Geliver, Kargonomi): gönderi oluştur,
  barkod/etiket PDF (bkz. `sky-print-pdf`), takip numarası, durum webhook'u → bkz. `sky-tr-integrations`.
- Kapıda ödeme (TR'de hâlâ yaygın) ek ücret seçeneği.

## Ürün sayfası dönüşüm detayları

- Büyük galeri (yakınlaştırma, video), varyant seçince görsel değişir, URL'de varyant (`?renk=siyah`).
- Fiyat + indirimli fiyat + taksit bilgisi ("3 taksit ₺333,33").
- Stok ve teslimat bilgisi düğmenin yanında; yapışkan mobil "Sepete ekle" çubuğu.
- Beden tablosu, iade koşulları özeti, güven rozetleri (gerçek olanlar), yorumlar + fotoğraflı yorumlar.
- `Product` + `Offer` JSON-LD (bkz. `sky-seo`).

## İade

Müşteri panelinden iade talebi (ürün seç, neden, fotoğraf) → iade kodu → onay → para iadesi (sağlayıcı API, bkz. `sky-payments`).
Mesafeli satış 14 gün cayma hakkı — süreci basit tut.

## Terk edilmiş sepet

E-posta bıraktıysa: 1 saat, 24 saat sonra hatırlatma (ürün görselleriyle, sepete dönüş bağlantısı); rıza ve İYS kuralları
(bkz. `sky-notifications`).
