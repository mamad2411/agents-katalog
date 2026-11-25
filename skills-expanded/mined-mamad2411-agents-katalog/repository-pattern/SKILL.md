---
name: repository-pattern
description: "Crear o revisar un Repository, decidir cómo combina un RemoteDataSource y un LocalDataSource, o decidir si una operación debe ser Flow o suspend."
---

# Skill: repository-pattern

## Objetivo

Definir cómo implementar el Repository Pattern en proyectos Kotlin Multiplatform siguiendo una estrategia **single source of truth (offline-first)**: el Repository coordina un `RemoteDataSource` y un `LocalDataSource` (Room KMP), donde la caché local es la única fuente de verdad para las lecturas y la red se usa exclusivamente para sincronizar esa caché.

Este Skill define únicamente cómo se estructura y coordina el Repository. No define el tipo de error (`result-pattern`), ni la configuración de Room KMP o Ktor (`room-multiplatform`, `ktor-client`), ni cómo se inyecta (`dependency-injection-koin`).

---

## Modelo conceptual

```text
Domain
  interface ItemRepository {                          ← Port
      fun observeItems(): Flow<Result<List<Item>, DomainError>>
      suspend fun refresh(): Result<Unit, DomainError>
      suspend fun create(item: Item): Result<Unit, DomainError>
  }
                ▲
                │ implementa
Infrastructure
  class ItemRepositoryImpl(
      private val remote: ItemRemoteDataSource,
      private val local: ItemLocalDataSource           ← Room KMP
  ) : ItemRepository {

      override fun observeItems() =
          local.observeItems().map { ... }              // 1. la UI siempre lee de local

      override suspend fun refresh(): Result<Unit, DomainError> {
          val dtos = remote.fetchItems()                 // 2. pide a la red
          local.replaceAll(dtos.map { it.toEntity() })    // 3. persiste en caché
          return Result.Success(Unit)                     // 4. el Flow de observeItems() propaga el cambio solo
      }
  }
```

La UI/Application nunca lee directamente del `RemoteDataSource`; siempre observa el `LocalDataSource` a través del Repository. La red solo alimenta la caché.

---

## Cuándo usarlo

- Crear un nuevo Repository para una entidad o agregado de Domain.
- Decidir cómo combinar un `RemoteDataSource` y un `LocalDataSource`.
- Decidir si una operación debe ser `Flow` o `suspend`.
- Revisar si una implementación de Repository respeta el single source of truth.
- Sincronizar datos tras una acción de escritura (crear, editar, borrar).

## Cuándo NO usarlo

- Para definir las capas en general → usar `clean-architecture-kmp`.
- Para tipar el error de las operaciones → usar `result-pattern`; este Skill solo consume `Result<T, DomainError>`, no lo redefine.
- Para configurar el cliente Ktor concreto (engine, interceptores, serialización) → usar `ktor-client`.
- Para configurar Room KMP (entidades, DAOs, migraciones, drivers por plataforma) → usar `room-multiplatform`.
- Para inyectar el Repository o sus DataSource en Koin → usar `dependency-injection-koin`.

---

## Dependencias

```text
- clean-architecture-kmp
- result-pattern
- room-multiplatform
- ktor-client
- dependency-injection-koin
```

---

## Entradas necesarias

- Entidad/agregado de Domain a exponer (ej. `Item`, `User`).
- Operaciones necesarias: ¿observar lista?, ¿observar detalle?, ¿crear/editar/borrar?, ¿forzar refresh manual?
- Forma del DTO remoto (API) y de la entidad Room (tabla local), para definir los Mappers.
- Política de sincronización si aplica (refrescar al entrar a la pantalla, refrescar periódicamente, solo pull-to-refresh manual).

---

## Criterios arquitectónicos

