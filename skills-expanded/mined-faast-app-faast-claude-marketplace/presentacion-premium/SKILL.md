---
name: presentacion-premium
description: Reglas de deck de lanzamiento para el equipo de Marketing - como se ve y se arma una presentacion comercial con estetica de keynote de Apple o de presentacion de un hiperdeportivo, y no una plantilla generica - estructura que sigue el desglose (apertura, contexto, una seccion por parte con portada, detalle, como funciona y resultado, benchmark, hoja de ruta, cierre, anexo), una idea por lamina, jerarquia y escala tipografica, grilla y aire, color con un solo acento de marca, tratamiento de capturas reales del producto, cifras gigantes con nota, graficos limpios, ritmo entre laminas de impacto y de explicacion, storyboard antes de construir, formatos (PowerPoint editable con skill pptx, PDF, HTML navegable o Artifact de presentacion), skills de diseño premium a usar si existen, accesibilidad y la lista de anti-patrones que hacen que un deck se vea horrible. Cargala antes de diseñar cualquier deck.
---

# Presentacion premium — deck de lanzamiento, no plantilla

## 1. Principios (no negociables)
1. **Una idea por lamina.** Si el titular necesita "y", son dos laminas.
2. **El producto real es la imagen principal.** Capturas reales grandes, bien enmarcadas; nunca
   iconos genericos en su lugar.
3. **La cifra es la noticia.** Cuando hay un numero fuerte, va a pantalla completa: numero gigante,
   unidad pequeña, una linea de contexto, nota de fuente.
4. **Aire.** Margenes ≥ 6% del ancho; mas vacio que lleno.
5. **Un acento.** Paleta neutra (negro/blanco/grises calidos o frios) + el acento de marca (ver
   `marca-faast`). Nada de 6 colores.
6. **Ritmo.** Alternar impacto (imagen o cifra a pantalla completa) y explicacion (2-3 elementos).
7. **Cada lamina tiene un trabajo.** Si no se puede decir cual, se elimina.

## 2. Estructura (hereda el desglose)
```
Apertura (1-3) → Contexto de mercado (2-4)
→ [por cada parte P01..Pnn, en el orden de la narrativa]
    Portada de la parte (imagen principal + titular)
    Detalle (que es, para quien)
    Como funciona (2-4 pasos con pantallas reales)
    Resultado (que gana: cifra con nota; antes/despues)
    (opcional) Benchmark de la parte
→ Benchmark general (1-2) → Hoja de ruta (1) → Cierre con la propuesta (1-2) → Anexo (fuentes, supuestos, origen de pantallas)
```
Deck para enviar (sin presentador): 8-12 laminas autoexplicativas, una por parte + apertura y cierre.

## 3. Tipografia
- 2 familias como maximo (display + texto), con licencia; las de la marca si estan confirmadas
  (ver `marca-faast`: el sitio usa Lato y Open Sauce One).
- Escala (16:9, 1920x1080): titular de impacto 96-160 pt; titular 54-72 pt; subtitulo 28-36 pt;
  cuerpo 24-28 pt (minimo absoluto 24); nota 12-14 pt.
- Tracking negativo leve en titulares grandes; interlineado 1,05-1,15 en titulares, 1,3-1,4 en cuerpo.
- Numerales tabulares en tablas y cifras; montos con su moneda (`US$`, `$`, `S/`, `COP`).
- Alineacion a la izquierda por defecto; centrado solo en laminas de impacto.

## 4. Grilla y composicion
- 12 columnas, margen exterior 96-120 px, medianil 24-32 px.
- Composiciones base: (a) imagen a sangre + titular; (b) captura 2/3 + texto 1/3; (c) cifra
  gigante centrada; (d) pasos en fila (3-4) con capturas; (e) antes/despues en espejo; (f) matriz
  de benchmark.
- No repetir la misma composicion mas de 2 laminas seguidas.

