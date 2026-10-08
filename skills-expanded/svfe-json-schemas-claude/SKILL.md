# CLAUDE.md

Este archivo proporciona orientación a Claude Code (claude.ai/code) cuando trabaja con código en este repositorio.

## Descripción general

Este repositorio contiene **definiciones de JSON Schema (Draft-07) y ejemplos funcionales** para los documentos tributarios electrónicos (DTE) de El Salvador, según las especificaciones del Ministerio de Hacienda (MH) para el SVFE (*Sistema de Validación de Factura Electrónica*). Los esquemas son utilizados por contribuyentes, certificadores y el propio MH para validar los payloads JSON transmitidos durante la facturación electrónica.

El repositorio es **únicamente de datos** — no hay código fuente, pipeline de construcción ni framework de pruebas. El trabajo consiste en editar los propios archivos JSON.

## Estructura del repositorio

Cada esquema tiene dos archivos asociados:

| Patrón de archivo | Propósito |
| --- | --- |
| `fe-<tipo>-v<n>.json` | Definición del esquema (Draft-07) para el tipo de DTE |
| `fe-<tipo>-v<n>-funcional.json` | Instancia de ejemplo que satisface el esquema |
| `<evento>-schema-v<n>.json` | Esquema para un evento (anulación, contingencia) |
| `<evento>-schema-v<n>-funcional.json` | Instancia de ejemplo del evento |

### Tipos de documentos (DTE)

- `fe-fc-v1` — Factura (Consumidor Final)
- `fe-ccf-v3` — Comprobante de Crédito Fiscal
- `fe-nc-v3` — Nota de Crédito
- `fe-nd-v3` — Nota de Débito
- `fe-nr-v3` — Nota de Remisión
- `fe-fex-v1` — Factura de Exportación
- `fe-fse-v1` — Factura de Sujeto Excluido
- `fe-cd-v1` — Comprobante de Donación
- `fe-cr-v1` — Comprobante de Retención
- `fe-cl-v1` — Comprobante de Liquidación
- `fe-dcl-v1` — Documento Catálogo de Liquidación

### Esquemas de eventos

- `anulacion-schema-v2` — Anulación / invalidación de un DTE
- `contingencia-schema-v3` — Reporte de transmisión por contingencia

## Convenciones comunes de los esquemas

Estos patrones se repiten en todos los esquemas — manténgalos consistentes al agregar campos:

- **Dialecto del esquema**: `"$schema": "http://json-schema.org/draft-07/schema#"` (note el `#`; el esquema de contingencia actualmente lo omite — vea Inconsistencias conocidas más abajo).
- **Ambiente** (`ambiente`): `"00"` = pruebas, `"01"` = producción.
- **Campo `version`**: se declara como `const` (p. ej. `"const": 2` en `fe-fc-v1`) para fijar el esquema a su versión de DTE.
- **`codigoGeneracion`** (UUID v4 en hexadecimal, mayúsculas, guiones, 36 caracteres):
  ```json
  "pattern": "^[A-F0-9]{8}-[A-F0-9]{4}-[A-F0-9]{4}-[A-F0-9]{4}-[A-F0-9]{12}$"
  ```
- **`numeroControl`** (31 caracteres) para DTE tipo factura:
  ```
  ^DTE-<tipoDte>-(M|B|S|P)([0-9]{3})(P)([0-9]{3})-[0-9]{15}
  ```
  Letras de prefijo: `M`=Matriz, `B`=Sucursal, `S`=Sede, `P`=Punto de venta.
- **Fecha/hora**: `fecEmi` / `fecAnula` usan `format: "date"` (ISO `yyyy-mm-dd`); `horEmi` / `horAnula` usan un patrón `HH:MM:SS`.
- **Descripciones**: cada propiedad lleva una `description` en español. Mantenga este estilo al agregar campos.

### Estructura típica de nivel superior (DTE de factura)

