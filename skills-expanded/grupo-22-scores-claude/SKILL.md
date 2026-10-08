# CLAUDE.md — Minijuego "Carrera de Rugby" (G22 Scores)

Convenciones del feature `src/features/career` y de la ruta
`src/app/juegos/minijuegos/carrera-rugby`. Aplican **siempre**, no solo en la
tarea que tengas entre manos.

---

## 1. La regla que no se rompe: el motor es determinista

Toda la simulación sale de una semilla. Una misma semilla + una misma secuencia
de decisiones tiene que producir exactamente la misma carrera, hoy y dentro de
seis meses.

**Dentro de `src/features/career/engine/` está prohibido:**

- `Math.random()`
- `Date.now()`, `new Date()`, `performance.now()`
- Leer `localStorage`, `window`, `navigator` o cualquier cosa del entorno
- Iterar `Object.keys()` / `Set` / `Map` para elegir un elemento sin ordenar antes
  (el orden de inserción es una fuente de no-determinismo encubierta)

**Lo único que se permite** es el PRNG de `engine/random.ts`
(`createRng`, `hashSeed`, `rngFromState` — mulberry32). Si necesitás azar, pedí
un `rng` por parámetro y devolvé el `rng` actualizado. Nunca lo tomes de un
scope superior.

`Math.random()` aparece **una sola vez en todo el proyecto**: en `CareerFlow.tsx`,
para generar la semilla inicial. Ese es el único lugar legítimo.

Cuando elijas entre candidatos, ordenalos de forma estable primero:

```ts
const ordered = [...rung.clubs].sort((a, b) => a.id.localeCompare(b.id));
const club = rng.weighted(ordered, (c) => strongest - c.rating + 4);
```

---

## 2. Persistencia: si tocás el estado, subí la versión

El guardado vive en
`src/app/juegos/minijuegos/carrera-rugby/careerStorage.ts`, bajo la clave
`g22-carrera-rugby`. El payload lleva **siete campos de versión**:

Los valores van **sin transcribir**: acá se documenta la forma, no el número.
Un ejemplo con versiones concretas envejece en el primer commit y después enseña
mal. Cada campo se lee de su constante, que es la única fuente:

```ts
{
  schema: <actual>,                    // SCHEMA en careerStorage.ts
  engineVersion: '<actual>',           // ENGINE_VERSION en types/career.ts
  clubCatalogVersion: '<actual>',      // CLUB_CATALOG_VERSION en data/clubs.ts
  nationsVersion: '<actual>',          // NATIONS_VERSION en data/nations.ts
  competitionLevelsVersion: '<actual>',// COMPETITION_LEVELS_VERSION en data/competition-levels2026.ts
  environmentVersion: '<actual>',      // CAREER_ENVIRONMENT_VERSION en engine/environment.ts
  internationalCalendarVersion: '<actual>', // INTERNATIONAL_CALENDAR_VERSION en data/international-calendar.ts
  savedAt: <timestamp>,
  state: CareerState
}
```

Reglas:

| Si cambiás… | Subí… |
|---|---|
| La forma de `CareerState` (campos nuevos, renombrados, borrados) | `schema` |
| Lógica de simulación que altera resultados con la misma semilla | `engineVersion` |
| `BY_EMPLOYMENT`, `STRUCTURE_BONUS`, `DEVELOPMENT_TRACK` u otra constante de `engine/environment.ts` | `CAREER_ENVIRONMENT_VERSION` |
| El catálogo de clubes | `clubCatalogVersion` |
| Países | `nationsVersion` |
| Niveles de competición | `competitionLevelsVersion` |
| El calendario internacional (torneos, participantes, ediciones, trofeos) | `internationalCalendarVersion` |
| El grafo de ascensos/descensos (`MOVEMENTS`) | `clubCatalogVersion` — es catálogo de competiciones, no lógica |
| El sistema argentino (`arSystem2026.ts`: divisiones, planteles, niveles, cupos del TDI) | `AR_SYSTEM_VERSION` **y** `clubCatalogVersion` |

