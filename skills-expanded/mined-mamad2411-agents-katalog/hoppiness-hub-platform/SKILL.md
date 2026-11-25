# ============================================================================
# .cursorrules — Reglas de Arquitectura Universal
# ============================================================================
# INSTRUCCIONES DE USO:
# 1. Copiá este archivo a la raíz de tu proyecto como ".cursorrules"
# 2. Completá la sección PROYECTO debajo con los datos de tu app
# 3. Cursor lo lee automáticamente en cada interacción
# 4. Cuando Cursor haga algo que no te guste, agregá una regla nueva
# ============================================================================


# ════════════════════════════════════════════════════════════════════════════
# SECCIÓN 1 — CONFIGURACIÓN DEL PROYECTO (EDITAR PARA CADA PROYECTO)
# ════════════════════════════════════════════════════════════════════════════

## Stack del proyecto
# Ejemplo: React, TypeScript, Supabase, Tailwind CSS, Vite
# Ejemplo: Next.js, TypeScript, Prisma, PostgreSQL, Tailwind CSS
# Ejemplo: Vue 3, TypeScript, Firebase, Pinia
Stack: [COMPLETAR]

## Estructura de carpetas
# Definí dónde va cada cosa en TU proyecto. Ejemplo:
#
# src/
#   services/     → Toda interacción con base de datos y APIs externas
#   hooks/        → Lógica de estado y efectos (React) o composables (Vue)
#   components/   → Componentes de UI puros
#   pages/        → Páginas/rutas
#   types/        → Tipos e interfaces compartidas
#   utils/        → Funciones puras reutilizables
#   lib/          → Configuración de clientes externos (DB, auth, storage)
#   constants/    → Valores constantes y configuración
#
Estructura: [COMPLETAR O DEJAR EL EJEMPLO DE ARRIBA]

## Cliente de base de datos
# El archivo que instancia la conexión a la DB.
# Ejemplo: src/lib/supabaseClient.ts
# Ejemplo: src/lib/prisma.ts
# Ejemplo: src/lib/firebase.ts
Cliente DB: [COMPLETAR]

## Idioma del código
# En qué idioma se nombran variables, funciones, componentes.
# Ejemplo: Inglés para código, Español para comentarios y UI
Idioma: [COMPLETAR]


# ════════════════════════════════════════════════════════════════════════════
# SECCIÓN 2 — JERARQUÍA DE CAPAS (NO MODIFICAR)
# ════════════════════════════════════════════════════════════════════════════
# Esta es la columna vertebral de la arquitectura. La dirección de las
# dependencias SIEMPRE es de arriba hacia abajo. Nunca al revés.
#
#   pages/routes  →  components  →  hooks  →  services  →  lib (DB client)
#        ↓              ↓             ↓           ↓
#      types          types         types       types
#        ↓              ↓             ↓           ↓
#      utils          utils         utils       utils
#
# REGLAS:
# - Pages importan components y hooks. NUNCA services directamente.
# - Components importan hooks y otros components. NUNCA services ni DB.
# - Hooks importan services. NUNCA el cliente de DB directamente.
# - Services importan el cliente de DB. NUNCA importan hooks ni components.
# - Types y utils pueden ser importados por cualquier capa.
# - NINGÚN archivo importa hacia ARRIBA en la jerarquía.
#   (Un hook NUNCA importa de un component. Un service NUNCA importa de un hook.)


# ════════════════════════════════════════════════════════════════════════════
# SECCIÓN 3 — REGLAS DE CÓDIGO OBLIGATORIAS (NO MODIFICAR)
# ════════════════════════════════════════════════════════════════════════════

## 3.1 — Acceso a datos
- El cliente de base de datos se importa ÚNICAMENTE en /services o /lib.
- NINGÚN archivo de pages/, components/, o hooks/ puede importar el cliente de DB.
- Cada tabla/entidad tiene su propio archivo de service: [entidad]Service.ts
- Las funciones de service son async, tipadas, y con nombres descriptivos.
- Si necesitás datos en un componente, creá o usá un hook que consuma el service.

## 3.2 — Componentes de UI
- Un componente hace UNA cosa: renderizar UI basada en props/estado.
- Si un componente necesita datos, los recibe por props o usa un hook. NUNCA fetch directo.
- Si un componente supera 200 líneas, hay que partirlo.
- Si un componente tiene más de 5 useState, la lógica debe ir a un hook o reducer.
- Los event handlers complejos (más de 3 líneas) van en funciones separadas o hooks.
- NO poner lógica de negocio dentro de onClick, onChange, o onSubmit directamente.

## 3.3 — Hooks / Composables
- Cada hook tiene una sola responsabilidad.
- Los hooks consumen services para datos. NUNCA el cliente de DB.
- Un hook expone: datos, estado de carga, errores, y acciones.
- Si la misma lógica de estado se repite en 2+ componentes, extraerla a un hook.

## 3.4 — DRY (Don't Repeat Yourself)
- Antes de crear una función, BUSCÁ si ya existe algo similar en el codebase.
- Si un bloque de código aparece en 2 o más archivos, extraerlo a:
  - Un service (si toca datos)
  - Un hook (si maneja estado)
  - Un util (si es lógica pura sin estado ni datos)
  - Un componente compartido (si es UI)
- Queries a la DB que hacen lo mismo pero están en distintos archivos = VIOLACIÓN.
  Deben estar en un solo service.

## 3.5 — Tipos
- NO usar `any`. Si no sabés el tipo, usá `unknown` y hacé type narrowing.
- Las interfaces compartidas (usadas en 2+ archivos) van en /types.
- Los tipos de respuesta de la DB se definen una sola vez en /types.
- Los tipos específicos de un solo componente pueden estar en ese archivo.
- Preferir `interface` para objetos, `type` para uniones y utilidades.

