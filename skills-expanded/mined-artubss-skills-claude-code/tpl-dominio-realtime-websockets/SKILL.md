---
name: tpl-dominio-realtime-websockets
description: Template do pack (dominio/11-realtime-websockets.md). Orienta o agente em regras de negocio e requisitos de produto alinhado a esse contexto.
metadata:
  version: 1.0.0
  source_template: dominio/11-realtime-websockets.md
  generated_by: install_pack_templates_as_claude_skills
---

# DOMAIN: Real-time (WebSockets + Socket.io / SSE)

Skill gerado a partir do pack `templates-claude-code`. Arquivo de origem: `dominio/11-realtime-websockets.md`. Use como baseline e adapte ao projeto antes de mudancas grandes.

## Conteudo do template

## CONTEXT
Real-time parece simples com Socket.io Hello World — e quebra em produção quando
você tem múltiplos servidores, reconexões do cliente causam mensagens duplicadas,
e backpressure de volume alto de mensagens derruba o servidor. A decisão entre
WebSockets e SSE muda a arquitetura inteira — escolher errado custa caro de corrigir.

## STACK ASSUMPTIONS
- WebSockets: Socket.io 4.x (com Redis adapter para escala) ou WS nativo
- SSE: EventSource API (nativo nos browsers)
- Pub/Sub: Redis (ou NATS para throughput muito alto)
- Auth: JWT validado no handshake (não em cada mensagem)
- Backend: Node.js (event loop eficiente) ou Go (goroutines)

## CORE CONCEPTS
- **Room**: agrupamento de conexões WebSocket que recebem as mesmas mensagens
- **Namespace**: partição lógica do servidor Socket.io (evita poluição de eventos)
- **Presence**: rastrear quais usuários estão online (com Redis HSET por room)
- **Reconnection**: cliente reconecta automaticamente — servidor deve suportar isso elegantemente
- **Backpressure**: fila de mensagens maior que o cliente consegue consumir
- **Redis Adapter**: sincronizar rooms e eventos entre múltiplas instâncias Node.js
- **SSE**: server-sent events — unidirecional (server→client), HTTP, sem handshake extra
- **Message Ordering**: TCP garante ordem por conexão, não entre reconexões

## ARCHITECTURE RULES

### SSE vs WebSockets Decision
| Critério | SSE | WebSocket |
|---------|-----|-----------|
| Direção | Server → Client apenas | Bidirecional |
| Protocolo | HTTP/1.1 + HTTP/2 | WS (upgrade do HTTP) |
| Reconexão | Automática (browser) | Manual (library) |
| Proxy/Firewall | Melhor compatibilidade | Pode ser bloqueado |
| Complexidade | Baixa | Alta |
| Casos de uso | Feeds, notificações, dashboards | Chat, games, colaboração |

**Use SSE para**: dashboards em tempo real, feeds de atividade, progresso de jobs
**Use WebSocket para**: chat, colaboração em tempo real, jogos, presença

### Authentication for WS
```javascript
// Socket.io: autenticar no handshake, não em cada evento
io.use(async (socket, next) => {
  const token = socket.handshake.auth.token;
  try {
    const user = await verifyJWT(token);
    socket.user = user; // disponível em todos os handlers
    next();
  } catch (err) {
    next(new Error('Authentication error'));
  }
});
```

### Room Management
- Naming convention: `{resource_type}:{resource_id}` → `post:123`, `org:456`
- Join/Leave rooms: sempre validar que usuário tem permissão para o resource
- Cleanup: ao desconectar, remover de todas as rooms (Socket.io faz automaticamente)
- Rooms efêmeras: criadas sob demanda, sem persistência no banco

### Presence Tracking
```
HSET presence:room:123 { userId: connectionId, joinedAt: timestamp }
EXPIRE presence:room:123 300  // TTL de segurança

On connect: HSET presence:room:123 userId {connectionId, online: true}
On disconnect: HDEL presence:room:123 userId (se não há outra conexão do mesmo user)
```

### Reconnection Handling
- Stateless: mensagens perdidas durante desconexão recuperadas via REST API no reconnect
- Stateful (cursor): cliente envia `lastEventId` → servidor reenvia mensagens após cursor
- Não tentar reconstruir estado completo via WebSocket na reconexão

### Scaling com Redis Adapter
```javascript
const { createAdapter } = require('@socket.io/redis-adapter');
const { createClient } = require('redis');

const pubClient = createClient({ url: process.env.REDIS_URL });
const subClient = pubClient.duplicate();
io.adapter(createAdapter(pubClient, subClient));
// Agora eventos emitidos em qualquer instância chegam a todos os clients
```

