---
name: investigacion-mercado
description: Como investiga el equipo de Marketing el mercado, la competencia y las tendencias sin inventar nada - jerarquia de fuentes (reguladores y estadistica oficial de Chile, Peru y Colombia, multilaterales, gremios, consultoras con metodologia, prensa economica, sitios de competidores como autodeclaracion, redes solo como senal), como buscar con WebSearch y verificar en la fuente original con WebFetch, el registro de fuentes con F-ID, URL, fecha de publicacion y de consulta, tipo y confianza, como citar en piezas (nota corta y anexo), cruce de cifras clave, estimaciones propias con formula y supuestos, benchmark por parte (tiene, parcial, no publica, nunca no tiene sin prueba), que es tendencia vs moda vs senal, la base .marketing/tendencias con vigencia, y la etica (solo informacion publica, sin datos personales, competidores con respeto). Cargala antes de investigar o de usar una cifra en una pieza.
---

# Investigacion de mercado — con fuente, fecha y criterio

## 1. Jerarquia de fuentes (de mas a menos confiable)
| Nivel | Tipo | Ejemplos (FAAST: CL, PE, CO, LATAM) | Uso |
|---|---|---|---|
| 1 | Regulador / estadistica oficial | CMF y SII (Chile); SBS y SUNAT (Peru); Superintendencia Financiera y DIAN (Colombia); bancos centrales; registros de factura electronica y cesion | dato `oficial` |
| 2 | Multilaterales | IFC, Banco Mundial, BID, CEPAL, OCDE | dato `tercero`, alta confianza |
| 3 | Gremios | asociaciones de factoring, de fintech, camaras de comercio | `tercero`, revisar sesgo |
| 4 | Consultoras / research con metodologia | informes de mercado con muestra y metodo declarados | `tercero`; anotar si es estimacion |
| 5 | Prensa economica seria | Diario Financiero, Pulso, Gestion, El Comercio, Portafolio, La Republica, Bloomberg Linea | `tercero`; ir a la fuente que cita |
| 6 | Sitio del competidor / de FAAST | paginas de producto, notas de prensa propias | `autodeclarado` — solo para lo que dicen de si mismos |
| 7 | Blogs, LinkedIn, redes, foros | posts, opiniones | `senal`; nunca dato en una pieza |

Regla: si una fuente cita a otra, se va a la original. Un numero de un agregador o de una IA no es
fuente.

