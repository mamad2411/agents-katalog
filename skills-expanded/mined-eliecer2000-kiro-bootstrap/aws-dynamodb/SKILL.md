---
name: aws-dynamodb
description: DynamoDB data modeling and access patterns. Use when designing partition/sort keys, GSIs, single-table design, transactions, DynamoDB Streams or optimizing query performance.
---

# AWS DynamoDB

Skill para modelado de datos DynamoDB, access patterns, diseño de PK/SK, GSIs, LSIs, single-table design, transacciones, costos, DynamoDB Streams y mejores prácticas de rendimiento.

## Principios fundamentales

- Modelar datos por access patterns, no por entidades. Primero definir las queries, luego diseñar la tabla.
- Single-table design cuando los access patterns están bien definidos y el equipo tiene experiencia. Multi-table cuando la simplicidad es prioridad.
- Nunca hacer Scan como patrón principal de lectura. Si necesitas Scan frecuente, el modelo de datos está mal diseñado.
- Partition key debe distribuir la carga uniformemente. Evitar hot partitions.
- Diseñar para el caso de uso más frecuente, optimizar los demás con GSIs.

## Proceso de modelado de datos

1. Listar todas las entidades del dominio.
2. Definir todos los access patterns (queries que la aplicación necesita).
3. Diseñar PK/SK para cubrir los access patterns principales.
4. Agregar GSIs para access patterns secundarios.
5. Documentar el modelo en una tabla de access patterns.

## Tabla de access patterns (ejemplo e-commerce)

| Access Pattern | PK | SK | GSI |
|---|---|---|---|
| Obtener usuario por ID | `USER#<userId>` | `PROFILE` | - |
| Listar pedidos de usuario | `USER#<userId>` | `ORDER#<timestamp>` | - |
| Obtener pedido por ID | `ORDER#<orderId>` | `METADATA` | - |
| Listar items de pedido | `ORDER#<orderId>` | `ITEM#<itemId>` | - |
| Buscar pedidos por estado | `ORDER#<orderId>` | `METADATA` | GSI1: PK=`STATUS#<status>`, SK=`<timestamp>` |
| Obtener producto por SKU | `PRODUCT#<sku>` | `METADATA` | - |

## Patrones de PK/SK

### Prefijos de tipo (recomendado)
```
PK: USER#12345          SK: PROFILE
PK: USER#12345          SK: ORDER#2024-01-15T10:30:00Z
PK: ORDER#abc-def       SK: METADATA
PK: ORDER#abc-def       SK: ITEM#001
```

### Composite sort key para queries flexibles
```
PK: TENANT#acme         SK: USER#active#2024-01-15
                        → begins_with(SK, "USER#active") → usuarios activos
                        → begins_with(SK, "USER#")        → todos los usuarios
```

### Sparse index pattern
- GSI donde solo algunos items tienen el atributo del index.
- Útil para filtrar subconjuntos: "solo pedidos pendientes", "solo usuarios premium".

## Diseño de GSIs

- Máximo 20 GSIs por tabla (soft limit, ajustable).
- Cada GSI consume WCU/RCU adicional (o capacidad on-demand).
- Proyectar solo los atributos necesarios (`KEYS_ONLY`, `INCLUDE`, `ALL`).
- GSI overloading: reutilizar un GSI para múltiples access patterns con prefijos diferentes.

```
GSI1PK: STATUS#pending     GSI1SK: 2024-01-15T10:30:00Z
GSI1PK: CATEGORY#electronics  GSI1SK: PRODUCT#laptop-001
```

## Transacciones

