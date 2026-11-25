---
name: sky-pwa
description: >-
  Progressive Web App: web uygulamasını telefona "uygulama gibi" kurulabilir yapma; manifest,
  ikon seti, Serwist ile service worker, önbellek stratejileri, çevrimdışı sayfa ve çevrimdışı
  veri, kurulum (install) butonu, iOS kısıtları, push bildirimine hazırlık, güncelleme akışı
  ("yeni sürüm var, yenile"). "Uygulama gibi olsun", "ana ekrana ekle", "çevrimdışı çalışsın"
  dendiğinde kullan.
disable-model-invocation: true
---

# Sky · PWA

## Kurulabilirlik minimumu

1. **HTTPS** (localhost hariç).
2. **Web manifest** (`app/manifest.ts`):
```ts
export default function manifest(): MetadataRoute.Manifest {
  return {
    name: "Randevu Defteri", short_name: "Randevu",
    start_url: "/?source=pwa", scope: "/", display: "standalone",
    background_color: "#0f0f12", theme_color: "#2b59ff", lang: "tr", dir: "ltr",
    icons: [
      { src: "/icons/192.png", sizes: "192x192", type: "image/png" },
      { src: "/icons/512.png", sizes: "512x512", type: "image/png" },
      { src: "/icons/maskable-512.png", sizes: "512x512", type: "image/png", purpose: "maskable" },
    ],
    shortcuts: [{ name: "Yeni randevu", url: "/randevu/yeni", icons: [{ src: "/icons/plus-96.png", sizes: "96x96" }] }],
    screenshots: [{ src: "/shots/mobile-1.png", sizes: "1080x1920", type: "image/png", form_factor: "narrow" }],
  };
}
```
3. **Service worker** kayıtlı.
4. İkonlar: maskable ikonda logo güvenli alanın (merkezdeki %80) içinde; `apple-touch-icon` 180×180.

`screenshots` ve `shortcuts` Android'de zengin kurulum ekranı ve uzun basma menüsü verir — insanlar bunu sever.

## Service worker: Serwist

`@serwist/next` ile: precache (build çıktıları) + runtime caching.

| Kaynak | Strateji |
|---|---|
| Hash'li statik dosyalar (JS/CSS/font) | **CacheFirst** (precache) |
| Görseller | **StaleWhileRevalidate**, maks 200 öğe, 30 gün |
| HTML sayfalar | **NetworkFirst**, 3 sn zaman aşımı → cache → çevrimdışı sayfa |
| API GET (okuma) | **NetworkFirst** veya SWR — veri tazeliğine göre |
| API POST/PUT | Önbellekleme yok; çevrimdışıysa **Background Sync** kuyruğu |
| Auth/ödeme uç noktaları | **NetworkOnly** — asla cache |

Kullanıcıya özel yanıtları paylaşılan cache'e koyma; çıkışta (`logout`) kullanıcı cache'lerini temizle.

## Çevrimdışı deneyim

- `/offline` sayfası: marka, "İnternet yok" mesajı, önbellekteki son içeriğe bağlantılar.
- Çevrimdışı rozeti: `navigator.onLine` + `online/offline` olayları → üstte ince bant
  ("Çevrimdışısın — değişikliklerin bağlanınca gönderilecek").
- Çevrimdışı yazma: IndexedDB'ye taslak (Dexie / idb-keyval), bağlanınca senkron; çakışma kuralı (bkz. `sky-realtime`).
- Formlar çevrimdışıyken gönder butonu "Bağlanınca gönder" olur.

## Kurulum butonu (Android/Chrome/Edge)

```ts
let deferred: BeforeInstallPromptEvent | null = null;
window.addEventListener("beforeinstallprompt", (e) => { e.preventDefault(); deferred = e; showInstallButton(); });
async function install() { await deferred?.prompt(); const { outcome } = await deferred!.userChoice; track("pwa_install", { outcome }); deferred = null; }
window.addEventListener("appinstalled", () => hideInstallButton());
```
- Butonu **değer anından sonra** göster (ikinci ziyaret, ilk başarılı işlem), açılışta değil.
- Zaten kurulduysa (`matchMedia("(display-mode: standalone)")`) gösterme.

## iOS (Safari) gerçekleri

- `beforeinstallprompt` yok → "Paylaş → Ana Ekrana Ekle" talimatını gösteren küçük bir ipucu
  (yalnızca iOS Safari'de, bir kez, kapatılabilir).
- Web Push yalnızca **ana ekrana eklenmiş** PWA'da (iOS 16.4+).
- Depolama baskı altında silinebilir; kritik veriyi sunucuda tut. `navigator.storage.persist()` iste.
- Safe area: `viewport-fit=cover` + `env(safe-area-inset-*)` (bkz. `sky-mobile-ux`).

## Güncelleme akışı

Yeni service worker beklemede → toast: "Yeni sürüm hazır · Yenile". Tıklanınca `skipWaiting` + reload.
Kullanıcı form doldururken zorla yenileme yapma.

## Uygulama hissi detayları

- `display: standalone`'da tarayıcı geri butonu yok → uygulama içinde geri navigasyonu olsun.
- Durum çubuğu rengi `theme_color` + koyu tema için `<meta name="theme-color" media="(prefers-color-scheme: dark)">`.
- Kısa yollar (shortcuts), paylaşım hedefi (`share_target`) ile "fotoğrafı uygulamamla paylaş".
- Uygulama ikonunda sayı rozeti: `navigator.setAppBadge(n)` (bkz. `sky-browser-apis`).

## Test

- DevTools → Application: manifest hataları, SW durumu, Cache Storage, "Offline" kutusu.
- Lighthouse kurulabilirlik denetimi.
- Gerçek telefonda: kur, uçak modunda aç, form gönder, bağlantıyı aç → senkron oldu mu.
