---
name: ingenieria-faast
description: Estandar de ingenieria compartido de los devs de dev-team (backend, frontend, dba, infra) para una fintech regulada (FAAST - factoring y confirming en Chile, Peru y Colombia). Metodo paso a paso (entender, planear, prueba primero, implementar, auto-revisar el diff, verificar, entregar), Definicion de Terminado, checklist de auto-revision e informe de entrega; reglas fintech (montos decimal, moneda y redondeo CLP/PEN/COP/USD/UF, idempotencia de giros/pagos/desembolsos, concurrencia optimista, outbox, auditoria, zonas horarias por pais, RUT/DNI/RUC/NIT redactados); API y observabilidad (RFC 9457, validacion en el borde, paginacion, versionado, timeouts/reintentos/circuit breaker, OpenTelemetry, logs sin secretos, health); pruebas por capa (unit, integracion con BD real/Testcontainers, contrato, e2e); BD y migraciones expand/contract; frontend (locale, WCAG 2.2 AA, seguridad, Core Web Vitals); stacks 2026 y revision de PR. Cargala antes de implementar, corregir, revisar o entregar codigo.
---

# Estandar de ingenieria FAAST (dev-team)

Este es el piso profesional comun de `backend`, `frontend`, `dba` e `infra`. El agente trae
su oficio; esta skill trae lo que es igual para todos y lo que es propio de una fintech
regulada. Se carga bajo demanda: lee aqui el resumen y abre la referencia del tema que
estas tocando.

| Tema | Referencia | Quien la usa sobre todo |
|---|---|---|
| Reglas fintech (dinero, moneda, idempotencia, concurrencia, auditoria, fechas, PII) | `references/fintech.md` | backend, dba, frontend |
| API, errores, resiliencia, observabilidad | `references/api-observabilidad.md` | backend, frontend (consumo), infra |
| Estrategia de pruebas por capa y por stack | `references/pruebas.md` | todos |
| Datos y BD: modelo, indices, bloqueos, migraciones expand/contract, backups | `references/datos-y-bd.md` | dba, backend |
| Frontend: formularios, locale, accesibilidad, seguridad, rendimiento | `references/frontend.md` | frontend |
| Stacks vigentes 2026 y como tratarlos en repos legados | `references/stacks-2026.md` | todos |
| Revision de PR y auto-revision del diff | `references/revision-pr.md` | todos, lead |

Skills hermanas del plugin (no se duplican aqui): `crear-tests-backend` (suite .NET desde
cero, caracterizacion), `migrar-dotnet` (subir de TFM), `scalar-api-docs` (UI de OpenAPI),
`dockerizar-componente` + `deployment-standard` (contenedor y despliegue), `visual-evidence`
(evidencia), `a11y-checklist` y `design-tokens-dtcg` (frontend), `security-testing` (cybersec).

---

## 1. Principios (lo que distingue al equipo)

1. **El repo existente manda sobre el generico.** En un repo legado se respeta su patron,
   su estilo, sus librerias y su version de runtime. Lo "mejor" de esta skill se aplica a
   codigo nuevo y a lo que la tarea toca, nunca como refactor colateral. Migrar de version,
   cambiar de ORM o de framework solo con pedido explicito.
2. **Cambio minimo, completo y verificable.** Se toca lo que la HU/bug exige, con sus
   pruebas y su documentacion. Nada de "ya que estaba".
3. **Nada se inventa.** Valores de config, URLs, credenciales, reglas de negocio, formatos:
   salen del repo, del config del proyecto, del handoff o se preguntan.
4. **Con plata de por medio, el default es cerrado.** Auth cerrada por defecto, montos en
   decimal, operaciones idempotentes, errores que no filtran detalle, datos personales
   redactados. Un "despues lo cerramos" es un incidente diferido.
5. **Evidencia, no opinion.** "Funciona" significa: compila, los tests pasan, se levanto y
   se probo el caso, y el informe de entrega dice como.

## 2. Metodo de trabajo (siempre, en este orden)

