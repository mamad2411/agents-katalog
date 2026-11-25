---
name: netsuite-clean-architecture
description: |-
  Guía y creador de proyectos NetSuite con TypeScript usando Clean Architecture.
  Usa cuando: usuario quiere crear proyecto NetSuite, clasificar tamaño (pequeño/mediano/grande),
  preguntar sobre arquitectura, o necesita estructura de código.

  Este skill te ayudará a:
  - Entender qué es Clean Architecture y por qué se usa en NetSuite
  - Clasificar tu proyecto con preguntas simples
  - Crear la estructura correcta según el tamaño
  - Clonar el repositorio template y configurarlo automáticamente

  Examples:
  - user: "quiero crear un proyecto netsuite" → hacer PREGUNTA 1 primero
  - user: "crear proyecto sales" → hacer preguntas de clasificación
  - user: "nuevo proyecto para facturacion" → hacer preguntas + crear estructura
---
compatibility: opencode
metadata:
  version: "1.6"
  author: Gateway Team
  license: MIT
---

# NetSuite Clean Architecture - Skill Guide

## 📦 Instalación en Claude Code

### Paso 1: Instalar el skill

```bash
claudeskill install gildder/netsuite-architecture-skill
```

### Paso 2: Crear estructura .claude/

Después de instalar, ejecutar el script de configuración:

```powershell
# Desde la raíz de tu proyecto
powershell -ExecutionPolicy Bypass -File .agents/skills/netsuite-clean-architecture/scripts/install-claude.ps1
```

O manualmente:

```bash
mkdir -p .claude/skills/netsuite-clean-architecture
mkdir -p .claude/agents/orkidns

cp .agents/skills/netsuite-clean-architecture/SKILL.md .claude/skills/netsuite-clean-architecture/
cp .agents/skills/netsuite-clean-architecture/AGENT.md .claude/agents/orkidns/ 2>/dev/null || \
cp .agents/skills/netsuite-clean-architecture/orkidns/AGENT.md .claude/agents/orkidns/
```

### Paso 3: Listo!

Reiniciá Claude Code y el skill estará disponible.

---

## ⚠️ IMPORTANTE: Flujo de Preguntas

**Este skill debe hacer las preguntas UNA A LA VEZ.**
- NO agrupe múltiples preguntas en un solo mensaje
- NO muestre la siguiente pregunta hasta que el usuario responda la actual
- Después de cada pregunta, espere la respuesta del usuario antes de continuar

---

## FASE 1: Preguntas Iniciales del Proyecto

### PREGUNTA 1/8: Ubicación del Proyecto

**Solo muestre esta pregunta. No muestre las demás.**

```
📍 PREGUNTA 1/8: ¿Dónde querés crear el proyecto?

Por favor, proporciona la ruta completa donde se creará la carpeta del proyecto.

Ejemplos de respuesta:
- "C:\Users\gguerrero\Documents\proyectos\mi-proyecto"
- "D:\NetSuite\proyectos\nuevo"
- "./nuevo-proyecto"
```

**ESPERE la respuesta del usuario. Luego continúe a la PREGUNTA 2.**

---

### PREGUNTA 2/8: Nombre del Proyecto

**Solo después de que el usuario responda la pregunta 1.**

```
📍 PREGUNTA 2/8: ¿Cuál es el nombre del proyecto?

Este nombre se usará para:
- Nombre de la carpeta del proyecto
- Nombre en package.json
- Parte del nombre de los archivos compilados

Ejemplos de respuesta:
- "facturacion"
- "tienda-online"
- "marketplace"
- "ventas-sucursales"
```

**ESPERE la respuesta del usuario. Luego continúe a la PREGUNTA 3.**

---

### PREGUNTA 3/8: Prefijo del Proyecto

**Solo después de que el usuario responda la pregunta 2.**

```
📍 PREGUNTA 3/8: ¿Cuál es el prefijo del proyecto?

El prefijo se usará para identificar tus scripts en NetSuite.
Aparecerá al inicio de todos los archivos de scripts.

Formato: [prefijo]_[tipo]_[nombre].ts

Ejemplos de respuesta:
- "gw" → gw_sl_facturas.ts, gw_rs_pedidos.ts
- "acme" → acme_sl_facturas.ts, acme_rs_pedidos.ts
- "tienda" → tienda_sl_carrito.ts

⚠️ IMPORTANTE: El prefijo debe ser:
- En minúsculas
- Sin guiones
- Sin espacios
- Solo letras y números
```

**ESPERE la respuesta del usuario. Luego continúe a la PREGUNTA 4.**