```typescript
// TransactWrite: hasta 100 items, ACID
await client.send(new TransactWriteItemsCommand({
  TransactItems: [
    {
      Put: {
        TableName: 'MyTable',
        Item: marshall(newOrder),
        ConditionExpression: 'attribute_not_exists(PK)',
      },
    },
    {
      Update: {
        TableName: 'MyTable',
        Key: marshall({ PK: `USER#${userId}`, SK: 'PROFILE' }),
        UpdateExpression: 'SET orderCount = orderCount + :inc',
        ExpressionAttributeValues: marshall({ ':inc': 1 }),
      },
    },
  ],
}));
```

- Máximo 100 items por transacción (4MB total).
- Costo: 2x WCU de una escritura normal.
- Usar para operaciones que deben ser atómicas (crear pedido + actualizar inventario).

## DynamoDB Streams

- Habilitar para CDC (Change Data Capture), sincronización y event-driven.
- Tipos de vista: `KEYS_ONLY`, `NEW_IMAGE`, `OLD_IMAGE`, `NEW_AND_OLD_IMAGES`.
- Usar `NEW_AND_OLD_IMAGES` para detectar cambios específicos en atributos.
- Lambda como consumer: batch size 10-100, bisect on error, max retry attempts.
- Retención de eventos: 24 horas.

## Patrones avanzados

### Paginación con ExclusiveStartKey
```typescript
const params = {
  TableName: 'MyTable',
  KeyConditionExpression: 'PK = :pk',
  ExpressionAttributeValues: { ':pk': { S: `USER#${userId}` } },
  Limit: 20,
  ExclusiveStartKey: lastEvaluatedKey, // del response anterior
};
```

### TTL para expiración automática
```typescript
// Atributo TTL con epoch timestamp
{
  PK: 'SESSION#abc',
  SK: 'METADATA',
  ttl: Math.floor(Date.now() / 1000) + 3600, // expira en 1 hora
}
```

### Optimistic locking con version
```typescript
await client.send(new UpdateItemCommand({
  TableName: 'MyTable',
  Key: marshall({ PK: `PRODUCT#${sku}`, SK: 'METADATA' }),
  UpdateExpression: 'SET stock = stock - :qty, version = version + :inc',
  ConditionExpression: 'version = :currentVersion',
  ExpressionAttributeValues: marshall({
    ':qty': quantity,
    ':inc': 1,
    ':currentVersion': currentVersion,
  }),
}));
```

## Costos y capacidad

### On-demand (recomendado para empezar)
- Pago por request: $1.25 por millón de WRU, $0.25 por millón de RRU.
- Sin planificación de capacidad. Escala automáticamente.
- Ideal para cargas impredecibles o nuevos proyectos.

### Provisioned
- Más barato para cargas estables y predecibles.
- Auto-scaling configurado con target utilization 70%.
- Reserved capacity para descuentos adicionales.

### Optimización de costos
- Usar `ProjectionExpression` para leer solo atributos necesarios.
- Usar `ConsistentRead: false` (eventual consistency) cuando sea aceptable (2x más barato).
- Comprimir atributos grandes con gzip antes de almacenar.
- TTL para eliminar datos expirados sin costo de WCU.

## Anti-patrones a evitar

- ❌ Scan como patrón principal de lectura.
- ❌ Hot partition: PK con baja cardinalidad (ej: `STATUS#active` con millones de items).
- ❌ Items mayores a 400KB (límite duro). Almacenar blobs en S3.
- ❌ Usar `FilterExpression` como sustituto de un buen diseño de PK/SK (filtra después de leer, consume RCU).
- ❌ GSIs con proyección `ALL` cuando solo se necesitan 2-3 atributos.
- ❌ No habilitar Point-in-Time Recovery en producción.
- ❌ No habilitar cifrado (SSE) — viene habilitado por defecto, no deshabilitarlo.
- ❌ Modelar datos como en SQL (normalización excesiva, JOINs simulados).
- ❌ Usar números secuenciales como PK (hot partition).
- ❌ Transacciones para operaciones que no necesitan atomicidad.

## Checklist de revisión DynamoDB

- [ ] Access patterns documentados en tabla antes de implementar.
- [ ] PK distribuye carga uniformemente (alta cardinalidad).
- [ ] No hay Scans en código de producción.
- [ ] GSIs justificados por access patterns específicos.
- [ ] Point-in-Time Recovery habilitado.
- [ ] Cifrado SSE habilitado (default).
- [ ] TTL configurado para datos temporales.
- [ ] DynamoDB Streams habilitado si se necesita CDC.
- [ ] Costos estimados y modo de capacidad elegido conscientemente.
- [ ] Tests con DynamoDB Local o mocks para desarrollo.
