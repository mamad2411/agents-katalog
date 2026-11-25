---
name: edge-case-data-catalog
description: Catálogo reutilizable de casos límite y adversos por tipo de dato — strings (vacío, whitespace, unicode, emoji, RTL, muy largo, con inyección), números (0, negativos, límites, decimales, overflow), fechas (borde de mes/año, bisiesto, zona horaria, DST), colecciones (vacía, uno, muchísimos), nulos/ausentes, dinero (redondeo, monedas) e identidad (duplicados, mayúsculas, unicode equivalente). Usar al diseñar casos de un endpoint, formulario o función, al escribir tests negativos, o al preguntarse "¿qué le meto para romperlo?".
---

<!-- ESPEJO GENERADO por AtlasPromptManager/tools/install_skills.py - NO EDITAR A MANO -->
<!-- La fuente es AtlasPromptManager/.claude/skills/. Lo que edites aca se pierde. -->

# Catálogo de casos límite

Tabla de referencia para no depender de la memoria al diseñar entradas. Los bugs viven en los
bordes, no en el camino feliz. Combiná esto con `test-case-design-techniques` (cómo elegir qué
combinar) y `synthetic-test-data-generation` (cómo producirlo). Para inyecciones con intención de
seguridad, el objetivo es *verificar el control*, no explotar: ver `security-testing`.

## Cómo usar el catálogo
Para cada campo de entrada, recorré su tipo y elegí los casos aplicables. Por cada caso decidí el
**comportamiento esperado** (aceptar / rechazar con qué error / normalizar) ANTES de correr el test.
Un caso sin comportamiento esperado no es un test, es una curiosidad.

## Strings
| Caso | Por qué |
|---|---|
| `""` vacío | ¿requerido? ¿lo distingue de ausente? |
| solo espacios / tabs / `\n` | trim; no debería pasar como "con contenido" |
| espacios al inicio/fin | normalización consistente |
| unicode: acentos, `ñ`, `ü` | encoding, comparación, longitud en bytes vs caracteres |
| emoji y pares subrogados | conteo de longitud, truncado que parte un carácter |
| RTL (árabe/hebreo) y bidi | render y almacenamiento |
| homoglifos / unicode equivalente (NFC vs NFD) | "café" en dos formas ≠ como bytes |
| muy largo (10k+) | límites de columna, truncado, DoS de UI |
| con `'`, `"`, `<`, `>`, `;`, `--`, `{{}}` | verificar codificación de salida y parametrización |
| solo dígitos en campo de texto | no confundir con número |

## Números
- `0`, `-0`, negativos donde se espera positivo.
- Límite exacto y límite ± 1 (si el máximo es 100: 99, 100, 101).
- Decimales donde se espera entero; muchísimos decimales (precisión).
- Muy grande / muy chico: overflow, `Number.MAX_SAFE_INTEGER`, notación científica.
- `NaN`, `Infinity`, string numérico con espacios o `+`.
- Coma vs punto decimal según locale.

## Dinero (nunca `float`)
- Redondeo (0.005), fracciones de centavo, monedas distintas mezcladas.
- Negativos (reintegros), cero, montos enormes.
- Representación entera en la unidad mínima (centavos) para evitar error de coma flotante.

## Fechas y horas
- Fin de mes, 29/02 en bisiesto y no bisiesto, 31 en meses de 30.
- Cambios de zona horaria y horario de verano (DST): horas que no existen o existen dos veces.
- Pasado lejano y futuro lejano; fecha anterior a otra que debería ser posterior.
- Medianoche, límites de día en UTC vs local.
- Formato ambiguo (dd/mm vs mm/dd); guardá siempre en UTC (ver `database-design`).

## Colecciones / paginación
- Vacía, exactamente uno, exactamente el tamaño de página, tamaño+1, muchísimos.
- Orden inestable (empates), duplicados, nulos dentro de la lista.
- Cursor inválido, vencido o de otro tenant (ver paginación en `api-testing`).

## Nulos y ausencia
- `null` explícito vs campo ausente vs `""` vs `undefined`: tres cosas distintas.
- Campos opcionales omitidos; objetos anidados parcialmente presentes.
- Mass assignment: campos extra que no deberían aceptarse (ver `authz-access-control`).

## Identidad y unicidad
- Mismo valor con distinta capitalización (`ANA@x.com` vs `ana@x.com`).
- Duplicado exacto; duplicado tras normalizar (espacios, unicode).
- Concurrencia: dos altas con el mismo `unique` a la vez (ver `concurrency-and-locking`).

## Archivos (si aplica)
- Tamaño 0, enorme, extensión que no coincide con el contenido, nombre con unicode/`../`,
  MIME falso. El control esperado vive en `file-uploads-media`.

## Anti-patrones
- Probar solo el camino feliz y declarar "funciona".
- Meter un caso raro sin definir qué se espera que pase.
- Asumir que el frontend ya filtró: el backend valida igual (ver `security-guardrails`).

## Checklist
- [ ] Cada campo recorrió los casos de su tipo.
- [ ] Cada caso tiene comportamiento esperado definido antes de correr.
- [ ] Strings: vacío, whitespace, unicode, largo y con caracteres especiales cubiertos.
- [ ] Fechas: bordes de mes/año, bisiesto y zona horaria cubiertos.
- [ ] Colecciones: vacía, uno y muchos cubiertos.
- [ ] Casos de unicidad y concurrencia considerados donde hay `unique`.
