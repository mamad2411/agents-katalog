---
name: visual-proof
description: Gate de evidencia visual para cambios de UI — capturas por viewport (móvil, tablet, desktop), tema claro y oscuro, y estados (carga, vacío, error), con inspección real de cada captura y consola/red sin errores. Usar después de cualquier cambio de layout, espaciado, modal, overlay, menú, tabla, formulario, responsive, tema o animación, y antes de declarar verificada una pantalla. Un E2E funcional en verde sin inspección visual solo alcanza "verificado funcionalmente".
effort: high
---

<!-- ESPEJO GENERADO por AtlasPromptManager/tools/install_skills.py - NO EDITAR A MANO -->
<!-- La fuente es AtlasPromptManager/.claude/skills/. Lo que edites aca se pierde. -->

# Prueba visual

Un test E2E afirma sobre el DOM: que el botón existe, que el texto aparece, que la
navegación ocurre. No ve que el botón quedó tapado por un overlay, que la tabla desborda
en móvil, que el texto es ilegible en modo oscuro ni que el modal se corta a 360 px de
ancho. **Verde funcional no es verde visual.**

Y tomar una captura no es mirarla. La evidencia es la **inspección**, no el archivo PNG.

## 1. Cuándo aplica

Cualquier cambio que toque: layout, grid, espaciado, tipografía, color o tokens, modales,
overlays, dropdowns, tooltips, menús, navegación, tablas, cards, formularios, imágenes,
iconografía, indicadores de progreso, responsive, tema claro/oscuro, animación.

No aplica a cambios sin superficie renderizada (lógica pura, tipos, tests). Si dudás de si
un cambio de lógica altera lo que se ve, aplica.

## 2. Niveles de afirmación

| Nivel | Qué se hizo | Qué podés afirmar |
|---|---|---|
| Escrito | Se editó el código | "Cambié X". Nada sobre cómo se ve. |
| Verificado funcionalmente | E2E/DOM en verde, sin mirar capturas | "El flujo funciona". **No** "se ve bien". |
| Verificado visualmente | Matriz de §3 capturada **e inspeccionada**, defectos corregidos y re-capturados | "Verificado visual en los viewports/temas/estados listados". |

Nunca subas de nivel sin la evidencia del nivel. La escalera general está en
`evidence-and-verification`.

## 3. Matriz de captura

Tres ejes. No hace falta el producto cartesiano completo: cubrí cada valor de cada eje al
menos una vez, y cruzá donde el cambio lo haga relevante.

**Viewport** — usá los que el proyecto ya tiene configurados; si no hay, documentá los que
elegiste. Mínimo: un móvil estrecho, una tablet, un desktop. Agregá un ancho **justo a cada
lado** de cada breakpoint que el cambio toque: ahí se rompen los layouts.

**Tema** — claro y oscuro, si el producto tiene ambos.

**Estado** — los que la vista pueda tomar (catálogo completo en `frontend-ux-states`):
cargando · vacío · error · con datos · contenido largo/extremo · sin permiso.

Además, cuando el cambio **es** una interacción, capturá con la interacción hecha: modal
abierto, dropdown desplegado, tooltip visible, foco de teclado sobre el control, campo con
error de validación, hover/activo.

## 4. Cómo capturar (Playwright)

```ts
for (const vp of viewports) {                       // los del proyecto
  await page.setViewportSize(vp.size);
  for (const colorScheme of ['light', 'dark'] as const) {
    await page.emulateMedia({ colorScheme, reducedMotion: 'reduce' });
    await page.goto(url);
    await expect(page.getByRole('heading', { name: titulo })).toBeVisible();
    await page.screenshot({ path: `${dir}/${vp.name}-${colorScheme}.png`, fullPage: true });
  }
}
```

1. Esperá a que la vista esté estable con una aserción web-first, nunca con esperas fijas.
2. `reducedMotion: 'reduce'` evita capturar a mitad de una transición. Si lo que cambió es una animación, revisala aparte (`frontend-motion`).
3. Estados difíciles de provocar (error, vacío, lento): forzalos interceptando la respuesta con `page.route`. Esto es válido para **evidencia visual de UI**; no cuenta como prueba del flujo real contra el backend — etiquetalo así.
4. `fullPage: true` para layout de página; captura del elemento (`locator.screenshot()`) para componentes y overlays.
5. Si el proyecto tema por clase/atributo en vez de `prefers-color-scheme`, activá el tema como lo hace el producto.
6. Datos de prueba sintéticos: jamás datos personales o clínicos reales en capturas (`data-privacy-sensitive`).
7. Serial y con un solo navegador: ver `agent-resource-control`. Patrones de locators y aislamiento: `e2e-playwright`.

