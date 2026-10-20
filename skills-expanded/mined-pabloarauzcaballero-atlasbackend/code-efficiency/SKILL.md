---
name: code-efficiency
description: Eficiencia de código y de sistema — medir antes de optimizar, complejidad algorítmica, N+1, batching, caching con invalidación, streaming/paginación, memoria, concurrencia async y trabajo empujado a la base de datos. Usar al revisar un endpoint lento, un loop sobre una colección grande, una query que crece con el dataset, o antes de agregar cache/paralelismo. Complementa a `clean-code` (simplicidad de código) y a `database-design` (índices, modelado).
---

<!-- ESPEJO GENERADO por AtlasPromptManager/tools/install_skills.py - NO EDITAR A MANO -->
<!-- La fuente es AtlasPromptManager/.claude/skills/. Lo que edites aca se pierde. -->

# Eficiencia — medir, no adivinar

Eficiencia no es solo "más rápido": es también menos código, menos estado y menos
recursos por unidad de trabajo útil. El código más eficiente suele ser el más simple:
antes de optimizar, preguntate si el trabajo se puede eliminar en vez de acelerar.

## 1. Medí antes de optimizar
- La intuición sobre dónde está el cuello de botella falla la mayoría de las veces;
  perfilá (profiler de CPU/memoria, `EXPLAIN ANALYZE`, APM) antes de tocar código.
- Optimización prematura: no reescribas código legible por una versión "rápida" sin un
  benchmark que muestre la mejora y sin que esa ruta esté en el camino caliente real.
