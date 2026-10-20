---
name: datos-sensibles
description: Reglas para que ninguna credencial ni dato sensible de la organización (datos personales de empleados o clientes, nóminas, documentos de identidad, datos bancarios, listados, volcados, infraestructura interna) entre al repositorio sin autorización previa. Actívate SIEMPRE que vayas a crear o editar fixtures, datos de prueba, seeds, migraciones con datos, documentación con ejemplos, capturas o logs; cuando el usuario pida cargar, importar, copiar o "usar los datos reales"; cuando aparezcan nombres de personas, correos, documentos, salarios, tarjetas o contraseñas en el código o en la conversación; y cuando el hook reglas-pr deniegue un push por secretos o datos sensibles.
---

# Datos sensibles — nada entra al repo sin autorización

El repositorio es, por diseño, transferible: hoy lo ve este equipo y mañana puede
verlo otra empresa, un auditor o cualquiera con acceso al remoto. **Todo lo que
entra a git queda en el historial para siempre**, aunque se borre en el commit
siguiente. Por eso la regla es una sola y no tiene excepciones implícitas:

> Ninguna credencial ni dato sensible de la organización entra al repositorio. Los
> datos de la organización solo entran con **autorización previa y explícita** del
> responsable de la información, registrada por el usuario en `.datos-autorizados`
> y declarada en el PR.

## Qué es sensible

| Categoría | Ejemplos | Qué hacer |
|---|---|---|
| **Credenciales** | `.env` con valores, tokens, API keys, contraseñas, llaves privadas, certificados con clave, connection strings con contraseña, cookies de sesión, JWTs, cuentas de servicio | **Nunca.** Van al gestor de secretos o a variables de entorno locales. En el repo solo `.env.example` sin valores. |
| **Datos personales** | nombre + apellido asociados a datos, documentos de identidad (DNI, CUIL/CUIT, RUT, CURP, pasaporte, SSN), fechas de nacimiento, domicilios, teléfonos y correos personales, fotos, datos de salud, datos biométricos | Solo con autorización. Para desarrollar: sintéticos o anonimizados. |
| **Nómina y RR. HH.** | salarios, recibos de sueldo, legajos, evaluaciones de desempeño, licencias, sanciones, organigramas con nombres y sueldos | Solo con autorización. Casi nunca hace falta el dato real para programar. |
| **Datos financieros** | cuentas bancarias (CBU, IBAN), tarjetas, facturación por cliente, precios y condiciones comerciales no públicas, contratos | Solo con autorización. Tarjetas: nunca, ni autorizadas (usa los PAN de prueba de la pasarela). |
| **Listados** | clientes, proveedores, contactos, pacientes, alumnos, leads, exportes de CRM/ERP | Solo con autorización. Para fixtures: muestras sintéticas. |
| **Volcados y logs reales** | dumps de base de datos, backups, logs de producción, capturas de pantalla con datos reales | **Nunca** en el repo. Para reproducir un bug: datos mínimos anonimizados. |
| **Infraestructura interna** | IPs privadas, hostnames internos, diagramas de red detallados, reglas de firewall, inventario de equipos | Solo lo imprescindible y con autorización; mejor por variables de entorno o documentación fuera del repo. |
| **Documentos internos** | actas, políticas no públicas, propuestas comerciales, auditorías | Solo con autorización; normalmente no pertenecen al repo de código. |

Ante la duda: **es sensible**. Pregunta antes de commitear, no después.

## Quién autoriza y cómo se registra

- **Autoriza el responsable de la información** (el dueño del dato en la
  organización o el coordinador del proyecto en su nombre), por escrito, antes de
  que el dato toque el repo. Una conversación informal o "lo necesitamos para la
  demo" no es una autorización.
- **El usuario registra la autorización en `.datos-autorizados`** (raíz del repo):
  una ruta o glob por línea, con un comentario que diga quién autorizó, cuándo y
  para qué. **La autorización vale cuando ya está en `dev`**: el check la lee de
  `origin/dev`, no del working tree, así que un mismo commit no puede traer el
  dato y su propia exención. Primero se mergea la línea de autorización (un PR
  chico), después entran los datos. Cambiar ese archivo pasa por revisión del
  coordinador (CODEOWNERS, donde el plan de GitHub lo aplica).
- **El agente nunca escribe en `.datos-autorizados`** ni agrega el marcador
  `coe:no-secreto` a una línea. Si el usuario te lo pide, dile que lo haga él: la
  autorización es un acto humano y debe quedar trazado como tal.
- **El PR lo declara** en la sección "Datos sensibles" de la plantilla: casilla
  "incluye datos con autorización", quién autorizó y el alcance. El check
  `pr-metadata` falla si falta.

Lo mismo aplica a los fixtures sintéticos que las heurísticas del check confunden
con datos reales: el usuario los registra en `.datos-autorizados` anotando que son
sintéticos, y listo.

## Cómo trabajar sin datos reales

Casi nunca hace falta el dato real para programar, probar o documentar:

- **Datos sintéticos**: genera registros con una librería tipo faker (nombres,
  documentos, correos y teléfonos inventados con el formato correcto) o escribe a
  mano un puñado de casos evidentemente ficticios (`persona-01`,
  `cliente-demo@example.com`). Para tarjetas usa los PAN de prueba publicados por
  la pasarela (`4111 1111 1111 1111`, `4242 4242 4242 4242`); para documentos,
  números que no pasen la validación o que sean claramente de prueba.