`AR_SYSTEM_VERSION` no es un octavo campo del guardado: entra dentro de
`NORMALIZED_CATALOG_VERSION`, que ya es compuesta (`catálogo + snapshot SA + canon
AR`). Agregar un campo persistido obligaría a subir `schema` y a migrar, y el dato
que hace falta —"esta partida se jugó con otro sistema argentino"— ya viaja con la
versión de catálogo.

El calendario va **aparte de `engineVersion`** por el mismo motivo que los
niveles de competición: es un catálogo, no lógica. Agregar un torneo o corregir
una lista de participantes no toca una línea del motor, pero cambia cuántos caps
suma una unión por temporada — o sea, invalida una partida en curso igual que un
cambio de reglas. Adentro de `engineVersion` obligaría a subir la versión del
motor cada vez que se toca un dato, y a los tres meses nadie sabría qué cambió.

**Lo DERIVADO no sube nada.** Antes de agregar un campo, fijate si el estado ya
lo contiene: `engine/club-tenure.ts` cuenta las temporadas consecutivas en el
club leyendo `seasons[]`, así que no invalida ninguna partida guardada ni puede
desincronizarse. Un contador guardado sería una segunda fuente de verdad y
alcanzaría un pase que se olvide de resetearlo para que la cabecera mienta.

Un texto de UI tampoco sube nada mientras no se persista. Ojo con cuál: el
`hint` de una opción es presentación pura, pero el `resultText` termina en
`decisionLog[].text` y en `seasons[].decisionText`, así que entra en el
`stateHash` del digest congelado y cambiarlo obliga a actualizar `EXPECTED` en
`determinism.test.ts` y a subir `engineVersion`.

`loadCareer()` devuelve `{ kind: 'none' | 'ok' | 'outdated' }`. **Nunca hagas que
una partida vieja explote**: si no podés migrarla, devolvé `'outdated'` y que la
UI ofrezca empezar de nuevo con un mensaje claro.

El guardado va siempre envuelto en `try/catch` — modo privado y cuota llena son
escenarios reales, y la partida tiene que poder seguir en memoria:

```ts
} catch {
  // Sin acceso a localStorage (modo privado, cuota): la partida sigue en memoria.
}
```

`CareerState` tiene que ser **serializable a JSON puro**. Nada de `Date`, `Map`,
`Set`, funciones ni referencias circulares. Si te tienta guardar un objeto club
entero, guardá el `id` y resolvelo desde el catálogo.

---

## 3. Los eventos son datos, no código

Viven en `src/features/career/data/events/*.ts` agrupados por familia:
`club.ts`, `discipline.ts`, `environment-events.ts`, `injuries.ts`, `media.ts`, `milestones.ts`,
`national-team.ts`, `personal.ts`, `tactical.ts`, y se exportan desde `index.ts`.

Forma canónica:

```ts
{
  id: 'env-semi-pro-offer',          // prefijo de familia + kebab-case, único
  category: 'club',
  title: 'Oferta profesional',
  text: 'Aparece la chance de dar el salto al profesionalismo full-time.',
  weight: 7,                          // probabilidad relativa dentro del pool
  repeatable: true,
  cooldown: 5,                        // temporadas hasta que puede repetirse
  requires: { employment: ['semi-professional'], maxAge: 31 },
  options: [
    {
      id: 'go-pro',
      label: 'Ir por el contrato',
      hint: 'Dedicarte por completo.',
      outcomes: [
        { weight: 3, effect: { … }, resultText: '…' },
        { weight: 1, effect: { … }, resultText: '…' }
      ]
    }
  ]
}
```

Para agregar contenido **no toques el selector**: agregá objetos al archivo de
la familia que corresponda. Si necesitás una precondición que `requires` todavía
no soporta, extendé `requires` y su evaluador en `engine/event-selector.ts`, no
metas un `if` especial para tu evento.