- El Repository es la única clase que conoce simultáneamente al `RemoteDataSource` y al `LocalDataSource`; ninguna otra clase de Infrastructure los combina.
- La interfaz del Repository (Port) vive en Domain; su implementación, en Infrastructure.
- La caché local (Room KMP) es la única fuente de verdad para las lecturas: toda lectura observable pasa siempre por el `LocalDataSource`, nunca directamente por el `RemoteDataSource`.
- El `RemoteDataSource` solo se usa para sincronizar/alimentar la caché local, nunca para devolver datos directamente a Application/Presentation.
- Un Repository representa un agregado o entidad, no un caso de uso ni una pantalla; no debe crearse un Repository por cada `UseCase`.
- Los `DataSource` (Remote/Local) son detalles de implementación internos del Repository; no se exponen como Port en Domain ni se inyectan directamente en Application.

---

## Reglas

- Debe definirse la interfaz del Repository en `domain/repositories` como Port; nunca en Infrastructure.
- Las operaciones que representan datos observables (listas, detalle reactivo) deben devolver `Flow<Result<T, DomainError>>`.
- Las operaciones puntuales (crear, editar, borrar, forzar refresh) deben ser funciones `suspend` que devuelvan `Result<T, DomainError>` (o `Result<Unit, DomainError>` si no hay valor de retorno relevante).
- El Repository debe leer siempre desde el `LocalDataSource` (Room KMP) para los `Flow` observables; no debe combinar `remote.observe()` y `local.observe()` en el mismo flujo expuesto a Application.
- Toda escritura debe seguir el patrón: escribir en remoto (si aplica) → persistir el resultado en local → dejar que el `Flow` del `LocalDataSource` propague el cambio automáticamente.
- El Repository nunca debe exponer el DTO remoto ni la `@Entity` de Room fuera de Infrastructure; siempre debe mapear a la Entity de Domain mediante un Mapper.
- Las excepciones técnicas del `RemoteDataSource`/`LocalDataSource` se capturan dentro del Repository y se traducen a `DomainError` (ver `result-pattern`); nunca se propaga la excepción original ni un tipo de Ktor/Room.
- El `RemoteDataSource` y el `LocalDataSource` deben ser interfaces propias de Infrastructure (no Ports de Domain), para poder sustituirse en tests sin acoplar el Repository directamente a Ktor/Room.
- Un Repository no debe contener reglas de negocio; solo coordina fuentes y mapea datos.

---

## Decisiones automáticas

```text
Si la operación devuelve datos que pueden cambiar mientras la pantalla está abierta (listas, detalle observado)
    → Flow<Result<T, DomainError>>, leído siempre del LocalDataSource

Si la operación es una acción puntual (crear, editar, borrar, sincronizar manualmente)
    → función suspend que devuelve Result<T, DomainError>

Si una operación de escritura tiene éxito en remoto
    → debe persistirse en local antes de devolver Result.Success; nunca se notifica éxito si la persistencia local falla

Si el RemoteDataSource falla pero el LocalDataSource ya tiene datos previos
    → el Flow sigue exponiendo los datos locales existentes; el fallo de red se reporta solo en el Result de la operación de refresh(), sin romper el Flow observado

Si una entidad no necesita observación reactiva en ninguna pantalla (recurso de solo lectura puntual)
    → puede exponerse solo con funciones suspend, sin Flow
```

---

## Proceso recomendado

1. Definir la Entity de Domain (si no existe).
2. Definir el Port `XxxRepository` en `domain/repositories` con sus operaciones (Flow para lo observable, suspend para lo puntual).
3. Definir `XxxRemoteDataSource` y `XxxLocalDataSource` como interfaces propias de Infrastructure.
4. Implementar `XxxLocalDataSource` con Room KMP (ver `room-multiplatform`) y `XxxRemoteDataSource` con Ktor (ver `ktor-client`).
5. Implementar `XxxRepositoryImpl`, inyectando ambos DataSource y coordinando lectura (local) y sincronización (remoto → local).
6. Definir los Mappers DTO↔Entity y RoomEntity↔Entity en `infrastructure/mappers`.
7. Registrar el Repository y los DataSource en Koin (ver `dependency-injection-koin`).
8. Cubrir con tests: lectura desde local, sincronización exitosa, fallo de red con caché previa disponible (ver `testing-kmp`).