- **Anonimización** cuando el caso de prueba necesita la distribución real
  (volúmenes, fechas, categorías): elimina identificadores directos, seudonimiza
  con un hash con sal **que no esté en el repo**, generaliza (edad en rangos,
  ciudad en vez de domicilio) y recorta a la muestra mínima. Verifica que no se
  pueda reidentificar cruzando columnas.
- **Muestras mínimas**: para reproducir un bug alcanza con el registro que lo
  dispara, con los campos sensibles reemplazados.
- **Redacción**: antes de pegar un log, una captura o la salida de un comando en
  un PR, un issue o `notes.md`, reemplaza tokens, contraseñas, documentos, correos
  y nombres por `[REDACTADO]`.
- **Fuera del repo** lo que no es código: exportes reales, volcados y documentos
  viven en el almacenamiento de la organización con su control de acceso, nunca
  en git.

## Qué haces tú (el agente) en cada situación

- **Vas a crear o editar fixtures, seeds, migraciones con datos, ejemplos o
  documentación**: usa datos sintéticos. Si el usuario te pasa datos reales para
  "probar", no los copies al repo: dile que necesitas autorización registrada o
  que los conviertes en sintéticos.
- **El usuario pide importar, cargar o commitear un archivo de datos de la
  organización**: para y pregunta si hay autorización del responsable. Sin
  autorización registrada en `.datos-autorizados`, no se commitea. Con ella, se
  commitea y el PR lo declara.
- **Ves datos sensibles ya presentes en el working tree o en commits sin
  pushear**: no los pushees. Avisa al usuario, sácalos del commit (`git reset
  --soft`, `git rm --cached` o edición del contenido) y vuelve a commitear. Si eran
  credenciales, hay que rotarlas aunque nunca se hayan pusheado: ya salieron del
  gestor de secretos.
- **Ves datos sensibles ya pusheados** (en la rama, en `dev` o en `main`): trátalo
  como una filtración. Avisa de inmediato al usuario y al coordinador: la
  credencial se rota ya; para los datos de personas, el coordinador decide la
  notificación y la limpieza del historial (`git filter-repo`, rotación de
  clones), que **no haces por tu cuenta**.
- **El hook `reglas-pr` denegó el push por secretos o datos sensibles**: lee el
  motivo. Si es real, resuélvelo como arriba. Si crees que es un falso positivo
  (un fixture sintético, un ejemplo en la documentación), **no lo decidas tú**:
  explícaselo al usuario y que él registre la ruta en `.datos-autorizados` o
  marque la línea con `coe:no-secreto`; ese push lo hace él. No rodees el hook.
- **Vas a pegar evidencia en el PR o en `notes.md`**: redacta primero.

## Las redes (y por qué no reemplazan el criterio)

El harness pone varias capas, cada una cubre lo que la anterior no ve:

1. `.claude/settings.json` deniega la lectura directa de archivos de credenciales
   con la tool `Read` (es una traba, no un muro: no cubre `cat` en Bash) y la
   edición con las tools de edición de los guardarraíles mismos (`.claude/hooks/`,
   `.claude/settings.json`, `scripts/check-pr-rules.mjs`, `.datos-autorizados`,
   `.github/workflows/`).
2. `.gitignore` excluye los archivos de credenciales típicos y los volcados.
3. El hook `reglas-pr` deniega, antes de cada `git push`, los commits que suben
   archivos de credenciales, llaves/tokens/contraseñas en el contenido o datos
   personales y de nómina (documentos de identidad, tarjetas, listados de
   correos, nombres de archivo de nómina o clientes), salvo las rutas ya
   autorizadas en el `.datos-autorizados` de `dev`. Incluye los merge commits.
   Si no puede verificar (un error, un timeout), pide confirmación en vez de
   dejar pasar.
4. El mismo check corre en CI (`reglas-pr.yml`) para lo que llega desde fuera de
   la sesión, y la plantilla del PR obliga a declarar los datos. Los marcadores
   `coe:no-secreto` y las líneas nuevas de `.datos-autorizados` que lleguen en el
   diff aparecen listados en el resultado (`excepciones-nuevas`), para que el
   revisor los vea.

Las heurísticas detectan formatos conocidos; **no detectan un nombre y apellido
sueltos, un salario en una celda sin encabezado ni un dato que no tiene forma de
patrón**. Tampoco escanean binarios, `.svg`, `.map`, lockfiles, líneas de más de
20 000 caracteres (se cuentan y se avisan), secretos codificados en base64/hex,
ni valores que contienen palabras de ejemplo (`example`, `sample`, `dummy`,
`fake`, `your-`). Esa parte es tuya: si sabes que es un dato de una persona real
o una credencial, no entra, tenga la forma que tenga.

## Checklist antes de commitear

- [ ] No hay `.env` con valores, llaves, certificados ni archivos de credenciales.
- [ ] No hay tokens, contraseñas ni connection strings en código, config, tests o
      docs (busca `password`, `secret`, `token`, `key`, `Bearer`, `BEGIN PRIVATE`).
- [ ] Los fixtures y seeds son sintéticos o están registrados en
      `.datos-autorizados` con su autorización.
- [ ] No hay volcados, exportes ni logs reales.
- [ ] Las capturas y logs de la evidencia están redactados.
- [ ] El PR declara la situación en "Datos sensibles" de verdad.
