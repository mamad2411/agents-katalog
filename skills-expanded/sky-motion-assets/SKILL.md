---
name: sky-motion-assets
description: >-
  Hazır animasyon varlıkları: Lottie (dotLottie), Rive (etkileşimli state machine
  animasyonları), animasyonlu SVG ve CSS keyframe illüstrasyonları, animasyonlu ikonlar,
  mikro kutlama animasyonları, yükleme/başarı/boş durum animasyonları, dosya boyutu ve
  performans, tembel yükleme, reduced-motion karşılıkları ve kaynak siteler. "Lottie ekle",
  "Rive", "animasyonlu illüstrasyon", "hareketli ikon", "başarı animasyonu" dendiğinde kullan.
disable-model-invocation: true
---

# Sky · Animasyon Varlıkları

Kod tabanlı UI hareketi `sky-motion`'da; burada **tasarımcıların hazırladığı** veya hazır kütüphanelerden gelen animasyonlar.

## Seçim

| İhtiyaç | Format |
|---|---|
| After Effects'ten gelen illüstrasyon animasyonu, döngü | **Lottie** (`.lottie` = sıkıştırılmış dotLottie) |
| Etkileşimli (hover/tıklama/kaydırmaya tepki veren), state machine | **Rive** (`.riv`) — küçük, hızlı, çok etkileyici |
| Basit ikon/logo animasyonu | **SVG + CSS** (stroke-dashoffset, transform) |
| Fotoğraf gerçekliğinde döngü | Video (WebM/MP4, sessiz, poster) |
| Karmaşık zaman çizelgesi, kaydırma hikâyesi | GSAP + SVG |

## Lottie

```tsx
import { DotLottieReact } from "@lottiefiles/dotlottie-react";
<DotLottieReact src="/anim/success.lottie" autoplay loop={false} style={{ width: 120, height: 120 }} />
```
- `.lottie` (dotLottie) JSON'dan ~%80 küçük; tema/renk değiştirme destekler.
- Dosya bütçesi: UI animasyonu ≤ 50KB, kahraman ≤ 200KB. LottieFiles'ta "optimize" et.
- Görünür olunca oynat, ekrandan çıkınca dur; oyuncu kütüphanesini `dynamic()` ile yükle.
- Kaynak: LottieFiles (lisansı kontrol et), IconScout; marka renklerine uyarla.

## Rive (insanların "bu nasıl yapıldı?" dediği)

```tsx
import { useRive, useStateMachineInput } from "@rive-app/react-canvas";
const { rive, RiveComponent } = useRive({ src: "/anim/mascot.riv", stateMachines: "Main", autoplay: true });
const hover = useStateMachineInput(rive, "Main", "isHovering");
<RiveComponent onMouseEnter={() => hover && (hover.value = true)} onMouseLeave={() => hover && (hover.value = false)} />
```
- Maskot form hatasında üzülür, başarıda zıplar; giriş formunda parolayı yazarken gözlerini kapatan ayıcık — klasik örnek.
- Butonlar, toggle'lar, ilerleme göstergeleri state machine ile — tek dosyada tüm durumlar.
- Dosyalar çok küçük (genelde 10–50KB); runtime ~150KB (WASM) — yalnızca kullanılan sayfada yükle.

## SVG + CSS

```css
.check path { stroke-dasharray: 48; stroke-dashoffset: 48; animation: draw .4s var(--ease-out) forwards .1s; }
@keyframes draw { to { stroke-dashoffset: 0; } }
```
Çizilerek beliren ✓, dönen yükleme halkası, nefes alan logo, dalgalanan ses dalgası — sıfır kütüphane.

## Nerede kullanılır (doz önemli)

- ✅ Başarı anı (ödeme, ilk randevu), boş durum (hafif döngü), yükleme (kısa), onboarding adımları, 404 sayfası, hover mikro etkileşimleri.
- ❌ Her kartın içinde, sürekli dikkat çeken döngüler, okuma alanının yanında, kritik bilgiyi geciktiren girişler.
Bir ekranda en fazla **bir** dikkat çeken animasyon.

## Erişilebilirlik ve performans

- `prefers-reduced-motion` → ilk/son kareyi statik göster (Lottie `autoplay={!reduced}`; Rive state "static").
- Döngü ≥ 5 sn ise durdurma kontrolü; yanıp sönme yok (3/sn sınırı).
- Dekoratifse `aria-hidden`; anlam taşıyorsa (başarı) metinle birlikte (`role="status"` "Ödeme alındı").
- Ana thread: Lottie SVG renderer çok katmanlı animasyonda ağır → canvas renderer veya Rive.
- LCP öğesi animasyon olmasın; poster/statik versiyon önce.
