---
name: norteia-formaciones
description: >
  Skill de NorteIA para generar programas de formación completos, profesionales 
  y auditables, módulo a módulo. Genera 4 entregables por módulo: Guía del Formador
  (DOCX), Presentación PPTX, Manual del Participante (DOCX) y Evaluaciones con
  clave de respuestas (DOCX). USAR SIEMPRE cuando el usuario diga "genera la formación
  para", "prepara el curso de", "crea el módulo de", "formación sobre", "programa
  formativo", "curso para", "módulo de formación", "prepara la formación", "training",
  "genera los materiales de", o cualquier referencia a crear contenido formativo,
  materiales didácticos, cursos, talleres o programas de capacitación. También cuando
  mencione "Art. 4", "AI Act", "alfabetización en IA", "FUNDAE", "formación bonificable",
  o cualquier programa educativo para empresas. Aplica a cualquier temática, no solo IA:
  transformación digital, herramientas específicas, soft skills, compliance, etc.
---

# NorteIA Formaciones — Generador de Programas Formativos

## Visión general

Esta skill genera programas de formación profesionales, módulo a módulo, con 4 entregables
por módulo. El flujo es:

1. **FASE 0**: Recoger datos del programa (cliente, temática, audiencia, módulos)
2. **FASE 1**: Generar el plan del programa completo (índice de módulos con duración y contenidos)
3. **FASE 2**: Producir módulo a módulo (4 entregables cada uno) hasta completar el programa
4. **FASE 3**: Módulo final de evaluación + certificado (si el programa lo incluye)

Cada módulo se produce en una interacción separada. El usuario dice "siguiente módulo" o 
"genera el módulo X" para avanzar.

---

## FASE 0 — Recoger datos del programa

Si el usuario no los ha proporcionado, solicitar estos campos. Si los ha dado parcialmente,
extraer lo disponible y preguntar solo lo que falte.

```
FORMULARIO — PROGRAMA FORMATIVO NORTEIA

1. DATOS DEL CLIENTE
   - Nombre de la organización: _______________
   - Sector de actividad: _______________
   - Tamaño (nº empleados aprox.): _______________
   - Herramientas/sistemas relevantes que usa: _______________
   - Logo o marca para personalizar (si procede): _______________

2. DATOS DEL PROGRAMA
   - Temática principal: _______________
   - Objetivo general del programa: _______________
   - Destinatarios (perfil, nivel, rol): _______________
   - Duración total estimada (horas): _______________
   - Modalidad: [Online tutorizado / Presencial / Blended]
   - ¿Bonificable FUNDAE?: [Sí / No]
   - ¿Incluye evaluación final con certificado?: [Sí / No]

3. PERSONALIZACIÓN
   - Nivel de los participantes: [Básico / Intermedio / Avanzado / Mixto]
   - Idioma: [Español / Otro]
   - Marca visual: [NorteIA estándar / Personalizada por cliente]
   - Paleta de colores preferida (si no NorteIA): _______________

4. CONTEXTO ADICIONAL (opcional)
   - Documentación de referencia proporcionada por el usuario
   - Requisitos normativos específicos
   - Necesidades especiales del grupo
```

Si el usuario proporciona un documento de referencia (como un research, un brief o un plan),
usarlo como base para diseñar los contenidos del programa.

---

## FASE 1 — Plan del programa

Antes de generar ningún entregable, presentar al usuario el **plan del programa completo**:

```
PLAN DEL PROGRAMA: [Nombre del programa]
Cliente: [Nombre]
Duración total: [X] horas
Nº módulos: [N]

| # | Módulo | Duración | Contenidos clave | Nivel |
|---|--------|----------|------------------|-------|
| 1 | ...    | ...      | ...              | ...   |
| 2 | ...    | ...      | ...              | ...   |
| N | Evaluación final y cierre | 1h | Test + casos + certificado | — |
```

El usuario confirma o ajusta antes de proceder. Solo después de confirmación se empieza
a producir módulo a módulo.

