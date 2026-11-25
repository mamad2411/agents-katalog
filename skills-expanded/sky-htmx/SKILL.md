---
name: sky-htmx
description: >-
  Sunucu tarafı render + HTMX/Alpine.js ile hafif etkileşim ("hypermedia" yaklaşımı): hx-get/
  hx-post/hx-target/hx-swap, kısmi HTML parçaları, hx-trigger ile arama/sonsuz kaydırma/polling,
  hx-boost, form doğrulama, CSRF, out-of-band güncellemeler, Alpine.js ile istemci durumu,
  Django/Laravel/Rails/Go/FastAPI şablonlarıyla kullanım, ne zaman SPA yerine tercih edilir ve
  sınırları. "SPA istemiyorum", "HTMX", "Alpine", "server-rendered" dendiğinde kullan.
disable-model-invocation: true
---

# Sky · HTMX & Alpine

## Ne zaman?

✓ CRUD ağırlıklı paneller, form/tablo uygulamaları, backend ekibi güçlü (Django/Laravel/Rails/Go), az JS isteyen projeler — tek dil, tek deploy, hızlı.
✗ Yoğun istemci durumu (editör, çevrimdışı-önce, karmaşık sürükle-bırak, gerçek zamanlı işbirliği) → React/Svelte/Vue.

## Temel kalıplar

```html
<!-- canlı arama: yazarken 300ms sonra, önceki isteği iptal ederek -->
<input type="search" name="q" placeholder="Müşteri ara"
       hx-get="/clients/search" hx-trigger="input changed delay:300ms, search" hx-target="#results" hx-sync="this:replace">
<div id="results"></div>

<!-- satır silme: onay + satırı kaldır -->
<button hx-delete="/bookings/42" hx-confirm="Randevu silinsin mi?" hx-target="closest tr" hx-swap="outerHTML swap:200ms">Sil</button>

<!-- sonsuz kaydırma -->
<tr hx-get="/bookings?cursor=abc" hx-trigger="revealed" hx-swap="afterend">…</tr>

<!-- polling (yalnızca görünürken) -->
<div hx-get="/jobs/7/status" hx-trigger="every 2s [document.visibilityState === 'visible']">%45</div>
```
- Sunucu tam sayfa değil **parça** döner (`HX-Request` başlığına bak); aynı şablon parçası hem tam sayfada hem HTMX yanıtında kullanılır.
- `hx-boost="true"` ile normal bağlantı/formlar AJAX'a döner (SPA hissi, geri tuşu çalışır).
- Out-of-band: yanıtta `<span id="cart-count" hx-swap-oob="true">3</span>` → başka bir yeri de güncelle.
- Yanıt başlıkları: `HX-Redirect`, `HX-Trigger` (istemci olayı → toast), `HX-Refresh`.
- Form hatası: 422 + formu hatalarla yeniden render (htmx 2'de 4xx swap ayarı `htmx.config.responseHandling`).

## Alpine.js (küçük istemci durumu)

```html
<div x-data="{ open: false }">
  <button @click="open = !open" :aria-expanded="open">Filtreler</button>
  <div x-show="open" x-transition @click.outside="open = false">…</div>
</div>
```
Dropdown, modal, sekme, kopyala butonu gibi tamamen istemci tarafı şeyler için; sunucu verisi HTMX'te kalsın.

## Güvenlik ve erişilebilirlik

- CSRF token'ı `hx-headers` veya meta etiketten tüm isteklere (Django/Laravel/Rails ile kolay).
- Sunucu parçalarında da kaçışlı şablon (XSS); yetki her uç noktada.
- Dinamik bölgeler `aria-live`, odak yönetimi (silme/ekleme sonrası), `hx-indicator` ile yükleniyor göstergesi.

## Framework eşleşmeleri

Django + `django-htmx`, Laravel + Blade (veya Livewire — benzer felsefe), Rails Hotwire (bkz. `sky-rails` — Turbo aynı felsefe), Go `html/template` / templ, FastAPI + Jinja2.
