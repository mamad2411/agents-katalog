---
name: 3d-immersive
description: Build stunning 3D/immersive websites using React Three Fiber, Spline, GSAP ScrollTrigger, and Lenis. Triggers on "3D", "immersive", "interactive 3D", "scroll animation", "particle", "WebGL", "cinematic".
user_invocable: true
---

# 3D / Immersive Website Skill — The Complete Toolbox

Build stunning, performance-optimized 3D and immersive web experiences. Two tiers:
**Tier 1** (Spline + GSAP) for decorative 3D, **Tier 2** (React Three Fiber) for interactive 3D.

This skill is the **toolbox** — every technique, code template, and implementation pattern. For design philosophy, brand application, and audit checklists, see `overkill-web-design`.

---

## Non-Negotiables

1. **60fps desktop, graceful degradation mobile.** Never ship janky scroll or canvas.
2. **Visible loading skeleton for all 3D.** Never show a blank canvas — always `<Suspense fallback={<LoadingSkeleton />}>`.
3. **Mandatory mobile fallback.** CSS gradient or static image replaces 3D on mobile/low-end devices.
4. **`prefers-reduced-motion`** disables animations and 3D autoplay.
5. **3D components lazy-loaded** via `next/dynamic` or `React.lazy` — never block initial paint.
6. **Lenis smooth scroll** as the outermost wrapper for any scroll-driven site.
7. **All GSAP ScrollTriggers + Lenis cleaned up** in `useEffect` return — no leaked listeners.
8. **Film grain on dark themes.** Every dark-themed site gets an SVG noise overlay (opacity 0.03-0.06). Zero cost, instant premium.
9. **Split-text stagger on hero headings.** GSAP SplitText (free in 3.12+) with per-char or per-word reveal. The #1 Awwwards signature.
10. **Custom cursor on desktop.** Mix-blend-mode: difference circle, context-aware (changes on hover targets). Hidden on touch/mobile.
11. **Memory management.** Dispose geometries, materials, and textures in cleanup functions. Three.js does NOT garbage-collect GPU resources.
12. **Lenis + ScrollControls conflict.** NEVER use Lenis and drei's `<ScrollControls>` together — they fight over scroll ownership. Use one or the other.

---

## Decision Framework

| Signal | Approach |
|--------|----------|
| Landing page, portfolio, marketing site | **Tier 1** (Spline + GSAP) or **Tier 2** if interactive |
| Data visualization, configurator, interactive experience | **Tier 2** (React Three Fiber) |
| Game, simulation, physics | **Tier 2** + rapier |
| Decorative 3D background | **Tier 1** (Spline embed) or R3F gradient mesh |
| User interacts WITH 3D objects | **Tier 2** |
| Dashboard / data viz | Split text + page transitions only |
| Admin panel / CRUD | None of this |

**Spline limitation:** The builder cannot create Spline scenes — it can only embed existing ones via URL. When no Spline URL is available, default to building the scene in R3F code (Tier 2).

**Technique Selection Matrix:**

| Project Type | Tier 1 (mandatory) | Tier 2 (elevated) | Tier 3 (showcase) |
|---|---|---|---|
| Landing page | Split-text, grain, cursor, smooth scroll | Preloader, Magnetic, Parallax | Cursor mask |
| Portfolio | ALL | ALL | Distortion, Mask |
| Marketing site | ALL | Preloader, Parallax | Optional |
| Interactive experience | ALL | ALL | Camera dolly, PostProc |
| Product showcase | ALL | Magnetic, Parallax | Distortion |

---

## Pinned Package Versions

Always use these versions to prevent API hallucination:

```
@react-three/fiber: ^10.0.0
@react-three/drei: ^10.0.0
@react-three/postprocessing: ^3.0.0
@react-three/rapier: ^2.0.0
three: ^0.170.0
postprocessing: ^7.0.0
@splinetool/react-spline: ^4.0.0
gsap: ^3.12.0
lenis: ^1.1.0
framer-motion: ^11.0.0
r3f-perf: ^8.0.0
howler: ^2.2.4
```

> **Note:** GSAP SplitText is bundled free with `gsap@^3.12.0` — no separate install needed.
> **Note:** `hover-effect` (^1.0.0) is legacy and may need manual patching for ESM. Consider CSS-based distortion alternatives for new projects.

---

## Foundation Code Templates

### Lenis Smooth Scroll Provider

```tsx
// components/SmoothScroll.tsx
"use client";
import { ReactLenis } from "lenis/react";

export function SmoothScroll({ children }: { children: React.ReactNode }) {
  return (
    <ReactLenis
      root
      options={{
        lerp: 0.1,
        duration: 1.2,
        smoothWheel: true,
      }}
    >
      {children}
    </ReactLenis>
  );
}
```

### Lenis + GSAP Sync (CRITICAL)

```tsx
// lib/gsap-lenis-sync.ts
"use client";
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";

gsap.registerPlugin(ScrollTrigger);

/**
 * Call once at app level (e.g., in layout or root component).
 * Syncs Lenis smooth scroll with GSAP ScrollTrigger.
 */
export function initGsapLenisSync(lenisInstance: any) {
  lenisInstance.on("scroll", ScrollTrigger.update);

  gsap.ticker.add((time) => {
    lenisInstance.raf(time * 1000);
  });
  gsap.ticker.lagSmoothing(0);
}
```

### Mobile Detection Hook

```tsx
// hooks/useIs3DCapable.ts
"use client";
import { useState, useEffect } from "react";

export function useIs3DCapable() {
  const [capable, setCapable] = useState(true);

  useEffect(() => {
    const isMobile = window.innerWidth < 768;
    const isLowEnd = navigator.hardwareConcurrency < 4;
    const prefersReduced = window.matchMedia(
      "(prefers-reduced-motion: reduce)"
    ).matches;
    setCapable(!isMobile && !isLowEnd && !prefersReduced);
  }, []);

  return capable;
}
```

### Reduced-Motion Hook

```tsx
// hooks/useReducedMotion.ts
"use client";
import { useState, useEffect } from "react";

export function useReducedMotion() {
  const [reduced, setReduced] = useState(false);

  useEffect(() => {
    const mq = window.matchMedia("(prefers-reduced-motion: reduce)");
    setReduced(mq.matches);
    const handler = (e: MediaQueryListEvent) => setReduced(e.matches);
    mq.addEventListener("change", handler);
    return () => mq.removeEventListener("change", handler);
  }, []);

  return reduced;
}
```

**Reduced-motion strategy:**

| Full Animation | Reduced Alternative |
|---------------|---------------------|
| Split-text stagger (1.2s) | Instant opacity 0->1 (0.3s) |
| Parallax scroll layers | Static layered composition (still has depth via z-index + scale) |
| 3D rotating model | Static hero image with subtle CSS shadow |
| Scroll-pinned sections | Normal scroll, content visible immediately |
| Preloader animation | Brief fade-in (0.5s) |
| Magnetic buttons | Standard hover scale (CSS transform) |
| Custom cursor | System cursor (hidden entirely) |
| Film grain animation | Static noise texture (single frame) |

**Rule:** Reduced motion != reduced quality. The site should still look premium — just with opacity/color transitions instead of movement.

### Mouse-Tracking Parallax Hook

```tsx
// hooks/useMouseParallax.ts
"use client";
import { useState, useEffect } from "react";

export function useMouseParallax(intensity = 0.02) {
  const [position, setPosition] = useState({ x: 0, y: 0 });

  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      const x = (e.clientX / window.innerWidth - 0.5) * intensity;
      const y = (e.clientY / window.innerHeight - 0.5) * intensity;
      setPosition({ x, y });
    };
    window.addEventListener("mousemove", handleMouseMove);
    return () => window.removeEventListener("mousemove", handleMouseMove);
  }, [intensity]);

  return position;
}
```

### Scroll Progress Hook

```tsx
// hooks/useScrollProgress.ts
"use client";
import { useState, useEffect } from "react";

export function useScrollProgress() {
  const [progress, setProgress] = useState(0);

  useEffect(() => {
    const handleScroll = () => {
      const scrollTop = window.scrollY;
      const docHeight = document.documentElement.scrollHeight - window.innerHeight;
      setProgress(docHeight > 0 ? scrollTop / docHeight : 0);
    };

    window.addEventListener("scroll", handleScroll, { passive: true });
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  return progress;
}
```

---

## Tier 1: Spline + GSAP Templates

### Spline Embed with Suspense

