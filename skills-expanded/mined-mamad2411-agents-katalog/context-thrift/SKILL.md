---
name: context-thrift
description: Economía de contexto para agentes — cargar solo lo que puede cambiar la próxima decisión. Usar al arrancar cualquier tarea en un repo grande o multi-repo, antes de abrir un archivo largo, un log, un diff extenso o documentación externa, y cuando la sesión se alarga y hay que pasar hallazgos a notas durables en vez de seguir acumulando dumps en el chat. Decidir si conviene delegar y con qué contrato es `agent-orchestration`; definir el subagente, `subagent-design`.
effort: medium
---

<!-- ESPEJO GENERADO por AtlasPromptManager/tools/install_skills.py - NO EDITAR A MANO -->
<!-- La fuente es AtlasPromptManager/.claude/skills/. Lo que edites aca se pierde. -->

# Economía de contexto

El contexto es un presupuesto, no un depósito. Cada token cargado compite con los que
necesitás para razonar, y lo irrelevante no es neutro: diluye la atención y produce
errores (mezclar dos módulos parecidos, citar una versión vieja de un archivo, seguir un
patrón de otra capa). Leer menos y mejor es una práctica de **calidad**, no solo de costo.

## 1. La pregunta de entrada

Antes de leer cualquier cosa:

> ¿Qué decisión concreta puede cambiar con este contenido?

Si no podés nombrar la decisión, no lo cargues. "Por las dudas" y "para tener contexto
general" no son decisiones.

## 2. Escalera de divulgación progresiva

Subí un escalón solo cuando el anterior no alcanzó.

| Escalón | Qué hacés | Cuándo alcanza |
|---|---|---|
| 1. Nombres | Glob / listado de directorio | Saber si algo existe y dónde vive |
| 2. Coincidencias | Grep con `files_with_matches` o `count` | Saber quién usa un símbolo, cuántos casos hay |
| 3. Fragmento | Grep con contexto (`-C`) o Read con `offset`/`limit` | Entender una función, un DTO, un bloque de config |
| 4. Archivo completo | Read entero | La **estructura** completa importa (ver §4) |
| 5. Fuente externa | Doc oficial, acotada a una pregunta | Una incertidumbre concreta sobre una API que ya sabés que se usa |

Reglas operativas:

1. Grep antes que Read. Buscá el símbolo, no abras el archivo para "ver si está".
2. En archivos largos, leé por rangos: primero el índice (imports, firmas, exports), después el cuerpo que te interesa.
3. Logs y salidas de comandos: filtrá en origen (patrón, últimas N líneas, solo errores). Nunca traigas un log entero para buscar una línea.
4. Diffs: `--stat` primero; el diff completo solo de los archivos que vas a tocar o revisar.
5. No abras documentación de una librería antes de confirmar que el proyecto la usa y en qué versión.

## 3. Libro de contexto

Mantené tres listas cortas y actualizalas al cambiar de fase:

- **SABIDO** — hechos con su fuente (`archivo:línea`, comando + salida).
- **NO SABIDO** — lo que falta.
- **PRÓXIMA PREGUNTA** — el único desconocido que bloquea la siguiente acción.

Investigá la próxima pregunta, no todos los desconocidos posibles. Un desconocido que no
bloquea ninguna acción se anota y se deja.

## 4. Cuándo SÍ leer completo

Leer por fragmentos también falla. Leé el archivo entero cuando:

- Vas a **editarlo** de forma no trivial: necesitás ver el estilo, el orden y lo que ya existe para no duplicar.
- Es corto (orden de un par de cientos de líneas): fragmentar cuesta más que leer.
- Es un contrato o fuente de verdad: spec OpenAPI del recurso, entidad ORM, definición del modelo, el `CLAUDE.md` y las rules del proyecto, la skill que estás aplicando.
- La lógica depende del orden o del flujo completo: una máquina de estados, un pipeline, un interceptor, una migración/patch.
- Ya leíste dos fragmentos del mismo archivo y seguís sin entender: el tercero es el archivo entero.

