---
name: django-channels
description: Django Channels and WebSocket expertise. Use when implementing real-time features, WebSocket consumers, channel layers, ASGI configuration, or Redis message broker. Activates for tasks involving real-time sync, live updates, or WebSocket connections.
---

# Django Channels — решения этого проекта

---

## Архитектура: server-only push

Клиент **не шлёт** WS-сообщения. Все изменения идут через REST API. WS используется только для рассылки событий всем подключённым клиентам.

```
HTTP PATCH /api/purchases/1/toggle/
  → views.py: Purchase.set_need_to_buy()
  → _broadcast('purchase.updated', payload)
  → channel_layer.group_send('shop', ...)
  → ShopConsumer.shop_event()
  → ws.send(JSON) → все браузеры
```

---

## Схема файлов

| Файл | Роль |
|------|------|
| `config/asgi.py` | ProtocolTypeRouter: http → Django, websocket → AuthMiddlewareStack → ShopConsumer |
| `apps/shop/routing.py` | `websocket_urlpatterns = [path('ws/shop/', ShopConsumer.as_asgi())]` |
| `apps/shop/consumers.py` | `ShopConsumer` + константа `WS_GROUP = 'shop'` |
| `apps/shop/views.py` | `_broadcast(event_type, payload)` — единственная точка входа в channel layer |

---

## `_broadcast()` — паттерн

```python
# views.py
logger = logging.getLogger(__name__)

def _broadcast(event_type, payload):
    channel_layer = get_channel_layer()  # внутри функции — на старте может быть None
    if channel_layer is None:
        return
    try:
        async_to_sync(channel_layer.group_send)(
            WS_GROUP,
            {'type': 'shop.event', 'payload': {'type': event_type, **payload}},
        )
    except Exception as e:
        logger.warning('WebSocket broadcast failed (%s): %s', event_type, e)
```

**Критично:** `get_channel_layer()` вызывать внутри функции, не на уровне модуля — при импорте Redis ещё не инициализирован.

---

## 6 event types (полный список)

```python
_broadcast('purchase.created',  {'purchase': serialize_purchase(p)})
_broadcast('purchase.updated',  {'purchase': serialize_purchase(p)})
_broadcast('purchase.deleted',  {'purchase_id': pk, 'category_id': cat_pk})
_broadcast('category.created',  {'category': serialize_category(c)})
_broadcast('category.updated',  {'category': serialize_category(c)})
_broadcast('category.deleted',  {'category_id': pk})
```

`category_id` в `purchase.deleted` нужен клиенту чтобы найти DOM-элемент.

---

## Тесты WS (паттерн)

```python
# conftest.py — фикстура для изоляции channel layer
@pytest.fixture(autouse=True)
def use_in_memory_channel_layer(settings):
    from channels.layers import channel_layers
    from asgiref.sync import async_to_sync
    from channels.layers import InMemoryChannelLayer
    old = channel_layers.backends.pop('default', None)
    channel_layers.backends['default'] = InMemoryChannelLayer()
    yield
    channel_layers.backends.pop('default')
    if old:
        channel_layers.backends['default'] = old

# test_consumers.py
@pytest.mark.asyncio
async def test_receives_broadcast(user):
    communicator = WebsocketCommunicator(ShopConsumer.as_asgi(), '/ws/shop/')
    communicator.scope['user'] = user  # обойти AuthMiddlewareStack
    await communicator.connect()

    await get_channel_layer().group_send(WS_GROUP, {
        'type': 'shop.event',
        'payload': {'type': 'purchase.updated', 'purchase_id': 1},
    })

    msg = await communicator.receive_json_from(timeout=3)
    assert msg['type'] == 'purchase.updated'
    await communicator.disconnect()
```

---

## Запрещено

- **Не кешировать `channel_layer` на уровне модуля** — будет None при старте
- **Не писать логику в consumer** — consumer только пересылает, логика в views/models
- **Не использовать `re_path`** — только `path()` для WS URL
- **Не забывать `AuthMiddlewareStack`** — без него `scope['user']` всегда анонимный
