---
name: hyperframes
description: HyperFrames kompozitsiyalarini yozish uchun ko'rsatma. Kompozitsiya — bu HTML5 fayl, ichida CSS animatsiyalar va GSAP timeline. Shu kompozitsiya keyin video (MP4) ga render qilinadi.
license: Apache-2.0
upstream: https://github.com/heygen-com/hyperframes
---

# HyperFrames Kompozitsiya Skill

Bu skill — qisqa, vertical (Reel/TikTok/YouTube Short) yoki gorizontal video uchun
yagona HTML kompozitsiya yozish bo'yicha to'liq qo'llanma. Skill upstream HeyGen
HyperFrames loyihasi (Apache 2.0) asosida tuzilgan; lekin Qanot AI uchun mos qilib
qisqartirilgan: bitta kompozitsiya, bitta video, sub-kompozitsiyasiz.

HTML — videoning **manba kodi**. Kompozitsiya HTML fayli `data-*` atributlari
yordamida vaqtni belgilaydi, GSAP timeline yordamida animatsiyani yuritadi, va CSS
yordamida ko'rinishni boshqaradi.

## Yondashuv

HTML yozishdan oldin baland darajada o'ylab oling:

1. **Nima** — tomoshabin nimani ko'rishi kerak? Hikoyaning markaziy g'oyasi va
   his-tuyg'usi nima?
2. **Tuzilish** — qancha sahna kerak? Har biri qanday element (matn, rasm, video, audio)
   tarkib topadi?
3. **Vaqt** — har bir sahna necha soniya? Animatsiya o'tishlari qachon ishga tushadi?
4. **Layout (joylashuv)** — har bir element to'liq ko'rinadigan eng yorqin kadrini
   chizing. Avval CSS bilan static joylashuv quring, keyin GSAP qo'shing.
5. **Animatsiya** — kirish/chiqish va vaqtni rejalashtiring.

## Ranglar va Tipografiya (DESIGN.md)

Agar bot workspace'ida `DESIGN.md` mavjud bo'lsa, undan rang palitra, font, va
harakat (motion) qoidalarini OLING. Default `#333`, `#3b82f6`, yoki `Roboto` ishlatish
— DESIGN.md o'qilmagan, demak xato.

DESIGN.md bo'lmasa, uchta-to'rtta toza rang tanlang (asos, asosiy matn, urg'u, soyali).
Font sifatida `'Inter', system-ui` yoki shu kabi sans-serif oilani ishlating.

## Layout: avval CSS, keyin GSAP

Har bir element o'zining **eng ko'rinarli kadrida** qayerda turishi kerakligini
**static CSS bilan** belgilang. Animatsiya esa shu pozitsiyaga **kirish** yo'lini
animatsiya qiladi.

`.scene-content` konteyneri butun sahnani to'ldirishi kerak:

```css
.scene-content {
  width: 100%;
  height: 100%;
  padding: 120px 80px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 24px;
  box-sizing: border-box;
}
```

Yo'l qo'ymang: tarkib uchun `position: absolute; top: ...px`. Bu joylashuv content
balandligi o'zgarganda toshib ketadi.

## Data atributlari

### Root element (kompozitsiya o'rni)

| Atribut | Talab | Qiymat |
|---|---|---|
| `data-composition-id` | Ha | Yagona ID, odatda `"main"` |
| `data-start` | Ha | Boshlanish vaqti (root uchun `"0"`) |
| `data-duration` | Ha | Soniyalarda umumiy davomiylik |
| `data-width` | Ha | Piksel kengligi (1080 yoki 1920) |
| `data-height` | Ha | Piksel balandligi (1920 yoki 1080) |

Format → o'lchamlar:
- 9:16 (Reel/Short) → 1080×1920
- 16:9 (gorizontal) → 1920×1080
- 1:1 (kvadrat) → 1080×1080

### Klip elementlari (matn, rasm, video, audio)

| Atribut | Talab | Qiymat |
|---|---|---|
| `id` | Ha | Yagona identifikator |
| `data-start` | Ha | Sekundlarda boshlanish vaqti |
| `data-duration` | Img/div uchun ha | Sekundlarda davomiyligi (video/audio default — manba davomiyligi) |
| `data-track-index` | Ha | Butun son. Bir trekdagi klipplar bir-biriga qoplanmaydi |
| `data-volume` | Yo'q | 0..1 (default 1) |

`data-track-index` faqat vaqt bo'yicha qatlamlashni boshqaradi, vizual qatlamlash uchun
CSS `z-index` ishlating.

## Kompozitsiya tuzilishi (yagona, standalone)

```html
<!doctype html>
<html>
<head>
  <meta charset="UTF-8">
  <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
  <style>
    /* CSS reset + root rang/font o'zgaruvchilari */
    html, body { margin: 0; padding: 0; overflow: hidden; }
    body { font-family: 'Inter', system-ui, sans-serif; background: #0a0a0a; color: #ffffff; }
    #root { width: 1080px; height: 1920px; position: relative; }

    .scene-content {
      width: 100%;
      height: 100%;
      padding: 120px 80px;
      display: flex;
      flex-direction: column;
      justify-content: center;
      gap: 24px;
      box-sizing: border-box;
      text-align: center;
    }
    h1 { font-size: 96px; font-weight: 800; margin: 0; line-height: 1.1; }
    p  { font-size: 42px; color: #a0a0a0; margin: 0; line-height: 1.4; }
  </style>
</head>
<body>
  <div id="root"
       data-composition-id="main"
       data-start="0"
       data-duration="6"
       data-width="1080"
       data-height="1920">
    <div class="scene-content">
      <h1 id="title">Mahsulotim</h1>
      <p id="sub">Endi onlayn buyurtma qabul qilinadi</p>
    </div>
  </div>

  <script>
    const tl = gsap.timeline({ paused: true });
    tl.from("#title", { y: 80, opacity: 0, duration: 0.7, ease: "power3.out" }, 0.1)
      .from("#sub",   { y: 40, opacity: 0, duration: 0.6, ease: "power3.out" }, 0.4);
    window.__timelines = window.__timelines || {};
    window.__timelines["main"] = tl;
  </script>
</body>
</html>
```

**Standalone kompozitsiyalar `<template>` ishlatmaydi.** Bu farqi muhim: HyperFrames'da
`<template>` faqat sub-kompozitsiyalar uchun. Bizda har bir render bitta yagona
kompozitsiya — uni to'g'ridan-to'g'ri `<body>` ichida qo'ying.

## Video va audio

Video element doim `muted` va `playsinline` bo'lishi kerak. Audio uchun alohida
`<audio>` elementi ishlating:

```html
<video id="bg" data-start="0" data-duration="30" data-track-index="0"
       src="..." muted playsinline></video>
<audio id="vo" data-start="0" data-duration="30" data-track-index="2"
       src="..." data-volume="1"></audio>
```

Audio manbasi sifatida workspace ichidagi TTS chiqishi yoki tashqi HTTPS URL bo'lishi
mumkin. Brauzer ichida `play()`/`pause()`/`seek()` chaqirmang — render dvigateli
o'zi boshqaradi.

## Timeline qoidalari

- Har bir GSAP timeline `{ paused: true }` bilan boshlanadi.
- Har bir timelineni ro'yxatga oling: `window.__timelines["main"] = tl`.
- Render dvigateli `data-duration`ga qarab o'zi to'xtatadi — siz timeline'ga sun'iy
  bo'sh tween qo'shmang.
- Timeline'ni `async`/`await`/`setTimeout`/`Promise` ichida QURMANG. Render dvigateli
  `window.__timelines`ni sahifa yuklangach **darhol** o'qiydi.
- `repeat: -1` (cheksiz) IShlAtMANG. Aynan necha marta takrorlash kerakligini
  hisoblang: `Math.ceil(duration / cycleDuration) - 1`.

## Qoidalar (qat'iy)

1. **Determinizm**: `Math.random()`, `Date.now()`, real vaqt — IShlAtMANG.
   Tasodifiylik kerak bo'lsa, mulberry32 kabi seeded PRNG.
2. **GSAP**: faqat vizual property'larni animatsiya qiling (`opacity`, `x`, `y`,
   `scale`, `rotation`, `color`, `backgroundColor`, `borderRadius`, transformlar).
   `visibility`, `display`, `video.play()`, `audio.play()` — animatsiya qilmang.
