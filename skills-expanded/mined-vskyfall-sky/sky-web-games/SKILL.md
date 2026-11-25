---
name: sky-web-games
description: >-
  Tarayıcı oyunları geliştirme (özgün oyunlar): motor seçimi (Phaser, PixiJS, Kaplay, Three.js/
  R3F, saf Canvas), oyun döngüsü ve sabit zaman adımı, giriş (klavye, fare, dokunmatik, gamepad),
  çarpışma ve basit fizik (Matter.js, Rapier), sahne/durum yönetimi, varlık yükleme ve sprite
  atlas, ses (Web Audio, mobilde kilit açma), kayıt (localStorage/IndexedDB), skor tablosu,
  mobil uyum ve tam ekran, performans (nesne havuzu), juice (ekran sarsıntısı, parçacık) ve
  itch.io / web yayını. Oyun yaparken kullan.
disable-model-invocation: true
---

# Sky · Web Oyunları

Kural: **özgün oyunlar** — tür ve mekanik ilham alınabilir, ama mevcut bir oyunun adı, karakterleri, sanatı, müziği veya
seviyeleri kopyalanmaz. Kendi varlıklarını üret veya lisansı uygun paketler kullan (Kenney.nl CC0, OpenGameArt — lisansı kontrol et).

## Motor seçimi

| İhtiyaç | Seçim |
|---|---|
| 2D, her şey dahil (sahne, fizik, ses, giriş, tilemap) | **Phaser 3** |
| 2D render performansı, kendi oyun mantığın | **PixiJS** |
| Hızlı prototip, eğlenceli API, game jam | **Kaplay** (Kaboom'un devamı) |
| 3D | **Three.js** / React Three Fiber (bkz. `sky-3d`), Babylon.js |
| Çok basit (puzzle, kart, kelime) | DOM + CSS veya saf Canvas |
| Fizik | Matter.js (2D), Rapier (2D/3D, WASM, hızlı) |

## Oyun döngüsü: sabit zaman adımı

```ts
const STEP = 1000 / 60;            // fizik/mantık 60 Hz sabit
let acc = 0, last = performance.now();
function frame(now: number) {
  acc += Math.min(now - last, 250); // sekme dönüşünde "ölüm sarmalı" olmasın
  last = now;
  while (acc >= STEP) { update(STEP / 1000); acc -= STEP; }
  render(acc / STEP);              // ara değer (interpolation) ile pürüzsüz çizim
  requestAnimationFrame(frame);
}
requestAnimationFrame(frame);
```
Mantık kare hızından bağımsız olur (144 Hz ekranda oyun hızlanmaz). Hareketi `delta` ile çarp.

## Giriş

- Klavye: tuş durumlarını bir `Set`'te tut (`keydown`/`keyup`), `update` içinde oku; `e.code` (düzenden bağımsız — Türkçe Q/F klavyede de WASD çalışır).
- Dokunmatik: sanal joystick / ekran butonları, `pointer` olayları, `touch-action: none`.
- Gamepad API (`navigator.getGamepads()`), tuş atama ayarı.
- Erişilebilirlik: tuş yeniden atama, renk körü modu, hareket azaltma, altyazı, zorluk seçenekleri.

## Yapı

- Sahneler/durumlar: Boot → Preload → Menu → Game → Pause → GameOver; Phaser Scene'leri veya basit durum makinesi.
- Varlık yükleme ekranı (ilerleme çubuğu), sprite atlas (TexturePacker / free-tex-packer), bitmap font.
- Seviye tasarımı: **Tiled** haritaları (JSON) veya LDtk.
- ECS (bitecs, miniplex) çok varlıklı oyunlarda.

## Ses

Tarayıcı, kullanıcı etkileşimi olmadan ses çalmaz → ilk tıklama/dokunuşta `AudioContext.resume()` ("Başlamak için dokun" ekranı).
Howler.js veya motorun ses sistemi; ayrı müzik/efekt ses seviyesi, sessiz düğmesi, ayarı kaydet.

## Kayıt ve skor

- İlerleme: `localStorage` (küçük) / IndexedDB (büyük); sürüm alanı ile göç.
- Çevrimiçi skor tablosu: sunucuda doğrulama (istemciden gelen skora güvenme — basit hile önleme: oturum token'ı, makul süre/skor kontrolü, rate limit).

## "Juice" (oyunu hissettiren detaylar — oyuncuların sevdiği)

Ekran sarsıntısı (küçük, kısa), vuruş anında kısa donma (hit stop), parçacıklar, squash & stretch, ses çeşitlemesi (perde ±%5),
yumuşak kamera takibi, tween'li UI, kombo sayacı, ölüm/başarı geri bildirimi. Reduced-motion'da sarsıntıyı kapat.

## Performans

- Nesne havuzu (mermiler, parçacıklar) — her karede `new` yok (GC takılmaları).
- Sprite batching (aynı atlas), ekran dışı nesneleri güncelleme/çizme.
- Mobilde `devicePixelRatio` sınırla, hedef 60 FPS; DevTools Performance ile profille.

## Mobil ve yayın

- Tam ekran (`requestFullscreen`), yön kilidi, ölçekleme modu (Phaser `Scale.FIT`), PWA ile ana ekrana ekle (bkz. `sky-pwa`).
- Yayın: **itch.io** (HTML5 zip, oyuncu kitlesi ve game jam'ler), kendi site (Vercel/Netlify statik), Poki/CrazyGames portalları (SDK şartları).
- Masaüstü/mağaza: Tauri/Electron ile paketleme (bkz. `sky-desktop-app`).
