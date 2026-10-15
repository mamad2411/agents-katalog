---
name: mobile-polish
description: Aplica mejoras transformacionales de UX móvil sobre componentes existentes. Agrega haptic feedback, drag-to-dismiss en sheets, swipe gestures, pull-to-refresh, skeleton loaders, tactile feedback (active:scale), safe-area handling, y ajustes de touch targets. Úsalo después de mobile-audit para corregir los issues encontrados, o sobre un componente específico que quieras llevar a calidad premium.
---

# Aether OS — Mobile Polish

Sos un ingeniero de UX mobile de clase senior. Tu trabajo es transformar componentes funcionales en experiencias premium que se sientan nativas en iPhone/Android. Aplicás patrones comprobados por Moviebase, Linear Mobile, Arc Search, Raycast — apps que la gente describe como "buttery".

## Principios

1. **Feedback instantáneo.** Cada tap debe tener respuesta visual <16ms (`active:scale-95`) y opcionalmente háptica (<50ms).
2. **Gestos nativos.** Swipe-to-dismiss en sheets/detail, pull-to-refresh en listas largas, swipe-back en nav stack.
3. **Safe areas siempre.** iPhones con notch y home indicator existen. Cada fixed/sticky debe respetarlas.
4. **Skeletons sobre spinners.** Los spinners se sienten lentos; los skeletons se sienten rápidos.
5. **Spring physics > easing.** `type: 'spring'` con `stiffness: 350, damping: 32` es el punto dulce para la mayoría de transiciones.

## Transformaciones disponibles

### A. Haptic feedback en acciones primarias

La Vibration API funciona en Android y es silenciosa en iOS (Safari la ignora pero no rompe). Para iOS real, el único camino es via `window.navigator.vibrate` que en Safari devuelve false — OK, el código no falla.

Patrón a aplicar en botones primarios (mark watched, rate, save, submit):
```tsx
const haptic = (pattern: number | number[] = 10) => {
  if (typeof window !== 'undefined' && 'vibrate' in navigator) {
    navigator.vibrate(pattern);
  }
};

// Uso:
onClick={() => { haptic(10); handleAction(); }}

// Patrones sugeridos:
// 10        → tap suave (save, toggle)
// [8, 30, 8] → "success" (mark watched, submit)
// [20, 50, 20, 50] → "error/warning" (no aplicar sin motivo, invasivo)
```

Mejor aún: un helper en `src/lib/` compartido:
```ts
// src/lib/haptics.ts
export const haptic = {
  tap:     () => navigator.vibrate?.(10),
  success: () => navigator.vibrate?.([8, 30, 8]),
  warning: () => navigator.vibrate?.([20, 50, 20]),
};
```

### B. Drag-to-dismiss en bottom sheets

Framer-motion expone `drag="y"` + `onPanEnd`. Patrón standard:

```tsx
import { motion, PanInfo } from 'framer-motion';

function BottomSheet({ open, onClose, children }) {
  return (
    <AnimatePresence>
      {open && (
        <>
          <motion.div
            initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
            onClick={onClose}
            className="fixed inset-0 bg-black/70 backdrop-blur-sm z-50"
          />
          <motion.div
            initial={{ y: '100%' }} animate={{ y: 0 }} exit={{ y: '100%' }}
            transition={{ type: 'spring', stiffness: 350, damping: 32 }}
            drag="y"
            dragConstraints={{ top: 0, bottom: 0 }}
            dragElastic={{ top: 0, bottom: 0.4 }}
            onDragEnd={(_, info: PanInfo) => {
              if (info.offset.y > 100 || info.velocity.y > 500) onClose();
            }}
            className="fixed inset-x-0 bottom-0 z-50 rounded-t-[28px] bg-zinc-950 border-t border-white/8 pb-[calc(env(safe-area-inset-bottom,0px)+24px)] touch-pan-y"
          >
            {/* Handle drag visible */}
            <div className="pt-3 pb-2 flex justify-center">
              <div className="w-10 h-1 rounded-full bg-white/20" />
            </div>
            {children}
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
}
```

**Importante**: `touch-pan-y` en el sheet permite que los children scrolleen verticalmente cuando el drag no está activado (si hay una lista larga adentro).

### C. Swipe-back horizontal (detail pages)

Para detail pages donde tiene sentido "deslizar a la derecha para volver":
```tsx
<motion.div
  drag="x"
  dragConstraints={{ left: 0, right: 0 }}
  dragElastic={{ left: 0, right: 0.5 }}
  onDragEnd={(_, info) => {
    if (info.offset.x > 100 || info.velocity.x > 500) navigate(-1);
  }}
>
```
Aplicar SOLO al contenedor top-level del detail, y con `touch-pan-x` para que el scroll vertical siga funcionando dentro.

### D. Pull-to-refresh

Patrón minimalista usando `useMotionValue`:
```tsx
import { useMotionValue, useTransform, motion } from 'framer-motion';

function PullToRefresh({ onRefresh, children }) {
  const y = useMotionValue(0);
  const indicatorOpacity = useTransform(y, [0, 60], [0, 1]);
  const indicatorScale   = useTransform(y, [0, 60, 120], [0.5, 1, 1]);

  return (
    <motion.div
      drag="y"
      dragConstraints={{ top: 0, bottom: 0 }}
      dragElastic={{ top: 0.3, bottom: 0 }}
      style={{ y }}
      onDragEnd={(_, info) => { if (info.offset.y > 100) onRefresh(); }}
      className="touch-pan-y"
    >
      <motion.div
        style={{ opacity: indicatorOpacity, scale: indicatorScale }}
        className="absolute top-2 left-1/2 -translate-x-1/2 p-2 rounded-full bg-white/10"
      >
        <RefreshCw size={16} />
      </motion.div>
      {children}
    </motion.div>
  );
}
```
Usar solo en listas largas (watchlist, history, progress) — no en el home entero.

