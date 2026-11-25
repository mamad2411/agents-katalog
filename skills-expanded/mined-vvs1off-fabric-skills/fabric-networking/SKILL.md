---
name: fabric-networking
description: Send data between Minecraft client and server in a Fabric mod using the current payload API - CustomPacketPayload records, StreamCodec, PayloadTypeRegistry, ServerPlayNetworking / ClientPlayNetworking, PlayerLookup - with server-side validation and strict client/server separation. Use when adding a custom packet, syncing state to clients, sending input to the server, or fixing "unknown payload", disconnects or desyncs.
---

# Fabric networking

There is **always** a server, even in singleplayer (the integrated server). Anything the client
wants to change in the world goes client -> server as a request; the server decides, applies,
and tells the clients what happened.

## Step 0 - Which API generation?

| Minecraft | API | Notes |
|---|---|---|
| **26.1+** | `CustomPacketPayload` + `StreamCodec`; `PayloadTypeRegistry.clientboundPlay()` / `serverboundPlay()` | Mojang names throughout |
| 1.20.5 - 1.21.11 | Same payload/codec design. Registry methods `playS2C()` / `playC2S()`. Yarn names: `CustomPayload`, `PacketCodec`, `PacketCodecs`, `RegistryByteBuf`, `CustomPayload.Id` | Mojang-mapped 1.21.x uses Mojang names with the `playS2C/playC2S` methods |
| 1.20.4 and older | Channel `Identifier` + `PacketByteBuf` (`ServerPlayNetworking.send(player, id, buf)`) | Legacy - do not use this shape on 1.20.5+ |

Detect it from `minecraft_version` in `gradle.properties`, then confirm the method names in
Fabric API's sources (`./gradlew genSources`, or open `PayloadTypeRegistry` in the IDE).
Version-matched docs: https://docs.fabricmc.net/develop/networking

Examples below use the **26.1+** names.

## 1. Define the payload (common code, `src/main`)

A payload is a `record` implementing `CustomPacketPayload`, with a `TYPE` and a `StreamCodec`.

```java
package com.example.examplemod.network;

import net.minecraft.core.BlockPos;
import net.minecraft.network.RegistryFriendlyByteBuf;
import net.minecraft.network.codec.ByteBufCodecs;
import net.minecraft.network.codec.StreamCodec;
import net.minecraft.network.protocol.common.custom.CustomPacketPayload;
import com.example.examplemod.ExampleMod;

/** Client -> server: "please ping this block". */
public record PingBlockPayload(BlockPos pos, int colorIndex) implements CustomPacketPayload {
    public static final Type<PingBlockPayload> TYPE = new Type<>(ExampleMod.id("ping_block"));

    public static final StreamCodec<RegistryFriendlyByteBuf, PingBlockPayload> CODEC = StreamCodec.composite(
        BlockPos.STREAM_CODEC, PingBlockPayload::pos,
        ByteBufCodecs.VAR_INT, PingBlockPayload::colorIndex,
        PingBlockPayload::new
    );

    @Override
    public Type<? extends CustomPacketPayload> type() {
        return TYPE;
    }
}
```

```java
/** Server -> client: "show a ping at this position". */
public record ShowPingPayload(BlockPos pos, int colorIndex, UUID from) implements CustomPacketPayload {
    public static final Type<ShowPingPayload> TYPE = new Type<>(ExampleMod.id("show_ping"));
    public static final StreamCodec<RegistryFriendlyByteBuf, ShowPingPayload> CODEC = StreamCodec.composite(
        BlockPos.STREAM_CODEC, ShowPingPayload::pos,
        ByteBufCodecs.VAR_INT, ShowPingPayload::colorIndex,
        UUIDUtil.STREAM_CODEC, ShowPingPayload::from,
        ShowPingPayload::new
    );
    @Override public Type<? extends CustomPacketPayload> type() { return TYPE; }
}
```

Codec tips:

- Primitives: `ByteBufCodecs.BOOL`, `VAR_INT`, `INT`, `FLOAT`, `DOUBLE`, `STRING_UTF8`
  (prefer `ByteBufCodecs.stringUtf8(maxLength)` to cap untrusted strings).
- Vanilla types ship their own: `BlockPos.STREAM_CODEC`, `ItemStack.STREAM_CODEC`,
  `ComponentSerialization.STREAM_CODEC`, `UUIDUtil.STREAM_CODEC`.
- Collections: `ByteBufCodecs.collection(ArrayList::new, elementCodec, maxSize)`.
- `StreamCodec.composite` has overloads up to a fixed number of fields; beyond that, nest a
  record or write the codec with `StreamCodec.of(encoder, decoder)`.
- Payload ids live in your mod's namespace (`examplemod:ping_block`). Never reuse vanilla ids.

## 2. Register payload types (common initializer - both sides)

```java
@Override
public void onInitialize() {
    PayloadTypeRegistry.serverboundPlay().register(PingBlockPayload.TYPE, PingBlockPayload.CODEC);
    PayloadTypeRegistry.clientboundPlay().register(ShowPingPayload.TYPE, ShowPingPayload.CODEC);

    ServerPlayNetworking.registerGlobalReceiver(PingBlockPayload.TYPE, ServerPings::handle);
}
```

Type registration **must** happen in the common `ModInitializer`, so both the client and the
dedicated server know the payload. Registering only in the client initializer gives
"unknown custom payload" / disconnects on servers.

## 3. Receive on the server - validate everything

