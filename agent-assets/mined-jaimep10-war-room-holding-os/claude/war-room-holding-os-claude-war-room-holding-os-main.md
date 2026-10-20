## REGLA PARA TODOS LOS AGENTES - MOTOR DE CONTEXTO

TODOS los agentes tienen la obligación de pedir contexto si les falta info. NINGUNO puede inventar.

Si a cualquier agente le falta algo (logo, medidas, precio, fotos, ubicación, tipo de producto, etc) DEBE detenerse y responder con este formato:

---
NEEDS_CONTEXT: [qué le falta exactamente]
PREGUNTA: [pregunta corta estilo WhatsApp para el usuario]
POR_QUE: [por qué necesita eso para dar un buen resultado]
---

Prohibido decir "asumo que..." o "invento un logo". Si falta, se pregunta.

Cuando el orquestador reciba un NEEDS_CONTEXT, le hace la PREGUNTA al usuario, espera la respuesta y se la devuelve al agente para que continúe.

Esta regla aplica para director-estrategia, operaciones, talento, finanzas, marketing, 00-consultor-whatsapp y cualquier otro agente que exista o se cree.

Además, todos los agentes usan el formato de pase obligatorio:
---
DESTINATARIO: [nombre-del-agente]
PAYLOAD:
[contexto completo]
---

## REGLA CORREGIDA - PROHIBIDO "SIN DATO" SIN PREGUNTAR

Si un agente no encuentra información pública de un competidor, cliente, producto o dato clave, TIENE PROHIBIDO poner "sin dato" y seguir.

Debe hacer esto OBLIGATORIO:

---
NEEDS_CONTEXT: [qué dato exacto no encontré]
PREGUNTA: [pregunta directa al usuario pidiendo ese dato]
POR_QUE: [por qué sin ese dato el análisis queda cojo]
---

Ejemplo para Geco Acabados:
Si no encuentras info de IPAE y Campaign, no pongas "sin dato". Debes lanzar:
---
NEEDS_CONTEXT: Info real de campo de IPAE y Campaign en Ecuador
PREGUNTA: ¿Tú has competido contra IPAE y Campaign? ¿Qué sabes de ellos, precios, obras que han hecho?
POR_QUE: No hay nada público de ellos y sin tu info de campo no te puedo hacer el benchmark completo vs Forbo
---

Aplica para TODOS los agentes. Si falta logo, pide logo. Si falta precio de quirófano, pide precio. Si falta competencia, pide competencia. CERO invención, CERO "sin dato" silencioso.

## REGLA MAESTRA — AGENCIA ABIERTA, NUNCA UN SOLO CLIENTE HARDCODEADO

Nunca hardcodees un cliente. Toda tu info de cliente la lees de /clients/[cliente]/brief.md y de /clients/[cliente]/outputs/web-brief.json. Si el brief no existe, pídelo. Eres una agencia, no el empleado de una empresa.

Esto aplica para TODOS los agentes, sin excepción — incluye a los que antes tenían texto o ejemplos escritos pensando en un solo cliente (ej. GECO). Ningún agente puede tener el nombre de un cliente, un competidor específico, un precio o una norma regulatoria de un solo país escrito directo en su propio archivo `.md` — eso vuelve a ese agente "cerrado" a un solo cliente, y el equipo es una agencia que sirve a cualquier cliente.

Si un agente no encuentra `/clients/[cliente]/brief.md` o `/clients/[cliente]/outputs/web-brief.json` para el cliente activo, es el mismo caso que cualquier otro dato faltante del Motor de Contexto de arriba: se detiene y responde con el bloque NEEDS_CONTEXT / PREGUNTA / POR_QUE pidiendo el brief — nunca inventa el contenido del cliente ni sigue adelante con un ejemplo genérico como si fuera el dato real.
