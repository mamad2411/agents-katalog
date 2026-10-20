---
name: realtime-websockets
description: Tiempo real en la API NestJS con WebSocket gateways — autenticación del socket en el handshake, autorización por sala/canal, límites de mensaje y backpressure, reconexión con reanudación, escalado horizontal con adaptador Redis, y el criterio para elegir WebSocket vs SSE vs polling. Usar al agregar notificaciones en vivo, un chat, presencia, o actualización en vivo de agenda/tablero; al escribir o revisar un gateway; o al diagnosticar sockets que no autorizan, se caen al escalar a varias instancias o se saturan.
---

<!-- ESPEJO GENERADO por AtlasPromptManager/tools/install_skills.py - NO EDITAR A MANO -->
<!-- La fuente es AtlasPromptManager/.claude/skills/. Lo que edites aca se pierde. -->

# Tiempo real con WebSockets

El tiempo real es caro en complejidad: conexiones con estado, autenticación fuera del ciclo
request/response, y un problema de escalado que no existe en HTTP. Antes de abrir un socket,
preguntá si de verdad lo necesitás (§1). API de gateways de NestJS verificada; el broker/adaptador
puede ser distinto según proyecto — definilo en el CLAUDE.md del proyecto.

## 1. ¿WebSocket, SSE o polling?

| Necesidad | Elegí | Por qué |
|---|---|---|
| Servidor → cliente, unidireccional (notificaciones, feed en vivo, progreso) | **SSE** | HTTP normal, reconexión automática, atraviesa proxies, más simple |
| Datos que cambian cada varios segundos y toleran latencia | **polling** con cache/ETag | lo más simple; a veces suficiente |
| Bidireccional y de baja latencia (chat, presencia, colaboración) | **WebSocket** | full-duplex real |
| "En vivo" pero en realidad cada 30–60s | polling | no pagues sockets por gusto |

No abras un WebSocket para lo que un SSE o un poll resuelven. El socket que menos mantenés es el
que no abriste.

## 2. Gateway y autenticación

```ts
@WebSocketGateway({ namespace: 'appointments', cors: { origin: ALLOWED } })
export class AppointmentsGateway implements OnGatewayConnection {
  @WebSocketServer() server: Server;

  async handleConnection(@ConnectedSocket() client: Socket) {
    try {
      const user = await this.auth.verifyFromHandshake(client);  // token del handshake
      client.data.user = user;                                   // contexto para este socket
      await client.join(`tenant:${user.tenantId}`);              // aislamiento por tenant
    } catch {
      client.disconnect(true);                                   // sin identidad → afuera
    }
  }

  @UseGuards(WsAuthGuard)
  @SubscribeMessage('appointment.subscribe')
  onSubscribe(@ConnectedSocket() client: Socket, @MessageBody() dto: SubscribeDto) { /* ... */ }
}
```

- **Autenticá en el handshake** (`handleConnection`), no en cada mensaje. Sin identidad válida,
  `disconnect`. El token va por el handshake (header/auth del cliente), no en la URL (queda en logs).
- Guardá el usuario resuelto en `client.data`; reconstruí tenant/actor/permisos como en un
  consumidor de cola (`authz-access-control`, `multi-tenancy`).
- Los guards de WS lanzan **`WsException`**, no `HttpException`. Filtros y pipes también aplican a
  `@SubscribeMessage`.
- Token vencido durante la conexión: revalidá periódicamente o al recibir mensajes sensibles;
  no confíes para siempre en el handshake inicial.

## 3. Autorización por sala/canal

- Una **sala** (room) es una lista de suscripción, **no** un control de acceso por sí sola. Antes
  de `join`, verificá que el usuario tiene derecho a ese recurso (que la cita/chat es suyo o tiene
  relación de atención).
- Nombrá las salas con el tenant y el recurso: `tenant:{t}:appointment:{id}`. Nunca dejes que el
  cliente pida unirse a una sala arbitraria por id sin chequear ownership (es el IDOR de WS).