## 2. Como buscar y verificar
1. Pregunta concreta y util para una ficha o lamina ("¿cuanto tarda hoy aprobar una operacion de
   factoring en una financiera mediana en Chile?").
2. WebSearch en español e ingles, por pais y año; `mode: extended` solo para panoramas complejos.
3. WebFetch de la fuente: extraer la frase textual, el valor, la unidad, el año del dato (no solo de
   la publicacion), el pais y la metodologia.
4. Registrar en `investigacion/fuentes.md` (F-ID).
5. Cruzar con una segunda fuente independiente o marcar `fuente unica`.

## 3. Registro de fuentes (obligatorio)
```markdown
| ID | Afirmacion | Valor | Unidad | Pais | Año del dato | Fuente | URL | Publicado | Consultado | Tipo | Confianza |
```
Tipos: `oficial` · `tercero` · `autodeclarado` · `estimacion-propia` · `supuesto`. Confianza:
alta (oficial o 2 fuentes concordantes) · media (1 fuente seria) · baja (autodeclarado, antiguo,
metodologia dudosa). Datos de mas de 24 meses: marcar `antiguo` y buscar uno mas reciente.

## 4. Como se cita en las piezas
- **Deck**: nota al pie corta `Fuente: CMF, 2025 [F003]` o superindice `[3]` → anexo con la tabla.
- **Video**: cartela breve en el cierre o subtitulo ("Fuente: ... 2025"); anexo en la descripcion.
- **Impreso**: nota al pie de 7-8 pt.
- **Supuestos**: siempre visibles como tales: "estimacion sobre 800 operaciones/mes; supuestos en
  anexo [S1-S2]".
- Autodeclaraciones: "segun {empresa}" con fecha de consulta.

## 5. Estimaciones propias
Cuando no hay dato publico: formula a la vista, cada insumo con su F-ID o `SUPUESTO` y su origen,
rango conservador/esperado, y una frase de como validarla con el cliente. Nunca se presenta como
dato de mercado.

## 6. Benchmark por parte
- Una matriz por parte del mapa + una general.
- Estados: `✔` (documentado), `parcial` (con detalle), `✗` (documentado que NO), `sin info publica a
  {fecha}`. **"No publica" no es "no tiene"**: una ✗ requiere documento.
- Columna "alternativa actual" (planilla, desarrollo propio, sistema legado): suele ser el
  competidor real.
- Lectura honesta: donde FAAST gana, empata y pierde. Un benchmark que siempre gana no es creible.
- Competidores: se nombran con precision y respeto; logos de terceros en piezas solo con decision
  del director, nunca como propios.

## 7. Tendencia, moda o senal
| | Tendencia | Moda | Senal |
|---|---|---|---|
| Evidencia | multiples fuentes independientes, sostenida ≥ 2 trimestres | mucha visibilidad, poca sustancia | 1-2 fuentes, temprana |
| Efecto | cambia decisiones de compra o regulacion | cambia la estetica o el tema de conversacion | podria convertirse en tendencia |
| Uso | argumento del "por que ahora" | con cuidado y fecha corta (estetica de una pieza) | se vigila, no se afirma |
| Vigencia por defecto | 90 dias (mercado, producto, diseño); 180 dias regulacion | 30-60 dias | 60 dias, revisar |

Ejemplos de ambito: regulacion de factura electronica y cesion, open finance, IA aplicada a riesgo
y cobranza, pagos instantaneos, embedded finance; y lenguaje visual (lanzamientos de Apple,
automotriz de lujo, decks SaaS recientes) como guia de estilo con fecha.

## 8. Base de tendencias `.marketing/tendencias/`
- Archivo por tendencia desde `templates/tendencias/tendencia.md` (frontmatter con `tipo`, `ambito`,
  `detectada`, `vigente_hasta`, `fuentes`, `aplica_a`).
- `INDEX.md` con vigentes, vencidas y archivadas. El hook de sesion avisa cuantas estan vencidas.
- Refresco (`/marketing:tendencias`): renovar con evidencia NUEVA, archivar en `tendencias/archivo/`,
  o reclasificar (una moda que se sostuvo pasa a tendencia). Se puede programar semanal con
  `/schedule`.

## 9. Etica
Solo informacion publica. Nada detras de login ajeno, nada filtrado, nada de datos personales, nada
de suplantar a un cliente para obtener informacion de un competidor. Lo que el equipo sabe por la
Mesa o por clientes es interno y no aparece en piezas sin autorizacion.

## 10. Confiabilidad: dos notas por dato
| Fuente | | Informacion | |
|---|---|---|---|
| A | oficial / regulador / estadistica | 1 | confirmada por otra fuente independiente |
| B | multilateral o gremio con metodo | 2 | probable (seria, sin cruce) |
| C | consultora con metodo declarado | 3 | posible (antigua o metodo poco claro) |
| D | prensa economica seria | 4 | dudosa (contradice otras) |
| E | autodeclaracion de una empresa | 5 | improbable |
| F | blogs, redes, foros | 6 | no evaluable |
A pieza externa: A-C con 1-2; D/E solo citadas como tales ("segun {medio}", "segun {empresa}").

## 11. Dimensionar: TAM / SAM / SOM
- **TAM**: todas las entidades que podrian usar un core de factoring/confirming/ordering en los paises.
- **SAM**: las que FAAST puede servir hoy (pais con integracion operativa, tipo y tamaño de entidad).
- **SOM**: la porcion realista en 12-36 meses (supuesto comercial declarado).
- **Top-down**: entidades del registro oficial o gremio × % con el perfil × (valor por cliente solo si
  comercial lo entrego; si no, en numero de entidades).
- **Bottom-up**: lista de entidades identificadas una a una × probabilidad.
- Se presentan ambos con formula y supuestos; la diferencia se explica.
Ejemplo de tabla:
```markdown
| Nivel | Definicion | Calculo | Resultado | Fuentes / supuestos |
| TAM | entidades con factoring/confirming en CL, PE, CO | n_CL + n_PE + n_CO | {n} | [F010][F011][F012] |
| SAM | perfil core SaaS | TAM × 0,6 | {n} | S3 (validar) |
| SOM | obtenible en 24 meses | SAM × 0,05 | {n} | S4 (comercial) |
```

## 12. Protocolo de benchmark ponderado
1. Criterios observables derivados de cada parte (2-4 por parte).
2. Pesos acordados con el estratega ANTES de puntuar (suman 100).
3. Escala: 2 completo · 1 parcial · 0 documentado que no · s/i sin informacion (se excluye, no es 0).
4. Puntaje normalizado por cobertura; se muestra "puntaje / cobertura".
5. Lectura honesta: gana, empata, pierde; la alternativa actual del cliente siempre como columna.
```markdown
| Criterio (peso) | FAAST | A | B | Alternativa actual |
| Aprobacion en un flujo (25) | 2 | 1 [F040] | s/i | 0 [F003] |
| Riesgo en la decision (25) | 2 | 2 [F041] | 1 [F042] | 0 |
| Puntaje / cobertura | 100 / 100% | 75 / 100% | 50 / 50% | 0 / 100% |
```

## 13. Vigilancia de tendencias (operativa)
- **Cadencia**: semanal o quincenal (`/marketing:tendencias refrescar`, programable con `/schedule`) +
  barrido antes de cada campana.
- **Lista de vigilancia**: reguladores y entes tributarios de CL/PE/CO, gremios, IFC/BID, prensa
  economica, notas de prensa de competidores; para estilo, lanzamientos recientes de producto premium.
- **Radar** en `INDEX.md`: `adoptar` · `probar` · `vigilar` · `descartar`, por ambito.
- **Regla de renovacion**: solo con evidencia nueva (fecha posterior a la ultima fuente).

## 14. Costear un problema (para la §2 de las fichas)
Unidad del problema → dato de mercado (A-D) o estimacion propia con insumos verificables → por periodo y
volumen de referencia declarado → rango y sensibilidad → al estratega.

## 15. Checklist de la investigacion
- [ ] Plan con preguntas utiles a fichas o laminas concretas.
- [ ] Cada dato con F-ID, URL, publicado, consultado, tipo y confiabilidad.
- [ ] Cifras clave cruzadas o `fuente unica`; monedas, años y unidades explicitos.
- [ ] Benchmark con pesos previos, escala, cobertura y lectura honesta.
- [ ] Tendencias con tipo, vigencia y anillo del radar.
- [ ] Conclusion arriba; vacios declarados.

## 16. Donde empezar a buscar, por pais (verificar vigencia)
| Pais | Regulador | Ente tributario / factura | Otros |
|---|---|---|---|
| Chile | CMF | SII (factura electronica, registro de cesiones) | Banco Central, gremios de factoring, CORFO |
| Peru | SBS | SUNAT (factura negociable), CAVALI | BCRP, PRODUCE |
| Colombia | Superintendencia Financiera | DIAN (RADIAN, factura como titulo valor) | Banco de la Republica, gremios |
| LATAM | — | — | IFC, BID, Banco Mundial, CEPAL, Factors Chain International |

## 17. Perfil de competidor (plantilla)
```markdown
# {Competidor} — corte {AAAA-MM-DD}
| Dato | Valor | Fuente | Conf. |
| Que vende | ... | [F030] | E2 |
| Paises | ... | [F030] | E2 |
| Clientes publicos | los que el mismo publica | [F031] | E2 |
| Señales recientes | ronda / alianza / lanzamiento con fecha | [F032] | D2 |
Capacidades por parte: ver benchmark.md · No verificable: {...}
```