---

## FASE 2 — Producción módulo a módulo

### Flujo por módulo

Para cada módulo, generar **4 entregables** en este orden:

1. **Guía del Formador** (.docx) — Ver `references/guia-formador.md`
2. **Presentación** (.pptx) — Ver `references/presentacion.md`
3. **Manual del Participante** (.docx) — Ver `references/manual-participante.md`
4. **Evaluaciones** (.docx) — Ver `references/evaluaciones.md`

### Proceso técnico por entregable

1. Leer la skill DOCX (`/mnt/skills/public/docx/SKILL.md`) antes de crear documentos Word
2. Leer la skill PPTX (`/mnt/skills/public/pptx/SKILL.md`) antes de crear presentaciones
3. Instalar dependencias si no están disponibles:
   ```bash
   npm install -g pptxgenjs docx react react-dom react-icons sharp
   pip install "markitdown[docx]" Pillow --break-system-packages
   ```
4. Generar cada archivo con Node.js (docx-js para .docx, pptxgenjs para .pptx)
5. Validar cada .docx con `python scripts/office/validate.py`
6. Hacer QA visual del .pptx:
   - Convertir a PDF + imágenes
   - Inspeccionar al menos 2-3 slides clave
   - Corregir si hay problemas
7. Copiar todos los archivos a `/mnt/user-data/outputs/` y usar `present_files`

### Nomenclatura de archivos

```
M[N]-[Audiencia]-[Tipo]-NorteIA.ext

Ejemplos:
M1-Usuarios-Guia-Formador-NorteIA.docx
M1-Usuarios-Presentacion-NorteIA.pptx
M1-Usuarios-Manual-Participante-NorteIA.docx
M1-Usuarios-Evaluaciones-NorteIA.docx
```

Audiencia: Usuarios, Directivos, Técnicos, o lo que corresponda al programa.

---

## FASE 3 — Módulo de evaluación final (si aplica)

El último módulo del programa es especial. Genera:

1. **Guía del Formador** — protocolo de evaluación, criterios de superación, dosier de evidencia
2. **Presentación** — slides de apertura/cierre (breve, 6-8 slides)
3. **Cuadernillo de evaluación** — test final (20 preguntas) + casos prácticos + encuesta satisfacción
4. **Clave de respuestas + Certificado** — respuestas + guía de corrección + plantilla certificado

---

## Sistema de diseño

### Leer SIEMPRE antes de producir

Antes de generar cualquier entregable, leer el archivo de referencia correspondiente:

| Entregable | Referencia |
|-----------|------------|
| Guía del Formador | `references/guia-formador.md` |
| Presentación PPTX | `references/presentacion.md` |
| Manual del Participante | `references/manual-participante.md` |
| Evaluaciones | `references/evaluaciones.md` |
| Sistema visual NorteIA | `references/diseno-norteia.md` |
| Marco pedagógico | `references/pedagogia-norteia.md` |

### Paleta de colores NorteIA (por defecto)

```
Navy (primario):  #1A2B4A   — Fondos de portada, headers de tabla, títulos
Cyan (acento):    #0891B2   — Acentos, logo "IA", enlaces, CTAs
Ice (fondo):      #F0F9FF   — Fondos claros de contenido
Text (cuerpo):    #1E293B   — Texto principal
Muted (secundario): #64748B — Texto secundario, subtítulos
White:            #FFFFFF   — Fondos de tarjetas
Green:            #059669   — Tips, buenas prácticas, confianza alta
Amber:            #D97706   — Notas, advertencias, confianza media
Red:              #DC2626   — Alertas, riesgos, confianza baja, prohibido
```

### Acento temático por módulo

Cada módulo puede tener un color de acento diferente para diferenciarlo visualmente.
El acento se usa en: barra lateral de portada, línea bajo títulos, divisores de sección,
badges de tiempo en agenda, y elementos destacados. Ejemplos:

