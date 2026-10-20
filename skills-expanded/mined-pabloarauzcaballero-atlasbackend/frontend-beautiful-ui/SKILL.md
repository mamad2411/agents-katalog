---
name: frontend-beautiful-ui
description: Oficio y pulido visual de interfaz — profundidad con sombras en capas, radios y bordes consistentes, alineación óptica, refinamientos tipográficos, dark mode, empty states y detalle de micro-interacción. Usar al pulir una pantalla ya estructurada, o para diagnosticar por qué una UI correcta funcionalmente "se ve genérica" o "hecha por IA". Para puntuarla con rúbrica y emitir veredicto, `ui-quality-review`.
---

<!-- ESPEJO GENERADO por AtlasPromptManager/tools/install_skills.py - NO EDITAR A MANO -->
<!-- La fuente es AtlasPromptManager/.claude/skills/. Lo que edites aca se pierde. -->

# UI hermosa — oficio y pulido

Esta skill asume que la jerarquía y la estructura ya están resueltas (`frontend-ui-design`)
y que hay tokens (`frontend-design-system`). Acá se trabaja el último 20% que separa
"funciona" de "se siente premium" — el que un usuario no puede nombrar pero nota.

## 1. Profundidad con sombras en capas

Una sombra realista nunca es un solo `box-shadow`: la luz genera una sombra de contacto
(ajustada, oscura, cerca del borde) y una de ambiente (difusa, tenue, lejos). Combiná
2-3 capas en vez de una sombra grande y borrosa:

```css
--shadow-sm: 0 1px 2px rgb(0 0 0 / 0.06);
--shadow-md: 0 1px 2px rgb(0 0 0 / 0.06), 0 4px 8px rgb(0 0 0 / 0.08);
--shadow-lg: 0 2px 4px rgb(0 0 0 / 0.06), 0 12px 24px rgb(0 0 0 / 0.12);
```

- La elevación es una escala (`sm`/`md`/`lg`/`xl`), no un valor por componente inventado
  cada vez — un modal siempre usa la elevación de "modal", nunca "lo que quedó lindo".
  Ver `frontend-design-system` para tokens de elevación.
- Más elevación = sombra más difusa y desplazada, no solo "más oscura".
- En dark mode una sombra oscura no se ve sobre fondo oscuro: la profundidad ahí se logra
  con un borde sutil más claro que el fondo, o con un fondo de superficie un tono más
  claro que el fondo base (ver §5).

## 2. Radios y bordes

- Escala de radios limitada y consistente (p. ej. `sm=6px`, `md=10px`, `lg=16px`, `full`).
  El radio de un elemento anidado es ligeramente menor que el de su contenedor
  (si la card es `lg`, el botón adentro es `md`) — así el padding se ve intencional
  en vez de que las esquinas choquen.
- Bordes de 1px con color de bajo contraste (`border-subtle`, ~10-15% de opacidad sobre
  el fondo) en vez de negro/gris puro — se leen como "borde" sin competir con el
  contenido.
- Nunca mezcles radios de distinta familia en la misma superficie (una card con
  esquinas de 4px y un botón adentro con 20px se ve como que no se diseñaron juntos).

## 3. Degradados y glass — con criterio

- Un degradado sutil (2 stops, diferencia de luminosidad chica) puede dar profundidad a
  un fondo o botón primario; un degradado de 3+ colores saturados en un botón es la
  firma visual más reconocible de "landing genérica hecha rápido". Si lo usás, que la
  diferencia entre stops sea sutil.
- Glassmorphism (`backdrop-filter: blur()` + fondo semitransparente + borde de 1px claro)
  funciona para overlays flotantes sobre contenido con movimiento (barras superiores,
  paneles flotantes) — no lo apliques a superficies grandes y estáticas donde no aporta
  nada y solo cuesta rendimiento de composición.
- Textura y ruido (grain) sutiles pueden evitar el look "demasiado plano" en fondos
  grandes de un solo color — con moderación, nunca sobre texto.

## 4. Alineación óptica

- El centrado matemático no siempre se ve centrado: un ícono de flecha o un triángulo
  necesita 1-2px de ajuste manual para *parecer* centrado (el ojo pesa las formas de
  manera distinta a como las mide una caja).
- El texto en mayúsculas dentro de un botón/badge necesita `letter-spacing` positivo
  (~0.02-0.05em): las mayúsculas juntas sin tracking se ven apretadas.
- Iconos junto a texto: alineá por el centro óptico del ícono (no su bounding box) contra
  la altura x del texto, y usá el mismo color/opacidad que el texto que acompañan salvo
  que el ícono sea la acción principal.

