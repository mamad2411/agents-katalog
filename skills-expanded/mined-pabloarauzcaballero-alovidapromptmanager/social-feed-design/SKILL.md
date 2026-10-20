---
name: social-feed-design
description: Diseño de una red social y su feed público — modelo de publicaciones, comentarios y reacciones, visibilidad y privacidad, estrategia de feed (fan-out en lectura vs en escritura), contadores concurrentes, autoría verificada, paginación por cursor y no filtrar datos privados. Usar al construir o revisar publicaciones públicas, muros, feeds, comentarios, likes o seguidores, y al decidir cómo se arma y pagina la línea de tiempo.
---

# Red social y feed — reglas de diseño

En un feed público conviven dos riesgos: **exponer lo que no corresponde** y **no escalar la
lectura**. Diseñá para los dos desde el modelo.

## 1. Modelo base

- **Publicación** (post): autor, contenido, visibilidad, timestamps, estado de moderación.
- **Comentario**: pertenece a una publicación (y opcionalmente a otro comentario para hilos).
- **Reacción/like**: par único (actor, objeto) — un usuario reacciona una vez; UNIQUE lo garantiza.
- **Relación** (seguir/amistad): dirigida o mutua según el producto.
- Autoría **verificada en el servidor**: el autor es el actor autenticado, nunca un campo del
  request (ver `authz-access-control`, mass assignment).

## 2. Visibilidad y privacidad primero

- Cada publicación tiene una **visibilidad** explícita (pública / seguidores / privada / grupo).
  El default seguro es el más restrictivo; la ampliación es una acción consciente.
- La visibilidad se evalúa **en cada lectura**, en el servidor. No confíes en que el cliente
  "no va a pedir" lo privado.
- **No filtres datos privados** en la respuesta: un perfil público expone lo mínimo; nada de
  email, teléfono, documento o datos clínicos (ver `data-privacy-phi`). En un producto de salud,
  que alguien sea profesional puede ser público, pero su información sensible no.
- Bloqueos y silenciados se aplican al construir el feed, no en el cliente.

## 3. Estrategia de feed: fan-out read vs write

| | Fan-out en LECTURA (pull) | Fan-out en ESCRITURA (push) |
|---|---|---|
| Cómo | armo el feed al pedirlo, consultando a quién sigo | al publicar, escribo en el feed de cada seguidor |
| Bueno para | cuentas con muchos seguidores; simple de mantener consistente | lectura muy rápida; seguidores por publicación acotados |
| Costo | lectura más cara | escritura amplificada; "celebridades" la rompen |

- Empezá por **fan-out en lectura** (más simple y consistente); pasá a push o híbrido solo cuando
  la medición lo justifique (ver `code-efficiency`). No optimices sin datos.
- Cachéa con criterio: el feed puede cachearse por usuario, pero **respetando visibilidad** y con
  invalidación por evento (ver `caching-strategy`). Nunca sirvas el feed de un usuario a otro.

## 4. Paginación por cursor, no offset

- El feed cambia todo el tiempo; `OFFSET` duplica y saltea items. Usá **cursor** estable
  (ej. `(created_at, id)` codificado) y traé N+1 para saber si hay más.
- El cursor es opaco para el cliente y no filtra información.

## 5. Contadores concurrentes

- Likes/comentarios/seguidores son contadores muy concurrentes. `UPDATE ... SET count = count + 1`
  serializa y puede volverse cuello; y contar `SELECT count(*)` en caliente es caro.
- Opciones: contador denormalizado actualizado transaccionalmente con la reacción, o agregación
  periódica, o tablas de conteo por shard. Elegí según volumen y protegé la carrera
  (ver `concurrency-and-locking`). Lo que no se hace: perder el UNIQUE que evita el doble like.

## 6. Moderación y abuso

- Toda superficie con contenido de usuario necesita moderación y control de abuso desde el diseño:
  reportes, estados de moderación, rate limiting de publicación (ver `content-moderation-abuse`).

## Anti-patrones

- Autor tomado del payload en vez del actor autenticado.
- Evaluar visibilidad/bloqueos en el cliente.
- Exponer campos privados en el perfil o en el post público.
- Paginar el feed con `OFFSET`.
- Cachear el feed sin considerar visibilidad, o compartir caché entre usuarios.
- Perder el UNIQUE (actor, objeto) y permitir doble reacción.

## Checklist

- [ ] Autoría verificada server-side; nada de autor por request.
- [ ] Visibilidad explícita con default restrictivo, evaluada en cada lectura en el servidor.
- [ ] Respuesta pública sin datos privados/sensibles; bloqueos aplicados al armar el feed.
- [ ] Estrategia de feed elegida por medición; arrancá por fan-out en lectura.
- [ ] Paginación por cursor opaco; sin offset.
- [ ] Contadores con UNIQUE contra doble reacción y carrera protegida.
- [ ] Reportes, estados de moderación y rate limiting previstos.
