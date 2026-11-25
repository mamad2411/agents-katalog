---
name: websocket-architect
description: "Design and implement real-time features using WebSockets. Covers Laravel Reverb, Pusher, Socket.io, broadcasting, and live update patterns."
category: php-frameworks
tags: ['websockets', 'realtime', 'laravel-reverb', 'pusher', 'socket.io']
complexity: advanced
risk: low
compatibility: [claude-code, antigravity, gemini-cli, cursor, copilot, codex-cli, autohand, kiro]
source: antigravity-official
version: "1.0.0"
date_added: "2026-07-10"
last_updated: "2026-07-10"
---

# WebSocket & Real-time Architect

## Purpose
Build real-time, bidirectional communication features using WebSockets for live updates, chat, notifications, and collaborative features.

## Operating Mode
You are a **real-time systems specialist** designing WebSocket architectures that scale.

## Technology Comparison
| Technology | Best For | Hosted? |
|---|---|---|
| Laravel Reverb | Laravel apps, self-hosted | Self-hosted |
| Pusher | Quick setup, managed | Managed (paid) |
| Soketi | Pusher-compatible, free | Self-hosted |
| Socket.io + Node | Complex real-time | Self-hosted |

## The Process

### 1️⃣ Laravel Reverb Setup (Self-hosted)
```bash
# Install Reverb (Laravel 11+)
php artisan install:broadcasting

# .env
BROADCAST_CONNECTION=reverb
REVERB_APP_ID=my-app-id
REVERB_APP_KEY=my-app-key
REVERB_APP_SECRET=my-app-secret
REVERB_HOST="localhost"
REVERB_PORT=8080

# Start the WebSocket server
php artisan reverb:start
```

### 2️⃣ Broadcasting Events
```php
// App/Events/OrderStatusUpdated.php
class OrderStatusUpdated implements ShouldBroadcast
{
    use Dispatchable, InteractsWithSockets, SerializesModels;

    public function __construct(
        public readonly Order $order,
    ) {}

    public function broadcastOn(): array
    {
        return [
            new PrivateChannel("orders.{$this->order->user_id}"),
        ];
    }

    public function broadcastAs(): string
    {
        return 'order.updated';
    }

    public function broadcastWith(): array
    {
        return [
            'id'     => $this->order->id,
            'status' => $this->order->status,
            'eta'    => $this->order->estimated_delivery,
        ];
    }
}

// Dispatch from controller or job
broadcast(new OrderStatusUpdated($order))->toOthers();
```

### 3️⃣ Channel Authorization
```php
// routes/channels.php
Broadcast::channel('orders.{userId}', function (User $user, int $userId) {
    return (int) $user->id === $userId;
});

Broadcast::channel('team.{teamId}', function (User $user, int $teamId) {
    return $user->belongsToTeam($teamId);
});
```

### 4️⃣ Frontend Subscription (Laravel Echo)
```javascript
// resources/js/bootstrap.js
import Echo from 'laravel-echo';
import Pusher from 'pusher-js';

window.Echo = new Echo({
    broadcaster: 'reverb',
    key: import.meta.env.VITE_REVERB_APP_KEY,
    wsHost: import.meta.env.VITE_REVERB_HOST,
    wsPort: import.meta.env.VITE_REVERB_PORT ?? 8080,
    forceTLS: false,
    enabledTransports: ['ws', 'wss'],
});

// Subscribe to private channel
window.Echo.private(`orders.${userId}`)
    .listen('.order.updated', (event) => {
        updateOrderStatus(event.id, event.status);
    });

// Presence channels (who is online)
window.Echo.join('room.1')
    .here((users) => { /* currently online users */ })
    .joining((user) => { console.log(user.name, 'joined'); })
    .leaving((user) => { console.log(user.name, 'left'); })
    .listen('MessageSent', (e) => { addMessage(e.message); });
```

### 5️⃣ Chat Application Pattern
```php
// Broadcasting a chat message
class MessageSent implements ShouldBroadcast
{
    public function broadcastOn(): array
    {
        return [new PresenceChannel("chat.{$this->message->room_id}")];
    }

    public function broadcastWith(): array
    {
        return [
            'id'      => $this->message->id,
            'content' => $this->message->content,
            'user'    => [
                'id'   => $this->message->user->id,
                'name' => $this->message->user->name,
            ],
            'sent_at' => $this->message->created_at->toISOString(),
        ];
    }
}
```

### 6️⃣ Production Scaling
```nginx
# Nginx WebSocket proxy
location /app/ {
    proxy_pass http://127.0.0.1:8080;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "Upgrade";
    proxy_set_header Host $host;
    proxy_read_timeout 60;
}
```

## Outputs
1. WebSocket server setup (Reverb/Pusher)
2. Event broadcasting implementation
3. Channel authorization
4. Frontend Echo subscription code
5. Chat/notification system template
6. Production nginx configuration
