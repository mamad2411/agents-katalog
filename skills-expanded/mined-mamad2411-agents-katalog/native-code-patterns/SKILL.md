---
name: native-code-patterns
description: Muestreo de patrones antes de escribir código en un repo existente, para que el cambio sea indistinguible del código vecino. Usar antes de crear o editar un controller, servicio, entidad ORM, DTO, componente, cliente de API, test o script — localizar 2–3 ejemplos cercanos del mismo tipo y copiar su forma (naming, estructura, errores, imports, densidad de comentarios). Cubre también qué hacer cuando el patrón existente es malo.
effort: medium
---

<!-- ESPEJO GENERADO por AtlasPromptManager/tools/install_skills.py - NO EDITAR A MANO -->
<!-- La fuente es AtlasPromptManager/.claude/skills/. Lo que edites aca se pierde. -->

# Código nativo — muestreo de patrones

Un repo tiene un idioma local. El código correcto pero escrito en otro idioma es deuda:
obliga al revisor a traducir, rompe el grep del equipo, duplica utilidades y abre una
segunda forma de hacer lo mismo. El objetivo es que nadie pueda decir qué archivo lo
escribió un agente.

Esta skill decide la **forma**. La calidad intrínseca la deciden `clean-code` y
`solid-principles`; la convención del repo manda sobre la preferencia genérica.

## 1. Muestreo: antes del primer edit

Para cada tipo de pieza que vas a crear o tocar, localizá **2–3 ejemplos vecinos del
mismo tipo** y leelos completos. Uno solo puede ser la excepción; tres muestran la regla.

Cómo elegir las muestras:

1. Mismo tipo exacto: controller con controller, test de servicio con test de servicio.
2. Lo más cerca posible: mismo módulo antes que otro módulo.
3. **Recientes**: preferí los tocados hace poco (`git log` del directorio). En repos con historia conviven el estilo viejo y el vigente; el vigente es el de los últimos cambios aceptados.
4. Si las muestras se contradicen entre sí, gana la más reciente y la más repetida. Anotá la inconsistencia.

## 2. Qué extraer de cada muestra

| Dimensión | Qué mirar |
|---|---|
| Ubicación y nombre de archivo | Carpeta, sufijos, singular/plural, kebab vs camel |
| Naming | Clases, métodos, variables, rutas, claves de i18n, nombres de tests |
| Estructura interna | Orden de miembros, tamaño de funciones, qué va en cada capa |
| Imports | Alias de paths, barrels, orden, extensión en ESM, imports de tipo |
| Inyección y wiring | Cómo se registran providers, rutas, clientes; qué archivo de registro hay que tocar además |
| Manejo de errores | Qué excepciones se lanzan, quién las traduce, qué códigos HTTP |
| Validación | Dónde se valida, con qué librería, qué mensajes |
| Acceso a datos | Transacciones, repositorios vs gestor de entidades, paginación |
| Estado y async (UI) | Signals vs observables, cómo se modelan carga/error/vacío |
| Estilos (UI) | Tokens/variables usadas, convención de clases, dónde viven los estilos |
| Tests | Framework, fixtures, factories, nivel de mock, forma de los `describe`/`it` |
| Comentarios | **Densidad** y tono: si los vecinos no comentan, vos tampoco |
| Generación | Si las piezas se crean con un generador/CLI, usalo: no las escribas a mano |

Las piezas rara vez van solas. Preguntá siempre: *¿qué más tocó el último que agregó una
de estas?* (registro de módulo, índice, cliente tipado, doc de API, seed, test). El commit
que agregó la muestra es la mejor lista de verificación.

## 3. Jerarquía de autoridad

Cuando dos fuentes discrepan, manda la de más arriba:

1. `CLAUDE.md` y rules del proyecto (convención declarada).
2. El patrón del **mismo archivo**.
3. El patrón del **mismo módulo**.
4. El patrón del **repositorio**.
5. La documentación del framework.
6. La preferencia genérica, incluidas las skills de la casa.

## 4. Escribir