```tsx
// components/SplineScene.tsx
"use client";
import { Suspense, lazy } from "react";
import { useIs3DCapable } from "@/hooks/useIs3DCapable";

const Spline = lazy(() => import("@splinetool/react-spline"));

function LoadingSkeleton() {
  return (
    <div className="canvas-loading">
      <span className="sr-only">Loading 3D scene...</span>
    </div>
  );
}

function FallbackHero() {
  return <div className="hero-fallback" aria-label="Decorative background" />;
}

export function SplineScene({ url }: { url: string }) {
  const is3D = useIs3DCapable();

  if (!is3D) return <FallbackHero />;

  return (
    <div className="canvas-container">
      <Suspense fallback={<LoadingSkeleton />}>
        <Spline scene={url} />
      </Suspense>
    </div>
  );
}
```

### GSAP ScrollTrigger Reveal Hook

```tsx
// hooks/useScrollReveal.ts
"use client";
import { useEffect, useRef } from "react";
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";

gsap.registerPlugin(ScrollTrigger);

export function useScrollReveal<T extends HTMLElement>(
  options: { y?: number; duration?: number; delay?: number } = {}
) {
  const ref = useRef<T>(null);
  const { y = 60, duration = 0.8, delay = 0 } = options;

  useEffect(() => {
    const el = ref.current;
    if (!el) return;

    const prefersReduced = window.matchMedia(
      "(prefers-reduced-motion: reduce)"
    ).matches;
    if (prefersReduced) return;

    const tween = gsap.from(el, {
      y,
      opacity: 0,
      duration,
      delay,
      ease: "power2.out",
      scrollTrigger: {
        trigger: el,
        start: "top 85%",
        toggleActions: "play none none none",
      },
    });

    return () => {
      tween.kill();
      ScrollTrigger.getAll().forEach((st) => {
        if (st.trigger === el) st.kill();
      });
    };
  }, [y, duration, delay]);

  return ref;
}
```

### GSAP Pin Section Hook

```tsx
// hooks/usePinSection.ts
"use client";
import { useEffect, useRef } from "react";
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";

gsap.registerPlugin(ScrollTrigger);

export function usePinSection<T extends HTMLElement>(
  options: { endOffset?: string } = {}
) {
  const ref = useRef<T>(null);
  const { endOffset = "+=100%" } = options;

  useEffect(() => {
    const el = ref.current;
    if (!el) return;

    const st = ScrollTrigger.create({
      trigger: el,
      pin: true,
      start: "top top",
      end: endOffset,
      pinSpacing: true,
    });

    return () => st.kill();
  }, [endOffset]);

  return ref;
}
```

### Split-Text Reveal Hook

```tsx
// hooks/useSplitTextReveal.ts
"use client";
import { useEffect, useRef } from "react";
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { SplitText } from "gsap/SplitText";

gsap.registerPlugin(ScrollTrigger, SplitText);

interface SplitTextOptions {
  type?: "chars" | "words" | "lines";
  stagger?: number;
  duration?: number;
  y?: number;
  clipMask?: boolean; // premium: overflow:hidden + slideUp per line
}

export function useSplitTextReveal<T extends HTMLElement>(
  options: SplitTextOptions = {}
) {
  const ref = useRef<T>(null);
  const {
    type = "words",
    stagger = 0.05,
    duration = 0.8,
    y = 40,
    clipMask = true,
  } = options;

  useEffect(() => {
    const el = ref.current;
    if (!el) return;

    const prefersReduced = window.matchMedia(
      "(prefers-reduced-motion: reduce)"
    ).matches;

    if (prefersReduced) {
      gsap.from(el, {
        opacity: 0,
        duration: 0.5,
        scrollTrigger: { trigger: el, start: "top 85%" },
      });
      return;
    }

    const split = new SplitText(el, { type });
    const targets =
      type === "chars" ? split.chars : type === "words" ? split.words : split.lines;

    if (clipMask) {
      targets.forEach((t: HTMLElement) => {
        t.style.overflow = "hidden";
        t.style.display = "inline-block";
      });
    }

    gsap.from(targets, {
      y,
      opacity: clipMask ? 1 : 0,
      duration,
      stagger,
      ease: "power3.out",
      scrollTrigger: {
        trigger: el,
        start: "top 85%",
        toggleActions: "play none none none",
      },
    });

    return () => {
      split.revert();
      ScrollTrigger.getAll().forEach((st) => {
        if (st.trigger === el) st.kill();
      });
    };
  }, [type, stagger, duration, y, clipMask]);

  return ref;
}
```

### Film Grain Overlay

```tsx
// components/FilmGrain.tsx
"use client";
import { useEffect, useRef } from "react";

export function FilmGrain({ opacity = 0.04 }: { opacity?: number }) {
  const seedRef = useRef(0);
  const baseRef = useRef<SVGFETurbulenceElement>(null);

  useEffect(() => {
    const prefersReduced = window.matchMedia(
      "(prefers-reduced-motion: reduce)"
    ).matches;
    if (prefersReduced) return;

    let raf: number;
    const animate = () => {
      seedRef.current += 1;
      if (baseRef.current) {
        baseRef.current.setAttribute("seed", String(seedRef.current % 100));
      }
      raf = requestAnimationFrame(animate);
    };
    raf = requestAnimationFrame(animate);
    return () => cancelAnimationFrame(raf);
  }, []);

  return (
    <svg
      className="film-grain"
      style={{
        position: "fixed",
        inset: 0,
        width: "100%",
        height: "100%",
        zIndex: 9999,
        pointerEvents: "none",
        opacity,
        mixBlendMode: "overlay",
      }}
    >
      <filter id="grain-filter">
        <feTurbulence
          ref={baseRef}
          type="fractalNoise"
          baseFrequency="0.65"
          numOctaves="3"
          stitchTiles="stitch"
        />
      </filter>
      <rect width="100%" height="100%" filter="url(#grain-filter)" />
    </svg>
  );
}
```

### Custom Cursor

```tsx
// components/CustomCursor.tsx
"use client";
import { useEffect, useRef } from "react";
import gsap from "gsap";

export function CustomCursor() {
  const outerRef = useRef<HTMLDivElement>(null);
  const dotRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if ("ontouchstart" in window) return;

    const outer = outerRef.current;
    const dot = dotRef.current;
    if (!outer || !dot) return;

    const xOuter = gsap.quickTo(outer, "x", { duration: 0.35, ease: "power3" });
    const yOuter = gsap.quickTo(outer, "y", { duration: 0.35, ease: "power3" });
    const xDot = gsap.quickTo(dot, "x", { duration: 0.15, ease: "power3" });
    const yDot = gsap.quickTo(dot, "y", { duration: 0.15, ease: "power3" });

    const onMouseMove = (e: MouseEvent) => {
      xOuter(e.clientX - 20);
      yOuter(e.clientY - 20);
      xDot(e.clientX - 3);
      yDot(e.clientY - 3);
    };

    const onMouseOver = (e: MouseEvent) => {
      const target = (e.target as HTMLElement).closest("[data-cursor]");
      if (!target) return;
      const cursorType = target.getAttribute("data-cursor");
      if (cursorType === "expand") {
        gsap.to(outer, { width: 80, height: 80, x: "-=20", y: "-=20", duration: 0.3 });
      } else if (cursorType === "hide") {
        gsap.to(outer, { scale: 0, duration: 0.2 });
        gsap.to(dot, { scale: 0, duration: 0.2 });
      } else if (cursorType?.startsWith("text:")) {
        outer.textContent = cursorType.slice(5);
        gsap.to(outer, { width: 100, height: 100, x: "-=30", y: "-=30", fontSize: 14, duration: 0.3 });
      }
    };

    const onMouseOut = (e: MouseEvent) => {
      const target = (e.target as HTMLElement).closest("[data-cursor]");
      if (!target) return;
      outer.textContent = "";
      gsap.to(outer, { width: 40, height: 40, scale: 1, fontSize: 0, duration: 0.3 });
      gsap.to(dot, { scale: 1, duration: 0.2 });
    };

    window.addEventListener("mousemove", onMouseMove);
    document.addEventListener("mouseover", onMouseOver);
    document.addEventListener("mouseout", onMouseOut);

    return () => {
      window.removeEventListener("mousemove", onMouseMove);
      document.removeEventListener("mouseover", onMouseOver);
      document.removeEventListener("mouseout", onMouseOut);
    };
  }, []);

  return (
    <>
      <div
        ref={outerRef}
        className="custom-cursor custom-cursor__outer"
        style={{
          position: "fixed",
          top: 0,
          left: 0,
          width: 40,
          height: 40,
          border: "1px solid white",
          borderRadius: "50%",
          zIndex: 10000,
          pointerEvents: "none",
          mixBlendMode: "difference",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          color: "white",
          fontSize: 0,
        }}
      />
      <div
        ref={dotRef}
        className="custom-cursor"
        style={{
          position: "fixed",
          top: 0,
          left: 0,
          width: 6,
          height: 6,
          background: "white",
          borderRadius: "50%",
          zIndex: 10000,
          pointerEvents: "none",
          mixBlendMode: "difference",
        }}
      />
    </>
  );
}
```

