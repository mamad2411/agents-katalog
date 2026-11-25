---
name: quotations-billing
description: Diseño de cotizaciones y facturación — líneas con impuestos y descuentos calculados en el servidor, versionado de la cotización, estados (borrador, enviada, aceptada, vencida, rechazada), conversión a factura u orden, inmutabilidad tras la emisión, numeración correlativa sin huecos y manejo de moneda. Usar al modelar o tocar cotizaciones, presupuestos, facturas, notas o cualquier documento con importes que un cliente acepta o paga, y al calcular totales, impuestos o descuentos.
---

<!-- ESPEJO GENERADO por AtlasPromptManager/tools/install_skills.py - NO EDITAR A MANO -->
<!-- La fuente es AtlasPromptManager/.claude/skills/. Lo que edites aca se pierde. -->

# Cotizaciones y facturación — reglas de diseño

Skill de ingeniería. Las reglas de impuestos, retenciones, requisitos de factura legal y
numeración obligatoria dependen del país: **validá con el responsable contable/legal** las tasas,
los campos obligatorios y el formato. Acá va cómo se modela el documento sin corromperlo.

## 1. El total se calcula en el servidor, siempre

- El cliente **propone** cantidades y productos; el servidor **calcula** precios, descuentos,
  impuestos y totales. Nunca confíes en un total que llega del front (ver `authz-access-control`,
  mass assignment).
- Guardá el desglose, no solo el total: por línea → subtotal, descuento, base imponible, impuesto,
  total; y el documento → suma de líneas + impuestos + descuentos globales.
- Dinero en enteros de la menor unidad + moneda, sin float (ver `accounting-double-entry`).
  El redondeo por línea vs por total debe ser consistente y definido una sola vez.

## 2. Precio congelado en el momento

- La línea guarda el **precio unitario vigente al emitir**, no una referencia viva al catálogo.
  Si mañana sube el precio, la cotización enviada ayer no cambia.
- Igual con la tasa de impuesto y el tipo de cambio: se congelan en el documento.

```ts
// ❌ línea que apunta al precio actual del producto
{ productId, quantity }          // el total cambia solo con el tiempo
// ✅ línea con el precio capturado
{ productId, quantity, unitPriceMinor: 5000, taxRate: 0.13, currencyCode: 'USD' }
```

## 3. Estados y ciclo de vida

Modelá el ciclo como máquina explícita (ver `state-machines-workflows`):

`draft` → `sent` → (`accepted` | `rejected` | `expired`) → `converted`

- `draft`: editable libremente.
- `sent`/`accepted`: **inmutable**. Un cambio genera una **nueva versión**, no una edición.
- `expired`: por fecha de validez; calculado, no dejado al azar.
- Las transiciones válidas y quién puede hacerlas se validan en el servidor.

## 4. Versionado

- Editar una cotización ya enviada crea la **versión N+1**, conservando la N. El cliente siempre
  ve qué versión aceptó. La versión aceptada es la que se convierte.
- Guardá qué versión se envió, cuándo y a quién (rastro auditable, ver `audit-trail-history`).

## 5. Conversión a factura/orden

- Aceptar una cotización habilita convertirla en factura u orden. La factura **hereda** las líneas
  congeladas; no recalcula contra el catálogo actual.
- La conversión es idempotente: aceptar dos veces no crea dos facturas (clave de idempotencia).
- Al emitir la factura, se genera el asiento contable correspondiente
  (ver `accounting-double-entry`); ambos comparten la clave de origen.

## 6. Numeración correlativa

- Las facturas suelen exigir **numeración correlativa sin huecos** por serie. Un simple
  `MAX(number)+1` bajo concurrencia genera huecos o duplicados.
- Usá una **secuencia por serie** con la garantía que exija la norma (a veces se requiere que no
  haya huecos ni siquiera ante rollback — eso puede obligar a reservar el número en una tabla
  con lock, no en una `SEQUENCE` de Postgres que sí deja huecos). **Definí el requisito exacto
  con el responsable legal** y elegí el mecanismo acorde (ver `concurrency-and-locking`).
- El número se asigna **al emitir**, no al crear el borrador.

## 7. Moneda e impuestos

- Cada documento tiene su moneda; multimoneda registra el tipo de cambio congelado.
- Los impuestos pueden ser por línea, por documento, incluidos o agregados: definí el modelo y sé
  consistente. No hardcodees la tasa: es un dato con vigencia (ver `terminology-value-sets` para
  catálogos de impuestos).

## Anti-patrones

- Confiar en el total enviado por el cliente.
- Línea que referencia el precio vivo del catálogo en vez de congelarlo.
- Editar una cotización/factura emitida en lugar de versionar o contra-documentar.
- `MAX(number)+1` para numeración legal bajo concurrencia.
- Recalcular impuestos de una factura vieja con la tasa de hoy.

## Checklist

- [ ] Todos los importes se calculan en el servidor; el desglose por línea se persiste.
- [ ] Precio, tasa de impuesto y tipo de cambio congelados en el documento al emitir.
- [ ] Ciclo de estados explícito; documento emitido es inmutable; los cambios versionan.
- [ ] Conversión a factura idempotente y con líneas heredadas.
- [ ] Numeración correlativa acorde al requisito legal (verificado), asignada al emitir.
- [ ] Dinero en enteros + moneda, sin float; redondeo consistente.
- [ ] Emisión de factura genera su asiento contable con clave de origen compartida.
