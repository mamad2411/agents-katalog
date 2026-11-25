---
name: moonshine-frontend-v4
description: Use when working on MoonShine v4 API mode, JWT authentication, OpenAPI generator, SDUI, Alpine.js events, JavaScript helpers, reactive fields, async UI updates, AsyncCallback, or custom Alpine.js components.
---

# MoonShine v4 -- Frontend (API, SDUI, JS & Alpine.js)

## Overview

MoonShine v4 provides a complete frontend interaction layer built on Alpine.js. It supports three modes of operation:

1. **Standard HTML** -- Server-rendered Blade views with Alpine.js reactivity (default).
2. **API mode** -- Add `Accept: application/json` to get JSON responses from CRUD routes, optionally with JWT authentication.
3. **SDUI (Server-Driven UI)** -- Request the component tree as a JSON structure for rendering in custom clients (mobile, SPA).

Alpine.js is bundled and initialized automatically. The global `MoonShine` JS class provides request helpers, UI toggles, and a callback registry for async response handling.

### Key Changes from v3

- **OpenAPI Generator** (`moonshine/oag`) is a new package for auto-generating API specs from resources.
- **AsyncCallback** system with `responseHandler`, `beforeRequest`, and `afterResponse` hooks is new.
- **JsonResponse** namespace changed to `MoonShine\Crud\JsonResponse` (was `MoonShine\Laravel\Http\Responses\MoonShineJsonResponse`).
- **JsEvent** enum moved to `MoonShine\Support\Enums\JsEvent`.
- New JS events: `TABLE_ROW_ADDED`, `TABLE_EMPTY_ROW_ADDED`, `TAB_ACTIVE`.

---

## 1. API Mode

Switch any MoonShine route to return JSON by including `Accept: application/json` in the request header.

### Available CRUD Routes

```
DELETE /admin/resource/{resourceUri}/crud                    -- Mass delete (ids[])
GET    /admin/resource/{resourceUri}/crud                    -- Listing
POST   /admin/resource/{resourceUri}/crud                    -- Create
PUT    /admin/resource/{resourceUri}/crud/{resourceItem}     -- Edit
DELETE /admin/resource/{resourceUri}/crud/{resourceItem}     -- Delete
```

When using MoonShine purely as an API backend, disable session middleware in `config/moonshine.php`:

```php
'middleware' => [
    // remove session-related middleware
],
```

> See [references/api-jwt.md](references/api-jwt.md) for full API setup, JWT configuration, and OpenAPI generation.

---

## 2. JWT Authentication

Install the JWT package for token-based API authentication:

```shell
composer require moonshine/jwt
php artisan vendor:publish --provider="MoonShine\JWT\Providers\JWTServiceProvider"
```

Add a base64-encoded secret to `.env`:

```ini
JWT_SECRET=YOUR_BASE64_SECRET_HERE
```

Configure middleware and auth pipeline in `config/moonshine.php`:

```php
use MoonShine\JWT\JWTAuthPipe;
use MoonShine\JWT\Http\Middleware\AuthenticateApi;

return [
    'middleware' => [
        // empty -- no session middleware for API mode
    ],
    'auth' => [
        // ...
        'middleware' => [
            AuthenticateApi::class,
        ],
        'pipelines' => [
            JWTAuthPipe::class,
        ],
    ],
    // ...
];
```

After successful authentication, use the returned token in subsequent requests:

```
Authorization: Bearer <token>
```

---

## 3. OpenAPI Generator (NEW in v4)

Generate OpenAPI specifications and documentation directly from MoonShine resources.

```shell
composer require moonshine/oag
php artisan vendor:publish --provider="MoonShine\OAG\Providers\OAGServiceProvider"
```

Generate the specification:

```shell
php artisan oag:generate
```

Specification files are output to the `resources` directory by default:

- `resources/oag.yaml`
- `resources/oag.json`

Documentation is served at `/docs`.

Config options (`config/oag.php`):

```php
return [
    'title' => 'Docs',
    'path' => realpath(resource_path('oag.yaml')),
    'route' => 'oag.json',
    'view' => 'oag::docs',
];
```

> See [references/api-jwt.md](references/api-jwt.md) for complete OpenAPI Generator setup details.

---

## 4. SDUI (Server-Driven UI)

Request any MoonShine page as a JSON component tree by adding the `X-MS-Structure: true` header. The response describes component types, states, attributes, and nested children -- suitable for mobile apps or custom SPA clients.

```
GET /admin/dashboard HTTP/1.1
X-MS-Structure: true
```

Response structure keys:

- `type` -- component type (e.g., "Dashboard", "Card", "Heading")
- `components` -- array of child components
- `states` -- component state data (title, content, level, etc.)
- `attributes` -- HTML attributes (class, id, data-* attributes)

### Customization Headers

| Header | Effect |
|---|---|
| `X-MS-Structure: true` | Return JSON component tree |
| `X-MS-Without-States: true` | Omit component states from response |
| `X-MS-Only-Layout: true` | Return only the layout structure |
| `X-MS-Without-Layout: true` | Return page content without layout wrapper |