### Magnetic Button

```tsx
// components/MagneticButton.tsx
"use client";
import { useRef, useState, useCallback } from "react";

interface MagneticButtonProps {
  children: React.ReactNode;
  className?: string;
  style?: React.CSSProperties;
  onClick?: () => void;
  type?: "button" | "submit" | "reset";
  disabled?: boolean;
  /** Magnetic pull strength in px (default 12). Use 5 for pills, 8-10 for CTAs */
  strength?: number;
  /** Glow color on hover (default gold). Match to button's theme */
  glowColor?: string;
}

/**
 * Premium magnetic button with 5 interactive layers:
 * 1. Magnetic pull — follows cursor with elastic spring-back
 * 2. Radial shine — light follows cursor position inside the button
 * 3. Glow on hover — colored box-shadow matching the button's theme
 * 4. Scale boost — subtle 1.03x scale on hover
 * 5. Smooth easing — fast response on enter (0.15s), smooth elastic return (0.5s)
 */
export function MagneticButton({
  children,
  className = "",
  style,
  onClick,
  type = "button",
  disabled = false,
  strength = 12,
  glowColor = "rgba(201,168,76,0.4)",
}: MagneticButtonProps) {
  const ref = useRef<HTMLButtonElement>(null);
  const [transform, setTransform] = useState("translate(0px, 0px) scale(1)");
  const [glowPos, setGlowPos] = useState({ x: 50, y: 50 });
  const [isHovered, setIsHovered] = useState(false);

  const handleMouseMove = useCallback(
    (e: React.MouseEvent<HTMLButtonElement>) => {
      if (disabled) return;
      const el = ref.current;
      if (!el) return;

      const rect = el.getBoundingClientRect();
      const centerX = rect.left + rect.width / 2;
      const centerY = rect.top + rect.height / 2;
      const deltaX = (e.clientX - centerX) / (rect.width / 2);
      const deltaY = (e.clientY - centerY) / (rect.height / 2);

      setTransform(
        `translate(${deltaX * strength}px, ${deltaY * strength}px) scale(1.03)`
      );
      setGlowPos({
        x: ((e.clientX - rect.left) / rect.width) * 100,
        y: ((e.clientY - rect.top) / rect.height) * 100,
      });
    },
    [disabled, strength]
  );

  const handleMouseLeave = useCallback(() => {
    setTransform("translate(0px, 0px) scale(1)");
    setIsHovered(false);
  }, []);

  const handleMouseEnter = useCallback(() => {
    if (!disabled) setIsHovered(true);
  }, [disabled]);

  return (
    <button
      ref={ref}
      type={type}
      disabled={disabled}
      onClick={onClick}
      onMouseMove={handleMouseMove}
      onMouseLeave={handleMouseLeave}
      onMouseEnter={handleMouseEnter}
      className={`relative overflow-hidden ${className}`}
      style={{
        ...style,
        transform,
        transition: isHovered
          ? "transform 0.15s cubic-bezier(0.25, 0.46, 0.45, 0.94)"
          : "transform 0.5s cubic-bezier(0.16, 1, 0.3, 1)",
        boxShadow: isHovered
          ? `0 0 30px ${glowColor}, 0 4px 15px rgba(0,0,0,0.3), inset 0 1px 0 rgba(255,255,255,0.1)`
          : (style?.boxShadow ?? "0 2px 8px rgba(0,0,0,0.3)"),
      }}
    >
      <div
        className="absolute inset-0 pointer-events-none"
        style={{
          background: isHovered
            ? `radial-gradient(circle at ${glowPos.x}% ${glowPos.y}%, rgba(255,255,255,0.2) 0%, transparent 60%)`
            : "none",
          transition: "background 0.2s ease",
        }}
      />
      <span className="relative z-10">{children}</span>
    </button>
  );
}
```

**Strength guidelines:**
| Element | Strength | Glow Color |
|---------|----------|------------|
| Hero CTA | 12px | Brand primary, 0.5 alpha |
| Standard CTA | 8-10px | Brand primary, 0.4 alpha |
| Feature pills / tags | 5px | Brand accent, 0.3 alpha |
| Nav links | 6px | White, 0.2 alpha |
| Icon buttons | 8px | Match icon color, 0.3 alpha |

### Parallax Layer Hook

```tsx
// hooks/useParallaxLayer.ts
"use client";
import { useEffect, type RefObject } from "react";
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";

gsap.registerPlugin(ScrollTrigger);

export function useParallaxLayer(
  ref: RefObject<HTMLElement | null>,
  options: { speed?: number } = {}
) {
  const { speed = 0.5 } = options;

  useEffect(() => {
    const el = ref.current;
    if (!el) return;

    const prefersReduced = window.matchMedia(
      "(prefers-reduced-motion: reduce)"
    ).matches;
    if (prefersReduced) return;

    const tween = gsap.to(el, {
      y: () => speed * -100,
      ease: "none",
      scrollTrigger: {
        trigger: el,
        start: "top bottom",
        end: "bottom top",
        scrub: true,
      },
    });

    return () => {
      tween.kill();
      ScrollTrigger.getAll().forEach((st) => {
        if (st.trigger === el) st.kill();
      });
    };
  }, [ref, speed]);
}
```

### Page Transition Wrapper

```tsx
// components/PageTransition.tsx
"use client";
import { motion, AnimatePresence } from "framer-motion";
import { usePathname } from "next/navigation";
import { type ReactNode } from "react";

const variants = {
  fade: {
    initial: { opacity: 0 },
    animate: { opacity: 1 },
    exit: { opacity: 0 },
  },
  slideUp: {
    initial: { opacity: 0, y: 20 },
    animate: { opacity: 1, y: 0 },
    exit: { opacity: 0, y: -20 },
  },
  scaleDown: {
    initial: { opacity: 0, scale: 0.95 },
    animate: { opacity: 1, scale: 1 },
    exit: { opacity: 0, scale: 1.05 },
  },
};

interface PageTransitionProps {
  children: ReactNode;
  variant?: keyof typeof variants;
}

/**
 * For Next.js App Router: use in app/template.tsx (NOT layout.tsx).
 * Layout doesn't remount on navigation — template does.
 */
export function PageTransition({
  children,
  variant = "slideUp",
}: PageTransitionProps) {
  const pathname = usePathname();
  const v = variants[variant];

  return (
    <AnimatePresence mode="wait">
      <motion.div
        key={pathname}
        initial={v.initial}
        animate={v.animate}
        exit={v.exit}
        transition={{ duration: 0.4, ease: [0.22, 1, 0.36, 1] }}
      >
        {children}
      </motion.div>
    </AnimatePresence>
  );
}
```

### Curtain Wipe Page Transition

```tsx
// components/CurtainTransition.tsx
"use client";
import { motion, AnimatePresence } from "framer-motion";
import { usePathname } from "next/navigation";

const curtainVariants = {
  initial: { clipPath: "inset(0 0 100% 0)" },
  animate: {
    clipPath: ["inset(0 0 100% 0)", "inset(0 0 0 0)", "inset(100% 0 0 0)"],
    transition: {
      duration: 0.8,
      ease: [0.76, 0, 0.24, 1],
      times: [0, 0.4, 1],
      delay: 0.2,
    },
  },
  exit: {
    clipPath: "inset(0 0 0 0)",
    transition: {
      duration: 0.5,
      ease: [0.76, 0, 0.24, 1],
      delay: 0.2,
    },
  },
};

const contentVariants = {
  initial: { opacity: 0, y: 30 },
  animate: {
    opacity: 1,
    y: 0,
    transition: {
      duration: 0.6,
      delay: 0.5,
      ease: [0.22, 1, 0.36, 1],
    },
  },
  exit: {
    opacity: 0,
    y: -20,
    transition: { duration: 0.3 },
  },
};

export function CurtainTransition({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();

  return (
    <AnimatePresence mode="wait">
      <motion.div key={pathname}>
        <motion.div
          className="fixed inset-0 z-[9999] bg-black pointer-events-none"
          variants={curtainVariants}
          initial="initial"
          animate="animate"
          exit="exit"
        />
        <motion.div
          variants={contentVariants}
          initial="initial"
          animate="animate"
          exit="exit"
        >
          {children}
        </motion.div>
      </motion.div>
    </AnimatePresence>
  );
}
```

### Preloader