3. **Bir property — bir timeline**: bir element + bir property kombinatsiyasini
   bir vaqtda ikki timeline'dan animatsiya qilmang.
4. **Default — kirish animatsiyasi**: har bir element `gsap.from()` bilan kiradi.
   `gsap.to()` (chiqish) faqat oxirgi sahnada (yakuniy fade-out uchun) ishlatiladi.
5. **Soat 0 da boshlamang**: birinchi animatsiyani 0.1–0.3s'ga kechiktiring.
6. **Easing xilma-xilligi**: bir sahna ichida kamida 3 xil ease ishlating
   (`power3.out`, `expo.out`, `power2.in`, `back.out`, ...).

## Sahna o'tishlari

- Bir nechta sahna bo'lsa, har biri orasida o'tish (transition) bo'lishi kerak.
  Jump-cut ishlatmang.
- Har bir sahnaning har bir elementi `gsap.from()` bilan kiradi. Birorta element
  "to'satdan paydo bo'lmasin".
- Chiqish animatsiyalari (`gsap.to(..., { opacity: 0 })`) faqat **oxirgi sahnada**
  ruxsat etiladi. Boshqa sahnalarda chiqish yo'q — o'tish o'zi ekranni almashtiradi.

## Tipografiya va Kontrast

- Sarlavhalar: 60px+ (ko'pincha 80–120px)
- Asosiy matn: 28–48px
- Ma'lumot/etiketkalar: 18px+
- Raqamli kolonkalar uchun: `font-variant-numeric: tabular-nums;`
- WCAG AA: oddiy matn uchun 4.5:1, katta matn uchun 3:1 kontrast.
- To'liq ekran chiziqli gradiyentlardan saqlaning (H.264 banding) — radial yoki
  bir hil rang + lokal yorug'lik effekt afzal.

## Asset URL'lari

Tashqi asset'larga (font, rasm, video, musiqa) faqat **HTTPS** orqali murojaat qiling.
`http://localhost` va `data:` (kichik tasvirlar uchun) bundan istisno. Ichki/private
IP'lar (10.x, 192.168.x, 172.16.x, 169.254.x) — ishlatish mumkin emas. Render
dvigateli bunday URL'larni `lint` paytida rad etadi.

## Default chiqish formati

- Resolution: 9:16 → 1080×1920, 16:9 → 1920×1080, 1:1 → 1080×1080
- FPS: 30 (default)
- Codec: H.264 (render dvigateli boshqaradi)

## Chiqish — qat'iy

Sizning chiqishingiz **faqat HTML hujjat**. Markdown blok belgilari (` ``` `) yo'q,
sharhlar yo'q, hech qanday muqaddima yo'q. Birinchi belgi `<!doctype html>` bo'lishi
shart. Oxirgi belgi `</html>`.

Render dvigateli birinchi belgisi `<!` bo'lmagan har qanday chiqishni rad etadi.
