---
name: synthetic-test-data-generation
description: Generación de datos de prueba sintéticos de calidad — factories deterministas con seed, datos de dominio (incluida salud) plausibles pero SIEMPRE inventados, coherencia referencial entre entidades, volumen para performance, distribuciones realistas, mezcla deliberada de casos válidos e inválidos, i18n con acentos y nombres compuestos, y reproducibilidad. Usar al construir factories o fixtures, al poblar un entorno de prueba o demo, al necesitar volumen para un test de carga, o cuando los tests fallan por datos poco realistas o irrepetibles.
allowed-tools: Read Grep Glob Bash
effort: high
---

<!-- ESPEJO GENERADO por AtlasPromptManager/tools/install_skills.py - NO EDITAR A MANO -->
<!-- La fuente es AtlasPromptManager/.claude/skills/. Lo que edites aca se pierde. -->

# Datos de prueba sintéticos de calidad

Datos de prueba de calidad = **plausibles, coherentes, reproducibles y sin un solo dato real**.
Un dataset de juguete (todo "Juan Pérez", una sola fila, sin acentos) esconde bugs que
producción sí va a exponer. Esta skill es sobre generarlos bien; el ciclo de vida en el test
(aislamiento, limpieza, reloj) lo cubre `test-data-management`, la privacidad `data-privacy-sensitive`,
y los catálogos reales sembrados en la app `seed-data-catalogs`.

## 0. Regla dura: sintético, nunca real
- Prohibido copiar datos de producción a un entorno de prueba. Si necesitás forma real, generá
  contra el modelo, no contra la base productiva. Datos de salud reales jamás salen de producción.
- "Sintético" no es "anonimizado": generá desde cero. Anonimizar mal re-identifica.
- Nada de fuentes reales usadas como si fueran ficticias ni al revés (ver `anti-hallucination-guard`).

## 1. Determinismo por seed
El mismo seed debe producir el mismo dataset byte a byte: sin eso, un fallo no se reproduce.

```ts
import { faker } from '@faker-js/faker';         // instancia global
// o localizada: import { fakerES as faker } from '@faker-js/faker';

faker.seed(1234);                                 // fija la secuencia
const nombre = faker.person.fullName();
```

- Seedeá al inicio del test o de la corrida de generación. Reseteá entre tests para no arrastrar
  estado: en Vitest/Jest, `afterEach(() => faker.seed())` (sin argumento vuelve a aleatorio real).
- Registrá el seed usado en la salida: un fallo trae su seed y se reproduce con él.
- No mezcles fuentes de aleatoriedad: si usás varias instancias Faker, compartí un `Randomizer`
  o seedeá todas, o la reproducibilidad se rompe.

## 2. Coherencia referencial y de negocio
Los datos sueltos pasan validación de tipo pero rompen invariantes.
- Generá el grafo, no filas aisladas: un `paciente` con sus `citas`, cada cita con un
  `profesional` y un `horario` que existan y no se solapen.
- Respetá las FKs y las reglas: una cita no puede ser anterior a la fecha de alta; un asiento
  contable debe cuadrar débito = crédito; un `*_concept_id` debe existir en el catálogo.
- Fechas relativas a un "ahora" fijo del test (ver reloj en `test-data-management`), no `Date.now()`.

## 3. Distribuciones realistas
- Variá: nombres compuestos, apellidos con `de la`, tildes, `ñ`, mayúsculas/minúsculas mezcladas,
  emails con `+`, teléfonos de largos distintos. Un builder que devuelve siempre lo mismo no prueba nada.
- Incluí la cola: registros muy viejos y muy nuevos, textos largos, colecciones grandes y vacías.
- Proporciones plausibles: si el 5% de las citas se cancelan, generá ~5%, no 50%.

## 4. Válidos e inválidos a propósito
Un buen generador produce también lo que debe ser rechazado, para los tests negativos.
- Marcá cada registro como `valid` / `invalid` con el motivo, para aseverar el comportamiento esperado.
- Para el catálogo sistemático de valores límite y adversos, usá `edge-case-data-catalog`.

## 5. Datos de personas (sintéticos)
- Nombres/documentos/direcciones: `faker` localizado. Nunca un documento de identidad real, ni la
  cédula de un conocido «para probar el OCR».
- Imágenes de identidad (carnet, selfie): generadas o de banco libre, nunca de una persona real.
- Datos financieros: montos, ingresos y movimientos plausibles pero claramente ficticios. Las
  reglas que los interpretan —tasas, plazos, umbrales de riesgo— no se inventan: se confirman.
- Etiquetá el dataset como sintético en la propia data (p. ej. dominio de email `@example.test`).

## 6. Volumen para performance
- Generá a escala con seed y por lotes; medí el tiempo de generación como parte del test de carga.
- Para volumen grande, generá una vez a un archivo/seed reproducible en vez de en cada corrida.
- El modelo de carga y los umbrales viven en `performance-load-testing`.

## Property-based (cuando el caso lo pide)
Cuando querés cubrir un espacio de entradas en vez de ejemplos elegidos a mano, generá con
`fast-check` y dejá que encuentre el contraejemplo:

```ts
import fc from 'fast-check';
it('el total nunca es negativo', () => {
  fc.assert(fc.property(fc.array(fc.nat()), (items) => total(items) >= 0));
});
```
Cuando falla, imprime `seed` y `path` para reproducir; pegalos en el reporte.

## Anti-patrones
- Dataset de una fila, o mil filas idénticas.
- `Math.random()` sin seed: irreproducible.
- Copiar un `dump` de producción "porque es más realista".
- Generadores que ignoran las FKs y dejan huérfanos (los caza `data-quality-validation`).
- Reusar el mismo email/documento en todos los registros y chocar con un `unique`.

## Checklist
- [ ] Seed fijado y registrado; misma seed ⇒ mismo dataset.
- [ ] Reset de la instancia entre tests.
- [ ] Grafo coherente: FKs válidas, invariantes de negocio respetadas.
- [ ] Distribución variada (acentos, largos, mayúsculas, cola).
- [ ] Registros inválidos etiquetados para los tests negativos.
- [ ] Cero datos reales; dataset marcado como sintético.

## Evidencia / DoD
Para afirmar que el generador sirve, pegá:
1. Comando de generación + **seed** usado.
2. Prueba de reproducibilidad: dos corridas con el mismo seed y su diff vacío (salida literal).
3. Resultado de `data-quality-validation` sobre el dataset (0 huérfanos, 0 duplicados indebidos).
4. Conteos por entidad y una muestra que evidencie variedad (no todo igual).
Sin la prueba de reproducibilidad, el dataset es `BLOCKED`, no `PASS`.