---

## Checklist

- [ ] El Port del Repository vive en Domain; la implementación, en Infrastructure.
- [ ] Toda lectura observable usa `Flow<Result<T, DomainError>>` leído del `LocalDataSource`.
- [ ] Toda escritura persiste en local antes de notificar éxito.
- [ ] El `RemoteDataSource` nunca se expone directamente a Application/Presentation.
- [ ] El Repository mapea DTO/RoomEntity a Entity de Domain; ninguno de los dos sale de Infrastructure.
- [ ] Las excepciones técnicas se traducen a `DomainError` dentro del Repository.
- [ ] Un Repository representa un agregado, no una pantalla ni un `UseCase`.

---

## Definition of Done

- La UI/Application siempre observa datos consistentes provenientes de Room KMP, incluso sin conexión.
- Las operaciones de sincronización (`refresh`/`create`/`update`/`delete`) actualizan la caché local y el cambio se propaga automáticamente por el `Flow` existente.
- Ningún tipo de Ktor o Room (DTO, `@Entity`) cruza el límite de Infrastructure.
- Los fallos de red no rompen los `Flow` observables; se reportan en el `Result` de la operación puntual correspondiente.

---

## Riesgos

- "God Repository" que mezcla varias entidades o responsabilidades no relacionadas.
- Pantallas u Use Cases leyendo directamente del `RemoteDataSource`, rompiendo el single source of truth.
- Escrituras que notifican éxito antes de confirmar la persistencia local, desincronizando la UI de la caché real.
- DTOs o entidades de Room filtrándose a Application/Presentation por mappers incompletos.
- Lógica de negocio (validaciones, reglas) colándose dentro del Repository en lugar de vivir en Domain/Application.

---

## Anti-patrones

- `interface ItemRepository` definida dentro de `infrastructure` en lugar de `domain`.
- Una función `suspend fun getItems(): List<Item>` (sin Flow) usada para una pantalla que necesita reactividad en tiempo real.
- Repository devolviendo directamente el resultado de `remote.fetchItems()` sin pasar por la caché local.
- `RoomEntity` o DTO de Ktor expuestos como tipo de retorno de un método del Repository.
- Repository con una función por cada `UseCase` de la app (`getItemsForHomeScreen()`, `getItemsForDetailScreen()`) en lugar de operaciones genéricas reutilizables por entidad.
- Capturar la excepción de Room/Ktor y relanzarla tal cual en lugar de mapearla a `DomainError`.

---

## Comandos útiles

N/A — este Skill no depende de comandos CLI específicos; la configuración de Room KMP y Ktor se cubre en sus Skills correspondientes (`room-multiplatform`, `ktor-client`).

---

## Salida esperada

```text
domain/
  repositories/
    ItemRepository.kt           → Port (interfaz)
infrastructure/
  datasources/
    ItemRemoteDataSource.kt      → interfaz + impl con Ktor
    ItemLocalDataSource.kt       → interfaz + impl con Room KMP
  repositories/
    ItemRepositoryImpl.kt        → implementación del Port
  mappers/
    ItemMappers.kt                → DTO↔Entity, RoomEntity↔Entity
```

---

## Ejemplos

### Correcto — Port en Domain

```kotlin
// domain/repositories/ItemRepository.kt
interface ItemRepository {
    fun observeItems(): Flow<Result<List<Item>, DomainError>>
    suspend fun refresh(): Result<Unit, DomainError>
    suspend fun create(item: Item): Result<Unit, DomainError>
    suspend fun delete(id: String): Result<Unit, DomainError>
}
```

### Correcto — DataSources en Infrastructure

