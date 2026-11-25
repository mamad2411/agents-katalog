---
name: faast-brain
description: El repo de conocimiento del negocio de FAAST (faast-brain) para el equipo de Mesa de Servicios - que es, como se estructura (productos, clientes, procesos, integraciones, glosario, reglas de negocio, decisiones, historial de solicitudes), como se LEE antes de preguntarle algo al cliente para que las preguntas sean puntuales y no obvias, como se CURA despues de cerrar cada solicitud para que el proximo caso sea mas rapido, y las reglas duras (sin secretos, sin datos personales de clientes, una pagina canonica por tema, se cita la fuente). Cargala antes de analizar una solicitud o al mantener el conocimiento del negocio.
---

# faast-brain — el conocimiento del negocio (Mesa de Servicios)

`faast-brain` es el repositorio donde vive lo que el equipo sabe del NEGOCIO: que productos
existen, que hace cada uno, quienes son los clientes y como operan, que procesos y reglas
rigen, que integraciones hay, y que se decidio antes. No es documentacion tecnica (esa vive
en los repos de cada producto): es el contexto que permite que la Mesa **pregunte poco y
pregunte bien**.

La regla que justifica su existencia: *una pregunta que el negocio ya respondio no se le
hace al cliente*. Si en el brain dice que Confirming opera con dos modos y que el cliente X
usa el modo 2.0, no se pregunta "¿que modo usan?"; se confirma lo que ya se sabe y se
pregunta solo lo que falta.

## Donde vive
Un repo git propio (`faast-brain`), fuera de los repos de producto, cuya ruta se guarda en
`.mesa/config.json` → `brain.path`. Lo crea e inicializa `/mesa-servicios:brain init`. Es
conocimiento acumulado del negocio, no de un proyecto: lo comparten todas las solicitudes.

## Estructura
```
faast-brain/
├── README.md                 que es y como se usa
├── CLAUDE.md                 este esquema (reglas para los agentes)
├── index.md                  portada: mapa del negocio con enlaces
├── productos/{producto}.md   que es, para quien, flujos clave, estados, terminos propios
├── clientes/{cliente}.md     quien es, que productos usa, particularidades, contactos de negocio (sin datos personales sensibles)
├── procesos/{proceso}.md     como opera el negocio de punta a punta (ej. ciclo de una operacion)
├── integraciones/{sistema}.md con quien se conversa (bancos, burós, SII, pasarelas) y para que, en terminos de negocio
├── reglas/{tema}.md          reglas de negocio duras (plazos, montos, aprobaciones, excepciones)
├── glosario.md               el vocabulario del negocio (giro, cesion, nomina, confirming, factoring...)
├── decisiones/{NNN}-{slug}.md decisiones de negocio tomadas y por que
└── solicitudes/{ID}.md       resumen destilado de cada solicitud cerrada (que se pidio, que se decidio, que se aprendio)
```

## Frontmatter obligatorio en cada pagina
```yaml
---
tipo: producto | cliente | proceso | integracion | regla | decision | solicitud | glosario | index
estado: vigente | en-revision | obsoleto
actualizado: YYYY-MM-DD
fuentes:                       # de donde salio lo que afirma la pagina
  - solicitudes/PRY-2026-014.md
  - reunion 2026-03-11 con cliente ACME (transcripcion)
---
```
Toda afirmacion del brain debe poder rastrearse a una fuente. Si algo se asume, se marca
explicitamente como supuesto no confirmado.

## Como se LEE (antes de preguntar)
Esta es la mitad que ahorra tiempo al cliente. Antes de redactar preguntas:
1. Identifica el **producto** y el **cliente** de la solicitud (o si es transversal).
2. Lee, en este orden y solo lo que aplique: `productos/{producto}.md`, `clientes/{cliente}.md`,
   `procesos/{proceso}.md` y las `reglas/` relacionadas. Sigue los enlaces solo si hacen falta.
3. Consulta el `glosario.md` cuando la solicitud use un termino del negocio: hay que usar el
   vocabulario del cliente, no inventar sinonimos.
4. Revisa `solicitudes/` por casos parecidos ya resueltos: muchas veces la respuesta, el
   alcance tipico o la trampa conocida ya estan documentados.
5. Con eso, separa lo que YA SABES (se confirma, no se pregunta) de lo que FALTA (se pregunta).

Si el brain no tiene nada del tema, dilo: se pregunta desde cero y, al cerrar, se crea la
pagina. Un brain vacio al principio es normal; cada solicitud lo hace mas util.

## Como se CURA (despues de cerrar)
Al cerrar una solicitud, el curador destila (no copia) lo aprendido:
- **Producto/cliente/proceso nuevo o cambiado** → crear o actualizar su pagina.
- **Regla de negocio descubierta** (un plazo, un tope, una aprobacion obligatoria) → `reglas/`.
- **Termino nuevo** → `glosario.md`.
- **Decision de negocio** → `decisiones/`.
- **Resumen de la solicitud** → `solicitudes/{ID}.md` con que se pidio, que se decidio y que
  conviene saber la proxima vez (incluida la pregunta que costo mas responder).
Cada edicion cita su fuente y actualiza `actualizado:`. Ante contradiccion entre el brain y
la realidad, gana la realidad y se corrige la pagina.

## Reglas duras
- **Jamas secretos**: ni credenciales, ni tokens, ni cadenas de conexion, ni claves de API.
- **Jamas datos personales sensibles** de clientes finales (RUT de personas, datos bancarios,
  correos personales). Se habla de roles y de la empresa cliente, no de individuos.
- **Una pagina canonica por tema**; si hay dos del mismo tema, se fusionan.
- **Lenguaje de negocio**, sin codigo ni jerga tecnica: lo lee gente de negocio y de mesa.
- **Solo el curador escribe** en el brain; el resto del equipo lo lee. Si una pagina esta
  desactualizada, se le avisa al curador en vez de editarla por cuenta propia.
- El brain **no reemplaza** al cliente: documenta lo que el negocio sabe, no lo que suponemos
  que el cliente quiere.
