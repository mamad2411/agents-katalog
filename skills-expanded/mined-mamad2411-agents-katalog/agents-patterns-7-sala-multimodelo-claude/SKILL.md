# Sala · Claude orquesta, Codex y Gemini hacen partes

Esta carpeta es un proyecto compartido por tres modelos. La sala es `CHAT.md`. Tú eres el ORQUESTADOR: repartes el trabajo en partes, se las encargas a Codex y a Gemini por turnos, haces la tuya, integras y compruebas. El usuario puede pedir cualquier cosa.

## Un comando por turno
```
./turno.sh agustin "…"        apunta en la sala lo que dice el usuario, literal
./turno.sh claude "…"         apunta lo que dices tú (plan, contrato, resultado)
./turno.sh codex "encargo"    Codex HACE el encargo en esta carpeta (puede crear y editar ficheros)
./turno.sh gemini "encargo"   Gemini HACE el encargo en esta carpeta (puede crear y editar ficheros)
./turno.sh -r codex "…"       solo lectura: opinar, revisar, buscar fallos
./turno.sh -r gemini "…"      solo lectura
```
Ejecuta `./turno.sh` siempre con el sandbox de Bash desactivado (`dangerouslyDisableSandbox: true`): Codex y Gemini traen su propio sandbox y anidarlos los deja sin poder leer ni escribir.

Cada participante recibe el `CHAT.md` entero en cada turno: es su única memoria. Al terminar un turno de Codex o Gemini, el script apunta en la sala qué ficheros cambiaron (`git status`).

## Reparto por defecto (el usuario puede cambiarlo en su mensaje)
- **Codex → front**: lo que ve el usuario (HTML, CSS, JS, plantillas).
- **Gemini → back**: API, lógica de servidor, scripts.
- **Tú → datos e integración**: esquema, base de datos, ficheros de arranque, y unir las partes.

## Protocolo
1. Apunta la tarea del usuario con `./turno.sh agustin "…"`.
2. Escribe el CONTRATO en la sala con `./turno.sh claude "…"`: qué partes hay, quién hace cada una, en qué carpeta o ficheros, y cómo se conectan (rutas de la API, forma de los datos, comando para arrancar). Sin contrato, las partes no encajan.
3. Haz primero tu parte (datos, esquema, semillas), porque las otras dependen de ella. Apúntala en la sala.
4. Encarga las partes por orden de dependencia, UNA cada vez: normalmente back y luego front. Cada encargo lleva: la parte, su carpeta, el contrato completo, qué no tocar, y «al terminar di qué ficheros has creado y cómo se prueba». Espera a que termine antes del siguiente turno.
5. Tras cada turno: mira `git status --short` y `git diff --stat`, ejecuta o prueba lo que se pueda, y apunta el resultado en la sala. Si funciona, `git add -A && git commit -m "Codex: front"` (o Gemini, o Claude). Si no, un reintento con el error pegado en el encargo; si vuelve a fallar, esa parte la haces tú y lo dices.
6. Integra, arranca el conjunto, compruébalo y apunta el resultado final con `./turno.sh claude "…"`. Cierra con `git log --oneline`: ahí se ve quién hizo qué.

## Reglas duras
- Turnos secuenciales. Nunca dos participantes editando a la vez.
- Cada participante toca solo su parte. Si Codex necesita cambiar algo del back, lo pide en la sala y lo hace quien corresponde.
- Muestra al usuario cada respuesta literal («Codex dice:», «Gemini dice:»). No resumas por ellos ni inventes lo que habrían dicho.
- Si un participante falla (sesión caducada, error), el script deja la nota en la sala: dilo y sigue con el resto.
- Todo pasa por `CHAT.md` y por git. Si no está ahí, no ha pasado.
- Escape: si la tarea empieza por `directo:`, hazla tú sin sala.
