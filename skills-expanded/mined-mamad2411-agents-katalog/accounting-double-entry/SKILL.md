---
name: accounting-double-entry
description: Gate de diseño para contabilidad por partida doble — asientos balanceados (débitos = créditos), plan de cuentas con naturaleza, libro mayor inmutable con corrección por contra-asiento, dinero en enteros de la menor unidad (nunca float), moneda y redondeo, periodos y cierre, idempotencia de asientos, conciliación y modelado de activos y pasivos. Usar al modelar o tocar cualquier registro contable, un asiento, un movimiento de saldo, un módulo de activos/pasivos, o antes de cerrar un cambio que mueva dinero.
allowed-tools: Read Grep Glob Bash
effort: high
---

<!-- ESPEJO GENERADO por AtlasPromptManager/tools/install_skills.py - NO EDITAR A MANO -->
<!-- La fuente es AtlasPromptManager/.claude/skills/. Lo que edites aca se pierde. -->

# Contabilidad por partida doble — reglas de diseño

Skill de ingeniería contable, no de asesoría. Las reglas fiscales, impositivas y de presentación
de estados financieros dependen del país y del marco (NIIF/US GAAP/local): **validá con el
responsable contable/legal** antes de fijar tasas, cuentas obligatorias o formatos de reporte.
Lo que sigue es cómo se construye el motor sin corromper los datos.

## 1. La invariante madre

Todo hecho económico se registra como un **asiento** con dos o más **líneas**; la suma de débitos
es igual a la suma de créditos, **siempre**, hasta el último centavo.

```sql
-- Invariante en la base, no solo en la app
CREATE CONSTRAINT TRIGGER entry_balanced ...  -- verifica SUM(debit) = SUM(credit) por asiento
-- o CHECK diferido sobre la agregación de líneas al COMMIT
```

- Nunca persistás un asiento a medio balancear. Si el proceso escribe línea por línea, envolvé
  todo en una transacción y verificá el balance **antes** del commit (ver `concurrency-and-locking`).
- Un asiento nace completo o no nace.

## 2. Dinero: enteros, nunca float

- Guardá importes como **enteros en la menor unidad** de la moneda (centavos), o `NUMERIC`/`DECIMAL`
  de precisión fija. **Prohibido `float`/`double`/`real`** para dinero: `0.1 + 0.2 != 0.3`.
- El tipo lleva **siempre** la moneda asociada (columna `currency_code`, ISO 4217). No sumes
  importes de monedas distintas; una operación multimoneda registra el tipo de cambio usado.
- Redondeo: definí el modo (medio-par / medio-arriba) **una vez** y aplicalo en un solo lugar.
  El redondeo se hace al calcular, no al mostrar; la suma de partes redondeadas debe cuadrar con
  el total (asigná el residuo a una línea, no lo pierdas).

```ts
// ❌ 19.99 dólares como número
price: 19.99
// ✅ centavos + moneda
amountMinor: 1999, currencyCode: 'USD'
```

## 3. Plan de cuentas y naturaleza

- Cada cuenta tiene un **tipo**: activo, pasivo, patrimonio, ingreso, gasto (modelalos como
  conceptos codificados, no enum de lenguaje — ver `terminology-value-sets`).
- La **naturaleza** define qué la aumenta: activo y gasto aumentan por el débito; pasivo,
  patrimonio e ingreso aumentan por el crédito. El signo del saldo se deriva de la naturaleza,
  no se guarda suelto.
- Ecuación contable: **Activo = Pasivo + Patrimonio**. El módulo de activos y pasivos es una vista
  sobre las cuentas de esos tipos; no dupliques saldos, derivalos del mayor.
- Cuentas jerárquicas (grupo → subcuenta): saldo del grupo = suma de hijas. Ver
  `database-design` para el árbol.

## 4. Inmutabilidad: el mayor no se edita

- El libro mayor es **append-only**. Un asiento contabilizado (posted) **no se edita ni se borra**.
- ¿Error? Se corrige con un **contra-asiento** (reversión) y luego el asiento correcto. Queda el
  rastro de los tres. Esto **es** el control de auditoría (ver `audit-trail-history`).
- Estados del asiento: `draft` → `posted` → (`reversed`). `draft` se puede editar; `posted` es
  inmutable. La transición a `posted` es la que valida balance, periodo y moneda
  (ver `state-machines-workflows`).

## 5. Idempotencia y concurrencia

- Cada asiento generado por un evento de negocio lleva una **clave de idempotencia** (ej.
  `source_type` + `source_id`): reintentar el mismo pago **no** crea dos asientos. Constraint UNIQUE.
- Saldos: no mantengas un contador de saldo mutable sin cuidado. Si lo cacheás/materializás,
  actualizalo dentro de la misma transacción del asiento y protegé la carrera del doble asiento
  con locking (ver `concurrency-and-locking`). Preferí derivar el saldo por suma cuando el volumen
  lo permita, o usar saldos por periodo (snapshot de cierre + movimientos del periodo).

## 6. Periodos y cierre

- Los asientos pertenecen a un **periodo contable**. Un periodo **cerrado** no acepta más asientos:
  rechazá con 409/422 (ver `error-handling-contract`). La fecha contable puede diferir de la fecha
  de registro; ambas se guardan.
- El cierre calcula saldos finales, traslada resultados y bloquea el periodo. Es una operación
  transaccional y auditada; su reversión es excepcional y registrada.

## 7. Conciliación

- Toda cuenta que refleje un ente externo (banco, pasarela, aseguradora) necesita **conciliación**:
  marcar qué movimientos del mayor corresponden a movimientos del extracto externo, y reportar
  diferencias. Modelá el estado de conciliación por línea, no lo infieras.

## Anti-patrones

- Dinero en `float`; importes sin moneda; sumar monedas distintas.
- Editar o borrar un asiento contabilizado; "arreglar" un saldo con un UPDATE manual.
- Saldo como verdad primaria en vez de derivarlo del mayor.
- Un asiento que no balancea "porque después lo ajusto".
- Numerar/fechar en la app sin considerar el periodo contable.

## Checklist

- [ ] Débitos = créditos garantizado en la base, no solo en la app.
- [ ] Importes en enteros de la menor unidad (o DECIMAL fijo) + moneda ISO 4217; sin float.
- [ ] Redondeo definido en un solo lugar; el residuo se asigna, no se pierde.
- [ ] Naturaleza de cuenta modelada; saldos derivados, ecuación A = P + Pn respetada.
- [ ] Mayor append-only; correcciones por contra-asiento; asiento `posted` inmutable.
- [ ] Clave de idempotencia por asiento de origen; carrera de saldo protegida.
- [ ] Periodo cerrado rechaza asientos; fecha contable y de registro separadas.
- [ ] Cuentas con contraparte externa tienen estado de conciliación.

## Evidencia / DoD

Para declarar correcto un cambio contable, pegá la **salida literal** de:
- una prueba que intenta un asiento desbalanceado y recibe el rechazo esperado;
- una prueba de idempotencia: el mismo evento de origen ejecutado dos veces deja **un** asiento
  (conteo `SELECT count(*)` = 1);
- una prueba de reversión: contra-asiento que deja el saldo neto correcto y ambos asientos visibles;
- un intento de asiento sobre periodo cerrado que devuelve 409/422.
Sin esa salida pegada, el estado es WRITTEN, no VERIFIED (ver `evidence-and-verification`).