```tsx
// components/Preloader.tsx
"use client";
import { useEffect, useRef, useState } from "react";
import gsap from "gsap";

interface PreloaderProps {
  onComplete?: () => void;
}

export function Preloader({ onComplete }: PreloaderProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const counterRef = useRef<HTMLSpanElement>(null);
  const [done, setDone] = useState(false);

  useEffect(() => {
    const prefersReduced = window.matchMedia(
      "(prefers-reduced-motion: reduce)"
    ).matches;

    if (prefersReduced) {
      setDone(true);
      onComplete?.();
      return;
    }

    const tl = gsap.timeline({
      onComplete: () => {
        setDone(true);
        onComplete?.();
      },
    });

    tl.to(
      { val: 0 },
      {
        val: 100,
        duration: 2,
        ease: "power2.inOut",
        onUpdate: function () {
          if (counterRef.current) {
            counterRef.current.textContent = String(Math.round(this.targets()[0].val));
          }
        },
      }
    );

    tl.to(containerRef.current, {
      clipPath: "inset(0 0 100% 0)",
      duration: 0.8,
      ease: "power4.inOut",
    });

    return () => {
      tl.kill();
    };
  }, [onComplete]);

  if (done) return null;

  return (
    <div
      ref={containerRef}
      className="preloader"
      style={{
        position: "fixed",
        inset: 0,
        zIndex: 10001,
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        background: "var(--color-bg, #0a0a0f)",
        clipPath: "inset(0 0 0 0)",
      }}
    >
      <span
        ref={counterRef}
        style={{
          fontFamily: "var(--font-display, sans-serif)",
          fontSize: "clamp(3rem, 8vw, 6rem)",
          color: "var(--color-text, white)",
          fontWeight: 700,
        }}
      >
        0
      </span>
    </div>
  );
}
```

### Cursor Mask / Spotlight Reveal

```tsx
// components/CursorMask.tsx
"use client";
import { useEffect, useRef, type ReactNode } from "react";

interface CursorMaskProps {
  defaultContent: ReactNode;
  revealContent: ReactNode;
  radius?: number;
}

export function CursorMask({
  defaultContent,
  revealContent,
  radius = 120,
}: CursorMaskProps) {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if ("ontouchstart" in window) return;

    const container = containerRef.current;
    if (!container) return;

    const onMouseMove = (e: MouseEvent) => {
      const rect = container.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      container.style.setProperty("--mx", `${x}px`);
      container.style.setProperty("--my", `${y}px`);
    };

    container.addEventListener("mousemove", onMouseMove);
    return () => container.removeEventListener("mousemove", onMouseMove);
  }, []);

  return (
    <div
      ref={containerRef}
      style={{ position: "relative", overflow: "hidden" }}
    >
      <div style={{ position: "relative", zIndex: 1 }}>
        {defaultContent}
      </div>
      <div
        style={{
          position: "absolute",
          inset: 0,
          zIndex: 2,
          maskImage: `radial-gradient(circle ${radius}px at var(--mx, -200px) var(--my, -200px), black, transparent)`,
          WebkitMaskImage: `radial-gradient(circle ${radius}px at var(--mx, -200px) var(--my, -200px), black, transparent)`,
        }}
      >
        {revealContent}
      </div>
    </div>
  );
}
```

### Scroll-Driven Video Playback

```tsx
// hooks/useScrollVideo.ts
"use client";
import { useEffect, useRef } from "react";
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";

gsap.registerPlugin(ScrollTrigger);

export function useScrollVideo<T extends HTMLElement>(
  videoRef: React.RefObject<HTMLVideoElement | null>,
  options: { start?: string; end?: string } = {}
) {
  const containerRef = useRef<T>(null);
  const { start = "top top", end = "bottom bottom" } = options;

  useEffect(() => {
    const video = videoRef.current;
    const container = containerRef.current;
    if (!video || !container) return;

    let st: globalThis.ScrollTrigger | null = null;

    const setup = () => {
      st = ScrollTrigger.create({
        trigger: container,
        start,
        end,
        scrub: true,
        onUpdate: (self) => {
          video.currentTime = self.progress * video.duration;
        },
      });
    };

    if (video.readyState >= 2) {
      setup();
    } else {
      video.addEventListener("loadeddata", setup, { once: true });
    }

    return () => {
      video.removeEventListener("loadeddata", setup);
      st?.kill();
    };
  }, [videoRef, start, end]);

  return containerRef;
}
```

### Beautiful Accessible Focus Rings

```css
/* globals.css — focus ring system */

:focus:not(:focus-visible) {
  outline: none;
}

:focus-visible {
  outline: none;
  box-shadow:
    0 0 0 2px var(--background),
    0 0 0 4px var(--ring-color, #6366f1);
  border-radius: inherit;
  transition: box-shadow 0.2s ease;
}

button:focus-visible,
a:focus-visible,
input:focus-visible,
select:focus-visible,
textarea:focus-visible {
  box-shadow:
    0 0 0 2px var(--background),
    0 0 0 4px var(--ring-color, #6366f1),
    0 0 20px -4px var(--ring-glow, rgba(99, 102, 241, 0.3));
  transition: box-shadow 0.3s cubic-bezier(0.22, 1, 0.36, 1);
}
```

---

## Word-Boundary Rule for Split Text

When splitting text into per-character spans for animation (outside of GSAP SplitText), ALWAYS group characters by word inside a `whitespace-nowrap` wrapper. Without this, the browser can line-break mid-word.

```tsx
// WRONG: characters can break mid-word
text.split("").map((c, i) => <span key={i} className="inline-block">{c}</span>)

// RIGHT: words stay together, spaces between words preserved
const words = text.split(" ");
words.map((word, wi) => (
  <span key={wi} className="inline-flex whitespace-nowrap">
    {word.split("").map((c, ci) => (
      <span key={ci} className="inline-block">{c}</span>
    ))}
    {wi < words.length - 1 && <span className="inline-block">&nbsp;</span>}
  </span>
))
```

This also applies to Framer Motion variants — any per-character animation must wrap characters in per-word containers.

### Font Consistency Rule

Animated text (scramble, typewriter, split-reveal) MUST use the same `font-family` as its final resting state. Never use a monospace font for scramble animation if the heading is a sans-serif. The font-swap creates a jarring visual jump.

### Video & Heavy Asset Mounting

Always mount videos and heavy assets ONCE and control visibility via opacity/display, not conditional rendering:

```tsx
// WRONG: remounts and reloads video on every toggle
{showVideo && <video src="..." autoPlay loop muted playsInline />}

// RIGHT: always mounted, toggle visibility — instant switching
<video
  src="..."
  autoPlay loop muted playsInline
  className="absolute inset-0 w-full h-full object-cover transition-opacity duration-500"
  style={{ opacity: showVideo ? 1 : 0, pointerEvents: showVideo ? "auto" : "none" }}
/>
```

This applies to any heavy asset: 3D canvases, iframes, Spline embeds. Mount once, show/hide with CSS.

---

## Tier 2: React Three Fiber Templates

### R3F Basic Scene

```tsx
// components/Scene3D.tsx
"use client";
import { Suspense } from "react";
import { Canvas } from "@react-three/fiber";
import {
  Environment,
  Float,
  ContactShadows,
  OrbitControls,
} from "@react-three/drei";
import { EffectComposer, Bloom, Vignette } from "@react-three/postprocessing";
import { useIs3DCapable } from "@/hooks/useIs3DCapable";

function LoadingSkeleton() {
  return (
    <div className="canvas-loading">
      <span className="sr-only">Loading 3D scene...</span>
    </div>
  );
}

function FallbackHero() {
  return <div className="hero-fallback" aria-label="Decorative background" />;
}

function SceneContent() {
  return (
    <>
      <ambientLight intensity={0.4} />
      <directionalLight position={[5, 5, 5]} intensity={0.8} />
      <Float speed={2} rotationIntensity={0.5} floatIntensity={1}>
        <mesh>
          <sphereGeometry args={[1, 64, 64]} />
          <meshStandardMaterial color="#8b5cf6" metalness={0.8} roughness={0.2} />
        </mesh>
      </Float>
      <ContactShadows
        position={[0, -1.5, 0]}
        opacity={0.4}
        blur={2}
        far={4}
      />
      <Environment preset="city" />
      <OrbitControls enableZoom={false} enablePan={false} autoRotate autoRotateSpeed={0.5} />
      <EffectComposer>
        <Bloom intensity={0.3} luminanceThreshold={0.8} />
        <Vignette eskil={false} offset={0.1} darkness={0.5} />
      </EffectComposer>
    </>
  );
}

export function Scene3D() {
  const is3D = useIs3DCapable();

  if (!is3D) return <FallbackHero />;

  return (
    <div className="canvas-container">
      <Suspense fallback={<LoadingSkeleton />}>
        <Canvas
          camera={{ position: [0, 0, 5], fov: 45 }}
          dpr={[1, 2]}
        >
          <SceneContent />
        </Canvas>
      </Suspense>
    </div>
  );
}
```

