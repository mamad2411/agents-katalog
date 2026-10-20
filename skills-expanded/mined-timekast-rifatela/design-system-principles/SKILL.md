---
name: design-system-principles
description: Universal design system consistency rules. Token usage, component reuse, theme verification, paradigm-agnostic anti-patterns. Applies to ANY stack (React, Flutter, vanilla, mobile).
---

# Design System Principles

> **Scope:** Universal — aplica a CUALQUIER design system, framework, y plataforma.
> **No es stack-specific:** Estos principios funcionan igual en React/Tailwind, Flutter/Material, SwiftUI, vanilla CSS, o cualquier otro stack.

---

## Cuándo se Carga Este Skill

- Cualquier tarea que toque **UI, componentes, estilos, temas, o tokens**
- Independientemente de si el proyecto usa React, Flutter, vanilla, u otro stack
- Complementa (no reemplaza) skills stack-specific como `domains/ui` o `flutter-mobile-design`

---

## Principios Fundamentales

1. **Tokens sobre valores** — usar variables/tokens del sistema, nunca valores literales
2. **Kit sobre inline** — usar componentes del sistema de diseño, nunca crear primitivas crudas
3. **Escala sobre arbitrarios** — seguir las escalas definidas del sistema (spacing, radius, shadow)
4. **Multi-tema siempre** — verificar coherencia en TODOS los temas definidos por el proyecto
5. **Paradigma-agnóstico** — estos principios aplican a neumorphism, glassmorphism, material, custom, o cualquier otro

---

## Design System Anti-patterns (Agnóstico al Paradigma)

> Estos anti-patterns aplican a **CUALQUIER** design system — neumorphism, glassmorphism, material, custom.
> Son reglas de **consistencia fundamentales**, no de estética.

### 1. Valores hardcoded vs tokens

Usar colores hex, shadows literales, o radius fijos en vez de tokens del sistema.

| ❌ Anti-pattern          | ✅ Correcto                                  | Por qué                                       |
| ------------------------ | -------------------------------------------- | --------------------------------------------- |
| Color hex/literal inline | Token del sistema (CSS var, ThemeData, etc.) | Los temas no pueden overridear valores inline |
| Shadow literal           | Token de shadow del sistema                  | Cada paradigma define sombras distinto        |
| Radius fijo en píxeles   | Token de radius del sistema                  | Consistencia con la escala del diseño         |

**Aplica igual en neumorphism** (donde shadows definen profundidad) **que en material** (donde shadows definen elevación) **que en glassmorphism** (donde son difusas). El principio es el mismo: tokens, no valores mágicos.

**Ejemplos por stack:**

| Stack        | ❌ Hardcoded            | ✅ Token                                |
| ------------ | ----------------------- | --------------------------------------- |
| CSS/Tailwind | `#25D366`, `8px`        | `var(--brand-success)`, `var(--radius)` |
| Flutter      | `Color(0xFF25D366)`     | `Theme.of(context).colorScheme.primary` |
| SwiftUI      | `.init(red: 0.14, ...)` | `Color.accentColor` del asset catalog   |

### 2. Mezcla de paradigmas de estilo

Usar utilidades genéricas del framework cuando el proyecto tiene tokens custom que redefinen esos conceptos.

> **Regla:** Si el proyecto define custom tokens para un concepto (shadow, radius, spacing),
> las utilidades genéricas del framework para ese concepto quedan **prohibidas**.
> El proyecto las redefinió por algo.

**Ejemplos:**

| Stack      | ❌ Genérico del framework                                | ✅ Token del proyecto                              |
| ---------- | -------------------------------------------------------- | -------------------------------------------------- |
| Tailwind   | Utilidad genérica de shadow cuando existen tokens custom | Token custom del sistema activo                    |
| Flutter    | `elevation: 4` cuando existe `AppShadows.card`           | `AppShadows.card`                                  |
| Cualquiera | Valores por defecto del framework                        | Tokens definidos por el design system del proyecto |

### 3. Componentes inline vs UI kit

Crear elementos crudos cuando existe un componente envuelto con theming en el UI kit del proyecto.

| ❌ Anti-pattern                      | ✅ Correcto                                       |
| ------------------------------------ | ------------------------------------------------- |
| Elemento crudo sin theming           | Componente del UI kit que hereda estilos del tema |
| Input sin wrapper                    | Componente Input del kit con estados consistentes |
| Container con estilos ad-hoc de card | Componente Card del sistema                       |

> 🔴 **OBLIGATORIO:** Consultar el inventario de componentes del proyecto antes de crear cualquier componente inline.
> Si existe en el kit → usarlo. Si no existe → crearlo en el kit, no inline.

**Referencia por stack:**

| Stack               | Inventario a consultar                  |
| ------------------- | --------------------------------------- |
| SK Projects (React) | `docs/reference/INVENTORY.md`           |
| Flutter             | `lib/widgets/` directory + pubspec deps |
| Otro                | Directorio de componentes del proyecto  |

### 4. Token inconsistency

Usar múltiples valores distintos de radius/shadow/spacing que no vienen de la misma escala.

| ❌ Anti-pattern                                      | ✅ Correcto                    |
| ---------------------------------------------------- | ------------------------------ |
| 3+ valores de radius distintos en la misma pantalla  | Un token de radius consistente |
| Spacing inconsistente (12, 16, 14 en la misma vista) | Escala de spacing del sistema  |
| Shadows con intensidades random                      | Escala de elevación definida   |

> Si una pantalla usa 3+ valores para el mismo concepto visual, es un error.
> Los design systems definen escalas con propósito.

### 5. Single-theme development

Implementar solo para un tema y no verificar los demás.

| ❌ Anti-pattern                                       | ✅ Correcto                                                |
| ----------------------------------------------------- | ---------------------------------------------------------- |
| Solo verificar light mode                             | Verificar **TODOS** los temas definidos por el proyecto    |
| Asumir que dark = light con colores invertidos        | Cada tema puede tener diferente contrast, spacing, shadows |
| No probar temas adicionales (midnight, high contrast) | Verificar coherencia en toda la palette                    |

> **Regla:** Verificar coherencia visual en **TODOS** los temas definidos por el proyecto.
> Si el proyecto tiene light, dark, y midnight → verificar los 3.

---

## Checklist de Verificación

Antes de cerrar cualquier tarea de UI, verificar:

- [ ] ¿Todos los colores usan tokens, no valores literales?
- [ ] ¿Todas las shadows, radius, y spacing usan tokens del sistema?
- [ ] ¿Se reutilizaron componentes del kit en vez de crear inline?
- [ ] ¿Los valores de una misma categoría (radius, spacing) son consistentes?
- [ ] ¿Se verificó en TODOS los temas del proyecto?

---

## Relación con Otros Skills

| Skill                   | Relación                                                                                            |
| ----------------------- | --------------------------------------------------------------------------------------------------- |
| `domains/ui`            | Stack-specific (React/Next). Este skill define los PRINCIPIOS; `domains/ui` define el CÓMO en React |
| `design-engineering`    | Execution de visual polish. Este skill define las REGLAS BASE que design-engineering debe respetar  |
| `frontend-design`       | Principios de UX/psicología. Este skill es sobre CONSISTENCIA del sistema                           |
| `flutter-mobile-design` | Stack-specific (Flutter). Misma relación que con `domains/ui`                                       |
| `tailwind-patterns`     | Framework-specific. Este skill es framework-agnostic                                                |

---

_TimeKast Factory — Design System Principles (Universal, Stack-Agnostic)_