## 5. Capturas reales del producto
- Desde `desglose/capturas/` (1920x1080 o 2x), nunca reescaladas hacia arriba.
- Tratamiento: recorte limpio con radio suave y sombra difusa, o marco de dispositivo sobrio; fondo
  neutro u oscuro profundo con luz suave detras ("estudio").
- Zoom/detalle: recorte de la zona relevante a gran tamaño con un indicador sutil (no flechas rojas).
- Prototipo o maqueta: rotulo discreto "Prototipo" / "Concepto" en la esquina.
- Datos: ficticios de demo; revisar que no se cuelen nombres reales.

## 6. Cifras y graficos (skill `dataviz` si esta)
- Una serie destacada en el acento; el resto en gris. Etiqueta directa en vez de leyenda.
- Sin 3D, sin sombras, sin tortas de mas de 3 porciones, ejes que empiezan en 0 en barras.
- Toda cifra con nota `[F00x]`/`[S1]` → anexo.

## 7. Benchmark y hoja de ruta
- Benchmark: matriz limpia (FAAST primera columna destacada), estados ✔ / parcial / ✗ /
  "sin info publica", fuente y fecha en la nota. Honesto: si FAAST no tiene algo, se ve.
- Hoja de ruta: tres columnas (Disponible / En construccion / Proximo) o linea de tiempo; nunca
  fechas comprometidas sin confirmacion del usuario.

## 8. Proceso
1. Storyboard (una fila por lamina: bloque, parte, mensaje, imagen, texto, fuente) → revision.
2. Sistema visual (paleta, tipos, escala, grilla, tratamiento de capturas y cifras).
3. Construccion (pptx editable / PDF / HTML navegable / Artifact de presentacion).
4. Previews PNG por lamina y revision con la checklist.

## 9. Herramientas
- `pptx` (PowerPoint editable, notas del orador), `pdf` (export/union), Artifact tipo Slides si la
  sesion lo ofrece, HTML autocontenido navegable (←/→, indice, `prefers-reduced-motion`).
- Diseño: `high-end-visual-design`, `impeccable`, `design-taste-frontend`, `minimalist-ui`,
  `apple-design`, `emil-design-eng`, `dataviz`; del dev-team `design-foundations`, `a11y-checklist`.

## 10. Accesibilidad
Contraste AA (4,5:1 texto; 3:1 texto grande ≥ 24 pt bold), nunca texto sobre foto sin velo, sin
depender solo del color en estados (icono + texto), orden de lectura correcto en pptx, alt text en
imagenes del pptx/HTML.

## 11. Anti-patrones (lo que hace que se vea horrible)
Plantillas de PowerPoint/Canva · fondos con degradado morado o "tech" azul · cajas de colores con
iconos de stock · clipart y fotos de "gente sonriendo a una pantalla" · bullets en cascada y
parrafos · 6 colores y 4 tipografias · logo en cada lamina y marcas de agua · transiciones de
PowerPoint · mockups genericos de dashboards · pantallas imaginadas · cifras sin fuente · laminas
"Nuestra solucion", "Beneficios", "¿Por que nosotros?" sin parte concreta · copiar laminas o claims
de Apple, Ferrari u otras marcas (se toma el lenguaje, no la marca).

## 12. Sistema de layouts (14 tipos)
| # | Layout | Composicion | Ritmo | Uso |
|---|---|---|---|---|
| L01 | Titular sobre imagen a sangre | imagen 12 col + titular sobre velo | I | apertura, portada de parte |
| L02 | Titular solo | titular centrado 120-160 pt | I | revelacion, respiro |
| L03 | Captura heroe | captura 8 col + titular 4 col | I | portada de parte |
| L04 | Captura + 3 llamadas | captura 7 col + 3 notas numeradas | E | detalle |
| L05 | Macro de detalle | recorte ampliado 12 col + rotulo | I | momento clave |
| L06 | Pasos en fila | 3-4 capturas con numero y verbo | E | como funciona |
| L07 | Cifra gigante | numero 200-320 pt + unidad + nota | I | resultado |
| L08 | Antes / despues | espejo 6 + 6 | E | resultado |
| L09 | Grafico unico | grafico 9 col + conclusion 3 col | E | mercado |
| L10 | Matriz de benchmark | tabla + lectura | E | benchmark |
| L11 | Tres columnas | pilares | E | propuesta de valor |
| L12 | Hoja de ruta | estados o linea de tiempo | E | hoja de ruta |
| L13 | Cierre | frase + siguiente paso + contacto | I | cierre |
| L14 | Anexo denso | tabla 14-16 pt | E | anexo |