### R3F Scroll-Driven Scene

**WARNING:** This uses drei's `<ScrollControls>`. Do NOT combine with Lenis — they conflict. Use one or the other.

```tsx
// components/ScrollScene.tsx
"use client";
import { Suspense } from "react";
import { Canvas } from "@react-three/fiber";
import { ScrollControls, Scroll, Float, Environment } from "@react-three/drei";
import { useIs3DCapable } from "@/hooks/useIs3DCapable";

function ScrollContent() {
  return (
    <ScrollControls pages={3} damping={0.25}>
      <Float speed={1.5} rotationIntensity={0.3}>
        <mesh position={[0, 0, 0]}>
          <torusKnotGeometry args={[1, 0.3, 128, 32]} />
          <meshStandardMaterial
            color="#6366f1"
            metalness={0.9}
            roughness={0.1}
          />
        </mesh>
      </Float>
      <Environment preset="sunset" />

      <Scroll html>
        <section className="h-screen flex items-center justify-center">
          <h1 className="text-display">Section One</h1>
        </section>
        <section className="h-screen flex items-center justify-center">
          <h2 className="text-heading">Section Two</h2>
        </section>
        <section className="h-screen flex items-center justify-center">
          <h2 className="text-heading">Section Three</h2>
        </section>
      </Scroll>
    </ScrollControls>
  );
}

export function ScrollScene() {
  const is3D = useIs3DCapable();

  if (!is3D) {
    return <div className="hero-fallback" aria-label="Decorative background" />;
  }

  return (
    <div style={{ height: "300vh" }}>
      <Canvas
        camera={{ position: [0, 0, 5], fov: 45 }}
        dpr={[1, 2]}
        style={{ position: "fixed", top: 0, left: 0 }}
      >
        <Suspense fallback={null}>
          <ScrollContent />
        </Suspense>
      </Canvas>
    </div>
  );
}
```

---

## Advanced R3F Techniques

### Custom GLSL Shaders — Animated Gradient Noise

A liquid, organic background that reacts to mouse movement. Use as hero background or full-page atmosphere.

```tsx
// components/GradientNoiseMesh.tsx
"use client";
import { useRef, useMemo } from "react";
import { useFrame, useThree } from "@react-three/fiber";
import * as THREE from "three";

const vertexShader = /* glsl */ `
  varying vec2 vUv;
  void main() {
    vUv = uv;
    gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
  }
`;

const fragmentShader = /* glsl */ `
  uniform float uTime;
  uniform vec2 uMouse;
  uniform vec2 uResolution;
  uniform vec3 uColorA;
  uniform vec3 uColorB;
  uniform vec3 uColorC;
  varying vec2 vUv;

  float hash(vec2 p) {
    return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453);
  }

  float noise(vec2 p) {
    vec2 i = floor(p);
    vec2 f = fract(p);
    f = f * f * (3.0 - 2.0 * f);
    return mix(
      mix(hash(i), hash(i + vec2(1.0, 0.0)), f.x),
      mix(hash(i + vec2(0.0, 1.0)), hash(i + vec2(1.0, 1.0)), f.x),
      f.y
    );
  }

  float fbm(vec2 p) {
    float value = 0.0;
    float amplitude = 0.5;
    for (int i = 0; i < 6; i++) {
      value += amplitude * noise(p);
      p *= 2.0;
      amplitude *= 0.5;
    }
    return value;
  }

  void main() {
    vec2 uv = vUv;
    vec2 mouse = uMouse * 0.3;
    float n = fbm(uv * 3.0 + uTime * 0.15 + mouse);
    float n2 = fbm(uv * 2.0 - uTime * 0.1 + mouse * 0.5);
    vec3 color = mix(uColorA, uColorB, n);
    color = mix(color, uColorC, n2 * 0.6);
    float vignette = 1.0 - length(uv - 0.5) * 0.8;
    color *= vignette;
    gl_FragColor = vec4(color, 1.0);
  }
`;

interface GradientNoiseMeshProps {
  colorA?: string;
  colorB?: string;
  colorC?: string;
}

export function GradientNoiseMesh({
  colorA = "#0a0a2e",
  colorB = "#1a0a3e",
  colorC = "#0a1a4e",
}: GradientNoiseMeshProps) {
  const meshRef = useRef<THREE.Mesh>(null);
  const mouseRef = useRef(new THREE.Vector2(0, 0));
  const { viewport } = useThree();

  const uniforms = useMemo(
    () => ({
      uTime: { value: 0 },
      uMouse: { value: new THREE.Vector2(0, 0) },
      uResolution: { value: new THREE.Vector2(1, 1) },
      uColorA: { value: new THREE.Color(colorA) },
      uColorB: { value: new THREE.Color(colorB) },
      uColorC: { value: new THREE.Color(colorC) },
    }),
    [colorA, colorB, colorC]
  );

  useFrame(({ clock, pointer }) => {
    uniforms.uTime.value = clock.getElapsedTime();
    mouseRef.current.lerp(pointer, 0.05);
    uniforms.uMouse.value.copy(mouseRef.current);
  });

  return (
    <mesh ref={meshRef} scale={[viewport.width, viewport.height, 1]}>
      <planeGeometry args={[1, 1, 1, 1]} />
      <shaderMaterial
        vertexShader={vertexShader}
        fragmentShader={fragmentShader}
        uniforms={uniforms}
      />
    </mesh>
  );
}
```

### Water / Distortion Shader

Noise-based displacement for liquid, underwater, or heat-haze effects on any mesh.

```tsx
// components/DistortionMesh.tsx
"use client";
import { useRef, useMemo } from "react";
import { useFrame } from "@react-three/fiber";
import * as THREE from "three";

const distortVert = /* glsl */ `
  uniform float uTime;
  uniform float uStrength;
  varying vec2 vUv;
  varying float vDisplacement;

  vec3 mod289(vec3 x) { return x - floor(x / 289.0) * 289.0; }
  vec4 mod289(vec4 x) { return x - floor(x / 289.0) * 289.0; }
  vec4 permute(vec4 x) { return mod289(((x * 34.0) + 1.0) * x); }
  vec4 taylorInvSqrt(vec4 r) { return 1.79284291400159 - 0.85373472095314 * r; }

  float snoise(vec3 v) {
    const vec2 C = vec2(1.0/6.0, 1.0/3.0);
    const vec4 D = vec4(0.0, 0.5, 1.0, 2.0);
    vec3 i = floor(v + dot(v, C.yyy));
    vec3 x0 = v - i + dot(i, C.xxx);
    vec3 g = step(x0.yzx, x0.xyz);
    vec3 l = 1.0 - g;
    vec3 i1 = min(g.xyz, l.zxy);
    vec3 i2 = max(g.xyz, l.zxy);
    vec3 x1 = x0 - i1 + C.xxx;
    vec3 x2 = x0 - i2 + C.yyy;
    vec3 x3 = x0 - D.yyy;
    i = mod289(i);
    vec4 p = permute(permute(permute(
      i.z + vec4(0.0, i1.z, i2.z, 1.0))
      + i.y + vec4(0.0, i1.y, i2.y, 1.0))
      + i.x + vec4(0.0, i1.x, i2.x, 1.0));
    float n_ = 0.142857142857;
    vec3 ns = n_ * D.wyz - D.xzx;
    vec4 j = p - 49.0 * floor(p * ns.z * ns.z);
    vec4 x_ = floor(j * ns.z);
    vec4 y_ = floor(j - 7.0 * x_);
    vec4 x = x_ * ns.x + ns.yyyy;
    vec4 y = y_ * ns.x + ns.yyyy;
    vec4 h = 1.0 - abs(x) - abs(y);
    vec4 b0 = vec4(x.xy, y.xy);
    vec4 b1 = vec4(x.zw, y.zw);
    vec4 s0 = floor(b0) * 2.0 + 1.0;
    vec4 s1 = floor(b1) * 2.0 + 1.0;
    vec4 sh = -step(h, vec4(0.0));
    vec4 a0 = b0.xzyw + s0.xzyw * sh.xxyy;
    vec4 a1 = b1.xzyw + s1.xzyw * sh.zzww;
    vec3 p0 = vec3(a0.xy, h.x);
    vec3 p1 = vec3(a0.zw, h.y);
    vec3 p2 = vec3(a1.xy, h.z);
    vec3 p3 = vec3(a1.zw, h.w);
    vec4 norm = taylorInvSqrt(vec4(dot(p0,p0), dot(p1,p1), dot(p2,p2), dot(p3,p3)));
    p0 *= norm.x; p1 *= norm.y; p2 *= norm.z; p3 *= norm.w;
    vec4 m = max(0.6 - vec4(dot(x0,x0), dot(x1,x1), dot(x2,x2), dot(x3,x3)), 0.0);
    m = m * m;
    return 42.0 * dot(m*m, vec4(dot(p0,x0), dot(p1,x1), dot(p2,x2), dot(p3,x3)));
  }

  void main() {
    vUv = uv;
    float displacement = snoise(vec3(position.x * 2.0, position.y * 2.0, uTime * 0.3)) * uStrength;
    vDisplacement = displacement;
    vec3 newPosition = position + normal * displacement;
    gl_Position = projectionMatrix * modelViewMatrix * vec4(newPosition, 1.0);
  }