---

## FASE 2: Preguntas de Clasificación

### PREGUNTA 4/8: Cantidad de Scripts

**Solo después de que el usuario responda la pregunta 3.**

```
📋 PREGUNTA 4/8: ¿Cuántos scripts NetSuite tendrá tu proyecto?

[A] POCOS (1-5 scripts)
    → Ejemplo: un Restlet simple o Suitelet básico

[B] MEDIO (6-15 scripts)
    → Ejemplo: CRUD completo con validaciones

[C] MUCHOS (>15 scripts)
    → Ejemplo: múltiples integraciones, colas, procesos
```

**ESPERE la respuesta del usuario (A, B o C). Luego continúe a la PREGUNTA 5.**

---

### PREGUNTA 5/8: Dominios

**Solo después de que el usuario responda la pregunta 4.**

```
📋 PREGUNTA 5/8: ¿Cuántos dominios necesitas?

(Dominios = módulos de negocio diferentes)

[A] SOLO 1 DOMINIO
    → Ejemplo: solo Sales, o solo Customer

[B] 2 DOMINIOS
    → Ejemplo: Sales + Customer, Sales + Inventory

[C] 3+ DOMINIOS
    → Ejemplo: Sales + Inventory + Customer + Accounting
```

**ESPERE la respuesta del usuario (A, B o C). Luego continúe a la PREGUNTA 6.**

---

### PREGUNTA 6/8: Operaciones

**Solo después de que el usuario responda la pregunta 5.**

```
📋 PREGUNTA 6/8: ¿Qué operaciones necesitas?

[A] SOLO CREAR o LEER
    → Una operación simple (solo lectura o crear un registro)

[B] CRUD COMPLETO
    → Crear, Leer, Actualizar, Borrar

[C] CRUD + PROCESOS ASÍNCRONOS + INTEGRACIONES
    → Transacciones complejas, colas, APIs externas, procesos batch
```

**ESPERE la respuesta del usuario (A, B o C). Luego continúe a la PREGUNTA 7.**

---

### PREGUNTA 7/8: Integraciones

**Solo después de que el usuario responda la pregunta 6.**

```
📋 PREGUNTA 7/8: ¿Tienes integraciones externas?

[A] NINGUNA o MÁXIMO 1
    → Solo operaciones internas de NetSuite

[B] 2-3 INTEGRACIONES
    → Gateway, VTEX, APIs de pagos, servicios externos

[C] MÁS DE 3
    → Múltiples sistemas externos (ERP, CRM, logística, etc.)
```

**ESPERE la respuesta del usuario (A, B o C). Luego continúe al RESULTADO.**

---

### PREGUNTA 8/8: Líneas de Código

**Solo después de que el usuario responda la pregunta 7.**

```
📋 PREGUNTA 8/8: ¿Cuántas líneas de código estimás?

[A] POCAS (hasta 1500 líneas)
    → Proyecto pequeño, código simple

[B] MEDIAS (1501-4000 líneas)
    → Proyecto mediano, funcionalidad moderada

[C] MUCHAS (más de 4000 líneas)
    → Proyecto grande, sistema completo
```

**ESPERE la respuesta del usuario (A, B o C). Luego continúe al RESULTADO.**

---

## FASE 3: Resultado de Clasificación

**Solo después de que el usuario responda la pregunta 8.**

Analice las respuestas y muestre el resultado:

```
🎯 RESULTADO DE CLASIFICACIÓN

Basado en tus respuestas:
- Scripts: [A/B/C]
- Dominios: [A/B/C]
- Operaciones: [A/B/C]
- Integraciones: [A/B/C]
- Líneas de código: [A/B/C]

Tu proyecto es: [PEQUEÑO/MEDIANO/GRANDE]

---

Datos del proyecto:
- Ubicación: [ruta proporcionada en pregunta 1]
- Nombre: [nombre proporcionado en pregunta 2]
- Prefijo: [prefijo proporcionado en pregunta 3]

---

Ahora voy a:
1. Clonar el repositorio template directamente en [ruta] (archivos en la raíz, sin subcarpeta)
2. Eliminar archivos de ejemplo del template (TypeScripts y Objects)
3. Configurar package.json, tsconfig.json
4. Configurar deploy.xml (actualizar path de FileCabinet)
5. Configurar manifest.xml (actualizar nombre del proyecto)
6. Configurar biome.json (incluir JS compilados, agregar overrides)
7. Crear estructura TypeScripts según tu clasificación
8. Crear scripts NetSuite con prefijo [prefijo]_
```