> See [references/sdui.md](references/sdui.md) for full SDUI response structure, JSON examples, and all customization options.

---

## 5. Alpine.js Integration

### Creating Components

Generate a component scaffold:

```shell
php artisan moonshine:component MyComponent
```

In the Blade view, declare the Alpine.js component:

```html
<div x-data="myComponent"></div>
```

Register the component logic in a separate JS file (loaded via AssetManager):

```js
document.addEventListener("alpine:init", () => {
    Alpine.data("myComponent", () => ({
        init() {
            // component initialization
        },
    }))
})
```

> **Warning:** Alpine.js is already installed and running (`window.Alpine`). Do not re-initialize it or include Alpine.js again -- this will cause errors.

---

## 6. JS Events System

MoonShine uses custom DOM events dispatched via Alpine.js `$dispatch` to coordinate UI updates. Every event follows the pattern `event_name:component_name`.

### JsEvent Enum

All events are available via `MoonShine\Support\Enums\JsEvent`:

| Event Pattern | JsEvent Constant | Purpose |
|---|---|---|
| `fragment_updated:{name}` | `JsEvent::FRAGMENT_UPDATED` | Refresh a Fragment area |
| `table_updated:{name}` | `JsEvent::TABLE_UPDATED` | Refresh an async TableBuilder |
| `table_reindex:{name}` | `JsEvent::TABLE_REINDEX` | Reindex table fields after sort |
| `table_row_updated:{name}-{row-id}` | `JsEvent::TABLE_ROW_UPDATED` | Refresh a single table row |
| `table_row_added:{name}` | `JsEvent::TABLE_ROW_ADDED` | Append new cloned row (NEW) |
| `table_empty_row_added:{name}` | `JsEvent::TABLE_EMPTY_ROW_ADDED` | Append/prepend new row (NEW) |
| `cards_updated:{name}` | `JsEvent::CARDS_UPDATED` | Refresh a CardsBuilder |
| `form_reset:{name}` | `JsEvent::FORM_RESET` | Reset form fields |
| `form_submit:{name}` | `JsEvent::FORM_SUBMIT` | Trigger form submission |
| `modal_toggled:{name}` | `JsEvent::MODAL_TOGGLED` | Open/close a Modal |
| `off_canvas_toggled:{name}` | `JsEvent::OFF_CANVAS_TOGGLED` | Open/close an OffCanvas |
| `popover_toggled:{name}` | `JsEvent::POPOVER_TOGGLED` | Open/close a Popover |
| `toast:{name}` | `JsEvent::TOAST` | Trigger a Toast notification |
| `show_when_refresh:{name}` | `JsEvent::SHOW_WHEN_REFRESH` | Re-evaluate showWhen conditions |
| `tab_active:{name}` | `JsEvent::TAB_ACTIVE` | Activate a tab (NEW) |

### Dispatching Events from PHP

```php
use MoonShine\Support\AlpineJs;
use MoonShine\Support\Enums\JsEvent;

// Simple event string
AlpineJs::event(JsEvent::TABLE_UPDATED, 'index')
// => "table_updated:index"

// Event with parameters
AlpineJs::event(JsEvent::TABLE_UPDATED, 'index', ['var' => 'foo'])
// => "table_updated:index|var=foo"
```

### Dispatching Events from JavaScript

```js
// Native DOM
document.addEventListener("DOMContentLoaded", () => {
    dispatchEvent(new CustomEvent("modal_toggled:my-modal"))
})

// Alpine.js $dispatch
this.$dispatch('modal_toggled:my-modal')
```

> See [references/js-events-alpine.md](references/js-events-alpine.md) for the complete events reference.

---

## 7. Response Events

Return events from a controller or resource method so they fire after the response is processed:

```php
use MoonShine\Crud\JsonResponse;
use MoonShine\Support\AlpineJs;
use MoonShine\Support\Enums\JsEvent;

return JsonResponse::make()
    ->events([
        AlpineJs::event(JsEvent::TABLE_UPDATED, 'index'),
    ]);
```

> **v4 change:** The namespace is now `MoonShine\Crud\JsonResponse` (was `MoonShine\Laravel\Http\Responses\MoonShineJsonResponse` in v3).

---

## 8. Blade Directives

### @defineEvent

Declare an event listener in HTML:

```blade
<div x-data="myComponent"
    @defineEvent('table-updated', 'index', 'asyncRequest')
>
</div>
{{-- Generates: @table-updated-index.window="asyncRequest" --}}
```

Signature:

```php
@defineEvent(string|JsEvent $event, ?string $name = null, ?string $call = null, array $params = [])
```

### @defineEventWhen

Conditionally declare an event listener:

```blade
<div x-data="myComponent"
    @defineEventWhen($isAsync, 'table-updated', 'index', 'asyncRequest')
>
</div>
```

