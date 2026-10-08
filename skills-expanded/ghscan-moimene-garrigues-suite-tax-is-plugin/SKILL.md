---
name: suite-is-export-aeat
description: >-
  Genera la BASE DE IMPORTACIÓN a la AEAT del Impuesto sobre Sociedades desde la contabilidad, Balance/PyG
  formulado o carpeta de expediente: el fichero BOE `.200` (conforme al DR200 de ancho fijo que importa
  Sociedades WEB) y el XML mod200 validado contra el XSD oficial. Úsala cuando el usuario quiera
  "picar/exportar la declaración", "generar la base de importación AEAT", "el DR200", "el XML del 200",
  correr un expediente por carpeta o procesar **muchas declaraciones en lote** para dejar de teclearlas a mano.
  Consume el motor por servicio (`/exportar-aeat`, ADR-001); el número lo firma el motor (fail-closed).
metadata:
  version: "1.8.0"
---

# Suite IS — Export AEAT (.200 + XML) desde la contabilidad, 1 a 1 o en lote

Convierte la contabilidad (Sumas y Saldos) en la **base de importación a la AEAT**, para que no haya que
**picar** la declaración a mano. Es la cara de plugin de la Fase 5 (D20): orquesta el endpoint
`/exportar-aeat` del motor; **no** reescribe lógica fiscal (ADR-001).

## Qué produce (por sociedad)
- **`declaracion_dr`** → `declaracion_mod200_{ej}.200`: fichero BOE **`.200`** conforme al DR200 de ancho
  fijo (identificativos + contable + **liquidación BASE coherente del motor**, o la liquidación firmada si se
  aporta). Es **la declaración que se importa en Sociedades WEB**. El lote emite el `.200` **completo e
  importable por defecto** (lleva las páginas obligatorias 12/13/14/14B/DID → **evita EMALOBL**); `--solo-contable`
  vuelve al `.200` contable-solo (solo para la vía «Importación de datos contables» con el XML).
- **`xml_mod200`** → `modelo200_contable_{ej}.xml`: XML validado contra el **XSD oficial** (entregable
  PRIMARIO para importación contable; 451 casillas).
- Secundarios/no importables en AEAT: `estados_contables_aeat.xlsx` (Balance/PyG/ECPN para revisión) y
  `agrupado_4d.xlsx` (A3).

## Reglas de oro
1. **El motor firma el número (fail-closed).** Un SyS descuadrado o cuya proyección AEAT no cuadra
   (00180 ≠ 00252) **no emite XML** (`ok:false` + `motivo`). No "ajustes": se corrige el dato de origen.
2. **PII a escala = LOCAL/INTERNO.** El DR y el XML llevan datos reales (NIF, razón, cifras). En Garrigues
   Windows Enterprise, usa el motor local `http://127.0.0.1:8000` gestionado por IT o una URL interna
   `SUITE_IS_ENGINE_URL`. La nube demo no se usa con datos reales. La carpeta de salida es **local y gitignored**;
   los nombres de salida usan **codename**, nunca el NIF (regla 2).
3. **El `.200` es PROVISIONAL.** La AEAT **no publica XSD** de la declaración completa → su validez final la
   confirma la **importación real en Sociedades WEB** (compuerta humana). La codificación por campo sí es oficial.
4. **No inventar.** Hay casillas del 200 que se alimentan/condicionan desde otros modelos o certificados de
   terceros y el export las **avisa** «a cero»; rellénalas desde el origen (`docs/info soporte/ECOSISTEMA_MODELOS_IS.md`).
   **Confirmado:** `202/222 → 00601–00606` (pagos fraccionados; 00601/603/605 Estado, 00602/604/606 forales).
   **Correcciones validadas contra el Manual 2025** (ver `docs/memoria/2026-06-17-revision-manual-procesos.md`):
   `00004` (pág. 12) **NO** es un volcado del 242 — es un **ajuste extracontable art. 15.b LIS** (el gasto del
   Impuesto Complementario no es deducible); el 242 es coherencia, no cifra. `01766/01784` **NO** son IRNR:
   01766 = total general de retenciones soportadas, 01784 = imputadas por AIE/UTE; el **impuesto extranjero
   soportado** va a **00573** (DDI art. 31/32), no a 01766. Dependientes adicionales a vigilar: el bloque de
   retenciones por concepto **01785–01799 + 00597** (certificados de terceros), **00573 + DP200015B** (DDI
   internacional) y **00575** (TFI). 2025 = casillas **provisionales** (= layout 2024).

5. **NUNCA construyas el `.200` a mano.** El `.200` lo emite y FIRMA el motor (`/exportar-aeat` o
   `/expediente/export-base`, ADR-001). Ante un error de importación AEAT (EMALOBL, EMODELOEECC2, E254…) **no
   improvises** un `.200` «in-process» ni rellenes la liquidación con ceros/borrador: eso rompe las identidades
   que el importador RECALCULA (cascada 00501→…→00621) y multiplica los rechazos (incidencia documentada
   2026-06-28). El camino correcto: deja que el motor emita el `.200` **completo** (liquidación base + páginas
   obligatorias) y resuelve los avisos en la skill `gestion-errores-is`.
