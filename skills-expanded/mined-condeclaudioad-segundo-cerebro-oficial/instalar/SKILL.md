---
name: instalar
description: Instala el segundo cerebro para una persona nueva. Le hace preguntas con opciones sobre ella, su negocio y cómo trabaja, completa CLAUDE.md, crea WIKI/yo.md, WIKI/negocio.md y sus primeras memorias, inicializa git y deja el repo listo. Usar con /instalar, "instalá mi cerebro", "empezar" o cuando CLAUDE.md todavía tiene llaves dobles {{ASÍ}}.
argument-hint: "[opcional: una sección para rehacer, ej. \"negocio\"]"
---

# /instalar — tu cerebro andando en 5 minutos

Objetivo: que al terminar, la persona tenga **su** cerebro (no una plantilla) y haya resuelto una primera cosa real con él.

## 0 · Mirá el estado antes de preguntar

- Si `CLAUDE.md` **no** tiene `{{`, el cerebro ya está instalado. Decilo y ofrecé rehacer solo una sección (vos / negocio / cómo trabajás). No pises nada sin OK.
- Si vino un argumento (ej. `negocio`), rehacé solo esa tanda.
- Corré `git remote -v`. Si `origin` apunta al repo público de la plantilla, **avisá ya**: si hace push ahí, su cerebro se publica. En el paso 5 se arregla.

## 1 · Bienvenida (3 líneas, no más)

> Vamos a armar tu segundo cerebro. Son 3 tandas de preguntas cortas, casi todas con opciones. Con eso tu IA ya sabe quién sos, qué hacés y qué decisiones no delegás nunca.

## 2 · Las preguntas — en 3 tandas, con opciones y tu recomendación

Si tu herramienta tiene un selector de opciones (por ejemplo `AskUserQuestion` en Claude Code), usalo. Si no, numeradas en texto, para que conteste tipo `1B 2A 3C`. **Siempre una opción marcada como (reco) y siempre "otra" para escribir libre.** Nunca más de 4 preguntas por tanda.

**Tanda 1 · Vos**
1. ¿Cómo te llamo? *(libre)*
2. ¿En qué zona horaria vivís? A) Buenos Aires / Montevideo · B) Ciudad de México · C) Bogotá / Lima · D) Madrid · E) otra
3. ¿Cómo querés que te hable? A) Directo y corto: veredicto + acción, el detalle en archivos **(reco)** · B) Explicativo, paso a paso · C) Depende de la tarea
4. ¿En qué idioma trabajamos? A) Español **(reco si escribió en español)** · B) Inglés · C) Mezcla

**Tanda 2 · Tu negocio**
1. ¿Qué tipo de negocio tenés? A) Productos digitales (cursos, ebooks, plantillas) · B) Servicios / agencia / consultoría · C) Software / app · D) Ecommerce físico · E) Creador de contenido · F) Todavía no tengo, estoy arrancando
2. ¿En qué etapa estás? A) Idea, sin vender · B) Vendiendo, buscando la oferta que funcione (testeo) · C) Oferta validada, quiero escalar · D) Estable, quiero que funcione sin mí
3. En una línea: **qué vendés y a quién.** *(libre — ofrecé un ejemplo: "plantillas de finanzas para freelancers que cobran en dólares")*
4. ¿Por dónde te llegan los clientes? *(varias)* A) Anuncios pagos · B) Contenido orgánico (IG, TikTok, YouTube) · C) Referidos · D) Prospección directa · E) Marketplaces · F) Todavía ninguno

**Tanda 3 · Cómo trabajás**
1. ¿Con qué IA trabajás? A) Claude Code **(reco: a la mayoría le alcanza)** · B) Codex · C) Las dos
2. ¿Qué decisiones NO querés delegar nunca? *(varias)* A) Precios y ofertas · B) Qué se publica con mi nombre · C) Mensajes a clientes (la IA deja borrador, yo envío) · D) Devoluciones y plata · E) Cuánto se gasta en anuncios · F) Contratar o despedir · G) otra
3. ¿Tu cerebro va a GitHub? A) Sí, creemos un repo **privado** ahora **(reco: lo que no está subido no lo ven la nube ni tus rutinas)** · B) Ya tengo uno · C) Después
4. ¿Qué es lo que más repetís en la semana? *(libre, opcional — es la semilla de tu primera skill)*