```
identificacion        → version, ambiente, tipoDte, numeroControl, codigoGeneracion,
                        tipoModelo (1=normal, 2=contingencia), tipoOperacion,
                        tipoContingencia, motivoContin, fecEmi, horEmi, tipoMoneda
documentoRelacionado  → arreglo de DTE relacionados (o null)
otrosDocumentos       → documentos adjuntos (o null)
emisor                → NIT, NRC, nombre, actividad económica, dirección, contacto
receptor              → documento, NIT/NRC, dirección, contacto
ventaTercero          → null o bloque de vendedor tercero
cuerpoDocumento       → arreglo de ítems (numItem, tipoItem, cantidad, precios, tributos)
resumen               → totales (gravada/exenta/no sujeta, descuentos, IVA, total a pagar)
extension             → entrega/recibe, observaciones, placaVehiculo
apendice              → arreglo de campos extra (o null)
```

`anulacion-schema-v2` y `contingencia-schema-v3` usan una forma de nivel superior distinta (`identificacion` + payload específico del evento) y no son intercambiables con los esquemas de factura.

## Validación

No hay un ejecutor de pruebas incluido. Para validar localmente use cualquier validador de JSON Schema Draft-07, por ejemplo:

```bash
# Instalar una vez (requiere Node.js)
npm i -g ajv-cli ajv-formats

# Validar una instancia de ejemplo contra su esquema
ajv validate -s fe-fc-v1.json -d fe-fc-v1-funcional.json --spec=draft7 --strict=false

# Igual para un evento
ajv validate -s anulacion-schema-v2.json -d anulacion-schema-v2-funcional.json \
  --spec=draft7 --strict=false
```

Alternativa en Python (puntual, sin instalación global):

```bash
python -m pip install jsonschema
python -c "import json, jsonschema; \
  jsonschema.Draft7Validator.check_schema(json.load(open('fe-fc-v1.json'))); \
  jsonschema.validate(json.load(open('fe-fc-v1-funcional.json')), \
  json.load(open('fe-fc-v1.json')))"
```

Al modificar un esquema, pase su archivo `*-funcional.json` compañero por el validador para confirmar que aún pasa, y actualice el ejemplo si es el ejemplo lo que se está corrigiendo.

## Guía de edición

- **Tenga cuidado al incrementar `version`.** El campo `version` es un `const`, por lo que cambiarlo obliga a todos los emisores a actualizarse a la vez. Coordine con los cambios de especificación del MH.
- **`additionalProperties: false`** se usa en algunos objetos (p. ej. `identificacion` en `anulacion-schema-v2`). Al agregar campos a un objeto cerrado, actualice también su arreglo `required`.
- **En este repositorio coexisten dos estilos de indentación**: 4 espacios (la mayoría de archivos `fe-*` y `anulacion`) y 2 espacios (`contingencia-schema-v3.json`). Use el estilo del archivo que esté editando.
- **Los montos monetarios** son números JSON con precisión implícita de 2 decimales. No los cambie a cadenas de texto.
- **Nombres de campos en español** — manténgalos en español, acorde a la nomenclatura del MH.

## Inconsistencias conocidas

- `contingencia-schema-v3.json` declara `"$schema": "http://json-schema.org/draft-07/schema"` (falta el `#`). Todos los demás esquemas incluyen el `#`. Prefiera la forma `schema#` al editar ese archivo.
- `fe-fc-v1.json` declara `"const": 2` para el campo `version`, mientras que el archivo se llama `…-v1.json`. El valor del esquema es la versión del esquema DTE (según MH), no el sufijo del nombre de archivo. Verifique antes de cambiar cualquier lado.
- Algunos ejemplos `*-funcional.json` usan valores como `"version": 1` que no satisfacen la restricción `const` de su esquema compañero. Vuelva a validar los ejemplos tras editar los esquemas.

## Flujo de trabajo con Git

Rama única (`main`) contra `https://github.com/Rey9530/svfe-json-schemas.git`. Los commits recientes siguen el patrón `<descripción corta>` (p. ej. `Nuevos`, `Contingencia`, `anulacion:true`, `La mayoria`). Mantenga los commits limitados a un tipo de DTE o evento cuando sea posible.
