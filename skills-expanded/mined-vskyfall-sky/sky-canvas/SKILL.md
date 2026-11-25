---
name: sky-canvas
description: >-
  Canvas ve SVG ile çizim etkileşimleri: imza alanı, serbest çizim/beyaz tahta, görsel
  düzenleme (metin, sticker, filtre), Konva/Fabric/tldraw/Excalidraw seçimi, Retina
  ölçekleme, pointer events ve kalem basıncı (perfect-freehand), geri al/yinele, hizalama
  kılavuzları, PNG/SVG/PDF dışa aktarım, konfeti kutlama anları ve OffscreenCanvas.
  "İmza alanı", "çizim tahtası", "görsel üzerine yazı", "konfeti", "whiteboard" dendiğinde kullan.
disable-model-invocation: true
---

# Sky · Canvas & Çizim

## Hazır mı, kendin mi?

| İhtiyaç | Seçim |
|---|---|
| Sonsuz beyaz tahta, şekiller, çok kullanıcı | **tldraw** veya **Excalidraw** |
| Sürüklenebilir nesneler, görsel editör | **Konva** (`react-konva`) |
| Klasik nesne düzenleyici | **Fabric.js** |
| İmza alanı | **signature_pad** veya `perfect-freehand` |
| Efekt | `canvas-confetti` |

## Retina ölçekleme (bulanıklığın 1 numaralı sebebi)

```ts
function setupCanvas(canvas: HTMLCanvasElement) {
  const dpr = Math.min(window.devicePixelRatio || 1, 2);
  const { width, height } = canvas.getBoundingClientRect();
  canvas.width = Math.round(width * dpr); canvas.height = Math.round(height * dpr);
  const ctx = canvas.getContext("2d")!; ctx.scale(dpr, dpr);
  return ctx;
}
```
`ResizeObserver` ile boyut değişince yeniden kur ve çiz.

## Pointer events ile çizim

```ts
canvas.addEventListener("pointerdown", (e) => { canvas.setPointerCapture(e.pointerId); start(e); });
canvas.addEventListener("pointermove", (e) => {
  for (const ev of e.getCoalescedEvents?.() ?? [e]) addPoint(ev.offsetX, ev.offsetY, ev.pressure || 0.5);
});
```
- Canvas'ta `touch-action: none` (yoksa sayfa kayar).
- `getCoalescedEvents` ile hızlı çizimde kayıp nokta yok → pürüzsüz çizgi.
- **perfect-freehand** basınç duyarlı, kalem gibi doğal çizgi — insanlar farkı hemen görür.

## İmza alanı

- Min 320×140, taban çizgisi + "Buraya imzalayın" soluk metni, "Temizle" butonu.
- Boşsa gönderim engelli; tek nokta geçersiz.
- Dışa aktar: **SVG** + PNG yedeği; zaman damgası ve IP ile kaydet (hukuki iz).
- Erişilebilir alternatif: "Adımı yazarak imzala" (el yazısı fontuyla render).

## Geri al / yinele

Komut deseni (`{ do, undo }`) veya küçük sahnelerde durum anlık görüntüleri. `⌘Z` / `⌘⇧Z`.

## Görsel editör kalıpları

- Metin ekle (sürükle, döndür, font/renk), sticker/emoji, kırp, filtre (`ctx.filter`), çerçeve.
- Katmanlar paneli: sırala, gizle, kilitle.
- Seçim tutamakları (Konva `Transformer`): Shift ile oran koru.
- **Hizalama kılavuzları:** nesne merkeze/kenara yaklaşınca pembe çizgi — profesyonel his.

## Dışa aktarım

- PNG: `canvas.toBlob(cb, "image/png")`; 2× çözünürlük seçeneği.
- SVG: Konva/Fabric export, tldraw `exportToSvg`. PDF: bkz. `sky-print-pdf`.
- Panoya kopyala ve paylaş (bkz. `sky-browser-apis`).
- Dış görseller canvas'ı kirletir (CORS) → `img.crossOrigin = "anonymous"` + sunucu CORS başlığı.

## Konfeti ve kutlama anları

```ts
import confetti from "canvas-confetti";
confetti({ particleCount: 120, spread: 70, origin: { y: 0.7 }, disableForReducedMotion: true });
```
Ne zaman: ilk başarılı işlem (ilk randevu, ödeme tamam, hedefe ulaşma). Her tıklamada değil.

## Performans

- `requestAnimationFrame`; sekme gizliyken dur.
- Statik arka planı ayrı katmanda çiz, yalnızca değişen katmanı yeniden çiz.
- Ağır iş → OffscreenCanvas + Worker. 10k+ nesne → PixiJS (WebGL).