| Paso | Que haces | Salida |
|---|---|---|
| **1. Entender** | Lee la HU/bug y sus criterios, el handoff, la pagina de la wiki del servicio/HU, el `CLAUDE.md` del repo y el codigo que vas a tocar **y su vecindario** (como resuelve el repo validacion, errores, logging, acceso a datos, tests). Identifica el patron real del repo. | Sabes que cambia, donde y con que convenciones |
| **2. Planear** | Plan corto (5-10 lineas) ANTES de tocar: archivos, contrato que cambia, migracion de BD, riesgos (dinero, auth, PII, concurrencia), como lo vas a probar. Si cambia un contrato publico o hay una decision de arquitectura, para y consulta. | Plan en tu respuesta o en el handoff |
| **3. Prueba primero** | En un bug: una prueba que **reproduce y falla** antes del fix. En una feature: las pruebas de los criterios de aceptacion (al menos el camino feliz y el borde mas caro). En legado sin tests: caracterizacion antes de cambiar comportamiento. | Prueba roja que explica el problema |
| **4. Implementar** | El cambio minimo, siguiendo el patron del repo, con validacion en el borde, errores controlados, logs utiles y sin secretos. | Codigo + prueba en verde |
| **5. Auto-revisar el diff** | `git diff` completo leido como revisor hostil con el checklist del §4. Quita debug, TODOs sin ticket, codigo muerto, archivos ajenos. | Diff limpio y explicable linea a linea |
| **6. Verificar** | Build + tests + linter/formatter del stack; levantas lo necesario (servicio y sus dependencias directas) y pruebas el caso real (curl/UI). En BD: script contra un ambiente de prueba o contenedor. | Comandos ejecutados y su resultado |
| **7. Entregar** | Commit(s) convencionales, PR si corresponde, handoffs (QA, Lead, DBA, Frontend, Cybersec segun el caso) con el **informe de entrega** (§5). | Trabajo listo para el gate de QA |

Reglas del metodo:
- Si el paso 1 revela que la tarea esta mal definida, contradictoria o es mas grande que lo
  asignado: no improvises, registra `esperando_usuario` o handoff al Lead con la pregunta.
- Si una prueba falla y no entiendes por que, no la desactives ni la "ajustes" para que
  pase: investiga. Un test rojo es informacion.
- Dos intentos fallidos con la misma hipotesis = cambia de hipotesis o pide ayuda. No
  iteres a ciegas quemando tokens.

## 3. Definicion de Terminado (DoD)

Una tarea de desarrollo esta TERMINADA solo si:
- [ ] Cumple cada criterio de aceptacion de la HU (o el bug no se reproduce mas) y la prueba
      que lo demuestra esta en el repo.
- [ ] Build limpio, sin warnings nuevos silenciados; tests del modulo y de la suite en verde;
      linter/formatter aplicado.
- [ ] Se levanto y se probo el caso real (no solo tests unitarios), con el resultado anotado.
- [ ] Contrato actualizado (OpenAPI/tipos) si cambio; breaking change avisado al Lead.
- [ ] Migraciones de BD con revision del DBA y plan de reversa; nada destructivo sin pedido.
- [ ] Sin secretos, sin datos personales en logs/fixtures/commits; config por variables.
- [ ] Observabilidad: errores logueados con contexto y correlacion; health intacto.
- [ ] Documentacion tecnica tocada si cambio el comportamiento (README/ADR/CHANGELOG).
- [ ] Auto-revision del diff hecha (§4) y diff acotado a la tarea.
- [ ] Handoff a QA con el informe de entrega; a Cybersec si toca auth/pagos/PII/superficie publica.

## 4. Checklist de auto-revision del diff

Antes de entregar, recorre tu diff con estas preguntas. Un "no se" es un "no".

**Correctitud:** ¿el cambio hace lo que pide el criterio, incluidos bordes (vacio, nulo,
cero, negativo, maximo, duplicado, fecha limite, zona horaria)? ¿hay una prueba por cada rama
nueva importante?
**Seguridad:** ¿endpoint nuevo con autorizacion explicita (y por recurso: que el usuario solo
vea lo suyo, anti IDOR)? ¿entrada validada en el borde? ¿SQL parametrizado? ¿nada de secretos,
tokens ni PII en codigo, logs o mensajes de error? ¿salida escapada en front?
**Errores:** ¿errores controlados con Problem Details (o el formato del repo), sin stack traces
al cliente? ¿no se tragan excepciones? ¿ningun borrado de datos/archivos en el manejo de error?
**Dinero y datos:** ¿montos en decimal con moneda explicita y redondeo definido? ¿la operacion
es idempotente si puede repetirse? ¿concurrencia controlada? ¿transaccion donde corresponde?
¿auditoria de quien/cuando/que?
**Logs y observabilidad:** ¿logs estructurados en los puntos de decision, con id de
correlacion y sin datos sensibles? ¿nivel correcto (no Error para un 404 esperado)?
**Performance:** ¿N+1? ¿consulta sin indice o sin paginar? ¿I/O sincrono? ¿llamada externa
sin timeout? ¿carga en memoria de colecciones grandes?
**Migraciones:** ¿compatible hacia atras (expand/contract)? ¿reversible? ¿probada sobre datos
con volumen? ¿revisada por el DBA?
**Contrato:** ¿cambio de forma de request/response, codigos o nombres? ¿consumidores
avisados? ¿OpenAPI y tipos del front al dia?
**Frontend:** ¿estados loading/empty/error/success? ¿accesible con teclado y lector de
pantalla, contraste AA, labels? ¿montos y fechas formateados por locale? ¿fiel al diseño?
**Higiene:** ¿sin `console.log`/prints de debug, codigo comentado, TODO sin ticket, archivos
ajenos al cambio, cambios de formato masivos que ensucian el diff?