---

## FASE 4: Pregunta Adicional (solo para MEDIANO)

**Solo si el resultado fue MEDIANO.**

```
📋 PREGUNTA EXTRA: Tu proyecto es MEDIANO.

¿Querés usar carpeta Modules?

[A] SÍ - Mi proyecto tendrá 3+ dominios o prevé crecer
[B] NO - Solo tendré 1-2 dominios y no pienso agregar más
```

**ESPERE la respuesta del usuario (A o B).**
**Luego proceda a crear el proyecto.**

---

## Estructuras por Tipo de Proyecto

### 🏠 PROYECTO PEQUEÑO

```
src/TypeScripts/[nombre]/
├── [Dominio]/
│   ├── [dominio].service.ts
│   ├── [dominio].repository.ts
│   └── [dominio].types.ts
├── Interface/
│   └── [prefijo]_sl_[nombre].ts
└── Shared/
    └── utils/
```

---

### 🏢 PROYECTO MEDIANO (sin Modules)

```
src/TypeScripts/[nombre]/
├── [Dominio]/
│   ├── Domain/entities/
│   ├── Application/services/, transforms/
│   ├── Infrastructure/repositories/
│   └── validations/
├── Interface/
│   ├── [prefijo]_rs_[nombre].ts
│   ├── [prefijo]_sl_[nombre].ts
│   └── [prefijo]_ue_[nombre].ts
└── Shared/
```

---

### 🏢 PROYECTO MEDIANO (con Modules)

```
src/TypeScripts/[nombre]/
├── Modules/
│   └── [Dominio]/
│       ├── Domain/entities/
│       ├── Application/services/, transforms/
│       ├── Infrastructure/repositories/
│       └── validations/
├── Interface/
│   ├── [prefijo]_rs_[nombre].ts
│   ├── [prefijo]_sl_[nombre].ts
│   └── [prefijo]_ue_[nombre].ts
└── Shared/
```

---

### 🏰 PROYECTO GRANDE

```
src/TypeScripts/[nombre]/
├── Modules/
│   └── [Dominio]/
│       ├── Domain/ (entities, value-objects, events, services)
│       ├── Application/ (use-cases, ports, dtos, services, transforms)
│       ├── Infrastructure/ (persistence, adapters)
│       └── validations/
├── Interface/
│   ├── [prefijo]_cs_[nombre].ts   ← Client Script
│   ├── [prefijo]_ue_[nombre].ts   ← User Event
│   ├── [prefijo]_sl_[nombre].ts   ← Suitelet
│   ├── [prefijo]_rl_[nombre].ts   ← RESTlet
│   ├── [prefijo]_pl_[nombre].ts   ← Portlet
│   ├── [prefijo]_sc_[nombre].ts   ← Scheduled
│   ├── [prefijo]_mr_[nombre].ts   ← Map/Reduce
│   ├── [prefijo]_gl_[nombre].ts   ← SuiteGL
│   ├── [prefijo]_wa_[nombre].ts   ← Workflow Action
│   ├── [prefijo]_mu_[nombre].ts   ← Mass Update
│   └── [prefijo]_bi_[nombre].ts   ← Bundle Installation
└── Shared/
    ├── domain/ (result.ts, guard.ts)
    ├── utils/
    └── constants/
```

---

## Nomenclatura de Scripts NetSuite

Formato: `[prefijo]_[tipo]_[nombre].ts`

| Tipo | Código | Ejemplo |
|------|--------|---------|
| Client Script | cs | gw_cs_validacion.ts |
| User Event | ue | gw_ue_factura.ts |
| Suitelet | sl | gw_sl_facturas.ts |
| RESTlet | rl | gw_rl_pedidos.ts |
| Portlet | pl | gw_pl_dashboard.ts |
| Scheduled | sc | gw_sc_sincronizacion.ts |
| Map/Reduce | mr | gw_mr_importacion.ts |
| SuiteGL | gl | gl_asiento_automatico.ts |
| Workflow Action | wa | wa_aprobacion_pedido.ts |
| Mass Update | mu | mu_actualizacion_masiva.ts |
| Bundle Installation | bi | bi_instalacion_bundle.ts |

---

## Configuración SDF

Al crear un proyecto, se configuran automáticamente los archivos de SDF:

### deploy.xml

```xml
<deploy>
    <configuration>
        <path>~/AccountConfiguration/*</path>
    </configuration>
    <files>
        <path>~/FileCabinet/SuiteScripts/[nombre-proyecto]/*</path>
    </files>
    <objects>
        <path>~/Objects/*</path>
    </objects>
    <translationimports>
        <path>~/Translations/*</path>
    </translationimports>
</deploy>
```