- Copiá la **forma**, no el contenido: partí del esqueleto de la mejor muestra y reemplazá la lógica.
- Reusá antes de crear: si existe un helper, un componente base, una excepción o un pipe que hace el trabajo, usalo. Buscalo antes de escribir el tuyo.
- Mismo nivel de defensividad que los vecinos: si el repo confía en la validación del borde, no re-valides en cada capa.
- Mismo nivel de abstracción: no introduzcas una interfaz, una factory o un genérico para un caso único si el repo no lo hace.
- No reformatees lo que no tocás. El formato global es otro cambio y otro PR (ver `scope-discipline`).

Ejemplo — el repo traduce errores con excepciones tipadas del framework:

```ts
// ❌ correcto en abstracto, extranjero en este repo
async findOne(id: string): Promise<Result<Patient, AppError>> {
  try {
    const p = await this.repo.findOne(id);
    return p ? ok(p) : err(new AppError('NOT_FOUND'));
  } catch (e) { return err(wrap(e)); }
}

// ✅ igual que los tres servicios vecinos
async findOne(id: string): Promise<Patient> {
  const patient = await this.repo.findOne(id);
  if (!patient) throw new NotFoundException(`Patient ${id} not found`);
  return patient;
}
```

## 5. Cuando el patrón existente es malo

La regla por defecto: **seguilo y anotalo. No bifurques.**

Dos formas de hacer lo mismo es peor que una forma mediocre: el próximo que llegue no sabe
cuál copiar, y tu versión "mejor" se convierte en la excepción que nadie mantiene.

| Situación | Qué hacer |
|---|---|
| Feo, verboso o pasado de moda, pero funciona | Seguilo. Anotá la mejora sugerida como nota o issue, fuera del cambio. |
| Inconsistente (dos estilos conviven) | Seguí el más reciente/repetido. Anotá la inconsistencia. |
| Deprecado con reemplazo **ya adoptado** en el repo | Usá el reemplazo: ese es el patrón vigente. |
| Contradice una regla declarada del proyecto | Manda la regla (§3). Decilo en el reporte. |
| Defecto real de **seguridad, integridad de datos o corrección** | No lo propagues. Hacé lo correcto en tu cambio, con la menor desviación de forma posible, y reportá el defecto del patrón de forma explícita para que se decida el arreglo general. |
| No existe ningún patrón | Doc del framework + skills de la casa. Alcance mínimo, y registrá la decisión (ver `technical-docs-and-adr`). |

Lo que **nunca**: arreglar el patrón en todos lados "de paso", o introducir el patrón nuevo
solo en tu archivo sin avisar. Migrar una convención es un trabajo propio, con su plan
(`refactoring-safely`).

## Anti-patrones

- ❌ Introducir una arquitectura nueva porque es "mejor".
- ❌ Envolver todo en `try/catch`, null-checks y helpers defensivos que el repo no usa.
- ❌ Comentarios narrativos que explican lo que el código ya dice, en un repo que no comenta.
- ❌ Traer una librería nueva para algo que el repo ya resuelve con otra.
- ❌ Escribir a mano lo que el equipo genera con un CLI.
- ❌ Muestrear un único archivo — y que fuera el legado.
- ❌ Crear la pieza y olvidar el archivo de registro que todas las piezas vecinas tocan.
- ❌ Nombres en otro idioma o convención que los vecinos.

## Checklist

- [ ] Leí completas 2–3 muestras del mismo tipo, cercanas y recientes.
- [ ] Mi archivo está donde están sus vecinos y se llama como ellos.
- [ ] Naming, orden de miembros, imports y manejo de errores coinciden con las muestras.
- [ ] Reusé helpers, bases y excepciones existentes; no dupliqué ninguno.
- [ ] Toqué los mismos archivos de registro/wiring que tocó la última pieza equivalente.
- [ ] Densidad de comentarios y nivel de defensividad iguales a los del módulo.
- [ ] Usé el generador del proyecto si las piezas se generan.
- [ ] No reformateé ni "mejoré" código fuera del alcance.
- [ ] Si me desvié de un patrón, está justificado por §5 y dicho en el reporte.
- [ ] Un revisor no podría distinguir este cambio del de un miembro del equipo.