`;

const distortFrag = /* glsl */ `
  uniform vec3 uColor;
  uniform float uOpacity;
  varying vec2 vUv;
  varying float vDisplacement;

  void main() {
    float intensity = 0.5 + vDisplacement * 2.0;
    vec3 color = uColor * intensity;
    gl_FragColor = vec4(color, uOpacity);
  }
`;

interface DistortionMeshProps {
  color?: string;
  strength?: number;
  opacity?: number;
  segments?: number;
}

export function DistortionMesh({
  color = "#4a00e0",
  strength = 0.3,
  opacity = 0.8,
  segments = 64,
}: DistortionMeshProps) {
  const meshRef = useRef<THREE.Mesh>(null);

  const uniforms = useMemo(
    () => ({
      uTime: { value: 0 },
      uStrength: { value: strength },
      uColor: { value: new THREE.Color(color) },
      uOpacity: { value: opacity },
    }),
    [color, strength, opacity]
  );

  useFrame(({ clock }) => {
    uniforms.uTime.value = clock.getElapsedTime();
  });

  return (
    <mesh ref={meshRef}>
      <sphereGeometry args={[1.5, segments, segments]} />
      <shaderMaterial
        vertexShader={distortVert}
        fragmentShader={distortFrag}
        uniforms={uniforms}
        transparent
      />
    </mesh>
  );
}
```

### Cinematic Post-Processing Stack

Complete EffectComposer with scroll-linked depth of field, chromatic aberration, noise, and color grading.

```tsx
// components/CinematicPostProcessing.tsx
"use client";
import { useRef } from "react";
import { useFrame } from "@react-three/fiber";
import {
  EffectComposer,
  ChromaticAberration,
  DepthOfField,
  Noise,
  Vignette,
  ToneMapping,
} from "@react-three/postprocessing";
import { BlendFunction, ToneMappingMode } from "postprocessing";
import { useScroll } from "@react-three/drei";
import * as THREE from "three";

export function CinematicPostProcessing() {
  const chromaRef = useRef<any>(null);
  const dofRef = useRef<any>(null);
  const scroll = useScroll();

  useFrame(() => {
    if (!scroll) return;
    const progress = scroll.offset;

    if (chromaRef.current) {
      const aberration = Math.sin(progress * Math.PI) * 0.003;
      chromaRef.current.offset = new THREE.Vector2(aberration, aberration);
    }

    if (dofRef.current) {
      dofRef.current.target = 3 + progress * 8;
    }
  });

  return (
    <EffectComposer multisampling={0}>
      <DepthOfField
        ref={dofRef}
        focusDistance={0}
        focalLength={0.05}
        bokehScale={4}
      />
      <ChromaticAberration
        ref={chromaRef}
        blendFunction={BlendFunction.NORMAL}
        offset={new THREE.Vector2(0.001, 0.001)}
      />
      <Noise
        blendFunction={BlendFunction.SOFT_LIGHT}
        opacity={0.15}
      />
      <Vignette
        darkness={0.5}
        offset={0.3}
      />
      <ToneMapping mode={ToneMappingMode.ACES_FILMIC} />
    </EffectComposer>
  );
}
```

### Physics Interactions with Rapier

Gravity-driven interactive objects. Use for playful hero sections or interactive backgrounds.

```tsx
// components/PhysicsScene.tsx
"use client";
import { Physics, RigidBody, CuboidCollider } from "@react-three/rapier";

function FallingBoxes({ count = 40 }: { count?: number }) {
  const boxes = Array.from({ length: count }, (_, i) => ({
    key: i,
    position: [
      (Math.random() - 0.5) * 8,
      Math.random() * 15 + 5,
      (Math.random() - 0.5) * 4,
    ] as [number, number, number],
    rotation: [
      Math.random() * Math.PI,
      Math.random() * Math.PI,
      Math.random() * Math.PI,
    ] as [number, number, number],
    scale: 0.2 + Math.random() * 0.4,
  }));

  return (
    <>
      {boxes.map(({ key, position, rotation, scale }) => (
        <RigidBody
          key={key}
          position={position}
          rotation={rotation}
          restitution={0.4}
          friction={0.8}
        >
          <mesh castShadow>
            <boxGeometry args={[scale, scale, scale]} />
            <meshStandardMaterial
              color={`hsl(${key * 9}, 60%, 50%)`}
              metalness={0.3}
              roughness={0.5}
            />
          </mesh>
        </RigidBody>
      ))}
    </>
  );
}

export function PhysicsScene() {
  return (
    <Physics gravity={[0, -9.81, 0]}>
      <RigidBody type="fixed">
        <CuboidCollider args={[10, 0.1, 10]} position={[0, -2, 0]} />
        <mesh receiveShadow position={[0, -2, 0]}>
          <boxGeometry args={[20, 0.2, 20]} />
          <meshStandardMaterial color="#1a1a2e" />
        </mesh>
      </RigidBody>
      <RigidBody type="fixed">
        <CuboidCollider args={[0.1, 10, 10]} position={[-5, 5, 0]} />
        <CuboidCollider args={[0.1, 10, 10]} position={[5, 5, 0]} />
      </RigidBody>
      <FallingBoxes />
    </Physics>
  );
}
```

### 3D Text

Two approaches: `Text3D` for hero moments, `<Text>` (SDF) for performant labels/body.

```tsx
// Hero moment — extruded 3D text
import { Text3D, Center, useMatcapTexture } from "@react-three/drei";

export function Hero3DText({ text = "OVERKILL" }: { text?: string }) {
  const [matcap] = useMatcapTexture("3E2335_D36A1B_8E4A2E_2842A5", 256);

  return (
    <Center>
      <Text3D
        font="/fonts/inter-bold.json"
        size={1.2}
        height={0.3}
        bevelEnabled
        bevelSize={0.02}
        bevelThickness={0.01}
        letterSpacing={0.05}
      >
        {text}
        <meshMatcapMaterial matcap={matcap} />
      </Text3D>
    </Center>
  );
}

// Performant SDF text — use for body text, labels, HUDs
import { Text } from "@react-three/drei";

export function SDFText({ children, ...props }: any) {
  return (
    <Text
      fontSize={0.5}
      color="#ffffff"
      anchorX="center"
      anchorY="middle"
      font="/fonts/inter-regular.woff"
      maxWidth={10}
      {...props}
    >
      {children}
    </Text>
  );
}
```

**When to use which:**
- `Text3D`: Hero titles, logo moments, anything needing depth and lighting
- `<Text>` (SDF): Everything else — labels, body text, HUD elements, many instances

### Model Loading — .glb Workflow

```tsx
// components/ProductModel.tsx
"use client";
import { Suspense } from "react";
import { useGLTF, OrbitControls, Stage, Preload } from "@react-three/drei";
import { Canvas } from "@react-three/fiber";

function Model({ url }: { url: string }) {
  const { scene } = useGLTF(url);
  return <primitive object={scene} />;
}

useGLTF.preload("/models/product.glb");

export function ProductViewer() {
  return (
    <Canvas camera={{ position: [0, 0, 5], fov: 45 }}>
      <Suspense fallback={null}>
        <Stage environment="city" intensity={0.5}>
          <Model url="/models/product.glb" />
        </Stage>
        <OrbitControls
          enableZoom={false}
          autoRotate
          autoRotateSpeed={1}
          minPolarAngle={Math.PI / 4}
          maxPolarAngle={Math.PI / 1.5}
        />
      </Suspense>
      <Preload all />
    </Canvas>
  );
}
```

**Draco compression pipeline:**
```bash
npx @gltf-transform/cli optimize input.glb output.glb --compress draco
npx gltfjsx input.glb --transform --types --output Model.tsx
```

### Scroll-Driven Camera Dolly

Camera moves along a spline path as the user scrolls. Cinematic storytelling.