6. **El modelo de estados contables se decide al inicio del expediente.** Si la ficha confirma `normal`,
   `abreviado` o `pymes`, el motor emite conforme a ese perfil. Para abreviado/PYMES no se manda detalle normal:
   se pliegan las partidas en sus carriers y se recomputan subtotales/totales; el ECPN se omite por defecto si no
   procede. Declarar abreviado con detalle normal provoca «no puede tener contenido».
7. **Foral y SOCIMI son reglas de importabilidad, no atajos fiscales.** Con `00028`, pagina 26 es obligatoria:
   si no hay reparto 2025, el motor puede proponer proxy N-1 con `requiere_revision_humana`. En SOCIMI, el `.200`
   queda importable con cuota 0 cuando procede; modelos 217/237 quedan fuera del alcance del 200.

## Una declaración (verifica primero motor y version)
`curl -s http://127.0.0.1:8000/salud` → `{"ok":true,...}` y
`curl -s http://127.0.0.1:8000/version` → `version >= 1.18.3` (o `SUITE_IS_MIN_ENGINE_VERSION`). Luego:

```bash
curl -s -X POST http://127.0.0.1:8000/exportar-aeat \
  -F "ejercicio=2024" -F "nif=<NIF>" -F "razon_social=<RAZON>" \
  -F 'liquidacion=<JSON {casilla:importe} del cierre firmado, opcional>' \
  -F "fichero=@/ruta/local/SyS_sociedad.xlsx"
```

La respuesta es JSON: `ok`, `validacion.valido_xsd`, `xsd_provisional`, `avisos`,
`casillas_dependientes_de_otros_modelos`, y `ficheros.{xml_mod200,declaracion_dr,...}.base64`. Decodifica
el base64 de `xml_mod200` y `declaracion_dr` y escríbelos en una carpeta local.

- **`liquidacion`** = JSON `{casilla: importe}` de la **liquidación firmada** del cierre. El contable +
  identificativos es **mecánico** (sale del SyS);
  la liquidación (BI/cuota) se añade por expediente desde el cierre. Sin ella, el `.200` sale solo con
  identificativos + contable (el `aviso` lo indica).

## Muchas declaraciones (lote = carpeta de sociedades) — la palanca de escala
El lote es una palanca de escala, no el carril por defecto para casos nuevos. Recomendacion operativa:

- procesa **declaracion a declaracion** si el caso tiene foralidad, SOCIMI, B.1/B.2 relevante, muchos
  administradores/titulares, datos fiscales sensibles, ECPN complejo, perfil abreviado/PYMES dudoso o anexos
  pesados;
- para un grupo nuevo, empieza por la sociedad mas compleja o representativa en individual;
- usa lote cuando el grupo sea homogeneo o cuando una sociedad representativa ya haya pasado OpenWeb;
- incluso en lote, revisa individualmente cada `manifiesto.md`, informe de importabilidad y
  `00_IMPORTAR_OPENWEB_*.200` antes de subir.

Una carpeta con **un SyS por sociedad** → un `.200` + un XML por sociedad + un informe de excepciones:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/suite-is-export-aeat/scripts/lote_export_aeat.py \
  --carpeta /ruta/local/expedientes --ejercicio 2024 --out /ruta/local/_export_aeat_out
```

- **Identificativos + liquidación por sociedad** (opcional): `--map map.csv` con
  `fichero;codename;nif;razon_social;liquidacion` (la última = ruta a un JSON `{casilla:importe}` firmado).
- Salida en `--out` (local): `<codename>_<ej>_mod200.xml`, `<codename>_<ej>_modelo200.200`,
  `<codename>_<ej>_estados_contables_aeat.xlsx`, `<codename>_<ej>_agrupado_4d.xlsx`,
  **`informe_lote.md`** (tabla por sociedad: ok / válido XSD / XLSX emitidos / provisional /
  liquidación / casillas dependientes a 0 / motivo) y `resumen.csv`.
- El script hace health-check de `/salud` y `/version`; aborta si el motor no responde o si es anterior a
  `1.18.3`.
- **Excepciones = trabajo humano:** las sociedades con `ok:false` (SyS a revisar) o con casillas
  dependientes a cero. El resto queda lista para importar. Así "miles, manual" → "automático + HITL solo
  en las excepciones".

## Endpoints del motor que se usan
`/salud` · `/version` · `/exportar-aeat` (este) · `/ingesta-multi` (SyS + mayores con reconciliación inter-fichero,
EPIC B/B5, si hay mayores) · `/campaigns` (versionado por ejercicio). El doble-check del número y la
cadena de casillas: skill `suite-is-motor`.

## Fuentes (repo `is200transmittalApp`)
- `docs/memoria/2026-06-14-fase5-export-aeat.md` — estado real del export AEAT (D20).
- `docs/info soporte/ECOSISTEMA_MODELOS_IS.md` — qué modelo alimenta qué casilla del 200 (verificado).
- `engine_service/engines.py::exportar_aeat` + `engine_service/.../dr200.py` — el motor del `.200`/XML.
- `docs/info soporte/EEDD/` — las XLS oficiales DR de la AEAT (200/202/222/220/232/210/216/242).
