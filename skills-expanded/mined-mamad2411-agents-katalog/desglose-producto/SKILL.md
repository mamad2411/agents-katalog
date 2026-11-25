---
name: desglose-producto
description: Metodo del equipo de Marketing para desglosar un producto PARTE POR PARTE antes de producir cualquier pieza - por que una presentacion generica no vende, como se arma el MAPA DEL PRODUCTO (4 a 10 partes entre modulos, capacidades y mejoras, con nombre de negocio orientado a resultado, estado real disponible / en construccion / hoja de ruta, evidencia y publico), de que fuentes reales sale (wiki, backlog, arquitectura y diseño del dev-team en .coordination, solicitudes y maquetas de la Mesa en .mesa, producto en demo capturado con Playwright MCP), la FICHA por parte con sus 6 preguntas (que es y para quien, problema y su costo, como funciona paso a paso con pantallas reales, que gana el cliente en numeros con fuente, antes/despues, benchmark) mas limites honestos y aptitud para pieza externa, la doble aprobacion del usuario (mapa y fichas), y como cada pieza hereda el desglose (deck por secciones, video por capitulos y clips, one-pager y panfletos por parte). Cargala al iniciar cualquier campana o propuesta.
---

# Desglose del producto — el producto parte por parte

## Por que existe esta regla
Una presentacion generica ("FAAST es una plataforma integral que potencia tu negocio") se ve
horrible y no vende: no dice que hace, no prueba nada y podria ser de cualquier empresa. Un
ejecutivo compra resultados concretos y quiere ver COMO se logran. Por eso el producto se
presenta como un lanzamiento de Apple o de un hiperdeportivo: **parte por parte**, cada una con su
momento, su imagen, su prueba y su cifra. El desglose es el primer entregable obligatorio de toda
campana; sin el aprobado, no se produce ninguna pieza.

## 1. Fuentes reales (en este orden)
| Fuente | Ruta tipica | Que aporta | Prueba de estado |
|---|---|---|---|
| Wiki del dev-team | `{proyecto}/.coordination/wiki/` (indice primero) | servicios, HUs, decisiones, modelo actual vs objetivo | paginas de servicio y HUs hechas |
| Backlog y sprint | `.coordination/backlog.md`, `sprint-actual.md` | que esta Hecho / En QA / En progreso / Backlog | estado del item en el tracker |
| Arquitectura | `.coordination/arquitectura/` o `architecture.md` | capacidades por servicio, vision | — |
| Diseño | `.coordination/design/DSN-*/` | propuesta aprobada, prototipo navegable, capturas, DESIGN.md | aprobacion registrada |
| Evidencia QA | `.coordination/evidence/` | capturas/videos de lo que ya funciona | veredicto APROBADA |
| Mesa de Servicios | `.mesa/solicitudes/`, documentos PRY/CTZ, `prototipo/` | dolores de clientes en sus palabras, maquetas | — |
| Producto desplegado | `config.json` → `ambientes.demo` | pantallas reales | captura con fecha |
| Usuario | — | lo que no esta en ninguna fuente | su respuesta registrada |

Lo que no esta en ninguna fuente se pregunta. Nunca se deduce "deberia tener X".

## 2. El MAPA DEL PRODUCTO
**Que es una "parte"**: una unidad que un ejecutivo entiende como un resultado propio. Puede ser un
modulo (Confirming), una capacidad transversal (entrar seguro con la cuenta de la empresa), o una
mejora (aprobar en un solo flujo lo que antes eran tres pantallas).

**Reglas del mapa**
- 4 a 10 partes. Menos de 4: el producto se ve chico o el corte es grueso. Mas de 10: es una lista
  de funciones; agrupar.
- **Nombre de negocio orientado a resultado**: "Aprobar en minutos", "Ver el riesgo antes de girar",
  "Una empresa, muchas marcas", "Entrar seguro sin claves que olvidar". Prohibidos los nombres de
  servicios tecnicos ("Identidad y acceso", "Core API", "Notificaciones", "BFF").
- **Estado real**: `disponible` (evidencia: produccion/demo/QA aprobada), `en construccion` (HU en
  sprint o backlog priorizado), `hoja de ruta` (decidido, sin construir). `idea` no entra al mapa.
- **Evidencia** por parte (ruta, issue, captura).
- **Publico** al que mas le importa y **apto para pieza externa** (si/no/parcial).
- **Orden** propuesto por impacto para el publico de la campana (lo afina el estratega).

Plantilla: `templates/desglose/mapa-producto.md`. Ejemplo de fila:
`| P03 | Una empresa, muchas marcas | Cada cliente opera con su logo y sus colores sin desarrollo | en construccion | prototipo DSN-001 | backlog #187, DSN-002 | gerente comercial | si |`

