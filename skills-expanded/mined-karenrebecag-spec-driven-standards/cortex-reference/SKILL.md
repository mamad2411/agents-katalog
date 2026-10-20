---
name: cortex-reference
description: >
  Referencia conceptual y funcional de Cortex (Atom): qué es cada panel, nodo,
  tipo de dato o feature, y cómo se usa desde la UI. Usar cuando alguien
  pregunte qué es Cortex, pida el significado de un término (nodo, etapa,
  tipificación, etiqueta, rama de condición, campo de guardado, etc.), quiera
  saber cómo se configura una función puntual de la plataforma (Configuración
  Global, base de conocimiento/RAG, tablas dinámicas, HTTP Request, Code Tool,
  MCP Servers, aplicaciones externas con OAuth, WhatsApp Flows, el simulador,
  evaluaciones, publicar vs guardar, integración con Flowbuilder), o pida
  buenas prácticas generales de diseño de flujos y prompts que no sean parte
  de una migración concreta. Para el proceso paso a paso de implementar o
  migrar un agente Cortex completo (análisis de un flow JSON existente,
  bugs conocidos de plataforma, checklist de conexión en Flowbuilder), usar
  en cambio el skill `cortex-implementation`.
---

# Referencia de Cortex

Manual de referencia funcional de Cortex, organizado en 10 secciones dentro de
`references/`. Consultar el archivo de la sección relevante en vez de intentar
responder de memoria: son 41 artículos y ~46.000 palabras en total, demasiado
para tener todo en contexto a la vez.

## Advertencia sobre el estado del contenido

**39 de los 41 artículos originales están marcados "Borrador" y solo 2 "En
revisión"** (ver metadata `Estado` al inicio de cada artículo dentro de los
archivos de `references/`). Nada de esto pasó una validación final del equipo
de producto al momento de generar este skill (agosto 2026). Tratar el
contenido como la mejor descripción disponible, no como verdad confirmada:

- Ante cualquier duda operativa importante (por ejemplo, algo que dispare una
  acción irreversible o afecte a un cliente en producción), señalar
  explícitamente que la fuente es un borrador y sugerir confirmar en el
  producto real o con el equipo de Cortex antes de actuar.
- Si el usuario reporta que el comportamiento real no coincide con lo
  descrito acá, confiar en lo que el usuario observa en la plataforma, no en
  este documento.

## Cómo está organizado el manual original

Sigue el recorrido de quien construye un flujo: entender el producto,
configurar lo global, armar el canvas, alimentarlo con datos y herramientas,
definir cómo responde, probarlo, publicarlo e integrarlo con Flowbuilder. La
sección 10 no documenta funcionalidad sino criterio de uso.

**Si es el primer contacto con Cortex, empezar por `references/01-fundamentos.md`**
(incluye el glosario de términos que usa el resto del manual).

## Índice de secciones

| Archivo | Sección | Cubre |
|---|---|---|
| `references/01-fundamentos.md` | 1. Fundamentos | Qué es Cortex y cuándo usarlo, glosario de términos, anatomía de un flujo |
| `references/02-configuracion-global.md` | 2. Configuración global | Panel de Configuración Global, etapas del funnel, tipificaciones y etiquetas, reconocimiento de cliente/memoria, módulo de seguridad |
| `references/03-construir-el-flujo.md` | 3. Construir el flujo | El canvas, el Nodo Cortex, nodos Fin, ramas de condición y enrutamiento multi-nodo, Prompt Wizard |
| `references/04-conocimiento-y-datos.md` | 4. Conocimiento y datos | Base de conocimiento (RAG), tablas dinámicas vs KB, campos de guardado |
| `references/05-herramientas-e-integraciones.md` | 5. Herramientas e integraciones | Aplicaciones externas por OAuth, HTTP Request y Code Tool, MCP Servers, variables de entorno |
| `references/06-mensajeria.md` | 6. Mensajería | Formatos de respuesta enriquecidos, WhatsApp Flows, multimedia y features de canal |
| `references/07-probar.md` | 7. Probar | El simulador, validaciones antes de publicar, guía de testing, evaluaciones (crear, ejecutar, leer resultados), personalidades de evaluación |
| `references/08-publicar-y-operar.md` | 8. Publicar y operar | Borrador vs publicado, exportar/importar configuración (JSON), publicar un flujo en uso |
| `references/09-integracion-con-flowbuilder.md` | 9. Integración con Flowbuilder | El Nodo Cortex en Flowbuilder, mapa completo de salidas, recupero por inactividad, campañas salientes |
| `references/10-buenas-practicas.md` | 10. Buenas prácticas | Diseñar el flujo antes de construir, escribir buenos prompts, condiciones de salida, evitar loops y spam, costos en WhatsApp |

Cada artículo dentro de estos archivos conserva su propio tag de estado
(`Borrador` / `En revisión`) justo debajo del título — revisarlo antes de citar
algo como si fuera definitivo.

## Relación con `cortex-implementation`

Este skill es **conceptual**: explica qué es cada pieza y cómo se usa en la
UI. `cortex-implementation` es **operativo**: guía el proceso completo de
migrar un flow existente o montar un agente Cortex desde cero, con checklist
de análisis previo, bugs de plataforma confirmados en producción y testing.
Si la tarea es "quiero migrar/implementar un agente para un cliente", usar
`cortex-implementation` como guía principal y este skill como apoyo cuando
haga falta entender un concepto puntual (por ejemplo, qué es exactamente una
"rama de finalización" o cómo funciona una tabla dinámica frente a una KB).

## Contenido no incluido

Tres artículos del manual original ("Aplicaciones externas con autenticación"
y "HTTP Request y Code Tool") tenían capturas de pantalla y videos
demostrativos (integración con Slack, HubSpot, HTTP Request) que no se
incluyeron acá — un skill no puede reproducir video, y las capturas quedaron
descritas en el texto circundante cuando aportaban información no redundante.
Si el detalle visual es necesario, señalar que existe en el manual original de
Notion y que conviene revisarlo ahí.