```kotlin
// infrastructure/datasources/ItemLocalDataSource.kt
interface ItemLocalDataSource {
    fun observeItems(): Flow<List<ItemEntity>>
    suspend fun replaceAll(items: List<ItemEntity>)
    suspend fun insert(item: ItemEntity)
    suspend fun delete(id: String)
}

class RoomItemLocalDataSource(private val dao: ItemDao) : ItemLocalDataSource {
    override fun observeItems(): Flow<List<ItemEntity>> = dao.observeAll()
    override suspend fun replaceAll(items: List<ItemEntity>) = dao.replaceAll(items)
    override suspend fun insert(item: ItemEntity) = dao.insert(item)
    override suspend fun delete(id: String) = dao.deleteById(id)
}

// infrastructure/datasources/ItemRemoteDataSource.kt
interface ItemRemoteDataSource {
    suspend fun fetchItems(): List<ItemDto>
    suspend fun createItem(item: ItemDto): ItemDto
    suspend fun deleteItem(id: String)
}

class KtorItemRemoteDataSource(private val client: HttpClient) : ItemRemoteDataSource {
    override suspend fun fetchItems(): List<ItemDto> = client.get("items").body()
    override suspend fun createItem(item: ItemDto): ItemDto = client.post("items") { setBody(item) }.body()
    override suspend fun deleteItem(id: String) { client.delete("items/$id") }
}
```

### Correcto — RepositoryImpl coordinando ambas fuentes

```kotlin
// infrastructure/repositories/ItemRepositoryImpl.kt
class ItemRepositoryImpl(
    private val remote: ItemRemoteDataSource,
    private val local: ItemLocalDataSource
) : ItemRepository {

    override fun observeItems(): Flow<Result<List<Item>, DomainError>> =
        local.observeItems()
            .map<List<ItemEntity>, Result<List<Item>, DomainError>> { entities ->
                Result.Success(entities.map { it.toDomain() })
            }
            .catch { emit(Result.Failure(DomainError.Unexpected(it.message ?: "unknown"))) }

    override suspend fun refresh(): Result<Unit, DomainError> = try {
        val dtos = remote.fetchItems()
        local.replaceAll(dtos.map { it.toEntity() })
        Result.Success(Unit)
    } catch (e: CancellationException) {
        throw e
    } catch (e: Exception) {
        Result.Failure(DomainError.NetworkUnavailable)
    }

    override suspend fun create(item: Item): Result<Unit, DomainError> = try {
        val created = remote.createItem(item.toDto())
        local.insert(created.toEntity())
        Result.Success(Unit)
    } catch (e: CancellationException) {
        throw e
    } catch (e: Exception) {
        Result.Failure(DomainError.NetworkUnavailable)
    }

    override suspend fun delete(id: String): Result<Unit, DomainError> = try {
        remote.deleteItem(id)
        local.delete(id)
        Result.Success(Unit)
    } catch (e: CancellationException) {
        throw e
    } catch (e: Exception) {
        Result.Failure(DomainError.NetworkUnavailable)
    }
}
```

### Incorrecto

```kotlin
// ❌ Lee directamente de la red, rompe el single source of truth
class ItemRepositoryImpl(private val remote: ItemRemoteDataSource) : ItemRepository {
    override fun observeItems(): Flow<Result<List<Item>, DomainError>> = flow {
        emit(Result.Success(remote.fetchItems().map { it.toDomain() })) // sin caché, sin reactividad real
    }
}

// ❌ Expone el DTO de Ktor fuera de Infrastructure
interface ItemRepository {
    suspend fun getItems(): List<ItemDto> // el DTO no debería cruzar el límite de Infrastructure
}
```

---

## Referencias

- clean-architecture-kmp
- result-pattern
- room-multiplatform
- ktor-client
- dependency-injection-koin
- ARCHITECTURE.md — secciones Domain, Infrastructure
