---
name: sky-shopify
description: >-
  Shopify geliştirme: Online Store 2.0 temaları (Liquid, sections, blocks, JSON şablonlar,
  theme editor ayarları), Shopify CLI, tema performansı, metafield ve metaobject'ler, Storefront
  API ve Hydrogen ile headless mağaza, Shopify uygulamaları (Remix/React Router şablonu, Admin
  GraphQL API, webhook'lar, Polaris, app extensions — theme app extension, checkout UI
  extensions), Shopify Functions (indirim, kargo, ödeme özelleştirme), Türkiye satışı notları.
  Shopify mağazası veya uygulaması geliştirirken kullan.
disable-model-invocation: true
---

# Sky · Shopify

## Tema geliştirme (Online Store 2.0)

```bash
shopify theme init        # Dawn tabanlı başlangıç
shopify theme dev --store acme.myshopify.com   # canlı önizleme + sıcak yenileme
shopify theme check       # lint: performans, erişilebilirlik, Liquid hataları
shopify theme push --unpublished
```
```
sections/featured-services.liquid    # {% schema %} ile ayarlar + blocks → müşteri theme editor'da düzenler
templates/product.json               # hangi section'lar, hangi sırada
snippets/price.liquid
blocks/                              # tema blokları (yeniden kullanılabilir)
assets/  config/settings_schema.json  locales/tr.json
```
- Section ayarları ile müşteri kod yazmadan sayfa kurar (bkz. `sky-cms` blok felsefesi).
- Liquid: `{{ product.price | money }}`, `{% render 'price', product: product %}` (`include` değil), `image_url` + `image_tag` (responsive, lazy).
- Performans: tema JS'i minimum, üçüncü parti uygulama scriptlerini denetle (en büyük yavaşlatıcı), Lighthouse ve Shopify'ın tema hız raporu.

## Veri: metafield ve metaobject

Ürün/koleksiyon/müşteriye özel alanlar (metafield), yapılandırılmış özel içerik (metaobject — SSS, mağazalar, ekip) — theme editor'da dinamik kaynak olarak bağlanır.

## Headless: Hydrogen / Storefront API

Hydrogen (React Router tabanlı, Oxygen'de barındırma) veya Next.js + Storefront API (GraphQL): ürün, koleksiyon, sepet (Cart API), müşteri hesapları; ödeme Shopify Checkout'ta kalır. Ne zaman: tamamen özel deneyim ve içerik entegrasyonu gerekiyorsa — çoğu mağazada OS 2.0 tema daha hızlı ve ucuz.

## Uygulama geliştirme

```bash
shopify app init          # React Router/Remix şablonu, OAuth ve oturum hazır
shopify app dev
```
- **Admin GraphQL API** (REST eski), maliyet tabanlı rate limit; toplu işler için Bulk Operations.
- **Webhook'lar** (TOML'da abonelik): HMAC doğrulama, hızlı 200, kuyrukta işleme (bkz. `sky-jobs`); zorunlu GDPR webhook'ları (müşteri verisi talep/silme).
- UI: **Polaris** (Admin'e uyumlu), App Bridge; uzantılar: theme app extension (tema içine blok — script enjekte etmek yerine), checkout UI extensions, admin action'lar.
- **Shopify Functions**: indirim, kargo ve ödeme yöntemi özelleştirme mantığı (Rust/JS → WASM, Shopify altyapısında çalışır).
- Faturalandırma: Billing API (abonelik/kullanım bazlı); App Store inceleme kuralları (performans, gizlilik, net fiyat).

## Türkiye notları

Shopify Payments Türkiye'de yok → yerel ödeme sağlayıcılarının Shopify entegrasyonlarını (ör. iyzico/PayTR uygulamaları) kontrol et; TL fiyat, KDV dahil gösterim, e-Fatura uygulamaları, kargo entegrasyonları (bkz. `sky-tr-integrations`); yerel platformlar (ikas, Ticimax, T-Soft) alternatif olarak değerlendirilebilir (bkz. `sky-ecommerce`).
