---
name: sky-wordpress
description: >-
  WordPress geliştirme: blok (Gutenberg) teması ve theme.json, özel blok geliştirme
  (@wordpress/scripts, block.json), tema ve eklenti yapısı, hook sistemi (action/filter), özel
  yazı türleri ve alanlar (ACF/meta), REST API ve headless WordPress, WooCommerce özelleştirme,
  güvenlik (nonce, yetki, kaçış, sanitize, SQL prepare), performans (önbellek, sorgu, görsel),
  çok dillilik (WPML/Polylang), yerel geliştirme (wp-env, LocalWP), WP-CLI ve güvenli güncelleme.
  WordPress/WooCommerce projesinde kullan.
disable-model-invocation: true
---

# Sky · WordPress

## Modern yol: blok teması

```
my-theme/
  style.css            # tema başlığı
  theme.json           # renkler, tipografi, boşluklar, düzen — tasarım token'ları burada
  templates/index.html, single.html, page.html   # blok şablonları
  parts/header.html, footer.html
  patterns/hero.php    # hazır blok desenleri (müşteri tek tıkla ekler)
  functions.php
```
`theme.json` ile editör ve ön yüz aynı token'ları kullanır (bkz. `sky-design-system` ilkeleri); müşteri Site Editor'da güvenle düzenler.
Klasik tema (PHP şablonlar) eski projelerde; yeni projede blok teması.

## Özel blok

```bash
npx @wordpress/create-block@latest sky-booking-cta
```
`block.json` (ad, nitelikler, destekler), `edit.js` (editör React bileşeni), `save.js` veya dinamik blok için `render.php` (sunucuda render — veri değişince içerik güncel kalır).

## Hook'lar

```php
add_action('init', function () {
    register_post_type('service', [
        'label' => 'Hizmetler', 'public' => true, 'show_in_rest' => true,
        'supports' => ['title', 'editor', 'thumbnail'], 'menu_icon' => 'dashicons-calendar-alt',
    ]);
});
add_filter('excerpt_length', fn () => 30);
```
Tema = görünüm, **eklenti = işlev** (özel yazı türleri, entegrasyonlar eklentide — tema değişince kaybolmasın). Ön ek kullan (`sky_`), global ad çakışması yok.

## Güvenlik (en kritik)

- **Kaçış (çıktıda)**: `esc_html()`, `esc_attr()`, `esc_url()`, `wp_kses_post()`.
- **Temizleme (girdide)**: `sanitize_text_field()`, `absint()`, `sanitize_email()`.
- **Nonce + yetki**: form/AJAX'ta `wp_nonce_field` / `check_ajax_referer` + `current_user_can('edit_posts')` — nonce yetki değildir.
- **SQL**: `$wpdb->prepare("SELECT * FROM {$wpdb->prefix}x WHERE id = %d", $id)`.
- REST uç noktalarında `permission_callback` zorunlu (`'__return_true'` yalnızca gerçekten herkese açıksa).
- Güncellemeler (çekirdek, eklenti, tema) düzenli; terk edilmiş eklenti kullanma; `DISALLOW_FILE_EDIT`; 2FA; admin kullanıcı adı `admin` olmasın.

## Performans

Sayfa önbelleği (sunucu/eklenti: WP Super Cache, LiteSpeed Cache), nesne önbelleği (Redis), görsel optimizasyonu (WebP/AVIF, lazy), gereksiz eklentileri kaldır, `WP_Query`'de `no_found_rows` ve `fields => 'ids'` gerektiğinde, autoload edilen option'ları temizle, Query Monitor ile yavaş sorguları bul.

## Headless WordPress

REST API veya WPGraphQL + Next.js/Astro ön yüz (bkz. `sky-cms`); önizleme ve yeniden doğrulama webhook'ları; ACF alanlarını REST'e aç. Karmaşıklık artar — basit sitede klasik/blok tema yeterli.

## WooCommerce

Hook'larla özelleştir (şablonları kopyalamak yerine), HPOS uyumlu kod, ödeme ağ geçitleri (iyzico/PayTR eklentileri — bkz. `sky-payments`), kargo entegrasyonları (bkz. `sky-tr-integrations`), e-Fatura eklentileri.

## Araçlar

Yerel: `wp-env` (Docker) veya LocalWP; **WP-CLI** (`wp plugin update --all`, `wp search-replace` — alan adı taşıma, önce yedek!), Composer (Bedrock yapısı), PHPCS + WordPress Coding Standards, staging ortamında güncelleme testi.