## 5. Inspección — la parte que cuenta

Abrí **cada** captura (leela como imagen) y recorré esta lista. Anotá el resultado por
captura, no un "se ve bien" global.

- **Recorte y desborde**: texto cortado, scroll horizontal, contenido fuera del contenedor, modal más alto que el viewport sin scroll.
- **Superposición**: elementos tapados, z-index de overlays/headers fijos, dropdown recortado por un `overflow` del padre.
- **Espaciado y alineación**: ritmo de la escala, bordes alineados, elementos pegados al borde en móvil.
- **Jerarquía y legibilidad**: tamaños, pesos, truncado con sentido, contraste en **ambos** temas.
- **Tema oscuro**: fondos blancos hardcodeados, bordes invisibles, íconos o imágenes que desaparecen, sombras que no leen.
- **Estados**: el vacío explica y ofrece acción; el error dice qué pasó; la carga no hace saltar el layout al resolver.
- **Contenido extremo**: nombre larguísimo, lista de 0/1/muchos, número grande, texto sin espacios.
- **Interacción**: foco visible, estado activo/seleccionado distinguible sin depender solo del color, objetivo táctil suficiente en móvil.
- **Regresión de vecinos**: lo que rodea al cambio sigue igual. Compará con la captura de base si la tomaste.

Defecto encontrado → corregir → **re-capturar la misma celda** → re-inspeccionar. Una
captura vieja no prueba el código nuevo.

## 6. Consola y red

Una pantalla que se ve bien con errores por debajo no está verificada.

```ts
const problemas: string[] = [];
page.on('console', m => { if (m.type() === 'error') problemas.push(`console: ${m.text()}`); });
page.on('pageerror', e => problemas.push(`pageerror: ${e.message}`));
page.on('response', r => { if (r.status() >= 400) problemas.push(`${r.status()} ${r.url()}`); });
// ...recorrido...
expect(problemas).toEqual([]);
```

Registrá los listeners **antes** de navegar. Los 4xx/5xx que el escenario provoca a
propósito (estado de error) se excluyen de forma explícita, no con un filtro general.
En SSR, mirá también los avisos de hidratación de la consola.

## Anti-patrones

- ❌ Tomar las capturas y no abrirlas.
- ❌ Solo desktop, solo tema claro, solo el camino feliz con datos.
- ❌ Declarar "verificado" con el E2E en verde y ninguna imagen mirada.
- ❌ Capturar durante una transición, o con esperas fijas.
- ❌ Corregir un defecto visual y no re-capturar.
- ❌ Actualizar en bloque los snapshots de regresión visual para que pase la suite (`visual-regression-testing`).
- ❌ Capturas con datos reales de personas.

## Evidencia / DoD

Para afirmar **verificado visualmente**, el reporte contiene:

- [ ] Tabla de celdas capturadas: viewport (con px) × tema × estado → ruta del archivo.
- [ ] Por cada captura, el resultado de la inspección de §5 en una línea: `OK` o el defecto hallado.
- [ ] Por cada defecto: descripción → corrección (`archivo:línea`) → ruta de la re-captura.
- [ ] Salida literal de la aserción de consola/red (`problemas` vacío), y las exclusiones deliberadas.
- [ ] Qué capturas usaron respuestas interceptadas.
- [ ] *No cubierto*: celdas de la matriz que no se capturaron, y por qué.

Si falta la inspección, el nivel alcanzado es **verificado funcionalmente**, y se dice así.

## Checklist

- [ ] Móvil, tablet, desktop y los anchos a cada lado de los breakpoints tocados.
- [ ] Claro y oscuro.
- [ ] Carga, vacío, error, con datos y contenido extremo.
- [ ] La interacción cambiada, capturada en su estado abierto/activo/con foco.
- [ ] Cada captura abierta e inspeccionada contra §5.
- [ ] Defectos corregidos y celdas re-capturadas.
- [ ] Consola y red sin errores inesperados.
- [ ] Sin datos reales en las imágenes.
- [ ] El nivel de afirmación del reporte coincide con la evidencia que tengo.
