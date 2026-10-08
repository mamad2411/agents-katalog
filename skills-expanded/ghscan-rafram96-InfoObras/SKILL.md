Sí, perfectamente. La idea es convertirlo de un prompt de análisis de reunión específico a una **skill reutilizable** que cualquier agente pueda invocar para levantar requerimientos de cualquier proyecto de software.

---

```markdown
# SKILL: requirements_extraction

## Descripción
Extrae requerimientos de software a partir de cualquier fuente de entrada 
(transcripción de reunión, notas, audio transcrito, documento de proceso, 
conversación de chat). Produce un documento estructurado listo para 
elaborar propuesta técnica y contrato de desarrollo.

## Cuándo invocar esta skill
- Hay una reunión con cliente grabada o transcrita
- El cliente describió su proceso actual (manual o semi-automatizado)
- Se necesita convertir una conversación informal en requerimientos formales
- Se quiere auditar qué tan completos están los requerimientos antes de cotizar

## Inputs aceptados
- Transcripción de reunión (texto plano o con timestamps)
- Notas de reunión (estructuradas o en prosa)
- Audio transcrito automáticamente (puede tener errores de STT)
- Documento que describe un proceso actual
- Hilo de conversación con el cliente (WhatsApp, correo, chat)
- Combinación de varios de los anteriores

## Parámetros opcionales
- `dominio`: industria o sector del cliente (ej: licitaciones, salud, logística)
  Si se provee, el agente usa vocabulario y ejemplos del dominio para 
  interpretar ambigüedades.
- `profundidad`: "rápido" | "completo" | "técnico"
  - rápido: solo RF, RNF y pendientes (útil para primera reunión corta)
  - completo: todas las partes (default)
  - técnico: énfasis en arquitectura, integraciones y reglas de negocio
- `output_format`: "markdown" | "json" | "ambos" (default: markdown)

---

## INSTRUCCIONES AL AGENTE

Eres un analista de software senior. Tu trabajo es leer el material 
proporcionado y producir un documento de requerimientos exhaustivo.

### Reglas generales
- Cita textualmente al cliente/fuente cuando sea relevante (entre comillas)
- Si algo no fue mencionado: escribe `[NO MENCIONADO]`
- Si algo fue ambiguo: `[AMBIGUO: descripción del problema]`
- Si algo requiere confirmación: `[CONFIRMAR: pregunta específica y directa]`
- Si algo se puede inferir pero no fue dicho: `[INFERIDO: razonamiento]`
- Al final de CADA sección: lista de preguntas de seguimiento pendientes
- Nunca inventes datos. Si no está en la fuente, márcalo explícitamente.

---

## PARTE 1 — CONTEXTO DE NEGOCIO

Extrae:
- Quién es el cliente: empresa, área, rol de quien habla
- Qué problema tiene hoy (en sus propias palabras si es posible)
- Qué hace manualmente y cuánto tiempo le toma por unidad de trabajo
- Cuántos usuarios usarán el sistema y si trabaja solo o en equipo
- Urgencia y plazos (explícitos o implícitos)
- Presupuesto mencionado (aunque sea de forma indirecta)
- Volumen de trabajo: frecuencia, tamaño de documentos, cantidad de casos

---

## PARTE 2 — REQUERIMIENTOS FUNCIONALES

Para cada funcionalidad mencionada, produce una ficha:

```
RF-XX: [Nombre corto]
─────────────────────────────────────────
Descripción : qué debe hacer el sistema
Input       : qué recibe (archivos, datos, eventos)
Output      : qué produce (formato, destino)
Reglas      : condiciones, validaciones, casos especiales
Ejemplos    : casos concretos mencionados por el cliente
Prioridad   : [ALTA / MEDIA / BAJA / NO DEFINIDA]
Estado      : [CONFIRMADO / SUGERIDO / MENCIONADO DE PASADA]
```

Agrupa las fichas en módulos lógicos según el dominio.
Si el cliente no mencionó un módulo pero es obvio que lo necesita, 
inclúyelo marcado como `[INFERIDO]`.

---

## PARTE 3 — REQUERIMIENTOS NO FUNCIONALES

Para cada dimensión, extrae lo que se dijo y lo que se puede inferir:

- **Rendimiento**: tiempos esperados, volumen de procesamiento simultáneo
- **Disponibilidad**: horarios, tolerancia a caídas, SLA mencionado
- **Privacidad y seguridad**: restricciones de datos, usuarios, permisos
- **Infraestructura**: on-premise, nube, híbrido, hardware mencionado
- **Usabilidad**: tipo de interfaz, dispositivos, usuarios técnicos vs. no técnicos
- **Integraciones**: sistemas externos, APIs, formatos de exportación
- **Escalabilidad**: crecimiento esperado, picos de uso

---

## PARTE 4 — REGLAS DE NEGOCIO

Lista cada regla como:

```
RN-XX: [Nombre]
─────────────────────────────────────────
Condición  : SI [condición] → ENTONCES [acción]
Ejemplo    : caso concreto del cliente
Impacto    : qué pasa si no se implementa correctamente
Alerta     : tipo si genera notificación [BLOQUEANTE / ADVERTENCIA / INFO]
Fuente     : cita o referencia en la transcripción
```

---

## PARTE 5 — FLUJO DE TRABAJO ACTUAL

Reconstruye el proceso AS-IS (cómo lo hace hoy):
1. Paso numerado con: qué hace, qué archivo usa, qué produce, cuánto tarda
2. Identifica claramente los cuellos de botella
3. Identifica los pasos que serán automatizados vs. los que quedarán manuales

Luego reconstruye el flujo TO-BE (cómo debería funcionar con el sistema):
1. Mismo formato
2. Señala en cada paso qué componente del sistema lo resuelve

---

## PARTE 6 — INFRAESTRUCTURA Y DEPLOYMENT

Extrae:
- Tipo de deployment preferido (local, nube, híbrido)
- Características de hardware mencionadas o inferidas
- Stack tecnológico mencionado por el cliente o sugerido en la reunión
- Restricciones: sistemas operativos, licencias, dependencias externas
- Requerimientos de red (intranet, VPN, acceso externo)
- Consideraciones de backup y recuperación

---

## PARTE 7 — ACUERDOS Y PENDIENTES

Produce dos listas:

**Compromisos del cliente**
- [ ] Tarea — responsable — fecha mencionada o [SIN FECHA]

**Compromisos del desarrollador / agente**
- [ ] Tarea — responsable — fecha mencionada o [SIN FECHA]

**Temas abiertos que necesitan resolverse antes de cotizar**
- Lista de preguntas críticas sin respuesta

---

## PARTE 8 — ANÁLISIS DE RIESGOS Y SEÑALES IMPLÍCITAS

Produce fichas de riesgo:

```
RIESGO-XX: [Nombre]
─────────────────────────────────────────
Descripción : qué podría salir mal
Probabilidad: [ALTA / MEDIA / BAJA]
Impacto     : [ALTO / MEDIO / BAJO]
Señal       : qué dijo o no dijo el cliente que sugiere este riesgo
Mitigación  : qué se puede hacer para reducirlo
```

También incluye:
- Funcionalidades que el cliente necesitará pero no mencionó
- Malentendidos potenciales detectados en la conversación
- Scope creep: funcionalidades que podrían inflarse durante el proyecto

---

## PARTE 9 — GLOSARIO

Para cada término técnico, sigla o concepto del dominio:

```
TÉRMINO: definición en el contexto de este proyecto
```

---

## PARTE 10 — RESUMEN EJECUTIVO

Al final, produce un bloque de máximo 200 palabras con:
- Qué quiere el cliente en una oración
- Los 3 módulos más críticos
- El riesgo técnico más importante
- La pregunta más urgente que hay que resolver antes de avanzar
- Una estimación de complejidad: [BAJA / MEDIA / ALTA / MUY ALTA] con justificación

---

## OUTPUT EN JSON (si output_format incluye json)

Además del markdown, produce un JSON con esta estructura mínima:

{
  "proyecto": {
    "cliente": "",
    "dominio": "",
    "complejidad_estimada": "",
    "urgencia": ""
  },
  "requerimientos_funcionales": [
    {
      "id": "RF-01",
      "nombre": "",
      "prioridad": "",
      "estado": "",
      "modulo": ""
    }
  ],
  "reglas_de_negocio": [
    {
      "id": "RN-01",
      "nombre": "",
      "condicion": "",
      "tipo_alerta": ""
    }
  ],
  "pendientes": {
    "cliente": [],
    "desarrollador": [],
    "sin_resolver": []
  },
  "riesgos": [
    {
      "id": "RIESGO-01",
      "nombre": "",
      "probabilidad": "",
      "impacto": ""
    }
  ]
}
```

---

## Notas de implementación para el agente

- Si la transcripción tiene errores de STT (palabras sin sentido, nombres 
  mal transcritos), intenta inferir el significado por contexto y márcalo 
  con `[STT-ERROR: interpretación usada]`
- Si hay múltiples speakers, distingue entre cliente y desarrollador para 
  atribuir correctamente las afirmaciones
- Si se proveen múltiples documentos, cruza la información entre ellos 
  y señala contradicciones
- Esta skill puede invocarse en iteraciones: primero con "rápido" para 
  una primera reunión, luego con "completo" cuando haya más contexto
```

---

La diferencia clave con el prompt original es que ahora el agente sabe **cuándo invocarla**, **qué parámetros ajustar según el contexto**, maneja **múltiples tipos de input** (no solo transcripciones), tiene un **output JSON** para que otro agente lo consuma, y está escrita para ser **reutilizable en cualquier dominio**, no solo licitaciones peruanas.