Prefijos vigentes: `env-` (entorno/empleo), `club-`, `per-` (personal),
`mil-` (hitos), `nt-` (selección), `tac-` (táctica), `med-` (medios),
`inj-` (lesiones), `dis-` (disciplina), `vet-` (fin de carrera).

Si agregás una familia, sumá el prefijo acá **y** en `events-shape.test.ts` (que
falla si un id no lo lleva) y en `EventFamily` de `engine/event-selector.ts`.

**Nunca escribas una decisión de una sola opción.** Si el jugador no elige nada,
no es una decisión: es un resultado, y va como tarjeta de resultado con un
"Continuar" visualmente distinto de los botones de decisión.

### 3.1 Los ejes de una decisión

Una decisión se piensa en el idioma del deporte, no en el de los atributos:

| Eje | De dónde sale |
|---|---|
| ⭐ **Valoración** | puntos de OVR: los deltas de atributo pesados por el puesto, más `valoracion` |
| 🕒 **Tiempo de juego** | `playingTime` (escalones), `form`, y lo que te saca de la cancha: lesión y suspensión |
| 🩹 **Lesión** | `forceInjury` / `injuryRisk` |
| 🚫 **Sanción** | `sanction` (tarjeta y partidos) |
| 🌟 **Reputación** | `fame` |

La traducción vive **entera** en `engine/impact.ts` y no se declara a mano: la ⭐
de un efecto es el OVR que ese efecto mueve de verdad en ese puesto (`ovrDeltaOf`,
la misma cuenta que `ovrExact`). Por eso una decisión escrita con atributos habla
el idioma nuevo sin tocarla, y por eso **no puede** prometer una cosa y hacer otra.

Reglas al escribir contenido:

- **La ⭐ de una tarjeta se queda en ±1, ±2 como máximo.** Está medido: con +2 en
  eventos repetibles el jugador llega a su techo dos o tres temporadas antes y la
  meseta del pico se estira. El grueso del crecimiento lo pone la temporada.
- `valoracion` está **acotada por el techo** (`appliedValoracion`): una decisión no
  puede pasar el potencial por arriba. Es un invariante medido
  (`progression-ceiling.test.ts`).
- **Nada de plata.** Si el premio de una decisión es material, se cobra en cancha
  (`statBoost`: tries, tackles). El eje económico del rugby es el escalafón de
  empleo (§5).
- Los modificadores de temporada (`playingTime`, `statBoost`) duran **una**
  temporada y se apagan solos en `simulate-season`.
- **La pantalla muestra dos ejes: ⭐ y 🕒** (`visibleChips`). No es que el resto se
  esconda: la lesión y la sanción son tiempo de juego que se pierde y se cuentan
  ahí; el ánimo, el físico y la reputación viven en el relato del desenlace. El
  color del revelado sí se calcula con el modelo completo, así que una suspensión
  se ilumina en rojo aunque su ficha no esté a la vista.
- **Las probabilidades se muestran.** Cada opción lista sus desenlaces con su
  porcentaje (`optionPreview`, enteros que suman 100). Elegir a ciegas entre dos
  frases no es decidir. Escribí los pesos como se van a leer (70/30, no 7/3).

---

## 4. Voz y escritura

Español rioplatense, voseo, segunda persona. Frases cortas. Sin signos de
exclamación. El tono es de crónica deportiva, no de videojuego.

Bien:

> **Trabajo y entrenamiento**
> El laburo te pisa los horarios de entrenamiento. Algo tenés que resignar.
> · **Priorizar el rugby** — Menos ingresos, más juego.
> · **Cumplir con el trabajo** — Estabilidad.

Mal: *"¡Tomá la decisión más importante de tu carrera!"*, *"Debes elegir"*,
*"tu equipo"* (es *tu club*).

Cada opción lleva un `hint` corto que dice el costo, no solo el beneficio. El
jugador tiene que poder elegir entendiendo qué resigna.

Vocabulario de rugby, no de fútbol: *club* (no equipo), *palos*, *tries*,
*tackles*, *caps*, *seleccionado*, *gira*, *plantel*, *primera*.

---

## 5. Rugby no es fútbol