```tsx
// components/CameraDolly.tsx
"use client";
import { useMemo } from "react";
import { useFrame } from "@react-three/fiber";
import { useScroll } from "@react-three/drei";
import * as THREE from "three";

interface CameraDollyProps {
  points?: [number, number, number][];
  lookAt?: [number, number, number];
}

export function CameraDolly({
  points = [
    [0, 2, 10],
    [5, 3, 5],
    [8, 1, 0],
    [5, 2, -5],
    [0, 4, -8],
  ],
  lookAt = [0, 0, 0],
}: CameraDollyProps) {
  const scroll = useScroll();
  const lookAtVec = useMemo(() => new THREE.Vector3(...lookAt), [lookAt]);

  const curve = useMemo(() => {
    const curvePoints = points.map(
      (p) => new THREE.Vector3(p[0], p[1], p[2])
    );
    return new THREE.CatmullRomCurve3(curvePoints, false, "centripetal", 0.5);
  }, [points]);

  useFrame(({ camera }) => {
    const progress = scroll.offset;
    const point = curve.getPointAt(progress);
    camera.position.lerp(point, 0.1);
    camera.lookAt(lookAtVec);
  });

  return null;
}

// Usage in a ScrollControls scene:
// <ScrollControls pages={5}>
//   <CameraDolly points={[[0,2,10], [5,3,5], [8,1,0]]} />
//   <YourScene />
// </ScrollControls>
```

### Instanced Meshes — Particle Field

For particle fields, starfields, floating debris, or data visualization points.

```tsx
// components/ParticleField.tsx
"use client";
import { useRef, useMemo } from "react";
import { useFrame } from "@react-three/fiber";
import * as THREE from "three";

interface ParticleFieldProps {
  count?: number;
  spread?: number;
  size?: number;
  color?: string;
}

export function ParticleField({
  count = 2000,
  spread = 20,
  size = 0.02,
  color = "#ffffff",
}: ParticleFieldProps) {
  const meshRef = useRef<THREE.InstancedMesh>(null);
  const dummy = useMemo(() => new THREE.Object3D(), []);

  const particles = useMemo(() => {
    return Array.from({ length: count }, () => ({
      position: new THREE.Vector3(
        (Math.random() - 0.5) * spread,
        (Math.random() - 0.5) * spread,
        (Math.random() - 0.5) * spread
      ),
      speed: 0.2 + Math.random() * 0.5,
      offset: Math.random() * Math.PI * 2,
    }));
  }, [count, spread]);

  useFrame(({ clock }) => {
    const mesh = meshRef.current;
    if (!mesh) return;
    const t = clock.getElapsedTime();

    for (let i = 0; i < count; i++) {
      const { position, speed, offset } = particles[i];
      dummy.position.set(
        position.x + Math.sin(t * speed + offset) * 0.5,
        position.y + Math.cos(t * speed * 0.7 + offset) * 0.3,
        position.z + Math.sin(t * speed * 0.5 + offset) * 0.4
      );
      dummy.updateMatrix();
      mesh.setMatrixAt(i, dummy.matrix);
    }
    mesh.instanceMatrix.needsUpdate = true;
  });

  return (
    <instancedMesh ref={meshRef} args={[undefined, undefined, count]}>
      <sphereGeometry args={[size, 6, 6]} />
      <meshBasicMaterial color={color} transparent opacity={0.6} />
    </instancedMesh>
  );
}
```

### Studio Lighting Setup

Three-point lighting for photorealistic product renders.

```tsx
// components/StudioLighting.tsx
"use client";

interface StudioLightingProps {
  intensity?: number;
  color?: string;
}

export function StudioLighting({
  intensity = 1,
  color = "#ffffff",
}: StudioLightingProps) {
  return (
    <>
      {/* Key light — main illumination, slight angle */}
      <directionalLight
        position={[5, 5, 5]}
        intensity={intensity * 1.2}
        color={color}
        castShadow
        shadow-mapSize-width={2048}
        shadow-mapSize-height={2048}
      />
      {/* Fill light — softer, opposite side */}
      <directionalLight
        position={[-3, 3, -2]}
        intensity={intensity * 0.4}
        color="#e8e0ff"
      />
      {/* Rim light — edge definition from behind */}
      <directionalLight
        position={[0, 2, -5]}
        intensity={intensity * 0.6}
        color="#ffe0c0"
      />
      {/* Ambient — lift shadows */}
      <ambientLight intensity={intensity * 0.15} />
    </>
  );
}
```

### Variable Font Weight on Scroll

GSAP-driven variable font weight that shifts from light to bold as user scrolls.

```tsx
// hooks/useVariableFontScroll.ts
"use client";
import { useEffect, useRef } from "react";
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";

gsap.registerPlugin(ScrollTrigger);

export function useVariableFontScroll<T extends HTMLElement>(
  options: { minWeight?: number; maxWeight?: number } = {}
) {
  const ref = useRef<T>(null);
  const { minWeight = 100, maxWeight = 900 } = options;

  useEffect(() => {
    const el = ref.current;
    if (!el) return;

    const prefersReduced = window.matchMedia(
      "(prefers-reduced-motion: reduce)"
    ).matches;
    if (prefersReduced) return;

    const tween = gsap.to(el, {
      fontVariationSettings: `'wght' ${maxWeight}`,
      ease: "none",
      scrollTrigger: {
        trigger: el,
        start: "top 80%",
        end: "top 20%",
        scrub: true,
      },
    });

    // Set initial state
    el.style.fontVariationSettings = `'wght' ${minWeight}`;

    return () => {
      tween.kill();
      ScrollTrigger.getAll().forEach((st) => {
        if (st.trigger === el) st.kill();
      });
    };
  }, [minWeight, maxWeight]);

  return ref;
}
```

### Sound Toggle (Howler.js)

Minimal opt-in sound pattern for ambient background or micro-sounds.

```tsx
// hooks/useSound.ts
"use client";
import { useRef, useCallback, useState } from "react";
import { Howl } from "howler";

interface UseSoundOptions {
  src: string;
  volume?: number;
  loop?: boolean;
}

export function useSound({ src, volume = 0.3, loop = false }: UseSoundOptions) {
  const soundRef = useRef<Howl | null>(null);
  const [isPlaying, setIsPlaying] = useState(false);

  const play = useCallback(() => {
    if (!soundRef.current) {
      soundRef.current = new Howl({ src: [src], volume, loop });
    }
    soundRef.current.play();
    setIsPlaying(true);
  }, [src, volume, loop]);

  const stop = useCallback(() => {
    soundRef.current?.stop();
    setIsPlaying(false);
  }, []);

  const toggle = useCallback(() => {
    if (isPlaying) stop();
    else play();
  }, [isPlaying, play, stop]);

  return { play, stop, toggle, isPlaying };
}
```

### Scroll Text Highlight

Background-size animation on scroll — text highlights as user scrolls past.

```tsx
// hooks/useScrollHighlight.ts
"use client";
import { useEffect, useRef } from "react";
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";

gsap.registerPlugin(ScrollTrigger);

/**
 * Highlights text with a background gradient as user scrolls past.
 * Apply to a text element. Set CSS:
 *   background: linear-gradient(to right, var(--color-primary) 50%, transparent 50%);
 *   background-size: 200% 100%;
 *   background-position: 100% 0;
 *   -webkit-background-clip: text;
 *   -webkit-text-fill-color: transparent;
 */
export function useScrollHighlight<T extends HTMLElement>() {
  const ref = useRef<T>(null);

  useEffect(() => {
    const el = ref.current;
    if (!el) return;

    const tween = gsap.to(el, {
      backgroundPosition: "0% 0",
      ease: "none",
      scrollTrigger: {
        trigger: el,
        start: "top 80%",
        end: "top 30%",
        scrub: true,
      },
    });

    return () => {
      tween.kill();
      ScrollTrigger.getAll().forEach((st) => {
        if (st.trigger === el) st.kill();
      });
    };
  }, []);

  return ref;
}
```

### Adaptive Scene (Mobile/Desktop)

```tsx
// components/AdaptiveScene.tsx
"use client";
import { Canvas } from "@react-three/fiber";
import { useIs3DCapable } from "@/hooks/useIs3DCapable";

interface AdaptiveSceneProps {
  desktopScene: React.ReactNode;
  mobileScene?: React.ReactNode;
  mobileFallback?: React.ReactNode;
}

export function AdaptiveScene({
  desktopScene,
  mobileScene,
  mobileFallback,
}: AdaptiveSceneProps) {
  const is3D = useIs3DCapable();

  if (!is3D && mobileFallback) return <>{mobileFallback}</>;

  if (!is3D && mobileScene) {
    return (
      <Canvas dpr={[1, 1.5]} performance={{ min: 0.5 }}>
        {mobileScene}
      </Canvas>
    );
  }

  return (
    <Canvas dpr={[1, 2]} performance={{ min: 0.5 }}>
      {desktopScene}
    </Canvas>
  );
}
```

