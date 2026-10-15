---
name: productivity-refactor
description: Refactors automatizados y seguros en cualquier lenguaje. Soporta renombrar símbolos en todo el proyecto, extraer funciones/métodos, mover archivos entre módulos actualizando imports, y eliminar código muerto. AST-aware para TypeScript (tsgo/ts-morph), Python (libcst/ast), y C# (Roslyn/dotnet-format). Úsala durante code review cuando un hallazgo requiera refactor, o cuando el usuario diga "renombra X a Y", "extrae esta función", "mueve este archivo", "elimina código muerto".
requires-devkits: auto-detect
---

# Productivity Refactor — Refactors Seguros

Ejecuta refactors automatizados con AST (Abstract Syntax Tree), no regex crudo. Sin miedo a romper el proyecto.

---

## Principio

> **Regex renombra strings. AST renombra símbolos.** Si renombras `user` con regex, rompes `username`, `user_id`, `getUser`, y el comentario "// user login". Con AST, solo tocas la definición y sus referencias exactas.

---

## Operaciones soportadas

### 1. Renombrar símbolo

```
Usuario: "renombra getUserOrders a getOrdersByCustomer"
```

**Proceso:**
1. Buscar definición del símbolo en todo el proyecto
2. Verificar que no exista ya otro símbolo con el nombre destino
3. Renombrar definición + todas las referencias (llamadas, imports, type annotations)
4. Si el símbolo se exporta y es parte de la API pública, advertir: "⚠️ Este símbolo se exporta desde `index.ts`. Esto es breaking change para consumidores externos."

```typescript
// ❌ Antes (service.ts + 14 archivos lo importan)
export async function getUserOrders(userId: string) {
  return db.orders.findMany({ where: { userId } });
}

// ✅ Después (service.ts + 14 archivos actualizados)
export async function getOrdersByCustomer(customerId: string) {
  return db.orders.findMany({ where: { customerId } });
}
```

### 2. Extraer función / método

```
Usuario: "extrae las líneas 42-55 de orders.service.ts a una función validateOrder"
```

**Proceso:**
1. Leer el bloque de código seleccionado
2. Identificar variables de entrada (parámetros) y salida (return)
3. Verificar que el bloque no dependa de variables locales que no se pasan como parámetro
4. Crear la función extraída con los parámetros necesarios
5. Reemplazar el bloque original con la llamada a la nueva función
6. Colocar la función en la ubicación adecuada:
   - Mismo archivo si es helper interno
   - `shared/utils/` si se usa en múltiples módulos
   - `shared/validation/` si es lógica de validación

```typescript
// ❌ Antes
async function createOrder(input: CreateOrderInput) {
  // Líneas 42-55: validación duplicada
  if (!input.customerId) throw new Error('Customer ID required');
  if (input.amount <= 0) throw new Error('Amount must be positive');
  if (input.amount > MAX_AMOUNT) throw new Error(`Max amount is ${MAX_AMOUNT}`);
  if (!VALID_CURRENCIES.includes(input.currency)) throw new Error('Invalid currency');
  // ... resto del código
}

// ✅ Después
async function createOrder(input: CreateOrderInput) {
  validateOrderInput(input);
  // ... resto del código
}

// Nueva función (al final del archivo o en shared/validation/)
function validateOrderInput(input: CreateOrderInput): void {
  if (!input.customerId) throw new Error('Customer ID required');
  if (input.amount <= 0) throw new Error('Amount must be positive');
  if (input.amount > MAX_AMOUNT) throw new Error(`Max amount is ${MAX_AMOUNT}`);
  if (!VALID_CURRENCIES.includes(input.currency)) throw new Error('Invalid currency');
}
```

### 3. Mover archivo entre módulos

```
Usuario: "mueve src/utils/formatCurrency.ts a src/shared/formatting/currency.ts"
```

**Proceso:**
1. Mover el archivo a la nueva ubicación
2. Encontrar todos los imports que referencian el archivo viejo
3. Actualizar las rutas de import
4. Si hay `index.ts` que re-exportaba el archivo, actualizarlo
5. Si hay `tsconfig.json` con `paths`, verificar que sigan funcionando