Al portar ideas del simulador de Copero, respetá las diferencias del deporte:

- **No hay valor de mercado en euros.** El eje económico del rugby es el
  escalafón de empleo (amateur → profesional), no una cifra de traspaso. Nunca
  agregues un "valor" en dinero al jugador.
- **Las estadísticas dependen del puesto.** Apertura → palos. Segunda línea →
  tackles. Wing → tries. Está resuelto en `data/positions.ts`; si agregás una
  estadística, agregala ahí y no en el componente.
- **Los caps valen más que los títulos.** En la jerarquía visual, la selección va
  antes que la vitrina de clubes.
- **La elegibilidad es por residencia, no solo por nacimiento** (`nt-eligibility-switch`).
- **El protocolo de conmoción no se banaliza.** `inj-concussion-protocol` puede
  tener una opción de ocultar el golpe, pero las consecuencias tienen que ser
  serias y estar del lado del riesgo real. No es una decisión "pícara".
- **La ventana del amateur no cruza la frontera.** A un pibe de 18 en un club
  amateur no lo ficha por mercado abierto un club de otro continente: llega allá
  por una VÍA DECLARADA (`TRANSFER_PATHWAYS`) — un convenio, una academia, una
  franquicia que lo scoutea—, con su nivel mínimo. Mientras el vínculo sea amateur
  o compensado, o esté en la academia, la ventana se queda en el país de su club y
  en el suyo de origen (`windowStaysHome` en `engine/club-offers.ts`); se abre sola
  al profesionalizarse.

  Y ojo con el porqué: el síntoma era un sudafricano recibiendo ofertas de la
  Tercera de la URBA, y la causa NO era el peso de cercanía sino el VOLUMEN del
  catálogo (200 clubes argentinos en los escalones bajos le ganan a 12
  sudafricanos por cantidad). Cuando un mercado se desbalancea por volumen, la
  respuesta es una puerta, no un multiplicador más grande: el multiplicador se
  vuelve a quedar corto con el próximo catálogo nacional que entre.

---

## 6. UI

- Next.js App Router + Tailwind. Los componentes del juego viven en
  `src/app/juegos/minijuegos/carrera-rugby/*.tsx`.
- **Un solo `<h1>` por página**, y es el título del juego. El logo de G22 nunca
  es un `h1`.
- Todas las imágenes con `loading="lazy"` salvo la que esté sobre el pliegue.
  Hoy el juego cumple 24 de 24 — no lo rompas.
- Los botones de solo ícono llevan `aria-label`.
- Escudos y banderas siempre con `alt` — vacío si son decorativos junto a un
  texto que ya nombra la entidad, descriptivo si van solos.
- Los grupos de selección (posición, nacionalidad, ruta) usan
  `role="radiogroup"` con `aria-checked`.
- Nada de layouts que dejen una columna vacía: si un panel no tiene contenido
  todavía, que colapse en vez de reservar media pantalla.