- Al **emitir**, apuntá a la sala correcta; no hagas broadcast global de algo que es de un tenant
  o de un usuario. Un `server.emit` a todos es una fuga.

## 4. Mensajes: validación, límites, backpressure

- El payload de un mensaje es **entrada hostil**: validalo con DTO igual que un body HTTP. No
  confíes en nada que mande el cliente, incluido "yo soy el usuario X".
- Límite de tamaño de mensaje y de **frecuencia** por cliente (rate limit): un cliente no puede
  inundar el gateway.
- **Backpressure**: si un cliente lento no drena, no acumules mensajes sin límite en memoria.
  Descartá/colapsá updates viejos (para estado en vivo, mandá el último estado, no la cola de
  deltas) o desconectá al cliente que no sigue el ritmo.
- No metas trabajo pesado en el handler del mensaje: encolalo (`background-jobs-scheduling`) y
  respondé/emití el resultado después.

## 5. Reconexión

- Los sockets se caen (red móvil, proxies, deploys). El cliente **reconecta** con backoff; el
  servidor no puede asumir conexión permanente.
- Tras reconectar, el cliente vuelve a autenticarse y a suscribirse; el servidor lo re-une a sus
  salas. No dependas de estado en memoria que se perdió con la conexión.
- Entrega en vivo **no es entrega garantizada**: lo que importa persistirlo (una notificación)
  va también por el canal durable (`notifications-delivery`), y el socket es solo el "avisá ya".
  Al reconectar, el cliente sincroniza el estado real por HTTP, no reproduce lo que se perdió.

## 6. Escalado horizontal — el error clásico

Con **varias instancias** de la API (lo normal detrás de Coolify/balanceador), los clientes de
una sala pueden estar conectados a instancias distintas. Un `emit` en la instancia A **no llega**
a los sockets de la instancia B.

- Solución: un **adaptador** que propaga los eventos entre instancias por un backend compartido
  (típicamente Redis). Configuralo desde el arranque; sin él, el tiempo real "funciona en dev con
  una instancia" y se rompe en producción.
- Sticky sessions en el balanceador si el transporte lo requiere (verificá según tu stack/proxy,
  incluido el de Coolify).
- Presencia y contadores compartidos entre instancias viven en el store compartido, no en memoria
  del proceso.
- Apagado limpio en un deploy: avisá el cierre, dejá que los clientes reconecten a la instancia
  nueva; no cortes en seco a mitad de un mensaje si podés evitarlo (`agent-resource-control` para
  el lado operativo).

## 7. Observabilidad

- Métricas: conexiones activas, conexiones/desconexiones por minuto, mensajes por segundo,
  tamaño de colas de salida, errores de auth en handshake (`backend-observability`).
- Propagá `correlationId` para poder seguir una acción del socket en los logs.
- No loguees payloads con datos sensibles ni tokens (`data-privacy-sensitive`).

## Anti-patrones

- WebSocket para lo que resolvían SSE o polling.
- Autenticar por mensaje en vez de en el handshake; token en la URL del socket.
- `join` a una sala por id sin chequear ownership; `emit` global de datos de un tenant.
- No validar el payload del mensaje; sin rate limit ni backpressure.
- Tratar el socket como entrega garantizada; estado crítico solo en memoria del proceso.
- Escalar a N instancias sin adaptador compartido: eventos que no llegan.

## Checklist

- [ ] Se justificó WS frente a SSE/polling.
- [ ] Auth en el handshake; sin identidad, disconnect; token fuera de la URL; guards lanzan `WsException`.
- [ ] `join` verifica ownership/relación; salas namespaceadas por tenant y recurso; sin emit global.
- [ ] Payload de cada mensaje validado por DTO; rate limit y límite de tamaño; backpressure resuelto.
- [ ] Reconexión re-autentica y re-suscribe; lo importante también va por canal durable y se sincroniza por HTTP.
- [ ] Adaptador compartido (Redis) configurado para varias instancias; presencia/contadores en store compartido.
- [ ] Métricas de conexiones/mensajes/errores; sin datos sensibles ni tokens en logs.
