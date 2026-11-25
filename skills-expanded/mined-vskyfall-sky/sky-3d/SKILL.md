---
name: sky-3d
description: >-
  Web'de 3D ve etkileyici görseller: Three.js / React Three Fiber / drei ile hero sahneleri,
  ürün görüntüleyici (döndür, yakınlaştır, renk değiştir), model-viewer ile AR, GLTF modelleri
  ve sıkıştırma (Meshopt, KTX2), Spline gömme, shader gradyan arka planlar, scroll ile senkron
  3D, performans bütçesi, düşük güçlü cihaz fallback'i ve erişilebilirlik. "3D ekle",
  "etkileyici hero", "ürünü döndürülebilir göster", "Three.js" dendiğinde kullan.
disable-model-invocation: true
---

# Sky · 3D

3D insanları etkiler ama pahalıdır: her 3D öğe **bir amaca** hizmet etsin ve sayfa onsuz da çalışsın.

## Araç seçimi

| İhtiyaç | Araç |
|---|---|
| Kod yazmadan tasarımcı sahnesi | **Spline** — hızlı, ama ağır runtime |
| React projesinde özel sahne | **React Three Fiber** + **drei** |
| Ürün görüntüleyici + AR (telefonda odaya yerleştir) | **`<model-viewer>`** — tek etiket |
| Gradyan/akışkan arka plan | Shader (R3F `shaderMaterial`) veya CSS gradyan animasyonu |
| 2D ama derinlik hissi | CSS 3D transform, paralaks, Rive (bkz. `sky-motion-assets`) |

## R3F iskeleti

```tsx
const Scene = dynamic(() => import("./Scene"), { ssr: false, loading: () => <HeroPoster /> });

// Scene.tsx
<Canvas dpr={[1, 1.75]} camera={{ position: [0, 0, 4], fov: 40 }} frameloop="demand">
  <Suspense fallback={null}>
    <Environment preset="city" />
    <Float speed={1.4} rotationIntensity={0.4}><Model /></Float>
    <ContactShadows opacity={0.4} blur={2.4} />
  </Suspense>
  <OrbitControls enableZoom={false} enablePan={false} autoRotate autoRotateSpeed={0.6} />
  <PerformanceMonitor onDecline={() => setDpr(1)} />
</Canvas>
```
`frameloop="demand"`: yalnızca değişince çiz → pil dostu.

## Model hazırlığı (en çok kazandıran adım)

- Blender'dan **GLB**; `gltf-transform optimize model.glb out.glb --compress meshopt --texture-compress webp`.
- Hedef: hero modeli **≤ 2MB**, poligon ≤ 100k, doku ≤ 2048px.
- `npx gltfjsx out.glb --types --transform` ile React bileşenine çevir.
- Işığı dokuya "bake" et → gerçek zamanlı ışık maliyeti düşer, görünüm güzelleşir.

## İnsanların sevdiği etkileşimler

- **Fareyi takip eden** hafif eğim (pointer'a lerp) — canlı hissettirir.
- **Ürün yapılandırıcı:** renk/malzeme seçince model anında değişir.
- **Scroll ile hikâye:** drei `ScrollControls` ile kamera yolculuğu.
- **Patlatılmış görünüm:** hover'da parçalar ayrılır — teknik ürünlerde etkileyici.
- **AR butonu:** `<model-viewer ar ar-modes="webxr scene-viewer quick-look">` — "odanda gör".

## Performans bütçesi

- Canvas ekrana girince başlasın, çıkınca dursun.
- `dpr` maks 1.75–2; mobilde gölge kalitesini düşür; draw call ≤ 100 (`Instances`).
- İlk boya için **poster görseli** → LCP bu görsel olur, 3D sonra canlanır.
- three ~600KB; yalnızca 3D olan route'ta yükle.

## Fallback ve erişilebilirlik

- WebGL yok / düşük güç (`hardwareConcurrency <= 4`, `saveData`) / `prefers-reduced-motion` → statik görsel veya video.
- Canvas yanında metinsel içerik; canvas `aria-hidden` veya `role="img" aria-label`.
- Otomatik dönme reduced-motion'da kapalı; döndür/sıfırla butonları klavyeyle erişilebilir.
- Scroll-jacking yok; zoom sayfa kaydırmasını engellemesin.

## Shader arka planlar (ucuz "vay")

Tam ekran plane + gürültü tabanlı gradyan shader: ~5KB, 60fps, markaya özel renkler; reduced-motion'da zamanı dondur.
CSS alternatifi: çoklu `radial-gradient` + yavaş `@property` animasyonu.
