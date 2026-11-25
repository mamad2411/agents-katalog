---
name: prestashop-js-routing
description: Skill for using the PrestaShop Javascript Router to generate admin links dynamically in PS 8 and 9.
---

# PrestaShop Javascript Routing Skill

This skill explains how to use the built-in Javascript Router component in the PrestaShop Back Office to generate URLs for AJAX requests or navigation dynamically.

## 1. Technical Guide

### Initializing the Router
Before using the router, you must ensure it is initialized.

```javascript
$(() => {
  if (typeof window.prestashop.component !== 'undefined') {
    window.prestashop.component.initComponents(['Router']);
  }
});
```

### Generating a Route
You can use the `generate` method of the router instance. The route name must be a Symfony route name.

```javascript
const route = window.prestashop.instance.router.generate('admin_customers_search');
```

### Passing Parameters
```javascript
const route = window.prestashop.instance.router.generate('admin_product_form', {id: 123});
```

## 2. Professional Development Guide

### Fallback Mechanism
For older PrestaShop versions or if the component fails, always provide a fallback or check for existence.

```javascript
let route;
if (window.prestashop?.instance?.router) {
    route = window.prestashop.instance.router.generate('my_route');
} else {
    // Legacy way or manual string construction
    route = 'admin-dev/index.php/sell/customers/search'; 
}
```

### Exposing Module Routes to JS
To make your module's Symfony routes available in Javascript, you might need to tag them or ensure the router component is aware of them. In PS 8/9, most admin routes registered in `routes.yml` are automatically available if the component is loaded.

## 3. User Guide

### Debugging in Console
You can test routes directly in the browser console:
```javascript
prestashop.instance.router.generate('admin_orders_index')
```

## Rules & Best Practices
- **Token Handling**: The router often handles the `_token` automatically if configured.
- **Dependency**: Ensure the script is loaded in the Back Office via `hookActionAdminControllerSetMedia`.
- **Performance**: Don't initialize components multiple times.
