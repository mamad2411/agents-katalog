---
name: documento-estandar
description: El documento ejecutivo estandarizado de la Mesa de Servicios y la Propuesta para el cliente - correlativo TIPO-ANO-NNN (BUG, PRY, CTZ) con alcance obligatorio (cliente especifico o transversal), estructura fija por tipo en lenguaje de negocio sin codigo, la Propuesta comercial para cotizaciones y proyectos (objetivo, alcance, entregables, supuestos, exclusiones, plazos, valorizacion, condiciones), como se incrustan las capturas del prototipo, el pipeline HTML -> PDF + DOCX con pandoc/LibreOffice, nombres de archivo, control de versiones del documento y la regla de que nada se inventa (todo sale de la solicitud cerrada). Cargala al redactar o revisar un documento o una propuesta.
---

# Documento estandarizado y Propuesta (Mesa de Servicios)

El documento es el entregable que **cierra** una solicitud: lo lee el lider de producto para
priorizar, el PO para escribir historias, el cliente para validar lo que pidio, y gerencia
para decidir. Por eso es ejecutivo, estandarizado y en lenguaje de negocio. No contiene codigo,
ni nombres de tablas, servicios o endpoints: el COMO lo decide desarrollo despues.

Regla de oro: **nada se inventa**. Cada seccion sale de la solicitud cerrada (`solicitud.md` +
`preguntas.md` con sus respuestas). Lo que no se cerro aparece como "Pendiente" explicito,
nunca se rellena con lo razonable.

## Correlativo y alcance
- Formato: `{TIPO}-{AÑO}-{NNN}` — `BUG-2026-003`, `PRY-2026-014`, `CTZ-2026-007`.
- El correlativo lo asigna el redactor al generar el documento por primera vez, leyendo y
  actualizando `.mesa/correlativos.json`:
  ```json
  { "2026": { "BUG": 3, "PRY": 14, "CTZ": 7 } }
  ```
  Es atomico: se lee, se incrementa, se escribe; nunca se reutiliza un numero (si un documento
  se anula, su numero queda anulado, no se recicla).
- **Alcance obligatorio** en la portada y en el nombre de archivo:
  - `Cliente: {NOMBRE} ({codigo})` cuando es de un cliente especifico (una cotizacion de ACME,
    un proyecto para un cliente).
  - `Transversal` cuando aplica al producto para todos (un bug que ven todos aunque lo reporte
    un cliente, una mejora general).
  - Puede ser `Clientes: ACME, BETA` si es para varios pero no para todos.
- La carpeta de la solicitud se renombra del ID provisional al correlativo:
  `.mesa/solicitudes/SOL-…/` → `.mesa/solicitudes/PRY-2026-014/`.

## Estructura por tipo (secciones fijas, en este orden)

### Portada (todos)
Correlativo · Tipo · Titulo de negocio · Alcance (cliente/transversal) · Producto(s) ·
Prioridad sugerida · Fecha · Version del documento · Elaborado por (mesa) · Estado
(Borrador / Cerrado / Pendiente de aprobacion comercial / Aprobado).

### Resumen ejecutivo (todos)
3-5 lineas que una gerencia entiende sin leer el resto: que se pide, para que, a quien afecta
y que se espera. Si es CTZ, que decision se necesita.

### BUG
1. **Que ve mal el usuario** (una frase, como lo vive el negocio)
2. **Pasos como usuario** (pantalla → accion → dato), numerados
3. **Resultado esperado vs. obtenido**, en terminos de negocio
4. **Desde cuando y con que frecuencia**; que cambio, si se sabe
5. **A quien afecta e impacto de negocio** (proceso frenado, dinero, plazos, solucion provisoria)
6. **Evidencia** (capturas o ejemplos concretos del cliente; IDs de operaciones reales)
7. **Ambiente y perfil** con el que ocurre
8. **Pendientes** (lo que no se pudo cerrar)