## 3.6 — Nombrado
- Funciones y variables: camelCase (getOrderById, isLoading)
- Componentes y clases: PascalCase (OrderCard, CheckoutService)
- Constantes globales: UPPER_SNAKE_CASE (MAX_RETRY_COUNT, API_BASE_URL)
- Archivos de componentes: PascalCase.tsx (OrderCard.tsx)
- Archivos de hooks: camelCase con prefijo use (useOrders.ts)
- Archivos de services: camelCase con sufijo Service (orderService.ts)
- Archivos de tipos: camelCase (order.ts dentro de /types)
- Nombres descriptivos siempre. NO abreviar. `getUserBranchRoles` NO `getUBR`.
- Booleanos empiezan con is, has, can, should: isLoading, hasPermission, canEdit.

## 3.7 — Manejo de errores
- UN SOLO patrón en todo el proyecto: try/catch con early return.
- Cada service atrapa sus propios errores y devuelve un resultado tipado o lanza.
- Los hooks manejan el estado de error para la UI.
- Los componentes MUESTRAN errores, no los manejan.
- NUNCA silenciar errores con catch vacío. Siempre loguear o propagar.
- NUNCA mezclar try/catch con .then().catch() en el mismo proyecto.

## 3.8 — Constantes y configuración
- Valores que pueden cambiar (URLs, keys, límites, textos) van en constantes
  centralizadas o variables de entorno. NUNCA hardcodeados en componentes.
- Strings mágicos (tipos, estados, roles) van como constantes o enums.
- Si un número aparece en la lógica sin contexto, darle nombre:
  MAL:  if (items.length > 50)
  BIEN: if (items.length > MAX_CART_ITEMS)


# ════════════════════════════════════════════════════════════════════════════
# SECCIÓN 4 — PROHIBICIONES ABSOLUTAS (NO MODIFICAR)
# ════════════════════════════════════════════════════════════════════════════

NUNCA hagas ninguna de estas cosas:

- NUNCA importar el cliente de DB fuera de /services o /lib.
- NUNCA duplicar una query que ya existe en un service.
- NUNCA crear un componente de más de 300 líneas sin partirlo.
- NUNCA dejar imports sin usar.
- NUNCA dejar funciones exportadas que nadie importa.
- NUNCA dejar variables de estado que se setean pero no se leen.
- NUNCA usar `any` como tipo.
- NUNCA hardcodear valores que pueden cambiar.
- NUNCA poner lógica de negocio dentro de un handler de evento inline.
- NUNCA hacer fetch de datos dentro del cuerpo de renderizado de un componente.
- NUNCA importar hacia arriba en la jerarquía de capas (Sección 2).
- NUNCA crear un archivo sin una sola responsabilidad clara.
- NUNCA mezclar dos patrones distintos para la misma operación.
- NUNCA asumir. Si algo es ambiguo, PREGUNTÁ antes de generar código.
- NUNCA modificar el archivo .env ni las variables de entorno.

# ════════════════════════════════════════════════════════════════════════════
# SECCIÓN 5 — PROCESO ANTES DE GENERAR CÓDIGO (NO MODIFICAR)
# ════════════════════════════════════════════════════════════════════════════

Cada vez que vayas a crear o modificar código, seguí este checklist mental:

□ ¿Ya existe algo parecido en el codebase?
  → Si sí: reutilizá. No dupliques.

□ ¿Estoy poniendo acceso a datos en un componente o page?
  → Si sí: mové a un service y consumí desde un hook.

□ ¿Este archivo hace más de una cosa?
  → Si sí: partilo.

□ ¿Este componente va a tener más de 200 líneas?
  → Si sí: extraé sub-componentes o hooks.

□ ¿Estoy usando un valor hardcodeado?
  → Si sí: mové a constantes o env.

□ ¿El nombre que elegí explica qué hace sin leer el código?
  → Si no: renombrá.

□ ¿Estoy repitiendo un bloque que ya escribí en otro archivo?
  → Si sí: extraé a un módulo compartido.

□ ¿Estoy importando algo de una capa superior?
  → Si sí: reestructurá. La dependencia va al revés.


# ════════════════════════════════════════════════════════════════════════════
# SECCIÓN 6 — ESTILO DE RESPUESTA (NO MODIFICAR)
# ════════════════════════════════════════════════════════════════════════════

Cuando generes código:
- Explicá brevemente qué hiciste y por qué.
- Si creás un archivo nuevo, mencioná en qué carpeta va y qué responsabilidad tiene.
- Si modificás un archivo existente, mostrá qué cambió.
- Si detectás un antipatrón en el código existente mientras trabajás,
  mencionalo y proponé la corrección, pero no la hagas sin que te lo pidan.
- Preferí soluciones simples. No sobre-ingenierices.
- Si hay dos formas de resolver algo, elegí la más fácil de entender.
- El código debe poder ser leído por alguien que no lo escribió.


# ════════════════════════════════════════════════════════════════════════════
# SECCIÓN 7 — REGLAS PERSONALIZADAS (AGREGAR LAS TUYAS ACÁ)
# ════════════════════════════════════════════════════════════════════════════
# Cada vez que Cursor haga algo que no te guste, agregá una regla acá.
# Ejemplos:
# - No usar librería X, usar Y en su lugar.
# - Los formularios siempre usan react-hook-form, no estado manual.
# - Los modales se manejan con el sistema de modales en /hooks/useModal.
# - El idioma de las variables es inglés, los comentarios en español.
# - Siempre usar Tailwind, nunca CSS modules ni styled-components.

[TUS REGLAS PERSONALIZADAS ACÁ]