### manifest.xml

```xml
<manifest projecttype="ACCOUNTCUSTOMIZATION">
  <projectname>[NOMBRE_UPPER_CASE]_Project</projectname>
  <frameworkversion>1.0</frameworkversion>
  <dependencies>
    <features>
      <feature required="true">SERVERSIDESCRIPTING</feature>
    </features>
  </dependencies>
</manifest>
```

### Archivos que se actualizan:

| Archivo | Campo actualizado |
|---------|-----------------|
| deploy.xml | `FileCabinet/SuiteScripts/[nombre-proyecto]` |
| manifest.xml | `projectname` → `[NOMBRE_UPPER]_Project` |

---

## Reglas de Compilación TypeScript → NetSuite

### ⚠️ Problemas Comunes y Soluciones

#### Problema 1: esModuleInterop contamina el output AMD

**Síntoma:** Cada archivo .js compilado comienza con ~33 líneas de código helper:
```javascript
var __importStar = (this && this.__importStar) || ...
var __createBinding = (this && this.__createBinding) || ...
```

**Causa:** Tener `"esModuleInterop": true` combinado con `import * as x from 'N/x'`

**Solución:** Eliminar `"esModuleInterop": true` del tsconfig.json. En NetSuite siempre se usan namespace imports que son AMD-native.

---

#### Problema 2: JSDoc @NApiVersion desaparece en la compilación

**Síntoma:** El header JSDoc requerido por NetSuite no aparece en el .js compilado.

**Causa:** tsc en modo AMD no preserva comentarios JSDoc a nivel de archivo.

**Solución:** Usar script post-build `scripts/prepend-headers.js` que inyecta el JSDoc después de compilar.

---

#### Problema 3: Biome no encuentra archivos en Windows

**Síntoma:** Biome reporta "0 files linted"

**Causa:** El patrón `["**/*.{ts,json}"]` no funciona en Biome 1.9.4 en Windows.

**Solución:** Separar en dos patrones:
```json
"include": ["**/*.ts", "**/*.json"]
```

---

#### Problema 4: Formatear JS compilados

**Síntoma:** El JavaScript compilado por tsc es compacto y difícil de leer.

**Solución:** Agregar Biome como paso de formateo al pipeline de build.

**biome.json - configuración completa:**
```json
{
  "files": {
    "include": ["**/*.ts", "**/*.json", "src/FileCabinet/SuiteScripts/[PROYECTO]/**/*.js"],
    "ignore": ["node_modules/**"]
  },
  "overrides": [
    {
      "include": ["src/FileCabinet/**"],
      "linter": { "enabled": false },
      "organizeImports": { "enabled": false }
    }
  ]
}
```

**Orden del build (obligatorio):**
1. `tsc` - compila TypeScript → JavaScript
2. `node scripts/prepend-headers.js` - inyecta JSDoc @NScriptType
3. `biome format` - formatea los JS compilados

**package.json:**
```json
"build": "tsc && node scripts/prepend-headers.js && biome format --write src/FileCabinet/SuiteScripts/mi-proyecto"
```

**Por qué usar overrides:** No queremos que Biome lint los archivos compilados (son output, no source), pero sí queremos que los formatee.

---

### tsconfig.json Recomendado

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "AMD",
    "moduleResolution": "Node",
    "lib": ["ESNext"],
    "strict": true,
    "skipLibCheck": true,
    "noEmitOnError": true,
    "experimentalDecorators": true
    // NO esModuleInterop — nunca en proyectos NetSuite AMD
  }
}
```

### Build Script

El proyecto debe usar:
```json
"build": "tsc && node scripts/prepend-headers.js"
```

El script `prepend-headers.js` recorrerá los archivos de Interface/ y injectará el JSDoc del .ts original al .js compilado.

---

### Reglas del Código

| Regla | Descripción |
|-------|-------------|
| **module: amd** | NetSuite usa AMD (define/require) |
| **target: ES2020** | SuiteScript 2.1 soporta ES2023 |
| **Sin esModuleInterop** | NUNCA usar en proyectos NetSuite AMD |
| **JSDoc obligatorio** | Incluir `@NApiVersion 2.1` en cada archivo |
| **Entry Points** | Exportar: `pageInit`, `onRequest`, `beforeSubmit`, etc. |
| **NModuleScope** | Usar: `Public`, `SameAccount`, o `Prerequisite` |

### Estructura de Archivo TypeScript

```typescript
/**
 * @NApiVersion 2.1
 * @NModuleScope Public
 * @NScriptType Suitelet
 */

