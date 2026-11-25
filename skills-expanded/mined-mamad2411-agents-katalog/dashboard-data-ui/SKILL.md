---
name: dashboard-data-ui
description: Diseño de interfaces con mucha densidad de datos — elegir el gráfico correcto según la pregunta, tarjetas de KPI honestas, tablas densas legibles, filtros y rango temporal, jerarquía resumen→detalle, color con significado, accesibilidad de gráficos y estados de dato por widget (cargando, vacío, parcial, error). Usar al diseñar un dashboard, un panel analítico, una vista de reportes o cualquier pantalla con métricas, gráficos y tablas juntos, y al revisar por qué un tablero "abruma" o no responde ninguna pregunta.
---

<!-- ESPEJO GENERADO por AtlasPromptManager/tools/install_skills.py - NO EDITAR A MANO -->
<!-- La fuente es AtlasPromptManager/.claude/skills/. Lo que edites aca se pierde. -->

# Interfaces de datos y dashboards

Un dashboard no es una pared de gráficos: es la respuesta a un puñado de preguntas concretas.
Antes de maquetar, escribí las 3–5 preguntas que la persona necesita responder de un vistazo
y qué decisión toma con cada una. Todo lo que no sirva a una pregunta, sobra.

## 1. El gráfico correcto según la pregunta

| La pregunta es… | Gráfico |
|---|---|
| ¿Cómo evoluciona en el tiempo? | Línea (área solo si importa la magnitud acumulada) |
| ¿Cómo se comparan categorías? | Barras (horizontales si las etiquetas son largas) |
| ¿Qué parte del total es cada cosa? | Barra apilada 100% o pocas rebanadas; **no** torta con 8+ rebanadas |
| ¿Hay correlación entre dos variables? | Dispersión |
| ¿Cuál es el valor puntual ahora? | Tarjeta KPI (número grande) |
| ¿Cómo se distribuye una variable? | Histograma / caja |

Reglas: eje Y en cero para barras (si no, exagera diferencias); nunca torta 3D ni doble eje Y
engañoso; etiquetá series directamente antes que depender de una leyenda lejana. La técnica de
paletas y encoding de gráficos está en `dataviz` si existe; no la repito acá.

## 2. Tarjetas de KPI honestas

- Número grande + etiqueta clara + contexto (comparación vs período anterior, meta, o tendencia
  en un sparkline). Un número sin referencia no informa.
- Mostrá la dirección con icono + signo + color, no solo color (ver `color-systems`).
- Unidad y período explícitos ("últimos 30 días"), no un número flotando.
- No infles: 3–6 KPI arriba, no 15. Si todo es KPI, nada es KPI.

## 3. Tablas densas pero legibles

- Alineá números a la derecha con `tabular-nums`; texto a la izquierda; fechas consistentes.
- Encabezados fijos (`position: sticky`) en tablas largas; zebra sutil o solo líneas finas, no ambas.
- Columna clave primero; acciones al final; oculta/colapsa lo secundario en pantallas chicas.
- Densidad configurable (cómoda/compacta) si el usuario vive en la tabla.
- Orden, filtro y paginación (por cursor, ver el backend) coherentes. El detalle de tablas
  vive en `frontend-data-tables`; acá solo su lugar en el tablero.

## 4. Filtros y rango temporal

- Un control de rango temporal global y visible; que se note qué rango está aplicado.
- Los filtros activos se muestran como chips removibles; nada de filtros "fantasma" que
  alteran los números sin que se vea por qué.
- Estado de filtros reflejado en la URL (compartible, recargable).
- Al cambiar un filtro, indicá que los datos se están recalculando (ver estados abajo).

## 5. Jerarquía resumen → detalle

Lo más importante arriba a la izquierda (lectura en Z/F): primero el titular (KPIs), después
las tendencias, después el detalle navegable. Permití profundizar (drill-down) en vez de
mostrar todo a la vez. Agrupá widgets relacionados con espacio y encabezados de sección, no
con cajas dentro de cajas dentro de cajas.

## 6. Estados de dato POR widget

Cada widget trae datos por su cuenta y puede fallar solo. No dejes que un panel roto tumbe el
tablero. Resolvé, por widget:

| Estado | Tratamiento |
|---|---|
| Cargando | Skeleton con la forma del widget, no un spinner centrado en toda la página |
| Vacío | "Sin datos en este rango" + qué hacer (ampliar rango, quitar filtro) |
| Parcial | Mostrá lo que hay + aviso de que falta una fuente; no finjas completo |
| Error | Mensaje acotado al widget + reintentar; el resto del tablero sigue vivo |

El catálogo completo de estados y su redacción está en `frontend-ux-states`.

## 7. Accesibilidad de gráficos

- El gráfico no puede ser la **única** forma de acceder al dato: ofrecé la tabla equivalente
  (o `aria`/resumen textual). Un `<canvas>` es invisible para el lector de pantalla.
- No distingas series solo por color: forma de punto, patrón, o etiqueta directa (daltonismo).
- Contraste de la serie contra el fondo ≥ 3:1 (criterio 1.4.11).
- Tooltips accesibles por teclado, no solo por hover.
- Respetá `prefers-reduced-motion` en transiciones de datos (ver `frontend-motion`).

## Anti-patrones

- Pantalla llena de gráficos sin una pregunta detrás de cada uno.
- Torta con muchas rebanadas / 3D / doble eje engañoso.
- KPI sin comparación ni unidad ni período.
- Series distinguidas solo por color.
- Un solo spinner para todo el tablero; un error que tumba toda la vista.
- Filtros que cambian los números sin dejar ver cuáles están activos.

## Checklist

- [ ] Cada widget responde una pregunta escrita de antemano.
- [ ] Tipo de gráfico correcto para la pregunta; barras desde cero, sin torta sobrecargada.
- [ ] KPIs con contexto (comparación/meta), unidad y período; 3–6, no 15.
- [ ] Tablas con números a la derecha + `tabular-nums`, encabezado fijo, orden/filtro claros.
- [ ] Rango temporal global visible; filtros activos como chips y en la URL.
- [ ] Cada widget resuelve cargando/vacío/parcial/error por su cuenta.
- [ ] Datos accesibles también sin color y sin el gráfico (tabla/resumen), contraste de serie ≥ 3:1.

Estados: `frontend-ux-states`. Tablas: `frontend-data-tables`. Color: `color-systems`.
Accesibilidad: `frontend-accessibility`. Performance de render pesado: `frontend-performance`.