## 5. Informe de entrega (formato exacto, va en el handoff a QA y al Lead)

```markdown
# Entrega {HU-nnn | BUG-nnn} — {titulo corto}
**Agente:** {backend|frontend|dba|infra}  **Repo/carpeta:** {repo}  **Rama:** {rama}  **PR:** {url o "sin PR (confirmado)"}

## Que cambio
- {cambio 1, en una linea, con archivo/endpoint/pantalla}

## Como se probo
- Automatizado: {tests agregados/ejecutados y resultado, p. ej. "dotnet test: 142 ok, 0 fail"}
- Manual: {que se levanto y que se probo, con el resultado observado}

## Riesgos y mitigacion
- {riesgo (dinero/auth/datos/concurrencia/performance) → como se mitigo o que queda abierto}

## Que debe mirar QA
- {criterio → donde y como verlo; datos de prueba; casos borde sugeridos}

## Version disponible para probar
- Componente {x} version {x.y.z / tag / commit} en {ambiente | "solo local: levantar {servicios}"}
- Si desplego otra persona o no se conoce la version: decirlo (QA la observara).
- Informe de conformidad: {adjunto si desplegaste | "no aplica"} — es OPCIONAL y su falta no frena la validacion.

## Pendientes / fuera de alcance
- {lo que no se hizo y por que; tickets sugeridos}
```

## 6. Reglas fintech — resumen (detalle en `references/fintech.md`)

- **Montos:** `decimal` (C#), `BigDecimal` (Java), `Decimal` (Python), string/decimal
  library en JS (nunca `number` para calcular plata). En BD `DECIMAL(p,s)`, jamas FLOAT/REAL.
- **Moneda explicita** en cada monto (ISO 4217). CLP sin decimales; PEN, USD con 2; COP con
  2 por norma pero el producto puede operar en enteros — lo define la regla del producto, no
  el desarrollador. **Redondeo definido** y documentado por calculo (half-up / half-even),
  en un solo lugar, al final del calculo, no en pasos intermedios.
- **Idempotencia** en giros, pagos, desembolsos, confirmaciones y callbacks: Idempotency-Key
  o clave natural con restriccion unica; repetir la peticion devuelve el mismo resultado,
  nunca un segundo movimiento.
- **Concurrencia:** optimistic locking (rowversion/columna version/ETag + If-Match);
  transiciones de estado con guardas (`UPDATE ... WHERE estado = 'X'`) y verificacion de filas
  afectadas.
- **Transacciones:** una unidad de negocio = una transaccion corta; efectos externos por
  outbox, nunca "commit y despues llamo y rezo".
- **Auditoria:** quien, cuando, que, desde donde y valor anterior/nuevo en toda operacion
  sobre dinero, estado de operaciones, permisos y datos de clientes.
- **Fechas:** UTC en almacenamiento y transporte; zona del pais solo para reglas y
  presentacion (`America/Santiago`, `America/Lima`, `America/Bogota`); dias habiles y feriados
  por pais; "fecha" de negocio (vencimiento) como fecha sin hora.
- **Datos personales** (RUT, DNI, RUC, NIT, cuentas, correos, telefonos): minimo necesario,
  enmascarados en logs y errores, nunca en fixtures reales ni en commits.

## 7. API y observabilidad — resumen (detalle en `references/api-observabilidad.md`)

Errores RFC 9457 (`application/problem+json`) con `type`, `title`, `status`, `detail`,
`instance`, `traceId` y `errors` de validacion; validacion en el borde; paginacion acotada
(limite maximo) con orden estable; versionado explicito (`/api/v1`) ante consumidores
activos; timeouts en TODA llamada saliente, reintentos solo de operaciones idempotentes con
backoff y jitter, circuit breaker; W3C `traceparent` propagado y OpenTelemetry; logs
estructurados con `traceId`, sin secretos ni PII; `/health/live` (proceso) y `/health`
(readiness con dependencias y version de `version.txt`).

## 8. Pruebas — resumen (detalle en `references/pruebas.md`)

El orden de escritura es el **orden del riesgo** (auth → dinero → estados/concurrencia →
integraciones → el resto), no la piramide. Unit para reglas puras; integracion con **BD real**
(Testcontainers o contenedor local), no InMemory, para todo lo que toque SQL; contrato
(OpenAPI/Schemathesis o tests de contrato) para lo que consumen otros; e2e de los flujos
criticos (los mantiene QA con Playwright). Tests deterministas: reloj, cultura, zona horaria y
aleatoriedad controlados. Nada de secretos ni datos reales en la suite.