```typescript
// ❌ Antes (14 archivos)
import { formatCurrency } from '../../utils/formatCurrency';

// ✅ Después (14 archivos actualizados)
import { formatCurrency } from '../../shared/formatting/currency';
```

### 4. Eliminar código muerto

```
Usuario: "elimina código muerto en src/"
```

**Proceso:**
1. Buscar funciones/clases/variables exportadas que no se importan en ningún otro archivo
2. Listar hallazgos y preguntar antes de eliminar
3. Si el usuario confirma, eliminar definiciones

```typescript
// ❌ Encontrado en shared/helpers.ts
export function deprecatedHelper(x: number): number {
  return x * 1.16; // Nadie la usa desde 2024
}

// ✅ Eliminada después de confirmación del usuario
```

---

## AST engines por lenguaje

| Lenguaje | Herramienta | Disponibilidad |
|----------|------------|----------------|
| **TypeScript** | `tsgo --findAllReferences` + `tsgo --rename` | TypeScript 7 built-in |
| **Python** | `libcst` (si instalado) o `ast` (stdlib) | `uv add libcst` o stdlib |
| **C#** | `dotnet-format` + Roslyn | .NET SDK built-in |
| **JavaScript** | `tsgo` (si tiene jsconfig) o regex con verificación | — |

Si la herramienta AST no está disponible, usar regex con verificación manual y pedir confirmación.

---

## Workflow

### Paso 1: Entender la intención

```
Usuario: "renombra getuserOrders a getOrdersByCustomer en todo el proyecto"
```

Parsear: operación = `rename`, símbolo = `getUserOrders`, destino = `getOrdersByCustomer`.

### Paso 2: Analizar impacto

Antes de tocar nada, mostrar:

```
🔍 Buscando referencias de `getUserOrders`...

Encontradas:
- Definición: src/modules/orders/orders.service.ts:23
- Referencias: 14 archivos (8 llamadas, 5 imports, 1 type annotation)
- Exportado en: src/modules/orders/index.ts

⚠️ Este símbolo es parte de la API pública del módulo.
¿Proceder con el renombre?
```

### Paso 3: Ejecutar refactor

Aplicar el cambio y mostrar diff resumido antes de guardar:

```diff
📝 Cambios a aplicar:

-  src/modules/orders/orders.service.ts:23
   -export async function getUserOrders(userId: string) {
   +export async function getOrdersByCustomer(userId: string) {

-  src/modules/orders/index.ts:5
   -export { getUserOrders } from './orders.service';
   +export { getOrdersByCustomer } from './orders.service';

... y 13 archivos más.

¿Aplicar cambios?
```

### Paso 4: Verificar post-refactor

Después de aplicar, ejecutar (si están disponibles):

```bash
npm run typecheck    # Verificar que no hay errores de tipo
npm run lint         # Verificar que no hay imports rotos
npm test             # Verificar que los tests pasan
```

Si algo falla, mostrar qué falló y ofrecer revertir.

### Paso 5: Reportar

```
✅ `getUserOrders` → `getOrdersByCustomer` en 15 archivos.
✅ TypeCheck: OK | Lint: OK | Tests: 42 passed

Cambios aplicados. ¿Quieres commitear con mensaje:
"refactor(orders): rename getUserOrders → getOrdersByCustomer"?
```

---

## Modo batch (desde CODE_REVIEW.md)

Si el usuario dice "aplica todos los refactors del reporte":

1. Leer `CODE_REVIEW.md`, buscar issues de tipo Mejoras que sugieran renombrar/extraer/mover
2. Priorizar: primero renombres (más seguros), luego extracciones, luego movimientos
3. Ejecutar uno por uno, verificando entre cada uno
4. Mostrar progreso: `[████░░░░] 3 de 7 refactors aplicados`

---

## Lo que NO debe hacer

- No refactorizar sin mostrar el diff planificado.
- No renombrar símbolos de dependencias externas (node_modules, paquetes NuGet).
- No eliminar código exportado sin verificar que no sea parte de API pública.
- No modificar tests sin preguntar (a veces el test prueba el nombre viejo a propósito).
- No ejecutar refactors en archivos con cambios sin commitear (stash sugerido).
