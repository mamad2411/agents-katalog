# Nuba Frontend — CLAUDE.md

## Qué es este proyecto
Sitio institucional de **Nuba Studio**, una agencia digital que hace páginas web, apps, marketplaces y productos digitales. Es la carta de presentación de la agencia — debe transmitir creatividad, profesionalismo y calidad.

## Stack
- **Next.js** (App Router, TypeScript)
- **Tailwind CSS v4**
- **GSAP + ScrollTrigger** — para animaciones de scroll y micro-interacciones
- **DM Sans** — fuente principal (ya configurada en `layout.tsx`)
- Framer Motion estaba en la versión anterior (branch `main`) — en el nuevo diseño preferir GSAP

## Colores
| Token | Valor |
|---|---|
| Negro | `#000000` |

| Blanco | `#ffffff` |
| Acento lima | `#C6FF00` |

Los colores pueden cambiar — no es definitivo.

## Logo
- SVG en `/public/Nuba logo.svg` — nube estilizada con path stroke negro
- Para fondo oscuro: cambiar stroke a blanco o `#C6FF00`

## Casos de portafolio
Los datos están en el branch `main` en `app/page.tsx` como array `works`. Los casos son:
- **Nuddo** — web & mobile
- **FFMates**
- **Kennedy's**
- **CheckRTO**

Las imágenes están en `/public/images/cases/`.

## Estructura de secciones (nueva versión)
1. **Hero** — fullscreen, tagline grande, video/imagen de fondo, scroll indicator
2. **Works** — grid de proyectos con hover effects
3. **About** — quiénes somos, filosofía
4. **Services** — qué hacemos (web, apps, marketplaces)
5. **Contact** — CTA grande + email + redes

Puede ser one-pager o multi-página — está por definir.

## Animaciones y micro-interacciones acordadas
- GSAP ScrollTrigger para reveals de secciones
- Cursor personalizado (círculo que sigue el mouse)
- Loader inicial antes de mostrar la página
- Parallax sutil en el hero
- Hover reveal de imagen al pasar sobre nombre de proyecto
- Fade-in escalonado de texto en viewport
- Marquee de texto horizontal (servicios, tecnologías, clientes)
- Transiciones de página suaves

## Referencias de diseño
- **Son Daven** (sondaven.com) — oscuro lujoso, SVG transitions, loader con %, parallax
- **REF Digital** (ref.digital) — agencia limpia, hover video en proyectos
- **Pacôme Pertant** (pacomepertant.com) — inmersivo, marquee, GSAP
- **Tresmares Capital** — estructura corporativa clara

## Convenciones
- Fondo oscuro (negro) como base — texto blanco
- Acento `#C6FF00` para CTAs, highlights, bordes activos
- Sin comentarios innecesarios en el código
- Componentes en `app/components/`
