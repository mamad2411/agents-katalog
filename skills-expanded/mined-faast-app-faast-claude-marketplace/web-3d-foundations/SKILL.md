---
name: web-3d-foundations
description: Fundamentos de 3D para web en dev-team - cuando se justifica el 3D, pipeline de assets glTF (Draco/meshopt, KTX2), escena Three.js/R3F con carga progresiva y fallback 2D, iluminacion y materiales PBR, presupuesto de rendimiento, accesibilidad del canvas e integracion con Spline/Blender. Cargala antes de proponer o construir una escena 3D.
---

# Web 3D foundations (dev-team)

## 1. ¿Se justifica?
Si: producto fisico configurable, datos espaciales, experiencia de marca deliberada,
visualizacion que el 2D no explica. No: "para que se vea moderno". Alternativa barata:
2.5D con CSS (parallax, capas, sombras, `perspective`).

## 2. Presupuesto (antes de modelar)
Hero: ≤ 2 MB de assets, ≤ 150k triangulos, ≤ 50 draw calls, primer frame < 1.5 s en 4G,
60 fps en portatil integrado, 30 fps en movil medio. Declararlo y medirlo.

## 3. Assets
- Formato **glTF 2.0 (.glb)**; compresion **Draco** o **meshopt** (`gltf-transform`);
  texturas **KTX2/Basis** o WebP, ≤ 2048 px, atlas cuando se pueda.
- Fuentes: propio (Blender), Spline (exportar glTF), librerias libres (Poly Haven,
  Kenney, Sketchfab CC-BY) — anotar licencia y origen en `assets/LICENSES.md`.
- LODs: poster (imagen) → low-poly → alta, con carga progresiva.

## 4. Escena (Three.js / React Three Fiber)
- Three.js por import map desde CDN pinneado; en React, R3F + `@react-three/drei`
  (`useGLTF`, `Environment`, `ContactShadows`, `Html`).
- Camara con limites (`OrbitControls` con `minDistance/maxDistance/maxPolarAngle`),
  `dampingFactor`, sin auto-rotacion infinita en UI de trabajo.
- Iluminacion: HDRI (`Environment`) + key light; sombras solo si el presupuesto lo permite.
- Materiales PBR (`MeshStandard/PhysicalMaterial`): baseColor, metalness, roughness,
  normal; colores desde la paleta del proyecto.
- Rendimiento: `renderer.setPixelRatio(Math.min(devicePixelRatio, 2))`, render on demand
  o pausa fuera de pantalla (`IntersectionObserver`) y con pestaña oculta, `dispose()` al
  desmontar, `powerPreference: "high-performance"` solo en desktop.
- WebGL 2 base; WebGPU como mejora progresiva con deteccion (`navigator.gpu`).

## 5. Accesibilidad y fallback
Canvas `aria-hidden="true"`; todo texto e informacion en HTML real; fallback 2D (imagen
o SVG) si no hay WebGL o si `prefers-reduced-motion`; controles con teclado
equivalentes (botones para rotar/zoom) cuando la interaccion es funcional.

## 6. Integracion con el equipo
Colores/materiales del visual-designer · movimiento de camara con los motion tokens ·
escena HTML autocontenida + captura/clip para el deck · `performance.md` con mediciones
(Playwright MCP + devtools) · handoff a frontend con la version del framework del proyecto.