Señal de que fragmentaste de más: estás **adivinando** lo que hay entre dos rangos.

## 5. Carga de skills y reglas por fase

1. `CLAUDE.md` y rules del proyecto: siempre, al inicio. Son baratos y mandan.
2. Skills transversales: solo cuando la fase las pide. La de seguridad al tocar authz, la de accesibilidad al tocar UI, la de datos al tocar esquema. No las cargues todas "para tenerlas".
3. Backlog o carriles: extraé solo el carril activo y su predecesor explícito. No leas el backlog entero.
4. `references/` de una skill: solo si el `SKILL.md` no alcanzó para el caso concreto.

## 6. Delegar búsquedas amplias

Delegá a un subagente de **solo lectura** cuando la respuesta exige barrer muchos
archivos, directorios o convenciones de nombres, y a vos solo te sirve la conclusión.

- Pedí el resultado con forma: hechos con `archivo:línea`, contratos encontrados, incertidumbres, riesgos. Límite de extensión explícito.
- Quedate con la conclusión. No releas los mismos archivos "para confirmar": si dudás de un hecho puntual, verificá **ese** hecho con un Grep.
- No delegues una búsqueda de un solo dato en un archivo que ya conocés: es más caro que hacerla.
- No dupliques: si delegaste una búsqueda, no la corras vos en paralelo.
- Respetá los límites de concurrencia de `agent-resource-control`; los roles y contratos están en `agent-orchestration`.

## 7. El chat no es un volcado

- No pegues archivos, logs ni diffs enteros en la respuesta. Citá `archivo:línea` y el fragmento mínimo que sostiene la afirmación.
- La evidencia de verificación es la excepción deliberada: salida **literal** pero **recortada** a lo que demuestra el punto (ver `evidence-and-verification`). Recortar no es parafrasear.
- No repitas en cada mensaje lo ya establecido. Referencialo.

## 8. Notas durables

Lo que costó descubrir no debe vivir solo en el contexto de la sesión: se pierde al
resumirse o al cambiar de sesión.

1. Hallazgos de discovery, decisiones y sus motivos, comandos que funcionaron y los que no: a un archivo de notas del carril o de la tarea.
2. Forma de cada nota: hecho + fuente + fecha. Sin narrativa.
3. Al retomar, leé la nota, no rehagas el discovery. Pero una nota es una foto: si nombra un archivo, símbolo o flag, verificá que sigue existiendo antes de apoyarte en él.
4. El estado de avance reanudable es de `progress-reporting`; acá van los **hechos** descubiertos.

## Anti-patrones

- ❌ Abrir los 20 archivos de un módulo "para entender la arquitectura" antes de saber qué vas a cambiar.
- ❌ Leer entera una carpeta de patches/migraciones sin saber qué entidad buscás.
- ❌ Re-leer un archivo que acabás de editar para "verificar" el edit.
- ❌ Traer la doc completa de un framework para resolver una duda de una opción.
- ❌ Pegar 300 líneas de log en el chat con "acá está el error".
- ❌ Delegar una búsqueda y además hacerla vos.
- ❌ El exceso contrario: editar un archivo del que leíste 15 líneas y romper una convención que estaba en la línea 40.

## Checklist

- [ ] Puedo nombrar la decisión que cambia con lo próximo que voy a leer.
- [ ] Usé Grep/Glob antes de Read, y rangos antes de archivo completo.
- [ ] Leí completos los archivos que voy a editar y los contratos que gobiernan el cambio.
- [ ] Cargué solo las skills que esta fase necesita.
- [ ] Las búsquedas amplias fueron a un subagente de solo lectura, y no las dupliqué.
- [ ] No hay dumps en el chat: solo `archivo:línea` y fragmentos mínimos.
- [ ] Los hallazgos que costaron están en una nota durable con fuente y fecha.
- [ ] Tengo una única PRÓXIMA PREGUNTA, y es la que bloquea la siguiente acción.
