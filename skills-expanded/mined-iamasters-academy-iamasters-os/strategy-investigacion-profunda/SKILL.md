---
name: strategy-investigacion-profunda
description: Genera informes completos de investigación profunda en español con triangulación multi-fuente, scoring de credibilidad, verificación de afirmaciones y salida Markdown + HTML. Úsala para decisiones complejas, estudios comparativos, estado del arte o research reports; para búsqueda ligera de 3-5 fuentes usa `strategy-web-research`.
---

# Investigación Profunda

## Propósito

Entregar informes de investigación con citas verificadas a través de un pipeline estructurado de 8 fases, con persistencia de evidencia, gestión de identidad de fuentes, verificación a nivel de afirmación, y control progresivo del contexto. Réplica adaptada del repo `199-biotechnologies/claude-deep-research-skill` para entorno Claude.ai (web/app).

**Diferencia con `strategy-web-research`:** `strategy-web-research` sirve para búsqueda ligera y rápida con 3-5 fuentes. `strategy-investigacion-profunda` se usa cuando hace falta informe completo con triangulación, scoring de fuentes, evidencias persistidas y verificación de afirmaciones.

**Principio de autonomía:** Opera de forma independiente. Infiere asunciones del contexto. Solo te detienes para errores críticos o preguntas incomprensibles. Hace explícitas las asunciones de alto impacto en la Introducción y Metodología en lugar de adoptarlas en silencio.

**Idioma:** El informe se redacta SIEMPRE en español (es el público objetivo), aunque las fuentes consultadas pueden estar en cualquier idioma. Las citas mantienen el título original de la fuente.

---

## Flujo de inicio (OBLIGATORIO)

Antes de empezar la investigación:

1. **Confirmar tema y modo con el usuario.** Si el usuario no ha especificado el modo, preguntar con `ask_user_input_v0` (un solo `single_select`):
   - **Quick** (3 fases, 2-5 min, 2.000-4.000 palabras) — Exploración inicial
   - **Standard** (6 fases, 5-10 min, 4.000-8.000 palabras) — Mayoría de casos
   - **Deep** (8 fases, 10-20 min, 8.000-15.000 palabras) — Decisiones críticas
   - **UltraDeep** (8+ fases, 20-45 min, 15.000-20.000 palabras) — Máximo rigor

2. **Si el tema es ambiguo**, pedir clarificación SOLO si es indispensable (ej. "compara X vs Y" sin decir X o Y). En caso contrario, inferir y declarar la asunción en la Introducción.

3. **Crear carpeta de trabajo** en `projects/investigacion/<YYYY-MM-DD>/<tema-slug>/` para todos los artefactos.

---

## Árbol de decisión

```
Análisis de la solicitud
├── ¿Búsqueda simple? → PARAR: usa web_search directo
├── ¿Pregunta factual rápida? → PARAR: responde sin skill
└── ¿Análisis complejo? → CONTINUAR

Selección de modo
├── Exploración inicial → quick (3 fases)
├── Investigación estándar → standard (6 fases) [SUGERIDO POR DEFECTO]
├── Decisión crítica → deep (8 fases)
└── Revisión exhaustiva → ultradeep (8+ fases)
```

**Asunciones por defecto:** Pregunta técnica = audiencia técnica. Comparación = perspectiva equilibrada. Tendencia = últimos 1-2 años.

---

## Visión general del flujo de trabajo

| Fase | Nombre | Quick | Std | Deep | Ultra |
|------|--------|-------|-----|------|-------|
| 1 | SCOPE (Encuadre) | ✓ | ✓ | ✓ | ✓ |
| 2 | PLAN (Estrategia) | - | ✓ | ✓ | ✓ |
| 3 | RETRIEVE (Recuperación) | ✓ | ✓ | ✓ | ✓ |
| 4 | TRIANGULATE (Triangulación) | - | ✓ | ✓ | ✓ |
| 4.5 | OUTLINE REFINEMENT (Refino de esquema) | - | ✓ | ✓ | ✓ |
| 5 | SYNTHESIZE (Síntesis) | - | ✓ | ✓ | ✓ |
| 6 | CRITIQUE (Crítica) | - | - | ✓ | ✓ |
| 7 | REFINE (Refinamiento) | - | - | ✓ | ✓ |
| 8 | PACKAGE (Empaquetado) | ✓ | ✓ | ✓ | ✓ |

