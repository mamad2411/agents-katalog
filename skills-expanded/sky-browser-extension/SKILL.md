---
name: sky-browser-extension
description: >-
  Tarayıcı eklentisi geliştirme: WXT ile Chrome/Firefox/Edge eklentisi, Manifest V3, içerik
  scriptleri ve Shadow DOM ile sayfaya UI enjekte etme, popup ve yan panel, sağ tık menüsü,
  klavye kısayolu, depolama ve mesajlaşma, minimum izinler, kendi web uygulamanla oturum,
  Chrome Web Store yayını ve red tuzakları. "Chrome eklentisi yap", "tarayıcı uzantısı",
  "sayfaya buton ekleyen eklenti" dendiğinde kullan.
disable-model-invocation: true
---

# Sky · Tarayıcı Eklentisi

## Araç

**WXT** (varsayılan): Vite tabanlı, dosya tabanlı giriş noktaları, HMR, çok tarayıcı, otomatik manifest.

```
entrypoints/
  background.ts          # MV3 service worker (olay tabanlı)
  content.ts             # sayfalara enjekte edilen script
  popup/index.html + App.tsx
  sidepanel/index.html   # Chrome yan panel — insanlar çok seviyor
  options/index.html
wxt.config.ts            # izinler, host_permissions
```

## İnsanların sevdiği kalıplar

- **Yan panel** (`chrome.sidePanel`): sayfanın yanında kalıcı araç (not, AI özet, CRM kartı).
- **Seçili metne sağ tık** (`contextMenus`): "Sky ile çevir/özetle/kaydet".
- **Sayfaya yüzen buton** (Shadow DOM): profil sayfasında "CRM'e ekle", ürün sayfasında "Fiyat geçmişi".
- **Klavye kısayolu** (`commands`): `Alt+S` ile paneli aç.
- **Rozet** (`action.setBadgeText`): okunmamış sayı.

## İçerik scripti + Shadow DOM UI

```ts
export default defineContentScript({
  matches: ["https://*.example.com/*"],
  cssInjectionMode: "ui",
  async main(ctx) {
    const ui = await createShadowRootUi(ctx, {
      name: "sky-widget", position: "inline", anchor: "body",
      onMount: (container) => { const root = createRoot(container); root.render(<Widget />); return root; },
      onRemove: (root) => root?.unmount(),
    });
    ui.mount();
  },
});
```
Shadow DOM, sayfa CSS'inin senin UI'nı bozmasını engeller. SPA'larda URL değişimini dinle.

## Mesajlaşma ve depolama

- Tipli mesajlaşma: `@webext-core/messaging`.
- `storage.local` (cihaz), `storage.sync` (hesapla senkron, küçük), `storage.session`. WXT `storage.defineItem` tipli.
- Service worker uyur: global değişkende state tutma.

## İzinler: minimum

- `activeTab` çoğu zaman `<all_urls>` yerine yeter → inceleme hızlı, kullanıcı korkmaz.
- `host_permissions` dar; isteğe bağlı izinleri `optional_permissions` ile çalışma anında iste.
- Her iznin gerekçesi mağaza açıklamasında.

## Web uygulamanla oturum

- `identity.launchWebAuthFlow` ile OAuth veya `externally_connectable` ile siteden eklentiye token.
- API çağrıları arka plan worker'dan.

## Güvenlik

- Uzak kod çalıştırma yasak (MV3); `eval` yok.
- Sayfadan gelen veriye güvenme; mesajları doğrula; DOM'a ham HTML basma.
- Veri topluyorsan gizlilik politikası.

## Yayın

- `wxt zip` → Chrome Web Store, Firefox AMO (`-b firefox`, kaynak kodu da ister), Edge Add-ons.
- Varlıklar: 128 ikon, 1280×800 ekran görüntüleri, Türkçe + İngilizce açıklama, tek amaç beyanı.
- Red sebepleri: geniş izin, belirsiz amaç, gizlilik beyanı eksik, kod gizleme.
- Büyük güncellemede `onInstalled` ile "Yenilikler" sayfası.