**Aprobacion 1**: el usuario aprueba el mapa (partes, nombres, orden) antes de escribir fichas.

## 3. La FICHA por parte
Plantilla: `templates/desglose/ficha-parte.md`. Archivo `desglose/fichas/P{NN}-{slug}.md`.

| § | Pregunta | Regla de calidad |
|---|---|---|
| 1 | Que es y para quien | 2 frases; perfil concreto (cargo) y momento de uso |
| 2 | Que problema resuelve hoy y cuanto cuesta | el costo con F-ID (investigacion) o `SUPUESTO` con calculo; en tiempo, dinero, riesgo o clientes perdidos |
| 3 | Como funciona, paso a paso | 3-6 pasos con verbo de negocio; cada paso con su pantalla real (ruta) y su origen (demo/prototipo/maqueta + fecha) |
| 4 | Que gana el cliente, en numeros | metrica de negocio, antes → despues, formula y supuestos, rango conservador/esperado (lo escribe el estratega) |
| 5 | Antes / despues | tabla: pasos, sistemas, personas, tiempo, errores; el "antes" con fuente |
| 6 | Frente a la competencia | benchmark de esa parte (investigador): tiene / parcial / no publica, con fuente y fecha |
| 7 | Limites honestos | que no hace todavia, que requiere (integracion, configuracion, datos del cliente) |
| 8 | Apto para pieza externa | que se puede mostrar, que no (nombres, cifras internas, IDs) |

**Checklist de la ficha** (todas ✔ para presentarla):
- [ ] Las 8 secciones completas o con `PENDIENTE` explicito y a quien se le pregunta.
- [ ] Ningun numero sin F-ID o `SUPUESTO`.
- [ ] Ningun paso sin pantalla real (o prototipo/maqueta rotulado) con origen.
- [ ] El estado coincide con la evidencia; nada `en construccion` en presente.
- [ ] Lenguaje de negocio; un CEO la entiende sin glosario.

**Aprobacion 2**: el usuario aprueba las fichas (puede ser por lotes). Recien ahi se produce.

## 4. Pantallas reales: como se consiguen
1. Producto en ambiente demo/pruebas con datos ficticios → Playwright MCP (`browser_resize`
   1920x1080, `browser_navigate`, `browser_wait_for`, `browser_take_screenshot`).
2. Prototipo navegable del dev-team (`DSN-*/0X-prototipo/index.html`) → mismo metodo, rotulo
   "Prototipo".
3. Maqueta wireframe de la Mesa (`.mesa/.../prototipo/maqueta.html`) → rotulo "Concepto".
4. Nada de lo anterior → la parte va como hoja de ruta, sin pantalla. **Jamas se dibuja una pantalla
   imaginada** ni se usa un mockup generico de dashboard.
Registro: `desglose/capturas/ORIGEN.md` → `| archivo | parte | paso | origen | URL/ruta | fecha | datos ficticios: si |`.

## 5. Como cada pieza hereda el desglose
| Pieza | Estructura obligatoria |
|---|---|
| Deck | apertura + contexto de mercado → **una seccion por parte** (portada con imagen principal, detalle, como funciona, resultado) → benchmark general → hoja de ruta → cierre con la propuesta → anexo de fuentes |
| Video keynote | apertura → contexto → **un capitulo por parte** (gancho, revelacion, como funciona, resultado) → hoja de ruta → cierre de marca |
| Clips | **un clip de 6-15 s por parte**, autonomo (y pieza extendida de 30-45 s por parte si se pide) |
| One-pager | titular + **un bloque por parte** (mini-captura, nombre, 1 linea, cifra con nota) + llamado |
| Panfleto | **una parte** por panfleto, cuando la parte lo merece |
| Redes | una parte por pieza o por lamina de carrusel |

## 6. Anti-patrones que este metodo evita
- "Lamina de beneficios" suelta → cada beneficio vive en el resultado de su parte.
- "Arquitectura para el CEO" → la arquitectura es interna; el CEO ve partes y resultados.
- "Todo es nuevo" → el estado real se muestra; la hoja de ruta tambien vende si es honesta.
- "Feature dump" de 25 items → agrupar en 4-10 partes.
- "Pantalla bonita inventada" → captura real, prototipo rotulado o nada.