## 3 · Escribí

1. **`CLAUDE.md`**: reemplazá cada `{{...}}` con sus respuestas, en una línea cada uno; en el título de la sección, cambiá "(lo completa `/instalar`; el detalle vive en" por "(detalle en". **Borrá el bloque de aviso** que empieza con *"¿Ves llaves dobles…"*. No cambies nada más del archivo.
2. **`RAW/AAAA-MM-DD-instalacion.md`**: las respuestas tal cual, como *"declaración de <nombre> del <fecha>"*. Es la fuente de todo lo que sigue.
3. **`WIKI/yo.md`**: quién es, zona, tono, herramientas, decisiones que no delega, lo que más repite. Con link a la fuente.
4. **`WIKI/negocio.md`**: tipo, etapa, qué vende, a quién, canales, y una sección **"Lo que todavía no sé"** con los huecos (precio, números, oferta principal…). Si la etapa es B o A, anotá el foco: **testeo diario** (una oferta por día, bien hecha, sabiendo qué se testea). Si es C o D: **marketing y escala**.
5. **`MEMORIA/`**: tres memorias con el formato de `MEMORIA/README.md`:
   - `zona-horaria.md` (regla): toda hora en su zona.
   - `como-hablarme.md` (preferencia): el tono elegido.
   - `decisiones-que-no-delego.md` (regla): la lista, con *"la IA prepara, yo decido"*.
   Sumalas al índice de `MEMORIA/README.md`.
6. **`WIKI/index.md`**: convertí las filas de `yo.md` y `negocio.md` en links (`[yo](yo.md)`, `[negocio](negocio.md)`) y sacá el "(nace con…)". En Temas, sacá el "_(vacío…)_".
7. **`changelog/AAAA-MM.md`** (mes actual): creá el archivo con `# Changelog — <mes> <año>` y la primera entrada **arriba**: *"Instalé mi segundo cerebro"* + archivos creados.

## 4 · Verificá antes de decir "listo"

- `grep -n "{{" CLAUDE.md` tiene que dar vacío.
- Reabrí `WIKI/yo.md`, `WIKI/negocio.md` y una memoria. Si algo no coincide con lo que contestó, corregilo.

## 5 · Git

- Si no hay `.git`: `git init -b main`.
- Si `origin` apunta a la plantilla pública: `git remote rename origin plantilla` (así puede traer mejoras de la plantilla sin riesgo de publicar su cerebro).
- `git add -A && git commit -m "Instalo mi segundo cerebro"`.
- Si eligió **crear repo ahora** y existe `gh` autenticado (`gh auth status`): proponé el comando y corrélo **solo con su OK**: `gh repo create <nombre-sugerido> --private --source . --push`. **Siempre `--private`.** Si no hay `gh`, dale los 3 pasos para hacerlo desde github.com (New repository → Private → `git remote add origin … && git push -u origin main`).

## 6 · El primer valor (no lo dejes con una carpeta vacía)

Cerrá con 3 opciones:
- **A) Mapear tu negocio en los 3 niveles** con `/mapear-negocio` **(reco: en 10 minutos sabés qué automatizar primero)**
- **B) Tirar algo a `RAW/`** (una nota, una transcripción) y correr `/procesar-raw`
- **C) Convertir lo que más repetís en tu primera skill** con `/crear-skill` *(si contestó la pregunta 3.4, nombrá esa tarea)*

Y una línea sobre `ejemplo/`: *"En `ejemplo/` tenés un cerebro ficticio con 3 meses de uso, para ver a dónde se llega. Podés borrarlo cuando quieras."*

## Reglas

- No inventes respuestas. Si deja algo vacío, queda como *"pendiente"* en `negocio.md`.
- Nada de datos sensibles: si pega una key o una contraseña, no la guardes y avisale.
- Toda la instalación en el idioma que eligió.