(`PingColors` and `RateLimiter` stand for your own mod's classes.)

```java
public final class ServerPings {
    private static final double MAX_DISTANCE = 64.0;

    public static void handle(PingBlockPayload payload, ServerPlayNetworking.Context context) {
        ServerPlayer player = context.player();
        BlockPos pos = payload.pos();

        // 1. Validate ranges and enums - the client can send ANY bytes.
        if (payload.colorIndex() < 0 || payload.colorIndex() >= PingColors.COUNT) return;

        // 2. Validate world state: loaded chunk, distance, permissions.
        if (!player.level().isLoaded(pos)) return;
        if (player.distanceToSqr(Vec3.atCenterOf(pos)) > MAX_DISTANCE * MAX_DISTANCE) return;

        // 3. Rate-limit anything a player can spam.
        if (!RateLimiter.tryAcquire(player.getUUID())) return;

        // 4. Act, then broadcast only to players who need it.
        ShowPingPayload out = new ShowPingPayload(pos, payload.colorIndex(), player.getUUID());
        for (ServerPlayer target : PlayerLookup.tracking(player.level(), pos)) {
            ServerPlayNetworking.send(target, out);
        }
    }
}
```

The handler already runs **on the server thread** (Fabric API documents this), so it may touch
the world directly. Do not spawn your own threads to handle packets.

Server-side validation checklist:

- Never trust ids, positions, counts, slot indexes, entity ids, strings or NBT from a client.
- Check the entity still exists (`level().getEntity(id)`), is the right type, and is within
  interaction range (`closerThan`, `distanceToSqr`).
- Check permissions for anything admin-like (the vanilla permission check changed shape in
  recent versions - look up how `ServerPlayer` exposes permissions in your sources).
- Check the chunk is loaded before reading blocks - loading chunks on request is a DoS vector.
- Clamp sizes of collections and strings; cap work per packet.
- Silently ignore (or log at debug) bad packets; do not crash or kick on the first bad value
  unless it is clearly malicious.

## 4. Receive on the client (client initializer, `src/client`)

```java
@Override
public void onInitializeClient() {
    ClientPlayNetworking.registerGlobalReceiver(ShowPingPayload.TYPE, (payload, context) -> {
        if (context.client().level == null) return;
        PingRenderer.add(payload.pos(), payload.colorIndex(), payload.from());
    });
}
```

Client handlers run on the client (render) thread. Keep them cheap: store the data, let
rendering/tick code use it.

## 5. Send

```java
// client -> server (client code only)
if (ClientPlayNetworking.canSend(PingBlockPayload.TYPE)) {
    ClientPlayNetworking.send(new PingBlockPayload(pos, color));
}

// server -> one client
ServerPlayNetworking.send(serverPlayer, payload);

// server -> many: pick the narrowest PlayerLookup
PlayerLookup.tracking(entity);                 // players that see this entity
PlayerLookup.tracking(serverLevel, blockPos);  // players with this chunk loaded
PlayerLookup.around(serverLevel, vec3, radius);
PlayerLookup.level(serverLevel);
PlayerLookup.all(server);
```

- `canSend` tells you whether the other side has your mod (i.e. registered a receiver for that
  type). Use it so a client-side feature degrades gracefully on servers without your mod, and
  so the server does not send packets to vanilla clients.
- Prefer `tracking`/`around` over `all`: fewer packets, and players far away should not learn
  about things they cannot see.

## Client/server separation

- `ClientPlayNetworking`, `Minecraft`, `LocalPlayer`, `ClientLevel` -> `src/client` only.
- `ServerPlayNetworking`, `PayloadTypeRegistry`, payload records -> `src/main` (common).
- The logical server also runs inside the client (singleplayer). Never use
  "am I on the client jar" checks to decide logic; use `level.isClientSide()` for logical side.
- A **client-only** mod (`"environment": "client"`) can still talk to a server that has a
  companion mod; it must check `canSend` and work fine when the server has nothing.

## Configuration-phase payloads (advanced)

Data the client needs *before* joining the world (e.g. server-side config to sync) can use the
configuration phase: `PayloadTypeRegistry.clientboundConfiguration()` /
`serverboundConfiguration()` with `ServerConfigurationNetworking` and a configuration task.
Read the docs page for your version before using it - this area changed in several releases.

## Common mistakes

- Using the pre-1.20.5 `Identifier` + `PacketByteBuf` channel API on modern versions, or the
  Yarn names (`CustomPayload`, `PacketCodec`) in a Mojang-named project.
- Using `playS2C()`/`playC2S()` on 26.1+ (renamed to `clientboundPlay()`/`serverboundPlay()`),
  or the new names on 1.21.x.
- Registering the payload type only on one side, or only in the client initializer.
- Registering receivers in a static initializer that the dedicated server also loads, while
  referencing client classes from it.
- No server-side validation: trusting a client-sent position, entity id, amount, or
  "isCreative" flag. This is how dupes and grief exploits happen.
- Doing heavy work or blocking I/O inside a handler; or, conversely, wrapping a server
  handler in `server.execute(...)` out of habit (it already runs on the server thread).
- Sending to `PlayerLookup.all` every tick instead of sending on change to tracking players.
- Sending per-tick packets with full state instead of deltas or change events.
- Missing `canSend` check, causing errors or kicks when joining vanilla/other servers.
- Reusing one payload record for both directions with different meanings. Make one payload
  per direction and purpose; name them clearly (`...ServerboundPayload` / `...ClientboundPayload`
  is the docs' convention).