## ROUTING TABLE
| Trigger | Action |
|---------|--------|
| WS connect | Autenticar JWT → associar user ao socket → emitir confirmação |
| WS: join_room | Validar permissão → `socket.join(room)` → atualizar presence |
| WS: leave_room | `socket.leave(room)` → remover de presence |
| WS: message (chat) | Validar → persistir no DB → broadcast para room |
| WS: typing_start | Broadcast para room sem persistir (efêmero) |
| WS: disconnect | Limpar presence → notificar room se relevante |
| GET /sse/feed | Criar SSE stream → autenticar → subscrever canal Redis |
| GET /sse/jobs/:id | SSE para progresso de job → fechar ao completar |
| Redis event: new_message | Broadcast para room correspondente via Redis adapter |
| Redis event: job_progress | Emitir para SSE subscribers do job |
| Business logic: notify user | `io.to(userRoom).emit('notification', data)` |
| GET /rooms/:id/history | REST endpoint para mensagens antes do cursor (reconexão) |

## CRITICAL RULES
1. Autenticação SEMPRE no handshake WS, nunca em cada mensagem individual
2. Validar autorização ao entrar em qualquer room (não só ao conectar)
3. Redis adapter obrigatório se deploy em mais de uma instância
4. Nunca processar lógica pesada no event handler principal (bloqueia event loop Node.js)
5. Mensagens efêmeras (typing, cursor) nunca persistidas no banco
6. Reconexão do cliente não assume estado anterior — buscar via REST para reconstituir
7. Backpressure: limitar buffer por connection, fechar conexão se constantemente lento
8. SSE: incluir `event:`, `id:` e `retry:` nos eventos (permite cursor de reconexão)
9. WS connections têm timeout de inatividade (heartbeat/ping-pong)
10. Nunca emitir para `broadcast.emit()` global — sempre para rooms específicas

## COMMON PITFALLS

### ❌ Presença sem TTL → ghost users
```javascript
// ERRADO: se servidor reiniciar sem disconnect event, usuário fica "online" para sempre
await redis.hset(`presence:room:${roomId}`, userId, JSON.stringify({ online: true }));

// CORRETO: TTL + heartbeat para renovar
await redis.hset(`presence:${roomId}`, userId, Date.now());
await redis.expire(`presence:${roomId}`, 60); // 60s TTL
// Client emite heartbeat a cada 30s, renova TTL
```

### ❌ Lógica pesada no event handler
```javascript
// ERRADO: query ao banco dentro do handler bloqueia outras connexões (Node.js single thread)
socket.on('get_history', async () => {
  const messages = await db.messages.findMany({ ... }); // demorado
  socket.emit('history', messages);
});

// CORRETO: offload para worker thread ou já ter dados cacheados
socket.on('get_history', async () => {
  const messages = await cache.get(`history:${roomId}`)
    ?? await db.messages.findMany({ ... }); // executado mas libera event loop via async
  socket.emit('history', messages);
});
```

### ❌ Escalar sem Redis adapter
```javascript
// ERRADO: com 3 instâncias, socket em instância #1 não recebe evento emitido em #2
io.to(roomId).emit('message', data); // só chega a connections na mesma instância

// CORRETO: Redis adapter sincroniza entre todas as instâncias
io.adapter(createAdapter(pubClient, subClient));
io.to(roomId).emit('message', data); // chega a TODOS os clients do room, qualquer instância
```

## QUALITY GATES
- [ ] Autenticação no handshake com rejeição clara de token inválido
- [ ] Redis adapter configurado antes de deploy multi-instância
- [ ] Rooms com validação de autorização no join
- [ ] Presence com TTL e heartbeat (sem ghost users)
- [ ] Mensagens efêmeras nunca persistidas
- [ ] Reconexão busca histórico via REST (não assume estado anterior)
- [ ] Heartbeat/ping-pong para detectar conexões mortas
- [ ] Backpressure handling (buffer limit por conexão)
- [ ] SSE com `id:` em cada evento (permite `Last-Event-ID` no reconnect)
- [ ] Zero broadcast global `.emit()` sem filtragem por room

## FORBIDDEN
- Autenticação por evento individual (degradação de performance)
- Deploy multi-instância sem Redis adapter (split-brain de rooms)
- Lógica síncrona pesada dentro de event handlers WebSocket
- Presença em Redis sem TTL ou heartbeat
- `socket.broadcast.emit()` global em produção sem filtro de room
- Assumir estado consistente após reconexão sem sincronização