**Nota:** Las fases 3-5 operan como un bucle de evidencia por sección (recuperar → almacenar evidencia → refinar esquema → redactar → verificar afirmaciones → buscar deltas si hace falta), no como puertas secuenciales estrictas.

---

## Ejecución

**Al invocar la skill, cargar los archivos de referencia relevantes:**

1. **Fases 1-7:** Lee [reference/methodology.md](./reference/methodology.md) para instrucciones detalladas de cada fase
2. **Fase 8 (Informe):** Lee [reference/report-assembly.md](./reference/report-assembly.md) para generación progresiva
3. **Salida HTML:** Lee [reference/html-generation.md](./reference/html-generation.md)
4. **Controles de calidad:** Lee [reference/quality-gates.md](./reference/quality-gates.md)

**Plantillas:**
- Estructura del informe: [templates/report_template.md](./templates/report_template.md)
- Estilo HTML: [templates/mckinsey_report_template.html](./templates/mckinsey_report_template.html)

**Scripts (ejecutar desde la raíz del skill):**
- `python scripts/validate_report.py --report [ruta]` — 9 checks de estructura
- `python scripts/verify_citations.py --report [ruta]` — verificación de citas y bibliografía
- `python scripts/source_evaluator.py --url [url]` — scoring de credibilidad 0-100
- `python scripts/md_to_html.py [ruta_md]` — conversión a HTML McKinsey

---

## Herramientas disponibles en este entorno

A diferencia del repo original (Claude Code), aquí en Claude.ai trabajas con:

- ✅ **`web_search`**: búsqueda principal. Lánzala en serie u en batch (varias llamadas seguidas) para paralelismo lógico.
- ✅ **`web_fetch`**: para extraer contenido completo de URLs específicas tras una búsqueda.
- ✅ **`bash_tool` + `create_file`**: ejecutar scripts Python de validación y guardar archivos.
- ❌ **No hay** `search-cli`, subagentes Task, ni MCPs custom. Sustituye batches de Task por múltiples `web_search` consecutivas con queries distintas.
- ❌ **No hay PDF nativo**. Solo MD + HTML como salida final.

---

## Contrato de salida

**Secciones obligatorias del informe (en español):**
- **Resumen ejecutivo** (200-400 palabras)
- **Introducción** (alcance, metodología, asunciones)
- **Análisis principal** (4-8 hallazgos, 600-2.000 palabras cada uno, con citas)
- **Síntesis e implicaciones** (patrones, conexiones)
- **Limitaciones y caveats**
- **Recomendaciones**
- **Bibliografía** (COMPLETA — toda cita usada, sin marcadores ni rangos)
- **Anexo metodológico**

**Archivos de salida (todos en `projects/investigacion/<YYYY-MM-DD>/<tema-slug>/`):**
- `informe_[YYYYMMDD]_[slug].md` — fuente de verdad
- `informe_[YYYYMMDD]_[slug].html` — versión estilo McKinsey
- `sources.json` — registro de fuentes con IDs estables
- `evidence.json` — evidencias con citas literales y localizadores
- `claims.json` — afirmaciones atómicas con estado de soporte
- `run_manifest.json` — consulta, modo, asunciones, configuración

**Estándares de calidad:**
- 10+ fuentes, 3+ por cada afirmación importante (independientes entre sí, no solo en número)
- Toda afirmación factual citada inmediatamente con [N] y respaldada en `evidence.json`
- Verificación de soporte de afirmaciones obligatoria: no pasan al entregable afirmaciones sin respaldo
- Sin marcadores, sin citas fabricadas
- Prosa primero (≥80%), viñetas con moderación

---

## Cuándo usar / NO usar

**SÍ usar:** Análisis exhaustivo, comparaciones tecnológicas, revisiones de estado del arte, investigación multi-perspectiva, análisis de mercado, decisiones estratégicas que requieren evidencia.

**NO usar:** Búsquedas simples, debugging, respuestas de 1-2 búsquedas, consultas urgentes que solo necesitan un dato.

Skill original de Angel Aparicio (IA Masters Academy), adaptada para iamasters-os.
