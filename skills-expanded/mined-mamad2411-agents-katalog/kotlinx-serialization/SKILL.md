---
name: kotlinx-serialization
description: kotlinx.serialization patterns for KMP — JSON configuration, polymorphism with sealed hierarchies, custom serializers, enum handling, null/default discipline, and KMP-specific gotchas. Load whenever writing or reviewing serialized boundaries (Ktor bodies, SQLDelight blob encodings, settings values).
---

# kotlinx.serialization

## Json configuration

One shared `Json` instance per app, configured once:

```kotlin
val appJson: Json = Json {
    ignoreUnknownKeys = true
    encodeDefaults = false
    explicitNulls = false
    isLenient = false
    coerceInputValues = true
    useAlternativeNames = false
    classDiscriminator = "type"
}
```

- `ignoreUnknownKeys = true` — forward-compat; new server fields don't crash old clients.
- `encodeDefaults = false` — smaller payloads; omit fields that equal their default.
- `explicitNulls = false` — a missing field deserializes to the default, a `null` explicitly clears.
- `isLenient = false` — fail fast on malformed JSON, don't guess.
- `coerceInputValues = true` — a bad enum in the wire becomes the property default instead of a crash. Accept the trade-off or set `false`.

Inject it into Ktor + anywhere else you parse/emit:

```kotlin
val httpClient = HttpClient(engine) {
    install(ContentNegotiation) { json(appJson) }
}
```

## Serializable classes

```kotlin
@Serializable
data class OrderDTO(
    val id: String,
    @SerialName("customer_id") val customerId: String,
    @SerialName("total_cents") val totalCents: Long,
    val status: OrderStatusDTO,
    @SerialName("created_at") val createdAt: Instant,
)

@Serializable
enum class OrderStatusDTO {
    @SerialName("pending") PENDING,
    @SerialName("paid") PAID,
    @SerialName("cancelled") CANCELLED,
}
```

- Field names in Kotlin stay `camelCase`. Use `@SerialName` to map to `snake_case` on the wire.
- Enum serialization uses the enum constant name by default; override with `@SerialName` for clarity and forward-compat.

## Polymorphism

For API unions, model as a sealed hierarchy:

```kotlin
@Serializable
sealed interface PaymentMethodDTO {
    @Serializable @SerialName("card")
    data class Card(val last4: String, val brand: String) : PaymentMethodDTO

    @Serializable @SerialName("bank")
    data class Bank(val iban: String) : PaymentMethodDTO

    @Serializable @SerialName("wallet")
    data class Wallet(val provider: String) : PaymentMethodDTO
}
```

`classDiscriminator = "type"` (set on `Json`) means the wire format is:

```json
{ "type": "card", "last4": "1234", "brand": "visa" }
```

Server-flexible discriminator? Use `JsonContentPolymorphicSerializer`:

```kotlin
object PaymentSerializer : JsonContentPolymorphicSerializer<PaymentMethodDTO>(PaymentMethodDTO::class) {
    override fun selectDeserializer(element: JsonElement): DeserializationStrategy<out PaymentMethodDTO> =
        when (val kind = element.jsonObject["kind"]?.jsonPrimitive?.content) {
            "CARD" -> PaymentMethodDTO.Card.serializer()
            "BANK" -> PaymentMethodDTO.Bank.serializer()
            else   -> throw IllegalArgumentException("unknown kind: $kind")
        }
}
```

Annotate the sealed interface with `@Serializable(with = PaymentSerializer::class)`.

## kotlinx-datetime

Don't roll your own timestamp format. `kotlinx-datetime` serializes `Instant` as ISO-8601 by default.

```kotlin
@Serializable
data class Event(val at: Instant, val window: LocalDate)
```

For custom formats (legacy server), write a `KSerializer<Instant>` and annotate the field:

```kotlin
object EpochMillisInstantSerializer : KSerializer<Instant> {
    override val descriptor = PrimitiveSerialDescriptor("Instant", PrimitiveKind.LONG)
    override fun deserialize(decoder: Decoder): Instant = Instant.fromEpochMilliseconds(decoder.decodeLong())
    override fun serialize(encoder: Encoder, value: Instant) = encoder.encodeLong(value.toEpochMilliseconds())
}

@Serializable
data class LegacyEvent(@Serializable(EpochMillisInstantSerializer::class) val at: Instant)
```

## Value classes

Value classes serialize as their underlying type (Long, String, etc.), which usually matches the wire. Use them freely at the DTO layer for IDs:

```kotlin
@Serializable @JvmInline value class OrderId(val raw: String)

@Serializable data class OrderDTO(val id: OrderId, val total: Long)
```

## Gotchas

### Default values and polymorphism

A `@Serializable sealed interface` with concrete types that have default-valued properties will lose those on decode unless every instance carries an explicit discriminator. Keep defaults minimal on polymorphic members.

### Enum name mismatch

`coerceInputValues = true` turns unknown enum values into the property default. This is fine for forward-compat but dangerous if you rely on `OrderStatus.PENDING` vs a silent fallback. Log the incoming unknown via a custom deserializer if you need visibility.

### iOS freeze

No longer a concern with new MM but in legacy memory model: `@Serializable` objects should be immutable data classes. Don't share mutable serializable types across threads.

### Generated `serializersModule`

For third-party sealed types outside your control, register a `SerializersModule`:

```kotlin
val appJson = Json {
    serializersModule = SerializersModule {
        polymorphic(Message::class) {
            subclass(ServerMessage::class, ServerMessage.serializer())
            subclass(LogMessage::class, LogMessage.serializer())
        }
    }
}
```

## Testing

Prefer parser round-trips to string assertions, unless the exact byte output is contractual:

```kotlin
@Test fun order_roundTrip() {
    val given = OrderDTO.sample
    val json = appJson.encodeToString(given)
    assertEquals(given, appJson.decodeFromString(json))
}
```

Golden assertions have their place for snapshot tests of your API serialization — keep them in one place so a serializer change is a focused review.

## Hard nos

- No leaking `@Serializable` DTOs into the domain layer. Map.
- No `Json { }` per call site. One shared instance.
- No `isLenient = true` in new code.
- No `explicitNulls = true` when you want to omit fields on encode — use `encodeDefaults = false` + nullable-with-default instead.
- No serializing `Throwable` to the wire. Model domain errors as DTOs.