- Fundamentos: Cyan (#0891B2)
- Riesgos: Red (#DC2626)
- Normativo: Indigo (#4F46E5)
- Práctico: Teal (#0D9488)
- Evaluación: Gold (#B45309)

### Tipografía

**DOCX**: Arial (headings + body). Alternativa: Calibri body con Arial headings.
**PPTX**: Trebuchet MS (headings) + Calibri (body).

### Logo

Texto: "NORTE" en color navy + "IA" en color cyan. Siempre juntos, siempre en bold.

### Web

Siempre incluir `www.norteia.es` en: portada, footer de todas las páginas, slide de cierre.

---

## Herramientas pedagógicas originales NorteIA

Estas herramientas son propiedad intelectual de NorteIA y deben integrarse en los
programas cuando sea relevante:

### Protocolo VERIFICA (interpretación de resultados de IA)

```
V — Veracidad: ¿Los datos factuales son correctos?
E — Exhaustividad: ¿Falta algo importante?
R — Relevancia: ¿Responde a lo que necesito?
I — Imparcialidad: ¿Hay sesgo injustificado?
F — Formato: ¿Tono y extensión adecuados?
I — Info sensible: ¿Contiene datos que no deberían estar?
C — Consecuencias: ¿Qué pasa si hay un error?
A — Autoría: ¿Lo firmarías como tuyo?
```

### Protocolo PARA (escalación de incidencias)

```
P — PARA: Deja de usar ese resultado inmediatamente
A — ANALIZA: ¿Qué ha pasado? ¿Alucinación, sesgo, fuga?
R — REPORTA: Informa al responsable designado
A — ALTERNATIVA: Busca otra forma de completar la tarea
```

### Test del Tablón de Anuncios (privacidad)

"Antes de introducir información en una herramienta de IA, pregúntate:
¿colgaría esto en el tablón de anuncios de la oficina?"

### Los 6 Compromisos del Usuario Alfabetizado (Art. 4)

1. Sé qué es la IA
2. Conozco los riesgos
3. Conozco las reglas
4. Uso la IA con criterio
5. Protejo la información
6. Escalo cuando toca

### Espectro de Confianza

| Nivel | Cuándo | Verificar |
|-------|--------|-----------|
| Alta | Brainstorming, borradores, ideas | No obligatorio |
| Media | Resúmenes, análisis, traducciones | Recomendado |
| Baja | Datos factuales, cifras, leyes, médico | SIEMPRE |

### 7 Técnicas de Prompting

1. Contexto claro
2. Rol específico
3. Formato deseado
4. Ejemplos (few-shot)
5. Restricciones
6. Paso a paso
7. Iteración

Estas herramientas se incluyen cuando son relevantes para la temática del programa,
especialmente en programas sobre IA, transformación digital o herramientas digitales.

---

## Requisitos de documentación auditable

Si el programa es bonificable FUNDAE o busca cumplir el Art. 4 del AI Act, cada módulo
debe generar evidencia:

- Registro de asistencia con campos: nombre, DNI/NIE, firma, fecha, hora
- Programa detallado de la sesión
- Materiales didácticos entregados
- Resultados de evaluación
- Certificado individual (en el módulo final)

---

## Checklist de calidad por entregable

Antes de entregar cada archivo, verificar:

- [ ] Portada con marca NorteIA + www.norteia.es + nombre módulo + datos programa
- [ ] Header y footer en todas las páginas de contenido
- [ ] Tablas con estilo NorteIA (header navy, bordes suaves, cell margins)
- [ ] Cajas de acento (tip/nota/alerta) con borde lateral coloreado
- [ ] Sin errores de validación (.docx)
- [ ] Sin errores de color hex (.pptx — nunca usar # ni 8 caracteres)
- [ ] Slides visualmente variados (nunca repetir layout 2 veces seguidas)
- [ ] Contenido en español (salvo que se indique otro idioma)
- [ ] Terminología coherente entre los 4 entregables del mismo módulo