### PRY (proyecto / funcionalidad nueva o cambio)
1. **Problema u oportunidad** (el "para que")
2. **Objetivo** medible en negocio
3. **Quienes lo usan** (perfiles) y quien aprueba por el cliente
4. **Alcance** — Incluye / **No incluye**
5. **Flujo deseado** de punta a punta, con los ejemplos concretos del cliente
6. **Prototipo** (si lo hay): las pantallas clave de la maqueta validada, con pie de foto
7. **Reglas de negocio** (plazos, montos, aprobaciones, excepciones)
8. **Dependencias y restricciones** (sistemas, areas, datos, normativa, fecha objetivo y motivo)
9. **Criterios de exito** (como se sabra que quedo bien; base de los criterios de aceptacion)
10. **Pendientes**

### CTZ (cotizacion)
Todo lo de PRY, y ademas: **Entregables**, **Supuestos**, **Exclusiones**, **Plazo esperado**,
**Quien decide y que necesita**, **Condiciones**. La CTZ genera SIEMPRE la Propuesta (abajo).

### Anexo (todos, separado)
Fuentes recibidas (lista con fechas), rondas de preguntas y respuestas (resumen), decisiones
tomadas y por quien, y referencias del tracker cuando exista el ticket. Es el unico lugar con
trazabilidad "interna"; sigue sin codigo.

## La Propuesta (documento para el cliente)
Obligatoria en CTZ; opcional en PRY cuando el cliente la pida o el lead lo decida. Es un
documento DISTINTO del requerimiento: va dirigido al cliente, con tono comercial-profesional.
1. **Portada**: "Propuesta — {titulo}", cliente, fecha, version, vigencia.
2. **Contexto y objetivo** (lo que entendimos de su necesidad, en sus palabras)
3. **Alcance** — Incluye / No incluye
4. **Solucion propuesta** en negocio (como quedara el proceso para ellos), con las pantallas
   del prototipo si lo hay
5. **Entregables**
6. **Supuestos** (si cambian, cambia la propuesta)
7. **Exclusiones**
8. **Plan y plazos** (etapas, hitos; estimados)
9. **Valorizacion** — espacio que completa comercial/lider de mesa (la Mesa NO inventa precios
   ni esfuerzos; si hace falta estimacion, se pide al equipo de desarrollo)
10. **Condiciones** (vigencia, forma de trabajo, aprobacion)
11. **Proximos pasos** (que necesita el cliente hacer para aprobar)

## Prototipo dentro del documento
Cuando existe maqueta (`.mesa/solicitudes/{ID}/prototipo/`), el redactor incrusta las
capturas clave (`captura-01-*.png`…) en la seccion "Prototipo" / "Solucion propuesta" con pie
de foto que diga que muestra cada pantalla. Son bocetos: se aclara en el documento que
ilustran la idea, no el diseño final.

## Generacion (PDF + DOCX)
Fuente de verdad: la plantilla HTML (`templates/documento/documento-mesa.html` y
`templates/documento/propuesta.html`, o las del proyecto si `config.json` → `documentos.plantillas`
las define). Se rellenan los `{{PLACEHOLDERS}}`, se eliminan las secciones de otros tipos, y:
```bash
soffice --headless --convert-to pdf  --outdir "{salida}" documento.html
soffice --headless --convert-to docx --outdir "{salida}" documento.html
```
Verificar que ambos abren, que los acentos y eñes estan intactos y que las imagenes se ven.
Si falta tooling: `/mesa-servicios:setup`.

Nombres de archivo (en `.mesa/solicitudes/{ID}/documento/`):
- `{ID} - {Titulo corto} - v{N}.pdf` / `.docx`
- `{ID} - Propuesta - {Cliente} - v{N}.pdf` / `.docx`

## Versionado del documento
`v1` al cerrar. Si el cliente pide cambios o una ronda nueva altera el alcance → `v2`, con
una linea de "Cambios respecto a v1" en el anexo. Nunca se sobreescribe una version entregada.

## Reglas duras
- Lenguaje de negocio; cero codigo y cero jerga. Test de lectura antes de exportar.
- Nada inventado: todo sale de la solicitud cerrada; lo abierto va a "Pendientes".
- Correlativo unico y no reutilizable; alcance (cliente/transversal) siempre explicito.
- La valorizacion la pone comercial, no la Mesa.
- Secretos y datos personales de personas: jamas en el documento ni en la propuesta.