## 7. Metodo de lectura por fuente (resumen operativo)
| Fuente | Que buscar | Como se convierte en desglose |
|---|---|---|
| HU (titulo + Gherkin) | el titulo de negocio; cada "Entonces" verificable | nombre candidato de la parte; pasos de "como funciona" (solo si la HU esta Hecha y aprobada por QA) |
| Epica / fase | agrupacion de capacidades; milestone | candidato a parte; hoja de ruta (sin fechas no confirmadas) |
| Wiki `current-model/` | como se hace hoy (legado) | el "antes" de la ficha |
| Wiki `target-model/` / servicios | capacidades nuevas | partes y limites |
| Decisiones | lo descartado o postergado | limites honestos / hoja de ruta |
| DSN-* brief y propuesta | el problema de diseño y la direccion aprobada | §2 problema; pantallas de prototipo rotuladas |
| Evidencia QA | capturas con veredicto APROBADA | prueba de `disponible` |
| Mesa de Servicios | frases textuales de clientes, frecuencia | §2 en palabras del cliente (interno) |
| Demo | el flujo real de punta a punta | §3 con capturas; medicion de tiempos (F-DEMO-xx) |

## 8. Agrupar por trabajo del cliente (JTBD)
Para cada capacidad del inventario se escribe el trabajo que hace el cliente con ella ("aprobar sin perder
al cliente", "saber a quien no girar", "operar con mi marca"). Las capacidades que sirven al mismo
trabajo forman UNA parte. Asi el mapa queda en el idioma del comprador y no en el de la arquitectura.

## 9. Test del nombre (cada parte)
1. ¿Empieza con un verbo o un resultado? ("Aprobar en minutos" ✔ · "Motor de aprobaciones" ✗)
2. ¿Un CEO entiende que gana solo con leerlo?
3. ¿Podria ser el nombre de una funcion de cualquier software? (si si, es generico → reescribir)
4. ¿Cabe en ≤ 6 palabras?

## 10. Matriz de trazabilidad
Toda afirmacion que llegara a una pieza tiene fila en `desglose/trazabilidad.md`:
`| # | Afirmacion (como se dira) | Parte | Fuente primaria | Verificacion | Estado | Apta externa |`.
Estados: ✔ verificada (fuente + recorrido en demo o QA) · en construccion · ✗ sin verificar. Una parte
`disponible` no puede tener afirmaciones ✗; las ✗ se preguntan al usuario antes de usarse.

## 11. Ejemplo ilustrativo de mapa (formato; los contenidos reales salen de las fuentes)
| ID | Parte | Valor en una linea | Tipo | Estado | Pantalla | Evidencia |
|---|---|---|---|---|---|---|
| P01 | Aprobar en minutos | Evaluar, decidir y girar en un solo flujo | capacidad | disponible | demo | HU Hecha + QA |
| P02 | Ver el riesgo antes de girar | Alertas del deudor en la decision | capacidad | disponible | demo | wiki + QA |
| P03 | Una plataforma, muchas marcas | Cada empresa con su logo y colores | capacidad | en construccion | prototipo DSN | issue en backlog |
| P04 | Entrar seguro, sin claves que olvidar | Cuenta de la empresa + segundo factor | capacidad | disponible | demo | QA de acceso |
| P05 | Cumplir sin planillas | Integracion con el ente tributario | modulo | {por pais} | demo | {por verificar} |
Orden para CEO: P01 → P02 → P04 → P05 → P03 (crecimiento → riesgo → seguridad → cumplimiento → lo que viene).

## 12. Como se presenta para aprobar
- **Mapa**: la tabla + orden propuesto con su porque + afirmaciones sin verificar + "¿apruebas, quitas,
  unes, renombras o reordenas?".
- **Fichas**: una linea por ficha (parte · que gana · cifra y tipo de fuente · pantallas · pendientes) +
  rutas. Aprobacion por lote o por ficha, registrada textual en `aprobaciones.md`.

## 13. Actualizar el desglose
Cuando el producto avanza: comparar mapa vs backlog/sprint/evidencia, proponer cambios de estado con su
evidencia y capturas nuevas, versionar la ficha (`v2`) y marcar las piezas afectadas para nueva version.
Nunca se reescribe en silencio una ficha aprobada.

## 14. Escenarios
- **Backlog dice Hecho pero la demo falla** → no es `disponible` hasta confirmarlo.
- **No hay demo** → prototipos y evidencia QA rotulados; lo invisible va a hoja de ruta.
- **El usuario quiere vender algo del backlog** → se vende como hoja de ruta, con su fase.
- **Producto enorme** → el mapa elige las partes que importan a ESTE publico; el resto al anexo.
- **Una parte existe solo en un pais** → se dice el pais en la ficha y en la pieza.

## 15. Checklist del desglose completo
- [ ] Inventario con fuente por fila; mapa de 4-10 partes que pasan el test del nombre.
- [ ] Estados con evidencia; trazabilidad sin ✗ en partes disponibles.
- [ ] Fichas con las 8 secciones (o pendientes explicitos); capturas reales con origen.
- [ ] Mapa y fichas aprobados y registrados en `aprobaciones.md`.