Signature:

```php
@defineEventWhen(mixed $condition, string|JsEvent $event, ?string $name = null, ?string $call = null, array $params = [])
```

---

## 9. AlpineJs Helper

### AlpineJs::event()

Build event strings for use in PHP:

```php
use MoonShine\Support\AlpineJs;
use MoonShine\Support\Enums\JsEvent;

AlpineJs::event(JsEvent::TABLE_UPDATED, 'index', ['var' => 'foo'])
// => "table_updated:index|var=foo"
```

### AlpineJs::eventBlade()

Build Blade attribute strings for `x-on` directives:

```php
AlpineJs::eventBlade(JsEvent::FORM_RESET, 'main-form')
// => "@form-reset-main-form.window"

// Usage in customAttributes:
FormBuilder::make('/crud/update')
    ->name('main-form')
    ->customAttributes([
        AlpineJs::eventBlade(JsEvent::FORM_RESET, 'main-form') => 'formReset',
    ])
```

---

## 10. Global MoonShine JS Class

The `window.MoonShine` object is available after the `moonshine:init` event fires.

### MoonShine.request()

```js
MoonShine.request(ctx, '/url', method = 'get', body = {}, headers = {}, data = {})
```

### MoonShine.ui.toast()

```js
MoonShine.ui.toast('Hello world', 'success')
```

### MoonShine.ui.toggleModal()

```js
MoonShine.ui.toggleModal('modal-name')
```

### MoonShine.ui.toggleOffCanvas()

```js
MoonShine.ui.toggleOffCanvas('canvas-name')
```

### MoonShine.iterable.sortable()

```js
MoonShine.iterable.sortable(container, url, group, events, attributes = { handle: '.handle' }, callback)
```

### MoonShine.iterable.reindex()

```js
MoonShine.iterable.reindex(container, itemSelector = '.item')
```

---

## 11. AsyncCallback (NEW in v4)

Components with async behavior (`ActionButton`, `FormBuilder`, `TableBuilder`, fields implementing `HasAsyncContract`) support `AsyncCallback` for hooking into the request lifecycle.

### PHP Setup

```php
use MoonShine\Support\DTOs\AsyncCallback;

ActionButton::make('Do Something')
    ->method('myMethod', callback: AsyncCallback::with(
        beforeRequest: 'myBeforeRequest',
        responseHandler: 'myResponseHandler',
        afterResponse: 'myAfterResponse',
    ))
```

### JS Registration

```js
document.addEventListener("moonshine:init", () => {
    // Before request -- receives element and Alpine component
    MoonShine.onCallback('myBeforeRequest', function(element, component) {
        console.log('Before request', element, component)
    })

    // Full response handler -- replaces default behavior
    MoonShine.onCallback('myResponseHandler', function(response, element, events, component) {
        console.log('Custom handler', response)
    })

    // After successful default processing
    MoonShine.onCallback('myAfterResponse', function(data, messageType, component) {
        console.log('After response', data, messageType)
    })
})
```

> **Note:** If you specify `responseHandler`, it takes full control of response handling and `afterResponse` will not be called.

> See [references/js-events-alpine.md](references/js-events-alpine.md) for complete AsyncCallback parameter details.

---

## 12. Reactive Fields

MoonShine supports reactive form fields that send their values to the server on change and receive updated field HTML in return. When a reactive field value changes:

1. A POST request is sent to `reactiveUrl` with `{ _component_name, values }`.
2. The server returns `{ fields: { column: html }, values: { column: value } }`.
3. The field wrapper HTML is replaced and focus is preserved on text inputs.

---

## 13. Fragment-Based Partial Updates

Wrap components in a `Fragment` for partial page updates without full reload:

```php
use MoonShine\Support\AlpineJs;
use MoonShine\Support\Enums\JsEvent;
use MoonShine\Crud\Components\Fragment;

Fragment::make([
    TableBuilder::make()->fields($fields)->items($items)->name('data-table')
])->name('data-fragment'),

ActionButton::make('Reload')
    ->dispatchEvent(AlpineJs::event(JsEvent::FRAGMENT_UPDATED, 'data-fragment'))
```

---

## Cross-References

- **moonshine-security-v4** -- JWT auth configuration, auth pipelines, guard setup, and the `AuthenticateApi` middleware.
- **moonshine-components-v4** -- Async components (FormBuilder, TableBuilder, Fragment), event wiring, and the full component API.
- **moonshine-resources-v4** -- API endpoints for resources, CRUD routes, `JsonResponse` modifiers, and resource method handlers.
- **moonshine-appearance-v4** -- Asset management for custom JS/CSS files.

## Reference Files

- `references/api-jwt.md` -- Full API mode setup, JWT package configuration, and OpenAPI Generator.
- `references/sdui.md` -- SDUI concept, response structure, headers, component types, and state management.
- `references/js-events-alpine.md` -- JavaScript events reference, Alpine.js integration, AsyncCallback details, and global MoonShine class.