## 13. Mapa de ritmo (regla)
Marcar cada lamina I (impacto) o E (explicacion). No mas de 3 E seguidas; cada seccion de parte abre con
I; un respiro (L02) entre bloques; el cierre es I; ningun layout mas de 2 veces seguidas.

## 14. Construccion tecnica
- **pptx**: 16:9 (13,333 × 7,5 in); patron con los layouts como diseños con marcadores nombrados; texto
  real (no imagenes); tipografias del kit (incrustar si la licencia lo permite); imagenes 2x comprimidas;
  notas del orador (guion breve + fuentes); texto alternativo; sin transiciones de PowerPoint.
- **PDF**: fuentes embebidas, vinculos al anexo, peso apto para correo.
- **HTML**: un archivo; `<section>` 1920x1080 escaladas; ←/→ y espacio; indice; `@page { size: 1920px
  1080px; margin: 0 }` para imprimir; `prefers-reduced-motion`; sin dependencias externas.
- **Artifact de presentacion**: si la sesion lo ofrece y el usuario quiere un link privado; el pptx/pdf
  sigue siendo el editable.

## 15. Revision (cuatro pruebas)
1. **Hoja de contactos**: ritmo visible, ninguna lamina "de otro deck".
2. **Tres metros**: al 25% de tamaño se lee el titular y se entiende la idea.
3. **Entrecerrar los ojos**: lo primero que se ve es lo mas importante.
4. **Nota y confidencialidad**: cada cifra con nota y anexo; ningun ID, ruta, cliente ni dato real.

## 16. Ejemplo de seccion de parte (5 laminas)
| Lamina | Layout | Contenido |
|---|---|---|
| Portada | L03 | captura heroe sobre fondo estudio + "02 · Ver el riesgo antes de girar." |
| Detalle | L04 | captura con 3 llamadas (alertas, deudor, decidir) |
| Macro | L05 | recorte de las alertas, rotulo |
| Como funciona | L06 | 1 Carga · 2 Revisa · 3 Decide |
| Resultado | L08 | antes/despues con nota [S1] |

## 17. Checklist del deck
- [ ] Una seccion por parte en el orden de la narrativa; ninguna lamina generica.
- [ ] Una idea por lamina; cuerpo ≥ 24 pt; ≤ 3 niveles; mapa de ritmo valido.
- [ ] Capturas reales con origen; graficos honestos con titulo-conclusion y fuente.
- [ ] Cada cifra con nota y fila en el anexo.
- [ ] Marca segun kit; contraste AA; texto alternativo.
- [ ] Formatos verificados (pptx editable, PDF con fuentes, HTML offline).

## 18. Tratamiento de capturas (referencia)
```css
.captura { border-radius: 14px; box-shadow: 0 40px 80px rgba(0,0,0,.35), 0 8px 20px rgba(0,0,0,.18); }
.estudio { background: radial-gradient(60% 60% at 50% 40%, #2a2d31 0%, #151515 70%); }
.rotulo  { font-size: 14pt; letter-spacing: .08em; text-transform: uppercase; opacity: .7; }
```
En pptx: rectangulo redondeado con relleno de imagen, sombra exterior difusa (40-60 pt, 30-35%), sin borde.

## 19. Notas del orador (formato)
Por lamina: 2-3 frases que el presentador dice (no lee la lamina) + las fuentes de lo que aparece.
> "Antes, revisar a un deudor era tres sistemas y una planilla. Ahora son tres pasos en la pantalla en que
> decides. Los tiempos son una estimacion; si quieres, los calculamos con los tuyos." — Fuentes: S1, wiki (interno).