---

## Memory Management

Three.js does NOT garbage-collect GPU resources. Always dispose in cleanup:

```tsx
useEffect(() => {
  return () => {
    // Dispose geometry
    geometry.dispose();
    // Dispose material (and its maps)
    if (material.map) material.map.dispose();
    material.dispose();
    // Dispose render targets
    renderTarget?.dispose();
  };
}, []);

// For loaded models:
useEffect(() => {
  return () => {
    scene.traverse((child) => {
      if (child instanceof THREE.Mesh) {
        child.geometry.dispose();
        if (Array.isArray(child.material)) {
          child.material.forEach((m) => m.dispose());
        } else {
          child.material.dispose();
        }
      }
    });
  };
}, [scene]);
```

**Rules:**
- Dispose everything you create: geometries, materials, textures, render targets
- For models loaded via `useGLTF`, drei handles cleanup on unmount
- For custom shaders, dispose the `ShaderMaterial` and any textures in uniforms
- Watch Chrome DevTools Memory tab for GPU memory leaks during development

---

## Mobile Performance Rules

| Desktop | Mobile |
|---------|--------|
| 2000 particles | 500 particles (`count / 4`) |
| `dpr={[1, 2]}` | `dpr={[1, 1.5]}` |
| Full post-processing | Remove post-processing entirely |
| 64-segment sphere | 32-segment sphere |
| Custom cursor | System cursor |
| Hover effects | Touch feedback (scale on tap) |
| Film grain animated | Static noise or remove |

**Hard numbers:**
- Mobile Canvas FPS target: 30fps minimum, fallback to static if below 20fps
- Mobile JS budget: < 200KB gzipped (defer 3D entirely if exceeded)
- Touch targets: > 44px
- Never depend on hover — all hover effects must have touch equivalents

---

## Performance Profiling

### GPU Profiling Tools

```tsx
// Add to any R3F scene during development
import { Stats } from "@react-three/drei";
import { Perf } from "r3f-perf";

// In your Canvas:
<Stats />
<Perf position="top-left" />
```

### Draw Call Budgets

| Site Complexity | Max Draw Calls | Max Triangles | Max Textures |
|----------------|---------------|---------------|--------------|
| Simple (landing) | < 50 | < 100K | < 10 |
| Medium (portfolio) | < 150 | < 500K | < 25 |
| Complex (experience) | < 300 | < 1M | < 50 |

**Reduce draw calls:**
- Use `<instancedMesh>` for repeated geometry (particles, grids)
- Merge static geometry with `<Merged>` from drei
- Use texture atlases instead of individual textures
- Avoid transparent materials where possible (extra draw calls)

### LOD (Level of Detail)

```tsx
import { Detailed } from "@react-three/drei";

<Detailed distances={[0, 25, 50, 100]}>
  <HighPolyModel />
  <MidPolyModel />
  <LowPolyModel />
  <BillboardSprite />
</Detailed>
```

### GPU Layer Promotion (CSS)

```css
.will-animate {
  will-change: transform, opacity;
  /* Remove after animation completes to free GPU memory */
}
/* Never put will-change on more than ~20 elements */
```

---

## Archetypes

### 1. Ambient Spline Background (Tier 1)
Full-screen Spline scene as background behind glass-morphism content cards.
- Spline scene fills viewport, `position: fixed`, `z-index: -1`
- Content floats above with `.glass` cards
- GSAP ScrollTrigger reveals cards on scroll
- Lenis provides smooth scroll feel
- Mobile: hide Spline, show `.hero-fallback` gradient

### 2. 3D Product Showcase (Tier 2)
Floating 3D model with orbit controls and glass info cards alongside.
- R3F Canvas with `<OrbitControls>` (constrain polar angle)
- `<Float>` wraps the model for gentle bob
- `<ContactShadows>` grounds the object
- Post-processing: subtle `<Bloom>` + `<Vignette>`
- Split layout: 3D on left, glass info cards on right
- Mobile: static product image replaces Canvas

### 3. Particle Hero (Tier 2)
Thousands of particles responding to mouse position and scroll progress.
- Custom `<Points>` geometry with `useFrame` animation
- Mouse position via `useMouseParallax` mapped to particle attraction
- Scroll progress via `useScroll` from drei shifts particle formation
- Post-processing glow with `<Bloom>`
- Mobile: CSS gradient with animated `background-position`

### 4. Scroll-Driven 3D Narrative (Either Tier)
Scene transforms as the user scrolls — camera moves, objects appear/disappear.
- **Tier 1 version:** Spline background + GSAP pin sections with content reveals
- **Tier 2 version:** `<ScrollControls>` from drei, camera lerps between positions
- Each scroll "page" triggers a scene state change
- Text sections overlay via `<Scroll html>` (Tier 2) or pinned divs (Tier 1)
- **Lenis:** Use with Tier 1 only. Tier 2 uses `<ScrollControls>` instead.

### 5. Award-Winning Landing Page (All Tiers)
Preloader -> split-text hero -> parallax depth -> magnetic CTAs -> film grain -> custom cursor -> smooth scroll with pin sections.
- `<Preloader />` runs first, counter 0->100, clip-path exit
- Hero heading uses `useSplitTextReveal` with clip-mask variant
- Background elements at different scroll speeds via `useParallaxLayer`
- All CTA buttons wrapped in `<MagneticButton>`
- `<FilmGrain />` in layout (dark theme)
- `<CustomCursor />` at app root, context-aware on CTAs
- Lenis smooth scroll with GSAP pin sections for content narrative

### 6. Interactive Portfolio (All Tiers, selective)
Preloader -> grid with WebGL hover distortion -> custom cursor showing "View" -> page transitions -> split-text on project titles -> cursor mask on featured hero.
- `<Preloader />` sets the tone
- Project grid cards use `hover-effect` library for WebGL distortion on hover
- `<CustomCursor />` with `data-cursor="text:View"` on project cards
- `<PageTransition variant="slideUp" />` in `app/template.tsx`
- Project detail titles use `useSplitTextReveal`
- Featured hero uses `<CursorMask>` for dark/light reveal
- `<FilmGrain />` throughout

### 7. Full Immersive Experience (All Tiers)
Preloader -> R3F scene with scroll-driven camera -> advanced post-processing -> split-text overlays -> film grain -> custom cursor -> full parallax depth layering.
- `<Preloader />` with branded animation
- R3F Canvas with `<ScrollControls>`, camera lerps between positions
- Post-processing: `<ChromaticAberration>`, `<DepthOfField>`, `<Noise>`, `<Bloom>`
- HTML overlay sections use `useSplitTextReveal` for text
- `<FilmGrain />` composited over everything
- `<CustomCursor />` with context changes (expand on 3D, text on links)
- Background elements at multiple parallax speeds

---

## Delivery Checklist

Before marking a 3D/immersive project complete, verify ALL:

- [ ] **Suspense wrapping** — every 3D component wrapped in `<Suspense>` with visible fallback
- [ ] **Mobile fallback** — Canvas/Spline hidden on mobile, CSS fallback shown
- [ ] **Reduced motion** — `prefers-reduced-motion` disables animations + 3D autoplay
- [ ] **Lenis sync** — Lenis smooth scroll active, synced with GSAP ScrollTrigger if used
- [ ] **No Lenis + ScrollControls** — never combined in the same page
- [ ] **Cleanup** — all ScrollTriggers, Lenis listeners, and animation frames killed in useEffect return
- [ ] **GPU memory** — geometries, materials, textures disposed in cleanup
- [ ] **DPR cap** — `dpr={[1, 2]}` on Canvas (retina without perf waste)
- [ ] **No layout shift** — 3D containers have explicit dimensions, no CLS on load
- [ ] **Lazy-loaded** — 3D components use `next/dynamic` or `React.lazy`, not blocking initial paint
- [ ] **60fps** — smooth animations on desktop, no jank on scroll
- [ ] **JS-disabled fallback** — `<noscript>` with static image or gradient
- [ ] **Split-text reveals** — hero heading uses SplitText stagger (not just fade)
- [ ] **Film grain** — dark themes have SVG noise overlay (opacity 0.03-0.06)
- [ ] **Custom cursor** — desktop shows custom cursor, hidden on touch devices
- [ ] **Magnetic interactions** — CTAs have magnetic pull effect on desktop
- [ ] **Parallax depth** — at least 2 elements at different scroll speeds
- [ ] **Page transitions** — route changes animated (if multi-page)
- [ ] **Preloader** — initial load has animated intro, not raw content flash
- [ ] **Spring easing** — interactive animations use elastic/spring, not linear
- [ ] **Generated assets** — all assets.md items exist in /public/, referenced in code, fallbacks present