- El botón deshabilitado siempre dice qué falta para habilitarse. Ya lo hacemos
  bien en `CreatePlayer.tsx` (*"Elegí una nacionalidad y una posición para
  empezar."*) — mantené ese estándar en cualquier formulario nuevo.

---

## 7. Mapa del feature

```
src/app/juegos/minijuegos/carrera-rugby/
  CareerFlow.tsx          orquestador; único lugar con Math.random (semilla)
  CreatePlayer.tsx        selector de nacionalidad + posición
  CountryPicker.tsx       24 destacados + "Ver más"
  PlayerHeader.tsx        cabecera con OVR, estadísticas y permanencia en el club
  EventCard.tsx           tarjeta de decisión (con las posibilidades de cada opción)
  OutcomeRoll.tsx         revelado del desenlace: números que giran, verde/rojo
  SeasonResultInline.tsx  resultado de temporada
  CareerTimeline.tsx      trayectoria
  RetirementSummary.tsx   pantalla de retiro
  EmploymentLadder.tsx    escalafón de empleo
  ClubBadge.tsx  Flag.tsx  clubCrest.ts
  advanceCareer.ts        avance de temporada
  careerStorage.ts        save / load / clear + versionado

src/features/career/
  engine/     random · run-career · simulate-season · apply-decision · aging
              impact  (los ejes de una decisión: la ÚNICA traducción entre el
                       efecto del motor y lo que lee el jugador)
              season-modifiers  (lo que una decisión le deja a la temporada:
                       tiempo de juego, suspensión, planilla — se apagan al cerrar)
              promotion  (ascenso/descenso: lee el grafo MOVEMENTS y resuelve el
                       club con la división de ESTA carrera)
              environment · event-selector · injuries · national-team
              club-offers · club-tenure · contracts · market-routes
              domestic-system · eligibility · scoring · statistics · headlines
              competition-identity · competition-results · create-player
              archetypes · development-profile
  data/       clubs · countries.generated · nations · positions · origins
              competition-levels2026 · guides · movement-copy
              international-calendar  (fixture de selecciones: de acá sale el
                                       tope de caps por temporada, y de nadie más)
              clubs2026/{saClubs.generated, competitions2026, rosters2026, clubStrength}
              clubs2026/arSystem2026  (CANON del rugby argentino: dos ramas —URBA
                                       e interior—, 28 divisiones, cupos del TDI.
                                       Datos puros, sin dependencias)
              clubs2026/arCatalog     (resuelve el canon a ClubDef heredando del
                                       snapshot el sourceId con el que se pide el
                                       ESCUDO; reporta lo que no pudo resolver)
              events/{club, discipline, environment-events, injuries, media,
                      milestones, national-team, personal, tactical, veteran, index}
  state/      career-reducer · career-actions
  types/      career · season
```

Regla de dependencia: `app/**` puede importar de `features/career/**`.
**`features/career/engine/**` no importa nada de `app/**` ni de React.** El motor
tiene que poder correr en un test de Node sin DOM.

---

## 8. Antes de dar algo por terminado

1. `npm run build` y `npx tsc --noEmit` sin errores nuevos.
2. Jugá **una carrera completa** de punta a punta en el navegador.
3. **Probá la recarga**: a mitad de carrera, F5, y verificá que retoma idéntico.
4. Si tocaste el motor, verificá el determinismo: misma semilla y mismas
   decisiones → mismo resultado.
5. Consola sin errores ni warnings nuevos.
6. Si cambiaste el estado, probá que una partida guardada con el esquema anterior
   se resuelve como `'outdated'` y no revienta.

No marques una tarea como completa si algo de esto falla.

## graphify

El proyecto tiene un grafo de conocimiento en `graphify-out/`: nodos hub,
comunidades y relaciones entre archivos, extraídos del AST. Es **derivado** —
no se versiona (está en `.gitignore`) y se reconstruye cuando haga falta.

Reglas:

- Para preguntas sobre el código, primero `graphify query "<pregunta>"`.
  `graphify path "<A>" "<B>"` para ver cómo se conectan dos cosas y
  `graphify explain "<concepto>"` para uno solo. Devuelven un subgrafo acotado,
  casi siempre mucho más chico que `GRAPH_REPORT.md` o que un grep a mano.
- `graphify-out/wiki/index.md` sirve para navegar de arriba hacia abajo cuando no
  sabés todavía qué preguntar. `graphify-out/GRAPH_REPORT.md` es para revisión
  amplia de arquitectura, no para una pregunta puntual.
- El vault de Obsidian vive **fuera del repo**, en
  `~/OneDrive/Documentos/________S22/OBSIDIAN/G22 Scores` — una nota por nodo con
  `[[wikilinks]]`, más `graph.canvas`. Se entra por `HOME.md`.
- Después de tocar código, `graphify update .` deja el grafo al día (solo AST,
  sin costo de API).

El grafo se armó con `--code-only`: entra el código (TS/TSX/JS/PY/SQL/CSS), no
los `.md` ni las imágenes. Sumarlos pide un backend LLM
(`graphify extract . --backend claude-cli`).
