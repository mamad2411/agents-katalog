---
name: productivity-patch
description: Aplica correcciones específicas a partir de hallazgos del CODE_REVIEW.md generado por productivity-code-review. Toma un número de issue del reporte y genera el diff/patch concreto, edita el archivo, o explica la corrección paso a paso. Úsala cuando el usuario diga "aplica el fix #7", "corrige el hallazgo de seguridad #3", "implementa la mejora #12 del reporte", o "patch el issue de XSS en orders.ts".
disable-model-invocation: true
requires-devkits: auto-detect
---

# Productivity Patch — Reporte a Corrección

Convierte hallazgos del `CODE_REVIEW.md` en correcciones concretas aplicadas al código.

---

## Workflow

### Paso 1: Identificar el hallazgo

El usuario referencia un hallazgo del reporte de `productivity-code-review` por:
- **Número de issue**: "#7" o "issue 7"
- **Archivo + línea**: "el XSS en orders.ts:42"
- **Descripción**: "el problema de CORS en Program.cs"

Buscar en `CODE_REVIEW.md` del proyecto el hallazgo exacto:

```markdown
| 7 | 🔴 Crítico | `src/orders.ts:42` | XSS: innerHTML con input de usuario | Usar textContent o sanitizar con DOMPurify | ⬜ |
```

### Paso 2: Analizar el archivo y contexto

Leer el archivo afectado y entender el contexto:
- Líneas alrededor del problema (±10 líneas)
- Dependencias, imports, tipado
- Si el archivo es parte de un módulo más grande, leer archivos relacionados

### Paso 3: Generar la corrección

#### Por categoría de hallazgo

| Categoría | Patrón de fix |
|-----------|---------------|
| **Seguridad — XSS** | `innerHTML = userInput` → `textContent = userInput` o `sanitize(userInput)` |
| **Seguridad — SQL Injection** | `query = "SELECT * FROM " + table` → query parametrizado |
| **Seguridad — CORS** | `AllowAnyOrigin()` → `WithOrigins("https://miapp.com")` |
| **Seguridad — Secrets** | `const apiKey = "sk_live_xxx"` → `const apiKey = process.env.STRIPE_KEY` |
| **Mejoras — any** | `function process(data: any)` → tipar con interfaz concreta |
| **Mejoras — código duplicado** | Extraer a función compartida, importar en ambos lugares |
| **Optimizaciones — N+1** | `.findMany()` en loop → `.findMany({ where: { id: { in: ids } } })` |
| **Optimizaciones — sin caché** | Agregar `lru_cache` o Redis al método |
| **Optimizaciones — sin paginación** | Agregar `.limit(pageSize).offset(...)` |

### Paso 4: Presentar el diff

Mostrar el cambio propuesto antes de aplicarlo:

```diff
- document.getElementById('output')!.innerHTML = userInput;
+ document.getElementById('output')!.textContent = userInput;
```

```typescript
// ❌ Antes (línea 42)
const apiKey = "sk_live_abc123xyz";

// ✅ Después
const apiKey = process.env.STRIPE_API_KEY;
if (!apiKey) throw new Error('STRIPE_API_KEY not set');
```

Preguntar: "¿Aplico este cambio?"

### Paso 5: Aplicar y verificar

Si el usuario confirma:

1. Editar el archivo con la herramienta `edit`
2. Si el fix requiere cambios en múltiples archivos, aplicarlos todos atómicamente
3. Verificar que el archivo sigue compilando/linter sin errores
4. Marcar el hallazgo como ✅ en `CODE_REVIEW.md`

```markdown
| 7 | 🔴 Crítico | `src/orders.ts:42` | XSS: innerHTML con input de usuario | Usar textContent | ✅ |
```

### Paso 6: Sugerir test

Para hallazgos de seguridad o lógica:

```
💡 Este fix previene XSS. ¿Quieres que genere un test que verifique que el input malicioso no se ejecuta?
```

Si el usuario dice sí, generar test mínimo (Vitest, pytest, xUnit según stack):

```typescript
it('sanitizes malicious input in order notes', () => {
  const malicious = '<img src=x onerror=alert(1)>';
  render(<OrderNotes notes={malicious} />);
  expect(screen.queryByRole('img')).not.toBeInTheDocument();
});
```

---

## Modo batch (múltiples fixes)

Si el usuario pide "aplica todos los fixes de seguridad":

1. Listar todos los hallazgos 🔴 de la tabla Seguridad
2. Aplicar uno por uno (el más crítico primero)
3. Mostrar progreso: `[████░░░░] 3 de 7 fixes aplicados`
4. Al final, resumen: "7 fixes aplicados en 5 archivos. CODE_REVIEW.md actualizado."

---

## Lo que NO debe hacer

- No aplicar fixes sin mostrar el diff antes (a menos que el usuario esté en modo batch y lo haya autorizado).
- No modificar lógica de negocio sin entenderla. Si el fix requiere cambiar comportamiento, preguntar.
- No arreglar "de paso" cosas que no están en el reporte (scope creep).
- No marcar como ✅ sin verificar que el fix compila/pasa lint.
- No generar tests para fixes triviales (typos, nombres de variable).
