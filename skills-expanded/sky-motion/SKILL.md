---
name: sky-motion
description: >-
  Arayüz hareketi: süre ve easing ölçeği, giriş/çıkış geçişleri, mikro etkileşimler, sayfa
  geçişleri, liste animasyonları, kaydırma tetikli animasyon, Framer Motion (motion/react),
  CSS transitions, View Transitions API ve prefers-reduced-motion. Animasyon eklerken veya
  "daha canlı hissettirsin", "geçiş ekle" dendiğinde kullan.
disable-model-invocation: true
---

# Sky · Hareket

## İlke

Hareket bir **açıklamadır**: bir şeyin nereden geldiğini, nereye gittiğini ve neyin değiştiğini
gösterir. Süs için hareket ekleme; her animasyonun bir görevi olsun.

## Süre ölçeği

| Token | Süre | Kullanım |
|---|---|---|
| `--dur-fast` | 100–150ms | hover, renk, opaklık, buton basma |
| `--dur-base` | 180–240ms | dropdown, tooltip, toggle, küçük panel |
| `--dur-slow` | 280–400ms | modal, drawer, sayfa geçişi |

400ms'yi aşan UI geçişi yavaş hissettirir. Çıkış, girişten ~%20 kısa olsun.

## Easing

- Giriş / beliren öğe: **ease-out** `cubic-bezier(0.22, 1, 0.36, 1)`
- Ekranda yer değiştiren: **ease-in-out** `cubic-bezier(0.65, 0, 0.35, 1)`
- Fiziksel his (sürükleme, sheet): **spring** — `{ type: "spring", stiffness: 400, damping: 32 }`
- `linear` yalnızca spinner/ilerleme için.

## Ne animasyonlanır

- Yalnızca **`transform` ve `opacity`** (GPU dostu). `width/height/top/left` animasyonundan kaçın;
  yükseklik için `grid-template-rows: 0fr → 1fr` hilesi veya Framer `layout`.
- Giriş: `opacity 0 → 1` + küçük kayma (`translateY(4–8px)`) veya `scale(0.96 → 1)`.
  Büyük mesafeler ucuz görünür.
- Popover/dropdown kaynağından açılsın (`transform-origin` tetikleyiciye doğru).

## Kalıplar

**CSS mikro etkileşim**
```css
.btn { transition: background-color var(--dur-fast) var(--ease-out), transform var(--dur-fast) var(--ease-out); }
.btn:active { transform: scale(0.98); }
```

**Framer Motion (motion/react) — giriş/çıkış**
```tsx
<AnimatePresence>
  {open && (
    <motion.div
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: 4, transition: { duration: 0.15 } }}
      transition={{ duration: 0.22, ease: [0.22, 1, 0.36, 1] }}
    />
  )}
</AnimatePresence>
```

**Liste kademeleme (stagger)** — öğe başı 30–50ms, toplam ≤ 300ms; 10+ öğede yalnızca ilk birkaçını kademele.

**Paylaşılan öğe / layout** — `layoutId` ile sekme göstergesi, kart → detay geçişi.

**Sayfa geçişleri** — destekleyen tarayıcıda View Transitions API (`document.startViewTransition`),
yoksa basit fade.

**Kaydırma tetikli** — `IntersectionObserver` veya `whileInView` + `viewport={{ once: true }}`;
yalnızca bir kez ve ince. Scroll-jacking yapma.

## Erişilebilirlik

- `prefers-reduced-motion: reduce` → kayma/ölçek animasyonlarını kaldır, yalnızca opaklık
  bırak veya anında geçiş. Framer'da `useReducedMotion()` ya da `<MotionConfig reducedMotion="user">`.
- 5 saniyeden uzun otomatik hareket (carousel, marquee) durdurulabilir olmalı.
- Saniyede 3'ten fazla yanıp sönme yok.

## Performans

- Animasyon sırasında layout tetikleme (ölçüm + yazma döngüsü) yok.
- `will-change` yalnızca animasyon süresince; kalıcı bırakma.
- Kütüphane boyutu: basit geçiş için CSS yeter; Framer Motion'ı `LazyMotion` + `domAnimation` ile yükle.
