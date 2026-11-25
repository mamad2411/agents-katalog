---
name: prestashop_js_events
description: Guía y componentes para rastrear, interceptar y reaccionar a eventos de JavaScript en el Core de PrestaShop (1.7, 8 y 9).
---

# Skill: PrestaShop JS Events Tracker

Este skill proporciona el conocimiento necesario para trabajar con el sistema de eventos de JavaScript nativo de PrestaShop, permitiendo la trazabilidad y auditoría de acciones del usuario en el frontend.

## Eventos Core Principales

Basado en la documentación oficial de PrestaShop:

| Evento | Descripción | Datos Disponibles |
| :--- | :--- | :--- |
| `updateCart` | Se dispara antes de actualizar el carrito. | `reason` |
| `updatedCart` | Se dispara tras una actualización exitosa del carrito. | `resp`, `reason` |
| `clickQuickView` | Al hacer clic en vista rápida. | `dataset` |
| `handleError` | Error general en el core de JS. | `eventType`, `resp` |
| `updateProductList` | Antes de refrescar lista de productos (filtros). | - |
| `updatedProductList` | Tras refrescar lista de productos. | - |
| `editAddress` | Al iniciar edición de dirección. | `idAddress` |

## Implementación de Interceptor Genérico

Para capturar todos los eventos y enviarlos a un logger:

```javascript
/**
 * Listener global de eventos PrestaShop
 */
$(document).ready(() => {
    if (typeof prestashop !== 'undefined') {
        const eventsToTrack = [
            'updateCart', 
            'updatedCart', 
            'clickQuickView', 
            'handleError',
            'updateProductList',
            'updatedProductList'
        ];

        eventsToTrack.forEach(eventName => {
            prestashop.on(eventName, (params) => {
                console.log(`[PS_EVENT] ${eventName}`, params);
                // Aquí se realizaría la llamada AJAX al servidor
                sendEventToServer(eventName, params);
            });
        });
    }
});

function sendEventToServer(event, details) {
    $.ajax({
        type: 'POST',
        url: prestashop.urls.base_url + 'module/ecom_log_events/logger',
        data: {
            ajax: true,
            action: 'logEvent',
            eventName: event,
            details: JSON.stringify(details),
            token: typeof prestashop_log_token !== 'undefined' ? prestashop_log_token : ''
        }
    });
}
```

## Trazabilidad y Análisis de Fallos

Para eventos como `updatedCart`, si la respuesta no contiene `success` o está vacía, se debe marcar como fallo de trazabilidad.

```javascript
prestashop.on('updatedCart', (event) => {
    if (!event.resp || Object.keys(event.resp).length === 0) {
        // Trazabilidad de fallo: El servidor no respondió correctamente
        sendEventToServer('ERROR_NO_RESPONSE', { originalEvent: 'updatedCart' });
    }
});
```

## Referencias
- [Documentación Oficial de Eventos JS](https://devdocs.prestashop-project.org/9/themes/reference/javascript-events/)