- Fijá un presupuesto antes de medir (p. ej. "este endpoint responde en bajo X ms con Y
  registros", "este job procesa Z filas por segundo") — sin presupuesto, "rápido" no
  significa nada y cualquier número parece una victoria.
- Reproducí con datos de tamaño realista: un algoritmo O(n²) es invisible con 10 filas
  y catastrófico con 100 000.

## 2. Complejidad algorítmica y estructuras de datos
- Antes de optimizar constantes, revisá la complejidad: un `O(n²)` con `n` chico a veces
  es más rápido en la práctica que un `O(n log n)` con overhead — medí con el `n` real.
- Estructura de datos según el acceso dominante: lookup por clave → mapa/set (O(1)
  amortizado) en vez de `array.find`/`includes` (O(n)) dentro de un loop; membership
  repetido → `Set`, no array.
- Cuidado con anidar iteraciones sobre la misma colección grande (`for` dentro de
  `.filter`/`.map` sobre el mismo dataset) — es un O(n²) disfrazado.

```ts
// ❌ O(n * m): busca en el array en cada iteración
function enrich(orders: Order[], users: User[]): EnrichedOrder[] {
  return orders.map(o => ({ ...o, user: users.find(u => u.id === o.userId) }));
}

// ✅ O(n + m): índice construido una sola vez
function enrich(orders: Order[], users: User[]): EnrichedOrder[] {
  const byId = new Map(users.map(u => [u.id, u]));
  return orders.map(o => ({ ...o, user: byId.get(o.userId) }));
}
```

## 3. N+1 y batching
- El patrón más caro y más común: un loop que dispara una query/llamada de red por
  elemento en vez de una sola llamada por lote. Buscá `for`/`.map` con `await
  db.query(...)` o `fetch(...)` adentro.
- Solución: cargar todo lo necesario en una query con `WHERE id IN (...)` (o el
  dataloader/batching del ORM) y resolver en memoria con un mapa, como en el ejemplo
  anterior. Ver `database-design` para el lado de índices y joins.
- Mismo patrón aplica a llamadas HTTP a otros servicios: agrupá en un endpoint batch si
  existe, o paralelizá con un límite de concurrencia en vez de secuencial.

```ts
// ❌ N+1: una query por cada order
for (const order of orders) {
  order.user = await db.user.findUnique({ where: { id: order.userId } });
}

// ✅ una sola query para todo el lote
const userIds = [...new Set(orders.map(o => o.userId))];
const users = await db.user.findMany({ where: { id: { in: userIds } } });
const byId = new Map(users.map(u => [u.id, u]));
orders.forEach(o => (o.user = byId.get(o.userId)));
```

## 4. Caching con invalidación
- Cacheá el resultado de trabajo caro y repetido con la misma entrada, nunca "por las
  dudas". Todo cache necesita una estrategia de invalidación explícita antes de
  escribirse: TTL, invalidación por evento (al escribir el dato de origen), o versión/tag.
- Un cache sin invalidación es un bug de datos obsoletos con retraso — decidí de
  entrada qué tan obsoleta puede estar la respuesta y documentalo.
- Cache-aside (leer cache, si falla leer origen y poblar) es el patrón por defecto;
  write-through cuando la consistencia importa más que la latencia de escritura.
- Cachear en el nivel más alto que sea seguro (respuesta de endpoint) ahorra más que
  cachear el nivel más bajo (una query chica), pero invalida más difícil — elegí el
  nivel según qué tan seguido cambia el dato.

## 5. Streaming, paginación y memoria
- Nunca cargues una colección completa en memoria para procesar y descartar la mayoría
  — paginá (`LIMIT`/`OFFSET` o cursor por clave), o procesá en streaming (leer de a
  chunks/generador) para datasets que puedan crecer sin límite conocido.
- Paginación por cursor (clave estable + `WHERE id > cursor LIMIT n`) escala mejor que
  `OFFSET` para páginas profundas, porque `OFFSET` sigue escaneando las filas saltadas.
- Liberá referencias a objetos grandes que ya no se necesitan antes de una operación
  larga, para no retenerlos en memoria durante todo el ciclo de vida de la función.

## 6. Concurrencia asíncrona
- Operaciones independientes en paralelo con `Promise.all` (o el equivalente del
  lenguaje) en vez de `await` secuencial cuando no hay dependencia entre ellas.
- Paralelismo sin control de concurrencia satura conexiones/rate limits — limitá con un
  pool/semáforo (tamaño de lote fijo, o una librería de límite de concurrencia) cuando
  el número de tareas puede ser grande.
- `Promise.all` falla entero ante el primer rechazo; usá `Promise.allSettled` cuando
  necesitás el resultado de cada tarea aunque alguna falle.

```ts
// ❌ secuencial cuando las llamadas son independientes
const a = await fetchA();
const b = await fetchB();

// ✅ en paralelo
const [a, b] = await Promise.all([fetchA(), fetchB()]);
```

## 7. Empujar trabajo a la base de datos
- Filtrar, agregar (`SUM`/`COUNT`/`GROUP BY`) y ordenar en la base es casi siempre más
  barato que traer todas las filas y procesarlas en memoria de la aplicación.
- Seleccioná solo las columnas que necesitás (`SELECT` explícito, no `SELECT *`) para
  bajar transferencia de red y uso de memoria del lado de la aplicación.
- Un índice mal elegido (o ausente) convierte un filtro barato en un table scan;
  confirmá con `EXPLAIN`/`EXPLAIN ANALYZE` que el plan usa el índice esperado — detalle
  de modelado en `database-design`.

## 8. Eficiencia también es simplicidad
- Menos código que hace lo mismo es más eficiente de mantener y suele compilar/correr
  más rápido: una dependencia menos, una abstracción menos, un branch menos.
- Eliminar trabajo (no calcular algo que nadie lee, no loguear a nivel debug en
  producción, no serializar campos que se descartan) gana siempre a optimizar ese
  mismo trabajo innecesario.
- Ver `clean-code` para simplicidad a nivel función/nombre; esta skill cubre el costo
  en tiempo/memoria/IO del diseño elegido.

## Checklist
- [ ] Hay un número (benchmark, `EXPLAIN`, profiler) que respalda el cambio, no intuición.
- [ ] Ningún loop dispara una query o llamada de red por elemento (N+1).
- [ ] Lookups repetidos usan `Map`/`Set`, no `array.find`/`includes` dentro de un loop.
- [ ] Todo cache tiene una estrategia de invalidación decidida antes de escribirse.
- [ ] Los datasets sin tamaño acotado se paginan o procesan en streaming, nunca se cargan enteros.
- [ ] Las operaciones independientes corren en paralelo, con límite de concurrencia si el volumen es grande.
- [ ] El filtrado/agregación pesada ocurre en la base, no en memoria de la aplicación.
- [ ] Ningún cambio de "performance" se hizo sin medir antes y después.