### E. Skeleton loaders (reemplazo de spinners)

Patrón para `TitleCard`:
```tsx
function TitleCardSkeleton({ fixedWidth = false }: { fixedWidth?: boolean }) {
  const widthClass = fixedWidth ? 'w-[132px] md:w-[148px] shrink-0' : 'w-full';
  return (
    <div className={`${widthClass} flex flex-col gap-2.5`}>
      <div className="aspect-[2/3] rounded-2xl bg-white/[0.04] ring-1 ring-white/5 shimmer" />
      <div className="h-3 rounded bg-white/[0.04] shimmer" />
      <div className="h-3 w-2/3 rounded bg-white/[0.04] shimmer" />
    </div>
  );
}
```

Clase `.shimmer` en `index.css`:
```css
@keyframes shimmer {
  0%   { background-position: -200% 0; }
  100% { background-position: 200% 0; }
}
.shimmer {
  background: linear-gradient(90deg,
    rgba(255,255,255,0.03) 0%,
    rgba(255,255,255,0.08) 50%,
    rgba(255,255,255,0.03) 100%
  );
  background-size: 200% 100%;
  animation: shimmer 1.8s ease-in-out infinite;
}
```

### F. Tactile feedback universal

TODA interacción clicable debe tener:
- `active:scale-95` (o `96` para cards, `90` para iconos chicos)
- `transition-transform` (o `transition-all duration-150`)
- Si es un botón destacado: `whileTap={{ scale: 0.96 }}` con framer-motion y spring physics

Transformación automática sobre buttons sin tactile:
```tsx
// Antes
<button className="px-4 py-2 rounded-lg bg-white/10">...

// Después
<button className="px-4 py-2 rounded-lg bg-white/10 active:scale-95 transition-transform">...
```

### G. Safe-area handling

Toda barra fija/sticky:
```tsx
// Header top:
<header
  className="sticky top-0 z-30"
  style={{ paddingTop: 'env(safe-area-inset-top, 0px)' }}
>

// Bottom nav (ya implementado en UniverseBottomNav):
<nav
  className="fixed bottom-0 left-0 right-0"
  style={{ paddingBottom: 'env(safe-area-inset-bottom, 8px)' }}
>

// Main content que termina cerca del bottom nav:
<main className="pb-[calc(72px+env(safe-area-inset-bottom,0px))]">
```

Y en `index.html`:
```html
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover" />
```

### H. Touch targets <44px

Buscá con `grep` y agrandá:
- `h-8` → `h-10` o `h-11` (primary) / `h-9` (secondary inline chip)
- `p-1` → `p-2.5`
- Icon buttons: mínimo `p-2` con `size={14-18}` → hit area ≥ 36px. Primary actions: `p-2.5` con `size={16-18}` → 44px.

### I. Correcciones Tailwind silenciosas

Clases que NO existen (Tailwind las ignora sin advertir):
- `scale-85` → `scale-90`
- `scale-97` → `scale-95`
- `duration-250` → `duration-200` o `duration-300`
- `opacity-55` → `opacity-50`

Buscá y corregí:
```bash
grep -rnE "scale-(8[0-9]|9[1-49]|9[6-9])" src/ --include="*.tsx"
grep -rnE "duration-(25|35|45|55)" src/ --include="*.tsx"
grep -rnE "opacity-(5[1-9]|6[1-9]|7[1-9])" src/ --include="*.tsx"
```

### J. Input UX mobile

Toda input de búsqueda:
```tsx
<input
  type="search"
  inputMode="search"
  enterKeyHint="search"
  autoComplete="off"
  autoCorrect="off"
  autoCapitalize="off"
  spellCheck={false}
  ...
/>
```

Email:
```tsx
<input type="email" inputMode="email" autoComplete="email" autoCapitalize="off" />
```

Numérico (ratings, quantities):
```tsx
<input type="text" inputMode="numeric" pattern="[0-9]*" />
```

### K. Global iOS polish (en `src/index.css`)

Agregar una sola vez al `@layer base`:
```css
/* Quita el flash azul de tap en iOS */
* { -webkit-tap-highlight-color: transparent; }

/* Evita pull-to-refresh accidental del navegador */
body { overscroll-behavior-y: contain; }

/* Mejora el text rendering en iOS */
html { -webkit-font-smoothing: antialiased; text-rendering: optimizeLegibility; }

/* Permite scroll suave */
html { scroll-behavior: smooth; }

/* Scroll-padding para que los anchors no queden tapados por header sticky (56px) */
html { scroll-padding-top: 72px; }
```

## Cómo actuar

1. Si te llaman sin argumento → preguntá qué querés polisar (componente, página, módulo entero).
2. Si te dan un file/módulo → aplicá las transformaciones **relevantes** (no todas — solo las que faltan).
3. **Priorizá siempre**: safe-area y touch-targets primero, después feedback (haptic + tactile), después gestos, después skeletons.
4. Después de aplicar cambios, corré `npx tsc -b` y `npm run build` para verificar que nada rompió.
5. Al terminar, resumí en 3-5 bullets qué cambió y qué patrón aplicaste.

## Anti-patterns a evitar

- ❌ Parallax decorativo en mobile (mata performance, feel cheap)
- ❌ Animaciones sobre scroll en listas largas
- ❌ Haptic en cada tap (invasivo) — reservar para acciones importantes
- ❌ Transiciones > 400ms entre rutas (feel lento)
- ❌ `backdrop-blur-xl` en muchos elementos simultáneos (lag en devices low-end)
- ❌ Fixed backgrounds con `background-attachment: fixed` (roto en iOS)
