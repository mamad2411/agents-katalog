---
name: visual-hierarchy-composition
description: Composición y jerarquía visual para dirigir la mirada — escala, peso, color y espacio como herramientas de énfasis, punto focal único, contraste y proximidad (Gestalt), ritmo y whitespace, patrones de lectura en Z y en F, y densidad según el tipo de vista (marketing, herramienta densa, dashboard). Usar al componer una pantalla nueva, al diagnosticar una interfaz donde "todo compite" o "no sé dónde mirar", y al revisar si el orden visual coincide con el orden de importancia.
---

<!-- ESPEJO GENERADO por AtlasPromptManager/tools/install_skills.py - NO EDITAR A MANO -->
<!-- La fuente es AtlasPromptManager/.claude/skills/. Lo que edites aca se pierde. -->

# Jerarquía visual y composición — dirigir la mirada

Componer es decidir el **orden en que el ojo recorre la pantalla** y hacer que coincida
con la importancia real. `frontend-ui-design` cubre el proceso y las leyes; acá se
profundiza en la técnica de énfasis y la composición. Si además hay que puntuar la
pantalla terminada, usá `ui-quality-review`.

## 1. Las cuatro herramientas de énfasis

Se ordenan por fuerza perceptual. Combiná pocas, no todas a la vez:

1. **Escala** — lo grande se ve primero. La herramienta más fuerte y la más abusada.
2. **Peso / contraste** — un texto en negrita o de alto contraste destaca sin ser más
   grande. Dos elementos del mismo tamaño con distinto contraste ya tienen jerarquía.
3. **Color** — un solo color de acento marca la acción o el dato clave. Si todo tiene
   color, nada resalta. Reservá el acento para lo que querés que se toque/lea primero.
4. **Espacio** — aislar un elemento con aire alrededor lo jerarquiza tanto como agrandarlo.
   El whitespace no es relleno: es énfasis.

Regla: para destacar algo, subí **una** palanca fuerte, no las cuatro. Un botón primario
no necesita ser más grande **y** de color **y** en negrita **y** con sombra — elegí.

## 2. Un solo punto focal

Cada pantalla tiene un elemento que gana. Si hay tres cosas gritando, no hay ninguna.
Definí el foco primario, luego el secundario (claramente por debajo) y el resto es fondo.
Test: entorná los ojos hasta que se vea borroso — lo que sigue destacando es tu jerarquía
real. Si destaca lo que no debía, corregí.

## 3. Gestalt aplicado a la composición

- **Proximidad**: lo que está cerca se percibe relacionado. Agrupás con espacio, no con
  cajas ni líneas. Más espacio *entre* grupos que *dentro* de cada grupo.
- **Similitud**: mismo estilo = mismo tipo de cosa. Si dos elementos se ven iguales, el
  usuario espera que hagan lo mismo.
- **Continuidad y alineación**: elementos alineados se leen como un conjunto ordenado; un
  borde que baila 3 px rompe la sensación de calidad.
- **Región común / cierre**: un fondo o borde compartido agrupa aun sin proximidad.

## 4. Ritmo, whitespace y grilla

- Escala de espaciado consistente (múltiplos de 4/8): el ritmo se siente aunque no se vea.
- Espaciado como sistema, no como decisión caso por caso — usá tokens (`frontend-design-system`).
- Alineá todo a una grilla; los ejes fuertes (izquierda del contenido, línea de base
  tipográfica) guían el ojo hacia abajo sin esfuerzo.
- El whitespace generoso comunica calma y foco (producto premium); el denso comunica
  eficiencia (herramienta de poder). Elegí a propósito, no por defecto.

## 5. Patrones de lectura

- **Z**: pantallas simples y de marketing con poco contenido — el ojo va de arriba-izq a
  arriba-der, cruza y baja. Poné logo/marca arriba-izq, CTA en los vértices del recorrido.
- **F**: pantallas con mucho texto o listas — el ojo escanea la primera línea, baja por la
  izquierda, escanea de a saltos. Poné lo importante al inicio de cada bloque, izquierda arriba.
- **Capas**: en apps densas el patrón lo define la jerarquía que vos construís, no un
  recorrido natural — por eso el punto focal (§2) importa más ahí.

## 6. Densidad por tipo de vista

| Tipo de vista | Densidad | Énfasis |
|---|---|---|
| Marketing / landing | Baja: mucho aire, pocas cosas grandes | Un CTA claro, patrón en Z |
| Herramienta densa (agenda, tablas) | Alta: información compacta pero legible | Agrupación y alineación fuertes; medida de línea corta |
| Dashboard | Media: bloques con jerarquía interna | KPI primario destacado, resto de apoyo (`dashboard-data-ui`) |
| Formulario / flujo | Baja-media: un paso a la vez | Foco en el campo activo y en la acción de avanzar |

## 7. Errores típicos

- Todo compite: cinco elementos con escala/color/peso máximos → cero jerarquía.
- Sin foco: la pantalla es un mar uniforme; nada dice "empezá acá".
- Énfasis sobrecargado: el mismo elemento con las 4 palancas subidas.
- Centrado por defecto: todo centrado porque evita decidir un eje de alineación.
- Espaciado igual dentro y entre grupos: se pierde la relación por proximidad.

## Checklist

- [ ] Entorné los ojos: destaca lo que debe destacar, no otra cosa.
- [ ] Un punto focal primario; secundario claramente por debajo.
- [ ] Para cada énfasis subí una palanca fuerte, no las cuatro.
- [ ] Grupos separados por más espacio del que tienen adentro (proximidad).
- [ ] Todo alineado a la grilla; espaciado por tokens, no valores sueltos.
- [ ] La densidad corresponde al tipo de vista.