import record from 'N/record';
import { EntryPoints } from 'N/types';

export let onRequest: EntryPoints.Suitelet.onRequest = (context) => {
  const rec = record.create({ type: record.Type.INVOICE });
  context.response.write('Hola');
};
```

### Transpilación

TypeScript convierte esto a:

```javascript
define(['N/record', 'N/types'], function(record, types) {
  var onRequest = function(context) {
    var rec = record.create({ type: record.Type.INVOICE });
    context.response.write('Hola');
  };
  return { onRequest: onRequest };
});
```

### Dependencias Requeridas

```json
{
  "devDependencies": {
    "@hitc/netsuite-types": "^2025.1.0",
    "typescript": "^5.4.0"
  }
}
```

---

## Referencias

- Template: https://github.com/gildder/netsuite-ts-sdf-template
- Clean Architecture: https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html
- Hexagonal: https://alistair.cockburn.us/hexagonal-architecture

---

## OrkidNS - Agente de Arquitectura

Para crear y validar componentes siguiendo la arquitectura, usá el agente **OrkidNS**.

### Comandos disponibles

| Comando | Descripción |
|---------|-------------|
| `orkidns add "idea"` | Crear componentes desde una idea |
| `orkidns check` | Validar arquitectura del proyecto |
| `orkidns info [carpeta]` | Explicar qué va y qué NO va en esa carpeta |
| `orkidns list` | Listar componentes del proyecto |
| `orkidns init` | Inicializar OrkidNS en un proyecto |
| `orkidns fix` | Corregir problemas de arquitectura |
| `orkidns normalize` | Corregir TypeScript al formato NetSuite |
| `orkidns hint` | Dar sugerencias basadas en código existente |

### Ejemplo de uso

```
USER: orkidns add "quiero hacer un servicio para crear facturas"

ORKIDNS:
📋 Basándome en tu idea "crear facturas":

Componentes sugeridos:
✅ Entity: Domain/entities/invoice.entity.ts
✅ Service: Application/services/invoice.service.ts
✅ Repository: Infrastructure/persistence/invoice.repository.ts

¿Querés que los cree? (sí/no)
```

### Palabras clave para inferencia

| Keyword | → | Componentes |
|---------|---|-------------|
| "crear" / "nuevo" | | Entity + Service + Repository |
| "integrar" | | Adapter + Port |
| "sincronizar" | | UseCase + Scheduled |
| "validar" | | Validation |
| "transformar" | | Transform |
| "evento" | | DomainEvent |
| "CRUD" | | Entity + Service + Repository + Validation + Transform |
| "api" | | Port + Adapter |
| "programado" | | Scheduled |

### orkidns normalize

Corrige archivos TypeScript para que compilen correctamente a JavaScript de NetSuite.

**Ejemplo de uso:**

```
USER: orkidns normalize "src/TypeScripts/Sales/invoice.ts"

ORKIDNS:
📝 Corrigiendo: src/TypeScripts/Sales/invoice.ts

✅ Agregado JSDoc:
   - @NApiVersion 2.1
   - @NModuleScope Public
   - @NScriptType Suitelet

✅ Corregido export:
   - Cambiado a formato NetSuite EntryPoints

✅ Corregido imports:
   - Agregado "N/types" para EntryPoints
```

**Correcciones automáticas:**

| Problema | Corrección |
|----------|------------|
| Falta JSDoc | Agrega `@NApiVersion 2.1`, `@NModuleScope Public` |
| Falta @NScriptType | Auto-detecta según nombre de función |
| Export incorrecto | Convierte al formato de NetSuite |
| Falta EntryPoints | Agrega `import { EntryPoints } from 'N/types'` |
| record.Type string | Cambia a `record.Type.INVOICE` (enum) |

**Detección automática de tipo de script:**

| Función detectada | → | Tipo de Script |
|-----------------|---|----------------|
| `onRequest` | | Suitelet |
| `pageInit` | | ClientScript |
| `beforeSubmit` / `afterSubmit` | | UserEvent |
| `getInputData` / `map` / `reduce` | | MapReduce |
| `execute` | | Scheduled |

### Para usar OrkidNS

1. Configurá el agente en `opencode.json`
2. Inicializá con `orkidns init` en tu proyecto
3. Usá los comandos para crear y validar

Ver `orkidns/AGENT.md` para documentación completa del agente.