## 5. Refinamientos tipográficos

- `tabular-nums` (o `font-variant-numeric: tabular-nums`) en cualquier columna de
  números que se comparan verticalmente (tablas, precios, contadores) — sin esto, cada
  dígito tiene un ancho distinto y las cifras no alinean.
- `text-wrap: balance` en títulos y encabezados cortos para evitar una última línea
  huérfana de una palabra sola; soporte amplio en navegadores actuales pero limitado a
  bloques de pocas líneas en motores Chromium — no lo apliques a párrafos largos.
  `text-wrap: pretty` (evita huérfanas en párrafos) tiene soporte más parcial (falta en
  Firefox) — usalo como mejora progresiva, nunca como dependencia dura; verificá el
  estado actual en caniuse antes de asumir cobertura total.
- Tracking negativo sutil (~-0.01 a -0.02em) en tamaños de display grandes: a tamaños
  grandes el tracking por defecto de la fuente se ve suelto.
- Line-height ajustado en títulos multi-línea (~1.1) y generoso en cuerpo de texto
  (~1.5-1.6) — ver `frontend-ui-design` §4.

## 6. Dark mode que no es "invertir los colores"

- No inviertas la escala de grises: en dark mode las superficies elevadas son **más
  claras** que el fondo (al revés que en light mode, donde son más blancas/limpias por
  la sombra) — así se percibe qué está "más arriba".
- Bajá la saturación de los colores de acento en dark mode (~10-20%) y subí levemente
  su luminosidad: un color muy saturado sobre fondo oscuro vibra y cansa la vista.
- El negro puro (`#000`) como fondo genera halo/ghosting en pantallas OLED y hace que
  los bordes sutiles desaparezcan — usá un gris muy oscuro (`~#0a0a0f`) como base.
- Sombras no funcionan en dark mode (ver §1) — reemplazalas por borde + diferencia de
  luminosidad de superficie.

## 7. Empty states y detalle de micro-interacción

- Todo estado vacío explica *por qué* está vacío y *qué hacer* a continuación (acción
  primaria incluida) — nunca un texto plano de "No hay datos" sin salida.
- Loading: skeleton que respeta el layout real del contenido final (mismo alto/ancho
  aproximado) en vez de un spinner genérico centrado — evita el salto de layout al
  llegar el dato.
- Feedback inmediato en cada acción disparada por el usuario (click, submit, drag) —
  óptimista cuando el resultado es predecible, con estado de carga visible cuando no.
  Profundizá timing y easing en `frontend-motion`.
- El cursor y el estado de hover comunican affordance: si algo es clickeable, se nota
  antes de hacer click (cambio de fondo, elevación, cursor pointer).

## 8. Anti-slop — patrones genéricos de IA a evitar

- Degradado violeta-a-azul (o rosa-a-naranja) de fondo completo como "hero" por defecto,
  sin relación con la marca o el contenido.
- Emojis como reemplazo de iconografía real en producto serio.
- Cards con la misma sombra grande y difusa, todas idénticas, sin jerarquía entre ellas.
- Texto centrado por defecto en bloques largos (el texto de lectura va alineado a la
  izquierda; centrado solo en titulares cortos).
- Iconos de "check" en círculo de color para cada feature de una lista, sin variar
  nada más.
- Botones con esquinas totalmente redondeadas (`border-radius: 9999px`) aplicado a todo
  sin distinción de jerarquía entre primario/secundario.
- Espaciado uniforme "de más" que hace la pantalla sentirse vacía sin razón compositiva
  (padding grande porque sí, no porque agrupa o separa algo).
- Paleta genérica de morados/índigos como default de cualquier producto sin justificación
  de marca — ver `frontend-ui-design` §5 sobre color por rol.

## Checklist de pulido (antes → después)

- [ ] Sombras en 2-3 capas desde una escala de tokens, no un valor inventado por componente.
- [ ] Radios anidados decrecientes; ninguna mezcla de familias de radio en una misma superficie.
- [ ] Degradados/glass usados con intención puntual, no como default de todo botón/fondo.
- [ ] Íconos alineados ópticamente, no solo por bounding box.
- [ ] `tabular-nums` en toda columna numérica comparable.
- [ ] Dark mode con superficies más claras (no sombras) para indicar elevación.
- [ ] Todo estado vacío tiene explicación + acción; todo loading respeta el layout final.
- [ ] Ningún patrón de la lista anti-slop presente sin justificación consciente.
